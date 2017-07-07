#
# Part of p5: A Python package based on Processing
# Copyright (C) 2017 Abhik Pal
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
"""The OpenGL renderer for p5."""

from ctypes import *
import builtins
import math

from pyglet.gl import *

from . import support
from ..tmp import Matrix4
from .shader import Shader
from .shader import vertex_default, fragment_default
from .shader import screen_texture_vert, screen_texture_frag

default_shader = None

transform_matrix = Matrix4()
modelview_matrix = Matrix4()
projection_matrix = Matrix4()

viewport = None

background_color = (0.8, 0.8, 0.8, 1.0)
fill_color = (1.0, 1.0, 1.0, 1.0)
stroke_color = (0, 0, 0, 1.0)
fill_enabled = True
stroke_enabled = True

context = None

fbo_support = False
frame_buffer = None
back_texture = None
front_texture = None
screen_shader = None

geometry_cache = {}

# screen quad (SQ) vertex and texture data
_SQ_vert_coords = [ -1, 1, 1, 1, 1, -1, -1, -1]
_SQ_vert_data = (GLfloat * len(_SQ_vert_coords))(*_SQ_vert_coords)

_SQ_tex_coords = [ 0, 1, 1, 1, 1, 0, 0, 0 ]
_SQ_tex_data = (GLfloat * len(_SQ_tex_coords))(*_SQ_tex_coords)


class FrameBuffer:
    """Encapsulates an OpenGL FrameBuffer."""
    def __init__(self):
        self._id = Gluint()
        glGenFramebuffersEXT(1, pointer(self._id))

        self._check_completion_status()

    def _check_completion_status(self):
        """Check the completion status of the framebuffer.

        :raises Exception: When the frame buffer is incomplete.
        """
        status = glCheckFramebufferStatusEXT(GL_FRAMEBUFFER_EXT)
        if status != GL_FRAMEBUFFER_COMPLETE_EXT:
            msg = "ERR {}: FrameBuffer could not be created.".format(status)
            raise Exception(msg)

    def activate(self):
        """Activate the current framebuffer."""
        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, self._id)

    def deactivate(self):
        """Deactivate the current framebuffer."""
        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, self._id)

    def attach_texture(self, texture):
        self.activate()
        glFramebufferTexture2DEXT(GL_FRAMEBUFFER_EXT,
                                  GL_COLOR_ATTACHMENT0_EXT,
                                  GL_TEXTURE_2D, texture.id, 0)
        self.deactivate()

    def delete(self):
        """Delete the current frame buffer."""
        glDeleteFramebuffersEXT(self._id)

    def __del__(self):
        self.delete()


class FrameTexture:
    """A texture to be used with the FrameBuffer"""
    def __init__(self, width, height):
        self._id = Gluint()
        glGenTextures(1, pointer(self._id))

        self.activate()

        _blank_texture = (GLubyte * (width * height * 4))()
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0,
                     GL_RGBA, GL_UNSIGNED_BYTE, _blank_texture)
        self._init_texture()

        self.deactivate()

    def _init_texture(self):
        # Initialize the texture bu uniformly filling with the
        # background color.
        pass

    @property
    def id(self):
        return self._id

    def activate(self):
        """Activate the current texture."""
        glBindTexture(GL_TEXTURE_2D, self._id)

    def deactivate(self):
        """Deactivate the current texture."""
        glBindTexture(GL_TEXTURE_2D, 0)


def initialize(window_context):
    """Initialize the OpenGL renderer.

    For an OpenGL based renderer this sets up the viewport and creates
    the shader program.

    :param window_context: The OpenGL context associated with this renderer.
    :type window_context: pyglet.gl.Context

    """
    global context
    global vertex_buffer
    global element_buffer
    global default_shader
    global screen_shader

    global fbo_support

    context = window_context
    gl_version = context.get_info().get_version()[:3]
    fbo_support = support.has_fbo(context)

    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)

    screen_shader = Shader(screen_texture_vert, screen_texture_frag, gl_version)
    screen_shader.activate()
    screen_shader.add_uniform('texMap', 'int')
    screen_shader.add_attribute('position', '2f')
    screen_shader.add_attribute('tex_coord', '2f')
    screen_shader.deactivate()

    default_shader = Shader(vertex_default, fragment_default, gl_version)

    default_shader.activate()

    default_shader.add_uniform('fill_color', 'vec4')
    default_shader.add_uniform('projection', 'mat4')
    default_shader.add_uniform('modelview', 'mat4')
    default_shader.add_uniform('transform', 'mat4')

    default_shader.add_attribute('position', '3f')

    reset_view()
    clear()

def cleanup():
    """Run the clean-up routine for the renderer.

    This method is called when all drawing has been completed and the
    program is about to exit.

    """
    default_shader.delete()
    for shape_hash, shape_buffers in geometry_cache.items():
        glDeleteBuffers(1, shape_buffers['vertex_buffer'])
        glDeleteBuffers(1, shape_buffers['edge_buffer'])
        glDeleteBuffers(1, shape_buffers['face_buffer'])


def clear():
    """Clear the renderer background."""
    glClearColor(*background_color)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

def reset_view():
    """Reset the view of the renderer."""
    global transform_matrix
    global modelview_matrix
    global projection_matrix
    global viewport

    viewport = (0, 0, builtins.width, builtins.height)
    glViewport(*viewport)

    cz = (builtins.height / 2) / math.tan(math.radians(30))
    projection = Matrix4.new_perspective(
        math.radians(60),
        builtins.width / builtins.height,
        0.1 * cz,
        10 * cz
    )
    view = Matrix4().translate(-builtins.width/2, builtins.height/2, -cz)
    view.scale(1, -1, 1)

    transform_matrix = Matrix4()
    modelview_matrix = view
    projection_matrix =  projection
    default_shader.update_uniform('transform', transform_matrix)
    default_shader.update_uniform('modelview', modelview_matrix)
    default_shader.update_uniform('projection', projection_matrix)

def pre_render():
    """Initialize things for a draw call.

    The pre_render is the first thing that is called when we want to
    refresh/redraw the contents of the screen on each draw call.

    """
    global transform_matrix
    transform_matrix = Matrix4()

    glViewport(*viewport)

    default_shader.activate()

    default_shader.update_uniform('transform', transform_matrix)
    default_shader.update_uniform('modelview', modelview_matrix)
    default_shader.update_uniform('projection', projection_matrix)

def post_render():
    """Cleanup things after a draw call.

    The post_render is called once all the rendering is done for the
    last draw call.

    """
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
    default_shader.deactivate()

def flatten(vertex_list):
    """Flatten a vertex list

    An unflattened list of vertices is a list of tuples [(x1, y2, z1),
    (x2, y2, z2), ...] where as a list of flattened vertices doesn't
    have any tuples [x1, y1, z2, x2, y2, z2, ...]

    :param vertex_list: list of vertices to be flattened.
    :type vertex_list: list of 3-tuples

    :returns: a flattened vertex_list
    :rtype: list

    """
    return [vi for vertex in vertex_list for vi in vertex]

def tessellate(shape):
    """Generate vertices from Shape data.

    :param shape: The input shape.
    :type shape: Shape

    :returns: The tesselated shape
    :rtype: Shape

    """
    if shape.vertices is None:
        shape.tessellate()
    if shape.kind in ['POLY', 'ELLIPSE', 'PATH']:
       shape.compute_edges()
    if shape.kind is not 'PATH':
       shape.compute_faces()
    return shape

def render(shape):
    """Use the renderer to render a Shape.

    :param shape: The shape to be rendered.
    :type shape: Shape
    """
    default_shader.update_uniform('transform', transform_matrix)

    shape_hash = hash(shape)
    if shape_hash not in geometry_cache:
        vertex_buffer = GLuint()
        glGenBuffers(1, pointer(vertex_buffer))

        edge_buffer = GLuint()
        glGenBuffers(1, pointer(edge_buffer))

        face_buffer = GLuint()
        glGenBuffers(1, pointer(face_buffer))

        tessellated_shape = tessellate(shape)

        vertices = flatten(tessellated_shape.vertices)
        num_vertices = len(vertices)
        vertices_typed = (GLfloat * num_vertices)(*vertices)

        glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
        glBufferData(
            GL_ARRAY_BUFFER,
            sizeof(vertices_typed),
            vertices_typed,
            GL_STATIC_DRAW
        )
        glBindBuffer(GL_ARRAY_BUFFER, 0)

        edges = flatten(tessellated_shape.edges)
        num_edges = len(edges)
        edges_typed = (GLuint * num_edges)(*edges)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, edge_buffer)
        glBufferData(
            GL_ELEMENT_ARRAY_BUFFER,
            sizeof(edges_typed),
            edges_typed,
            GL_STATIC_DRAW
        )
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

        if shape.kind not in  ['PATH', 'POINT']:
            faces = flatten(tessellated_shape.faces)
            num_faces = len(faces)
            faces_typed = (GLuint * num_faces)(*faces)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, face_buffer)
            glBufferData(
                GL_ELEMENT_ARRAY_BUFFER,
                sizeof(faces_typed),
                faces_typed,
                GL_STATIC_DRAW
            )
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
        else:
            faces = []
            num_faces = 0

        geometry_cache[shape_hash] = {
            'vertex_buffer': vertex_buffer,
            'edge_buffer': edge_buffer,
            'face_buffer': face_buffer,

            'num_vertices': num_vertices,
            'num_edges': num_edges,
            'num_faces': num_faces
        }
    else:
        vertex_buffer = geometry_cache[shape_hash]['vertex_buffer']
        edge_buffer = geometry_cache[shape_hash]['edge_buffer']
        face_buffer = geometry_cache[shape_hash]['face_buffer']

        num_vertices = geometry_cache[shape_hash]['num_vertices']
        num_edges = geometry_cache[shape_hash]['num_edges']
        num_faces = geometry_cache[shape_hash]['num_faces']

    default_shader.update_attribute('position', vertex_buffer)

    if fill_enabled and (shape.kind not in ['POINT', 'PATH']):
        default_shader.update_uniform('fill_color', fill_color)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, face_buffer)
        glDrawElements(
            GL_TRIANGLES,
            num_faces,
            GL_UNSIGNED_INT,
            0
        )
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

    if stroke_enabled:
        default_shader.update_uniform('fill_color', stroke_color)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, edge_buffer)
        if shape.kind == 'POINT':
            glDrawElements(GL_POINTS, num_edges, GL_UNSIGNED_INT, 0)
        elif shape.kind == 'PATH':
            glDrawElements(GL_LINE_STRIP, num_edges, GL_UNSIGNED_INT, 0)
        else:
            glDrawElements(GL_LINE_LOOP, num_edges, GL_UNSIGNED_INT, 0)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

def test_render():
    """Render the renderer's default test drawing."""
    global background_color
    global fill_color

    class Triangle:
        def __init__(self):
            self.faces = [(0, 1, 2)]
            self.kind = 'POLY'
            self.vertices = [
                (450, 150, 0),
                (600, 450, 0),
                (750, 150, 0)
            ]

    class Square:
        def __init__(self):
            self.faces = [(0, 1, 2), (2, 3, 0)]
            self.kind = 'POLY'
            self.vertices = [
                (50, 150, 0),
                (50, 450, 0),
                (350, 450, 0),
                (350, 150, 0)
            ]

    background_color = (1.0, 1.0, 1.0, 1.0)
    clear()

    fill_color = (0.8, 0.8, 0.4, 1.0)
    render(Triangle())

    fill_color = (0.4, 0.4, 0.8, 1.0)
    render(Square())

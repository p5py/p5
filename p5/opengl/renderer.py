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

from pyglet import gl

from ..tmp import Matrix4
from .shader import Shader
from .shader import vertex_default, fragment_default

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

geometry_cache = {}


def initialize(window_context):
    """Initialize the OpenGL renderer.

    For an OpenGL based renderer this sets up the viewport and creates
    the shader program.

    :param window_context: The OpenGL context associated with this renderer.
    :type window_context: pyglet.gl.Context

    """
    global context
    global default_shader

    context = window_context
    gl_version = context.get_info().get_version()[:3]

    gl.glEnable(gl.GL_DEPTH_TEST)
    gl.glDepthFunc(gl.GL_LEQUAL)

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
        gl.glDeleteBuffers(1, shape_buffers['vertex_buffer'])
        gl.glDeleteBuffers(1, shape_buffers['edge_buffer'])
        gl.glDeleteBuffers(1, shape_buffers['face_buffer'])


def clear():
    """Clear the renderer background."""
    gl.glClearColor(*background_color)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

def reset_view():
    """Reset the view of the renderer."""
    global transform_matrix
    global modelview_matrix
    global projection_matrix
    global viewport

    viewport = (0, 0, builtins.width, builtins.height)
    gl.glViewport(*viewport)

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

    clear()
    gl.glViewport(*viewport)

    default_shader.activate()

    default_shader.update_uniform('transform', transform_matrix)
    default_shader.update_uniform('modelview', modelview_matrix)
    default_shader.update_uniform('projection', projection_matrix)

def post_render():
    """Cleanup things after a draw call.

    The post_render is called once all the rendering is done for the
    last draw call.

    """
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
    gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, 0)
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
        vertex_buffer = gl.GLuint()
        gl.glGenBuffers(1, pointer(vertex_buffer))

        edge_buffer = gl.GLuint()
        gl.glGenBuffers(1, pointer(edge_buffer))

        face_buffer = gl.GLuint()
        gl.glGenBuffers(1, pointer(face_buffer))

        tessellated_shape = tessellate(shape)

        vertices = flatten(tessellated_shape.vertices)
        num_vertices = len(vertices)
        vertices_typed = (gl.GLfloat * num_vertices)(*vertices)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vertex_buffer)
        gl.glBufferData(
            gl.GL_ARRAY_BUFFER,
            sizeof(vertices_typed),
            vertices_typed,
            gl.GL_STATIC_DRAW
        )
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)

        edges = flatten(tessellated_shape.edges)
        num_edges = len(edges)
        edges_typed = (gl.GLuint * num_edges)(*edges)
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, edge_buffer)
        gl.glBufferData(
            gl.GL_ELEMENT_ARRAY_BUFFER,
            sizeof(edges_typed),
            edges_typed,
            gl.GL_STATIC_DRAW
        )
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, 0)

        if shape.kind not in  ['PATH', 'POINT']:
            faces = flatten(tessellated_shape.faces)
            num_faces = len(faces)
            faces_typed = (gl.GLuint * num_faces)(*faces)
            gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, face_buffer)
            gl.glBufferData(
                gl.GL_ELEMENT_ARRAY_BUFFER,
                sizeof(faces_typed),
                faces_typed,
                gl.GL_STATIC_DRAW
            )
            gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, 0)
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

        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, face_buffer)
        gl.glDrawElements(
            gl.GL_TRIANGLES,
            num_faces,
            gl.GL_UNSIGNED_INT,
            0
        )
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, 0)

    if stroke_enabled:
        default_shader.update_uniform('fill_color', stroke_color)

        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, edge_buffer)
        if shape.kind == 'POINT':
            gl.glDrawElements(gl.GL_POINTS, num_edges, gl.GL_UNSIGNED_INT, 0)
        elif shape.kind == 'PATH':
            gl.glDrawElements(gl.GL_LINE_STRIP, num_edges, gl.GL_UNSIGNED_INT, 0)
        else:
            gl.glDrawElements(gl.GL_LINE_LOOP, num_edges, gl.GL_UNSIGNED_INT, 0)
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, 0)


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

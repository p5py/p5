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

import builtins
import ctypes as ct
from contextlib import contextmanager
import math

import numpy as np
from pyglet import gl

from .gloo import (
    VertexBuffer,
    Texture,
    FrameBuffer,
)
from .shader import (
    Shader,
    vertex_default, fragment_default,
    texture_vertex_default, texture_fragment_default
)
from .support import has_fbo
from ..pmath import Matrix4


##
## Renderer globals.
##
## TODO (2017-08-01 abhikpal):
##
## - Higher level objects *SHOULD NOT* have direct access to internal
##   state variables.
##

## Renderer Globals: USEFUL CONSTANTS
COLOR_WHITE = (1, 1, 1, 1)
COLOR_BLACK = (0, 0, 0, 1)
COLOR_DEFAULT_BG = (0.8, 0.8, 0.8, 1.0)

MATRIX_IDENTITY = Matrix4()

## Renderer Globals: STYLE/MATERIAL PROPERTIES
##
background_color = COLOR_DEFAULT_BG

fill_color = COLOR_WHITE
fill_image = None
fill_enabled = True
fill_image_enabled = False

tint_color = COLOR_WHITE
tint_enabled = True

stroke_color = COLOR_BLACK
stroke_enabled = True

## Renderer Globals
## VIEW MATRICES, ETC
##
viewport = None

transform_matrix = Matrix4()
modelview_matrix = Matrix4()
projection_matrix = Matrix4()

## Renderer Globals: OPEN GL SPECIFIC
##
context = None

default_shader = None
texture_shader = None

geometry_cache = {}
texture_cache = {}

## Renderer Globals: FRAME BUFFERS
##
frame_buffer_support = False
frame_buffer = None

front_frame_tex = None
back_frame_tex = None

frame_vertices = None
frame_texcoords = None
frame_elements = None


## RENDERER UTILITY FUNCTIONS
##
## Mostly for internal user. Ideally, higher level components *SHOULD
## NOT* need these.
##
def add_common_uniforms(shader):
    """Add a default set of uniforms to the shader.
    """
    shader.add_uniform('projection', 'mat4')
    shader.add_uniform('modelview', 'mat4')
    shader.add_uniform('transform', 'mat4')
    shader.add_uniform('fill_color', 'vec4')

def add_texture(image):
    """Add the given image as a texture to the renderer.
    """
    global fill_image
    global fill_image_enabled
    fill_image_enabled = True
    image_hash = hash(image)
    if image_hash not in texture_cache:
        tex = Texture(image.width, image.height)
        tex.data = bytes(image)
        texture_cache[image_hash] = tex
    else:
        tex = texture_cache[image_hash]

    fill_image = tex

def draw_frame_texture(texture):
    """Draw the given texture to the frame.
    """
    texture_shader.activate()
    texture_shader.update_uniform('transform', MATRIX_IDENTITY)
    texture_shader.update_uniform('fill_color', COLOR_WHITE)
    texture.activate()
    texture_shader.update_attribute('texcoord', frame_texcoords.id)
    texture_shader.update_attribute('position', frame_vertices.id)
    frame_vertices.activate()
    frame_elements.draw('TRIANGLES')

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

def transform_points(points):
    """Transform the given list of points using the transformation matrix.

    :param points: List of points to be transformed.
    :type points: a list of 3-tuples

    :returns: a numpy array with the transformed points.
    :rtype: np.ndarray

    """
    # The Matrix4 internally stores data in the following format:
    #
    # a b c d
    # e f g h
    # i j k l
    # m n o p
    #
    transform = np.array([
        [transform_matrix.a, transform_matrix.b, transform_matrix.c],
        [transform_matrix.e, transform_matrix.f, transform_matrix.g],
        [transform_matrix.i, transform_matrix.j, transform_matrix.k]
    ])
    points = np.array(points, dtype=np.float32)
    return points.dot(transform)

## RENDERER SETUP FUNCTIONS.
##
## These don't handle shape rendering directly and are used for setup
## tasks like initialization, cleanup before exiting, resetting views,
## clearing the screen, etc.
##

def initialize(window_context):
    """Initialize the OpenGL renderer.

    For an OpenGL based renderer this sets up the viewport and creates
    the shader program.

    :param window_context: The OpenGL context associated with this renderer.
    :type window_context: pyglet.gl.Context

    """
    global context
    global default_shader
    global texture_shader
    global frame_buffer
    global frame_buffer_support

    context = window_context
    gl_version = context.get_info().get_version()[:3]

    frame_buffer_support = has_fbo(context)
    if frame_buffer_support:
        frame_buffer = FrameBuffer()

    gl.glEnable(gl.GL_BLEND)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

    gl.glEnable(gl.GL_DEPTH_TEST)
    gl.glDepthFunc(gl.GL_LEQUAL)

    default_shader = Shader(vertex_default, fragment_default, gl_version)
    texture_shader = Shader(texture_vertex_default,
                            texture_fragment_default, gl_version)

    texture_shader.activate()
    add_common_uniforms(texture_shader)
    texture_shader.add_uniform('texture', 'int')
    texture_shader.add_attribute('position', '3f')
    texture_shader.add_attribute('texcoord', '2f')

    default_shader.activate()
    add_common_uniforms(default_shader)
    default_shader.add_attribute('position', '3f')

    reset_view()

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

    global front_frame_tex
    global back_frame_tex

    global frame_vertices
    global frame_texcoords
    global frame_elements

    viewport = (0, 0, builtins.width, builtins.height)
    gl.glViewport(*viewport)

    cz = (builtins.height / 2) / math.tan(math.radians(30))
    projection_matrix = Matrix4.new_perspective(
        math.radians(60),
        builtins.width / builtins.height,
        0.1 * cz,
        10 * cz
    )

    modelview_matrix = Matrix4()
    modelview_matrix.translate(-builtins.width/2, builtins.height/2, -cz)
    modelview_matrix.scale(1, -1, 1)

    transform_matrix = Matrix4()

    texture_shader.activate()
    texture_shader.update_uniform('transform', transform_matrix)
    texture_shader.update_uniform('modelview', modelview_matrix)
    texture_shader.update_uniform('projection', projection_matrix)

    default_shader.activate()
    default_shader.update_uniform('transform', transform_matrix)
    default_shader.update_uniform('modelview', modelview_matrix)
    default_shader.update_uniform('projection', projection_matrix)

    if frame_buffer_support:
        front_frame_tex = Texture(builtins.width, builtins.height, reset=True)
        back_frame_tex = Texture(builtins.width, builtins.height, reset=True)
        frame_vertices = VertexBuffer('float',
                                      data=[0, 0, 0,
                                            builtins.width, 0, 0,
                                            builtins.width, builtins.height, 0,
                                            0, builtins.height, 0])
        frame_texcoords = VertexBuffer('float',
                                       data=[0, 1,
                                             1, 1,
                                             1, 0,
                                             0, 0])
        frame_elements = VertexBuffer('uint',
                                      data=[0, 1, 2, 0, 2, 3],
                                      buffer_type='elem')

def cleanup():
    """Run the clean-up routine for the renderer.

    This method is called when all drawing has been completed and the
    program is about to exit.

    """
    default_shader.delete()
    texture_shader.delete()
    for shape_hash, shape_buffers in geometry_cache.items():
        shape_buffers['vertex_buffer'].delete()
        shape_buffers['edge_buffer'].delete()
        shape_buffers['face_buffer'].delete()
    for texture_hash, texture in texture_cache:
        texture.delete()
    if frame_buffer_support:
        frame_vertices.delete()
        frame_texcoords.delete()
        frame_elements.delete()
        frame_buffer.delete()


## RENDERING FUNTIONS + HELPERS
##
## These are responsible for actually rendring things to the screen.
## For some draw call the methods should be called as follows:
##
##    with draw_loop():
##        # multiple calls to render()
##

@contextmanager
def draw_loop():
    """The main draw loop context manager.
    """
    pre_render()
    try:
        yield
    finally:
        post_render()

def pre_render():
    """Initialize things for a draw call.

    The pre_render is the first thing that is called when we want to
    refresh/redraw the contents of the screen on each draw call.

    """
    global transform_matrix
    transform_matrix = Matrix4()

    gl.glViewport(*viewport)

    texture_shader.activate()
    texture_shader.update_uniform('transform', transform_matrix)
    texture_shader.update_uniform('modelview', modelview_matrix)
    texture_shader.update_uniform('projection', projection_matrix)
    texture_shader.deactivate()

    default_shader.activate()
    default_shader.update_uniform('transform', transform_matrix)
    default_shader.update_uniform('modelview', modelview_matrix)
    default_shader.update_uniform('projection', projection_matrix)
    default_shader.deactivate()

    if frame_buffer_support:
        # 1. Turn on blending and depth test as they get disabled at
        #    the end of the draw loop.
        #
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

        # 2. In the main draw loop, we will render to the back buffer and
        #    then blit it on the screen at the end of the draw loop. So,
        #    attach the back buffer texture to the frame buffer to render
        #    everything to it.
        #
        frame_buffer.attach_texture(back_frame_tex)

        # 3. Activate the frame buffer.
        #
        frame_buffer.activate()

        # 4. If this is the first frame of the sketch, we don't have an
        #    old buffer yet, so we just clear the screen. If we are not on
        #    the first frame, we need to render the contents of the last
        #    draw loop (stored in the front frame texture.)
        #
        if not builtins.frame_count > 0:
            clear()
        else:
            draw_frame_texture(front_frame_tex)
    else:
        clear()

def post_render():
    """Cleanup things after a draw call.

    The post_render is called once all the rendering is done for the
    last draw call.

    """
    global front_frame_tex
    global back_frame_tex

    if frame_buffer_support:
        # 1. We need to stop rendering to the framebuffer; deactivate the
        #    frame buffer.
        #
        frame_buffer.deactivate()

        # 2. clear the screen (depth buffer, color buffer, everything.)
        #
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        # 3. We need to draw the frame_buffer without blending; disable blending.
        #
        gl.glDisable(gl.GL_BLEND)
        gl.glDisable(gl.GL_DEPTH_TEST)

        # 4. draw the back texture
        draw_frame_texture(back_frame_tex)

        # 5. swap the front and the back textures.
        front_frame_tex, back_frame_tex = back_frame_tex, front_frame_tex
    VertexBuffer.deactivate_all()

def render(shape):
    """Use the renderer to render a Shape.

    :param shape: The shape to be rendered.
    :type shape: Shape
    """
    if fill_image_enabled:
        active_shader = texture_shader
    else:
        active_shader = default_shader

    active_shader.activate()
    active_shader.update_uniform('transform', transform_matrix)

    vertices = transform_points(shape.vertices).flatten()
    vertex_buffer = VertexBuffer('float', data=vertices)

    texcoords = np.array(flatten(shape.texcoords), dtype=np.float32)
    texcoords_buffer = VertexBuffer('float', data=texcoords)

    point_buffer = None
    edge_buffer = None
    face_buffer = None

    if shape.kind == 'POINT':
        points = np.array(list(range(len(vertex_buffer.data))), dtype=np.uint32)
        point_buffer = VertexBuffer('uint',
                                    data=points,
                                    buffer_type='elem')
    elif shape.kind == 'PATH':
        edges = np.array(shapes.edges, dtype=np.uint32)
        edge_buffer = VertexBuffer('uint',
                                   data=flatten(shape.edges),
                                   buffer_type='elem')
    else:
        edges = np.array(flatten(shape.edges), dtype=np.uint32)
        edge_buffer = VertexBuffer('uint',
                                   data=edges,
                                   buffer_type='elem')
        faces = np.array(flatten(shape.faces), dtype=np.uint32)
        face_buffer = VertexBuffer('uint',
                                   data=faces,
                                   buffer_type='elem')

    if fill_image_enabled:
        fill_image.activate()
        active_shader.update_attribute('texcoord', texcoords_buffer.id)

    active_shader.update_attribute('position', vertex_buffer.id)

    if shape.kind not in ['PATH', 'POINT']:
        if fill_image_enabled:
            if tint_enabled:
                active_shader.update_uniform('fill_color', tint_color)
            else:
                active_shader.update_uniform('fill_color', COLOR_WHITE)
            face_buffer.draw('TRIANGLE_FAN')
        elif fill_enabled:
            active_shader.update_uniform('fill_color', fill_color)
            face_buffer.draw('TRIANGLE_FAN')

    if stroke_enabled and (not fill_image_enabled):
        active_shader.update_uniform('fill_color', stroke_color)
        if shape.kind == 'POINT':
            point_buffer.draw('POINTS')
        elif shape.kind == 'PATH':
            edge_buffer.draw('LINE_STRIP')
        else:
            edge_buffer.draw('LINE_LOOP')

    buffers = [vertex_buffer, texcoords_buffer, point_buffer,
               edge_buffer, face_buffer]

    for b in buffers:
        if not (b is None):
            b.delete()
            del b

    active_shader.deactivate()

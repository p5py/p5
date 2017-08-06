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

texture_cache = {}


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
    transform = np.array(transform_matrix[:]).reshape((4, 4))
    points = np.hstack((np.array(points, dtype=np.float32),
                        np.array([[1]] * len(points)))).dot(transform)

    return points[:, :3]

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
    context = window_context
    gl_version = context.get_info().get_version()[:3]

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
    texture_shader.add_attribute('color', '4f')

    default_shader.activate()
    add_common_uniforms(default_shader)
    default_shader.add_attribute('position', '3f')
    default_shader.add_attribute('color', '4f')

    reset_view()

def clear(color=True, depth=True):
    """Clear the renderer background."""
    gl.glClearColor(*background_color)
    color_bit = gl.GL_COLOR_BUFFER_BIT if color else 0
    depth_bit = gl.GL_DEPTH_BUFFER_BIT if depth else 0
    gl.glClear(color_bit | depth_bit)

def reset_view():
    """Reset the view of the renderer."""
    global transform_matrix
    global modelview_matrix
    global projection_matrix
    global viewport

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
    texture_shader.update_uniform('modelview', modelview_matrix)
    texture_shader.update_uniform('projection', projection_matrix)

    default_shader.activate()
    default_shader.update_uniform('modelview', modelview_matrix)
    default_shader.update_uniform('projection', projection_matrix)

def cleanup():
    """Run the clean-up routine for the renderer.

    This method is called when all drawing has been completed and the
    program is about to exit.

    """
    default_shader.delete()
    texture_shader.delete()
    for texture_hash, texture in texture_cache:
        texture.delete()


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
    texture_shader.update_uniform('modelview', modelview_matrix)
    texture_shader.update_uniform('projection', projection_matrix)
    texture_shader.deactivate()

    default_shader.activate()
    default_shader.update_uniform('modelview', modelview_matrix)
    default_shader.update_uniform('projection', projection_matrix)
    default_shader.deactivate()

def post_render():
    """Cleanup things after a draw call.

    The post_render is called once all the rendering is done for the
    last draw call.

    """
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

    color_buffer = VertexBuffer('float')
    color_size = len(shape.vertices)

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
        edges = np.array(shape.edges, dtype=np.uint32)
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
                color_buffer.data = np.array(tint_color * color_size,
                                             dtype=np.float32)
            else:
                color_buffer.data = np.array(COLOR_WHITE * color_size,
                                             dtype=np.float32)
            active_shader.update_attribute('color', color_buffer.id)
            face_buffer.draw('TRIANGLE_FAN')
        elif fill_enabled:
            color_buffer.data = np.array(fill_color * color_size,
                                         dtype=np.float32)
            active_shader.update_attribute('color', color_buffer.id)
            face_buffer.draw('TRIANGLE_FAN')

    if stroke_enabled and (not fill_image_enabled):
        color_buffer.data = np.array(stroke_color * color_size, dtype=np.float32)
        active_shader.update_attribute('color', color_buffer.id)
        if shape.kind == 'POINT':
            point_buffer.draw('POINTS')
        elif shape.kind == 'PATH':
            edge_buffer.draw('LINE_STRIP')
        else:
            edge_buffer.draw('LINE_LOOP')

    buffers = [color_buffer, vertex_buffer, texcoords_buffer,
               point_buffer, edge_buffer, face_buffer]

    for b in buffers:
        if not (b is None):
            b.delete()
            del b

    active_shader.deactivate()

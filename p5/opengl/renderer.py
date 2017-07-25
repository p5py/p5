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

from ..pmath import Matrix4

from .gloo import VertexBuffer
from .shader import Shader
from .shader import vertex_default, fragment_default
from .shader import texture_vertex_default, texture_fragment_default

default_shader = None
texture_shader = None

transform_matrix = Matrix4()
modelview_matrix = Matrix4()
projection_matrix = Matrix4()

viewport = None

background_color = (0.8, 0.8, 0.8, 1.0)
fill_color = (1.0, 1.0, 1.0, 1.0)
tint_color = (1.0, 1.0, 1.0, 1.0)
tint_enabled = True
stroke_color = (0, 0, 0, 1.0)
fill_enabled = True
stroke_enabled = True

context = None

geometry_cache = {}

def add_common_uniforms(shader):
    """Add a default set of uniforms to the shader.
    """
    shader.add_uniform('projection', 'mat4')
    shader.add_uniform('modelview', 'mat4')
    shader.add_uniform('transform', 'mat4')
    shader.add_uniform('fill_color', 'vec4')

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

    default_shader.activate()
    add_common_uniforms(default_shader)
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
        shape_buffers['vertex_buffer'].delete()
        shape_buffers['edge_buffer'].delete()
        shape_buffers['face_buffer'].delete()

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
    default_shader.deactivate()

def post_render():
    """Cleanup things after a draw call.

    The post_render is called once all the rendering is done for the
    last draw call.

    """
    VertexBuffer.deactivate_all()

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

def render(shape):
    """Use the renderer to render a Shape.

    :param shape: The shape to be rendered.
    :type shape: Shape
    """
    default_shader.activate()
    default_shader.update_uniform('transform', transform_matrix)

    shape_hash = hash(shape)

    if shape_hash not in geometry_cache:
        vertex_buffer = VertexBuffer('float', data=flatten(shape.vertices))

        point_buffer = None
        edge_buffer = None
        face_buffer = None

        if shape.kind == 'POINT':
            point_buffer = VertexBuffer('uint',
                                        data=list(range(len(vertex_buffer.data))),
                                        buffer_type='elem')
        elif shape.kind == 'PATH':
            edge_buffer = VertexBuffer('uint',
                                       data=flatten(shape.edges),
                                       buffer_type='elem')
        else:
            edge_buffer = VertexBuffer('uint',
                                       data=flatten(shape.edges),
                                       buffer_type='elem')
            face_buffer = VertexBuffer('uint',
                                       data=flatten(shape.faces),
                                       buffer_type='elem')

        geometry_cache[shape_hash] = {
            'vertex_buffer': vertex_buffer,
            'point_buffer': point_buffer,
            'edge_buffer': edge_buffer,
            'face_buffer': face_buffer,
        }
    else:
        vertex_buffer = geometry_cache[shape_hash]['vertex_buffer']
        point_buffer = geometry_cache[shape_hash]['point_buffer']
        edge_buffer = geometry_cache[shape_hash]['edge_buffer']
        face_buffer = geometry_cache[shape_hash]['face_buffer']

    default_shader.update_attribute('position', vertex_buffer.id)

    if shape.kind == 'POINT' and stroke_enabled:
        default_shader.update_uniform('fill_color', stroke_color)
        point_buffer.draw('POINTS')
    elif shape.kind == 'PATH' and stroke_enabled:
        default_shader.update_uniform('fill_color', stroke_color)
        edge_buffer.draw('LINE_STRIP')
    else:
        default_shader.update_uniform('fill_color', fill_color)
        face_buffer.draw('TRIANGLE_FAN')
        if stroke_enabled:
            default_shader.update_uniform('fill_color', stroke_color)
            edge_buffer.draw('LINE_LOOP')
    default_shader.deactivate()

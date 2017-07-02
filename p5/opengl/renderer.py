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

from ..tmp import Matrix4
from .shader import Shader
from .shader import fragment_default
from .shader import vertex_default

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

vertex_buffer = -1
element_buffer = -1

def initialize(gl_version):
    """Initialize the OpenGL renderer.

    For an OpenGL based renderer this sets up the viewport and creates
    the shader program.

    :param gl_version: The version of OpenGL to use.
    :type gl_version: str

    """
    global vertex_buffer
    global element_buffer
    global default_shader

    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)

    default_shader = Shader(vertex_default, fragment_default, gl_version)

    default_shader.activate()

    default_shader.add_uniform('fill_color', 'vec4')
    default_shader.add_uniform('projection', 'mat4')
    default_shader.add_uniform('modelview', 'mat4')
    default_shader.add_uniform('transform', 'mat4')

    default_shader.add_attribute('position', '3f')

    vertex_buffer = GLuint()
    glGenBuffers(1, pointer(vertex_buffer))

    element_buffer = GLuint()
    glGenBuffers(1, pointer(element_buffer))

    reset_view()
    clear()

def cleanup():
    """Run the clean-up routine for the renderer.

    This method is called when all drawing has been completed and the
    program is about to exit.

    """
    default_shader.delete()
    glDeleteBuffers(1, vertex_buffer)
    glDeleteBuffers(1, element_buffer)

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
    view = Matrix4().translate(-builtins.width/2, -builtins.height/2, -cz)

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

def render(shape):
    """Use the renderer to render a Shape.

    :param shape: The shape to be rendered.
    :type shape: Shape
    """

    default_shader.update_uniform('transform', transform_matrix)

    vertices = [vi for vertex in shape.vertices for vi in vertex]
    vertices_typed =  (GLfloat * len(vertices))(*vertices)

    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
    glBufferData(
        GL_ARRAY_BUFFER,
        sizeof(vertices_typed),
        vertices_typed,
        GL_STATIC_DRAW
    )
    glBindBuffer(GL_ARRAY_BUFFER, 0)

    elements = [idx for face in shape.faces for idx in face]
    elements_typed = (GLuint * len(elements))(*elements)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, element_buffer)
    glBufferData(
        GL_ELEMENT_ARRAY_BUFFER,
        sizeof(elements_typed),
        elements_typed,
        GL_STATIC_DRAW
    )
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

    default_shader.update_attribute('position', vertex_buffer)

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, element_buffer)
    if fill_enabled and (shape.kind not in ['POINT', 'LINE']):
        default_shader.update_uniform('fill_color', fill_color)
        glDrawElements(
            GL_TRIANGLES,
            len(elements),
            GL_UNSIGNED_INT,
            0
        )
    if stroke_enabled:
        default_shader.update_uniform('fill_color', stroke_color)
        if shape.kind is 'POINT':
            glDrawElements(
                GL_POINTS,
                len(elements),
                GL_UNSIGNED_INT,
                0
            )
        else:
            glDrawElements(
                GL_LINE_LOOP,
                len(elements),
                GL_UNSIGNED_INT,
                0
            )
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

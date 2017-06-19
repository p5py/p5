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
import math

from pyglet.gl import *

from .. import core
from .. import sketch
from ..tmp import Matrix4
from .shader import Shader
from .shader import ShaderProgram
from .shader import fragment_default
from .shader import vertex_default

_shader_program = ShaderProgram()
_geometries = {}

def initialize():
    """Initialize the OpenGL renderer.

    For an OpenGL renderer this shouudl setup the required buffers,
    compile the default shaders, etc.

    """
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glViewport(0, 0, sketch.width, sketch.height)

    _init_shaders()

    core.reset_transforms()
    _shader_program['model'] = sketch.model_matrix_stack[0]
    _shader_program['view'] = sketch.mat_view
    _shader_program['projection'] = sketch.mat_projection

def _init_shaders():
    shaders = [
        Shader(vertex_default, 'vertex'),
        Shader(fragment_default, 'fragment'),
    ]

    for shader in shaders:
        shader.compile()
        _shader_program.attach(shader)

    _shader_program.link()
    _shader_program.activate()

    _shader_program.add_uniform('fill_color', 'vec4')
    _shader_program.add_uniform('projection', 'mat4')
    _shader_program.add_uniform('view', 'mat4')
    _shader_program.add_uniform('model', 'mat4')

def cleanup():
    """Run the clean-up routine for the renderer"""
    pass

def clear():
    glClearColor(*sketch.background_color.normalized)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

def pre_render():
    sketch.model_matrix_stack[0] = Matrix4()
    _shader_program['model'] = sketch.model_matrix_stack[0]

def post_render():
    pass

def render(shape):
    """Use the renderer to render a Shape.

    :param shape: The shape to be rendered.
    :type shape: Shape
    """

    #
    # TODO (abhikpal, 2017-06-10)
    #
    # - Ideally, this should be implemented by the Shape's
    #   __hash__ so that we can use the shape itself as the dict
    #   key and get rid of this str(__dict__(...) business.
    #
    # TODO (abhikpal, 2017-06-14)
    #
    # All of the buffer stuff needs refactoring.
    #
    shape_hash = str(shape.__dict__)

    if shape_hash not in _geometries:
        vertex_buffer = GLuint()
        glGenBuffers(1, pointer(vertex_buffer))

        index_buffer = GLuint()
        glGenBuffers(1, pointer(index_buffer))

        glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)

        vertices = [vi for vertex in shape.vertices for vi in vertex]
        vertices_typed =  (GLfloat * len(vertices))(*vertices)

        glBufferData(
            GL_ARRAY_BUFFER,
            sizeof(vertices_typed),
            vertices_typed,
            GL_STATIC_DRAW
        )

        elements = [idx for face in shape.faces for idx in face]
        elements_typed = (GLuint * len(elements))(*elements)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, index_buffer)
        glBufferData(
            GL_ELEMENT_ARRAY_BUFFER,
            sizeof(elements_typed),
            elements_typed,
            GL_STATIC_DRAW
        )

        position_attr = glGetAttribLocation(_shader_program.pid, b"position")
        glEnableVertexAttribArray(position_attr)
        glVertexAttribPointer(position_attr, 3, GL_FLOAT, GL_FALSE, 0, 0)

        _geometries[shape_hash] = {
            'vertex_buffer': vertex_buffer,
            'index_buffer': index_buffer,
            'num_elements': len(elements)
        }

    _shader_program['model'] = sketch.model_matrix_stack[0]

    glBindBuffer(GL_ARRAY_BUFFER, _geometries[shape_hash]['vertex_buffer'])

    position_attr = glGetAttribLocation(_shader_program.pid, b"position")
    glEnableVertexAttribArray(position_attr)
    glVertexAttribPointer(position_attr, 3, GL_FLOAT, GL_FALSE, 0, 0)

    if sketch.fill_enabled and (shape.kind not in ['POINT', 'LINE']):
        _shader_program['fill_color'] =  sketch.fill_color.normalized

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, _geometries[shape_hash]['index_buffer'])
        glDrawElements(
            GL_TRIANGLES,
            _geometries[shape_hash]['num_elements'],
            GL_UNSIGNED_INT,
            0
        )

    if sketch.stroke_enabled:
        _shader_program['fill_color'] = sketch.stroke_color.normalized
        if shape.kind is 'POINT':
            glDrawElements(
                GL_POINTS,
                _geometries[shape_hash]['num_elements'],
                GL_UNSIGNED_INT,
                0
            )
        else:
            glDrawElements(
                GL_LINE_LOOP,
                _geometries[shape_hash]['num_elements'],
                GL_UNSIGNED_INT,
                0
            )

def test_render():
    """Render the renderer's default test drawing.

    The render() methods requires a Shape object. In the absence
    of such an object/class the user should be able to check that
    the renderer is working by calling this method.
    """
    class Shape:
        def __init__(self):
            self.vertices = []
            self.faces = []

    class TestRect(Shape):
        def __init__(self, x, y, w, h):
            self.vertices = [
                (x - w/2, y - h/2, 0),
                (x - w/2, y + h/2, 0),
                (x + w/2, y + h/2, 0),
                (x + w/2, y - h/2, 0)
            ]
            self.faces = [(0, 1, 2), (2, 3, 0)]
            self.kind = 'POLY'

        def __eq__(self, other):
            return self.__dict__ == other.__dict__

    clear()

    r = TestRect(0, 0, 90, 90)

    with core.push_matrix():
        core.translate(100, 300)
        core.fill(0.8, 0.8, 0.8, 0.5)
        core.square((-45, -45), 90)

    with core.push_matrix():
        core.fill(0.8, 0.8, 0.4, 0.5)
        core.translate(200, 300)
        core.rotate(math.radians(45))
        render(r)

    with core.push_matrix():
        core.fill(0.8, 0.4, 0.8, 0.5)
        core.translate(300, 300)
        core.shear_y(math.radians(45))
        render(r)

    with core.push_matrix():
        core.fill(0.8, 0.4, 0.4, 0.5)
        core.translate(400, 300)
        core.shear_x(math.radians(45))
        render(r)

    with core.push_matrix():
        core.fill(0.4, 0.8, 0.8, 0.5)
        core.translate(500, 300)
        core.scale(0.5)
        render(r)

    with core.push_matrix():
        core.fill(0.4, 0.8, 0.4, 0.5)
        core.translate(600, 300)
        core.scale(1.5)
        render(r)

    with core.push_matrix():
        core.fill(0.4, 0.4, 0.8, 0.5)
        core.translate(700, 300)
        core.scale(1.25, 2)
        render(r)

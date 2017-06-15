#
# Part of p5py: A Python package based on Processing
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

from collections import namedtuple
from ctypes import *
import math

from pyglet.gl import *

from .. import core
from .. import sketch
from ..tmp import Matrix4
from .shader import Shader
from .shader import ShaderProgram


__all__ = ['OpenGLRenderer', 'BaseRenderer']

#
# TODO (abhikpal, 2017-06-06);
#
# - Fill in the missing args for all methods (maybe after
#   OpenGLRenderer is done?)
#
class BaseRenderer:
    """Base abstraction layer for all renderers."""
    def __init__(self):
        raise NotImplementedError("Abstract")

    def initialize(self):
        """Initilization routine for the renderer."""
        raise NotImplementedError("Abstract")

    def check_support(self):
        """Check if the the system supports the current renderer.

        :returns: True if the renderer is supported.
        :rtype: bool

        :raises RuntimeError: if the renderer is not supported.
        """
        raise NotImplementedError("Abstract")

    def pre_render(self):
        """Run the pre-render routine(s).

        The pre_render is called before the renderer is used to draw
        anything in the current iteration of the draw*() loop. This
        method could, for instance:

        - reset the transformations for the viewport
        - clear the screen,
        - etc.
        """
        pass

    def render(self, shape):
        """Use the renderer to render the given shape.

        :param shape: The shape that needs to be rendered.
        :type shape: Shape
        """
        raise NotImplementedError("Abstract")

    def post_render(self):
        """Run the post-render routine(s).

        The post_render is called when we are done drawing things for
        the current iteration of the draw call. Any draw-loop specific
        cleanup steps should go here.
        """
        pass

    def clear(self):
        """Clear the screen."""
        raise NotImplementedError("Abstract")

    def cleanup(self):
        """Run the cleanup routine for the renderer.

        This is the FINAL cleanup routine for the renderer and would
        ideally be called when the program is about to exit.
        """
        pass

    def test_render(self):
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

            def __eq__(self, other):
                return self.__dict__ == other.__dict__

        self.clear()

        r = TestRect(0, 0, 90, 90)

        core.fill(0.8, 0.8, 0.8, 0.5)
        core.translate(100, 300)
        self.render(r)
        core.reset_transforms()

        core.fill(0.8, 0.8, 0.4, 0.5)
        core.translate(200, 300)
        core.rotate(math.radians(45))
        self.render(r)
        core.reset_transforms()

        core.fill(0.8, 0.4, 0.8, 0.5)
        core.translate(300, 300)
        core.shear_y(math.radians(45))
        self.render(r)
        core.reset_transforms()

        core.fill(0.8, 0.4, 0.4, 0.5)
        core.translate(400, 300)
        core.shear_x(math.radians(45))
        self.render(r)
        core.reset_transforms()

        core.fill(0.4, 0.8, 0.8, 0.5)
        core.translate(500, 300)
        core.scale(0.5)
        self.render(r)
        core.reset_transforms()

        core.fill(0.4, 0.8, 0.4, 0.5)
        core.translate(600, 300)
        core.scale(1.5)
        self.render(r)
        core.reset_transforms()

        core.fill(0.4, 0.4, 0.8, 0.5)
        core.translate(700, 300)
        core.scale(1.25, 2)
        self.render(r)
        core.reset_transforms()

    def __repr__(self):
        print("{}( version: {} )".format(self.__class__.__name__, self.version))

    __str__ = __repr__


class OpenGLRenderer(BaseRenderer):
    """The main OpenGL renderer.

    :param sketch_attrs: The main dictionary containing all attributes
        for the sketch.
    :type sketch_attrs: dict
    """

    def __init__(self):
        #
        # TODO (abhikpal, 2017-06-06)
        #
        # - Do we want to initialize the renderer here or get the
        #   sketch to do it explicitly when it has everything else
        #   ready?
        #
        self.shader_program = ShaderProgram()

        self.geoms = {}

    def initialize(self):
        """Run the renderer initialization routine.

        For an OpenGL renderer this should setup the required buffers,
        compile the shaders, etc.
        """

        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        glViewport(0, 0, sketch.width, sketch.height)

        self._init_shaders()

        core.reset_transforms()
        self.shader_program['model'] = sketch.model_matrix_stack[0]
        self.shader_program['view'] = sketch.mat_view
        self.shader_program['projection'] = sketch.mat_projection

    def _init_shaders(self):
        vertex_shader_source = """
            #version 130

            in vec3 position;

            uniform mat4 model;
            uniform mat4 view;
            uniform mat4 projection;

            void main()
            {
                gl_Position = projection * view * model * vec4(position, 1.0);
            }
        """

        fragment_shader_source = """
            #version 130

            uniform vec4 fill_color;

            void main()
            {
                gl_FragColor = fill_color;
            }
        """
        shaders = [
            Shader(vertex_shader_source, 'vertex'),
            Shader(fragment_shader_source, 'fragment'),
        ]

        for shader in shaders:
            shader.compile()
            self.shader_program.attach(shader)

        self.shader_program.link()
        self.shader_program.activate()

        self.shader_program.add_uniform('fill_color', 'vec4')
        self.shader_program.add_uniform('projection', 'mat4')
        self.shader_program.add_uniform('view', 'mat4')
        self.shader_program.add_uniform('model', 'mat4')

    def _create_buffers(self, shape):
        """Create the required buffers for the given shape.

        :param shape: Create buffers for this shape.
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
        if shape_hash in self.geoms:
            return shape_hash

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

        position_attr = glGetAttribLocation(self.shader_program.pid, b"position")
        glEnableVertexAttribArray(position_attr)
        glVertexAttribPointer(position_attr, 3, GL_FLOAT, GL_FALSE, 0, 0)

        self.geoms[shape_hash] = {
            'vertex_buffer': vertex_buffer,
            'index_buffer': index_buffer,
            'num_elements': len(elements)
        }
        return shape_hash

    def _draw_buffers(self, shape_hash):
        self.shader_program['model'] = sketch.model_matrix_stack[0]
        glBindBuffer(GL_ARRAY_BUFFER, self.geoms[shape_hash]['vertex_buffer'])

        position_attr = glGetAttribLocation(self.shader_program.pid, b"position")
        glEnableVertexAttribArray(position_attr)
        glVertexAttribPointer(position_attr, 3, GL_FLOAT, GL_FALSE, 0, 0)

        if sketch.fill_enabled:
            self.shader_program['fill_color'] =  sketch.fill_color.normalized

            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.geoms[shape_hash]['index_buffer'])
            glDrawElements(
                GL_TRIANGLES,
                self.geoms[shape_hash]['num_elements'],
                GL_UNSIGNED_INT,
                0
            )

        if sketch.stroke_enabled:
            self.shader_program['fill_color'] = sketch.stroke_color.normalized
            glDrawElements(
                GL_LINE_LOOP,
                self.geoms[shape_hash]['num_elements'],
                GL_UNSIGNED_INT,
                0
            )

    def render(self, shape):
        """Use the renderer to render a shape.

        :param shape: The shape to be rendered.
        :type shape: Shape

        """
        shape_hash = self._create_buffers(shape)
        self._draw_buffers(shape_hash)

    def clear(self):
        """Clear the screen."""
        glClearColor(*sketch.background_color.normalized)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def pre_render(self):
        sketch.model_matrix_stack[0] = Matrix4()
        self.shader_program['model'] = sketch.model_matrix_stack[0]

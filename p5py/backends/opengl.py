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

from pyglet.gl import *

from .. import core
from .. import sketch
from ..backends import BaseRenderer

sketch_attrs = sketch._attrs

# This should only have the renderer.
__all__ = ['OpenGLRenderer']


class Shader:
    """Represents a shader in OpenGL.

    :param source: GLSL source code/filename for the shader.
    :type source: str or bytes

    :param kind: the type of shader {'vertex', 'fragment', etc}
    :type kind: str

    :param pid: The ID of the program to which the shader belongs.
        (Optional; defaults to None)
    :type pid: int

    :param from_file: Set to True if `source` specifies a filename;
        False otherwise.
    :type filename: bool

    :raises TypeError: When the give shader type is not supported. 

    """
    _supported_shader_types = {
        'vertex': GL_VERTEX_SHADER,
        'fragment': GL_FRAGMENT_SHADER
    }

    _glsl_versions = { '2.0': 110, '2.1': 120, '3.0': 130, '3.1': 140,
        '3.2': 150, '3.3': 330, '4.0': 400, '4.1': 410, '4.2': 420,
        '4.3': 430, '4.4': 440, '4.5': 450, }

    def __init__(self, source, kind, from_file=False, preprocess=False):
        if from_file:
            with open(self.filename) as f:
                src = f.read()
            self.source = stc.encode('utf-8')
        else:
            self.source = source.encode('utf-8')

        if kind in self._supported_shader_types:
            self.kind = kind
        else:
            raise TypeError("Shader type not supported.")

        if preprocess:
            glsl_version = self._glsl_versions[sketch_attrs['gl_version']]
            self.preprocess(glsl_version)

        self._sid = None

    def preprocess(self, glsl_version):
        """Preprocess a shader.

        The GLSL syntax has changed significantly, to make sure that
        our shader is compatible with the version of OpenGL that
        pyglet is running, we change the shader's internal syntax
        before compilation.

        :param gl_version: The version of glsl we should process the
            shader for.
        :type gl_version: str

        """
        pass

    def compile(self):
        """Generate a shader id and compile the shader"""
        shader_type = self._supported_shader_types.get(self.kind)
        self._sid = glCreateShader(shader_type)
        src = c_char_p(self.source)
        glShaderSource(
            self._sid,
            1,
            cast(pointer(src), POINTER(POINTER(c_char))),
            None
        )
        glCompileShader(self._sid)
        self.log_info()

    def attach(self, program):
        """Attach the shader to the given program.

        :param program: The shader program
        :type program: ShaderProgram

        """
        program.attach_shader(self)

    def log_info(self, verbose=sketch_attrs['debug']):
        """Print the shader log and raise appropriate errors.

        :param verbose: Verbose state (False by default)
        :type verbose: bool

        """
        status_code = c_int(0)
        glGetShaderiv(self._sid, GL_COMPILE_STATUS, pointer(status_code))

        log_size = c_int(0)
        glGetShaderiv(self._sid, GL_INFO_LOG_LENGTH, pointer(log_size))

        log_message = create_string_buffer(log_size.value)
        glGetShaderInfoLog(self._sid, log_size, None, log_message)
        log_message = log_message.value.decode('utf-8')

        if verbose:
            print("Shader compilation status code: {}.".format(status_code.value))
            print("Log size is {} bytes".format(log_size.value))
            print("Shader source:")
            print(self._source.decode('utf-8'))
            print("Log:")
            print(log_message)

    @property
    def sid(self):
        """Return the shader id of the shader.

        :rtype: into
        :raises NameError: If the shader hasn't been created.

        """
        if self._sid:
            return self._sid
        else:
            raise NameError("Shader hasn't been created yet.")


class ShaderProgram:
    """A thin abstraction layer that helps work with shader programs."""

    def __init__(self):
        #: The program ID for the current shader program.
        self.pid = glCreateProgram()
        self._uniforms = {}

    def add_uniform(self, uniform_name, uniform_function):
        """Add a uniform to the shader program.

        :param uniform_name: name of the uniform.
        :type uniform_name: str

        :param uniform_function: function to call while setting the
            current uniform.
        :type uniform_function: function

        """
        Uniform = namedtuple('Uniform', ['uid', 'function'])
        self._uniforms[uniform_name] = Uniform(
            glGetUniformLocation(self.pid, uniform_name.encode()),
            uniform_function
        )

    def set_uniform_data(self, uni_name, *data):
        """Set data for the given uniform.

        :param uni_name: Name of the uniform.
        :type uni_name: str

        :param data: data to which the uniform should be set to.
        :type data: tuple

        """
        uniform = self._uniforms[uni_name]
        uniform.function(uniform.uid, *data)

    def attach_shader(self, *shaders):
        """Attach a list of shaders to the current program.

        :param shaders: The list of shaders to be attached.
        :type shaders: list of Shader objects
        """
        for shader in shaders:
            glAttachShader(self.pid, shader.sid)

    def link(self):
        """Link the current shader."""
        glLinkProgram(self.pid)

    def activate(self):
        """Activate the current shader."""
        glUseProgram(self.pid)

    def __repr__(self):
        return "{}( pid={})".format(self.__class__.__name__, self.pid)

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
        glViewport(0, 0, sketch_attrs['width'], sketch_attrs['height'])

        self._init_shaders()

    def _init_shaders(self):
        vertex_shader_source = """
            #version 130

            in vec3 position;

            void main()
            {
                gl_Position = vec4(position, 1.0);
            }
        """

        fragment_shader_source = """
            #version 130

            out vec4 outColor;
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
            shader.attach(self.shader_program)

        self.shader_program.link()
        self.shader_program.activate()

        self.shader_program.add_uniform('fill_color', glUniform4f)

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
        glBindBuffer(GL_ARRAY_BUFFER, self.geoms[shape_hash]['vertex_buffer'])

        position_attr = glGetAttribLocation(self.shader_program.pid, b"position")
        glEnableVertexAttribArray(position_attr)
        glVertexAttribPointer(position_attr, 3, GL_FLOAT, GL_FALSE, 0, 0)


        if sketch_attrs['fill_enabled']:
            self.shader_program.set_uniform_data(
                'fill_color',
                *sketch_attrs['fill_color'].normalized
            )

            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.geoms[shape_hash]['index_buffer'])
            glDrawElements(
                GL_TRIANGLES,
                self.geoms[shape_hash]['num_elements'],
                GL_UNSIGNED_INT,
                0
            )

        #
        # TODO (abhikpal, 2017-06-08)
        #
        # Figure out a way to get stroke_width
        #

        if sketch_attrs['stroke_enabled']:
            self.shader_program.set_uniform_data(
                'fill_color',
                *sketch_attrs['stroke_color'].normalized
            )

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
        glClearColor(*sketch_attrs['background_color'].normalized)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def test_render(self):
        class Shape:
            def __init__(self):
                self.vertices = []
                self.faces = []

        class TestRect(Shape):
            def __init__(self, x, y, w, h):
                self.vertices = [
                    (x, y, 0),
                    (x + w, y, 0),
                    (x + w, y - h, 0),
                    (x, y - h, 0)
                ]
                self.faces = [(0, 1, 2), (2, 3, 0)]

            def __eq__(self, other):
                return self.__dict__ == other.__dict__

        lim = 16
        for i in range(-1*lim, lim):
            norm_i = (i + lim)/(lim * 2)

            r = TestRect(i/8, 0.95, 0.2, 0.6)
            core.fill(1 - norm_i, 0.1, norm_i)
            self.render(r)

            r = TestRect(i/8, 0.3, 0.2, 0.6)
            core.fill(0.1, norm_i, 1 - norm_i, 1.0)
            self.render(r)

            r = TestRect(i/8, -0.35, 0.2, 0.6)
            core.fill(norm_i, 1 - norm_i, 0.1, 1.0)

            self.render(r)

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

from ctypes import *

from pyglet.gl import *

from ..backends import BaseRenderer
from ..core import Color

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

    def __init__(self, source, kind, from_file=False):
        if from_file:
            with open(self.filename) as f:
                src = f.read()
            self.source = src
        else:
            self.source = source

        if kind in self._supported_shader_types:
            self._kind = kind
        else:
            raise TypeError("Shader type not supported.")

        self._attached_programs = set()

        self._sid = None

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

    def attach(self, program):
        """Attach the shader to the given program.

        :param program: The shader program to which we need to attach
            the shader.
        :type pid: ShaderProgram
        
        :raises ValueError: If the shader is already attached to the
            program.

        """
        if program.pid in self._attached_programs:
            raise ValueError("Shader already attached to the program.")
        self._attached_programs.add(program.pid)
        glAttachShader(program.pid, self.sid)

        self.log_info(verbose=True)

    def log_info(self, verbose=False):
        """Print the shader log and raise appropriate errors.

        :param verbose: Verbose state (False by default)
        :type verbose: bool

        :raises RuntimeError: When the shader compiler reports an
            error.
        """
        status_code = c_int(0)
        glGetShaderiv(self._sid, GL_COMPILE_STATUS, pointer(status_code))

        log_size = c_int(0)
        glGetShaderiv(self._sid, GL_INFO_LOG_LENGTH, pointer(log_size))

        log_message = create_string_buffer(log_size.value)
        glGetShaderInfoLog(self._sid, log_size, None, log_message)

        if log_message.value:
            if verbose:
                print("Shader compilation status code: {}.".format(status_code.value))
                print("Log size is {} bytes".format(log_size.value))
                print("Shader source:")
                print(self._source.decode('utf-8'))
            error_message = log_message.value.decode('utf-8')
            raise RuntimeError("Error compiling {} shader.\n"
                               "\t{}".format(self._kind, error_message))

    @property
    def source(self):
        """Return the GLSL source code for the shader.

        :rtype: bytes
        """
        return self._source
    
    @source.setter
    def source(self, src):
        if isinstance(src, bytes):
            self._source = src
        else:
            self._source = src.encode('utf-8')

    @property
    def kind(self):
        """Return the type of the shader.

        :rtype: str

        """
        return self._kind

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

    @property
    def attached_programs(self):
        """Returns the ids of the program to which the shader is attached.

        :rtype: set

        """
        return self._attached_programs

class ShaderProgram:
    """A thin abstraction layer that helps work with shader programs."""

    def __init__(self):
        #: The program ID for the current shader program.
        self.pid = glCreateProgram()

    def attach(self, *shaders):
        """Attach a list of shaders to the current program.

        :param shaders: The list of shaders to be attached.
        :type shaders: list of Shader objects
        """
        for shader in shaders:
            shader.attach(self)

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

    def __init__(self, sketch_attrs):
        #
        # TODO (abhikpal, 2017-06-06)
        #
        # - Do we want to initialize the renderer here or get the
        #   sketch to do it explicitly when it has everything else
        #   ready?
        #
        self.sketch_attrs = sketch_attrs
        self.shader_program = ShaderProgram()

        self.shader_uniforms = {}

    def initialize(self):
        """Run the renderer initialization routine.

        For an OpenGL renderer this should setup the required buffers,
        compile the shaders, etc.
        """

        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)

        glViewport(0, 0, self.sketch_attrs['width'], self.sketch_attrs['height'])

        vao = GLuint()
        glGenVertexArrays(1, pointer(vao))
        glBindVertexArray(vao)

        self._init_shaders()

        self.shader_program.link()
        self.shader_program.activate()

        self.shader_uniforms['fill_color'] = glGetUniformLocation(
            self.shader_program.pid, b"fill_color" )

    def check_support(self):
        # TODO (abhikpal, 2017-06-06)
        #
        # - decide on a base OpenGL class and use gl_info.have_version
        #   to implement this.
        pass

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
                outColor = fill_color;
            }
        """
        shaders = [
            Shader(vertex_shader_source, 'vertex'),
            Shader(fragment_shader_source, 'fragment'),
        ]

        for shader in shaders:
            shader.compile()
            self.shader_program.attach(shader)

        glBindFragDataLocation(self.shader_program.pid, 0, b"outColor")

    def _create_buffers(self, shape):
        """Create the required buffers for the given shape.

        :param shape: Create buffers for this shape.
        :type shape: Shape

        """
        self.vertex_buffer = GLuint()
        glGenBuffers(1, pointer(self.vertex_buffer))

        self.index_buffer = GLuint()
        glGenBuffers(1, pointer(self.index_buffer))

        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer)

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
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.index_buffer)
        glBufferData(
            GL_ELEMENT_ARRAY_BUFFER,
            sizeof(elements_typed),
            elements_typed,
            GL_STATIC_DRAW
        )
        self.num_elements = len(elements)

        position_attr = glGetAttribLocation(self.shader_program.pid, b"position")
        glEnableVertexAttribArray(position_attr)
        glVertexAttribPointer(position_attr, 3, GL_FLOAT, GL_FALSE, 0, 0)

    def _draw_buffers(self):
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer)

        position_attr = glGetAttribLocation(self.shader_program.pid, b"position")
        glEnableVertexAttribArray(position_attr)
        glVertexAttribPointer(position_attr, 3, GL_FLOAT, GL_FALSE, 0, 0)

        glUniform4f(self.shader_uniforms['fill_color'],
                    *self.sketch_attrs['fill_color'].normalized)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.index_buffer)
        glDrawElements(
            GL_TRIANGLES,
            self.num_elements,
            GL_UNSIGNED_INT,
            0
        )
        #
        # TODO (abhikpal, 2017-06-08)
        #
        # Figure out a way to get stroke_width
        # 
        glUniform4f(self.shader_uniforms['fill_color'],
                    *self.sketch_attrs['stroke_color'].normalized)
        glDrawElements(
            GL_LINE_LOOP,
            self.num_elements,
            GL_UNSIGNED_INT,
            0
        )


    def render(self, shape):
        """Use the renderer to render a shape.

        :param shape: The shape to be rendered.
        :type shape: Shape

        """
        self._create_buffers(shape)
        self._draw_buffers()

    def clear(self):
        """Clear the screen."""
        glClearColor(*self.sketch_attrs['background_color'].normalized)
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

        for i in range(-8, 8):
            norm_i = (i + 8)/16

            r = TestRect(i/8, 0.95, 0.2, 0.6)
            self.sketch_attrs['fill_color'] = Color(1 - norm_i, 0.1, norm_i)
            self.render(r)

            r = TestRect(i/8, 0.3, 0.2, 0.6)
            self.sketch_attrs['fill_color'] = Color(0.1, norm_i, 1 - norm_i, 1.0)
            self.render(r)

            r = TestRect(i/8, -0.35, 0.2, 0.6)
            self.sketch_attrs['fill_color'] = Color(norm_i, 1 - norm_i, 0.1, 1.0)
            self.render(r)


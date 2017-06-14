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

from .. import sketch

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

    def log_info(self, verbose=sketch._debug):
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
            print(self.source.decode('utf-8'))
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

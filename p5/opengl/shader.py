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

from collections import namedtuple
from ctypes import *
import re

from pyglet.gl import *

debug = True

_glsl_versions = {'2.0': 110, '2.1': 120, '3.0': 130, '3.1': 140,
                  '3.2': 150, '3.3': 330, '4.0': 400, '4.1': 410,
                  '4.2': 420, '4.3': 430, '4.4': 440, '4.5': 450, }

_shader_preprocessor = """
#ifdef GL_ES
precision mediump float;
precision mediump int;
#endif
"""

vertex_default = """
attribute vec3 position;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main()
{
    gl_Position = projection * view * model * vec4(position, 1.0);
}
"""

fragment_default = """
uniform vec4 fill_color;

void main()
{
    gl_FragColor = fill_color;
}
"""

_re_glsl_id = "(?<![0-9A-Z_a-z])({})(?![0-9A-Z_a-z]|\\s*\\()"
_re_glsl_fn = "(?<![0-9A-Z_a-z])(%s)(?=\\s*\\()"

_preprocess_vertex_patterns = [
    (_re_glsl_id, "varying", "out"),
    (_re_glsl_id, "attribute", "in"),
    (_re_glsl_id, "texture", "texMap"),
    (_re_glsl_fn, "texture2DRect|texture2D|texture3D|textureCube", "texture"),
]

_preprocess_fragment_patterns = [
    (_re_glsl_id, "varying|attribute", "in"),
    (_re_glsl_id, "texture", "texMap"),
    (_re_glsl_fn, "texture2DRect|texture2D|texture3D|textureCube", "texture"),
    (_re_glsl_id, "gl_FragColor", "_fragColor"),
]

def _uvec4(uniform, data):
    glUniform4f(uniform, *data)

def _umat4(uniform, matrix):
    flattened = matrix[:]
    glUniformMatrix4fv(uniform, 1, GL_FALSE, (GLfloat * 16)(*flattened))

_uniform_function_map = {
    'vec4': _uvec4,
    'mat4': _umat4,
}

ShaderUniform = namedtuple('Uniform', ['name', 'uid', 'function'])

class Shader:
    """Represents a shader in OpenGL.

    :param source: GLSL source code of the shader.
    :type source: str

    :param kind: the type of shader {'vertex', 'fragment', etc}
    :type kind: str

    :raises TypeError: When the give shader type is not supported. 

    """
    _supported_shader_types = {
        'vertex': GL_VERTEX_SHADER,
        'fragment': GL_FRAGMENT_SHADER
    }

    def __init__(self, source, kind, version='110', preprocess=True):
        self.source = source
        self.kind = kind
        self._id = None

        # preprocessing only makes sense if the shader doesn't have an
        # explicitly defined version string.
        if preprocess and ("#version" not in self.source):
            target_version = _glsl_versions[version]
            self.preprocess(target_version)

    def preprocess(self, target_version):
        """Preprocess a shader.

        The GLSL syntax has changed significantly, to make sure that
        our shader is compatible with the version of OpenGL that
        pyglet is running, we change the shader's internal syntax
        before compilation.

        :param target_version: The version of glsl we should process the
            shader for.
        :type gl_version: str

        """
        processed_shader = "#version {}\n".format(target_version)

        if target_version < 130:
            return processed_shader + self.source

        if self.kind == 'vertex':
            patterns = _preprocess_vertex_patterns
        elif self.kind == 'fragment':
            patterns = _preprocess_fragment_patterns
            processed_shader += "out vec4 _fragColor;"

        for line in self.source.split('\n'):
            processed_line = line
            for regex, search, replace in patterns:
                processed_line = re.sub(regex.format(search), replace, processed_line)
            processed_shader += processed_line + '\n'

        self.source = processed_shader

    def compile(self):
        """Generate a shader id and compile the shader"""
        shader_type = self._supported_shader_types[self.kind]
        self._id = glCreateShader(shader_type)
        src = c_char_p(self.source.encode('utf-8'))
        glShaderSource(
            self._id,
            1,
            cast(pointer(src), POINTER(POINTER(c_char))),
            None
        )
        glCompileShader(self._id)

        if debug:
            status_code = c_int(0)
            glGetShaderiv(self._id, GL_COMPILE_STATUS, pointer(status_code))

            log_size = c_int(0)
            glGetShaderiv(self._id, GL_INFO_LOG_LENGTH, pointer(log_size))

            log_message = create_string_buffer(log_size.value)
            glGetShaderInfoLog(self._id, log_size, None, log_message)
            log_message = log_message.value.decode('utf-8')

            if len(log_message) > 0:
                print(self.source)
                print(log_message)
                # In Windows (OpenGL 3.3 + intel card) the log_message
                # is set to "No errors" on a successful compilation
                # and the code raises the Exception even though it
                # shouldn't. There should be a proper fix, but getting
                # rid of this line for now, will fix it.
                # 
                # raise Exception(log_message)

    @property
    def sid(self):
        """Return the shader id of the shader.

        :rtype: int
        :raises NameError: If the shader hasn't been created.

        """
        if self._id:
            return self._id
        else:
            raise NameError("Shader hasn't been created yet.")

    @classmethod
    def create_from_file(cls, filename, kind, **kwargs):
        """Create a shader from a file.

        :param filename: file name of the shader source code.
        :type filename: str

        :param kind: the type of shader
        :type kind: str

        :para kwargs: extra keyword arguments for the Shader
            constuctor.
        :type kwargs: dict

        :returns: A shader constucted using the given filename.
        :rtype: Shader

        """
        with open(filename) as f:
            shader_source = f.read()
        return cls(shader_source, kind, **kwargs)


class ShaderProgram:
    """A thin abstraction layer that helps work with shader programs."""

    def __init__(self):
        self._id = glCreateProgram()
        self._uniforms = {}

    @property
    def pid(self):
        """The program id of the shader."""
        return self._id

    def add_uniform(self, uniform_name, dtype):
        """Add a uniform to the shader program.

        :param uniform_name: name of the uniform.
        :type uniform_name: str

        :param dtype: data type of the uniform: 'vec3', 'mat4', etc
        :type dtype: str

        """
        uniform_function = _uniform_function_map[dtype]
        self._uniforms[uniform_name] = ShaderUniform(
            uniform_name,
            glGetUniformLocation(self.pid, uniform_name.encode()),
            uniform_function
        )

    def __getitem__(self, uniform_name):
        return self._uniforms[uniform_name]

    def __setitem__(self, uni_name, data):
        """Set data for the given uniform.

        :param uni_name: Name of the uniform.
        :type uni_name: str

        :param data: data to which the uniform should be set to.
        :type data: tuple

        """
        uniform = self._uniforms[uni_name]
        uniform.function(uniform.uid, data)

    def attach(self, shader):
        """Attach a shader to the current program.

        :param shader:The shader to be attached.
        :type shader: Shader
        """
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

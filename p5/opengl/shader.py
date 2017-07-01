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

GLSL_VERSIONS = {'2.0': 110, '2.1': 120, '3.0': 130, '3.1': 140,
                  '3.2': 150, '3.3': 330, '4.0': 400, '4.1': 410,
                  '4.2': 420, '4.3': 430, '4.4': 440, '4.5': 450, }


vertex_default = """
attribute vec3 position;

uniform mat4 transform;
uniform mat4 modelview;
uniform mat4 projection;

void main()
{
    gl_Position = projection * modelview * transform * vec4(position, 1.0);
}
"""

fragment_default = """
uniform vec4 fill_color;

void main()
{
    gl_FragColor = fill_color;
}
"""


Uniform = namedtuple('Uniform', ['name', 'uid', 'function'])

def _uvec4(uniform, data):
    glUniform4f(uniform, *data)

def _umat4(uniform, matrix):
    flattened = matrix[:]
    glUniformMatrix4fv(uniform, 1, GL_FALSE, (GLfloat * 16)(*flattened))

_uniform_function_map = {
    'vec4': _uvec4,
    'mat4': _umat4,
}


class Shader:
    """A thin abstraction layer that helps work with shader programs."""

    def __init__(self, vertex, fragment, version='2.0'):
        self._vertex_source = preprocess_shader(vertex, 'vert', version)
        self._fragment_source = preprocess_shader(fragment, 'frag', version)
        self._pid = glCreateProgram()

        self.compile_vertex_shader()
        self.compile_fragment_shader()

        glAttachShader(self._pid, self._vid)
        glAttachShader(self._pid, self._fid)

        glLinkProgram(self._pid)

        self._uniforms = {}

    @property
    def pid(self):
        return self._pid

    def _compile(self, source, kind):
        """Compile a shader from its source code.

        :param source: Source code of the shader to be compiled.
        :type source: str

        :param kind: The kind of shader we are compiling.
        :type kind: int

        :returns: The shader id of the compiled shader.
        :rtype: int

        """
        shader_id = glCreateShader(kind)
        src = c_char_p(source.encode('utf-8'))
        glShaderSource(
            shader_id,
            1,
            cast(pointer(src), POINTER(POINTER(c_char))),
            None
        )
        glCompileShader(shader_id)
        status_code = c_int(0)
        glGetShaderiv(shader_id, GL_COMPILE_STATUS, pointer(status_code))

        log_size = c_int(0)
        glGetShaderiv(shader_id, GL_INFO_LOG_LENGTH, pointer(log_size))

        log_message = create_string_buffer(log_size.value)
        glGetShaderInfoLog(shader_id, log_size, None, log_message)
        log_message = log_message.value.decode('utf-8')

        if len(log_message) > 0:
            print(source)
            print(log_message)
            # In Windows (OpenGL 3.3 + intel card) the log_message
            # is set to "No errors" on a successful compilation
            # and the code raises the Exception even though it
            # shouldn't. There should be a proper fix, but getting
            # rid of this line for now, will fix it.
            #
            # raise Exception(log_message)

        return shader_id

    def compile_vertex_shader(self):
        """Compile the vertex shader associated with this program."""
        self._vid = self._compile(self._vertex_source, GL_VERTEX_SHADER)

    def compile_fragment_shader(self):
        """Compile the fragmen shader associated with this program."""
        self._fid = self._compile(self._fragment_source, GL_FRAGMENT_SHADER)

    def add_uniform(self, uniform_name, dtype):
        """Add a uniform to the shader program.

        :param uniform_name: name of the uniform.
        :type uniform_name: str

        :param dtype: data type of the uniform: 'vec3', 'mat4', etc
        :type dtype: str

        """
        uniform_function = _uniform_function_map[dtype]
        self._uniforms[uniform_name] = Uniform(
            uniform_name,
            glGetUniformLocation(self._pid, uniform_name.encode()),
            uniform_function
        )

    def update_uniform(self, uniform_name, data):
        """Set data for the given uniform.

        :param uniform_name: Name of the uniform.
        :type uniform_name: str

        :param data: data to which the uniform should be set to.
        :type data: tuple

        """
        uniform = self._uniforms[uniform_name]
        uniform.function(uniform.uid, data)

    def activate(self):
        """Activate the current shader."""
        glUseProgram(self._pid)

    def deactivate(self):
        """Deactivate the current shader"""
        glUseProgram(0)

    def __repr__(self):
        return "{}( pid={} )".format(self.__class__.__name__, self._pid)

    __str__ = __repr__


def preprocess_shader(shader_source, shader_type, open_gl_version):
    """Preprocess a shader to be compatible with the given OpenGL version.

    :param shader_source: Source code of the shader.
    :type shader_source: str

    :shader_type: type of shader we are using. Should be one of
         {'vertex', 'fragment'}
    :type shader_type: str

    :param open_gl_version: The version of OpenGL we should process the
        shader for.
    :type open_gl_version: str

    :returns: The modified shader code that is compatible with the
        given OpenGL version.
    :rtype: str

    :raises TypeError: if the shader type is unsupported.

    """

    target_glsl_version = GLSL_VERSIONS[open_gl_version]

    # If the user has already defined a version string for the shader,
    # we can safely assume that they know what they are doing and we
    # don't do any preprocessing.
    #
    if "#version" in shader_source:
        return shader_source

    processed_shader = "#version {}\n".format(target_glsl_version)

    # We are assuming that the shader source code was written for
    # older versions of OpenGL (< 3.0). If the target version is
    # indeed below 3.0, we don't need to do any preprocessing.
    #
    if target_glsl_version < 130:
        return processed_shader + shader_source

    # Processing uses the following regexes to find and replace
    # identifiers (repid) and function names (re_fn) from the old GLSL
    # versions and change them to the newever syntax.
    #
    # See: GLSL_ID_REGEX and GLSL_FN_REGEX in PGL.java (~line 1981).
    #
    repid = "(?<![0-9A-Z_a-z])({})(?![0-9A-Z_a-z]|\\s*\\()"
    re_fn = "(?<![0-9A-Z_a-z])({})(?=\\s*\\()"

    # The search and replace strings for different shader types.
    # Terrible things will happen if the search replace isn't applied
    # in the order defined here (this is especially true for the
    # textures.)
    #
    # DO NOT CHANGE THE ORDER OF THE SEARCH/REPALCE PATTERNS.
    if shader_type == 'vert':
        patterns = [
            (repid, "varying", "out"),
            (repid, "attribute", "in"),
            (repid, "texture", "texMap"),
            (re_fn, "texture2DRect|texture2D|texture3D|textureCube", "texture")
        ]
    elif shader_type == 'frag':
        patterns = [
            (repid, "varying|attribute", "in"),
            (repid, "texture", "texMap"),
            (re_fn, "texture2DRect|texture2D|texture3D|textureCube", "texture"),
            (repid, "gl_FragColor", "_fragColor"),
        ]
        processed_shader += "out vec4 _fragColor;"
    else:
        raise TypeError("Cannot preprocess {} shader.".format(shader_type))

    for line in shader_source.split('\n'):
        new_line = line
        for regex, search, replace in patterns:
            new_line = re.sub(regex.format(search), replace, new_line)
        processed_shader += new_line + '\n'

    return processed_shader

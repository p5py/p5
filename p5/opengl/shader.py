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
"""Helper functions and classes to work with OpenGL shaders.
"""
from collections import namedtuple
import ctypes as ct
import re

from pyglet import gl

debug = True

# A mapping from OpenGL versions to the corresponding GLSL version.
# Required for preprocessing shaders and determining GLSL shader
# versions to use.
GLSL_VERSIONS = {'2.0': 110, '2.1': 120, '3.0': 130, '3.1': 140,
                  '3.2': 150, '3.3': 330, '4.0': 400, '4.1': 410,
                  '4.2': 420, '4.3': 430, '4.4': 440, '4.5': 450, }

# shader preprocessor directive for GLES
SHADER_PREPROCESSOR = """
#ifdef GL_ES
precision mediump float;
precision mediump int;
#endif
"""


# Default vertex and fragment shaders.
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

# Shader sources to draw framebuffers textues.
screen_texture_vert = """
attribute vec2 position;
attribute vec2 tex_coord;

varying vec2 vert_tex_coord;

void main() {
    gl_Position = vec4(position, 0, 1);
    vert_tex_coord = tex_coord;
}
"""

screen_texture_frag = """
uniform sampler2D texMap;
varying vec2 vert_tex_coord;

void main() {
    gl_FragColor = texture2D(texMap, vert_tex_coord.st);
}
"""
screen_texture_frag = SHADER_PREPROCESSOR + screen_texture_frag

# A named tuple that descibes a shader uniform.
#
# - name: name of the shader uniform.
# - uid: uniform id, location of the uniform.
# - function: function that needs to be called while setting the
#   shader
Uniform = namedtuple('Uniform', ['name', 'uid', 'function'])


# A named tuple that descibes a attribute.
#
# - name: name of the attribute
# - loc: location of the attribute
# - size: number of values that descibe this attribute.
# - dtype: data type of the attribute.
# - norm: should the attribute be normalized to the (0, 1) range?
# - stride: stride in the main data array descibing the attribute.
# - offset: offset in the main data array descibing the attribute.
#
Attribute = namedtuple('Attribute', ['name', 'loc', 'size',
                                     'dtype','norm', 'stride',
                                     'offset'])

# functions to set data to uniforms. All of them take *ONLY* two
# params: the uniform location and the data to be set.
def _uvec4(uniform, data):
    gl.glUniform4f(uniform, *data)

def _umat4(uniform, matrix):
    data_array = (gl.GLfloat * 16)(*matrix[:])
    gl.glUniformMatrix4fv(uniform, 1, gl.GL_FALSE, data_array)

def _uint(uniform, data):
    gl.glUniform1i(uniform, data)

uniform_function_map = {
    'vec4': _uvec4,
    'mat4': _umat4,
    'int': _uint,
}

attribute_dtype_map = {
    'f': gl.GL_FLOAT,
    'float': gl.GL_FLOAT,
}


class Shader:
    """Encapsulates a GLSL shader program.

    Every shader requires the vertex and fragment sources during
    initialization. These shaders are preprocessed to be compatible
    with the OpenGL version of the user's GL context. So,
    additionally, the OpenGL version of the context is also required
    during initialization.

    Note that shader sources that explicitly mention the required
    OpenGL version (using `#version`) *ARE NOT* preprocessed.

    :param vertex: source code of the vertex shader.
    :type vertex: str

    :param fragment: source code of the fragment. shader.
    :type fragment: str

    :param version: OpenGL version being used (defaults to None)
    :type version: str

    """

    def __init__(self, vertex, fragment, version=None):
        self._pid = gl.glCreateProgram()

        self._vertex_source = preprocess_shader(vertex, 'vert', version)
        self._fragment_source = preprocess_shader(fragment, 'frag', version)

        self.compile_vertex_shader()
        self.compile_fragment_shader()

        gl.glAttachShader(self._pid, self._vid)
        gl.glAttachShader(self._pid, self._fid)

        gl.glLinkProgram(self._pid)

        self._uniforms = {}
        self._attributes = {}

    def _compile(self, source, kind):
        """Compile a shader from its source code.

        :param source: Source code of the shader to be compiled.
        :type source: str

        :param kind: The kind of shader we are compiling.
        :type kind: int

        :returns: The shader id of the compiled shader.
        :rtype: int

        """
        shader_id = gl.glCreateShader(kind)
        _src = ct.c_char_p(source.encode('utf-8'))
        src = ct.cast(ct.pointer(_src), ct.POINTER(ct.POINTER(ct.c_char)))
        gl.glShaderSource(shader_id, 1, src, None)

        gl.glCompileShader(shader_id)
        status_code = ct.c_int(0)
        status_code_pointer = ct.pointer(status_code)
        gl.glGetShaderiv(shader_id, gl.GL_COMPILE_STATUS, status_code_pointer)

        log_size = ct.c_int(0)
        log_size_pointer = ct.pointer(log_size)
        gl.glGetShaderiv(shader_id, gl.GL_INFO_LOG_LENGTH, log_size_pointer)

        log_message = ct.create_string_buffer(log_size.value)
        gl.glGetShaderInfoLog(shader_id, log_size, None, log_message)
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
        self._vid = self._compile(self._vertex_source, gl.GL_VERTEX_SHADER)

    def compile_fragment_shader(self):
        """Compile the fragment shader associated with this program."""
        self._fid = self._compile(self._fragment_source, gl.GL_FRAGMENT_SHADER)

    def add_uniform(self, uname, dtype):
        """Add a uniform to the shader program.

        :param uname: name of the uniform.
        :type uname: str

        :param dtype: data type of the uniform -- 'vec3', 'mat4', etc
        :type dtype: str

        """
        ufunc = uniform_function_map[dtype]
        loc = gl.glGetUniformLocation(self._pid, uname.encode())
        self._uniforms[uname] = Uniform(uname, loc, ufunc)

    def update_uniform(self, uname, data):
        """Set data for the given uniform.

        :param uname: Name of the uniform.
        :type uname: str

        :param data: data to which the uniform should be set to.
        :type data: dependent on the uniform

        """
        uniform = self._uniforms[uname]
        uniform.function(uniform.uid, data)

    def add_attribute(self, name, data_format,
                      normalize=False, stride=0, offset=0):
        """Add an attribute to the current shader.

        :param name: name of the attribute being added.
        :type name: str

        :param data_format: a string describing the data format of the
            attribute. The general syntax is `<size><data_type>` where
            size is the number of the data points that describe the
            attribute and data_type represents the data type of the
            data points. For example '3f' describes an attribute with
            3 floating point data points.
        :type data_format: str

        :param normalize: When set to True, OpenGL will normalize the
            data to the range [0.0, 1.0] (defaults to False)
        :type normalize: bool

        :param stride: Specifies the offset between consecutive
            attributes (defaults to 0).
        :type stride: int

        :param offset: Location of the first component of the
            attribute in the data array (defaults to 0).
        :type offset: int

        """

        size = int(data_format[0])
        dtype = attribute_dtype_map[data_format[1:]]
        norm = gl.GL_TRUE if normalize else gl.GL_FALSE
        loc = gl.glGetAttribLocation(self._pid, name.encode('utf-8'))
        self._attributes[name] = Attribute(name, loc, size, dtype,
                                           norm, stride, offset)

    def update_attribute(self, name, vbo_id):
        """Update the value of the given attribute.

        :param name: name of the attribute to be updated.
        :type name: str

        :param vbo_id: The id of the vertex buffer object that
            contains the data for the given attribute.
        :type vbo_id: int

        """
        attr = self._attributes[name]
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo_id)
        gl.glEnableVertexAttribArray(attr.loc)
        gl.glVertexAttribPointer(attr.loc, attr.size, attr.dtype,
                              attr.norm, attr.stride, attr.offset)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)

    def activate(self):
        """Activate the current shader."""
        gl.glUseProgram(self._pid)

    def deactivate(self):
        """Deactivate the current shader"""
        gl.glUseProgram(0)

    def delete(self):
        """Delete the current shader."""
        gl.glDeleteProgram(self._pid)
        gl.glDeleteShader(self._fid)
        gl.glDeleteShader(self._vid)

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

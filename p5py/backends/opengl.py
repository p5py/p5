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


class Shader:
    """Represents a shader in OpenGL.

    :param source: GLSL source code/filename for the shader.
    :type source: str or bytes

    :param kind: the type of the shader (should ideally be a const
        from pyglet.gl)
    :type kind: int

    :param pid: The ID of the program to which the shader belongs.
        (Optional; defaults to None)
    :type pid: int

    :param from_file: Set to True if `source` specifies a filename;
        False otherwise.
    :type filename: bool

    """

    def __init__(self, source, kind, program=None, from_file=False):
        if from_file:
            with open(self.filename) as f:
                src = f.read()
            self.source = src
        else:
            self.source = source

        self.__pid = program
        self.__kind = kind
        self.__sid = None

    def compile(self):
        """Generate a shader id and compile the shader"""
        self.__sid = glCreateShader(self.__kind)
        src = c_char_p(self.source)
        glShaderSource(
            self.sid,
            1,
            cast(pointer(src), POINTER(POINTER(c_char))),
            None
        )
        glCompileShader(self.sid)

    def attach(self, pid=None):
        """Attach the shader to the given program.

        :param pid: The program id.
        :type pid: int

        """
        if self.pid and (not pid):
            pid = self.pid

        glAttachShader(pid, self.sid)

    @property
    def source(self):
        """Return the GLSL source code for the shader.

        :rtype: str
        """
        return self.__source

    @source.setter
    def source(self, src):
        if isinstance(src, bytes):
            self.__source = src
        else:
            self.__source = src.encode('utf-8')

    @property
    def kind(self):
        """Return the type of the shader.

        :rtype: int
        :raises AttributeError: On modification attempt.

        """
        return self.__kind

    @kind.setter
    def kind(self, k):
        raise AttributeError("Cannot modify the shader type"
                             "after it has been instantiated")

    @property
    def sid(self):
        """Return the shader id of the shader.

        :rtype: int
        :raises AttributeError: On modification attempt.
        :raises NameError: If the shader hasn't been created.

        """
        if self.__sid:
            return self.__sid
        else:
            raise NameError("Shader hasn't been created yet.")

    @sid.setter
    def sid(self, k):
        raise AttributeError("The shader id is read-only.")

    @property
    def pid(self):
        """Returns the id of the program to which the shader is attached.

        :rtype: int
        :raises AttributeError: On modification attempt.
        :raises NameError: If the shader hasn't been attached to a program.

        """
        if self.__pid:
            return self.__pid
        raise NameError("Shader hasn't been attached to a program yet.")

    @pid.setter
    def pid(self, k):
        raise AttributeError("The program id is read-only.")


vertex_shader_source = b"""
    #version 130
    
    in vec3 position;

    void main()
    {
        gl_Position = vec4(position, 1.0);
    }
"""

fragment_shader_source = b"""
    #version 130
    
    out vec4 outColor;
    
    void main()
    {
        outColor = vec4(1.0, 1.0, 1.0, 1.0);
    }
"""


# a simple triangle for to test things out
# (all z-coords are zero as this is a 2D triangle)
vertices = [
    0, 0.5, 0,
    0.5, -0.5, 0,
    -0.5, -0.5, 0,
]

def initialize():
    vao = GLuint()
    glGenVertexArrays(1, pointer(vao))
    glBindVertexArray(vao)

    vbo = GLuint()
    glGenBuffers(1, pointer(vbo))

    vertices_ctype = (GLfloat * len(vertices))(*vertices)

    glBindBuffer(GL_ARRAY_BUFFER, vbo)

    glBufferData(
        GL_ARRAY_BUFFER,
        sizeof(vertices_ctype),
        vertices_ctype,
        GL_STATIC_DRAW
    )

    shader_program = _init_shaders()

    position_attr = glGetAttribLocation(shader_program, b"position")
    glEnableVertexAttribArray(position_attr)
    glVertexAttribPointer(position_attr, 3, GL_FLOAT, GL_FALSE, 0, 0)
    
def _init_shaders():
    shader_ids = []

    shaders = [
        (vertex_shader_source, GL_VERTEX_SHADER),
        (fragment_shader_source, GL_FRAGMENT_SHADER)
    ]

    for shader_source, kind in shaders:
        shader_id = glCreateShader(kind)
        src = c_char_p(shader_source)
        glShaderSource(
            shader_id,
            1,
            cast(pointer(src), POINTER(POINTER(c_char))),
            None
        )

        glCompileShader(shader_id)

        shader_ids.append(shader_id)

    shader_program = glCreateProgram()

    for sid in shader_ids:
        glAttachShader(shader_program, sid)

    glBindFragDataLocation(shader_program, 0, b"outColor")
    glLinkProgram(shader_program)
    glUseProgram(shader_program)

    return shader_program

def set_defaults(*args):
    width, height, _ = args
    glClearColor(0.0, 0.0, 0., 0.0)


def clear():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

def sample_draw():
    """Render a test drawing"""
    glDrawArrays(GL_TRIANGLES, 0, 3)

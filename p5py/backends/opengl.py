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

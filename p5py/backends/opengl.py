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

# TODO (abhikpal, 2017-06-01)
# 
#    - Setup some global data struct to store/retrive all buffers.
# 
#    - Get rid of the hardcoded `vertices` buffer thing inside
#      _init_buffers(). Ideally, _init_buffers() and _create_buffers()
#      should be combined somehow.


renderer_pid = None

# Dummy shape class for testing.
class Shape:
    def __init__(self, *vertices):
        self.vertices = list(vertices)


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

        self._pid = program
        self._kind = kind
        self._sid = None

    def compile(self):
        """Generate a shader id and compile the shader"""
        self._sid = glCreateShader(self._kind)
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

        :rtype: int

        """
        return self._kind

    @property
    def sid(self):
        """Return the shader id of the shader.

        :rtype: int
        :raises NameError: If the shader hasn't been created.

        """
        if self._sid:
            return self._sid
        else:
            raise NameError("Shader hasn't been created yet.")

    @property
    def pid(self):
        """Returns the id of the program to which the shader is attached.

        :rtype: int
        :raises NameError: If the shader hasn't been attached to a program.

        """
        if self._pid:
            return self._pid
        raise NameError("Shader hasn't been attached to a program yet.")


def initialize():
    """Run the renderer initialization routine.

    For an OpenGL renderer this should setup the required buffers,
    compile the shaders, etc.
    """
    global renderer_pid
    renderer_pid = glCreateProgram()

    vao = GLuint()
    glGenVertexArrays(1, pointer(vao))
    glBindVertexArray(vao)


    _test_triangle = Shape((0, 0.5, 0), (0.5, -0.5, 0), (-0.5, -0.5, 0))
    _create_buffers(_test_triangle)
    _init_shaders()

    glLinkProgram(renderer_pid)
    glUseProgram(renderer_pid)

    position_attr = glGetAttribLocation(renderer_pid, b"position")
    glEnableVertexAttribArray(position_attr)
    glVertexAttribPointer(position_attr, 3, GL_FLOAT, GL_FALSE, 0, 0)

    # Defaults
    glClearColor(0.0, 0.0, 0., 0.0)

def _init_shaders():
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
    
    void main()
    {
        outColor = vec4(1.0, 1.0, 1.0, 1.0);
    } 
   """
    shaders = [
        Shader(vertex_shader_source, GL_VERTEX_SHADER, renderer_pid),
        Shader(fragment_shader_source, GL_FRAGMENT_SHADER, renderer_pid),
    ]

    for shader in shaders:
        shader.compile()
        shader.attach()

    glBindFragDataLocation(renderer_pid, 0, b"outColor")

def _create_buffers(shape):
    """Create the required buffers for the given shape.

    :param shape: Create buffers for this shape.
    :type shape: Shape

    """
    vertex_buffer = GLuint()
    glGenBuffers(1, pointer(vertex_buffer))
    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)

    vertices = [vi for vertex in shape.vertices for vi in vertex]
    vertices_typed =  (GLfloat * len(vertices))(*vertices)
    
    glBufferData(
        GL_ARRAY_BUFFER,
        sizeof(vertices_typed),
        vertices_typed,
        GL_STATIC_DRAW
    )

def render(shape):
    """Use the renderer to render a shape.
    
    :param shape: The shape to be rendered.
    :type shape: Shape

    """
    # bind the correct buffers,
    # select shape type GL_LINES, GL_TRIANGLES, etc
    # set the attrib pointers.
    raise NotImplementedError

def clear():
    """Clear the screen."""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

def test_render():
    """Render a test drawing"""
    glDrawArrays(GL_TRIANGLES, 0, 3)

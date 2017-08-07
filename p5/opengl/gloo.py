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
"""Provides an Object Oriented interface to OpenGL."""

from abc import ABCMeta, abstractmethod
import ctypes as ct

from pyglet import gl

_buffer_type_map = {
    'data': gl.GL_ARRAY_BUFFER,
    'elem': gl.GL_ELEMENT_ARRAY_BUFFER
}

_dtype_map = {
    'float': (gl.GLfloat, gl.GL_FLOAT),
    'uint': (gl.GLuint, gl.GL_UNSIGNED_INT)
}

_mode_map = {
    'POINTS': gl.GL_POINTS,
    'LINE_STRIP': gl.GL_LINE_STRIP,
    'LINE_LOOP': gl.GL_LINE_LOOP,
    'TRIANGLES': gl.GL_TRIANGLES,
    'TRIANGLE_FAN': gl.GL_TRIANGLE_FAN,
}

class GLObject(metaclass=ABCMeta):
    """An abstract class for GL objects."""
    @abstractmethod
    def activate(self):
        """Activate the object."""
        pass

    @abstractmethod
    def deactivate(self):
        """Deactivate the object."""
        pass

    @abstractmethod
    def delete(self):
        """Delete the object."""
        pass

    @property
    def id(self):
        return self._id

class VertexBuffer(GLObject):
    """Encapsulates an OpenGL VertexBuffer.
    """
    def __init__(self, dtype, data=None, buffer_type='data'):
        self.buffer_type = buffer_type
        self._type = _buffer_type_map[buffer_type]

        self.data_type = dtype
        self._dtype, self._dtype_const = _dtype_map[dtype]

        self._data = None

        self._id = gl.GLuint()
        gl.glGenBuffers(1, ct.pointer(self._id))

        if data is not None:
            self.data = data

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        value_typed = (self._dtype * len(value))(*value)
        self.activate()
        gl.glBufferData(self._type, ct.sizeof(value_typed),
                        value_typed, gl.GL_DYNAMIC_DRAW)
        self.deactivate()
        self._data = value

    def activate(self):
        """Activate the current buffer.
        """
        gl.glBindBuffer(self._type, self._id)

    def deactivate(self):
        """Deactivate the current buffer.
        """
        gl.glBindBuffer(self._type, 0)

    @staticmethod
    def deactivate_all():
        """Deactivate all buffers.
        """
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, 0)

    def draw(self, mode):
        draw_mode = _mode_map[mode]
        self.activate()
        if self.buffer_type == 'elem':
            gl.glDrawElements(draw_mode, len(self.data), self._dtype_const, 0)
        else:
            raise ValueError("cannot draw a data buffer.")
        self.deactivate()

    def delete(self):
        """Delete the current buffer."""
        gl.glDeleteBuffers(1, self._id)

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

class FrameBuffer:
    """Encapsulates an OpenGL FrameBuffer."""
    def __init__(self):
        self._id = Gluint()
        gl.glGenFramebuffersEXT(1, pointer(self._id))

        self._check_completion_status()

    def _check_completion_status(self):
        """Check the completion status of the framebuffer.

        :raises Exception: When the frame buffer is incomplete.
        """
        status = gl.glCheckFramebufferStatusEXT(gl.GL_FRAMEBUFFER_EXT)
        if status != gl.GL_FRAMEBUFFER_COMPLETE_EXT:
            msg = "ERR {}: FrameBuffer could not be created.".format(status)
            raise Exception(msg)

    def activate(self):
        """Activate the current framebuffer."""
        gl.glBindFramebufferEXT(gl.GL_FRAMEBUFFER_EXT, self._id)

    def deactivate(self):
        """Deactivate the current framebuffer."""
        gl.glBindFramebufferEXT(gl.GL_FRAMEBUFFER_EXT, self._id)

    def attach_texture(self, texture):
        self.activate()
        gl.glFramebufferTexture2DEXT(gl.GL_FRAMEBUFFER_EXT,
                                     gl.GL_COLOR_ATTACHMENT0_EXT,
                                     gl.GL_TEXTURE_2D, texture.id, 0)
        self.deactivate()

    def delete(self):
        """Delete the current frame buffer."""
        gl.glDeleteFramebuffersEXT(self._id)

    def __del__(self):
        self.delete()


class FrameTexture:
    """A texture to be used with the FrameBuffer"""
    def __init__(self, width, height):
        self._id = gl.Gluint()
        gl.glGenTextures(1, pointer(self._id))

        self.activate()

        _blank_texture = (gl.GLubyte * (width * height * 4))()
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_EDGE)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_EDGE)

        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, width, height, 0,
                        gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, _blank_texture)
        self._init_texture()

        self.deactivate()

    def _init_texture(self):
        # Initialize the texture bu uniformly filling with the
        # background color.
        pass

    @property
    def id(self):
        return self._id

    def activate(self):
        """Activate the current texture."""
        gl.glBindTexture(gl.GL_TEXTURE_2D, self._id)

    def deactivate(self):
        """Deactivate the current texture."""
        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)


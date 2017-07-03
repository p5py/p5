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
"""Module to check support for various OpenGL components."""

def has_fbo(context):
    """Check if the open gl context supports frame buffers.

    :param context: The OpenGL context to be tested (defaults to the
        one used by the renderer.)
    :type context: pyglet.gl.Context

    :returns: True if the context supports frame buffers; false
        otherwise.
    :rtype: bool

    """
    context_info = context.get_info()

    gl_major_version = int(context_info.get_version()[0])
    required_ogl_version = 3
    if gl_major_version >= required_ogl_version:
        return True

    available_extensions = context_info.get_extensions()
    required_extensions = [ 'GL_ARB_framebuffer_object',
                            'GL_EXT_framebuffer_object', ]

    # These could come in handy at some point.
    #
    # 'GL_EXT_framebuffer_blit',
    # 'GL_EXT_framebuffer_multisample',
    # 'GL_EXT_packed_depth_stencil',

    return any(ext in available_extensions for ext in required_extensions)
    

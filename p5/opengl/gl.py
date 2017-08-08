# This code was orignally written for the Glumpy project and is being
# used here with slight modifications.
#
# Copyright notice from the original source:
#
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
#
# The full license text for Glumpy has been included in
# LICENSES/glumpy.txt

import ctypes

import OpenGL
OpenGL.ERROR_ON_COPY = True
# -> if set to a True value before importing the numpy/lists support modules,
#    will cause array operations to raise OpenGL.error.CopyError if the
#    operation would cause a data-copy in order to make the passed data-type
#    match the target data-type.

from OpenGL.plugins import FormatHandler
FormatHandler( 'glumpy',
               'OpenGL.arrays.numpymodule.NumpyHandler',[
                   'glumpy.gloo.buffer.VertexBuffer',
                   'glumpy.gloo.buffer.IndexBuffer',
                   'glumpy.gloo.atlas.Atlas',
                   'glumpy.gloo.texture.Texture2D',
                   'glumpy.gloo.texture.Texture1D',
                   'glumpy.gloo.texture.FloatTexture2D',
                   'glumpy.gloo.texture.FloatTexture1D',
                   'glumpy.gloo.texture.TextureCube',
               ])



from OpenGL import contextdata
def cleanupCallback( context=None ):
    """Create a cleanup callback to clear context-specific storage for the current context"""
    def callback( context = contextdata.getContext( context ) ):
        """Clean up the context, assumes that the context will *not* render again!"""
        contextdata.cleanupContext( context )
    return callback

from OpenGL.GL import *
from OpenGL.GL.EXT.geometry_shader4 import *
from OpenGL.GL.NV.geometry_program4 import *
from OpenGL.GL.ARB.texture_rg import *


# Patch: pythonize the glGetActiveAttrib
_glGetActiveAttrib = glGetActiveAttrib
def glGetActiveAttrib(program, index):
    # Prepare
    bufsize = 32
    length = ctypes.c_int()
    size = ctypes.c_int()
    type = ctypes.c_int()
    name = ctypes.create_string_buffer(bufsize)
    # Call
    _glGetActiveAttrib(program, index,
                       bufsize, ctypes.byref(length), ctypes.byref(size),
                       ctypes.byref(type), name)
    # Return Python objects
    return name.value, size.value, type.value

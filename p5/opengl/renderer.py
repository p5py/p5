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
"""The OpenGL renderer for p5."""

import builtins
from contextlib import contextmanager
import math

import numpy as np

from . import gl
from .gloo import IndexBuffer
from .gloo import Program
from .gloo import VertexBuffer
from .shader import vertex_default, fragment_default
from .support import has_fbo

from ..pmath import matrix

##
## Renderer globals.
##
## TODO (2017-08-01 abhikpal):
##
## - Higher level objects *SHOULD NOT* have direct access to internal
##   state variables.
##

## Renderer Globals: USEFUL CONSTANTS
COLOR_WHITE = (1, 1, 1, 1)
COLOR_BLACK = (0, 0, 0, 1)
COLOR_DEFAULT_BG = (0.8, 0.8, 0.8, 1.0)

## Renderer Globals: STYLE/MATERIAL PROPERTIES
##
background_color = COLOR_DEFAULT_BG

fill_color = COLOR_WHITE
fill_enabled = True

stroke_color = COLOR_BLACK
stroke_enabled = True

## Renderer Globals
## VIEW MATRICES, ETC
##
viewport = None

transform_matrix = np.identity(4)
modelview_matrix = np.identity(4)
projection_matrix = np.identity(4)

## Renderer Globals: OPEN GL SPECIFIC
##
context = None

default_shader = None

## Renderer Globals: RENDERING
poly_draw_queue = []
line_draw_queue = []
point_draw_queue = []

## RENDERER UTILITY FUNCTIONS
##
## Mostly for internal user. Ideally, higher level components *SHOULD
## NOT* need these.
##

def flatten(vertex_list):
    """Flatten a vertex list

    An unflattened list of vertices is a list of tuples [(x1, y2, z1),
    (x2, y2, z2), ...] where as a list of flattened vertices doesn't
    have any tuples [x1, y1, z2, x2, y2, z2, ...]

    :param vertex_list: list of vertices to be flattened.
    :type vertex_list: list of 3-tuples

    :returns: a flattened vertex_list
    :rtype: list

    """
    return [vi for vertex in vertex_list for vi in vertex]

def transform_points(points):
    """Transform the given list of points using the transformation matrix.

    :param points: List of points to be transformed.
    :type points: a list of 3-tuples

    :returns: a numpy array with the transformed points.
    :rtype: np.ndarray

    """
    points = points.dot(transform_matrix.T)
    return points[:, :3]

## RENDERER SETUP FUNCTIONS.
##
## These don't handle shape rendering directly and are used for setup
## tasks like initialization, cleanup before exiting, resetting views,
## clearing the screen, etc.
##

def initialize(window_context):
    """Initialize the OpenGL renderer.

    For an OpenGL based renderer this sets up the viewport and creates
    the shader program.

    :param window_context: The OpenGL context associated with this renderer.
    :type window_context: pyglet.gl.Context

    """
    global context
    global default_shader

    context = window_context
    gl_version = context.get_info().get_version()[:3]

    gl.glEnable(gl.GL_BLEND)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

    gl.glEnable(gl.GL_DEPTH_TEST)
    gl.glDepthFunc(gl.GL_LEQUAL)

    gl.glEnable(gl.GL_MULTISAMPLE)

    default_shader = Program(vertex_default, fragment_default)
    reset_view()

def clear(color=True, depth=True):
    """Clear the renderer background."""
    gl.glClearColor(*background_color)
    color_bit = gl.GL_COLOR_BUFFER_BIT if color else 0
    depth_bit = gl.GL_DEPTH_BUFFER_BIT if depth else 0
    gl.glClear(color_bit | depth_bit)

def reset_view():
    """Reset the view of the renderer."""
    global transform_matrix
    global modelview_matrix
    global projection_matrix
    global viewport

    viewport = (0, 0, builtins.width, builtins.height)
    gl.glViewport(*viewport)

    cz = (builtins.height / 2) / math.tan(math.radians(30))
    projection_matrix = matrix.perspective_matrix(
        math.radians(60),
        builtins.width / builtins.height,
        0.1 * cz,
        10 * cz
    )

    modelview_matrix = matrix.translation_matrix(-builtins.width / 2, builtins.height / 2, -cz)
    modelview_matrix = modelview_matrix.dot(matrix.scale_transform(1, -1, 1))

    transform_matrix = np.identity(4)

    default_shader['modelview'] = modelview_matrix.T.flatten()
    default_shader['projection'] = projection_matrix.T.flatten()

def cleanup():
    """Run the clean-up routine for the renderer.

    This method is called when all drawing has been completed and the
    program is about to exit.

    """
    # default_shader.delete()
    # texture_shader.delete()
    pass

## RENDERING FUNTIONS + HELPERS
##
## These are responsible for actually rendring things to the screen.
## For some draw call the methods should be called as follows:
##
##    with draw_loop():
##        # multiple calls to render()
##

def flush_geometry():
    """Flush all the shape geometry from the draw queue to the GPU.
    """
    global poly_draw_queue
    global line_draw_queue
    global point_draw_queue

    ## RETAINED MODE RENDERING.
    #
    draw_names = ['poly', 'line', 'point']
    draw_types = [gl.GL_TRIANGLES, gl.GL_LINES, gl.GL_POINTS]
    draw_queues = [poly_draw_queue, line_draw_queue, point_draw_queue]

    for draw_type, draw_queue, name in zip(draw_types, draw_queues, draw_names):
        # 1. Get the maximum number of vertices persent in the shapes
        # in the draw queue.
        #
        if len(draw_queue) == 0:
            continue

        num_vertices = sum([len(shape.vertices) for shape, _ in draw_queue])

        # 2. Create empty buffers based on the number of vertices.
        #
        data = np.zeros(num_vertices,
                        dtype=[('position', np.float32, 3),
                               ('color', np.float32, 4)])

        # 3. Loop through all the shapes in the geometry queue adding
        # it's information to the buffer.
        #
        sidx = 0
        draw_indices = []
        for shape, color in draw_queue:
            num_shape_verts = len(shape.vertices)

            data['position'][sidx:(sidx + num_shape_verts),] = \
                shape.transformed_vertices[:, :3]

            color_array = np.array([color] * num_shape_verts)
            data['color'][sidx:sidx + num_shape_verts, :] = color_array

            if name == 'point':
                idx = np.arange(0, num_shape_verts, dtype=np.uint32)
            elif name == 'line':
                idx = np.array(shape.edges, dtype=np.uint32).ravel()
            else:
                idx = np.array(shape.faces, dtype=np.uint32).ravel()

            draw_indices.append(sidx + idx)

            sidx += num_shape_verts

        V = data.view(VertexBuffer)
        I = np.hstack(draw_indices).view(IndexBuffer)

        # 4. Bind the buffer to the shader.
        #
        default_shader.bind(V)

        # 5. Draw the shape using the proper shape type and get rid of
        # the buffers.
        #
        default_shader.draw(draw_type, indices=I)

        V.delete()
        I.delete()

    # 6. Empty the draw queue.
    poly_draw_queue = []
    line_draw_queue = []
    point_draw_queue = []

@contextmanager
def draw_loop():
    """The main draw loop context manager.
    """
    global transform_matrix
    gl.glViewport(*viewport)
    transform_matrix = np.identity(4)

    yield

    flush_geometry()

def render(shape):
    """Use the renderer to render a Shape.

    :param shape: The shape to be rendered.
    :type shape: Shape
    """
    global poly_draw_queue
    global line_draw_queue
    global point_draw_queue

    ## RETAINED MODE RENDERING
    #
    # 1. Transform the shape using the current transform matrix.
    #
    shape.transform(transform_matrix)

    # 2. Depending on the current property add the shape and the color
    # to the correct draw queue
    #
    if fill_enabled and shape.kind not in ['POINT', 'PATH']:
        poly_draw_queue.append((shape, fill_color))

    if stroke_enabled:
        if shape.kind == 'POINT':
            point_draw_queue.append((shape, stroke_color))
        else:
            line_draw_queue.append((shape, stroke_color))

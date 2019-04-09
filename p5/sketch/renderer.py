#
# Part of p5: A Python package based on Processing
# Copyright (C) 2017-2018 Abhik Pal
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

from vispy import gloo
from vispy.gloo import FrameBuffer
from vispy.gloo import IndexBuffer
from vispy.gloo import Program
from vispy.gloo import RenderBuffer
from vispy.gloo import Texture2D
from vispy.gloo import VertexBuffer

from ..pmath import matrix
from .shaders import src_default
from .shaders import src_fbuffer
from .shaders import src_texture


from ..core.structure import push_style
from ..core.transforms import push_matrix
from ..core.image import image, image_mode

##
## Renderer globals.
##
## TODO (2017-08-01 abhikpal):
##
## - Higher level objects *SHOULD NOT* have direct access to internal
##   state variables.
##
default_prog = None
fbuffer_prog = None
texture_prog = None

fbuffer = None
fbuffer_tex_front = None
fbuffer_tex_back = None

vertex_buffer = None
index_buffer = None

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

tint_color = COLOR_BLACK
tint_enabled = False

## Renderer Globals
## VIEW MATRICES, ETC
##
viewport = None
texture_viewport = None
transform_matrix = np.identity(4)
modelview_matrix = np.identity(4)
projection_matrix = np.identity(4)

## Renderer Globals: RENDERING
poly_draw_queue = []
line_draw_queue = []
point_draw_queue = []

## RENDERER SETUP FUNCTIONS.
##
## These don't handle shape rendering directly and are used for setup
## tasks like initialization, cleanup before exiting, resetting views,
## clearing the screen, etc.
##

def _comm_toggles(state=True):
    gloo.set_state(blend=state)
    gloo.set_state(depth_test=state)

    if state:
        gloo.set_state(blend_func=('src_alpha', 'one_minus_src_alpha'))
        gloo.set_state(depth_func='lequal')

def initialize_renderer():
    """Initialize the OpenGL renderer.

    For an OpenGL based renderer this sets up the viewport and creates
    the shader programs.

    """
    global fbuffer
    global fbuffer_prog
    global default_prog
    global texture_prog
    global vertex_buffer
    global index_buffer

    fbuffer = FrameBuffer()

    vertices = np.array([[-1.0, -1.0],
                         [+1.0, -1.0],
                         [-1.0, +1.0],
                         [+1.0, +1.0]],
                        np.float32)
    texcoords = np.array([[0.0, 0.0],
                          [1.0, 0.0],
                          [0.0, 1.0],
                          [1.0, 1.0]],
                         dtype=np.float32)

    fbuf_vertices = VertexBuffer(data=vertices)
    fbuf_texcoords = VertexBuffer(data=texcoords)

    fbuffer_prog = Program(src_fbuffer.vert, src_fbuffer.frag)
    fbuffer_prog['texcoord'] = fbuf_texcoords
    fbuffer_prog['position'] = fbuf_vertices

    vertex_buffer = VertexBuffer()
    index_buffer = IndexBuffer()

    default_prog = Program(src_default.vert, src_default.frag)
    texture_prog = Program(src_texture.vert, src_texture.frag)
    texture_prog['texcoord'] = fbuf_texcoords

    reset_view()

def clear(color=True, depth=True):
    """Clear the renderer background."""
    gloo.set_state(clear_color=background_color)
    gloo.clear(color=color, depth=depth)

def reset_view():
    """Reset the view of the renderer."""
    global viewport
    global texture_viewport

    global transform_matrix
    global modelview_matrix
    global projection_matrix

    global fbuffer_tex_front
    global fbuffer_tex_back

    viewport = (
        0,
        0,
        int(builtins.width * builtins.pixel_x_density),
        int(builtins.height * builtins.pixel_y_density),
    )
    texture_viewport = (
        0,
        0,
        builtins.width,
        builtins.height,
    )
    gloo.set_viewport(*viewport)

    cz = (builtins.height / 2) / math.tan(math.radians(30))
    projection_matrix = matrix.perspective_matrix(
        math.radians(60),
        builtins.width / builtins.height,
        0.1 * cz,
        10 * cz
    )
    modelview_matrix = matrix.translation_matrix(-builtins.width / 2, \
                                                 builtins.height / 2, \
                                                 -cz)
    modelview_matrix = modelview_matrix.dot(matrix.scale_transform(1, -1, 1))

    transform_matrix = np.identity(4)

    default_prog['modelview'] = modelview_matrix.T.flatten()
    default_prog['projection'] = projection_matrix.T.flatten()

    texture_prog['modelview'] = modelview_matrix.T.flatten()
    texture_prog['projection'] = projection_matrix.T.flatten()

    fbuffer_tex_front = Texture2D((builtins.height, builtins.width, 3))
    fbuffer_tex_back = Texture2D((builtins.height, builtins.width, 3))

    for buf in [fbuffer_tex_front, fbuffer_tex_back]:
        fbuffer.color_buffer = buf
        with fbuffer:
            clear()

def cleanup():
    """Run the clean-up routine for the renderer.

    This method is called when all drawing has been completed and the
    program is about to exit.

    """
    default_prog.delete()
    fbuffer_prog.delete()
    fbuffer.delete()

## RENDERING FUNTIONS + HELPERS
##
## These are responsible for actually rendring things to the screen.
## For some draw call the methods should be called as follows:
##
##    with draw_loop():
##        # multiple calls to render()
##

def render_image(image, location, size):
    """Render the image.

    :param image: image to be rendered
    :type image: p5.Image

    :param location: top-left corner of the image
    :type location: tuple | list | p5.Vector

    :param size: target size of the image to draw.
    :type size: tuple | list | p5.Vector
    """
    flush_geometry()

    texture_prog['fill_color'] = tint_color if tint_enabled else COLOR_WHITE
    texture_prog['transform'] = transform_matrix.T.flatten()

    x, y = location
    sx, sy = size
    imx, imy = image.size
    data = np.zeros(4,
                    dtype=[('position', np.float32, 2),
                           ('texcoord', np.float32, 2)])
    data['texcoord'] = np.array([[0.0, 1.0],
                                 [1.0, 1.0],
                                 [0.0, 0.0],
                                 [1.0, 0.0]],
                                dtype=np.float32)
    data['position'] = np.array([[x, y + sy],
                                 [x + sx, y + sy],
                                 [x, y],
                                 [x + sx, y]],
                                dtype=np.float32)

    texture_prog['texture'] = image._texture
    texture_prog.bind(VertexBuffer(data))
    texture_prog.draw('triangle_strip')

def flush_geometry():
    """Flush all the shape geometry from the draw queue to the GPU.
    """
    global poly_draw_queue
    global line_draw_queue
    global point_draw_queue

    ## RETAINED MODE RENDERING.
    #
    names = ['poly', 'line', 'point']
    types = ['triangles', 'lines', 'points']
    queues = [poly_draw_queue, line_draw_queue, point_draw_queue]

    for draw_type, draw_queue, name in zip(types, queues, names):
        # 1. Get the maximum number of vertices persent in the shapes
        # in the draw queue.
        #
        if len(draw_queue) == 0:
            continue

        num_vertices = 0
        for vertices, _, _ in draw_queue:
            num_vertices = num_vertices + len(vertices)

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
        for vertices, idx, color in draw_queue:
            num_shape_verts = len(vertices)

            data['position'][sidx:(sidx + num_shape_verts),] = vertices

            color_array = np.array([color] * num_shape_verts)
            data['color'][sidx:sidx + num_shape_verts, :] = color_array

            draw_indices.append(sidx + idx)

            sidx += num_shape_verts

        vertex_buffer.set_data(data)
        index_buffer.set_data(np.hstack(draw_indices))

        # 4. Bind the buffer to the shader.
        #
        default_prog.bind(vertex_buffer)

        # 5. Draw the shape using the proper shape type and get rid of
        # the buffers.
        #
        default_prog.draw(draw_type, indices=index_buffer)

    # 6. Empty the draw queue.
    poly_draw_queue = []
    line_draw_queue = []
    point_draw_queue = []

@contextmanager
def draw_loop():
    """The main draw loop context manager.
    """
    global transform_matrix

    global fbuffer_tex_front
    global fbuffer_tex_back

    transform_matrix = np.identity(4)

    default_prog['modelview'] = modelview_matrix.T.flatten()
    default_prog['projection'] = projection_matrix.T.flatten()

    fbuffer.color_buffer = fbuffer_tex_back

    with fbuffer:
        gloo.set_viewport(*texture_viewport)
        _comm_toggles()
        fbuffer_prog['texture'] = fbuffer_tex_front
        fbuffer_prog.draw('triangle_strip')

        yield

        flush_geometry()

    gloo.set_viewport(*viewport)
    _comm_toggles(False)
    clear()
    fbuffer_prog['texture'] = fbuffer_tex_back
    fbuffer_prog.draw('triangle_strip')

    fbuffer_tex_front, fbuffer_tex_back = fbuffer_tex_back, fbuffer_tex_front

def add_to_draw_queue(stype, vertices, edges, faces, fill=None, stroke=None):
    """Add the given vertex data to the draw queue.

    :param stype: type of shape to be added. Should be one of {'poly',
        'path', 'point'}
    :type stype: str

    :param vertices: (N, 3) array containing the vertices to be drawn.
    :type vertices: np.ndarray

    :param edges: (N, 2) array containing edges as tuples of indices
        into the vertex array. This can be None when not appropriate
        (eg. for points)
    :type edges: None | np.ndarray

    :param faces: (N, 3) array containing faces as tuples of indices
        into the vertex array. For 'point' and 'path' shapes, this can
        be None
    :type faces: np.ndarray

    :param fill: Fill color of the shape as a normalized RGBA tuple.
        When set to `None` the shape doesn't get a fill (default: None)
    :type fill: None | tuple

    :param stroke: Stroke color of the shape as a normalized RGBA
        tuple. When set to `None` the shape doesn't get stroke
        (default: None)
    :type stroke: None | tuple

    """
    global poly_draw_queue
    global line_draw_queue
    global point_draw_queue

    fill_shape = fill_enabled and not (fill is None)
    stroke_shape = stroke_enabled and not (stroke is None)

    if fill_shape and stype not in ['point', 'path']:
        idx = np.array(faces, dtype=np.uint32).ravel()
        poly_draw_queue.append((vertices, idx, fill))

    if stroke_shape:
        if stype == 'point':
            idx = np.arange(0, len(vertices), dtype=np.uint32)
            point_draw_queue.append((vertices, idx, stroke))
        else:
            idx = np.array(edges, dtype=np.uint32).ravel()
            line_draw_queue.append((vertices, idx, stroke))

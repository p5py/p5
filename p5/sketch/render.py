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
"""Main OpenGL renderer for p5.
"""

import builtins
import math

import numpy as np
from vispy import gloo

from ..pmath import matrix
from .shaders import src_default
from .shaders import src_fbuffer
from .shaders import src_texture

COLOR_WHITE = (1, 1, 1, 1)
COLOR_BLACK = (0, 0, 0, 1)
COLOR_DEFAULT_BG = (0.8, 0.8, 0.8, 1.0)

# vertex and texture coordinates for blitting the framebuffers to the
# window
_fbuf_verts = np.array([[-1, -1], [1, -1], [-1, 1], [1, 1]], dtype=np.float32)
_fbuf_texcs = np.array([[0, 0], [1, 0], [0, 1], [1, 1]], dtype=np.float32)

class Renderer:
    """Main class for an OpenGL renderer.

    Note :: All colors are expected to be 4-tuples with normalized
        RGBA float values.

    :param size: the size (width, height) of the renderer
    :type size: tuple
    
    :param pixel_density: the pixel density (x_density, y_density) of the
        renderer (default: (1, 1))
    :type pixel_density: tuple

    :param background: default background color of the renderer
        (default: Processing's (JAVA) 20% gray).
    :type background: tuple

    :param fill: initial fill color of the renderer (default: white)
    :type fill: tuple

    :param stroke: initial stroke color of the renderer (default:
       black)
    :type stroke: tuple

    """
    def __init__(self, size, pixel_density=(1, 1),
                 background=COLOR_DEFAULT_BG, fill=COLOR_WHITE,
                 stroke=COLOR_BLACK):
        self.background_color = background
        self.fill_enabled = not (fill is None)
        self.fill_color = fill if self.fill_enabled else COLOR_WHITE
        self.stroke_enabled = not (stroke is None)
        self.stroke_color = stroke if self.stroke_enabled else COLOR_BLACK

        self.modelview = np.identity(4)
        self.projection = np.identity(4)
        self.transform = np.identity(4)

        self._size = size
        self._pixel_density = pixel_density

        self.fbuffer_prog = gloo.Program(src_fbuffer.vert, src_fbuffer.frag)
        self.fbuffer_prog['position'] = gloo.VertexBuffer(data=_fbuf_verts)
        self.fbuffer_prog['texcoord'] = gloo.VertexBuffer(data=_fbuf_texcs)

        self.default_prog = gloo.Program(src_default.vert, src_default.frag)

        # TODO: Check if the machine actually supports FrameBuffer
        # rendering.
        self.fbuffer = gloo.FrameBuffer()

        self._draw_queues = dict.fromkeys(['poly', 'line', 'point'], [])

        self.reset()

    def reset(self):
        """Reset the renderer and regenerate required Textures.
        """
        gloo.set_viewport(*self.physical_viewport)

        width, height = self.size

        aspect_ratio = width / height
        cz = (height / 2) / math.tan(math.radians(30))
        self.projection = matrix.perspective_matrix(
            math.radians(60), aspect_ratio, 0.1 * cz, 10 * cz)

        self.modelview = matrix.translation_matrix(-width / 2, height / 2, -cz)
        self.modelview = self.modelview.dot(matrix.scale_transform(1, -1, 1))

        self.transform = np.identity(4)

        self.default_prog['modelview'] = self.modelview.T.flatten()
        self.default_prog['projection'] = self.projection.T.flatten()

        self.fbuffer_tex_front = gloo.Texture2D((height, width, 3))
        self.fbuffer_tex_back = gloo.Texture2D((height, width, 3))
        
    def _comm_toggles(self, state=True):
        gloo.set_state(blend=state)
        gloo.set_state(depth_test=state)

        if state:
            gloo.set_state(blend_func=('src_alpha', 'one_minus_src_alpha'))
            gloo.set_state(depth_func='lequal')

    def clear(self, color=True, depth=True):
        """Clear the renderer background.

        :param color: whether the color buffer should be cleared.
        :type color: bool

        :param depth: whether the depth buffer should be cleared
        :type depth: bool

        """
        gloo.set_state(clear_color=self.background_color)
        gloo.clear(color=color, depth=depth)

    def __enter__(self):
        self.transform = np.identity(4)

        # TODO: maybe not needed?
        self.default_prog['modelview'] = self.modelview.T.flatten()
        self.default_prog['projection'] = self.projection.T.flatten()

        self.fbuffer.color_buffer = self.fbuffer_tex_back
        self.fbuffer.activate()

        gloo.set_viewport(*self.texture_viewport)
        self._comm_toggles()
        self.fbuffer_prog['texture'] = self.fbuffer_tex_front
        self.fbuffer_prog.draw('triangle_strip')

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self._flush_geometry()
        self.fbuffer.deactivate()

        # blit the back-texture to the screen
        gloo.set_viewport(*self.physical_viewport)
        self._comm_toggles()
        self.clear()
        self.fbuffer_prog['texture'] = self.fbuffer_tex_back
        self.fbuffer_prog.draw('triangle_strip')

        # swap the front and the back buffers.
        self.fbuffer_tex_front, self.fbuffer_tex_back = \
            self.fbuffer_tex_back, self.fbuffer_tex_front

        return False

    def add_to_queue(self, shape):
        """Add the given shape to the main draw queue.
        
        :param shape: The shape to be added to the draw queue.
        :type shape: p5.Shape
        
        """
        shape.transform(self.transform)

        if self.fill_enabled and shape.kind not in ['POINT', 'PATH']:
            self._draw_queues['poly'].append((shape, self.fill_color))

        if self.stroke_enabled:
            if shape.kind == 'POINT':
                self._draw_queues['point'].append((shape, self.stroke_color))
            else:
                self._draw_queues['line'].append((shape, self.stroke_color))

    def _flush_geometry(self):
        """Flush all the shape geometry from the draw queue to the GPU.
        """
        ## RETAINED MODE RENDERING.
        #
        names = ['poly', 'line', 'point']
        types = ['triangles', 'lines', 'points']

        for draw_type, name in zip(types, names):
            # 1. Get the maximum number of vertices persent in the shapes
            # in the draw queue.
            #
            draw_queue = self._draw_queues[name]
            if len(draw_queue) == 0:
                continue

            num_vertices = 0
            for shape, _ in draw_queue:
                num_vertices = num_vertices + len(shape.vertices)

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

            # TODO: *do not* regenerate these buffers on each draw
            # call and have common buffers for the whole renderer.
            V = gloo.VertexBuffer(data)
            I = gloo.IndexBuffer(np.hstack(draw_indices))

            # 4. Bind the buffer to the shader.
            #
            self.default_prog.bind(V)

            # 5. Draw the shape using the proper shape type and get rid of
            # the buffers.
            #
            self.default_prog.draw(draw_type, indices=I)

            V.delete()
            I.delete()

        # 6. Empty the draw queue.
        #
        self._draw_queues = dict.fromkeys(['poly', 'line', 'point'], [])

    @property
    def size(self):
        """Size of the renderer.

        :rtype: tuple
        """
        return self._size

    @size.setter
    def size(self, new_size):
        self._size = new_size
        self.reset()

    @property
    def pixel_density(self):
        """Pixel density of the renderer

        :rtype: tuple
        """
        return self._pixel_density

    @pixel_density.setter
    def pixel_density(self, new_density):
        self._pixel_density = new_density
        self.reset()

    @property
    def physical_size(self):
        """Actual size of the renderer (taking into account the pixel density)

        :rtype: tuple

        """
        return (self._size[0] * self._pixel_density[0],
                self._size[1] * self._pixel_density[1])

    @property
    def physical_viewport(self):
        """The physical viewport in pixels.

        :rtype: tuple

        """
        px, py = self.physical_size
        return (0, 0, px, py)

    @property
    def texture_viewport(self):
        """The viewport to blit the textures to.

        :rtype: tuple

        """
        sx, sy = self.size
        return (0, 0, sx, sy)

    def __del__(self):
        self.default_prog.delete()
        self.fbuffer_prog.delete()
        self.fbuffer.delete()

    def __repr__(self):
        return "Renderer(size=({}, {}))".format(self.width, self.height)

    __str__ = __repr__

    





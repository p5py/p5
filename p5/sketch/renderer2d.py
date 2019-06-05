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

import numpy as np
import math
from ..pmath import matrix

from vispy import gloo
from vispy.gloo import FrameBuffer
from vispy.gloo import IndexBuffer
from vispy.gloo import Program
from vispy.gloo import RenderBuffer
from vispy.gloo import Texture2D
from vispy.gloo import VertexBuffer

from contextlib import contextmanager

from ..core import p5
from ..core.constants import *

from .shaders import src_default
from .shaders import src_fbuffer
from .shaders import src_texture
from .shaders import src_line

class Renderer2D:
	def __init__(self):
		self.default_prog = None
		self.fbuffer_prog = None
		self.texture_prog = None
		self.line_prog = None

		self.fbuffer = None
		self.fbuffer_tex_front = None
		self.fbuffer_tex_back = None

		self.vertex_buffer = None
		self.index_buffer = None

		## Renderer Globals: USEFUL CONSTANTS
		self.COLOR_WHITE = (1, 1, 1, 1)
		self.COLOR_BLACK = (0, 0, 0, 1)
		self.COLOR_DEFAULT_BG = (0.8, 0.8, 0.8, 1.0)

		## Renderer Globals: STYLE/MATERIAL PROPERTIES
		##
		self.background_color = self.COLOR_DEFAULT_BG

		self.fill_color = self.COLOR_WHITE
		self.fill_enabled = True

		self.stroke_color = self.COLOR_BLACK
		self.stroke_enabled = True

		self.tint_color = self.COLOR_BLACK
		self.tint_enabled = False

		## Renderer Globals: Curves
		self.stroke_weight = 1
		self.stroke_cap = PROJECT
		self.stroke_join = MITER

		## Renderer Globals
		## VIEW MATRICES, ETC
		##
		self.viewport = None
		self.texture_viewport = None
		self.transform_matrix = np.identity(4)
		self.modelview_matrix = np.identity(4)
		self.projection_matrix = np.identity(4)



		## Renderer Globals: RENDERING
		self.poly_draw_queue = []
		self.line_draw_queue = []
		self.point_draw_queue = []
		self.draw_queue = []

	def initialize_renderer(self):
		self.fbuffer = FrameBuffer()

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

		self.fbuf_vertices = VertexBuffer(data=vertices)
		self.fbuf_texcoords = VertexBuffer(data=texcoords)

		self.fbuffer_prog = Program(src_fbuffer.vert, src_fbuffer.frag)
		self.fbuffer_prog['texcoord'] = self.fbuf_texcoords
		self.fbuffer_prog['position'] = self.fbuf_vertices

		self.vertex_buffer = VertexBuffer()
		self.index_buffer = IndexBuffer()

		self.default_prog = Program(src_default.vert, src_default.frag)
		self.texture_prog = Program(src_texture.vert, src_texture.frag)
		self.texture_prog['texcoord'] = self.fbuf_texcoords

		self.reset_view()

	def reset_view(self):
		self.viewport = (
			0,
			0,
			int(p5.width * p5.pixel_x_density),
			int(p5.height * p5.pixel_y_density),
		)
		self.texture_viewport = (
			0,
			0,
			p5.width,
			p5.height,
		)

		gloo.set_viewport(*self.viewport)

		cz = (p5.height / 2) / math.tan(math.radians(30))
		self.projection_matrix = matrix.perspective_matrix(
			math.radians(60),
			p5.width / p5.height,
			0.1 * cz,
			10 * cz
		)
		self.modelview_matrix = matrix.translation_matrix(-p5.width / 2, \
													 p5.height / 2, \
													 -cz)
		self.modelview_matrix = self.modelview_matrix.dot(matrix.scale_transform(1, -1, 1))

		self.transform_matrix = np.identity(4)

		self.default_prog['modelview'] = self.modelview_matrix.T.flatten()
		self.default_prog['projection'] = self.projection_matrix.T.flatten()

		self.texture_prog['modelview'] = self.modelview_matrix.T.flatten()
		self.texture_prog['projection'] = self.projection_matrix.T.flatten()

		self.line_prog = Program(src_line.vert, src_line.frag)

		self.line_prog['modelview'] = self.modelview_matrix.T.flatten()
		self.line_prog['projection'] = self.projection_matrix.T.flatten()

		self.fbuffer_tex_front = Texture2D((p5.height, p5.width, 3))
		self.fbuffer_tex_back = Texture2D((p5.height, p5.width, 3))

		print(self.modelview_matrix)
		print(self.projection_matrix)

		for buf in [self.fbuffer_tex_front, self.fbuffer_tex_back]:
			self.fbuffer.color_buffer = buf
			with self.fbuffer:
				self.clear()

	def clear(self, color=True, depth=True):
		"""Clear the renderer background."""
		gloo.set_state(clear_color=self.background_color)
		gloo.clear(color=color, depth=depth)

	def _comm_toggles(self, state=True):
		gloo.set_state(blend=state)
		gloo.set_state(depth_test=state)

		if state:
			gloo.set_state(blend_func=('src_alpha', 'one_minus_src_alpha'))
			gloo.set_state(depth_func='lequal')

	@contextmanager
	def draw_loop(self):
		"""The main draw loop context manager.
		"""

		self.transform_matrix = np.identity(4)

		self.default_prog['modelview'] = self.modelview_matrix.T.flatten()
		self.default_prog['projection'] = self.projection_matrix.T.flatten()

		self.fbuffer.color_buffer = self.fbuffer_tex_back

		with self.fbuffer:
			gloo.set_viewport(*self.texture_viewport)
			self._comm_toggles()
			self.fbuffer_prog['texture'] = self.fbuffer_tex_front
			self.fbuffer_prog.draw('triangle_strip')

			yield

			self.flush_geometry()

		gloo.set_viewport(*self.viewport)
		self._comm_toggles(False)
		self.clear()
		self.fbuffer_prog['texture'] = self.fbuffer_tex_back
		self.fbuffer_prog.draw('triangle_strip')

		self.fbuffer_tex_front, self.fbuffer_tex_back = self.fbuffer_tex_back, self.fbuffer_tex_front


	def _transform_vertices(self, vertices, local_matrix, global_matrix):
		return np.dot(np.dot(vertices, local_matrix.T), global_matrix.T)[:, :3]

	def render(self, shape):
		vertices = shape._draw_vertices
		n, _ = vertices.shape
		tverts = self._transform_vertices(
			np.hstack([vertices, np.zeros((n, 1)), np.ones((n, 1))]),
			shape._matrix,
			self.transform_matrix)
		fill = shape.fill.normalized if shape.fill else None
		stroke = shape.stroke.normalized if shape.stroke else None

		edges = shape._draw_edges
		faces = shape._draw_faces

		if edges is None:
			print(vertices)
			print("whale")
			exit()

		if 'open' in shape.attribs:
			overtices = shape._draw_outline_vertices
			no, _  = overtices.shape
			toverts = self._transform_vertices(
				np.hstack([overtices, np.zeros((no, 1)), np.ones((no, 1))]),
				shape._matrix,
				self.transform_matrix)


			self.add_to_draw_queue('path', toverts, shape._draw_outline_edges,
							  None, None, stroke)
			self.add_to_draw_queue('poly', tverts, edges, faces, fill, None)
		else:
			self.add_to_draw_queue(shape.kind, tverts, edges, faces, fill, stroke)

	def add_to_draw_queue(self, stype, vertices, edges, faces, fill=None, stroke=None):
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

		fill_shape = self.fill_enabled and not (fill is None)
		stroke_shape = self.stroke_enabled and not (stroke is None)

		if fill_shape and stype not in ['point', 'path']:
			idx = np.array(faces, dtype=np.uint32).ravel()
			self.draw_queue.append(["triangles", (vertices, idx, fill)])

		if stroke_shape:
			if stype == 'point':
				idx = np.arange(0, len(vertices), dtype=np.uint32)
				self.draw_queue.append(["points", (vertices, idx, stroke)])
			else:
				idx = np.array(edges, dtype=np.uint32).ravel()
				self.draw_queue.append(["lines", (vertices, idx, stroke, self.stroke_weight)])

	def flush_geometry(self):
		"""Flush all the shape geometry from the draw queue to the GPU.
		"""
		for shape in self.draw_queue:
			if shape[0] == "point" or shape[0] == "triangles":
				self.render_default(shape[0], shape[1])
			elif shape[0] == "lines":
				self.render_line(shape[1])

		self.draw_queue = []

	def render_default(self, draw_type, queue):

		# 1. Get the maximum number of vertices persent in the shapes
		# in the draw queue.
		#
		if len(queue) == 0:
			return

		num_vertices = len(queue[0])
		
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
		
		vertices, idx, color = queue
		num_shape_verts = len(vertices)

		data['position'][sidx:(sidx + num_shape_verts),] = vertices

		color_array = np.array([color] * num_shape_verts)
		data['color'][sidx:sidx + num_shape_verts, :] = color_array

		draw_indices.append(idx)

		self.vertex_buffer.set_data(data)
		self.index_buffer.set_data(np.hstack(draw_indices))

		# 4. Bind the buffer to the shader.
		#
		self.default_prog.bind(self.vertex_buffer)

		# 5. Draw the shape using the proper shape type and get rid of
		# the buffers.
		#
		self.default_prog.draw(draw_type, indices=self.index_buffer)

	def render_line(self, vertices):
		self.line_prog["color"] = vertices[2]
		vertex = vertices[0]

		p0 = []
		p1 = []
		p2 = []

		positions0 = []
		positions1 = []
		positions2 = []
		markers = []

		for i in range(len(vertex)):
			if i == 0:
				positions0.extend([vertex[i], vertex[i], vertex[i + 1]])
				positions0.extend([vertex[i + 1], vertex[i + 1], vertex[i]])

				positions1.extend([vertex[i], vertex[i], vertex[i + 1]])
				positions1.extend([vertex[i + 1], vertex[i + 1], vertex[i]])

				positions2.extend([vertex[i + 1], vertex[i + 1], vertex[i]])
				positions2.extend([vertex[i], vertex[i], vertex[i + 1]])

			elif i == len(vertex) - 1:
				continue
				positions0.extend([vertex[i + 1], vertex[i + 1], vertex[i - 1]])
				positions0.extend([vertex[i - 1], vertex[i - 1], vertex[i + 1]])

				positions1.extend([vertex[i], vertex[i], vertex[i + 1]])
				positions1.extend([vertex[i + 1], vertex[i + 1], vertex[i]])

				positions2.extend([vertex[i], vertex[i], vertex[i + 1]])
				positions2.extend([vertex[i + 1], vertex[i + 1], vertex[i]])

			else:
				positions0.extend([vertex[i - 1], vertex[i - 1], vertex[i + 1]])
				positions0.extend([vertex[i + 1], vertex[i + 1], vertex[i - 1]])

				positions1.extend([vertex[i], vertex[i], vertex[i + 1]])
				positions1.extend([vertex[i + 1], vertex[i + 1], vertex[i]])

				positions2.extend([vertex[i + 1], vertex[i + 1], vertex[i]])
				positions2.extend([vertex[i], vertex[i], vertex[i + 1]])

			markers.extend([1, -1, 1])
			markers.extend([1, -1, 1])

		positions0 = np.array(positions0, np.float32)
		positions1 = np.array(positions1, np.float32)
		positions2 = np.array(positions2, np.float32)
		markers = np.array(markers, np.float32)

		self.line_prog['position0'] = gloo.VertexBuffer(positions0)
		self.line_prog['position1'] = gloo.VertexBuffer(positions1)
		self.line_prog['position2'] = gloo.VertexBuffer(positions2)
		self.line_prog['marker'] = gloo.VertexBuffer(markers)
		self.line_prog['linewidth'] = gloo.VertexBuffer([vertices[3]]*len(markers))

		self.line_prog.draw('triangles')

	def render_image(self, image, location, size):
		"""Render the image.

		:param image: image to be rendered
		:type image: p5.Image

		:param location: top-left corner of the image
		:type location: tuple | list | p5.Vector

		:param size: target size of the image to draw.
		:type size: tuple | list | p5.Vector
		"""
		self.flush_geometry()

		self.texture_prog['fill_color'] = self.tint_color if self.tint_enabled else self.COLOR_WHITE
		self.texture_prog['transform'] = self.transform_matrix.T.flatten()

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

		self.texture_prog['texture'] = image._texture
		self.texture_prog.bind(VertexBuffer(data))
		self.texture_prog.draw('triangle_strip')

	def cleanup(self):
		"""Run the clean-up routine for the renderer.

		This method is called when all drawing has been completed and the
		program is about to exit.

		"""
		self.default_prog.delete()
		self.fbuffer_prog.delete()
		self.line_prog.delete()
		self.fbuffer.delete()


#
# Part of p5: A Python package based on Processing
# Copyright (C) 2017-2019 Abhik Pal
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
from numpy.linalg import inv
import math
from ..pmath import matrix

import builtins

from vispy import gloo
from vispy.gloo import Texture2D

from contextlib import contextmanager

from ..core.constants import Z_EPSILON
from ..core.geometry import Geometry
from ..core.shape import PShape

from ..pmath.matrix import translation_matrix
from .openglrenderer import OpenGLRenderer

class Renderer3D(OpenGLRenderer):
	def __init__(self):
		super().__init__()
		self.lookat_matrix = np.identity(4)

	def initialize_renderer(self):
		super().initialize_renderer()
		self.reset_view()

	def reset_view(self):
		self.viewport = (
			0,
			0,
			int(builtins.width * builtins.pixel_x_density),
			int(builtins.height * builtins.pixel_y_density),
		)
		self.texture_viewport = (
			0,
			0,
			builtins.width,
			builtins.height,
		)

		gloo.set_viewport(*self.viewport)

		cz = (builtins.height / 2) / math.tan(math.radians(30))
		self.projection_matrix = matrix.perspective_matrix(
			math.radians(60),
			builtins.width / builtins.height,
			0.1 * cz,
			10 * cz
		)

		self.transform_matrix = np.identity(4)

		self.default_prog['projection'] = self.projection_matrix.T.flatten()
		self.default_prog['perspective_matrix'] = self.lookat_matrix.T.flatten()

		self.fbuffer_tex_front = Texture2D((builtins.height, builtins.width, 3))
		self.fbuffer_tex_back = Texture2D((builtins.height, builtins.width, 3))

		for buf in [self.fbuffer_tex_front, self.fbuffer_tex_back]:
			self.fbuffer.color_buffer = buf
			with self.fbuffer:
				self.clear()

		self.fbuffer.depth_buffer = gloo.RenderBuffer((builtins.height, builtins.width))

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

		self.default_prog['projection'] = self.projection_matrix.T.flatten()
		self.default_prog['perspective_matrix'] = self.lookat_matrix.T.flatten()

		self.fbuffer.color_buffer = self.fbuffer_tex_back

		with self.fbuffer:
			gloo.set_viewport(*self.texture_viewport)
			self._comm_toggles()
			self.fbuffer_prog['texture'] = self.fbuffer_tex_front
			self.fbuffer_prog.draw('triangle_strip')

			yield

			self.flush_geometry()
			self.transform_matrix = np.identity(4)

		gloo.set_viewport(*self.viewport)
		self._comm_toggles(False)
		self.clear()
		self.fbuffer_prog['texture'] = self.fbuffer_tex_back
		self.fbuffer_prog.draw('triangle_strip')

		self.fbuffer_tex_front, self.fbuffer_tex_back = self.fbuffer_tex_back, self.fbuffer_tex_front

	def render(self, shape):
		if isinstance(shape, Geometry):
			n = len(shape.vertices)
			tverts = self._transform_vertices(
				np.hstack([shape.vertices, np.ones((n, 1))]),
				shape.matrix,
				self.transform_matrix)

			edges = shape.edges
			faces = shape.faces

			self.add_to_draw_queue('poly', tverts, edges, faces, self.fill_color, self.stroke_color)

		elif isinstance(shape, PShape):
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

				self.add_to_draw_queue('poly', tverts, edges, faces, fill, None)
				self.add_to_draw_queue('path', toverts, edges[:-1],
								  None, None, stroke)
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
				self.draw_queue.append(["lines", (vertices, idx, stroke)])

	def flush_geometry(self):
		"""Flush all the shape geometry from the draw queue to the GPU.
		"""
		current_queue = []
		for index, shape in enumerate(self.draw_queue):
			current_shape, current_obj = self.draw_queue[index][0], self.draw_queue[index][1]
			# If current_shape is lines, bring it to the front by epsilon
			# to resolve z-fighting
			if current_shape == 'lines':
				# line_transform is used whenever we render lines to break ties in depth
				# We transform the points to camera space, move them by Z_EPSILON, and them move them back to world space
				line_transform = inv(self.lookat_matrix).dot(translation_matrix(0, 0, Z_EPSILON).dot(self.lookat_matrix))
				vertices = current_obj[0]
				current_obj = (np.hstack([vertices, np.ones((vertices.shape[0], 1))]).dot(line_transform.T)[:, :3],
								current_obj[1], current_obj[2])
			current_queue.append(current_obj)

			if index < len(self.draw_queue) - 1:
				if self.draw_queue[index][0] == self.draw_queue[index + 1][0]:
					continue

			self.render_default(current_shape, current_queue)
			current_queue = []

		self.draw_queue = []

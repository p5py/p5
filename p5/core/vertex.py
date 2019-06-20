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

from . import p5
from . import primitives
from .shape import PShape

from ..pmath import curves

shape_kind = None
vertices = [] # stores the vertex coordinates
vertices_types = [] # stores the type of vertex. Eg: bezier, curve, etc
contour_vertices = []
contour_vertices_types = []
is_bezier = False
is_curve = False
is_quadratic = False
is_contour = False
is_first_contour = True

def begin_shape(kind=None):
	global shape_kind, vertices, contour_vertices, vertices_types, contour_vertices_types
	if (
		kind == "POINTS" or
		kind == "LINES" or
		kind == "TRIANGLES" or
		kind == "TRIANGLE_FAN" or
		kind == "TRIANGLE_STRIP" or 
		kind == "QUADS" or 
		kind == "QUAD_STRIP"
		):
		shape_kind = kind
	else:
		shape_kind = None

	vertices = []
	contour_vertices = []
	vertices_types = []
	contour_vertices_types = []

def curve_vertex(x, y):
	global is_curve, vertices, contour_vertices, vertices_types, contour_vertices_types
	is_curve = True

	if p5.mode == "3D":
		return
	else:
		if is_contour:
			contour_vertices.append((x, y))
			contour_vertices_types.append(2)
		else:
			vertices.append((x, y)) # False attribute if the vertex is 
			vertices_types.append(2)

def bezier_vertex(x2, y2, x3, y3, x4, y4):
	global is_bezier, vertices, contour_vertices, vertices_types, contour_vertices_types
	is_bezier = True

	if p5.mode == "3D":
		return
	else:
		if is_contour:
			contour_vertices.append((x2, y2, x3, y3, x4, y4))
			contour_vertices_types.append(3)
		else:
			vertices.append((x2, y2, x3, y3, x4, y4)) 
			vertices_types.append(3)

def quadratic_vertex(cx, cy, x3, y3):
	global is_quadratic, vertices, contour_vertices, vertices_types, contour_vertices_types
	is_quadratic = True

	if p5.mode == "3D":
		return
	else:
		if is_contour:
			contour_vertices.append((cx, cy, x3, y3))
			contour_vertices_types.append(4)
		else:
			vertices.append((cx, cy, x3, y3)) 
			vertices_types.append(3)

def vertex(x, y):
	global vertices, contour_vertices, vertices_types, contour_vertices_types
	if p5.mode == "3D":
		return
	else:
		if is_contour:
			contour_vertices.append((x, y))
			contour_vertices_types.append(1)
		else:
			vertices.append((x, y))
			vertices_types.append(1)

@primitives._draw_on_return
def end_shape(mode=""):
	global vertices, is_bezier, is_curve, is_quadratic, is_contour, shape_kind

	if len(vertices) == 0:
		return

	if (not p5.renderer.stroke_enabled) and (not p5.renderer.fill_enabled):
		return

	close_shape = mode == "CLOSE"

	# if the shape is closed, the first element is also the last element
	if close_shape and (not is_contour):
		vertices.append(vertices[0])

	shape = PShape([(0,0)])
	if is_curve and (shape_kind == "POLYGON" or shape_kind == None):
		if len(vertices) > 3:
			b = []
			s = 1 - curves.curve_tightness_amount
			shape_vertices = [(vertices[1][0], vertices[1][1], 0.0)]
			steps = curves.curve_resolution

			for i in range(1, len(vertices) - 2):
				v = vertices[i]
				start = (shape_vertices[len(shape_vertices) - 1][0], shape_vertices[len(shape_vertices) - 1][1])
				c1 = [
					v[0] + (s * vertices[i + 1][0] - s * vertices[i - 1][0]) / 6,
					v[1] + (s * vertices[i + 1][1] - s * vertices[i - 1][1]) / 6
				]
				c2 = [
					vertices[i + 1][0] +
					(s * vertices[i][0] - s * vertices[i + 2][0]) / 6,
					vertices[i + 1][1] + (s * vertices[i][1] - s * vertices[i + 2][1]) / 6
				]
				stop = [vertices[i + 1][0], vertices[i + 1][1]]
				
				for i in range(steps + 1):
					t = i / steps
					p = curves.bezier_point(start, c1, c2, stop, t)
					shape_vertices.append(p[:3])

			shape.add_child(PShape(shape_vertices))
	elif is_bezier and (shape_kind == "POLYGON" or shape_kind == None):
		shape_vertices = []
		steps = curves.curve_resolution
		for i in range(len(vertices)):
			if vertices_types[i] == 1 or vertices_types[i] == 2:
				shape_vertices.append((vertices[i][0], vertices[i][1], 0.0))
			else:
				start = (shape_vertices[len(shape_vertices) - 1][0], shape_vertices[len(shape_vertices) - 1][1])
				c1 = [vertices[i][0], vertices[i][1]]
				c2 = [vertices[i][2], vertices[i][3]]
				stop = [vertices[i][4], vertices[i][5]]

				for i in range(steps + 1):
						t = i / steps
						p = curves.bezier_point(start, c1, c2, stop, t)
						shape_vertices.append(p[:3])

		shape.add_child(PShape(shape_vertices))
	elif is_quadratic and (shape_kind == "POLYGON" or shape_kind == None):
		shape_vertices = []
		steps = curves.curve_resolution
		for i in range(len(vertices)):
			if vertices_types[i] == 1 or vertices_types[i] == 2:
				shape_vertices.append((vertices[i][0], vertices[i][1], 0.0))
			else:
				start = (shape_vertices[len(shape_vertices) - 1][0], shape_vertices[len(shape_vertices) - 1][1])
				control = [vertices[i][0], vertices[i][1]]
				stop = [vertices[i][2], vertices[i][3]]

				for i in range(steps + 1):
						t = i / steps
						p = curves.quadratic_point(start, control, stop, t)
						shape_vertices.append(p[:3])

		shape.add_child(PShape(shape_vertices))
	else:
		if shape_kind == "POINTS":
			shape.add_child(PShape(vertices, attribs='point'))
		elif shape_kind == "LINES":
			if len(vertices) < 2:
				raise ValueError("Insufficient number of vertices %s" % (len(vertices)))
			else:
				for i in range(0, len(vertices), 2):
					shape.add_child(PShape([vertices[i], vertices[i + 1]], attribs='path'))
		elif shape_kind == "TRIANGLES":
			if len(vertices) < 3:
				raise ValueError("Insufficient number of vertices %s" % (len(vertices)))
			else:
				for i in range(0, len(vertices) - 2, 3):
					shape.add_child(PShape([vertices[i], vertices[i + 1], vertices[i + 2]]))
		elif shape_kind == "TRIANGLE_STRIP":
			if len(vertices) < 3:
				raise ValueError("Insufficient number of vertices %s" % (len(vertices)))
			else:
				for i in range(0, len(vertices) - 2, 1):
					print(i)
					shape.add_child(PShape([vertices[i], vertices[i + 1], vertices[i + 2]]))
		elif shape_kind == "TRIANGLE_FAN":
			if len(vertices) < 3:
				raise ValueError("Insufficient number of vertices %s" % (len(vertices)))
			else:
				for i in range(1, len(vertices) - 1):
					shape.add_child(PShape([vertices[0], vertices[i], vertices[i + 1]]))
		elif shape_kind == "QUADS":
			if len(vertices) < 4:
				raise ValueError("Insufficient number of vertices %s" % (len(vertices)))
			else:
				for i in range(0, len(vertices) - 3, 4):
					shape.add_child(PShape([vertices[i], vertices[i + 1], vertices[i + 2], vertices[i + 3]]))
		elif shape_kind == "QUAD_STRIP":
			if len(vertices) < 4:
				raise ValueError("Insufficient number of vertices %s" % (len(vertices)))
			else:
				for i in range(0, len(vertices) - 2, 2):
					shape.add_child(PShape([vertices[i], vertices[i + 1], vertices[i + 3], vertices[i + 2]]))
		else:
			shape.add_child(PShape(vertices))

	is_bezier = False
	is_curve = False
	is_quadratic = False
	is_contour = False
	is_first_contour = True
	 
	return shape

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

shape_kind = None
vertices = []
contour_vertices = []
is_bezier = False
is_curve = False
is_quadratic = False
is_contour = False
is_first_contour = True

def begin_shape(kind=None):
	global shape_kind, vertices, contour_vertices
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

def vertex(x, y):
	global vertices
	if p5.mode == "3D":
		return
	else:
		if is_contour:
			contour_vertices.append((x, y))
		else:
			vertices.append((x, y))

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

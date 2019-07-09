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

from . import PShape
import xml.etree.ElementTree as etree
from ..pmath import Point
from . import primitives

def parse_rect(element):
	width = float(element.get('width'))
	height = float(element.get('height'))
	x = float(element.get('x'))
	y = float(element.get('y'))

	return PShape([
		(x, y),
		(x + width, y),
		(x + width, y + height),
		(x, y + height)
		], children=[])

def parse_circle(element):
	cx = float(element.get('cx'))
	cy = float(element.get('cy')) 
	r = float(element.get('r'))
	return primitives.circle((cx, cy), r)

def parse_line(element):
	x1 = float(element.get('x1'))
	y1 = float(element.get('y1'))
	x2 = float(element.get('x2'))
	y2 = float(element.get('y2'))
	return PShape([(x1, y1), (x2, y2)], attribs='path')

def parse_ellipse(element):
	cx = float(element.get('cx'))
	cy = float(element.get('cx'))
	rx = float(element.get('rx'))
	ry = float(element.get('ry'))
	return primitives.ellipse((cx, cy), rx, ry)

parser_function = {
	# tag: parser
	"rect": parse_rect,
	"circle": parse_circle,
	"line": parse_line,
	"ellipse": parse_ellipse,
	#"path": parse_path
}

def load_shape(filename):
	tree = etree.parse(filename)

	root = tree.getroot()
	if root.tag != "{http://www.w3.org/2000/svg}svg":
		raise TypeError('file %s does not seem to be a valid SVG file', filename)

	width = root.get('width')
	height = root.get('height')
	
	return parser(root)

def parser(elements):
	shape = PShape([(0,0)], children=[])
 
	for e in elements:
		tag = e.tag.replace('{http://www.w3.org/2000/svg}', "")
		if tag in parser_function.keys():
			shape.add_child(parser_function[tag](e))
		elif tag == "g":
			shape.add_child(parser(e))
		else:
			continue

	return shape

@primitives._draw_on_return
def shape(shape, x, y):
	return shape

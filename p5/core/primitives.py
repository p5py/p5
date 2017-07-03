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

import builtins
from collections import namedtuple

from .. import sketch

__all__ = ['Shape', 'point', 'line', 'arc', 'triangle', 'quad',
           'rect', 'square', 'circle', 'ellipse']

_Point = namedtuple('Point', ['x', 'y', 'z'])
_Point.__new__.__defaults__ = (None, None, 0)

_rect_mode = 'CORNER'
_ellipse_mode = 'CENTER'

builtins.CORNER = 'CORNER'
builtins.CORNERS = 'CORNERS'
builtins.CENTER = 'CENTER'
builtins.RADIUS = 'RADIUS'

class Shape:
    """Represents a Shape in p5py.

    :param kind: The type of this shape. Should be one of {'POLY', ...}
    :type kind: str

    :param vertices: A list of vertices (3-tuples) that make up the
        shape.
    :type vertices: list of tuples

    :param edges: A list of indices into the vertices list that
        represent edges. (Defaults to the empty list `[]`)
    :type edges: list of tuples

    """

    def __init__(self, kind, vertices, faces=[]):
        self.kind = kind
        self.vertices = vertices
        self.faces = faces

    def __repr__(self):
        return "({} Shape with vertices {})".format(self.kind, self.vertices)

    __str__ = __repr__

@sketch.artist
def point(x, y, z=0):
    """Returns a point Shape.

    :param x: x-coordinate of the shape.
    :type x: int or float

    :param y: y-coordinate of the shape.
    :type y: int or float

    :param z: z-coordinate of the shape (defaults to 0).
    :type z: int or float

    :returns: A point Shape.
    :rtype: Shape

    """
    return Shape('POINT', [_Point(x, y, z)], [(0,)])

@sketch.artist
def line(p1, p2):
    """Returns a line Shape.

    :param p1: Coordinates of the starting point of the line.
    :type p1: tuple

    :param p2: Coordinates of the end point of the line.
    :type p2: tuple

    :returns: A line Shape.
    :rtype: Shape

    """
    return Shape('LINE', [_Point(*p1), _Point(*p2)], [(0, 1)])

@sketch.artist
def arc(*args):
    raise NotImplementedError

@sketch.artist
def triangle(p1, p2, p3):
    """Return a triangle.

    :param p1: coordinates of the first point of the triangle
    :type p1: 3-tuple

    :param p2: coordinates of the second point of the triangle
    :type p2: 3-tuple

    :param p3: coordinates of the third point of the triangle
    :type p3: 3-tuple

    :returns: A triangle.
    :rtype: Shape
    """
    vertices = [_Point(*p1), _Point(*p2), _Point(*p3)]
    faces = [(0, 1, 2)]
    return Shape('POLY', vertices, faces)

@sketch.artist
def quad(p1, p2, p3, p4):
    """Return a quad.

    :param p1: coordinates of the first point of the quad
    :type p1: 3-tuple

    :param p2: coordinates of the second point of the quad
    :type p2: 3-tuple

    :param p3: coordinates of the third point of the quad
    :type p3: 3-tuple

    :param p4: coordinates of the fourth point of the quad
    :type p4: 3-tuple

    :returns: A triangle.
    :rtype: Shape
    """
    vertices = [_Point(*p1), _Point(*p2), _Point(*p3), _Point(*p4)]
    faces = [(0, 1, 2), (2, 3, 0)]
    return Shape('POLY', vertices, faces)

def rect(coordinate, *args, mode=_rect_mode):
    """Return a rectangle.

    :param coordinate: Represents the lower left corner of then
        rectangle when mode is 'CORNER', the center of the rectangle
        when mode is 'CENTER' or 'RADIUS', and an arbitrary corner
        when mode is 'CORNERS'

    :type coordinate: 3-tuple

    :param args: For modes'CORNER' or 'CENTER' this has the form
        (width, height); for the 'RADIUS' this has the form
        (half_width, half_height); and for the 'CORNERS' mode, args
        should be the corner opposite to `coordinate`.

    :type: tuple

    :param mode: The drawing mode for the rectangle. Should be one of
        {'CORNER', 'CORNERS', 'CENTER', 'RADIUS'} (defaults to the
        mode being used by the sketch.)

    :type mode: str

    :returns: A rectangle.
    :rtype: Shape

    """
    if mode == 'CORNER':
        corner = coordinate
        width, height = args
    elif mode == 'CENTER':
        center = _Point(*coordinate)
        width, height = args
        corner = _Point(center.x - width/2, center.y - height/2, center.z)
    elif mode == 'RADIUS':
        center = _Point(*coordinate)
        half_width, half_height = args
        corner = _Point(center.x - half_width, center.y - half_height, center.z)
        width = 2 * half_width
        height = 2 * half_height
    elif mode == 'CORNERS':
        corner = _Point(*coordinate)
        corner_2, = args
        corner_2 = _Point(*corner_2)
        width = corner_2.x - corner.x
        height = corner_2.y - corner.y
    else:
        raise ValueError("Unknown rect mode {}".format(mode))

    p1 = _Point(*corner)
    p2 = _Point(p1.x + width, p1.y, p1.z)
    p3 = _Point(p2.x, p2.y + height, p2.z)
    p4 = _Point(p1.x, p3.y, p3.z)
    return quad(p1, p2, p3, p4)

def square(coordinate, side_length, mode=_rect_mode):
    """Return a square.

    :param coordinate: When mode is set to 'CORNER', the coordinate
        represents the lower-left corner of the square. For modes
        'CENTER' and 'RADIUS' the coordinate represents the center of
        the square.

    :type coordinate: 3-tuple

    :param side_length: The side_length of the square (for modes
        'CORNER' and 'CENTER') or hald of the side length (for the
        'RADIUS' mode)

    :type side_length: int or float

    :param mode: The drawing mode for the square. Should be one of
        {'CORNER', 'CORNERS', 'CENTER', 'RADIUS'} (defaults to the
        mode being used by the sketch.)

    :type mode: str

    :returns: A rectangle.
    :rtype: Shape

    :raises ValueError: When the mode is set to 'CORNERS'

    """
    if mode == 'CORNERS':
        raise ValueError("Cannot draw square with {} mode".format(mode))
    return rect(coordinate, side_length, side_length, mode=mode)

def rect_mode(mode):
    """Change the rect mode for the sketch.

    :param mode: The new mode for drawing rectangles. Should be one of
        {'CORNER', 'CORNERS', 'CENTER', 'RADIUS'}
    :type mode: str
    """
    global _rect_mode
    _rect_mode = mode

@sketch.artist
def ellipse(*args):
    raise NotImplementedError

@sketch.artist
def circle(*args):
    raise NotImplementedError

def ellipse_mode(mode):
    """Change the ellipse drawing mode for the sketch.

    :param mode: The new mode for drawing ellipses. Should be one of
        {'CORNER', 'CORNERS', 'CENTER', 'RADIUS'}
    :type mode: str
    """
    global _ellipse_mode
    _ellipse_mode = mode

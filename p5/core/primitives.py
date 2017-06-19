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

from collections import namedtuple

from .. import sketch

__all__ = ['Shape', 'point', 'line', 'arc', 'triangle', 'quad',
           'rect', 'square', 'circle', 'ellipse']

_Point = namedtuple('Point', ['x', 'y', 'z'])
_Point.__new__.__defaults__ = (None, None, 0)

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

def rect(coordinate, width, height):
    """Return a rectangle.

    :param coordinate: The lower-left corner of the rectangle.
    :type coordinate: 3-tuple

    :param width: The width of the rectangle.
    :type: width: int or float

    :param height: The height of the rectangle.
    :type: height: int or float

    :returns: A rectangle.
    :rtype: Shape

    """
    p1 = _Point(*coordinate)
    p2 = _Point(p1.x + width, p1.y, p1.z)
    p3 = _Point(p2.x, p2.y + height, p2.z)
    p4 = _Point(p1.x, p3.y, p3.z)
    return quad(p1, p2, p3, p4)

def square(coordinate, side_length):
    """Return a square.

    :param coordinate: The lower-left corner of the square.
    :type coordinate: 3-tuple

    :param side_length: The side_length of the square.
    :type side_length: int or float

    :returns: A rectangle.
    :rtype: Shape

    """
    return rect(coordinate, side_length, side_length)

@sketch.artist
def ellipse(*args):
    raise NotImplementedError

@sketch.artist
def circle(*args):
    raise NotImplementedError

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
import math

from .. import sketch

from ..pmath.curves import Point

__all__ = ['Shape', 'point', 'line', 'arc', 'triangle', 'quad',
           'rect', 'square', 'circle', 'ellipse']

Point = namedtuple('vert', ['x', 'y', 'z'])
Point.__new__.__defaults__ = (None, None, 0)

_rect_mode = 'CORNER'
_ellipse_mode = 'CENTER'
_shape_mode = 'CORNER'

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

class Ellipse(Shape):
    def __init__(self, center, x_radius, y_radius, tessellate=False):
        self.kind = 'ELLIPSE'
        self.vertices = None
        self.faces = None
        self.center = Point(*center)
        self.radius = Point(x_radius, y_radius)

        if tessellate:
            self._tesseallate

    def _tesseallate(self, resolution=2):
        """Generate vertex and face data using radii.

        :param resolution: Determines the number of vertices per angle
            (in degrees) to produce
        :type resolution: int

        """
        self.vertices = [
            (
                self.center.x +
                self.radius.x *
                math.cos(math.radians(angle / resolution)),

                self.center.y +
                self.radius.y *
                math.sin(math.radians(angle / resolution)),

                self.center.z
            ) for angle in range(360 * resolution)
        ]

        self.faces = [
            (0, i, (i + 1)) for i in range(1, 360*resolution - 1)
        ]

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
    return Shape('POINT', [Point(x, y, z)], [(0,)])

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
    return Shape('PATH', [Point(*p1), Point(*p2)], [(0, 1)])

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
    vertices = [Point(*p1), Point(*p2), Point(*p3)]
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
    vertices = [Point(*p1), Point(*p2), Point(*p3), Point(*p4)]
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
        center = Point(*coordinate)
        width, height = args
        corner = Point(center.x - width/2, center.y - height/2, center.z)
    elif mode == 'RADIUS':
        center = Point(*coordinate)
        half_width, half_height = args
        corner = Point(center.x - half_width, center.y - half_height, center.z)
        width = 2 * half_width
        height = 2 * half_height
    elif mode == 'CORNERS':
        corner = Point(*coordinate)
        corner_2, = args
        corner_2 = Point(*corner_2)
        width = corner_2.x - corner.x
        height = corner_2.y - corner.y
    else:
        raise ValueError("Unknown rect mode {}".format(mode))

    p1 = Point(*corner)
    p2 = Point(p1.x + width, p1.y, p1.z)
    p3 = Point(p2.x, p2.y + height, p2.z)
    p4 = Point(p1.x, p3.y, p3.z)
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

def rect_mode(mode='CORNER'):
    """Change the rect mode for the sketch.

    :param mode: The new mode for drawing rects. Should be one of
        {'CORNER', 'CORNERS', 'CENTER', 'RADIUS'}. This defaults to
        'CORNER' so calling rect_mode without parameters will reset
        the sketch's rect mode.
    :type mode: str
    """
    global _rect_mode
    _rect_mode = mode

@sketch.artist
def ellipse(coordinate, *args, mode=_ellipse_mode):
    """Return a ellipse.

    :param coordinate: Represents the center of the ellipse when mode
        is 'CENTER' (the default) or 'RADIUS', the lower-left corner
        of the ellipse when mode is 'CORNER' or, and an arbitrary
        corner when mode is 'CORNERS'.

    :type coordinate: 3-tuple

    :param args: For modes'CORNER' or 'CENTER' this has the form
        (width, height); for the 'RADIUS' this has the form
        (x_radius, y_radius); and for the 'CORNERS' mode, args
        should be the corner opposite to `coordinate`.

    :type: tuple

    :param mode: The drawing mode for the ellipse. Should be one of
        {'CORNER', 'CORNERS', 'CENTER', 'RADIUS'} (defaults to the
        mode being used by the sketch.)

    :type mode: str

    :returns: An ellipse.
    :rtype: Ellipse

    """

    if mode == 'CORNER':
        corner = Point(*coordinate)
        width, height = args
        xrad = width/2
        yrad = height/2
        center = Point(corner.x + xrad, corner.y + yrad, corner.z)
    elif mode == 'CENTER':
        center = Point(*coordinate)
        xrad, yrad = args
    elif mode == 'RADIUS':
        center = Point(*coordinate)
        xrad, yrad = args
    elif mode == 'CORNERS':
        corner = Point(*coordinate)
        corner_2, = args
        corner_2 = Point(*corner_2)
        xrad = (corner_2.x - corner.x)/2
        yrad = (corner_2.y - corner.y)/2
        center = Point(corner.x + xrad, corner.y + yrad, corner.z)
    else:
        raise ValueError("Unknown ellipse mode {}".format(mode))
    return Ellipse(center, xrad, yrad)

def circle(coordinate, radius, mode=_ellipse_mode):
    """Return a ellipse.

    :param coordinate: Represents the center of the ellipse when mode
        is 'CENTER' (the default) or 'RADIUS', the lower-left corner
        of the ellipse when mode is 'CORNER' or, and an arbitrary
        corner when mode is 'CORNERS'.

    :type coordinate: 3-tuple

    :param radius: For modes'CORNER' or 'CENTER' this actually
        represents the diameter; for the 'RADIUS' this represents the
        radius.

    :type: tuple

    :param mode: The drawing mode for the ellipse. Should be one of
        {'CORNER', 'CORNERS', 'CENTER', 'RADIUS'} (defaults to the
        mode being used by the sketch.)

    :type mode: str

    :returns: An ellipse.
    :rtype: Ellipse

    :raises ValueError: When mode is set to 'CORNERS'

    """
    if mode == 'CORNERS':
        raise ValueError("Cannot create circle in CORNERS mode")
    return ellipse(coordinate, radius, radius, mode=mode)

def ellipse_mode(mode='CENTER'):
    """Change the ellipse drawing mode for the sketch.

    :param mode: The new mode for drawing ellipses. Should be one of
        {'CORNER', 'CORNERS', 'CENTER', 'RADIUS'}. This defaults to
        'CENTER' so calling ellipse_mode without parameters will reset
        the sketch's ellipse mode.
    :type mode: str

    """
    global _ellipse_mode
    _ellipse_mode = mode

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
from ..pmath import curves

__all__ = ['Shape', 'point', 'line', 'arc', 'triangle', 'quad',
           'rect', 'square', 'circle', 'ellipse', 'ellipse_mode',
           'rect_mode', 'bezier', 'curve']

_rect_mode = 'CORNER'
_ellipse_mode = 'CENTER'
_shape_mode = 'CORNER'

AnchorPoint = namedtuple('ANCHOR', ['x', 'y', 'z'])
BezierPoint = namedtuple('BEZIER', ['x', 'y', 'z'])
CurvePoint = namedtuple('CURVE', ['x', 'y', 'z'])
Point = namedtuple('DEFAULT', ['x', 'y', 'z'])

AnchorPoint.__new__.__defaults__ = (None, None, 0)
BezierPoint.__new__.__defaults__ = (None, None, 0)
CurvePoint.__new__.__defaults__ = (None, None, 0)
Point.__new__.__defaults__ = (None, None, 0)

def get_point_type(point):
    return type(point).__name__

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

    def __init__(self, vertices, kind='POLY', edges=None, faces=None):
        self.kind = kind
        self.edges = edges
        self.faces = faces
        self.vertices = None

        self._raw_vertices = vertices
        self._hash_string = self._compute_hash_string()

    def compute_faces(self):
        """Compute the faces for this shape."""
        if self.faces is None:
            self.faces = [
                (0, k, k + 1)
                for k in range(1, len(self.vertices) - 1)
            ]

    def compute_edges(self):
        """Compute the edges for this shape."""
        if self.edges is None:
            self.edges = [
                (k, k+1)
                for k in range(len(self.vertices) - 1)
            ]

    def tessellate(self):
        """Generate actual vertex data from limited number of parameters.
        """
        psig = ''.join(get_point_type(v)[0] for v in self._raw_vertices)
        if all(pi == 'D' for pi in psig):
            # the path is already tessellated. Nothing to be done.
            self.vertices = self._raw_vertices
        elif psig == 'DBBD':
            self.vertices = []
            steps = curves.bezier_resolution
            for i in range(steps + 1):
                t = i / steps
                p = curves.bezier_point(*self._raw_vertices, t)
                self.vertices.append(p)
        elif psig == 'DCCD':
            self.vertices = []
            steps = curves.curve_resolution
            for i in range(steps + 1):
                t = i / steps
                p = curves.curve_point(*self._raw_vertices, t)
                self.vertices.append(p)
        else:
            raise ValueError("Cannot complete tessillation. Unknown shape type.")

    def _compute_hash_string(self):
        vert_str = [
            '{}x{:.3f}y{:.3f}z{:.3f}'.format(get_point_type(p)[:2], p.x, p.y, p.z)
            for p in self._raw_vertices
        ]
        # a additionally, we need to store information about the
        # current curve resolutions
        meta_data = '/{}/{}/{}/'.format(curves.bezier_resolution,
                                     curves.curve_resolution,
                                     curves.curve_tightness_amount)
        return '{}{}:{}'.format(meta_data, self.kind, ''.join(vert_str))

    def __hash__(self):
        if self._hash_string is not None:
            return hash(self._hash_string)
        return hash(str(self.__dict__))

class Ellipse(Shape):
    def __init__(self, center, x_radius, y_radius):
        self.kind = 'ELLIPSE'

        self.vertices = None
        self.faces = None
        self.edges = None

        self.center = Point(*center)
        self.radius = Point(x_radius, y_radius)

    def tessellate(self, resolution=2):
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

    def __hash__(self):
        center_str = 'x{:.3f}y{:.3f}z{:.3f}'.format(*self.center)
        rad_str = '{}x{}'.format(self.radius.x, self.radius.y)
        hash_str = '{}:{}-{}'.format(self.kind, center_str, rad_str)
        return hash(hash_str)

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
    return Shape([Point(x, y, z)], faces=[(0,)], edges=[(0,)], kind='POINT')

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
    path = [
        Point(*p1),
        Point(*p2)
    ]
    return Shape(path, kind='PATH')

@sketch.artist
def bezier(start, control_point_1, control_point_2, stop):
    path = [
        Point(*start),
        BezierPoint(*control_point_1),
        BezierPoint(*control_point_2),
        Point(*stop)
    ]
    return Shape(path, kind='PATH')

@sketch.artist
def curve(point_1, point_2, point_3, point_4):
    path = [
        Point(*point_1),
        CurvePoint(*point_2),
        CurvePoint(*point_3),
        Point(*point_4)
    ]
    return Shape(path, kind='PATH')

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
    return Shape([Point(*p1), Point(*p2), Point(*p3)])

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
    return Shape([Point(*p1), Point(*p2), Point(*p3), Point(*p4)])

def rect(coordinate, *args, mode=None):
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
    if mode is None:
        mode = _rect_mode

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

def square(coordinate, side_length, mode=None):
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
    if mode is None:
        mode = _rect_mode

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
def ellipse(coordinate, *args, mode=None):
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
    if mode is None:
        mode = _ellipse_mode

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

def circle(coordinate, radius, mode=None):
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
    if mode is None:
        mode = _ellipse_mode

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

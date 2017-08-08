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
from math import sin
from math import cos
from math import radians

import numpy as np

from .transforms import _screen_coordinates
from .. import sketch

from ..pmath import Point
from ..pmath import curves
from ..pmath import remap
from ..pmath.utils import SINCOS
from ..pmath.utils import SINCOS_PRECISION

__all__ = ['Shape', 'point', 'line', 'arc', 'triangle', 'quad',
           'rect', 'square', 'circle', 'ellipse', 'ellipse_mode',
           'rect_mode', 'bezier', 'curve']

_rect_mode = 'CORNER'
_ellipse_mode = 'CENTER'
_shape_mode = 'CORNER'

BezierPoint = namedtuple('Bezier', Point._fields)
BezierPoint.__new__.__defaults__ = (None, None, 0, 'B')

CurvePoint = namedtuple('Curve', Point._fields)
CurvePoint.__new__.__defaults__ = (None, None, 0, 'C')

# We use these in ellipse tessellation. The algorithm is similar to
# the one used in Processing and the we compute the number of
# subdivisions per ellipse using the following formula:
#
#    min(M, max(N, (2 * pi * size / F)))
#
# Where,
#
# - size :: is the measure of the dimensions of the circle when
#   projected in screen coordiantes.
#
# - F :: sets the minimum number of subdivisions. A smaller `F` would
#   produce more detailed circles (== POINT_ACCURACY_FACTOR)
#
# - N :: Minimum point accuracy (== MIN_POINT_ACCURACY)
#
# - M :: Maximum point accuracy (== MAX_POINT_ACCURACY)
#
MIN_POINT_ACCURACY = 20
MAX_POINT_ACCURACY = 200
POINT_ACCURACY_FACTOR = 10

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

    def __init__(self, vertices, kind='POLY', edges=None, faces=None,
                 visible=True):
        self.kind = kind
        self._raw_vertices = vertices
        self._vertices = None
        self._edges = edges
        self._faces = faces
        self._texcoords = None
        self.visible = visible

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, is_visible):
        self._visible = is_visible
        if is_visible:
            # Shape, show thyself.
            sketch.draw_shape(self)

    @property
    def vertices(self):
        if self._vertices is None:
            self.tessellate()
        return self._vertices

    @property
    def edges(self):
        if self._edges is None:
            self.compute_edges()
        return self._edges

    @property
    def faces(self):
        if self._faces is None:
            self.compute_faces()
        return self._faces

    @property
    def texcoords(self):
        if self._texcoords is None:
            self.compute_texcoords()
        return self._texcoords

    def compute_faces(self):
        """Compute the faces for this shape."""
        self._faces = [
            (0, k, k + 1)
            for k in range(1, len(self.vertices) - 1)
        ]

    def compute_edges(self):
        """Compute the edges for this shape."""
        self._edges = [
            (k, k+1)
            for k in range(len(self.vertices) - 1)
        ]
        # connect the last vertex to the first vertex
        self._edges.append((len(self.vertices) - 1, 0))

    def compute_texcoords(self):
        """Compute the texture coordinates for the current shape."""
        xs = [v[0] for v in self.vertices]
        ys = [v[1] for v in self.vertices]

        rangex = (min(xs), max(xs))
        rangey = (min(ys), max(ys))

        if (rangex[0] - rangex[1] == 0) or (rangey[0] - rangey[1] == 0):
            self._texcoords = ((0.5, 0.5) for v in self.vertices)
        else:
            self._texcoords = [
                (remap(x, rangex, (0, 1)), remap(y, rangey, (0, 1)))
                for x, y, z in self.vertices
            ]

    def tessellate(self):
        """Generate actual vertex data from limited number of parameters.
        """
        psig = ''.join((v.flag if not v.flag is None else 'D')
                       for v in self._raw_vertices)
        if 'D' in set(psig) and len(set(psig)) == 1:
            # the path is already tessellated. Nothing to be done.
            self._vertices = np.array(
                [v[:3] for v in self._raw_vertices]
            )
        elif psig == 'DBBD':
            vertices = []
            steps = curves.bezier_resolution
            for i in range(steps + 1):
                t = i / steps
                p = curves.bezier_point(*self._raw_vertices, t)
                vertices.append(p)
            self._vertices = np.array(vertices)
        elif psig == 'DCCD':
            vertices = []
            steps = curves.curve_resolution
            for i in range(steps + 1):
                t = i / steps
                p = curves.curve_point(*self._raw_vertices, t)
                vertices.append(p)
            self._vertices = np.array(vertices)
        else:
            raise ValueError("Cannot complete tessillation. Unknown shape type.")


class Ellipse(Shape):
    def __init__(self, center, dim):
        self.center = Point(*center)
        self.radius =  Point(*dim)
        super().__init__([], 'ELLIPSE')

    def tessellate(self):
        """Generate vertex and face data using radii.
        # """
        c1 = self.center.x - self.radius.x, self.center.y - self.radius.y
        s1 = _screen_coordinates(*c1)

        c2 = self.center.x + self.radius.x, self.center.y + self.radius.y,
        s2 = _screen_coordinates(*c2)

        size_acc = (s1.distance(s2) * math.pi * 2) / POINT_ACCURACY_FACTOR

        acc = min(MAX_POINT_ACCURACY, max(MIN_POINT_ACCURACY, int(size_acc)))
        inc = int(len(SINCOS) / acc)

        vertices = [self.center[:3]]
        vertices.extend(
            [(self.center.x + self.radius.x * cs,
              self.center.y + self.radius.y * sn,
              self.center.z) for sn, cs in SINCOS][0:-1:inc])
        vertices.append(vertices[1])
        self._vertices = np.array(vertices)

    def compute_edges(self):
        """Compute the edges for this shape."""
        self._edges = [
            (k, k+1)
            for k in range(1, len(self.vertices) - 1)
        ]
        self._edges.append((len(self.vertices) - 1, 1))

def point(x, y, z=0):
    """Returns a point.

    :param x: x-coordinate of the shape.
    :type x: int or float

    :param y: y-coordinate of the shape.
    :type y: int or float

    :param z: z-coordinate of the shape (defaults to 0).
    :type z: int or float

    :returns: A point Shape.
    :rtype: Shape

    """
    return Shape([Point(x, y, z)], kind='POINT')

def line(p1, p2):
    """Returns a line.

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

def bezier(start, control_point_1, control_point_2, stop):
    """Return a bezier path defined by two control points.

    :param start: The starting point of the bezier curve.
    :type start: tuple.

    :param control_point_1: The first control point of the bezier
        curve.
    :type control_point_1: tuple.

    :param control_point_2: The second control point of the bezier
        curve.
    :type control_point_2: tuple.

    :param stop: The end point of the bezier curve.
    :type stop: tuple.

    :returns: A bezier path.
    :rtype: Shape.

    """
    path = [
        Point(*start),
        BezierPoint(*control_point_1),
        BezierPoint(*control_point_2),
        Point(*stop)
    ]
    return Shape(path, kind='PATH')

def curve(point_1, point_2, point_3, point_4):
    """Return a Catmull-Rom curve defined by four points.

    :param point_1: The first point of the curve.
    :type point_1: tuple

    :param point_2: The first point of the curve.
    :type point_2: tuple

    :param point_3: The first point of the curve.
    :type point_3: tuple

    :param point_4: The first point of the curve.
    :type point_4: tuple

    :returns: A curved path.
    :rtype: Shape

    """
    path = [
        Point(*point_1),
        CurvePoint(*point_2),
        CurvePoint(*point_3),
        Point(*point_4)
    ]
    return Shape(path, kind='PATH')

def arc(*args):
    raise NotImplementedError

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
    return Shape(vertices)

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

    :returns: A quad.
    :rtype: Shape
    """
    vertices = [Point(*p1), Point(*p2), Point(*p3), Point(*p4)]
    return Shape(vertices)

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
    """Change the rect and square drawing mode for the sketch.

    :param mode: The new mode for drawing rects. Should be one of
        {'CORNER', 'CORNERS', 'CENTER', 'RADIUS'}. This defaults to
        'CORNER' so calling rect_mode without parameters will reset
        the sketch's rect mode.
    :type mode: str

    """
    global _rect_mode
    _rect_mode = mode

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
        dim = Point(*args)
        center = (corner.x + (dim.x / 2), corner.y + (dim.y / 2), corner.z)
    elif mode == 'CENTER':
        center = Point(*coordinate)
        dim = Point(args[0] / 2, args[1] / 2)
    elif mode == 'RADIUS':
        center = Point(*coordinate)
        dim = Point(*args)
    elif mode == 'CORNERS':
        corner = Point(*coordinate)
        corner_2, = args
        corner_2 = Point(*corner_2)
        dim = Point((corner_2.x - corner.x) / 2, (corner_2.y - corner.y) / 2)
        center = (corner.x + dim.x, corner.y + dim.y)
    else:
        raise ValueError("Unknown ellipse mode {}".format(mode))
    return Ellipse(center, dim)

def circle(coordinate, radius, mode=None):
    """Return a circle.

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

    :returns: A circle.
    :rtype: Ellipse

    :raises ValueError: When mode is set to 'CORNERS'

    """
    if mode is None:
        mode = _ellipse_mode

    if mode == 'CORNERS':
        raise ValueError("Cannot create circle in CORNERS mode")
    return ellipse(coordinate, radius, radius, mode=mode)

def ellipse_mode(mode='CENTER'):
    """Change the ellipse and circle drawing mode for the sketch.

    :param mode: The new mode for drawing ellipses. Should be one of
        {'CORNER', 'CORNERS', 'CENTER', 'RADIUS'}. This defaults to
        'CENTER' so calling ellipse_mode without parameters will reset
        the sketch's ellipse mode.
    :type mode: str

    """
    global _ellipse_mode
    _ellipse_mode = mode

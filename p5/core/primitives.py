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
        self._transformed_vertices = None
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

    @property
    def transformed_vertices(self):
        """The transformed vertices of the shape (when available)

        :note: This returns the un-transformed shape vertices when the
            shape hasn't been transformed.

        """
        if not self._transformed_vertices is None:
            return self._transformed_vertices
        return self.vertices

    @property
    def has_been_transformed(self):
        """Whether the shape has been transformed by a matrix."""
        return self._transformed_vertices is None

    def transform(self, matrix):
        """Use the given matrix to transform the shape's vertices

        :param matix: The transform matrix to use while transforming
            shape.
        :type matrix: np.ndarray

        """
        self._transformed_vertices = self.vertices.dot(matrix.T)

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
        if not self.kind is 'PATH':
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
                [(*v[:3], 1) for v in self._raw_vertices]
            )
        elif psig == 'DBBD':
            vertices = []
            steps = curves.bezier_resolution
            for i in range(steps + 1):
                t = i / steps
                p = curves.bezier_point(*self._raw_vertices, t)
                vertices.append((*p[:3], 1))
            self._vertices = np.array(vertices)
        elif psig == 'DCCD':
            vertices = []
            steps = curves.curve_resolution
            for i in range(steps + 1):
                t = i / steps
                p = curves.curve_point(*self._raw_vertices, t)
                vertices.append((*p[:3], 1))
            self._vertices = np.array(vertices)
        else:
            raise ValueError("Cannot complete tessillation. Unknown shape type.")

class Arc(Shape):
    def __init__(self, center, dim, start_angle, stop_angle,
                 mode='OPEN PIE'):
        self.center = Point(*center)
        self.radius = Point(*dim)
        self.start_angle = start_angle
        self.stop_angle = stop_angle
        self.modes = set(mode.split())
        super().__init__([], 'ARC')

    def tessellate(self):
        """Generate vertex and face data using radii.
        # """
        c1 = self.center.x - self.radius.x, self.center.y - self.radius.y, 0, 1
        s1 = sketch.renderer.transform_matrix.dot(np.array(c1))

        c2 = self.center.x + self.radius.x, self.center.y + self.radius.y, 0, 1
        s2 = sketch.renderer.transform_matrix.dot(np.array(c2))

        size_acc = (np.sqrt((s2 - s1) @ (s2 - s1)) * math.pi * 2) / POINT_ACCURACY_FACTOR

        acc = min(MAX_POINT_ACCURACY, max(MIN_POINT_ACCURACY, int(size_acc)))
        inc = int(len(SINCOS) / acc)

        sclen = len(SINCOS)
        start_index = int((self.start_angle / (math.pi * 2)) * sclen)
        end_index = int((self.stop_angle / (math.pi * 2)) * sclen)

        vertices = [(*self.center[:3], 1)]
        for idx in range(start_index, end_index, inc):
            i = idx % sclen
            vertices.append((
                self.center.x + self.radius.x * SINCOS[i][1],
                self.center.y + self.radius.y * SINCOS[i][0],
                self.center.z,
                1
            ))
        vertices.append((
            self.center.x + self.radius.x * SINCOS[end_index % sclen][1],
            self.center.y + self.radius.y * SINCOS[end_index % sclen][0],
            self.center.z,
            1
        ))
        self._vertices = np.array(vertices)

    def compute_edges(self):
        """Compute the edges for this shape."""
        v = len(self.vertices) - 1
        self._edges = [
            (k, k+1)
            for k in range(1, v)
        ]

        if 'OPEN' in self.modes:
            return
        elif 'PIE' in self.modes:
            self._edges.append((v, 0))
            self._edges.append((0, 1))
        elif 'CHORD' in self.modes:
            self._edges.append((v, 1))

    def compute_faces(self):
        """Compute the faceds for the Arc.
        """
        v = len(self.vertices) - 1
        self._faces = [
            (0, k, k + 1) for k in range(1, v)
        ]

        if 'PIE' in self.modes:
            return
        if ('OPEN' in self.modes) or ('CHORD' in self.modes):
            self._faces.append((0, v, 1))


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

def arc(coordinate, width, height, start_angle, stop_angle,
        mode='OPEN PIE', ellipse_mode=None):
    """Return a ellipse.

    :param coordinate: Represents the center of the arc when mode
        is 'CENTER' (the default) or 'RADIUS', the lower-left corner
        of the ellipse when mode is 'CORNER'.

    :type coordinate: 3-tuple

    :param width: For ellipse modes 'CORNER' or 'CENTER' this
        represents the width of the the ellipse of which the arc is a
        part. Represents the x-radius of the parent ellipse when
        ellipse mode is 'RADIUS

    :type width: float

    :param height: For ellipse modes 'CORNER' or 'CENTER' this
        represents the height of the the ellipse of which the arc is a
        part. Represents the y-radius of the parent ellipse when
        ellipse mode is 'RADIUS

    :type height: float

    :param mode: The mode used to draw an arc can be some combination
        of {'OPEN', 'CHORD', 'PIE'} separated by spaces. For instance,
        'OPEN PIE', etc (defaults to 'OPEN PIE')

    :type mode: str

    :param ellipse_mode: The drawing mode used for the ellipse. Should be one of
        {'CORNER', 'CENTER', 'RADIUS'} (defaults to the
        mode being used by the sketch.)

    :type mode: str

    :returns: An arc.
    :rtype: Arc

    """
    amode = mode

    if ellipse_mode is None:
        emode = _ellipse_mode
    else:
        emode = ellipse_mode

    if emode == 'CORNER':
        corner = Point(*coordinate)
        dim = Point(width, height)
        center = (corner.x + (dim.x / 2), corner.y + (dim.y / 2), corner.z)
    elif emode == 'CENTER':
        center = Point(*coordinate)
        dim = Point(width / 2, height / 2)
    elif emode == 'RADIUS':
        center = Point(*coordinate)
        dim = Point(width, height)
    else:
        raise ValueError("Unknown arc mode {}".format(emode))
    return Arc(center, dim, start_angle, stop_angle, mode=amode)

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

    :returns: An ellipse
    :rtype: Arc

    """
    if mode is None:
        mode = _ellipse_mode

    if mode == 'CORNERS':
        corner = Point(*coordinate)
        corner_2, = args
        corner_2 = Point(*corner_2)
        width = corner_2.x - corner.x
        height = corner_2.y - corner.y
        mode = 'CORNER'
    else:
        width, height = args
    return arc(coordinate, width, height, 0, math.pi * 2, 'CHORD', mode)

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

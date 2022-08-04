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

import math
import builtins

from ..pmath import Point
from ..pmath import curves

from ..sketch.Vispy2DRenderer.shape import PShape
from .constants import ROUND, SQUARE, PROJECT

from . import p5

from ..sketch.Skia2DRenderer.util import should_draw, mode_adjust

__all__ = [
    "point",
    "line",
    "arc",
    "triangle",
    "quad",
    "rect",
    "square",
    "circle",
    "ellipse",
    "ellipse_mode",
    "rect_mode",
    "bezier",
    "curve",
    "create_shape",
]


def point(x, y, z=0):
    """Returns a point.

    :param x: x-coordinate of the shape.
    :type x: int or float

    :param y: y-coordinate of the shape.
    :type y: int or float

    :param z: z-coordinate of the shape (defaults to 0).
    :type z: int or float

    :returns: A point PShape.
    :rtype: PShape

    """
    if builtins.current_renderer == "vispy":
        if p5.renderer.style.stroke_cap == SQUARE:
            pass
        elif p5.renderer.style.stroke_cap == PROJECT:
            return square((x, y, z), p5.renderer.style.stroke_weight, mode="CENTER")
        elif p5.renderer.style.stroke_cap == ROUND:
            return circle((x, y, z), p5.renderer.style.stroke_weight / 2, mode="CENTER")
        raise ValueError("Unknown stroke_cap value")
    elif builtins.current_renderer == "skia":
        if p5.renderer.style.stroke_enabled:
            p5.renderer.point(x, y)


def line(*args):
    """Returns a line.

    :param x1: x-coordinate of the first point
    :type x1: float

    :param y1: y-coordinate of the first point
    :type y1: float

    :param z1: z-coordinate of the first point
    :type z1: float

    :param x2: x-coordinate of the first point
    :type x2: float

    :param y2: y-coordinate of the first point
    :type y2: float

    :param z2: z-coordinate of the first point
    :type z2: float

    :param p1: Coordinates of the starting point of the line.
    :type p1: tuple

    :param p2: Coordinates of the end point of the line.
    :type p2: tuple

    :returns: A line PShape.
    :rtype: PShape

    """
    if len(args) == 2:
        p1, p2 = args[0], args[1]
    elif len(args) == 4:
        p1, p2 = args[:2], args[2:]
    elif len(args) == 6:
        p1, p2 = args[:3], args[3:]
    else:
        raise ValueError("Unexpected number of arguments passed to line()")

    path = [Point(*p1), Point(*p2)]
    p5.renderer.line(path)


def bezier(*args):
    """Return a bezier path defined by two control points.

    :param x1: x-coordinate of the first anchor point
    :type x1: float

    :param y1: y-coordinate of the first anchor point
    :type y1: float

    :param z1: z-coordinate of the first anchor point
    :type z1: float

    :param x2: x-coordinate of the first control point
    :type x2: float

    :param y2: y-coordinate of the first control point
    :type y2: float

    :param z2: z-coordinate of the first control point
    :type z2: float

    :param x3: x-coordinate of the second control point
    :type x3: float

    :param y3: y-coordinate of the second control point
    :type y3: float

    :param z3: z-coordinate of the second control point
    :type z3: float

    :param x4: x-coordinate of the second anchor point
    :type x4: float

    :param y4: y-coordinate of the second anchor point
    :type y4: float

    :param z4: z-coordinate of the second anchor point
    :type z4: float

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
    :rtype: PShape.

    """
    if len(args) == 4:
        start, control_point_1, control_point_2, stop = args
    elif len(args) == 8:
        start, control_point_1, control_point_2, stop = (
            args[:2],
            args[2:4],
            args[4:6],
            args[6:],
        )
    elif len(args) == 12:
        start, control_point_1, control_point_2, stop = (
            args[:3],
            args[3:6],
            args[6:9],
            args[9:],
        )
    else:
        raise ValueError("Unexpected number of arguments passed to bezier()")

    vertices = []
    steps = curves.bezier_resolution
    for i in range(steps + 1):
        t = i / steps
        p = curves.bezier_point(start, control_point_1, control_point_2, stop, t)
        vertices.append(p[:3])

    p5.renderer.bezier(vertices)


def curve(*args):
    """Return a Catmull-Rom curve defined by four points.

    :param x1: x-coordinate of the beginning control point
    :type x1: float

    :param y1: y-coordinate of the beginning control point
    :type y1: float

    :param z1: z-coordinate of the beginning control point
    :type z1: float

    :param x2: x-coordinate of the first point
    :type x2: float

    :param y2: y-coordinate of the first point
    :type y2: float

    :param z2: z-coordinate of the first point
    :type z2: float

    :param x3: x-coordinate of the second point
    :type x3: float

    :param y3: y-coordinate of the second point
    :type y3: float

    :param z3: z-coordinate of the second point
    :type z3: float

    :param x4: x-coordinate of the ending control point
    :type x4: float

    :param y4: y-coordinate of the ending control point
    :type y4: float

    :param z4: z-coordinate of the ending control point
    :type z4: float

    :param point_1: The first point of the curve.
    :type point_1: tuple

    :param point_2: The first point of the curve.
    :type point_2: tuple

    :param point_3: The first point of the curve.
    :type point_3: tuple

    :param point_4: The first point of the curve.
    :type point_4: tuple

    :returns: A curved path.
    :rtype: PShape

    """
    if len(args) == 4:
        point_1, point_2, point_3, point_4 = args
    elif len(args) == 8:
        point_1, point_2, point_3, point_4 = args[:2], args[2:4], args[4:6], args[6:]
    elif len(args) == 12:
        point_1, point_2, point_3, point_4 = args[:3], args[3:6], args[6:9], args[9:]
    else:
        raise ValueError("Unexpected number of arguments passed to curve()")

    vertices = []
    steps = curves.curve_resolution
    for i in range(steps + 1):
        t = i / steps
        p = curves.curve_point(point_1, point_2, point_3, point_4, t)
        vertices.append(p[:3])

    p5.renderer.curve(vertices)


def triangle(*args):
    """Return a triangle.

    :param x1: x-coordinate of the first point
    :type x1: float

    :param y1: y-coordinate of the first point
    :type y1: float

    :param x2: x-coordinate of the second point
    :type x2: float

    :param y2: y-coordinate of the second point
    :type y2: float

    :param x3: x-coordinate of the third point
    :type x3: float

    :param y3: y-coordinate of the third point
    :type y3: float

    :param p1: coordinates of the first point of the triangle
    :type p1: tuple | list | p5.Vector

    :param p2: coordinates of the second point of the triangle
    :type p2: tuple | list | p5.Vector

    :param p3: coordinates of the third point of the triangle
    :type p3: tuple | list | p5.Vector

    :returns: A triangle.
    :rtype: p5.PShape
    """
    if len(args) == 6:
        p1, p2, p3 = args[:2], args[2:4], args[4:]
    elif len(args) == 3:
        p1, p2, p3 = args
    else:
        raise ValueError("Unexpected number of arguments passed to triangle()")
    if builtins.current_renderer == "vispy":
        path = [Point(*p1), Point(*p2), Point(*p3)]
        p5.renderer.triangle(path)
    elif builtins.current_renderer == "skia":
        if should_draw():
            p5.renderer.triangle(*p1, *p2, *p3)


def quad(*args):
    """Return a quad.

    :param x1: x-coordinate of the first point
    :type x1: float

    :param y1: y-coordinate of the first point
    :type y1: float

    :param x2: x-coordinate of the second point
    :type x2: float

    :param y2: y-coordinate of the second point
    :type y2: float

    :param x3: x-coordinate of the third point
    :type x3: float

    :param y3: y-coordinate of the third point
    :type y3: float

    :param x4: x-coordinate of the forth point
    :type x4: float

    :param y4: y-coordinate of the forth point
    :type y4: float

    :param p1: coordinates of the first point of the quad
    :type p1: tuple | list | p5.Vector

    :param p2: coordinates of the second point of the quad
    :type p2: tuple | list | p5.Vector

    :param p3: coordinates of the third point of the quad
    :type p3: tuple | list | p5.Vector

    :param p4: coordinates of the fourth point of the quad
    :type p4: tuple | list | p5.Vector

    :returns: A quad.
    :rtype: PShape
    """
    if len(args) == 8:
        p1, p2, p3, p4 = args[:2], args[2:4], args[4:6], args[6:]
    elif len(args) == 4:
        p1, p2, p3, p4 = args
    else:
        raise ValueError("Unexpected number of arguments passed to quad()")

    if builtins.current_renderer == "vispy":
        path = [Point(*p1), Point(*p2), Point(*p3), Point(*p4)]
        p5.renderer.quad(path)
    elif builtins.current_renderer == "skia":
        x1, y1 = p1
        x2, y2 = p2
        x3, y3 = p3
        x4, y4 = p4
        p5.renderer.quad(x1, y1, x2, y2, x3, y3, x4, y4)


def rect(*args, mode=None):
    """Return a rectangle.

    :param x: x-coordinate of the rectangle by default
    :type float:

    :param y: y-coordinate of the rectangle by default
    :type float:

    :param w: width of the rectangle by default
    :type float:

    :param h: height of the rectangle by default
    :type float:

    :param coordinate: Represents the lower left corner of then
        rectangle when mode is 'CORNER', the center of the rectangle
        when mode is 'CENTER' or 'RADIUS', and an arbitrary corner
        when mode is 'CORNERS'

    :type coordinate: tuple | list | p5.Vector

    :param args: For modes'CORNER' or 'CENTER' this has the form
        (width, height); for the 'RADIUS' this has the form
        (half_width, half_height); and for the 'CORNERS' mode, args
        should be the corner opposite to `coordinate`.

    :type: tuple

    :param mode: The drawing mode for the rectangle. Should be one of
        {'CORNER', 'CORNERS', 'CENTER', 'RADIUS'} (defaults to the
        mode being used by the p5.renderer.)

    :type mode: str

    :returns: A rectangle.
    :rtype: p5.PShape

    TODO: Update docs for rect, we support border radius as well
    """
    if builtins.current_renderer == "vispy":
        if len(args) == 4:
            coordinate, args = args[:2], args[2:]
        elif len(args) == 3:
            coordinate, args = args[0], args[1:]
        else:
            raise ValueError("Unexpected number of arguments passed to rect()")

        if mode is None:
            mode = p5.renderer.style.rect_mode

        if mode == "CORNER":
            corner = coordinate
            width, height = args
        elif mode == "CENTER":
            center = Point(*coordinate)
            width, height = args
            corner = Point(center.x - width / 2, center.y - height / 2, center.z)
        elif mode == "RADIUS":
            center = Point(*coordinate)
            half_width, half_height = args
            corner = Point(center.x - half_width, center.y - half_height, center.z)
            width = 2 * half_width
            height = 2 * half_height
        elif mode == "CORNERS":
            corner = Point(*coordinate)
            (corner_2,) = args
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

    elif builtins.current_renderer == "skia":
        if len(args) == 4:
            x, y, w, h = args
        elif len(args) == 3:
            x, y = args[0]
            w, h = args[1:]
        vals = mode_adjust(
            x, y, w, h, mode if mode is not None else p5.renderer.style.rect_mode
        )
        p5.renderer.rect(*(vals["x"], vals["y"], vals["w"], vals["h"]) + args[4:])


def square(*args, mode=None):
    """Return a square.

    :param x: x-coordinate of the square by default
    :type float:

    :param y: y-coordinate of the square by default
    :type float:

    :param coordinate: When mode is set to 'CORNER', the coordinate
        represents the lower-left corner of the square. For modes
        'CENTER' and 'RADIUS' the coordinate represents the center of
        the square.

    :type coordinate: tuple | list | p5.Vector

    :param side_length: The side_length of the square (for modes
        'CORNER' and 'CENTER') or hald of the side length (for the
        'RADIUS' mode)

    :type side_length: int or float

    :param mode: The drawing mode for the square. Should be one of
        {'CORNER', 'CORNERS', 'CENTER', 'RADIUS'} (defaults to the
        mode being used by the p5.renderer.)

    :type mode: str

    :returns: A rectangle.
    :rtype: p5.PShape

    :raises ValueError: When the mode is set to 'CORNERS'

    """
    if builtins.current_renderer == "vispy":
        if len(args) == 2:
            coordinate, side_length = args
        elif len(args) == 3:
            coordinate, side_length = args[:2], args[2]
        else:
            raise ValueError("Unexpected number of arguments passed to square()")

        if mode is None:
            mode = p5.renderer.style.rect_mode

        if mode == "CORNERS":
            raise ValueError("Cannot draw square with {} mode".format(mode))
        return rect(coordinate, side_length, side_length, mode=mode)
    elif builtins.current_renderer == "skia":
        if should_draw():
            if len(args) == 2:
                x, y = args[0]
                side = args[1]
            elif len(args) == 3:
                x, y, side = args
            rect(x, y, side, side)


def rect_mode(mode="CORNER"):
    """Change the rect and square drawing mode for the p5.renderer.

    :param mode: The new mode for drawing rects. Should be one of
        {'CORNER', 'CORNERS', 'CENTER', 'RADIUS'}. This defaults to
        'CORNER' so calling rect_mode without parameters will reset
        the sketch's rect mode.
    :type mode: str

    """
    p5.renderer.style.rect_mode = mode


def arc(*args, mode=None, ellipse_mode=None):
    """Return a ellipse.

    :param x: x-coordinate of the arc's ellipse.
    :type x: float

    :param y: y-coordinate of the arc's ellipse.
    :type y: float

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

    :param mode: The mode used to draw an arc can be any of {None, 'OPEN', 'CHORD', 'PIE'}.

    :type mode: str

    :param ellipse_mode: The drawing mode used for the ellipse. Should be one of
        {'CORNER', 'CENTER', 'RADIUS'} (defaults to the
        mode being used by the p5.renderer.)

    :type mode: str

    :returns: An arc.
    :rtype: Arc

    """
    if len(args) == 5:
        coordinate, width, height, start_angle, stop_angle = args
    elif len(args) == 6:
        coordinate = args[:2]
        width, height, start_angle, stop_angle = args[2:]
    else:
        raise ValueError("Unexpected number of arguments passed to arc()")

    if ellipse_mode is None:
        emode = p5.renderer.style.ellipse_mode
    else:
        emode = ellipse_mode

    if builtins.current_renderer == "vispy":
        if emode == "CORNER":
            corner = Point(*coordinate)
            dim = Point(width / 2, height / 2)
            center = (corner.x + dim.x, corner.y + dim.y, corner.z)
        elif emode == "CENTER":
            center = Point(*coordinate)
            dim = Point(width / 2, height / 2)
        elif emode == "RADIUS":
            center = Point(*coordinate)
            dim = Point(width, height)
        else:
            raise ValueError("Unknown arc mode {}".format(emode))
        p5.renderer.arc(center, dim, start_angle, stop_angle, mode)

    elif builtins.current_renderer == "skia":
        if not should_draw() or start_angle == stop_angle:
            return
        x, y = coordinate[0], coordinate[1]
        vals = mode_adjust(x, y, width, height, emode)
        # TODO: normalize_arc_angles
        p5.renderer.arc(
            vals["x"], vals["y"], vals["w"], vals["h"], start_angle, stop_angle, mode
        )


def ellipse(*args, mode=None):
    """Return a ellipse.

    :param a: x-coordinate of the ellipse
    :type a: float

    :param b: y-coordinate of the ellipse
    :type b: float

    :param c: width of the ellipse
    :type c: float

    :param d: height of the ellipse
    :type d: float

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
        mode being used by the p5.renderer.)

    :type mode: str

    :returns: An ellipse
    :rtype: Arc

    """
    if len(args) == 3:
        coordinate, args = args[0], args[1:]
    elif len(args) == 4:
        coordinate, args = args[:2], args[2:]
    else:
        raise ValueError("Unexpected number of arguments passed to ellipse()")

    if mode is None:
        mode = p5.renderer.style.ellipse_mode

    if builtins.current_renderer == "vispy":
        if mode == "CORNERS":
            corner = Point(*coordinate)
            (corner_2,) = args
            corner_2 = Point(*corner_2)
            width = corner_2.x - corner.x
            height = corner_2.y - corner.y
            mode = "CORNER"
        else:
            width, height = args
        return arc(
            coordinate, width, height, 0, math.pi * 2, mode="CHORD", ellipse_mode=mode
        )

    elif builtins.current_renderer == "skia":
        if not should_draw():
            return
        x, y = coordinate
        w, h = args
        vals = mode_adjust(x, y, w, h, mode)
        p5.renderer.ellipse(vals["x"], vals["y"], vals["w"], vals["h"])


def circle(*args, mode=None):
    """Return a circle.

    :param x: x-coordinate of the centre of the circle.
    :type x: float

    :param y: y-coordinate of the centre of the circle.
    :type y: float

    :param coordinate: Represents the center of the ellipse when mode
        is 'CENTER' (the default) or 'RADIUS', the lower-left corner
        of the ellipse when mode is 'CORNER' or, and an arbitrary
        corner when mode is 'CORNERS'.

    :type coordinate: 3-tuple

    :param diameter: For modes'CORNER' or 'CENTER' this actually
        represents the diameter; for the 'RADIUS' this represents the
        radius.

    :type diameter: float

    :param mode: The drawing mode for the ellipse. Should be one of
        {'CORNER', 'CORNERS', 'CENTER', 'RADIUS'} (defaults to the
        mode being used by the p5.renderer.)

    :type mode: str

    :returns: A circle.
    :rtype: Ellipse

    :raises ValueError: When mode is set to 'CORNERS'

    """
    if len(args) == 2:
        coordinate, diameter = args[0], args[1]
    elif len(args) == 3:
        coordinate, diameter = args[:2], args[2]
    else:
        raise ValueError("Unexpected number of arguments passed to circle()")

    if mode is None:
        mode = p5.renderer.style.ellipse_mode
    if builtins.current_renderer == "vispy":
        if mode == "CORNERS":
            raise ValueError("Cannot create circle in CORNERS mode")
        return ellipse(coordinate, diameter, diameter, mode=mode)
    elif builtins.current_renderer == "skia":
        x, y = coordinate
        p5.renderer.circle(x, y, diameter)


def ellipse_mode(mode="CENTER"):
    """Change the ellipse and circle drawing mode for the p5.renderer.

    :param mode: The new mode for drawing ellipses. Should be one of
        {'CORNER', 'CORNERS', 'CENTER', 'RADIUS'}. This defaults to
        'CENTER' so calling ellipse_mode without parameters will reset
        the sketch's ellipse mode.
    :type mode: str

    """
    p5.renderer.style.ellipse_mode = mode


def create_shape(kind=None, *args, **kwargs):
    """Create a new PShape

    Note :: A shape created using this function is *not* visible by
        default. Please make the shape visible by setting the shapes's
        `visible` attribute to true.

    :param kind: Type of shape. When left unspecified a generic PShape
        is returned (which can be edited later). Valid values for
        `kind` are: { 'point', 'line', 'triangle', 'quad', 'rect',
        'ellipse', 'arc', }

    :type kind: None | str

    :param args: Initial arguments to be passed to the shape creation
        function (only applied when `kind` is *not* None)

    :param kwargs: Initial keyword arguments to be passed to the shape
        creation function (only applied when `kind` is *not* None)

    :returns: The requested shape
    :rtype: p5.PShape

    """

    # TODO: add 'box', 'sphere' support
    valid_values = {
        None,
        "point",
        "line",
        "triangle",
        "quad",
        "rect",
        "square",
        "ellipse",
        "circle",
        "arc",
    }

    def empty_shape(*args, **kwargs):
        return PShape()

    shape_map = {
        "arc": arc,
        "circle": circle,
        "ellipse": ellipse,
        "line": line,
        "point": point,
        "quad": quad,
        "rect": rect,
        "square": square,
        "triangle": triangle,
        None: empty_shape,
    }

    # kwargs['visible'] = False
    return shape_map[kind](*args, **kwargs)

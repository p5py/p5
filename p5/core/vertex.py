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

import builtins

from p5.pmath.vector import Point
from . import p5
from .constants import TESS
from ..pmath import curves
import copy

shape_kind = None
vertices = []  # stores the vertex coordinates
vertices_types = []  # stores the type of vertex. Eg: bezier, curve, etc
curr_contour_vertices = []
curr_contour_vertices_types = []
contour_vertices = []  # list of all contours [[v1, v2, ...], [v1, v2, ...]]
contour_vertices_types = []  # list of all vertex types [[t1, t2, ...], [t1, t2, ...]]
is_bezier = False
is_curve = False
is_quadratic = False
is_contour = False
in_contour = False
is_first_contour = True

__all__ = [
    "begin_shape",
    "end_shape",
    "begin_contour",
    "end_contour",
    "curve_vertex",
    "bezier_vertex",
    "quadratic_vertex",
    "vertex",
]


def begin_shape(kind=TESS):
    """Begin shape drawing.  This is a helpful way of generating custom shapes quickly.

    :param kind: TESS, POINTS, LINES, TRIANGLES, TRIANGLE_FAN, TRIANGLE_STRIP, QUADS, or QUAD_STRIP; defaults to TESS
    :type kind: SType
    """
    global shape_kind, vertices, contour_vertices, vertices_types, contour_vertices_types, is_contour
    global curr_contour_vertices, curr_contour_vertices_types

    shape_kind = kind
    is_contour = False
    vertices = []
    vertices_types = []
    contour_vertices = []
    contour_vertices_types = []
    curr_contour_vertices = []
    curr_contour_vertices_types = []


def curve_vertex(x, y, z=0):
    """
    Specifies vertex coordinates for curves. The first
    and last points in a series of curveVertex() lines
    will be used to guide the beginning and end of a the
    curve. A minimum of four points is required to draw a
    tiny curve between the second and third points. Adding
    a fifth point with curveVertex() will draw the curve
    between the second, third, and fourth points. The
    curveVertex() function is an implementation of
    Catmull-Rom splines.

    :param x: x-coordinate of the vertex
    :type x: float

    :param y: y-coordinate of the vertex
    :type y: float

    :param z: z-coordinate of the vertex
    :type z: float
    """

    global is_curve
    is_curve = True

    if p5.mode == "3D":
        return
    if builtins.current_renderer == "vispy":
        if is_contour:
            curr_contour_vertices.append((x, y, z))
            curr_contour_vertices_types.append(2)
        else:
            vertices.append((x, y, z))  # False attribute if the vertex is
            vertices_types.append(2)
    elif builtins.current_renderer == "skia":
        vertex(x, y)


def bezier_vertex(x2, y2, x3, y3, x4, y4):
    """
    Specifies vertex coordinates for Bezier curves

    :param x2: x-coordinate of the first control point
    :type x2: float

    :param y2: y-coordinate of the first control point
    :type y2: float

    :param x3: x-coordinate of the second control point
    :type x3: float

    :param y3: y-coordinate of the second control point
    :type y3: float

    :param x4: x-coordinate of the anchor point
    :type x4: float

    :param y4: y-coordinate of the anchor point
    :type y4: float
    """
    global is_bezier
    is_bezier = True

    if p5.mode == "3D":
        return
    if builtins.current_renderer == "vispy":
        if is_contour:
            curr_contour_vertices.append((x2, y2, x3, y3, x4, y4))
            curr_contour_vertices_types.append(3)
        else:
            vertices.append((x2, y2, x3, y3, x4, y4))
            vertices_types.append(3)
    elif builtins.current_renderer == "skia":
        vert_data = [x2, y2, x3, y3, x4, y4, {"is_vert": False}]
        if is_contour:
            contour_vertices.append(vert_data)
        else:
            vertices.append(vert_data)


def quadratic_vertex(cx, cy, x3, y3):
    """
    Specifies vertex coordinates for quadratic Bezier curves

    :param cx: x-coordinate of the control point
    :type cx: float

    :param cy: y-coordinate of the control point
    :type cy: float

    :param x3: x-coordinate of the anchor point
    :type x3: float

    :param y3: y-coordinate of the anchor point
    :type y3: float

    """

    if p5.mode == "3D":
        return
    global is_quadratic
    is_quadratic = True

    if builtins.current_renderer == "vispy":
        if is_contour:
            curr_contour_vertices.append((cx, cy, x3, y3))
            curr_contour_vertices_types.append(4)
        else:
            vertices.append((cx, cy, x3, y3))
            vertices_types.append(3)
    elif builtins.current_renderer == "skia":
        vert_data = [cx, cy, x3, y3, {"is_vert": False}]
        if is_contour:
            contour_vertices.append(vert_data)
        else:
            vertices.append(vert_data)


def vertex(x, y, z=0):
    """
    All shapes are constructed by connecting a series of
    vertices. vertex() is used to specify the vertex
    coordinates for points, lines, triangles, quads,
    and polygons. It is used exclusively within the
    beginShape() and endShape() functions.

    :param x: x-coordinate of the vertex
    :type x: float

    :param y: y-coordinate of the vertex
    :type y: float

    :param z: z-coordinate of the vertex
    :type z: float
    """
    if p5.mode == "3D":
        return
    if builtins.current_renderer == "vispy":
        if is_contour:
            curr_contour_vertices.append((x, y, z))
            curr_contour_vertices_types.append(1)
        else:
            vertices.append((x, y, z))
            vertices_types.append(1)
    elif builtins.current_renderer == "skia":
        vert_data = [
            x,
            y,
            0,
            0,
            0,
            tuple(255 * c for c in p5.renderer.style.fill_color),
            tuple(255 * c for c in p5.renderer.style.stroke_color),
            {},
        ]
        vert_data[-1]["is_vert"] = True

        if is_contour:
            if len(contour_vertices) == 0:
                vert_data[-1]["move_to"] = True
            contour_vertices.append(vert_data)
        else:
            vertices.append(vert_data)


def begin_contour():
    """
    Use the beginContour() and endContour() functions
    to create negative shapes within shapes such as
    the center of the letter 'O'. beginContour() begins
    recording vertices for the shape and endContour() stops
    recording. The vertices that define a negative shape must
    "wind" in the opposite direction from the exterior shape.
    First draw vertices for the exterior clockwise order, then
    for internal shapes, draw vertices shape in counter-clockwise.

    """
    global is_contour, contour_vertices, contour_vertices_types, in_contour
    is_contour = True
    in_contour = True
    contour_vertices = []
    contour_vertices_types = []


def end_contour():
    """Ends the current contour.

    For more info, see :any:`begin_contour`.
    """
    global in_contour, curr_contour_vertices, curr_contour_vertices_types, is_first_contour
    in_contour = False
    # https://github.com/p5py/p5/pull/357#discussion_r935221732
    # is_contour = False
    if builtins.current_renderer == "vispy":
        # Close contour
        curr_contour_vertices.append(curr_contour_vertices[0])
        curr_contour_vertices_types.append(curr_contour_vertices_types[0])
        # Save contour
        contour_vertices.append(curr_contour_vertices)
        contour_vertices_types.append(curr_contour_vertices_types)
        curr_contour_vertices, curr_contour_vertices_types = [], []
    elif builtins.current_renderer == "skia":

        vert_data = copy.deepcopy(contour_vertices[0])
        vert_data[-1]["is_vert"] = contour_vertices[0][-1].get("is_vert", None)
        vert_data[-1]["move_to"] = False

        contour_vertices.append(vert_data)

        # Close the shape before starting the contour
        if is_first_contour:
            vertices.append(vertices[0])
            is_first_contour = False

        for vert in contour_vertices:
            vertices.append(vert)


def get_curve_vertices(verts):
    if len(verts) == 0:
        return []

    s = 1 - curves.curve_tightness_amount
    shape_vertices = [(verts[1][0], verts[1][1], 0.0)]
    steps = curves.curve_resolution

    for i in range(1, len(verts) - 2):
        v = verts[i]
        start = (
            shape_vertices[len(shape_vertices) - 1][0],
            shape_vertices[len(shape_vertices) - 1][1],
        )
        c1 = [
            v[0] + (s * verts[i + 1][0] - s * verts[i - 1][0]) / 6,
            v[1] + (s * verts[i + 1][1] - s * verts[i - 1][1]) / 6,
        ]
        c2 = [
            verts[i + 1][0] + (s * verts[i][0] - s * verts[i + 2][0]) / 6,
            verts[i + 1][1] + (s * verts[i][1] - s * verts[i + 2][1]) / 6,
        ]
        stop = [verts[i + 1][0], verts[i + 1][1]]

        for i in range(steps + 1):
            t = i / steps
            p = curves.bezier_point(start, c1, c2, stop, t)
            shape_vertices.append(Point(*p))

    return shape_vertices


def get_bezier_vertices(verts, vert_types):
    if len(verts) == 0:
        return []

    shape_vertices = []
    steps = curves.curve_resolution
    for i in range(len(verts)):
        if vert_types[i] == 1 or vert_types[i] == 2:
            shape_vertices.append((verts[i][0], verts[i][1], 0.0))
        else:
            start = (
                shape_vertices[len(shape_vertices) - 1][0],
                shape_vertices[len(shape_vertices) - 1][1],
            )
            c1 = [verts[i][0], verts[i][1]]
            c2 = [verts[i][2], verts[i][3]]
            stop = [verts[i][4], verts[i][5]]

            for i in range(steps + 1):
                t = i / steps
                p = curves.bezier_point(start, c1, c2, stop, t)
                shape_vertices.append(Point(*p))
    return shape_vertices


def get_quadratic_vertices(verts, vert_types):
    if len(verts) == 0:
        return []

    shape_vertices = []
    steps = curves.curve_resolution
    for i in range(len(verts)):
        if vert_types[i] == 1 or vert_types[i] == 2:
            shape_vertices.append((verts[i][0], verts[i][1], 0.0))
        else:
            start = (
                shape_vertices[len(shape_vertices) - 1][0],
                shape_vertices[len(shape_vertices) - 1][1],
            )
            control = [verts[i][0], verts[i][1]]
            stop = [verts[i][2], verts[i][3]]

            for i in range(steps + 1):
                t = i / steps
                p = curves.quadratic_point(start, control, stop, t)
                shape_vertices.append(Point(*p))

    return shape_vertices


def end_shape(mode=""):
    """
    The endShape() function is the companion to beginShape()
    and may only be called after beginShape(). When endshape()
    is called, all of image data defined since the previous call
    to beginShape() is rendered.

    :param mode: use CLOSE to close the shape
    :type mode: str

    """
    global is_bezier, is_curve, is_quadratic, is_contour, is_first_contour, in_contour
    if is_curve or is_bezier or is_quadratic:
        assert shape_kind == TESS, "Should not specify primitive type for a curve"
    assert not in_contour, "begin_contour called without calling end_contour"

    if len(vertices) == 0:
        return

    if (not p5.renderer.style.stroke_enabled) and (not p5.renderer.style.fill_enabled):
        return

    if builtins.current_renderer == "vispy":
        # if the shape is closed, the first element is also the last element
        if mode == "CLOSE":
            vertices.append(vertices[0])
            vertices_types.append(vertices_types[0])

        if is_curve:
            if len(vertices) > 3:
                p5.renderer.shape(
                    vertices=get_curve_vertices(vertices),
                    contours=[get_curve_vertices(c) for c in contour_vertices],
                    shape_type=TESS,
                )
        elif is_bezier:
            p5.renderer.shape(
                vertices=get_bezier_vertices(vertices, vertices_types),
                contours=[
                    get_bezier_vertices(contour_vertices[i], contour_vertices_types[i])
                    for i in range(len(contour_vertices))
                ],
                shape_type=TESS,
            )
        elif is_quadratic:
            p5.renderer.shape(
                vertices=get_quadratic_vertices(vertices, vertices_types),
                contours=[
                    get_quadratic_vertices(
                        contour_vertices[i], contour_vertices_types[i]
                    )
                    for i in range(len(contour_vertices))
                ],
                shape_type=TESS,
            )
        else:
            p5.renderer.shape(
                vertices=vertices, contours=contour_vertices, shape_type=shape_kind
            )

    elif builtins.current_renderer == "skia":
        close_shape = mode == "CLOSE"
        if close_shape and not is_contour:
            vertices.append(vertices[0])
        p5.renderer.end_shape(
            mode,
            vertices,
            is_curve,
            is_bezier,
            is_quadratic,
            is_contour,
            None if shape_kind == TESS else shape_kind,
        )
        if close_shape:
            vertices.pop()

    is_bezier = False
    is_curve = False
    is_quadratic = False
    is_contour = False
    is_first_contour = True

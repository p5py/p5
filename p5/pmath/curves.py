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
"""Utility functions to work with curves.
"""

from collections import namedtuple
from functools import wraps
import math

from ..tmp import Matrix4

__all__ = [ 'bezier_point', 'bezier_tangent', 'bezier_detail',
            'curve_point', 'curve_tangent', 'curve_detail',
            'curve_tightness']

Point = namedtuple('Point', ['x', 'y', 'z'])
Point.__new__.__defaults__ = (None, None, 0)

curve_resolution = 20
curve_tightness_amount = 0
curve_basis_matrix = None
curve_draw_matrix = None

bezier_resolution = 20

def typecast_arguments_as_points(func):
    """Typecast all but the last argument of the function as Points."""
    @wraps(func)
    def decorated(*args, **kwargs):
        parameter = args[-1]
        new_args = [Point(*arg) for arg in args[:-1]]
        ret_value = func(*new_args, parameter, **kwargs)
        return ret_value
    return decorated

def bezier_detail(detail_value):
    """Change the resolution used to draw bezier curves.

    :param detail_value: New resolution to be used.
    :type detail_value: int
    """
    global bezier_resolution
    bezier_resolution = detail_value

@typecast_arguments_as_points
def bezier_point(start, control_1, control_2, stop, parameter):
    """Return the coordinate of a point along a bezier curve.

    :param start: The start point of the bezier curve
    :type start: 3-tuple.

    :param control_1: The first control point of the bezier curve
    :type control_1: 3-tuple.

    :param control_2: The second control point of the bezier curve
    :type control_2: 3-tuple.

    :param stop: The end point of the bezier curve
    :type stop: 3-tuple.

    :param parameter: The parameter for the required location along
        the curve. Should be in the range [0.0, 1.0] where 0 indicates
        the start of the curve and 1 indicates the end of the curve.
    :type parameter: float

    :returns: The coordinate of the point along the bezier curve.
    :rtype: Point (namedtuple with x, y, z attributes)

    """
    t = parameter
    t_ = 1 - parameter

    P = [start, control_1, control_2, stop]
    coeffs = [t_*t_*t_, 3*t*t_*t_,  3*t*t*t_, t*t*t]

    x = sum(pt.x * c for pt, c in zip(P, coeffs))
    y = sum(pt.y * c for pt, c in zip(P, coeffs))

    return Point(x, y)

@typecast_arguments_as_points
def bezier_tangent(start, control_1, control_2, stop, parameter):
    """Return the tangent at a point along a bezier curve.

    :param start: The start point of the bezier curve
    :type start: 3-tuple.

    :param control_1: The first control point of the bezier curve
    :type control_1: 3-tuple.

    :param control_2: The second control point of the bezier curve
    :type control_2: 3-tuple.

    :param stop: The end point of the bezier curve
    :type stop: 3-tuple.

    :param parameter: The parameter for the required tangent location
        along the curve. Should be in the range [0.0, 1.0] where 0
        indicates the start of the curve and 1 indicates the end of
        the curve.
    :type parameter: float

    :returns: The tangent at the required point along the bezier
        curve.
    :rtype: Point (namedtuple with x, y, z attributes)

    """
    t = parameter
    tangent = lambda a, b, c, d: 3*t*t*(3*b - 3*c + d - a) + \
                                 6*t*(a - 2*b + c) + \
                                 3*(b - a)
    x = tangent(start.x, control_1.x, control_2.x, stop.x)
    y = tangent(start.y, control_1.y, control_2.y, stop.y)
    return Point(x, y)

def _reinit_curve_matrices():
    global curve_basis_matrix
    global curve_draw_matrix

    s = curve_tightness_amount
    curve_basis_matrix = Matrix4()
    curve_basis_matrix[:] = [
        0.5*(s - 1),  0.5*(s + 3), -0.5*(s + 3), 0.5*(1 - s),
        1 - s,       -0.5*(s + 5), s + 2,        0.5*(s - 1),
        0.5*(s - 1),  0,           0.5*(1 - s),  0,
        0,            1,           0,            0,
    ]

    # curve_draw_matrix = Matrix4()
    # f = 1 / curve_resolution
    # curve_draw_matrix[:] = [
    #     0,        0,        0,  1,
    #     f**3,     f**2,     f,  0,
    #     6*(f**3), 2*(f**2), 0,  0,
    #     6*(f**3), 0,        0,  0
    # ]
    #
    # curve_draw_matrix = curve_draw_matrix * curve_basis_matrix

def curve_detail(detail_value):
    """Change the resolution used to draw bezier curves.

    :param detail_value: New resolution to be used.
    :type detail_value: int
    """
    global curve_resolution
    curve_resolution = detail_value

def curve_tightness(amount):
    """Change the curve tightness used to draw curves.

    :param amount: new curve tightness amount.
    :type amount: int
    """
    global curve_tightness_amount
    curve_tightness_amount = amount
    _reinit_curve_matrices()

@typecast_arguments_as_points
def curve_point(point_1, point_2, point_3, point_4, parameter):
    """Return the coordinates of a point along a curve.

    :param point_1: The first control point of the curve.
    :type point_1: 3-tuple.

    :param point_2: The second control point of the curve.
    :type point_2: 3-tuple.

    :param point_3: The third control point of the curve.
    :type point_3: 3-tuple.

    :param point_4: The fourth control point of the curve.
    :type point_4: 3-tuple.

    :param parameter: The parameter for the required point location
        along the curve. Should be in the range [0.0, 1.0] where 0
        indicates the start of the curve and 1 indicates the end of
        the curve.
    :type parameter: float

    :returns: The coordinate of the point at the required location
        along the curve.
    :rtype: Point (namedtuple with x, y, z attributes)

    """
    t = parameter
    basis = curve_basis_matrix
    P = [point_1, point_2, point_3, point_4]

    coeffs = [sum(t**(3 - i) * basis[4*i + j] for i in range(4)) for j in range(4)]

    x = sum(pt.x * c for pt, c in zip(P, coeffs))
    y = sum(pt.y * c for pt, c in zip(P, coeffs))

    return Point(x, y)

@typecast_arguments_as_points
def curve_tangent(point_1, point_2, point_3, point_4, parameter):
    """Return the tangent at a point along a curve.

    :param point_1: The first control point of the curve.
    :type point_1: 3-tuple.

    :param point_2: The second control point of the curve.
    :type point_2: 3-tuple.

    :param point_3: The third control point of the curve.
    :type point_3: 3-tuple.

    :param point_4: The fourth control point of the curve.
    :type point_4: 3-tuple.

    :param parameter: The parameter for the required tangent location
        along the curve. Should be in the range [0.0, 1.0] where 0
        indicates the start of the curve and 1 indicates the end of
        the curve.
    :type parameter: float

    :returns: The tangent at the required point along the curve.
    :rtype: Point (namedtuple with x, y, z attributes)

    """
    t = parameter
    basis = curve_basis_matrix
    P = [point_1, point_2, point_3, point_4]

    coeffs = [
        sum((3 - i)*(t**(2 - i)) * basis[4*i + j] for i in range(3))
        for j in range(4)
    ]

    x = sum(pt.x * c for pt, c in zip(P, coeffs))
    y = sum(pt.y * c for pt, c in zip(P, coeffs))

    return Point(x, y)

# Set the default values.
bezier_detail(20)
curve_detail(20)
curve_tightness(0)

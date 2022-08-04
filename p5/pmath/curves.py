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
"""Functions to work with Bezier curves and Catmul-Rom splines.

"""

from collections.abc import Iterable
from functools import wraps
from ..pmath import Point

__all__ = [
    # BEZIER METHODS
    "bezier_point",
    "bezier_tangent",
    "bezier_detail",
    # CURVE METHODS
    "curve_point",
    "curve_tangent",
    "curve_detail",
    "curve_tightness",
    # QUADRATIC METHODS
    "quadratic_point",
]

curve_resolution = 20

bezier_resolution = 20

curve_tightness_amount = 0

curve_basis_matrix = [
    [-0.5, 1.5, -1.5, 0.5],
    [1, -2.5, 2, -0.5],
    [-0.5, 0, 0.5, 0],
    [0, 1, 0, 0],
]


def typecast_arguments_as_points(func):
    """Typecast all but the last argument of the function as Points."""

    @wraps(func)
    def decorated(*args, **kwargs):
        new_args = [Point(*arg) for arg in args[:-1]]
        new_args.append(args[-1])
        ret_value = func(*new_args, **kwargs)
        return ret_value

    return decorated


def bezier_detail(detail_value):
    """Change the resolution used to draw bezier curves.

    :param detail_value: New resolution to be used.
    :type detail_value: int
    """
    global bezier_resolution
    bezier_resolution = max(1, detail_value)


def bezier_point(start, control_1, control_2, stop, parameter):
    """Return the coordinate of a point along a bezier curve.

    :param start: The start point of the bezier curve
    :type start: float or n-tuple

    :param control_1: The first control point of the bezier curve
    :type control_1: float or n-tuple

    :param control_2: The second control point of the bezier curve
    :type control_2: float or n-tuple

    :param stop: The end point of the bezier curve
    :type stop: float or n-tuple

    :param parameter: The parameter for the required location along
        the curve. Should be in the range [0.0, 1.0] where 0 indicates
        the start of the curve and 1 indicates the end of the curve.
    :type parameter: float

    :returns: The coordinate of the point along the bezier curve.
    :rtype: float or n-tuple

    """
    # Package floats into tuples
    is_iterable = isinstance(start, Iterable)
    if not is_iterable:
        start, control_1, control_2, stop = (
            (start,),
            (control_1,),
            (control_2,),
            (stop,),
        )

    t = parameter
    t_ = 1 - parameter
    P = [start, control_1, control_2, stop]
    coeffs = [t_ * t_ * t_, 3 * t * t_ * t_, 3 * t * t * t_, t * t * t]
    ans = tuple(sum(pt[i] * c for pt, c in zip(P, coeffs)) for i in range(len(start)))
    # Unpack answer if input is not iterable
    if not is_iterable:
        ans = ans[0]
    return ans


def bezier_tangent(start, control_1, control_2, stop, parameter):
    """Return the tangent at a point along a bezier curve.

    :param start: The start point of the bezier curve
    :type start: float or n-tuple.

    :param control_1: The first control point of the bezier curve
    :type control_1: float or n-tuple.

    :param control_2: The second control point of the bezier curve
    :type control_2: float or n-tuple.

    :param stop: The end point of the bezier curve
    :type stop: float or n-tuple.

    :param parameter: The parameter for the required tangent location
        along the curve. Should be in the range [0.0, 1.0] where 0
        indicates the start of the curve and 1 indicates the end of
        the curve.
    :type parameter: float

    :returns: The tangent at the required point along the bezier
        curve.
    :rtype: float or n-tuple

    """
    # Package floats into tuples
    is_iterable = isinstance(start, Iterable)
    if not is_iterable:
        start, control_1, control_2, stop = (
            (start,),
            (control_1,),
            (control_2,),
            (stop,),
        )

    t = parameter

    def tangent(a, b, c, d):
        return (
            3 * t * t * (3 * b - 3 * c + d - a) + 6 * t * (a - 2 * b + c) + 3 * (b - a)
        )

    ans = tuple(
        tangent(start[i], control_1[i], control_2[i], stop[i])
        for i in range(len(start))
    )
    # Unpack answer if input is not iterable
    if not is_iterable:
        ans = ans[0]
    return ans


def _reinit_curve_matrices():
    # TODO: Add basis matrices for faster tessellation.
    pass


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


def curve_point(point_1, point_2, point_3, point_4, parameter):
    """Return the coordinates of a point along a curve.

    :param point_1: The first control point of the curve.
    :type point_1: float or n-tuple.

    :param point_2: The second control point of the curve.
    :type point_2: float or n-tuple.

    :param point_3: The third control point of the curve.
    :type point_3: float or n-tuple.

    :param point_4: The fourth control point of the curve.
    :type point_4: float or n-tuple.

    :param parameter: The parameter for the required point location
        along the curve. Should be in the range [0.0, 1.0] where 0
        indicates the start of the curve and 1 indicates the end of
        the curve.
    :type parameter: float

    :returns: The coordinate of the point at the required location
        along the curve.
    :rtype: float or n-tuple

    """
    # Package floats into tuples
    is_iterable = isinstance(point_1, Iterable)
    if not is_iterable:
        point_1, point_2, point_3, point_4 = (
            (point_1,),
            (point_2,),
            (point_3,),
            (point_4,),
        )

    t = parameter
    basis = curve_basis_matrix
    P = [point_1, point_2, point_3, point_4]
    coeffs = [sum(t ** (3 - i) * basis[i][j] for i in range(4)) for j in range(4)]
    ans = tuple(sum(pt[i] * c for pt, c in zip(P, coeffs)) for i in range(len(point_1)))
    # Unpack answer if input is not iterable
    if not is_iterable:
        ans = ans[0]
    return ans


def curve_tangent(point_1, point_2, point_3, point_4, parameter):
    """Return the tangent at a point along a curve.

    :param point_1: The first control point of the curve.
    :type point_1: float or n-tuple.

    :param point_2: The second control point of the curve.
    :type point_2: float or n-tuple.

    :param point_3: The third control point of the curve.
    :type point_3: float or n-tuple.

    :param point_4: The fourth control point of the curve.
    :type point_4: float or n-tuple.

    :param parameter: The parameter for the required tangent location
        along the curve. Should be in the range [0.0, 1.0] where 0
        indicates the start of the curve and 1 indicates the end of
        the curve.
    :type parameter: float

    :returns: The tangent at the required point along the curve.
    :rtype: float or n-tuple

    """
    # Package floats into tuples
    is_iterable = isinstance(point_1, Iterable)
    if not is_iterable:
        point_1, point_2, point_3, point_4 = (
            (point_1,),
            (point_2,),
            (point_3,),
            (point_4,),
        )

    t = parameter
    basis = curve_basis_matrix
    P = [point_1, point_2, point_3, point_4]
    coeffs = [
        sum((3 - i) * (t ** (2 - i)) * basis[i][j] for i in range(3)) for j in range(4)
    ]
    ans = tuple(sum(pt[i] * c for pt, c in zip(P, coeffs)) for i in range(len(point_1)))
    # Unpack answer if input is not iterable
    if not is_iterable:
        ans = ans[0]
    return ans


def quadratic_point(start, control, stop, parameter):
    """Return the coordinates of a point along a bezier curve.

    :param point_1: The start point of the curve.
    :type point_1: float or n-tuple.

    :param point_3: The control point of the curve.
    :type point_3: float or n-tuple.

    :param point_4: The end point of the curve.
    :type point_4: float or n-tuple.

    :param parameter: The parameter for the required point location
        along the curve. Should be in the range [0.0, 1.0] where 0
        indicates the start of the curve and 1 indicates the end of
        the curve.
    :type parameter: float

    :returns: The coordinate of the point at the required location
        along the curve.
    :rtype: float or n-tuple

    """
    is_iterable = isinstance(start, Iterable)
    if not is_iterable:
        start, control, stop = (start,), (control,), (stop,)

    t = parameter
    t_ = 1 - parameter
    P = [start, control, stop]
    coeffs = [t_ * t_, 2 * t * t_, t * t]
    ans = tuple(sum(pt[i] * c for pt, c in zip(P, coeffs)) for i in range(len(start)))
    # Unpack answer if input is not iterable
    if not is_iterable:
        ans = ans[0]
    return ans


# Set the default values.
bezier_detail(20)
curve_detail(20)
curve_tightness(0)

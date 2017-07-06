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

__all__ = [ 'bezier_point', 'bezier_tangent', 'bezier_detail',
            'curve_point', 'curve_tangent', 'curve_detail', ]

Point = namedtuple('Point', ['x', 'y', 'z'])
Point.__new__.__defaults__ = (None, None, 0)

curve_resolution = 20
bezier_resolution = 20

def bezier_detail(detail_value):
    """Change the resolution used to draw bezier curves.

    :param detail_value: New resolution to be used.
    :type detail_value: int
    """
    global bezier_resolution
    bezier_resolution = detail_value

def curve_detail(detail_value):
    """Change the resolution used to draw bezier curves.

    :param detail_value: New resolution to be used.
    :type detail_value: int
    """
    global curve_resolution
    curve_resolution = detail_value

def _point_typecast(func):
    """Typecast all but the last argument of the function to Points.

    """
    @wraps(func):
    def decorated(*args, **kwargs):
        parameter = args[-1]
        new_args = [Point(*arg) for arg in args[:-1]]
        ret_value = func(*new_args, parameter, **kwargs)
        return ret_value
    return decorated

@_point_typecast
def bezier_point(start, stop, control_1, control_2, parameter):
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
    raise NotImplementedError()

@_point_typecast
def bezier_tangent(start, stop, control_1, control_2, parameter):
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
    raise NotImplementedError()
    
@_point_typecast
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
    raise NotImplementedError()

@_point_typecast
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
    raise NotImplementedError()

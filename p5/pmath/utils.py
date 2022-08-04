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
"""General purpose math utility functions.

"""

import math
from math import ceil, floor, exp, log, sqrt, modf
from math import degrees, radians
from math import sin, cos, tan
from math import asin, acos, atan, atan2

import numpy as np

__all__ = [
    # TRIG FUNCTIONS
    "sin",
    "cos",
    "tan",
    "degrees",
    "radians",
    # INVERSE TRIG FUNCTIONS
    "asin",
    "acos",
    "atan",
    "atan2",
    # TRIG CONSTANTS
    "TWO_PI",
    "PI",
    "HALF_PI",
    "QUARTER_PI",
    "TAU",
    "HALF_TAU",
    # MATH FUNCTIONS FROM THE STANDARD LIBRARY (abs and round are
    # available in builtins.)
    "ceil",
    "floor",
    "exp",
    "log",
    "sqrt",
    # MATH FUNCTIONS DEFINED HERE
    "constrain",
    "lerp",
    "remap",
    "normalize",
    "distance",
    "dist",
    "magnitude",
    "mag",
    "sq",
    "fract",
]

TWO_PI = 2 * math.pi
PI = math.pi
HALF_PI = math.pi / 2.0
QUARTER_PI = math.pi / 4.0

TAU = 2 * math.pi
HALF_TAU = math.pi

# We will be using these a lot, just precompute a whole lot of sin and
# cosine values.
SINCOS_PRECISION = 0.5
SINCOS_LENGTH = int(360 / SINCOS_PRECISION)

PRE_SIN = [sin(radians(d) * SINCOS_PRECISION) for d in range(SINCOS_LENGTH)]
PRE_COS = [cos(radians(d) * SINCOS_PRECISION) for d in range(SINCOS_LENGTH)]

SINCOS = list(zip(PRE_SIN, PRE_COS))


def _sanitize(point, target_dimension=3):
    return list(point) + [0] * (target_dimension - len(point))


def _is_numeric(val):
    return isinstance(val, int) or isinstance(val, float)


def constrain(amount, low, high):
    """Constrain the given value in the specified range.

    Examples ::

        >>> constrain(8, 1, 5)
        5

        >>> constrain(5, 1, 5)
        5

        >>> constrain(3, 1, 5)
        3

        >>> constrain(1, 1, 5)
        1

        >>> constrain(-3, 1, 5)
        1

    :param amount: The the value to be contrained.

    :param low: The lower constain.

    :param high: The upper constain.

    """
    if amount < low:
        return low
    elif amount > high:
        return high
    else:
        return amount


def lerp(start, stop, amount):
    """Linearly interpolate the start value to the stop value.

    Examples ::

        >>> lerp(0, 10, 0.0)
        0.0

        >>> lerp(0, 10, 0.5)
        5.0

        >>> lerp(0, 10, 0.8)
        8.0

        >>> lerp(0, 10, 1.0)
        10.0

    :param start: The start value

    :param stop: The stop value

    :param amount: The amount by which to interpolate. (:math:`0 \leq
        amount \leq 1`).
    :type amount: float

    """
    return start + amount * (stop - start)


def remap(value, source_range, target_range):
    """Remap a value from the source range to the target range.

    Examples ::

         >>> remap(50, (0, 100), (0, 10))
         5.0

         >>> remap(5, (0, 10), (0, 100))
         50.0

         >>> remap(5, (0, 10), (10, 20))
         15.0

         >>> remap(15, (10, 20), (0, 10))
         5.0

    :param value: The value to be remapped.

    :param source_range: The source range for :code:`value`
    :type source_range: tuple

    :param target_range: The target range for :code:`value`
    :type target_range: tuple

    """
    s0, s1 = source_range
    t0, t1 = target_range
    S = s1 - s0
    T = t1 - t0
    return t0 + ((value - s0) / S) * T


def normalize(value, low, high):
    """Normalize the given value to the specified range.

    Examples ::

        >>> normalize(10, 0, 100)
        0.1

        >>> normalize(0.3, 0, 1)
        0.3

        >>> normalize(100, 0, 100)
        1.0

        >>> normalize(1, 1, 15)
        0.0

    :param value:
    :type value: float

    :param low: The lower bound for the range.
    :type low: float

    :param high: The upper bound for the range.
    :type high: float
    """
    return remap(value, (low, high), (0, 1))


def magnitude(x, y, z=0):
    """Return the magnitude of the given vector.

    Examples ::

        >>> magnitude(3, 4)
        5.0

        >>> magnitude(2, 3, 6)
        7.0

        >>> magnitude(0, 0, 0)
        0.0

    :param x: The x-component of the vector.
    :type x: float

    :param y: The y-component of the vector.
    :type y: float

    :param z: The z-component of the vector (defaults to 0).
    :type z: float

    :returns: The magnitude of the vector.
    :rtype: float

    """
    return np.sqrt(np.sum(np.array([x, y, z]) ** 2))


def distance(point_1, point_2):
    """Return the distance between two points.

    Examples ::

        >>> distance((0, 0, 0), (2, 3, 6))
        7.0

        >>> distance((2, 3, 6), (2, 3, 6))
        0.0

        >>> distance((6, 6, 6), (2, 3, 6))
        5.0

    :param point_1:
    :type point_1: tuple

    :param point_2:
    :type point_2: tuple

    :returns: The distance between two points
    :rtype: float

    """
    p1 = np.array(_sanitize(point_1))
    p2 = np.array(_sanitize(point_2))
    return np.sqrt(np.sum((p1 - p2) ** 2))


def sq(number):
    """Square a number.

    Examples ::

        >>> square(-25)
        625

        >>> square(0)
        0

        >>> square(13)
        169


    :param number: The number to be squared.
    :type number: float

    :returns: The square of the number.
    :rtype: float

    """
    return number ** 2


def fract(number):
    """Calculates the fractional part of a number.

    Examples ::

        >>> fract(7345.73472742)
        0.73472742

        >>> fract(1.4215e-15)
        1.4215e-15

    :param number: Number whose fractional part needs to be found out.
    :type number: float

    :returns: Fractional part of the number.
    :rtype: float

    """
    return modf(number)[0]


# Helpful aliases
dist = distance
mag = magnitude

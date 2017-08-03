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
"""General purpose math utility functions.

"""

import math

from collections import namedtuple
from math import ceil, floor, exp, log, sqrt
from math import degrees, radians
from math import sin, cos, tan
from math import asin, acos, atan, atan2

__all__ = [
    # TRIG FUNCTIONS
    'sin', 'cos', 'tan', 'degrees', 'radians',

    # INVERSE TRIG FUNCTIONS
    'asin', 'acos', 'atan', 'atan2',

    # TRIG CONSTANTS
    'TWO_PI', 'PI', 'HALF_PI', 'QUARTER_PI', 'TAU', 'HALF_TAU',

    # MATH FUNCTIONS FROM THE STANDARD LIBRARY (abs and round are
    # available in builtins.)
    'ceil', 'floor', 'exp', 'log', 'sqrt',

    # MATH FUNCTIONS DEFINED HERE
    'constrain', 'lerp', 'remap', 'normalize', 'dist', 'magnitude', 'sq', 'pow'
]

Point = namedtuple('Point', ['x', 'y', 'z'])
Point.__new__.__defaults__ = (0, 0, 0)

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

PRE_SIN = [ sin(radians(d) * SINCOS_PRECISION) for d in range(SINCOS_LENGTH) ]
PRE_COS = [ cos(radians(d) * SINCOS_PRECISION) for d in range(SINCOS_LENGTH) ]

SINCOS = list(zip(PRE_SIN, PRE_COS))


def constrain(amount, low, high):
    """Constrain the given value in the specified range.

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

    :param start: The start value
    
    :param stop: The stop value

    :param amount: The amount by which to interpolate. (:math:`0 \leq
        amount \leq 1`).
    :type amount: float

    """
    return start + amount * (stop - start)

def remap(value, source_range, target_range):
    """Remap a value from the source range to the target range.

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

    :param x: The x-component of the vector.
    :type x: float

    :param y: The y-component of the vector.
    :type y: float

    :param z: The z-component of the vector (defaults to 0).
    :type z: float

    """
    return math.sqrt((x ** 2) + (y ** 2) + (z ** 2))

def dist(point_1, point_2):
    """Return the distance between two points.

    :param point_1:
    :type point_1: tuple

    :param point_2:
    :type point_2: tuple

    """
    p1 = Point(*point_1)
    p2 = Point(*point_2)
    return magnitude(p1.x - p2.x, p1.y - p2.y, p1.z - p2.z)

def pow(base, exponent):
    """Raise a number to a power.

    :param base: the number to be raised to a power.
    :type base: float

    :pararm exponent: the power to be raised to
    :type exponent: float

    :returns: :math:`{base}^{exponent}`
    :rtype: float

    """
    return base ** exponent

def sq(number):
    """Square a number.

    :param number: The number to be squared.
    :type number: float

    :returns: The square of the number.
    :rtype: float

    """
    return number ** 2

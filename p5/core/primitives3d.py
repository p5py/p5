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

from collections import namedtuple
import functools
import math
from math import sin
from math import cos
from math import radians

import numpy as np

from ..pmath import Point
from ..pmath import curves
from ..pmath import remap
from ..pmath.utils import SINCOS
from ..pmath.utils import SINCOS_PRECISION

from .shape import PShape

from . import p5

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

def _draw_on_return(func):
    """Set shape parameters to default renderer parameters

    """
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        s = func(*args, **kwargs)
        draw_shape(s)
        return s

    return wrapped

def draw_shape(shape, pos=(0, 0, 0)):
    """Draw the given shape at the specified location.

    :param shape: The shape that needs to be drawn.
    :type shape: p5.PShape

    :param pos: Position of the shape
    :type pos: tuple | Vector

    """
    p5.renderer.render(shape)
    for child_shape in shape.children:
        p5.renderer.render(child_shape)

@_draw_on_return
def plane(width, height):
    return PShape([
        (0, 0, 0), 
        (0, height, 0), 
        (width, height, 0), 
        (height, 0, 0)
        ])

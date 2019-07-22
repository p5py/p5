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

from vispy import geometry
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

@_draw_on_return
def cylinder(radius=20, height=20, detail_x=24, detail_y=1):
    """
    Draws a cylinder

    :param radius: radius of the surface
    :type radius: float

    :param height: height of the cylinder
    :type height: float

    :param detail_x: number of segments, the more segments the smoother geometry default is 24
    :type detail_x: int

    :param detail_y: number of segments in y-dimension, the more segments the smoother geometry default is 1
    :type detail_y: int
    """
    return geometry.create_cylinder(cols=detail_x, rows=detail_y, radius=[radius, radius], length=height)

@_draw_on_return
def cone(radius=20, height=20, detail_x=24, detail_y=1):
    """
    Draws a cone

    :param radius: radius of the bottom surface
    :type radius: float

    :param height: height of the cone
    :type height: float

    :param detail_x: number of segments, the more segments the smoother geometry default is 24
    :type detail_x: int

    :param detail_y: number of segments in y-dimension, the more segments the smoother geometry default is 1
    :type detail_y: int
    """
    return geometry.create_cone(cols=detail_x , radius=radius, length=height)

@_draw_on_return
def sphere(radius=10, detail_x=24, detail_y=24):
    """
    Draws a sphere

    :param radius: radius of the sphere
    :type radius: float

    :param detail_x: number of segments, the more segments the smoother geometry default is 24
    :type detail_x: int

    :param detail_y: number of segments, the more segments the smoother geometry default is 24
    :typ
    """
    return geometry.create_sphere(rows=detail_x, cols=detail_y, radius=radius)

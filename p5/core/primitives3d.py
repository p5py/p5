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

import numpy as np

from vispy import geometry
from . import p5
from .geometry import Geometry

from ..pmath import matrix

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

@_draw_on_return
def box(width, height, depth, detail_x=1, detail_y=1):
    geom = Geometry(detail_x, detail_y)

    cube_indices = [
        [0, 4, 2, 6], # -1, 0, 0],// -x
        [1, 3, 5, 7], # +1, 0, 0],// +x
        [0, 1, 4, 5], # 0, -1, 0],// -y
        [2, 6, 3, 7], # 0, +1, 0],// +y
        [0, 2, 1, 3], # 0, 0, -1],// -z
        [4, 5, 6, 7] # 0, 0, +1] // +z
    ]

    geom.stroke_indices = [
        [0, 1],
        [1, 3],
        [3, 2],
        [6, 7],
        [8, 9],
        [9, 11],
        [14, 15],
        [16, 17],
        [17, 19],
        [18, 19],
        [20, 21],
        [22, 23]
    ]

    for i in range(len(cube_indices)):
        cube_index = cube_indices[i]
        v = i * 4
        for j in range(4):
            d = cube_index[j]

            octant = [
                ((d & 1) * 2 - 1) / 2,
                ((d & 2) - 1) / 2,
                ((d & 4) / 2 - 1) / 2
            ]

            geom.vertices.append(octant)
            geom.uvs.extend([j & 1, (j & 2) / 2])

        geom.faces.append([v, v + 1, v + 2])
        geom.faces.append([v + 2, v + 1, v + 3])

    geom.compute_normals()
    geom.make_triangle_edges()
    #geom.compute_normals()
    geom.matrix = matrix.scale_transform(width, height, depth)

    return geom

@_draw_on_return
def plane(width, height, detail_x=1, detail_y=1):
    geom = Geometry(detail_x, detail_y)

    for i in range(detail_y + 1):
        v = i/detail_y
        for j in range(detail_x + 1):
            u = j/detail_x
            p = [u - 0.5, v - 0.5, 0]
            geom.vertices.append(p)
            geom.uvs.extend([u, v])

    geom.compute_faces()
    #geom.compute_normals()
    geom.make_triangle_edges()
    geom.matrix = matrix.scale_transform(width, height, 1)

    return geom

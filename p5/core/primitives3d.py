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
import functools
from .geometry import Geometry
from . import p5
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
    """Set shape parameters to default renderer parameters"""

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

    if isinstance(shape, Geometry):
        return

    for child_shape in shape.children:
        draw_shape(child_shape)


@_draw_on_return
def box(width, height, depth, detail_x=1, detail_y=1):
    """
    Draw a plane with given a width and height

    :param width: width of the box
    :type width: float

    :param height: height of the box
    :type height: float

    :param depth: depth of the box
    :type depth: float

    :param detail_x: Optional number of triangle subdivisions in x-dimension. Default is 1
    :type detail_x: integer

    :param detail_y: Optional number of triangle subdivisions in y-dimension. Default is 1
    :type detail_y: integer
    """

    geom = Geometry(detail_x, detail_y)

    cube_indices = [
        [0, 4, 2, 6],  # -1, 0, 0],// -x
        [1, 3, 5, 7],  # +1, 0, 0],// +x
        [0, 1, 4, 5],  # 0, -1, 0],// -y
        [2, 6, 3, 7],  # 0, +1, 0],// +y
        [0, 2, 1, 3],  # 0, 0, -1],// -z
        [4, 5, 6, 7],  # 0, 0, +1] // +z
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
        [22, 23],
    ]

    for i in range(len(cube_indices)):
        cube_index = cube_indices[i]
        v = i * 4
        for j in range(4):
            d = cube_index[j]

            octant = [((d & 1) * 2 - 1) / 2, ((d & 2) - 1) / 2, ((d & 4) / 2 - 1) / 2]

            geom.vertices.append(octant)
            geom.uvs.extend([j & 1, (j & 2) / 2])

        geom.faces.append([v, v + 1, v + 2])
        geom.faces.append([v + 2, v + 1, v + 3])

    geom.compute_normals()
    geom.make_triangle_edges()
    geom.matrix = matrix.scale_transform(width, height, depth)

    return geom


@_draw_on_return
def plane(width, height, detail_x=1, detail_y=1):
    """
    Draw a plane with given a width and height

    :param width: width of the plane
    :type width: float

    :param height: height of the plane
    :type height: float

    :param detail_x: Optional number of triangle subdivisions in x-dimension. Default is 1
    :type detail_x: integer

    :param detail_y: Optional number of triangle subdivisions in y-dimension. Default is 1
    :type detail_y: integer
    """
    geom = Geometry(detail_x, detail_y)

    for i in range(detail_y + 1):
        v = i / detail_y
        for j in range(detail_x + 1):
            u = j / detail_x
            p = [u - 0.5, v - 0.5, 0]
            geom.vertices.append(p)
            geom.uvs.extend([u, v])

    geom.compute_faces()
    geom.compute_normals()
    geom.make_triangle_edges()
    geom.edges_to_vertices()
    geom.matrix = matrix.scale_transform(width, height, 1)

    return geom


def sphere(radius=50, detail_x=24, detail_y=16):
    """
    Draw a sphere with given radius

    :param radius: radius of circle
    :type radius: float

    :param detail_x: Optional number of triangle subdivisions in x-dimension. Default is 24
    :type detail_x: integer

    :param detail_y: Optional number of triangle subdivisions in y-dimension. Default is 16
    :type detail_y: integer
    """

    return ellipsoid(radius, radius, radius, detail_x, detail_y)


@_draw_on_return
def ellipsoid(radius_x, radius_y, radius_z, detail_x=24, detail_y=24):
    """
    Draw an ellipsoid with given radius

    :param radius_x: x-radius of ellipsoid
    :type radius_x: float

    :param radius_y: y-radius of ellipsoid
    :type radius_y: float

    :param radius_z: z-radius of ellipsoid
    :type radius_z: float

    :param detail_x: Optional number of triangle subdivisions in x-dimension. Default is 24
    :type detail_x: integer

    :param detail_y: Optional number of triangle subdivisions in y-dimension. Default is 16
    :type detail_y: integer
    """
    geom = Geometry(detail_x, detail_y)

    for i in range(detail_y + 1):
        v = i / detail_y
        phi = math.pi * v - math.pi / 2
        cosPhi = math.cos(phi)
        sinPhi = math.sin(phi)

        for j in range(detail_x + 1):
            u = j / detail_x
            theta = 2 * math.pi * u
            cosTheta = math.cos(theta)
            sinTheta = math.sin(theta)
            p = [cosPhi * sinTheta, sinPhi, cosPhi * cosTheta]

            geom.vertices.append(p)
            geom.vertex_normals.append(p)
            geom.uvs.extend([u, v])

    geom.compute_faces()
    geom.make_triangle_edges()
    geom.edges_to_vertices()
    geom.matrix = matrix.scale_transform(radius_x, radius_y, radius_z)

    return geom


def truncated_cone(
    bottom_radius, top_radius, height, detail_x, detail_y, bottom_cap, top_cap
):
    geom = Geometry(detail_x, detail_y)

    bottom_radius = 1 if bottom_radius <= 0 else bottom_radius
    top_radius = 0 if top_radius < 0 else top_radius
    height = bottom_radius if height <= 0 else height
    detail_x = 3 if detail_x < 3 else detail_x
    detail_y = 1 if detail_y < 1 else detail_y

    start = -2 if bottom_cap else 0
    end = detail_y + (2 if top_cap else 0)

    slant = math.atan2(bottom_radius - top_radius, height)
    sin_slant = math.sin(slant)
    cos_slant = math.cos(slant)

    for yy in range(start, end + 1):
        # for the middle
        v = yy / detail_y
        y = height * v
        ring_radius = bottom_radius + (top_radius - bottom_radius) * v

        if yy < 0:
            # for the bottomCap edge
            y = 0
            v = 0
            ring_radius = bottom_radius
        elif yy > detail_y:
            # for the topCap edge
            y = height
            v = 1
            ring_radius = top_radius

        if yy == -2 or yy == detail_y + 2:
            # center of bottom or top caps
            ring_radius = 0

        y -= height / 2  # shift coordinate origin to the center of object
        for ii in range(detail_x):
            u = ii / detail_x
            ur = 2 * math.pi * u
            sur = math.sin(ur)
            cur = math.cos(ur)

            geom.vertices.append([sur * ring_radius, y, cur * ring_radius])

            if yy < 0:
                vertex_normals = [0, -1, 0]
            elif yy > detail_y and top_radius:
                vertex_normals = [0, 1, 0]
            else:
                vertex_normals = [sur * cos_slant, sin_slant, cur * cos_slant]

            geom.vertex_normals.append(vertex_normals)
            geom.uvs.extend([u, v])

    start_index = 0
    if bottom_cap:
        for jj in range(detail_x):
            nextjj = (jj + 1) % detail_x
            geom.faces.append(
                [
                    start_index + jj,
                    start_index + detail_x + nextjj,
                    start_index + detail_x + jj,
                ]
            )

        start_index += detail_x * 2

    for yy in range(detail_y):
        for ii in range(detail_x):
            nextii = (ii + 1) % detail_x
            geom.faces.append(
                [
                    start_index + ii,
                    start_index + nextii,
                    start_index + detail_x + nextii,
                ]
            )
            geom.faces.append(
                [
                    start_index + ii,
                    start_index + detail_x + nextii,
                    start_index + detail_x + ii,
                ]
            )

        start_index += detail_x

    if top_cap:
        start_index += detail_x
        for ii in range(detail_x):
            geom.faces.append(
                [
                    start_index + ii,
                    start_index + (ii + 1) % detail_x,
                    start_index + detail_x,
                ]
            )

    return geom


@_draw_on_return
def cylinder(
    radius=50, height=50, detail_x=24, detail_y=1, top_cap=True, bottom_cap=True
):
    """
    Draw a cylinder with given radius and height

    :param radius: radius of the surface
    :type radius: float

    :param height: height of the cylinder
    :type height: float

    :param detail_x: Number of segments, the more segments the smoother geometry. Default is 24
    :type detail_x: integer

    :param detail_y: number of segments in y-dimension, the more segments the smoother geometry. Default is 1
    :type detail_y: integer

    :param bottom_cap: whether to draw the bottom of the cylinder
    :type bottom_cap: boolean

    :param top_cap: whether to draw the top of the cylinder
    :type top_cap: boolean
    """

    geom = truncated_cone(1, 1, 1, detail_x, detail_y, bottom_cap, top_cap)
    geom.matrix = matrix.scale_transform(radius, height, radius)

    geom.make_triangle_edges()
    geom.edges_to_vertices()

    return geom


@_draw_on_return
def cone(radius=50, height=50, detail_x=24, detail_y=1, cap=True):
    """
    Draw a cone with given radius and height

    :param radius: radius of the bottom surface
    :type radius: float

    :param height: height of the cone
    :type height: float

    :param detail_x: Optional number of triangle subdivisions in x-dimension. Default is 24
    :type detail_x: integer

    :param detail_y: Optional number of triangle subdivisions in y-dimension. Default is 1
    :type detail_y: integer
    """
    geom = truncated_cone(1, 0, 1, detail_x, detail_y, cap, False)

    geom.make_triangle_edges()
    geom.edges_to_vertices()

    geom.matrix = matrix.scale_transform(radius, height, radius)
    return geom


@_draw_on_return
def torus(radius=50, tube_radius=10, detail_x=24, detail_y=16):
    """
    Draws torus on the window

    :param radius: radius of the whole ring
    :type radius: float

    :param tube_radius: radius of the tube
    :type tube_radius: float

    :param detail_x: Optional number of triangle subdivisions in x-dimension. Default is 24
    :type detail_x: integer

    :param detail_y: Optional number of triangle subdivisions in y-dimension. Default is 16
    :type detail_y: integer
    """
    tube_ratio = tube_radius / radius
    geom = Geometry(detail_x, detail_y)

    for i in range(detail_y + 1):
        v = i / detail_y
        phi = 2 * math.pi * v
        cosPhi = math.cos(phi)
        sinPhi = math.sin(phi)
        r = 1 + tube_ratio * cosPhi

        for j in range(detail_x + 1):
            u = j / detail_x
            theta = 2 * math.pi * u
            cosTheta = math.cos(theta)
            sinTheta = math.sin(theta)

            geom.vertices.append([r * cosTheta, r * sinTheta, tube_ratio * sinPhi])

        n = [cosPhi * cosTheta, cosPhi * sinTheta, sinPhi]
        geom.vertex_normals.append(n)
        geom.uvs.extend([u, v])

    geom.compute_faces()
    geom.make_triangle_edges()
    geom.edges_to_vertices()
    geom.matrix = matrix.scale_transform(radius, radius, radius)

    return geom

#
# Part of p5py: A Python package based on Processing
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

from .. import sketch

artist = sketch._p5_artist

class Shape:
    """Represents a Shape in p5py.

    :param kind: The type of this shape. Should be one of {'POLY', ...}
    :type kind: str

    :param vertices: A list of vertices (3-tuples) that make up the
        shape.
    :type vertices: list of tuples

    :param edges: A list of indices into the vertices list that
        represent edges. (Defaults to the empty list `[]`)
    :type edges: list of tuples

    """

    def __init__(self, kind, vertices, edges=[]):
        self.kind = kind
        self.vertices = vertices
        self.edges = edges

    def __repr__(self):
        return "({} Shape with vertices {})".format(self.kind, self.vertices)

    __str__ = __repr__

@artist
def point(x, y, z=0):
    """Returns a point Shape.

    :param x: x-coordinate of the shape.
    :type x: int or float

    :param y: y-coordinate of the shape.
    :type y: int or float

    :param z: z-coordinate of the shape (defaults to 0).
    :type z: int or float

    :returns: A point Shape.
    :rtype: Shape

    """
    return Shape('POLY', [(x, y, z)])

@artist
def line(start_point, end_point):
    """Returns a line Shape.

    :param start_point: Coordinates of the starting point of the line.
    :type start_point: tuple

    :param end_point: Coordinates of the end point of the line.
    :type end_point: tuple

    :returns: A line Shape.
    :rtype: Shape

    """
    if len(start_point) == 2:
        start_point = *start_point, 0
    if len(end_point) == 2:
        end_point = *end_point, 0
    return Shape('POLY', [start_point, end_point], [(0, 1)])

@artist
def rect(*args):
    """Returns a rect object."""
    raise NotImplementedError

# etc...

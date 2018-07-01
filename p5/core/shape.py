#
# Part of p5: A Python package based on Processing
# Copyright (C) 2017-2018 Abhik Pal
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
"""Shape class for p5.
"""

import builtins
from collections import namedtuple
import math
from math import sin
from math import cos
from math import radians

import numpy as np

from .. import sketch

__all__ = ['Shape']


class Shape:
    """Represents a Shape in p5py.

    :param kind: The type of this shape. Should be one of {'POLY', ...}
    :type kind: str

    :param vertices: A list of vertices (Point named-tuples) that make
        up the shape.
    :type vertices: list of named-tuples (of type `Point`)

    :param edges: A list of indices into the vertices list that
        represent edges. (Defaults to the empty list `[]`)
    :type edges: list of tuples

    """

    def __init__(self, vertices, kind='POLY', edges=None, faces=None,
                 visible=True):
        self.kind = kind
        self._raw_vertices = vertices
        self._vertices = None
        self._transformed_vertices = None
        self._edges = edges
        self._faces = faces
        self._texcoords = None
        self.visible = visible

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, is_visible):
        self._visible = is_visible
        if is_visible:
            # Shape, show thyself.
            sketch.draw_shape(self)

    @property
    def vertices(self):
        if self._vertices is None:
            self.tessellate()
        return self._vertices

    @property
    def edges(self):
        if self._edges is None:
            self.compute_edges()
        return self._edges

    @property
    def faces(self):
        if self._faces is None:
            self.compute_faces()
        return self._faces

    @property
    def texcoords(self):
        if self._texcoords is None:
            self.compute_texcoords()
        return self._texcoords

    @property
    def transformed_vertices(self):
        """The transformed vertices of the shape (when available)

        :note: This returns the un-transformed shape vertices when the
            shape hasn't been transformed.

        """
        if not self._transformed_vertices is None:
            return self._transformed_vertices
        return self.vertices

    @property
    def has_been_transformed(self):
        """Whether the shape has been transformed by a matrix."""
        return self._transformed_vertices is None

    def transform(self, matrix):
        """Use the given matrix to transform the shape's vertices

        :param matix: The transform matrix to use while transforming
            shape.
        :type matrix: np.ndarray

        """
        self._transformed_vertices = self.vertices.dot(matrix.T)

    def compute_faces(self):
        """Compute the faces for this shape."""
        self._faces = [
            (0, k, k + 1)
            for k in range(1, len(self.vertices) - 1)
        ]

    def compute_edges(self):
        """Compute the edges for this shape."""
        self._edges = [
            (k, k+1)
            for k in range(len(self.vertices) - 1)
        ]
        # connect the last vertex to the first vertex
        if not self.kind is 'PATH':
            self._edges.append((len(self.vertices) - 1, 0))

    def compute_texcoords(self):
        """Compute the texture coordinates for the current shape."""
        xs = [v[0] for v in self.vertices]
        ys = [v[1] for v in self.vertices]

        rangex = (min(xs), max(xs))
        rangey = (min(ys), max(ys))

        if (rangex[0] - rangex[1] == 0) or (rangey[0] - rangey[1] == 0):
            self._texcoords = ((0.5, 0.5) for v in self.vertices)
        else:
            self._texcoords = [
                (remap(x, rangex, (0, 1)), remap(y, rangey, (0, 1)))
                for x, y, z in self.vertices
            ]

    def tessellate(self):
        """Generate actual vertex data from limited number of parameters.
        """
        psig = ''.join((v.flag if not v.flag is None else 'D')
                       for v in self._raw_vertices)
        if 'D' in set(psig) and len(set(psig)) == 1:
            # the path is already tessellated. Nothing to be done.
            self._vertices = np.array(
                [(*v[:3], 1) for v in self._raw_vertices]
            )
        elif psig == 'DBBD':
            vertices = []
            steps = curves.bezier_resolution
            for i in range(steps + 1):
                t = i / steps
                p = curves.bezier_point(*self._raw_vertices, t)
                vertices.append((*p[:3], 1))
            self._vertices = np.array(vertices)
        elif psig == 'DCCD':
            vertices = []
            steps = curves.curve_resolution
            for i in range(steps + 1):
                t = i / steps
                p = curves.curve_point(*self._raw_vertices, t)
                vertices.append((*p[:3], 1))
            self._vertices = np.array(vertices)
        else:
            raise ValueError("Cannot complete tessillation. Unknown shape type.")




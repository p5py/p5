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
from contextlib import contextmanager
from functools import wraps

import numpy as np
from vispy import geometry

from .. import sketch

from .color import Color

__all__ = ['Shape', 'PShape']

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

def _ensure_editable(func):
    """A decorater that ensures that a shape is in 'edit' mode.

    """
    @wraps(func)
    def editable_method(instance, *args, **kwargs):
        if not instance._in_edit_mode:
            raise ValueError('{} only works in edit mode'.format(func.__name__))
        return func(instance, *args, **kwargs)
    return editable_method

class PShape:
    """Custom shape class for p5.

    :param vertices: List of (polygonal) vertices for the shape.
    :type vertices: list | np.ndarray

    :param fill_color: Fill color of the shape (default: 'auto' i.e.,
        the current renderer fill)
    :type fill_color: 'auto' | None | tuple | p5.Color

    :param stroke_color: Stroke color of the shape (default: 'auto'
        i.e., the current renderer stroke color)

    :type stroke_color: 'auto' | None | tuple | p5.color

    :param visible: toggles shape visibility (default: False)
    :type visible: bool

    :param children: List of sub-shapes for the current shape
        (default: [])
    :type children: list

    """
    def __init__(self, vertices=[], fill_color='auto', stroke_color='auto',
                 visible=False, children=[]):
        # basic properties of the shape
        self._vertices = np.array([])
        self._edges = None


        # a flag to check if the shape is being edited right now.
        self._in_edit_mode = False
        self._vertex_cache = None

        # The triangulation used to render the shapes.
        self._tri = None

        if len(vertices) > 0:
            self.vertices = vertices

        # TODO: support different vertex types
        self._vertex_types = ['P'] * len(vertices)

        # self.fill = fill_color
        # self.stroke = stroke_color

        # TODO: support adding children nodes.
        self.children = children

        self.visible = visible

    def _set_color(color, name, value):
        if value is 'auto':
            # get the current active colors
            raise NotImplementedError
        elif value is None:
            color = value
        elif isinstance(value, Color):
            color = value
        else:
            color = Color(*value)

        if name == 'stroke':
            self._stroke_color = color
        elif name == 'fill':
            self._fill_color = color

    @property
    def fill(self):
        return self._fill_color

    @fill.setter
    def fill(self, new_color):
        self._set_color('fill', new_color)

    @property
    def stroke(self):
        return self._stroke_color

    @stroke.setter
    def stroke(self, new_color):
       self._set_color('stroke', new_color)

    def _sanitize_vertex_list(self, vertices, tdim=2, sdim=3):
        """Convert all vertices to the given dimensions.

        :param vertices: List of vertices
        :type vertices: list

        :param tdim: Target dimension for sanitization (default: 3)
        :type tdim: int

        :param sdim: Source dimension for the points (default: 2).
            Whenever sdim > tdim, the last (sdim - tdim) components will
            be discarded.
        :type sdim: int

        :raises ValueError: when the point dimension is between sdim and tdim

        :returns: A sanitized array of vertices.
        :type: np.ndarray

        """
        sanitized = []

        for v in vertices:
            if (len(v) > max(tdim, sdim)) or (len(v) < min(tdim, sdim)):
                raise ValueError("unexpected vertex dimension")

            if tdim > sdim:
                sanitized.append(list(v) + [0] * (tdim - sdim))
            elif tdim < sdim:
                sanitized.append(list(v)[:tdim])
            else:
                sanitized.append(list(v))

        return np.array(sanitized)

    @property
    def vertices(self):
        return self._vertices

    @vertices.setter
    def vertices(self, new_vertices):
        self._vertices = self._sanitize_vertex_list(new_vertices)
        self._retriangulate()

    @property
    def edges(self):
        if self._edges is None:
            n, _ = self._vertices.shape
            self._edges = np.vstack([np.arange(n),
                                     (np.arange(n) + 1) % n]).transpose()
        return self._edges

    def _retriangulate(self):
        """Triangulate the shape
        """
        self._edges = None
        self._tri = geometry.Triangulation(self.vertices, self.edges)
        self._tri.triangulate()

    def _draw_data(self):
        """Data required to draw the shape.

        :returns: vertices, edges, faces of the current shape.
        :rtype: tuple
        """
        vertices = self._tri.pts

        if isinstance(self._tri.edges, np.ndarray):
            edges = self._tri.edges
        else:
            edges = np.array([])

        if isinstance(self._tri.tris, np.ndarray):
            faces = self._tri.tris
        else:
            faces = np.array([])

        return vertices, edges, faces

    def apply_matrix(self, matrix):
        """Transform all points based on the given matrix.

        :param matrix: a (4, 4) matrix specifying the transformation to
            be applied
        :type matrix: np.ndarray

        :returns: list of transformed vertices
        :rtype: np.ndarray

        """
        n = len(self._tri.pts)
        vertices = np.hstack([self._tri.pts, np.zeros((n, 1)), np.ones((n, 1))])
        transformed = np.dot(vertices, matrix.T)
        return transformed[:, :3]

    @contextmanager
    def edit(self, reset=True):
        """Put the shape in edit mode.

        :param reset: Toggles whether the shape should be "reset"
            during editing. When set to `True` all existing shape
            vertices are cleared. When set to `False` the new vertices
            are appended at the end of the existing vertex list.
            (default: True)
        :type reset: bool

        :raises ValueError: if the shape is already being edited.

        """
        if self._in_edit_mode:
            raise ValueError("Shape is being edited already")

        self._in_edit_mode = True
        if reset:
            self._vertices = np.array([])
        self._vertex_cache = []
        yield
        self.vertices = self._vertex_cache
        self._in_edit_mode = False

    @_ensure_editable
    def add_vertex(self, vertex):
        """Add a vertex to the current shape

        :param vertex: The (next) vertex to add to the current shape.
        :type vertex: tuple | list | p5.Vector | np.ndarray

        :raises ValueError:  when the vertex is of the wrong dimension
        """
        self._vertex_cache.append(vertex)

    def update_vertex(self, idx, vertex):
        """Edit an indicidual vertex.

        :param idx: index of the vertex to be edited
        :type idx: int

        :param vertex: The (next) vertex to add to the current shape.
        :type vertex: tuple | list | p5.Vector | np.ndarray

        :raises ValueError:  when the vertex is of the wrong dimension
        """
        if len(vertex) != 2:
            raise ValueError("Wrong vertex dimension")
        self._vertices[idx] =  np.array(vertex)
        self._retriangulate()

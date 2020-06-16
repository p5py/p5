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
"""Shape class for p5.
"""

import contextlib
import functools

import numpy as np
import triangle as tr

from .color import Color
from .constants import *
from ..pmath import matrix

from . import p5
from OpenGL.GLU import gluTessBeginPolygon, gluTessBeginContour, gluTessEndPolygon, gluTessEndContour, gluTessVertex

__all__ = ['PShape']

def _ensure_editable(func):
    """A decorater that ensures that a shape is in 'edit' mode.

    """
    @functools.wraps(func)
    def editable_method(instance, *args, **kwargs):
        if not instance._in_edit_mode:
            raise ValueError('{} only works in edit mode'.format(func.__name__))
        return func(instance, *args, **kwargs)
    return editable_method

def _apply_transform(func):
    """Apply the matrix transformation to the shape.
    """
    @functools.wraps(func)
    def mfunc(instance, *args, **kwargs):
        tmat = func(instance, *args, **kwargs)
        instance._matrix = instance._matrix.dot(tmat)
        return tmat
    return mfunc

def _call_on_children(func):
    """Call the method on all child shapes
    """
    @functools.wraps(func)
    def rfunc(instance, *args, **kwargs):
        rval = func(instance, *args, **kwargs)
        for child in instance.children:
            rfunc(child, *args, **kwargs)
        return rval
    return rfunc

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

    :param attribs: space-separated list of attributes that control
        shape drawing. Each attribute should be one of {'point',
        'path', 'open', 'closed'}. (default: 'closed')
    :type attribs: str

    :param children: List of sub-shapes for the current shape
        (default: [])
    :type children: list

    """
    def __init__(self, vertices=[], fill_color='auto',
                 stroke_color='auto', stroke_weight="auto",
                 stroke_join="auto", stroke_cap="auto",
                 visible=False, attribs='closed',
                 children=None, contour=[], temp_overriden_draw_queue=[], temp_stype='TESS'):
        # basic properties of the shape
        self._vertices = np.array([])
        self._contour = np.array([])
        self._edges = None
        self._outline = None
        self._outline_vertices = None

        self.attribs = set(attribs.lower().split())
        self._fill = None
        self._stroke = None
        self._stroke_weight = None
        self._stroke_cap = None
        self._stroke_join = None

        self._matrix = np.identity(4)
        self._transform_matrix = np.identity(4)
        self._transformed_draw_vertices = None

        # a flag to check if the shape is being edited right now.
        self._in_edit_mode = False
        self._vertex_cache = None

        # The triangulation used to render the shapes.
        self._tri = None
        self._tri_required = not ('point' in self.attribs) and \
                             not ('path' in self.attribs)
        self._tri_vertices = None
        self._tri_edges = None
        self._tri_faces = None

        if len(vertices) > 0:
            self.vertices = vertices

        if len(contour) > 0:
            self.contour = contour

        self.fill = fill_color
        self.stroke = stroke_color
        self.stroke_weight = stroke_weight
        self.stroke_cap = stroke_cap
        self.stroke_join = stroke_join

        self.children = children or []
        self.visible = visible

        self.temp_overriden_draw_queue = temp_overriden_draw_queue
        self.temp_vertices = []
        self.temp_stype = temp_stype
        self.temp_contours = [] # List of all contours
        self.temp_curr_contour = None # The contour currently being edited
        self.temp_all_vertices = set() # Set of all vertices (plus ones from contours)

    def _set_color(self, name, value=None):
        color = None

        if isinstance(value, Color):
            color = value
        else:
            if name == 'stroke' and p5.renderer.stroke_enabled:
                color = Color(*p5.renderer.stroke_color,
                              color_mode='RGBA', normed=True)
            if name == 'fill' and p5.renderer.fill_enabled:
                color = Color(*p5.renderer.fill_color,
                              color_mode='RGBA', normed=True)

        if name == 'stroke':
            self._stroke = color
        elif name == 'fill':
            self._fill = color

    @property
    def fill(self):
        return self._fill

    @fill.setter
    def fill(self, new_color):
        self._set_color('fill', new_color)

    @property
    def stroke(self):
        return self._stroke

    @stroke.setter
    def stroke(self, new_color):
        self._set_color('stroke', new_color)

    @property
    def stroke_weight(self):
        return self._stroke_weight

    @stroke_weight.setter
    def stroke_weight(self, stroke):
        if stroke == "auto":
            self._stroke_weight = p5.renderer.stroke_weight
        else:
            self._stroke_weight = stroke

    @property
    def stroke_join(self):
        return self._stroke_join

    @stroke_join.setter
    def stroke_join(self, stroke):
        if stroke == "auto":
            self._stroke_join = p5.renderer.stroke_join
        else:
            self._stroke_join = stroke

    @property
    def stroke_cap(self):
        return self._stroke_cap

    @stroke_cap.setter
    def stroke_cap(self, stroke):
        if stroke == "auto":
            self._stroke_cap = p5.renderer.stroke_cap
        else:
            self._stroke_cap = stroke

    @property
    def kind(self):
        if 'point' in self.attribs:
            return 'point'
        elif 'path' in self.attribs:
            return 'path'
        else:
            return 'poly'

    def _sanitize_vertex_list(self, vertices, tdim=2, sdim=3):
        """Convert all vertices to the given dimensions.
        Removes consecutive duplicates to prevent errors in triangulation.

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
        for i in range(len(vertices)):
            if i < len(vertices) - 1:
                if vertices[i] == vertices[i + 1]:
                    continue
            elif i == len(vertices) - 1 and i != 0:
                if vertices[i] == vertices[0]:
                    continue

            v = vertices[i]
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

        n = len(self._vertices)
        self._outline_vertices = np.hstack([self._vertices, np.zeros((n, 1))])
        self._tri_vertices = None
        self._tri_edges = None
        self._tri_faces = None

    @property
    def contour(self):
        return self._contour

    @contour.setter
    def contour(self, contour_vertices):
        self._contour = np.array(contour_vertices)

    def _compute_poly_edges(self):
        n, _ = self._vertices.shape
        return np.vstack([np.arange(n), (np.arange(n) + 1) % n]).transpose()

    def _compute_outline_edges(self):
        n, _ = self._vertices.shape
        return np.vstack([np.arange(n - 1),
                          (np.arange(n - 1) + 1) % n]).transpose()

    @property
    def edges(self):
        if 'point' in self.attribs:
            return np.array([])

        if self._edges is None:
            n, _ = self._vertices.shape

            if 'point' in self.attribs:
                self._edges = np.array([])
            elif 'path' in self.attribs:
                self._edges = self._compute_outline_edges()
            else:
                self._edges = self._compute_poly_edges()

            if 'open' in self.attribs:
                self._outline = self._compute_outline_edges()
            else:
                self._outline = self._edges

        return self._edges

    def get_interior_point(self, shape_vertices):
        # Returns a random point inside the shape
        if len(shape_vertices) < 2:
            return []

        # Triangulate the shape
        triangulate = tr.triangulate(dict(vertices=shape_vertices), "a5")
        for vertex in triangulate["vertices"]:
            if vertex not in shape_vertices:
                return [vertex]

        return []

    def _retriangulate(self):
        """Triangulate the shape
        """
        if len(self.vertices) < 2:
            self._tri_edges = np.array([])
            self._tri_faces = np.array([])
            self._tri_vertices = self.vertices
            return

        if len(self._contour) > 1:
            n, _ = self._contour.shape
            contour_edges = np.vstack([np.arange(n), (np.arange(n) + 1) % n]).transpose()
            triangulation_vertices = np.vstack([self.vertices, self._contour])
            triangulation_segments = np.vstack([self.edges, contour_edges + len(self.edges)])
            triangulate_parameters = dict(vertices=triangulation_vertices, 
                segments=triangulation_segments, holes=self.get_interior_point(self._contour))

            self._tri = tr.triangulate(triangulate_parameters, "p")
        else:
            triangulate_parameters = dict(vertices=self.vertices, segments=self.edges)
            self._tri = tr.triangulate(triangulate_parameters, "p")

        if "segments" in self._tri.keys():
            self._tri_edges = self._tri["segments"]
        else:
            self._tri_edges = self.edges

        self._tri_faces = self._tri["triangles"]
        self._tri_vertices = self._tri["vertices"]

    @property
    def _draw_outline_vertices(self):
        if 'open' in self.attribs:
            return self._draw_vertices
        return self.vertices

    @property
    def _draw_outline_edges(self):
        if 'open' in self.attribs:
            return self._outline
        return self._edges

    @property
    def _draw_vertices(self):
        if self._tri_required and (self._tri_vertices is None):
            self._retriangulate()

        if self._tri_required:
            return self._tri_vertices
        return self._vertices

    @property
    def _draw_edges(self):
        if self._tri_required:
            if self._tri_edges is None:
                self._retriangulate()
            return self._tri_edges
        return self.edges

    @property
    def _draw_faces(self):
        if self._tri_required:
            if self._tri_faces is None:
                self._retriangulate()
            return self._tri_faces

        return np.array([])

    @contextlib.contextmanager
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
        self._edges = None

    def temp_add_vertex_unsafe(self, vertex):
        self.temp_all_vertices.add(vertex)
        self.temp_vertices.append(vertex)

    def temp_add_contour_vertex_unsafe(self, vertex):
        self.temp_all_vertices.add(vertex)
        self.temp_curr_contour.append(vertex)

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
        self._tri_vertices = None
        self._tri_edges = None
        self._tri_faces = None
        self._edges = None

    def add_child(self, child):
        """Add a child shape to the current shape

        :param child: Child to be added
        :type child: PShape
        """
        self.children.append(child)

    def transform_matrix(self, mat):
        self._transform_matrix = mat

    @property
    def child_count(self):
        """Number of children.

        :returns: The current number of children.
        :rtype: int
        """
        return len(self.children)

    def apply_matrix(self, mat):
        """Apply the given transformation matrix to the shape.

        :param mat: the 4x4 matrix to be applied to the current shape.
        :type mat: (4, 4) np.ndarray

        """
        self._matrix = self._matrix.dot(mat)

    @_call_on_children
    def apply_transform_matrix(self, mat):
        self._matrix = self._matrix.dot(mat)

    @_call_on_children
    def reset_matrix(self):
        """Reset the transformation matrix associated with the shape.

        """
        self._matrix = np.identity(4)

    @_call_on_children
    @_apply_transform
    def translate(self, x, y, z=0):
        """Translate the shape origin to the given location.

        :param x: The displacement amount in the x-direction (controls
            the left/right displacement)
        :type x: int

        :param y: The displacement amount in the y-direction (controls
            the up/down displacement)
        :type y: int

        :param z: The displacement amount in the z-direction (0 by
            default). This controls the displacement away-from/towards
            the screen.
        :type z: int

        :returns: The translation matrix applied to the transform
            matrix.
        :rtype: np.ndarray

        """
        tmat = matrix.translation_matrix(x, y, z)
        return tmat

    @_call_on_children
    @_apply_transform
    def rotate(self, theta, axis=[0, 0, 1]):
        """Rotate the shape by the given angle along the given axis.

        :param theta: The angle by which to rotate (in radians)
        :type theta: float

        :param axis: The axis along which to rotate (defaults to the
            z-axis)
        :type axis: np.ndarray | list

        :returns: The rotation matrix used to apply the
            transformation.
        :rtype: np.ndarray

        """
        axis = np.array(axis[:])
        tmat = matrix.rotation_matrix(axis, theta)
        return tmat

    def rotate_x(self, theta):
        """Rotate the shape along the x axis.

        :param theta: angle by which to rotate (in radians)
        :type theta: float

        :returns: The rotation matrix used to apply the
            transformation.
        :rtype: np.ndarray

        """
        return self.rotate(theta, axis=[1, 0, 0])

    def rotate_y(self, theta):
        """Rotate the shape along the y axis.

        :param theta: angle by which to rotate (in radians)
        :type theta: float

        :returns: The rotation matrix used to apply the
             transformation.
        :rtype: np.ndarray

        """
        return self.rotate(theta, axis=[0, 1, 0])

    def rotate_z(self, theta):
        """Rotate the shape along the z axis.

        :param theta: angle by which to rotate (in radians)
        :type theta: float

        :returns: The rotation matrix used to apply the
            transformation.
        :rtype: np.ndarray

        """
        return self.rotate(theta)

    @_call_on_children
    @_apply_transform
    def scale(self, sx, sy=None, sz=None):
        """Scale the shape by the given factor.

        :param sx: scale factor along the x-axis.
        :type sx: float

        :param sy: scale factor along the y-axis (defaults to None)
        :type sy: float

        :param sz: scale factor along the z-axis (defaults to None)
        :type sz: float

        :returns: The transformation matrix used to appy the
            transformation.
        :rtype: np.ndarray

        """
        if (not sy) and (not sz):
            sy = sx
            sz = sx
        elif not sz:
            sz = 1
        tmat = matrix.scale_transform(sx, sy, sz)
        return tmat

    @_call_on_children
    @_apply_transform
    def shear_x(self, theta):
        """Shear shape along the x-axis.

        :param theta: angle to shear by (in radians)
        :type theta: float

        :returns: The shear matrix used to apply the tranformation.
        :rtype: np.ndarray

        """
        shear_mat = np.identity(4)
        shear_mat[0, 1] = np.tan(theta)
        return shear_mat

    @_call_on_children
    @_apply_transform
    def shear_y(self, theta):
        """Shear shape along the y-axis.

        :param theta: angle to shear by (in radians)
        :type theta: float

        :returns: The shear matrix used to apply the transformation.
        :rtype: np.ndarray

        """
        shear_mat = np.identity(4)
        shear_mat[1, 0] = np.tan(theta)
        return shear_mat

    # Given the number of vertices, return a numpy array of edges that connects those vertices sequentially
    def _get_sequential_edges(self, n):
        return np.hstack((np.vstack(np.arange(0, n - 1)),
                          np.vstack(np.arange(1, n))))

    # Given a list of vertices, return a line object that's ready to be inserted to draw queue
    def _get_line(self, vertices):
        return ['lines', np.asarray(vertices), self._get_sequential_edges(len(vertices))]

    # Given a list of vertices, evoke gluTess to create a contour
    # vertex_map is the map of every possible vertex to its index in a list of all vertices
    def _tess_new_contour(self, vertices, vertex_map):
        gluTessBeginContour(p5.tess.tess)
        for v in vertices:
            gluTessVertex(p5.tess.tess, v, vertex_map[v])
        gluTessEndContour(p5.tess.tess)

    # Returns a list of vertices and a map of vertex to its index
    def _gen_vertex_mapping(self, vertices):
        vertex_list = list(vertices)
        return vertex_list, { v: i for i, v in enumerate(vertex_list) }

    def temp_triangulate(self):
        # Add meshes
        if p5.renderer.fill_enabled and self.temp_stype not in [SType.POINTS.name, SType.LINES.name]:
            vertex_list, vertex_map = self._gen_vertex_mapping(self.temp_all_vertices)
            gluTessBeginPolygon(p5.tess.tess, None)
            self._tess_new_contour(self.temp_vertices, vertex_map)
            if len(self.temp_contours) > 0:
                for i, contour in enumerate(self.temp_contours):
                    self._tess_new_contour(contour, vertex_map)
            gluTessEndPolygon(p5.tess.tess)
            self.temp_overriden_draw_queue += [[obj[0], np.asarray(vertex_list), np.asarray(obj[1], dtype=np.uint32)]
                                              for obj in p5.tess.process_draw_queue()]

        # Add borders
        if p5.renderer.stroke_enabled and self.temp_stype not in [SType.POINTS.name]:
            self.temp_overriden_draw_queue.append(self._get_line(self.temp_vertices))
            for contour in self.temp_contours:
                self.temp_overriden_draw_queue.append(self._get_line(contour))

    def begin_contour(self):
        self.temp_curr_contour = []

    def end_contour(self):
        # Unlike end_shape, end_contour does not take the optional 'CLOSE'
        # Just in case, we manually close the contour
        self.temp_curr_contour.append(self.temp_curr_contour[-1])
        # Add current contour to canonical list
        self.temp_contours.append(self.temp_curr_contour)
        self.temp_curr_contour = None

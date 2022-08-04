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
import math

from p5.core.color import Color
from p5.core.constants import SType
from p5.pmath import matrix
from p5.pmath.vector import Point
from p5.pmath.utils import SINCOS
from p5.core import p5

__all__ = ["PShape"]


def _ensure_editable(func):
    """A decorater that ensures that a shape is in 'edit' mode."""

    @functools.wraps(func)
    def editable_method(instance, *args, **kwargs):
        if not instance._in_edit_mode:
            raise ValueError("{} only works in edit mode".format(func.__name__))
        return func(instance, *args, **kwargs)

    return editable_method


def _apply_transform(func):
    """Apply the matrix transformation to the shape."""

    @functools.wraps(func)
    def mfunc(instance, *args, **kwargs):
        tmat = func(instance, *args, **kwargs)
        instance._matrix = instance._matrix.dot(tmat)
        return tmat

    return mfunc


def _call_on_children(func):
    """Call the method on all child shapes"""

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

    :param children: List of sub-shapes for the current shape
        (default: [])
    :type children: list

    """

    def __init__(
        self,
        fill_color="auto",
        stroke_color="auto",
        stroke_weight="auto",
        stroke_join="auto",
        stroke_cap="auto",
        visible=False,
        children=None,
        contours=tuple(),
        vertices=tuple(),
        shape_type=SType.TESS,
    ):
        # basic properties of the shape
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

        self.fill = fill_color
        self.stroke = stroke_color
        self.stroke_weight = stroke_weight
        self.stroke_cap = stroke_cap
        self.stroke_join = stroke_join

        self.children = children or []
        self.visible = visible

        self.vertices = list(vertices)
        self.shape_type = shape_type
        self.contours = [list(c) for c in contours]  # List of all contours

    def _set_color(self, name, value=None):
        color = None

        if isinstance(value, Color):  # Is Color, no need to parse
            color = value
        else:  # Not Color, attempt to parse it
            if name == "stroke" and p5.renderer.style.stroke_enabled:
                color = Color(
                    *p5.renderer.style.stroke_color, color_mode="RGBA", normed=True
                )
            if name == "fill" and p5.renderer.style.fill_enabled:
                color = Color(
                    *p5.renderer.style.fill_color, color_mode="RGBA", normed=True
                )

        if name == "stroke":
            self._stroke = color
        elif name == "fill":
            self._fill = color

    @property
    def fill(self):
        return self._fill

    @fill.setter
    def fill(self, new_color):
        self._set_color("fill", new_color)

    @property
    def stroke(self):
        return self._stroke

    @stroke.setter
    def stroke(self, new_color):
        self._set_color("stroke", new_color)

    @property
    def stroke_weight(self):
        return self._stroke_weight

    @stroke_weight.setter
    def stroke_weight(self, stroke):
        if stroke == "auto":
            self._stroke_weight = p5.renderer.style.stroke_weight
        else:
            self._stroke_weight = stroke

    @property
    def stroke_join(self):
        return self._stroke_join

    @stroke_join.setter
    def stroke_join(self, stroke):
        if stroke == "auto":
            self._stroke_join = p5.renderer.style.stroke_join
        else:
            self._stroke_join = stroke

    @property
    def stroke_cap(self):
        return self._stroke_cap

    @stroke_cap.setter
    def stroke_cap(self, stroke):
        if stroke == "auto":
            self._stroke_cap = p5.renderer.style.stroke_cap
        else:
            self._stroke_cap = stroke

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
        if reset:
            self.vertices = []
            self.contours = []
        self._in_edit_mode = True
        yield
        self._in_edit_mode = False

    @_ensure_editable
    def add_vertex(self, vertex):
        """Add a vertex to the current shape

        :param vertex: The (next) vertex to add to the current shape.
        :type vertex: tuple | list | p5.Vector | np.ndarray
        """
        self.vertices.append(Point(*vertex))

    @_ensure_editable
    def update_vertex(self, idx, vertex):
        """Edit an individual vertex.

        :param idx: index of the vertex to be edited
        :type idx: int

        :param vertex: The (next) vertex to add to the current shape.
        :type vertex: tuple | list | p5.Vector | np.ndarray
        """
        self.vertices[idx] = Point(*vertex)

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
        """Reset the transformation matrix associated with the shape."""
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
    def rotate(self, theta, axis=(0, 0, 1)):
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
        if sy is None and sz is None:
            sy = sx
            sz = sx
        elif sz is None:
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


class Arc(PShape):
    def __init__(
        self,
        center,
        radii,
        start_angle,
        stop_angle,
        mode=None,
        fill_color="auto",
        stroke_color="auto",
        stroke_weight="auto",
        stroke_join="auto",
        stroke_cap="auto",
        **kwargs
    ):
        self._center = center
        self._radii = radii
        self._start_angle = start_angle
        self._stop_angle = stop_angle
        self.arc_mode = mode

        gl_type = SType.TESS if mode in ["OPEN", "CHORD"] else SType.TRIANGLE_FAN
        super().__init__(
            fill_color=fill_color,
            stroke_color=stroke_color,
            stroke_weight=stroke_weight,
            stroke_join=stroke_join,
            stroke_cap=stroke_cap,
            shape_type=gl_type,
            **kwargs
        )
        self._tessellate()

    def _tessellate(self):
        """Generate vertex and face data using radii."""
        rx = self._radii[0]
        ry = self._radii[1]

        c1x = self._center[0]
        c1y = self._center[1]
        s1 = p5.renderer.transform_matrix.dot(np.array([c1x, c1y, 0, 1]))

        c2x = c1x + rx
        c2y = c1y + ry
        s2 = p5.renderer.transform_matrix.dot(np.array([c2x, c2y, 0, 1]))

        sdiff = s2 - s1
        size_acc = (
            np.sqrt(np.sum(sdiff * sdiff)) * math.pi * 2
        ) / POINT_ACCURACY_FACTOR

        acc = min(MAX_POINT_ACCURACY, max(MIN_POINT_ACCURACY, int(size_acc)))
        inc = int(len(SINCOS) / acc)

        sclen = len(SINCOS)
        start_index = int((self._start_angle / (math.pi * 2)) * sclen)
        end_index = int((self._stop_angle / (math.pi * 2)) * sclen)

        vertices = [(c1x, c1y, 0)] if self.arc_mode in ["PIE", None] else []
        for idx in range(start_index, end_index, inc):
            i = idx % sclen
            vertices.append((c1x + rx * SINCOS[i][1], c1y + ry * SINCOS[i][0], 0))
        vertices.append(
            (
                c1x + rx * SINCOS[end_index % sclen][1],
                c1y + ry * SINCOS[end_index % sclen][0],
                0,
            )
        )
        if self.arc_mode == "CHORD" or self.arc_mode == "PIE":
            vertices.append(vertices[0])
        self.vertices = vertices

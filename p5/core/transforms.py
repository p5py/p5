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

import builtins
from contextlib import contextmanager
import math

from ..sketch import renderer
from ..pmath import Matrix4
from ..pmath import Vector

from ..tmp.euclid import Vector3

__all__ = ['push_matrix', 'reset_transforms', 'translate', 'rotate',
           'rotate_x', 'rotate_y', 'rotate_z', 'scale', 'shear_x',
           'shear_y', 'camera', 'frustum', 'ortho', 'perspective',
           'print_matrix', 'reset_matrix', 'apply_matrix']

@contextmanager
def push_matrix():
    previous_matrix = renderer.transform_matrix.copy()
    try:
        yield previous_matrix
    finally:
        renderer.transform_matrix = previous_matrix

def reset_transforms():
    """Reset all transformations to their default state.

    """
    renderer.reset_view()

def translate(x, y, z=0):
    """Translate the display origin to the given location.

    :param x: The displacement amount in the x-direction (controls the
        left/right displacement)

    :type x: int

    :param y: The displacement amount in the y-direction (controls the
        up/down displacement)

    :type y: int

    :param z: The displacement amount in the z-direction (0 by
        default). This controls the displacement away-from/towards the
        screen.
    :type z: int

    """
    renderer.transform_matrix.translate(x, y, z)

def rotate(theta, axis=Vector3(0, 0, 1)):
    """Rotate the display by the given angle along the given axis.

    :param theta: The angle by which to rotate (in radians)
    :type theta: float

    :param axis: The axis along which to rotate (defaults to the z-axis)
    :type axis: Vector3
    """
    renderer.transform_matrix.rotate_axis(theta, axis)

def rotate_x(theta):
    """Rotate the view along the x axis.

    :param theta: angle by which to rotate (in radians)
    :type theta: float
    """
    renderer.transform_matrix.rotatex(theta)

def rotate_y(theta):
    """Rotate the view along the y axis.

    :param theta: angle by which to rotate (in radians)
    :type theta: float
    """
    renderer.transform_matrix.rotatey(theta)

def rotate_z(theta):
    """Rotate the view along the z axis.

    :param theta: angle by which to rotate (in radians)
    :type theta: float
    """
    renderer.transform_matrix.rotatez(theta)

def scale(sx, sy=None, sz=None):
    """Scale the display by the given factor.

    :param sx: scale factor along the x-axis.
    :type sx: float

    :param sy: scale factor along the y-axis (defaults to None)
    :type sy: float

    :param sz: scale factor along the z-axis (defaults to None)
    :type sz: float
    """
    if (not sy) and (not sz):
        sy = sx
        sz = sx
    elif not sz:
        sz = 1
    renderer.transform_matrix.scale(sx, sy, sz)

def apply_matrix(transform_matrix):
    """Use the given matrix as the sketch's transform matrix.

    :param transform_matrix: The new transform matrix.
    :type transform_matrix: Matrix4
    """
    renderer.transform_matrix = transform_matrix

def reset_matrix():
    """Reset the current transform matrix.
    """
    renderer.transform_matrix = Matrix4()

def print_matrix():
    """Print the transform matrix being used by the sketch.
    """
    print(renderer.transform_matrix)

# Matrix structure:
#     a b c d
#     e f g h
#     i j k l
#     m n o p

def shear_x(theta):
    """Shear display along the x-axis.

    :param theta: angle to shear by (in radians)
    :type theta: float
    """
    shear_mat = Matrix4()
    shear_mat.b = math.tan(theta)
    renderer.transform_matrix = renderer.transform_matrix * shear_mat

def shear_y(theta):
    """Shear display along the y-axis.

    :param theta: angle to shear by (in radians)
    :type theta: float
    """
    shear_mat = Matrix4()
    shear_mat.e = math.tan(theta)
    renderer.transform_matrix = renderer.transform_matrix * shear_mat

def _screen_coordinates(x, y, z=0):
    """Return the screen coordinates for the given point.

    :param x: x coordinates of the input point.
    :type x: float

    :param y: y coordinates of the input point.
    :type y: float

    :param z: z coordinates of the input point (defaults to 0).
    :type z: float

    :returns: a vector with the transformed x, y, z coordinates.
    :rtype: Vector

    """
    p = renderer.transform_matrix * Vector3(x, y, z)
    return Vector(p.x, p.y, p.z)

def camera():
    raise NotImplementedError

def frustum():
    raise NotImplementedError

def ortho():
    raise NotImplementedError

def perspective():
    raise NotImplementedError

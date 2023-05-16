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

import numpy as np


def _magnitude(arr: np.ndarray) -> float:
    """Return the magnitude of the given array.

    :param arr: Input array.

    :returns: The magnitude of the input array.
    """
    return np.sqrt(arr.dot(arr))


def _normalize(arry: np.ndarray) -> np.ndarray:
    """Return the normalized version of the given array.

    :param arry: Input array to be normalized.

    :returns: Normalized version of the input array.

    """
    mag = _magnitude(arry)
    return arry / mag


def scale_transform(x: float, y: float, z: float = 1) -> np.ndarray:
    """Return a scale transformation matrix.

    :param x: Scale factor in the x direction.

    :param y: Scale factor in the y direction.

    :param z: Scale factor in the z direction.

    :returns: A scale transformation matrix.

    """
    scale_matrix = np.identity(4)
    scale_matrix[0, 0] = x
    scale_matrix[1, 1] = y
    scale_matrix[2, 2] = z
    return scale_matrix


def translation_matrix(x: float, y: float, z: float = 0) -> np.ndarray:
    """Return a new translation matrix.

    :param x: translation in the x-direction.

    :param y: translation in the y-direction.

    :param z: translation in the z-direction.

    :returns: A transform matrix with the given translation applied to
        it

    """
    translate_matrix = np.identity(4)
    translate_matrix[0, -1] = x
    translate_matrix[1, -1] = y
    translate_matrix[2, -1] = z
    return translate_matrix


def rotation_matrix(axis: np.ndarray, angle: float) -> np.ndarray:
    """Return a rotation matrix with the given angle and rotation.

    :param axis: The axis along which the matrix should be rotated.

    :param angle: Angle by which to rotate (in radians).

    :returns: A rotation matrix along the given axis and angle.

    """
    x, y, z = _normalize(axis)
    s = np.sin(angle)
    c = np.cos(angle)
    c1 = 1 - c

    rotation = np.identity(4)

    rotation[0, 0] = x * x * c1 + c
    rotation[0, 1] = x * y * c1 - z * s
    rotation[0, 2] = x * z * c1 + y * s
    rotation[1, 0] = y * x * c1 + z * s
    rotation[1, 1] = y * y * c1 + c
    rotation[1, 2] = y * z * c1 - x * s
    rotation[2, 0] = x * z * c1 - y * s
    rotation[2, 1] = y * z * c1 + x * s
    rotation[2, 2] = z * z * c1 + c

    return rotation


def euler_rotation_matrix(heading, attitude, bank):
    """

    :returns: A rotation matrix based on the given parameters.
    :rtype: np.ndarray
    """
    pass


def triple_axis_rotation_matrix(
    x: np.ndarray, y: np.ndarray, z: np.ndarray
) -> np.ndarray:
    """Return a rotation matrix based on three axes.

    :param x: x-axis for the rotation matrix.

    :param y: y-axis for the rotation matrix.

    :param z: z-axis for the rotation matrix.

    :returns: A rotation matrix based on the given parameters.
    """
    rotation_matrix = np.identity(4)
    rotation_matrix[0, :3] = x
    rotation_matrix[1, :3] = y
    rotation_matrix[2, :3] = z
    return rotation_matrix


def look_at(eye: np.ndarray, at: np.ndarray, up: np.ndarray) -> np.ndarray:
    """Return a new 'look-at' matrix.

    :param eye: Location of the 'eye'

    :param at: The point being looked at.

    :param up: Vector specifying the up-direction.

    :returns: A new look at matrix.
    """
    z = _normalize(eye - at)
    x = _normalize(np.cross(up, z))
    y = np.cross(z, x)

    mat = triple_axis_rotation_matrix(x, y, z)
    mat.transpose()

    mat[0, 3] = (-1) * x.dot(eye)
    mat[1, 3] = (-1) * y.dot(eye)
    mat[2, 3] = (-1) * z.dot(eye)

    return mat


def perspective_matrix(
    field_of_view: float, aspect_ratio: float, near_plane: float, far_plane: float
) -> np.ndarray:
    """Return a perspective matrix.

    :param field_of_view: The field_of_view to use.

    :param aspect_ratio: The aspect ratio of the projection.

    :param near_plane: Location of the near plane of the projection.

    :param far_plane: Location of the far plane of the projection.

    :returns: A new perspective matrix.

    :raises AssertionError: When the near plane is zero or the near
         plane is the same as the far plane.

    """
    assert not math.isclose(near_plane, 0), "Near plane cannot be at zero."
    assert not math.isclose(
        near_plane, far_plane
    ), "Near plane and far plane can't be same"
    f = 1 / math.tan(field_of_view / 2)
    mat = np.identity(4)
    mat[0, 0] = f / aspect_ratio
    mat[1, 1] = f
    mat[2, 2] = (far_plane + near_plane) / (near_plane - far_plane)
    mat[2, 3] = 2 * far_plane * near_plane / (near_plane - far_plane)
    mat[3, 2] = -1
    mat[3, 3] = 0
    return mat

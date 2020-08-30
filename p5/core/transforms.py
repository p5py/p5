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

from contextlib import AbstractContextManager
import numpy as np
import math
import builtins
from ..pmath import matrix

from . import p5

__all__ = ['push_matrix', 'pop_matrix', 'reset_transforms',
           'translate', 'rotate', 'rotate_x', 'rotate_y', 
           'rotate_z', 'scale', 'shear_x', 'shear_y', 
           'camera', 'frustum', 'ortho', 'perspective',
           'print_matrix', 'reset_matrix', 'apply_matrix']

class _MatrixContext(AbstractContextManager):
    def __exit__(self, exc_type, exc_value, traceback):
        pop_matrix()

matrix_stack = []

def push_matrix():
    """Pushes the current transformation matrix onto the matrix stack.
    """
    matrix_stack.append(p5.renderer.transform_matrix.copy())
    return _MatrixContext()

def pop_matrix():
    """Pops the current transformation matrix off the matrix stack.
    """
    assert len(matrix_stack) > 0, "No matrix to pop"
    p5.renderer.transform_matrix = matrix_stack.pop()

def reset_transforms():
    """Reset all transformations to their default state.

    """
    p5.renderer.transform_matrix = np.identity(4)

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

    :returns: The translation matrix applied to the transform matrix.
    :rtype: np.ndarray

    """
    tmat = matrix.translation_matrix(x, y, z)
    p5.renderer.transform_matrix = p5.renderer.transform_matrix.dot(tmat)
    return tmat

def rotate(theta, axis=np.array([0, 0, 1])):
    """Rotate the display by the given angle along the given axis.

    :param theta: The angle by which to rotate (in radians)
    :type theta: float

    :param axis: The axis along which to rotate (defaults to the z-axis)
    :type axis: np.ndarray or list

    :returns: The rotation matrix used to apply the transformation.
    :rtype: np.ndarray

   """
    axis = np.array(axis[:])
    tmat = matrix.rotation_matrix(axis, theta)
    p5.renderer.transform_matrix = p5.renderer.transform_matrix.dot(tmat)
    return tmat

def rotate_x(theta):
    """Rotate the view along the x axis.

    :param theta: angle by which to rotate (in radians)
    :type theta: float

    :returns: The rotation matrix used to apply the transformation.
    :rtype: np.ndarray

    """
    rotate(theta, axis=np.array([1, 0, 0]))

def rotate_y(theta):
    """Rotate the view along the y axis.

    :param theta: angle by which to rotate (in radians)
    :type theta: float

    :returns: The rotation matrix used to apply the transformation.
    :rtype: np.ndarray

   """
    rotate(theta, axis=np.array([0, 1, 0]))

def rotate_z(theta):
    """Rotate the view along the z axis.

    :param theta: angle by which to rotate (in radians)
    :type theta: float

    :returns: The rotation matrix used to apply the transformation.
    :rtype: np.ndarray

   """
    rotate(theta, axis=np.array([0, 0, 1]))

def scale(sx, sy=None, sz=None):
    """Scale the display by the given factor.

    :param sx: scale factor along the x-axis.
    :type sx: float

    :param sy: scale factor along the y-axis (defaults to None)
    :type sy: float

    :param sz: scale factor along the z-axis (defaults to None)
    :type sz: float

    :returns: The transformation matrix used to appy the transformation.
    :rtype: np.ndarray
    """
    if sy is None and sz is None:
        sy = sx
        sz = sx
    elif sz is None:
        sz = 1
    tmat = matrix.scale_transform(sx, sy, sz)
    p5.renderer.transform_matrix = p5.renderer.transform_matrix.dot(tmat)
    return tmat

def apply_matrix(transform_matrix):
    """Apply the given matrix to the sketch's transform matrix..

    :param transform_matrix: The new transform matrix.
    :type transform_matrix: np.ndarray (or a 4×4 list)
    """
    tmatrix = np.array(transform_matrix)
    p5.renderer.transform_matrix = p5.renderer.transform_matrix.dot(tmatrix)

def reset_matrix():
    """Reset the current transform matrix.
    """
    p5.renderer.transform_matrix = np.identity(4)

def print_matrix():
    """Print the transform matrix being used by the sketch.
    """
    print(p5.renderer.transform_matrix)

def shear_x(theta):
    """Shear display along the x-axis.

    :param theta: angle to shear by (in radians)
    :type theta: float

    :returns: The shear matrix used to apply the tranformation.
    :rtype: np.ndarray

    """
    shear_mat = np.identity(4)
    shear_mat[0, 1] = np.tan(theta)
    p5.renderer.transform_matrix = p5.renderer.transform_matrix.dot(shear_mat)
    return shear_mat

def shear_y(theta):
    """Shear display along the y-axis.

    :param theta: angle to shear by (in radians)
    :type theta: float

    :returns: The shear matrix used to apply the transformation.
    :rtype: np.ndarray

    """
    shear_mat = np.identity(4)
    shear_mat[1, 0] = np.tan(theta)
    p5.renderer.transform_matrix = p5.renderer.transform_matrix.dot(shear_mat)
    return shear_mat

def camera(*args, **kwargs):
    """Sets the camera position for a 3D sketch. 
    Parameters for this function define the position for 
    the camera, the center of the sketch (where the 
    camera is pointing), and an up direction (the 
    orientation of the camera).

    When called with no arguments, this function 
    creates a default camera equivalent to::

        camera((0, 0, height / math.tan(math.pi / 6))),
               (0, 0, 0),
               (0, 1, 0))

    :param position_x: x-coordinate of the position vector
    :type position_x: float

    :param position_y: y-coordinate of the position vector
    :type position_y: float

    :param position_z: z-coordinate of the position vector
    :type position_z: float

    :param target_x: x-coordinate of the target vector
    :type target_x: float

    :param target_y: y-coordinate of the target vector
    :type target_y: float

    :param target_z: z-coordinate of the target vector
    :type target_z: float

    :param up_x: x-coordinate of the up vector
    :type up_x: float

    :param up_y: y-coordinate of the up vector
    :type up_y: float

    :param up_z: z-coordinate of the up vector
    :type up_z: float

    :param position: camera position coordinates
    :type position: tuple

    :param target_position: target position of camera in world coordinates 
    :type target_position: tuple

    :param up_vector: up direction vector for the camera
    :type up_vector: tuple

    """
    def real_camera(position=(0, 0, p5.sketch.size[1] / math.tan(math.pi / 6)),
                    target_position=(0, 0, 0), up_vector=(0, 1, 0)):
        p5.renderer.lookat_matrix = matrix.look_at(
            np.array(position),
            np.array(target_position),
            np.array(up_vector))
        p5.renderer.camera_pos = np.array(position)

    if len(args) == 9: # If using non-tuple arguments
        kwargs['position'] = args[:3]
        kwargs['target_position'] = args[3:6]
        kwargs['up_vector'] = args[6:]
    elif len(args) <= 3: # If using tuple arguments
        if len(args) >= 1:
            kwargs['position'] = args[0]
        if len(args) >= 2:
            kwargs['target_position'] = args[1]
        if len(args) >= 3:
            kwargs['up_vector'] = args[2]
    else:
        raise ValueError("Unexpected number of arguments passed to camera()")

    real_camera(**kwargs)


def perspective(fovy, aspect, near, far):
    """
    Sets a perspective projection for the camera in a 3D sketch.  

    :param fovy: camera frustum vertical field of view, from bottom to top of view, in angleMode units
    :type fovy: float

    :param aspect: camera frustum aspect ratio
    :type aspect: float

    :param near: frustum near plane length
    :type near: float

    :param far: frustum far plane length
    :type far: float   
    """
    p5.renderer.projection_matrix = matrix.perspective_matrix(
            fovy,
            aspect,
            near,
            far
        )

def ortho(left, right, bottom, top, near, far):
    """
    Sets an orthographic projection for the camera in
    a 3D sketch and defines a box-shaped viewing frustum
    within which objects are seen.

    :param left: camera frustum left plane
    :type left: float

    :param right: camera frustum right plane
    :type right: float

    :param bottom: camera frustum bottom plane
    :type bottom: float

    :param top: camera frustum top plane
    :type top: float

    :param near: camera frustum near plane
    :type near: float

    :param far: camera frustum far plane
    :type far: float   
    """
    p5.renderer.projection_matrix = np.array([
        [2/(right - left), 0, 0, -(right + left)/(right - left)],
        [0, 2/(top - bottom), 0, -(top + bottom)/(top - bottom)],
        [0, 0, -2/(far - near), -(far + near)/(far - near)],
        [0, 0, 0, 1],
        ])

def frustum():
    raise NotImplementedError

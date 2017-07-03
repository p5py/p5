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
from ..tmp.euclid import Matrix4
from ..tmp.euclid import Vector3

__all__ = ['push_matrix', 'reset_transforms', 'translate', 'rotate',
           'rotate_x', 'rotate_y', 'rotate_z', 'scale', 'shear_x',
           'shear_y', 'camera', 'frustum', 'ortho', 'perspective']

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
    renderer.transform_matrix.translate(x, y, z)

def rotate(theta, axis=Vector3(0, 0, 1)):
    renderer.transform_matrix.rotate_axis(theta, axis)
    
def rotate_x(theta):
    renderer.transform_matrix.rotatex(theta)

def rotate_y(theta):
    renderer.transform_matrix.rotatey(theta)

def rotate_z(theta):
    renderer.transform_matrix.rotatez(theta)

def scale(sx, sy=None, sz=None):
    if (not sy) and (not sz):
        sy = sx
        sz = sx
    elif not sz:
        sz = 1
    renderer.transform_matrix.scale(sx, sy, sz)

# Matrix structure:
#     a b c d
#     e f g h
#     i j k l
#     m n o p

def shear_x(theta):
    shear_mat = Matrix4()
    shear_mat.b = math.tan(theta)
    renderer.transform_matrix = renderer.transform_matrix * shear_mat

def shear_y(theta):
    shear_mat = Matrix4()
    shear_mat.e = math.tan(theta)
    renderer.transform_matrix = renderer.transform_matrix * shear_mat

def camera():
    raise NotImplementedError

def frustum():
    raise NotImplementedError

def ortho():
    raise NotImplementedError

def perspective():
    raise NotImplementedError

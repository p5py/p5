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

from collections import deque
from contextlib import contextmanager
import math

from ..opengl import renderer
from .. import sketch
from ..tmp.euclid import Matrix4
from ..tmp.euclid import Vector3

__all__ = ['push_matrix', 'reset_transforms', 'translate', 'rotate',
           'rotate_x', 'rotate_y', 'rotate_z', 'scale', 'shear_x',
           'shear_y', 'camera', 'frustum', 'ortho', 'perspective']

@contextmanager
def push_matrix():
    current_matrix = renderer._matrix_stack[0].copy()
    renderer._matrix_stack.appendleft(current_matrix)
    try:
        yield current_matrix
    finally:
        renderer._matrix_stack.popleft()

def reset_transforms():
    cz = (sketch.height / 2) / math.tan(math.radians(30))

    projection = Matrix4.new_perspective(
        math.radians(60),
        sketch.width/sketch.height,
        0.1 * cz,
        10 * cz
    )
    view = Matrix4()
    view.translate(-sketch.width / 2,
                   -sketch.height/2, -cz)

    renderer._matrix_stack = deque()
    renderer._matrix_stack.append(Matrix4())

    renderer._attribute['view'] =  view
    renderer._attribute['projection'] =  projection
    renderer._attribute['model'] =  renderer._matrix_stack[0]

def translate(x, y, z=0):
    renderer._matrix_stack[0].translate(x, y, z)

def rotate(theta, axis=Vector3(0, 0, 1)):
    renderer._matrix_stack[0].rotate_axis(theta, axis)
    
def rotate_x(theta):
    renderer._matrix_stack[0].rotatex(theta)

def rotate_y(theta):
    renderer._matrix_stack[0].rotatey(theta)

def rotate_z(theta):
    renderer._matrix_stack[0].rotatez(theta)

def scale(sx, sy=None, sz=None):
    if (not sy) and (not sz):
        sy = sx
        sz = sx
    elif not sz:
        sz = 1
    renderer._matrix_stack[0].scale(sx, sy, sz)

#
# Matrix structure:
#     a b c d
#     e f g h
#     i j k l
#     m n o p

def shear_x(theta):
    shear_mat = Matrix4()
    shear_mat.b = math.tan(theta)
    renderer._matrix_stack[0] = renderer._matrix_stack[0] * shear_mat

def shear_y(theta):
    shear_mat = Matrix4()
    shear_mat.e = math.tan(theta)
    renderer._matrix_stack[0] = renderer._matrix_stack[0] * shear_mat

def camera():
    raise NotImplementedError

def frustum():
    raise NotImplementedError

def ortho():
    raise NotImplementedError

def perspective():
    raise NotImplementedError

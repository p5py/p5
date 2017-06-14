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

import math

from .. import sketch
from ..tmp.euclid import Vector3
from ..tmp.euclid import Matrix4

def reset_transforms():
    cz = (sketch.height / 2) / math.tan(math.radians(30))
    sketch.mat_projection = Matrix4.new_perspective(
        math.radians(60),
        sketch.width/sketch.height,
        0.1 * cz,
        10 * cz
    )
    sketch.mat_view = Matrix4()
    sketch.mat_view.translate(-sketch.width / 2,
                              -sketch.height/2, -cz)
    sketch.mat_model = Matrix4()

def translate(x, y, z=0):
    sketch.mat_model.translate(x, y, z)

def rotate(theta, axis=Vector3(0, 0, 1)):
    sketch.mat_model.rotate_axis(theta, axis)
    
def rotate_x(theta):
    sketch.mat_model.rotatex(theta)

def rotate_y(theta):
    sketch.mat_model.rotatey(theta)

def rotate_z(theta):
    sketch.mat_model.rotatez(theta)

def scale(sx, sy=None, sz=None):
    if (not sy) and (not sz):
        sy = sx
        sz = sx
    elif not sz:
        sz = 1
    sketch.mat_model.scale(sx, sy, sz)

#
# Matrix structure:
#     a b c d
#     e f g h
#     i j k l
#     m n o p

def shear_x(theta):
    shear_mat = Matrix4()
    shear_mat.b = math.tan(theta)
    sketch.mat_model = sketch.mat_model * shear_mat

def shear_y(theta):
    shear_mat = Matrix4()
    shear_mat.e = math.tan(theta)
    sketch.mat_model = sketch.mat_model * shear_mat

def camera():
    raise NotImplementedError

def frustum():
    raise NotImplementedError

def ortho():
    raise NotImplementedError

def perspective():
    raise NotImplementedError

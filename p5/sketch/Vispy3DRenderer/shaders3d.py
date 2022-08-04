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
"""Shaders used by the main program"""

from collections import namedtuple
from ..util import read_shader

ShaderSource = namedtuple("ShaderSource", "vert frag")

src_default = ShaderSource(
    read_shader("Vispy3DRenderer/shaders/3d/default3d.vert"),
    read_shader("Vispy3DRenderer/shaders/common/default.frag"),
)
# Shader sources to draw framebuffers textues.
src_fbuffer = ShaderSource(
    read_shader("Vispy3DRenderer/shaders/common/fbuffer.vert"),
    read_shader("Vispy3DRenderer/shaders/common/fbuffer.frag"),
)
src_normal = ShaderSource(
    read_shader("Vispy3DRenderer/shaders/3d/normal.vert"),
    read_shader("Vispy3DRenderer/shaders/3d/normal.frag"),
)
src_phong = ShaderSource(
    read_shader("Vispy3DRenderer/shaders/3d/phong.vert"),
    read_shader("Vispy3DRenderer/shaders/3d/phong.frag"),
)

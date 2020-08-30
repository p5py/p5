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
from contextlib import contextmanager
from copy import copy

from . import primitives
from . import color
from . import p5

@contextmanager
def push_style():
    """Save the current style settings and then restores them on exit.

    The 'style' information consists of all the parameters controlled
    by the following functions (the ones indicated by an asterisks '*'
    aren't available yet):

    - background
    - fill, no_fill
    - stroke, no_stroke
    - rect_mode
    - ellipse_mode
    - shape_mode
    - color_mode
    - tint
    - (*) stroke_weight
    - (*) stroke_cap
    - (*) stroke_join
    - (*) image_mode
    - (*) text_align
    - (*) text_font
    - (*) text_mode
    - (*) text_size
    - (*) text_leading
    -  emissive
    -  specular
    -  shininess
    -  ambient
    -  material

    """
    prev_style = copy(p5.renderer.style)

    prev_ellipse_mode = primitives._ellipse_mode
    prev_rect_mode = primitives._rect_mode
    prev_shape_mode = primitives._shape_mode

    prev_color_mode = color.color_parse_mode
    prev_color_range = color.color_range

    prev_ambient, prev_diffuse, prev_specular, prev_shininess, prev_material = [None] * 5
    if p5.mode == 'P3D':
        prev_ambient = p5.renderer.ambient
        prev_diffuse = p5.renderer.diffuse
        prev_specular = p5.renderer.specular
        prev_shininess = p5.renderer.shininess
        prev_material = p5.renderer.material

    yield

    p5.renderer.style = prev_style

    primitives._ellipse_mode = prev_ellipse_mode
    primitives._rect_mode = prev_rect_mode
    primitives._shape_mode = prev_shape_mode

    color.prev_color_parse_mode = prev_color_mode
    color.prev_color_range = prev_color_range

    if p5.mode == 'P3D':
        p5.renderer.ambient = prev_ambient
        p5.renderer.diffuse = prev_diffuse
        p5.renderer.specular = prev_specular
        p5.renderer.shininess = prev_shininess
        p5.renderer.material = prev_material

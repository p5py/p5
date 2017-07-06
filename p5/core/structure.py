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
from contextlib import contextmanager

from ..sketch import renderer
from . import primitives

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
    - (*) tint
    - (*) stroke_weight
    - (*) stroke_cap
    - (*) stroke_join
    - (*) image_mode
    - (*) color_mode
    - (*) text_align
    - (*) text_font
    - (*) text_mode
    - (*) text_size
    - (*) text_leading
    - (*) emissive
    - (*) specular
    - (*) shininess
    - (*) ambient

    """
    prev_background_color = renderer.background_color
    prev_fill_color = renderer.fill_color
    prev_stroke_color = renderer.stroke_color
    prev_fill_enabled = renderer.fill_enabled
    prev_stroke_enabled = renderer.stroke_enabled
    prev_ellipse_mode = primitives._ellipse_mode
    prev_rect_mode = primitives._rect_mode
    prev_shape_mode = primitives._shape_mode
    try:
        yield
    finally:
        renderer.background_color = prev_background_color
        renderer.fill_color = prev_fill_color
        renderer.stroke_color = prev_stroke_color
        renderer.fill_enabled = prev_fill_enabled
        renderer.stroke_enabled = prev_stroke_enabled
        primitives._ellipse_mode = prev_ellipse_mode
        primitives._rect_mode = prev_rect_mode
        primitives._shape_mode = prev_shape_mode


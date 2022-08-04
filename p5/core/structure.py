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
from copy import deepcopy

from . import p5

from contextlib import AbstractContextManager


class _StyleContext(AbstractContextManager):
    def __exit__(self, exc_type, exc_value, traceback):
        pop_style()


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
    renderer_styles = deepcopy(p5.renderer.style)
    p5.renderer.style_stack.append(renderer_styles)
    return _StyleContext()


def pop_style():
    """Restores previously pushed style settings"""
    assert len(p5.renderer.style_stack) > 0, "No styles to pop"
    renderer_styles = p5.renderer.style_stack.pop()

    p5.renderer.style = renderer_styles

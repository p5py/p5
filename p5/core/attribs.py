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

from ..sketch import renderer
from .color import Color
from .primitives import rect
from .structure import push_style
from .transforms import push_matrix

__all__ = [ 'background', 'fill', 'no_fill',
            'stroke', 'no_stroke', 'tint', 'no_tint' ]

def fill(*fill_args, **fill_kwargs):
    """Set the fill color of the shapes.

    :param fill_args: positional arguments to be parsed as a color.
    :type fill_args: tuple

    :param fill_kwargs: keyword arguments to be parsed as a color.
    :type fill_kwargs: dict

    :returns: The fill color.
    :rtype: Color

    """
    fill_color = Color(*fill_args, **fill_kwargs)
    renderer.fill_enabled = True
    renderer.fill_image_enabled = False
    renderer.fill_color = fill_color.normalized
    return fill_color

def no_fill():
    """Disable filling geometry."""
    renderer.fill_enabled = False

def stroke(*color_args, **color_kwargs):
    """Set the color used to draw lines around shapes

    :param color_args: positional arguments to be parsed as a color.
    :type color_args: tuple

    :param color_kwargs: keyword arguments to be parsed as a color.
    :type color_kwargs: dict

    :note: Both color_args and color_kwargs are directly sent to
        Color.parse_color

    :returns: The stroke color.
    :rtype: Color
    """
    stroke_color = Color(*color_args, **color_kwargs)
    renderer.stroke_enabled = True
    renderer.stroke_color = stroke_color.normalized

def no_stroke():
    """Disable drawing the stroke around shapes."""
    renderer.stroke_enabled = False

def tint(*color_args, **color_kwargs):
    """Set the tint color for the sketch.

    :param color_args: positional arguments to be parsed as a color.
    :type color_args: tuple

    :param color_kwargs: keyword arguments to be parsed as a color.
    :type color_kwargs: dict

    :note: Both color_args and color_kwargs are directly sent to
        Color.parse_color

    :returns: The tint color.
    :rtype: Color
    """
    raise NotImplementedError("Renderer doesn't support textures.")

def no_tint():
    """Disable tinting of images."""
    raise NotImplementedError("Renderer doesn't support textures.")

def background(*color_args, **color_kwargs):
    """Set the background color for the renderer.

    :param color_args: positional arguments to be parsed as a color.
    :type color_args: tuple

    :param color_kwargs: keyword arguments to be parsed as a color.
    :type color_kwargs: dict

    :note: Both color_args and color_kwargs are directly sent to
        Color.parse_color

    :returns: The background color.
    :rtype: Color
    """
    with push_style():
        background_color = Color(*color_args, **color_kwargs, color_mode='RGB')
        fill(background_color)
        no_stroke()
        with push_matrix():
            rect((0, 0), builtins.width, builtins.height, mode='CORNER')
    renderer.background_color = background_color.normalized
    return background_color

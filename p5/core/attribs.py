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

import builtins

from .color import Color
from .image import image
from .image import image_mode
from .image import PImage
from .structure import push_style
from .transforms import push_matrix
from .constants import SQUARE, PROJECT, ROUND, MITER, BEVEL

from . import p5

__all__ = [
    "background",
    "clear",
    "fill",
    "no_fill",
    "stroke",
    "no_stroke",
    "tint",
    "no_tint",
    "stroke_weight",
    "stroke_cap",
    "stroke_join",
]


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
    p5.renderer.style.fill_enabled = True
    p5.renderer.fill_image_enabled = False
    p5.renderer.style.fill_color = fill_color.normalized
    return fill_color


def no_fill():
    """Disable filling geometry."""
    p5.renderer.style.fill_enabled = False


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
    p5.renderer.style.stroke_enabled = True
    p5.renderer.style.stroke_color = stroke_color.normalized


def stroke_weight(thickness):
    """Sets the width of the stroke used for lines, points, and the border around shapes. All widths are set in units of pixels.

    :param weight: thickness of stroke in pixels
    :type weight: int

    """
    p5.renderer.style.stroke_weight = thickness


def no_stroke():
    """Disable drawing the stroke around shapes."""
    p5.renderer.style.stroke_enabled = False


def stroke_cap(c):
    """Sets the style of line endings. The ends are SQUARE,
    PROJECT, and ROUND. The default cap is ROUND.

    :param c: either 'SQUARE', 'PROJECT' or 'ROUND'
    :type c: string

    """
    if c in [SQUARE, PROJECT, ROUND]:
        p5.renderer.style.set_stroke_cap(c)
    else:
        raise ValueError("Invalid Stroke Cap %s" % c)


def stroke_join(j):
    """Sets the style of the joints which connect line segments.
    These joints are either mitered, beveled, or rounded and
    specified with the corresponding parameters MITER, BEVEL,
    and ROUND. The default joint is MITER.

    :param weight: either 'MITER', 'BEVEL' or 'ROUND'
    :type j: string

    """
    if j in [MITER, BEVEL, ROUND]:
        p5.renderer.style.set_stroke_join(j)
    else:
        raise ValueError("Invalid Stroke Cap %s" % j)


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
    tint_color = Color(*color_args, **color_kwargs)
    p5.renderer.style.tint_enabled = True
    p5.renderer.style.tint_color = tint_color.normalized


def no_tint():
    """Disable tinting of images."""
    p5.renderer.style.tint_enabled = False


def background(*args, **kwargs):
    """Set the background color for the p5.renderer.

    :param args: positional arguments to be parsed as a color.
    :type color_args: tuple

    :param kwargs: keyword arguments to be parsed as a color.
    :type kwargs: dict

    :note: Both args and color_kwargs are directly sent to
        color.parse_color

    :note: When setting an image as the background, the dimensions of
        the image should be the same as that of the sketch window.

    :returns: The background color or image.
    :rtype: p5.Color | p5.PImage

    :raises ValueError: When the dimensions of the image and the
        sketch do not match.

    """
    if builtins.current_renderer == "vispy":
        if len(args) == 1 and isinstance(args[0], PImage):
            background_image = args[0]
            sketch_size = (builtins.width, builtins.height)

            if sketch_size != background_image.size:
                msg = "Image dimension {} and sketch dimension {} do not match"
                raise ValueError(msg.format(background_image.size, sketch_size))

            with push_style():
                no_tint()
                image_mode("corner")
                with push_matrix():
                    image(background_image, (0, 0))

            return background_image

        with push_style():
            background_color = Color(*args, **kwargs)
            fill(background_color)
            no_stroke()

            with push_matrix():
                p5.renderer.style.background_color = background_color.normalized
                p5.renderer.clear()
    else:
        p5.renderer.background(*args, **kwargs)


def clear():
    """
    Clears the pixels within a buffer.
    """
    p5.renderer.clear()

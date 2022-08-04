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
import textwrap

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageFilter
from PIL import ImageChops

from .image import image
from .image import PImage
from .structure import push_style

from . import p5

__all__ = [
    "create_font",
    "load_font",
    "text",
    "text_font",
    "text_align",
    "text_leading",
    "text_size",
    "text_width",
    "text_ascent",
    "text_descent",
]

_font_family = ImageFont.load_default()
_text_align_x = "LEFT"
_text_align_y = "TOP"
_text_leading = 0


def create_font(name, size=10):
    """Create the given font at the appropriate size.

    :param name: Filename of the font file (only pil, otf and ttf
        fonts are supported.)
    :type name: str

    :param size: Font size (only required when `name` refers to a
        truetype font; defaults to None)
    :type size: int | None

    """

    if name.endswith("ttf") or name.endswith("otf"):
        font = ImageFont.truetype(name, size)
    elif name.endswith("pil"):
        font = ImageFont.load(name)
    else:
        raise NotImplementedError("Font type not supported.")

    return font


def load_font(font_name):
    """Loads the given font into a font object"""
    return create_font(font_name)


def text(*args, wrap_at=None):
    """Draw the given text on the screen and save the image.

    :param text_string: text to display
    :type text_string: str

    :param x: x-coordinate of text
    :type x: float

    :param y: y-coordinate of text
    :type y: float

    :param z: z-coordinate of text
    :type z: float

    :param position: position of the text on the screen
    :type position: tuple

    :param wrap_at: specifies the text wrapping column (defaults to
        None)
    :type wrap_at: int

    :returns: actual text that was drawn to the image (when wrapping
        is not set, this is just the unmodified text_string)
    :rtype: str

    """
    if len(args) == 2:
        text_string, position = args
    elif len(args) == 3 or len(args) == 4:
        text_string, position = args[0], args[1:]
    else:
        raise ValueError("Unexpected number of arguments passed to text()")

    if len(text_string) == 0:
        return

    global _font_family, _text_leading

    multiline = False
    if not (wrap_at is None):
        text_string = textwrap.fill(text_string, wrap_at)
        size = _font_family.getsize_multiline(text_string)
        multiline = True
    elif "\n" in text_string:
        multiline = True
        size = list(_font_family.getsize_multiline(text_string))
        size[1] += _text_leading * text_string.count("\n")
    else:
        size = _font_family.getsize(text_string)

    is_stroke_valid = False  # True when stroke_weight != 0
    is_min_filter = False  # True when stroke_weight <0
    if p5.renderer.style.stroke_enabled:
        stroke_weight = p5.renderer.style.stroke_weight
        if stroke_weight < 0:
            stroke_weight = abs(stroke_weight)
            is_min_filter = True

        if stroke_weight > 0:
            if stroke_weight % 2 == 0:
                stroke_weight += 1
            is_stroke_valid = True

    if is_stroke_valid:
        new_size = list(map(lambda x: x + 2 * stroke_weight, size))
        is_stroke_valid = True
        text_xy = (stroke_weight, stroke_weight)
    else:
        new_size = size
        text_xy = (0, 0)

    canvas = Image.new("RGBA", new_size, color=(0, 0, 0, 0))
    canvas_draw = ImageDraw.Draw(canvas)

    if multiline:
        canvas_draw.multiline_text(
            text_xy, text_string, font=_font_family, spacing=_text_leading
        )
    else:
        canvas_draw.text(text_xy, text_string, font=_font_family)

    text_image = PImage(*new_size)
    text_image._img = canvas

    if is_stroke_valid:
        if is_min_filter:
            canvas_dilate = canvas.filter(ImageFilter.MinFilter(stroke_weight))
        else:
            canvas_dilate = canvas.filter(ImageFilter.MaxFilter(stroke_weight))
        canvas_stroke = ImageChops.difference(canvas, canvas_dilate)
        text_stroke_image = PImage(*new_size)
        text_stroke_image._img = canvas_stroke

    width, height = new_size
    position = list(position)
    if _text_align_x == "LEFT":
        position[0] += 0
    elif _text_align_x == "RIGHT":
        position[0] -= width
    elif _text_align_x == "CENTER":
        position[0] -= width / 2

    if _text_align_y == "TOP":
        position[1] += 0
    elif _text_align_y == "BOTTOM":
        position[1] -= height
    elif _text_align_y == "CENTER":
        position[1] -= height / 2

    with push_style():
        if p5.renderer.style.fill_enabled:
            p5.renderer.style.tint_enabled = True
            p5.renderer.style.tint_color = p5.renderer.style.fill_color
            image(text_image, position)
        if p5.renderer.style.stroke_enabled and is_stroke_valid:
            p5.renderer.style.tint_enabled = True
            p5.renderer.style.tint_color = p5.renderer.style.stroke_color
            image(text_stroke_image, position)

    return text_string


def text_font(font, size=10):
    """Set current text font.

    :param font:
    :type font: PIL.ImageFont.ImageFont

    """
    global _font_family
    _font_family = font


def text_align(align_x, align_y=None):
    """Set the alignment of drawing text

    :param align_x: "RIGHT", "CENTER" or "LEFT".
    :type align_x: string

    :param align_y: "TOP", "CENTER" or "BOTTOM".
    :type align_y: string

    """

    global _text_align_x, _text_align_y
    _text_align_x = align_x

    if align_y:
        _text_align_y = align_y


def text_leading(leading):
    """Sets the spacing between lines of text in units of pixels

    :param leading: the size in pixels for spacing between lines
    :type align_x: int

    """

    global _text_leading
    _text_leading = leading


def text_size(size):
    """Sets the current font size

    :param leading: the size of the letters in units of pixels
    :type align_x: int

    """

    global _font_family

    # reload the font with new size
    if hasattr(_font_family, "path"):
        if _font_family.path.endswith("ttf") or _font_family.path.endswith("otf"):
            _font_family = ImageFont.truetype(_font_family.path, size)
    else:
        raise ValueError("text_size is not supported for Bitmap Fonts")


def text_width(text):
    """Calculates and returns the width of any character or text string

    :param text_string: text
    :type text_string: str

    :returns: width of any character or text string
    :rtype: int

    """

    return _font_family.getsize(text)[0]


def text_ascent():
    """Returns ascent of the current font at its current size

    :returns: ascent of the current font at its current size
    :rtype: float

    """
    global _font_family
    ascent, descent = _font_family.getmetrics()
    return ascent


def text_descent():
    """Returns descent of the current font at its current size

    :returns:  descent of the current font at its current size
    :rtype: float

    """

    global _font_family
    ascent, descent = _font_family.getmetrics()
    return descent

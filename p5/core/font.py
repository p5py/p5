#
# Part of p5: A Python package based on Processing
# Copyright (C) 2017-2018 Abhik Pal
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
import contextlib
import functools
import textwrap

import PIL
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from .image import image
from .image import PImage
from .structure import push_style

__all__ = ['create_font', 'load_font', 'text', 'text_font',]

_font_family = ImageFont.load_default()

def create_font(name, size=None):
    """Create the given font at the appropriate size.
    
    :param name: Filename of the font file (only pil and ttf fonts are
        supported.)
    :type name: str

    :param size: Font size (only required when `name` refers to a
        truetype font; defaults to None)
    :type size: int | None

    """
    if name.endswith('ttf'):
        _font_family = ImageFont.truetype(name, size)
    elif name.endswith('pil'):
        _font_family = ImageFont.load(name)
    else:
        raise NotImplementedError("Font type not supported.")

    return _font_family

def load_font(font_name):
    """Loads the given font into a font object

    """
    return create_font(font_name)

def text(text_string, position, wrap_at=None):
    """Draw the given text on the screen and save the image.

    :param text_string: text to display
    :type text_string: str

    :param position: position of the text on the screen
    :type position: tuple

    :param wrap_at: specifies the text wrapping column (defaults to
        None)
    :type wrap_at: int

    :returns: actual text that was drawn to the image (when wrapping
        is not set, this is just the unmodified text_string)
    :rtype: str

    """
    global _font_family
    
    if not (wrap_at is None):
        text_string = textwrap.fill(text_string, wrap_at)
        size = _font_family.getsize_multiline(text_string)
    else:
        size = _font_family.getsize(text_string)
        
    canvas = Image.new("RGBA", size, color=(0, 0, 0, 0))
    canvas_draw = ImageDraw.Draw(canvas)
    
    canvas_draw.text((0, 0), text_string, font=_font_family)

    text_image = PImage(*size)
    text_image._img = canvas

    with push_style():
        if p5.renderer.fill_enabled:
            p5.renderer.tint_enabled = True
            p5.renderer.tint_color = p5.renderer.fill_color
        image(text_image, position)
    
    return text_string

def text_font(font):
    """Set current text font.

    :param font:
    :type font: PIL.ImageFont.ImageFont

    """
    global _font_family
    _font_family = font

def text_size(new_size):
    """Set the current size of the font.

    :param size: new size for the rendered font.
    :type size: int

    """
    raise NotImplementedError
    

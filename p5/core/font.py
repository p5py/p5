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
    "text_style",
    "text_wrap",
]


def create_font(name, size=10):
    """Create the given font at the appropriate size.

    :param name: Filename of the font file (only pil, otf and ttf
        fonts are supported.)
    :type name: str

    :param size: Font size (only required when `name` refers to a
        truetype font; defaults to None)
    :type size: int | None

    """
    return p5.renderer.create_font(name, size)


def load_font(font_name):
    """Loads the given font into a font object"""
    return p5.renderer.load_font(font_name)


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
    return p5.renderer.text(text_string, position, wrap_at)


def text_font(font, size=None):
    """Set current text font.

    :param font: PIL.ImageFont.ImageFont for Vispy, Object|String: a font loaded via loadFont(), or a String
    representing a web safe font (a font that is generally available across all systems)

    :type font: PIL.ImageFont.ImageFont or Font Object

    """
    p5.renderer.text_font(font, size)


def text_align(align_x, align_y=None):
    """Set the alignment of drawing text

    :param align_x: "RIGHT", "CENTER" or "LEFT".
    :type align_x: string

    :param align_y: "TOP", "CENTER" or "BOTTOM".
    :type align_y: string

    """
    p5.renderer.style.text_align_x = align_x
    if align_y:
        p5.renderer.style.text_align_y = align_y


def text_leading(leading):
    """Sets the spacing between lines of text in units of pixels

    :param leading: the size in pixels for spacing between lines
    :type align_x: int

    """

    p5.renderer.style.text_leading = leading


def text_size(size):
    """Sets the current font size

    :param leading: the size of the letters in units of pixels
    :type align_x: int

    """

    # reload the font with new size
    p5.renderer.text_size(size)


def text_width(text):
    """Calculates and returns the width of any character or text string

    :param text_string: text
    :type text_string: str

    :returns: width of any character or text string
    :rtype: int

    """

    return p5.renderer.text_width(text)


def text_ascent():
    """Returns ascent of the current font at its current size

    :returns: ascent of the current font at its current size
    :rtype: float

    """
    return p5.renderer.text_ascent()


def text_descent():
    """Returns descent of the current font at its current size

    :returns:  descent of the current font at its current size
    :rtype: float

    """
    return p5.renderer.text_descent()


def text_style(s):
    """
    Sets/Gets the style of the text for system fonts to NORMAL, ITALIC, BOLD or BOLDITALIC
    For non-system fonts (opentype, truetype, etc.) please load styled fonts instead.

    :param s: Style for the font
    :type s: NORMAL | ITALIC | BOLD | BOLDITALIC

    :returns: Current text style
    :rtype: NORMAL | ITALIC | BOLD | BOLDITALIC
    """
    return p5.renderer.text_style(s)


def text_wrap(wrap_style):
    """
    Specifies how lines of text are wrapped within a text box. This requires a wrap_at set on the text area,
    specified in text() as parameter wrap_at. WORD wrap style only breaks lines at spaces. A single string without
    spaces that exceeds the boundaries of the canvas or text area is not truncated, and will overflow the desired area,
    disappearing at the canvas edge. CHAR wrap style breaks lines wherever needed to stay within the text box.
    WORD is the default wrap style, and both styles will still break lines at any line breaks (\n) specified in the
    original text.
    :param wrap_style: One of the wrap style mode 'CHAR' or 'WORD'
    :type wrap_style: str
    """
    p5.renderer.text_wrap(wrap_style)

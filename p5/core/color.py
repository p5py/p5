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

import colorsys
from ..sketch import renderer

__all__ = [ 'Color', 'background', 'color_mode', 'fill', 'no_fill',
            'stroke', 'no_stroke', ]

def to_rgb(h, s, v):
    r, g, b = colorsys.hsv_to_rgb(h/255, s/255, v/255)
    r *= 255
    g *= 255
    b *= 255
    return r, g, b

def to_hsv(r, g, b):
    h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
    h *= 255
    s *= 255
    v *= 255
    return h, s, v

class Color:
    """Represents a color."""
    def __init__(self, *args, color_mode='RGBA', **kwargs):
        r, g, b, a = self.parse_color(*args, color_mode=color_mode, **kwargs)
        self._r = r
        self._g = g
        self._b = b
        self._a = a
        self._normalized_values = (r/255, g/255, b/255, a/255)

    @property
    def normalized(self):
        """Normalized RGB color values"""
        return tuple(self._normalized_values)

    @property
    def rgb(self):
        """
        :returns: Color components in RGB.
        :rtype: tuple
        """
        return (self._r, self._g, self._b)

    @property
    def rgba(self):
        """
        :returns: Color components in RGBA.
        :rtype: tuple
        """
        return (self._r, self._g, self._b, self._a)

    @property
    def hsv(self):
        """
        :returns: Color components in HSV.
        :rtype: tuple
        """
        return to_hsv(self._r, self._g, self._b)

    @property
    def hsva(self):
        """
        :returns: Color components in HSVA.
        :rtype: tuple
        """
        h, s, v = self.hsv
        return (h, s, v, self._a)

    @property
    def hex(self):
        """
        :returns: Color as a hex value
        :rtype: str
        """
        raise NotImplementedError()
    
    @staticmethod
    def parse_color(*args, color_mode='RGB', **kwargs):
        """Parses a color from a range of different input formats.

        This assumes that the args and kwargs are in the following form:

        - gray
        - gray, alpha = ...
        - gray, alpha
        - r, g, b
        - h, s, v
        - r, g, b, a
        - h, s, v, a

        - gray = ...
        - gray = ..., alpha = ...
        - r = ..., g = ..., b = ...,
        - red = ..., green = ..., blue = ...,
        - h = ..., s = ..., v = ...,
        - hue = ..., saturation = ..., value = ...,
        - r = ..., g = ..., b = ..., a = ...
        - red = ..., green = ..., blue = ..., alpha = ...
        - h = ..., s = ..., v = ..., a = ...
        - hue = ..., saturation = ..., value = ..., alpha = ...

        :param args: The positional arguments that define the color.
        :type args: tuple

        :param kwargs: The keyword arguments that define the color.
        :type kwargs: dict

        :returns: The color parsed as r, g, b, a values.
        :rtype: tuple

        """

        if 'alpha' in kwargs:
            alpha = kwargs['alpha']
        elif 'a' in kwargs:
            alpha = kwargs['a']
        else:
            alpha = 255

        if len(args) == 1:
            gray = args[0]
            red, green, blue = gray, gray, gray
        elif len(args) == 2:
            gray, alpha = args
            red, green, blue =  gray, gray, gray
        elif len(args) == 3:
            alpha = 255
            if color_mode.startswith('RGB'):
                red, green, blue = args
            elif color_mode.startswith('HSV'):
                red, green, blue = to_rgb(*args)
            else:
                raise ValueError("Invalid color mode {}".format(color_mode))
        elif len(args) == 4:
            if color_mode.startswith('RGB'):
                red, green, blue, alpha = args
            elif color_mode.startswith('HSV'):
                hue, saturation, value, alpha = args
                red, green, blue = to_rgb(hue, saturation, value)
            else:
                raise ValueError("Invalid color mode {}".format(color_mode))
        elif 'gray' in kwargs:
            red, green, blue = kwargs['gray'], kwargs['gray'], kwargs['gray']
        elif all(param in kwargs for param in ['red', 'green', 'blue']):
            red = kwargs['red']
            green = kwargs['green']
            blue = kwargs['blue']
        elif all(param in kwargs for param in ['r', 'g', 'b']):
            red = kwargs['r']
            green = kwargs['g']
            blue = kwargs['b']
        elif all(param in kwargs for param in ['hue', 'saturation', 'value']):
            h, s, v = kwargs['hue'], kwargs['saturation'], kwargs['value']
            red, green, blue = to_rgb(h, s, v)
        elif all(param in kwargs for param in ['h', 's', 'v']):
            red, green, blue = to_rgb(kwargs['h'], kwargs['s'], kwargs['v'])
        else:
            raise ValueError("Failed to parse color.")
        return red, green, blue, alpha

def fill(*color_args, **color_kwargs):
    """Set the fill color of the shapes.

    :param color_args: positional arguments to be parsed as a color.
    :type color_args: tuple

    :param color_kwargs: keyword arguments to be parsed as a color.
    :type color_kwargs: dict

    :note: Both color_args and color_kwargs are directly sent to
        Color.parse_color

    """
    renderer.fill_enabled = True
    renderer.fill_color = Color(*color_args, **color_kwargs).normalized

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
    """
    renderer.stroke_enabled = True
    renderer.stroke_color = Color(*color_args, **color_kwargs).normalized

def no_stroke():
    """Disable drawing the stroke around shapes."""
    renderer.stroke_enabled = False
    
def background(*color_args, **color_kwargs):
    """Set the background color for the renderer.

    :param color_args: positional arguments to be parsed as a color.
    :type color_args: tuple

    :param color_kwargs: keyword arguments to be parsed as a color.
    :type color_kwargs: dict

    :note: Both color_args and color_kwargs are directly sent to
        Color.parse_color
    """
    renderer.background_color = Color(*color_args, **color_kwargs).normalized
    renderer.clear()

def color_mode(mode):
    """Set the color mode of the renderer.
    
    :param mode: One of {'RGB', 'HSB'} corresponding to Red/Green/Blue
        or Hue/Saturation/Brightness
    :type mode: str

    """
    raise NotImplementedError()

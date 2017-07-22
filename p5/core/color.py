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

from ..pmath import lerp
from ..sketch import renderer

__all__ = [ 'Color', 'background', 'color_mode', 'fill', 'no_fill',
            'stroke', 'no_stroke', ]

_color_mode = 'RGB'

def to_rgb(h, s, b):
    red, green, blue = colorsys.hsv_to_rgb(h/255, s/255, b/255)
    red *= 255
    green *= 255
    blue *= 255
    return red, green, blue

def to_hsb(r, g, b):
    hue, saturation, brightness = colorsys.rgb_to_hsv(r/255, g/255, b/255)
    hue *= 255
    saturation *= 255
    brightness *= 255
    return hue, saturation, brightness

class Color:
    """Represents a color."""
    def __init__(self, *args, color_mode=None, **kwargs):
        if color_mode is None:
            color_mode = _color_mode

        if (len(args) == 1) and isinstance(args[0], Color):
            r, g, b, a = args[0].rgba
        else:
            r, g, b, a = self.parse_color(*args, color_mode=color_mode, **kwargs)
        self._red = r
        self._green = g
        self._blue = b
        self._alpha = a
        self._normalized = (r/255, g/255, b/255, a/255)

        self._recompute_hsb()

    def _recompute_norm(self):
        """Recompute the normalized color from RGB values"""
        self._normalized = (self._red / 255, self._green / 255,
                            self._blue / 255, self._alpha / 255)

    def _recompute_rgb(self):
        """Recompute the RGB values from HSB values."""
        r, g, b = to_rgb(self._hue, self._saturation, self._brightness)
        self._red = r
        self._greeen = g
        self._blue = b
        self._recompute_norm()

    def _recompute_hsb(self):
        """Recompute the HSB values from the RGB values."""
        h, s, b = to_hsb(self._red, self._green, self._blue)
        self._hue = h
        self._saturation = s
        self._brightness = b
        self._recompute_norm()

    def lerp(self, target, amount):
        """Linearly interpolate one color to another by the given amount.

        :param target: The target color to lerp to.
        :type target: Color

        :param amount: The amount by which the color should be lerped
            (should be a float between 0 and 1).
        :type amount: float

        :returns: A new color lerped between the current color and the
            other color.
        :rtype: Color

        """
        lerped = (lerp(s, t, amount) for s, t in zip(self.rgba, target.rgba))
        return Color(*lerped, color_mode='RGB')

    @property
    def normalized(self):
        """Normalized RGBA color values"""
        return tuple(self._normalized)

    @property
    def gray(self):
        """The gray-scale value of the color.

        Performs a luminance preservation of the current color to
        grayscale.

        """

        # FORMULA:
        # https://en.wikipedia.org/wiki/Grayscale#Colorimetric_.28luminance-preserving.29_conversion_to_grayscale
        # REFERENCE: https://www.w3.org/Graphics/Color/sRGB
        linear_rgb = []
        for c in self._normalized[:3]:
            if c <= 0.0405:
                lvalue =  c / 12.92
            else:
                lvalue = ((c + 0.055) / 1.055) ** 2.4
            linear_rgb.append(lvalue)

        coeffs = (0.2126, 0.7152, 0.0722)
        return 255 * sum(l*c for l, c in zip(coeffs, linear_rgb))

    @gray.setter
    def gray(self, value):
        self._red = value
        self._green = value
        self._blue = value
        self._recompute_hsb()

    @property
    def alpha(self):
        """The alpha value for the color."""
        return self._alpha

    @alpha.setter
    def alpha(self, value):
        self._alpha = value
        self._recompute_norm()

    @property
    def rgb(self):
        """
        :returns: Color components in RGB.
        :rtype: tuple
        """
        return (self._red, self._green, self._blue)

    @property
    def rgba(self):
        """
        :returns: Color components in RGBA.
        :rtype: tuple
        """
        return (self._red, self._green, self._blue, self._alpha)

    @property
    def red(self):
        """The red component of the color"""
        return self._red

    @red.setter
    def red(self, value):
        self._red = value
        self._recompute_hsb()

    @property
    def green(self):
        """The green component of the color"""
        return self._green

    @green.setter
    def green(self, value):
        self._green = value
        self._recompute_hsb()

    @property
    def blue(self):
        """The blue component of the color"""
        return self._blue

    @blue.setter
    def blue(self, value):
        self._blue = value
        self._recompute_hsb()

    @property
    def hsb(self):
        """
        :returns: Color components in HSB.
        :rtype: tuple
        """
        return (self._hue, self._saturation, self._brightness)

    @property
    def hsba(self):
        """
        :returns: Color components in HSBA.
        :rtype: tuple
        """
        return (self._hue, self._saturation, self._brightness, self._alpha)

    @property
    def hue(self):
        """The hue component of the color"""
        return self._hue

    @hue.setter
    def hue(self, value):
        self._hue = value
        self._recompute_rgb()

    @property
    def saturation(self):
        """The saturation component of the color"""
        return self._saturation

    @saturation.setter
    def saturation(self, value):
        self._saturation = value
        self._recompute_rgb()

    @property
    def brightness(self):
        """The brightness component of the color"""
        return self._brightness

    @brightness.setter
    def brightness(self, value):
        self._brightness = value
        self._recompute_rgb()

    # ...and some convenient aliases
    r = red
    g = green
    h = hue
    s = saturation
    value = brightness
    v = value

    # `b` is tricky. depending on the current color code, this could
    # either be the brightness value or the blue value.
    @property
    def b(self):
        """The blue or the brightness value (depending on the color mode)."""
        if _color_mode == 'RGB':
            return self.blue
        elif _color_mode == 'HSB':
            return self.brightness
        else:
            raise ValueError("Unknown color mode {}".format(_color_mode))

    @b.setter
    def b(self, value):
        if _color_mode == 'RGB':
            self.blue = value
        elif _color_mode == 'HSB':
            self.brightness = value
        else:
            raise ValueError("Unknown color mode {}".format(_color_mode))

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
        - h = ..., s = ..., b = ...,
        - hue = ..., saturation = ..., brightness = ...,
        - r = ..., g = ..., b = ..., a = ...
        - red = ..., green = ..., blue = ..., alpha = ...
        - h = ..., s = ..., b = ..., a = ...
        - hue = ..., saturation = ..., brightness = ..., alpha = ...

        :param args: The positional arguments that define the color.
        :type args: tuple

        :param kwargs: The keyword arguments that define the color.
        :type kwargs: dict

        :returns: The color parsed as red, green, blue, alpha values.
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
        elif (len(args) == 3) and color_mode.startswith('RGB'):
            red, green, blue = args
        elif (len(args) == 3) and color_mode.startswith('HSB'):
            hue, saturation, brightness = args
            red, green, blue = to_rgb(hue, saturation, brightness)
        elif (len(args) == 4) and color_mode.startswith('RGB'):
            red, green, blue, alpha = args
        elif (len(args) == 4) and color_mode.startswith('HSB'):
            hue, saturation, value, alpha = args
            red, green, blue = to_rgb(hue, saturation, value)
        elif 'gray' in kwargs:
            gray = kwargs['gray']
            red, green, blue = gray, gray, gray
        elif all(param in kwargs for param in ['red', 'green', 'blue']):
            red = kwargs['red']
            green = kwargs['green']
            blue = kwargs['blue']
        elif all(param in kwargs for param in ['r', 'g', 'b']):
            red = kwargs['r']
            green = kwargs['g']
            blue = kwargs['b']
        elif all(param in kwargs for param in ['hue', 'saturation', 'brightness']):
            hue = kwargs['hue']
            saturation = kwargs['saturation']
            brightness = kwargs['brightness']
            red, green, blue = to_rgb(hue, saturation, brightness)
        elif all(param in kwargs for param in ['h', 's', 'b']):
            hue = kwargs['h']
            saturation = kwargs['s']
            brightness = kwargs['b']
            red, green, blue = to_rgb(hue, saturation, brightness)
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
    global _color_mode
    _color_mode = mode

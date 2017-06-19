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

from ..opengl import renderer

__all__ = [ 'Color', 'background', 'color_mode', 'fill', 'no_fill',
            'stroke', 'no_stroke', ]

class Color:
    """Represents a color."""

    def __init__(self, r, g, b, a=1.0, color_mode='RGBA'):
        self._normalized_values = (r, g, b, a)

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
        raise NotImplementedError()

    @property
    def hsv(self):
        """
        :returns: Color components in HSV.
        :rtype: tuple
        """
        raise NotImplementedError()    

    @property
    def hex(self):
        """
        :returns: Color as a hex value
        :rtype: str
        """
        raise NotImplementedError()
    
    @staticmethod
    def parse_color(*args, **kwargs):
        """Parses a color from a range of different input formats.

        :returns: A color based on the parsed arguments.
        :rtype: Color
        """
        raise NotImplementedError()

def fill(*color_args):
    """Set the fill color of the shapes."""
    renderer._attributes['fill_enabled'] = True
    renderer._attributes['fill_color'] = Color(*color_args).normalized

def no_fill():
    """Disable filling geometry."""
    renderer._attributes['fill_enabled'] = False

def stroke(*color_args):
    """Set the color used to draw lines around shapes"""
    renderer._attributes['stroke_enabled'] = True
    renderer._attributes['stroke_color'] = Color(*color_args).normalized

def no_stroke():
    """Disable drawing the stroke around shapes."""
    renderer._attributes['stroke_enabled'] = False
    
def background(*color_args):
    """Set the background color for the renderer._attributes[']"""
    renderer._attributes['background_color'] = Color(*color_args).normalized
    renderer.clear()

def color_mode(mode):
    """Set the color mode of the renderer._attributes[']
    
    :param mode: One of {'RGB', 'HSB'} corresponding to Red/Green/Blue
        or Hue/Saturation/Brightness
    :type mode: str

    """
    raise NotImplementedError

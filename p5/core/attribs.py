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

__all__ = ['color_mode']

color_parse_mode = 'RGB'
color_range = (255, 255, 255, 255)

def color_mode(mode):
    """Set the color mode of the renderer.

    :param mode: One of {'RGB', 'HSB'} corresponding to Red/Green/Blue
        or Hue/Saturation/Brightness
    :type mode: str

    """
    global color_parse_mode
    color_parse_mode = mode

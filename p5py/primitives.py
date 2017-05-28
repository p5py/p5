#
# Part of p5py: A Python package based on Processing
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

from . import _p5

# we will pass around these shape objects internally to draw and
# render stuff. A Shape will contain attributes for changing its shape
# type -- POLY, LINE, etc -- and its shape attributes -- color,
# stroke, etc --.
class Shape:
    def __init__(self):
        raise NotImplementedError


@_p5.artist
def point(*args):
    """Returns a point Shape"""
    raise NotImplementedError

@_p5.artist
def line(*args):
    """Returns a line Shape"""

@_p5.artist
def rect(*args):
    """Returns a rect object."""
    raise NotImplementedError

# etc...

@_p5.attribute
def fill(*args):
    """Returns a new fill color for the sketch."""
    raise NotImplementedError

# etc...

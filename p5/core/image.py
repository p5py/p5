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

import pyglet
from ..sketch import renderer

__all__ = ['Image']

class Image:
    def __init__(self, file_name):
        self._file_name = file_name
        self._has_loaded = False
        self._load()

    @property
    def width(self):
        if not self._has_loaded:
            self._load()
        return self._width

    @property
    def height(self):
        if not self._has_loaded:
            self._load()
        return self._height

    @property
    def pixels(self):
        raise NotImplementedError()

    def _load(self):
        self._load_local()

    def _load_local(self):
        image = pyglet.image.load(self._file_name)
        width = image.width
        height = image.height
        self._raw_data = image.get_data('RGB', - width * 3)
        self._width = width
        self._height = height
        self._has_loaded = True

    def display(self, location, *args, mode=None):
        raise NotImplementedError()

    def resize(self, width, height):
        raise NotImplementedError()

    def blend(self):
        raise NotImplementedError()

    def filter(self, kind, param=None):
        raise NotImplementedError()

    def mask(self, mask_array):
        raise NotImplementedError()

    def load_pixels(self):
        raise NotImplementedError()

    def save(self, filename):
        raise NotImplementedError()

    def __getitem__(self, key):
        raise NotImplementedError()

    def __setitem__(self, key, value):
        raise NotImplementedError()

    def __hash__(self):
        return hash(self._file_name)

    def __bytes__(self):
        if not self._has_loaded:
            self._load()
        return self._raw_data

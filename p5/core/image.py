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
import functools

from PIL import Image
import numpy as np
from vispy.gloo import Texture2D



from .. import sketch

__all__ = ['image', 'load_image']

def _check_reload(func):
    """Reloads the image if required before calling the function.

    """
    @functools.wraps(func)
    def rfunc(instance, *args, **kwargs):
        if instance._img_data is None or instance._reload:
            instance._load()
        return func(instance, *args, **kwargs)
    return rfunc

class PImage:
    """Image class for p5.

    :param width: width of the image.
    :type width: int

    :param height: height of the image.
    :type height:

    :param fmt: color format to use for the image. Should be one of
    {'RGB', 'RGBA', 'ALPHA'}

    """
    def __init__(self, width, height, fmt='RGBA'):
        self._width = width
        self._height = height

        format_map = {
            'rgb': 'RGB',
            'rgba': 'RGBA',
            'alpha': "L"
        }

        self._reload = False
        self._img = None
        self._img_format = format_map[fmt.upper()]
        self._img_texture = None
        self._img_data = None

    @property
    @_check_reload
    def width(self):
        return self._width

    @width.setter
    def width(self, new_width):
        self.size = (new_width, self._height)

    @property
    @_check_reload
    def height(self):
        return self._height

    @height.setter
    def height(self, new_height):
        self.size = (self._width, new_height)

    @property
    @_check_reload
    def size(self):
        return self._size

    @size.setter
    def size(self, new_size):
        self._resize(new_size)

    @property
    @_check_reload
    def aspect_ratio(self):
        return self._width / self._height

    @property
    @_check_reload
    def _texture(self):
        if self._img_texture is None:
            self._img_texture = Texture2D(self._data)
        return self._img_texture

    @property
    @_check_reload
    def _data(self):
        return self._img_data

    def _load(self):
        if self._img is None:
            self._img = Image.new(self._img_format, (self._width, self._height))

        width, height = self._img.size
        self._width = width
        self._height = height
        self._size = (widt, height)

        data = np.array(self._img.getdata(), dtype=np.float32)
        _, self._channels = data.shape
        self._img_data = data.reshape(width, height, self._channels) / 255.0

    def load_pixels(self):
        raise NotImplementedError

    def mask(self, image):
        raise NotImplementedError

    def filter(self, kind, param=None):
        """Filter the image.

        :param kind: The kind of filter to use on the image. Should be
            one of { 'threshold', 'gray', 'opaque', 'invert',
            'posterize', 'blur', 'erode', 'dilate', }

        :type kind: str

        :param param: optional parameter for the filter in use
            (defaults to None). Only required for 'threshold' (the
            threshold to use, param should be a value between 0 and 1;
            defaults to 0.5), 'posterize' (limiting value for each
            channel should be between 2 and 255), and 'blur' (gaussian
            blur radius, defaults to 1.0).

        :type param: int | float | None

        """
        filter_name = kind.lower()
        if param is None:
            default_values = {
                'threshold': 0.5,
                'blur': 1.0,
            }
            param = default_values.get(filter_name, None)

        raise NotImplementedError

    def copy(self, *args):
        raise NotImplementedError

    def blend(self, *args):
        raise NotImplementedError

    def save(self, file_name):
        """Save the image into a file

        """
        raise NotImplementedError


def image(img, loc, size=None):
    """Display the given image.

    :param img: the image to be displayed.
    :type img: p5.Image

    :param loc: location of the image on the screen.
    :type loc: tuple | list | np.ndarray | p5.Vector | p5.Point

    :param size: target size of the image. Defaults to the image size.
    :type size: tuple | list

    """
    if size is None:
        size = img.size
    sketch.render_image(img, loc, size)

def image_mode(mode):
    """Modifies the locaton from which the images are drawn.

    :param mode: should be one of {'corner', 'center', 'corners'}
    :type mode: str

    """
    raise NotImplementedError

def load_image(filename):
    """Load an image from the given filename.

    :param filename: Filename of the given image. The file-extennsion
        is automatically inferred
    :type filename: str

    """
    img = Image.open(filename)
    w, h = img.size
    pimg = PImage(w, h)
    pimg._img = img
    return pimg

    







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
import contextlib

import numpy as np
import PIL
from PIL import Image
from PIL import ImageFilter
from PIL import ImageChops
from PIL import ImageOps
from vispy import gloo

from . import color
from .. import sketch
from ..pmath import constrain
from ..pmath.utils import _is_numeric

__all__ = ['image', 'load_image', 'image_mode']

_image_mode = 'corner'

def _ensure_loaded(func):
    """Reloads the image if required before calling the function.

    """
    @functools.wraps(func)
    def rfunc(instance, *args, **kwargs):
        if instance._img_data is None or instance._reload:
            instance._load()
        return func(instance, *args, **kwargs)
    return rfunc

@contextlib.contextmanager
def _restore_color_mode():
    old_mode = color.color_parse_mode
    old_range = color.color_range
    color.color_mode('RGB', 255, 255, 255, 255)

    yield

    color.color_mode(old_mode, *old_range)

class PImage:
    """Image class for p5.

    :param width: width of the image.
    :type width: int

    :param height: height of the image.
    :type height:

    :param fmt: color format to use for the image. Should be one of
        {'RGB', 'RGBA', 'ALPHA'}. Defaults to 'RGBA'

    :type fmt: str

    """
    def __init__(self, width, height, fmt='RGBA'):
        self._width = width
        self._height = height

        format_map = {
            'rgb': 'RGB',
            'rgba': 'RGBA',
            'alpha': 'L',
        }

        self._reload = False
        self._img = None
        self._img_format = format_map[fmt.lower()]
        self._img_texture = None
        self._img_data = None

    @property
    @_ensure_loaded
    def width(self):
        return self._width

    @width.setter
    def width(self, new_width):
        self.size = (new_width, self._height)

    @property
    @_ensure_loaded
    def height(self):
        return self._height

    @height.setter
    def height(self, new_height):
        self.size = (self._width, new_height)

    @property
    @_ensure_loaded
    def size(self):
        return self._size

    @size.setter
    def size(self, new_size):
        self._img = self._img.resize(new_size)
        self._reload = True

    @property
    @_ensure_loaded
    def aspect_ratio(self):
        return self._width / self._height

    @property
    @_ensure_loaded
    def _texture(self):
        if self._img_texture is None:
            texdata = self._data.astype(np.float32) / 255.0
            self._img_texture = gloo.Texture2D(texdata)
        return self._img_texture

    @property
    @_ensure_loaded
    def _data(self):
        return self._img_data

    def _load(self):
        if self._img is None:
            self._img = Image.new(self._img_format, (self._width, self._height))

        width, height = self._img.size
        self._width = width
        self._height = height
        self._size = (width, height)

        data = np.array(self._img.getdata(), dtype=np.uint8)

        if len(data.shape) == 1:
            self._channels = 1
        else:
            _, self._channels = data.shape

        self._img_data = data.reshape(height, width, self._channels)
        self._reload = False

    @_ensure_loaded
    def _get_pixel(self, key):
        """Return the pixel color at the given positions.

        :param key: An (x, y) tuple specifying the pixel location.
        :type key: tuple

        :retuns: the Color of the given pixel in the image.
        :rtype: p5.Color

        :raises KeyError: When the pixel location is invalid.

        """
        px = int(key[0])
        py = int(key[1])

        if px >= self.width or py >= self.height:
            raise KeyError("Invalid pixel coordinates {}.".format(key))

        with _restore_color_mode():
            col = color.Color(*self._img.getpixel((px, py)))

        return col

    @_ensure_loaded
    def _get_patch(self, key):
        """Return the patch (a sub-image) specified by the given key.

        :param key: a tuple index-ing into a valid 2D array.
        :type key: tuple

        :returns: the patch specified by the given key
        :rtype: p5.PImage

        """
        xidx, yidx = key
        if self._channels == 1:
            patch_data = self._img_data[xidx, yidx]
        else:
            patch_data = self._img_data[xidx, yidx, :]

        patch_width = patch_data.shape[0]
        patch_height = patch_data.shape[1]

        patch_img = Image.fromarray(patch_data, self._img.mode)

        patch = PImage(patch_width, patch_height)
        patch._img_format = self._img_format
        patch._img = patch_img
        return patch

    @_ensure_loaded
    def __getitem__(self, key):
        """Return the color of the indexed pixel or the requested sub-region

        Note :: when the specified `key` denotes a single pixel, the
            color of that pixel is returned. Else, a new PImage
            (constructed using the slice specified by `key`). Note
            that this causes the internal buffer data to be reloaded
            (when the image is in an "unclean" state) and hence, many
            such operations can potentially slow things down.

        :returns: a sub-image or a the pixel color
        :rtype: p5.Color | p5.PImage

        :raises KeyError: When `key` is invalid.

        """
        if len(key) != 2:
            raise KeyError("Invalid image index")

        if _is_numeric(key[0]) and _is_numeric(key[1]):
            return self._get_pixel(key)

        return self._get_patch(key)

    def _set_pixel(self, key, point):
        # since both posx and posy are numeric, we are only pasting in
        # a "single" color. Hence, whenever patch is a PImage, we
        # require it to be exactly one pixel by one pixel large

        if isinstance(point, PImage):
            if point.size != (1, 1):
                raise AttributeError("Incompatible image dimensions")
            # ...and extract the color of that pixel
            point_color = point[0, 0]

        # if the patch is a color, we don't do much
        elif isinstance(point, color.Color):
            point_color = point

        # otherwise, we try to parse the given patch as a color (if
        # `value` is invalid, the parsing will fail).
        else:
            # the try-catch just takes care of the situation when
            # patch is just a single (non-iterable) value. Then we
            # don't unpack it.
            try:
                point_color = color.Color(*point)
            except TypeError as te:
                point_color = color.Color(point)

        # finally, write the color value to the image based on the
        # number of channels.
        with _restore_color_mode():
            red = int(point_color.red)
            green = int(point_color.green)
            blue = int(point_color.blue)
            alpha = int(point_color.alpha)

            if self._channels == 1:
                pixel_value = int(point_color.gray)
            elif self._channels == 3:
                pixel_value = (red, green, blue)
            elif self._channels == 4:
                pixel_value = (red, green, blue, alpha)
            else:
                raise ValueError("Image has unexpected number of channels")

        pixel_position = int(key[0]), int(key[1])
        self._img.putpixel(pixel_position, pixel_value)

    @_ensure_loaded
    def _set_patch(self, key, patch):
        """Paste the given patch in the image.

        """
        # we first ensure that both the source patch and the target
        # image (self) have the same color modes, if not, convert the
        # target.
        target_mode = self._img.mode
        source_mode = patch._img.mode

        if target_mode != source_mode:
            patch._img.convert(target_mode)

        self._img_data[key] = patch._data[key]
        self._img = Image.fromarray(self._img_data, self._img.mode)

    def __setitem__(self, key, patch):
        """Paste the given `patch` into the current image.
        """
        if len(key) != 2:
            raise KeyError("Invalid image index")
        if _is_numeric(key[0]) and _is_numeric(key[1]):
            self._set_pixel(key, patch)
        else:
            self._set_patch(key, patch)
        self._reload = True

    def load_pixels(self):
        self._load()

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
                'gaussian_blur': 1.0,
                'box_blur': 1.0,
                'posterize': 1,
            }
            param = default_values.get(filter_name, None)

        if filter_name in ['blur', 'gaussian_blur']:
            fim = self._img.filter(ImageFilter.GaussianBlur(radius=param))
            self._img = fim
        elif filter_name == 'box_blur':
            self._img = self._img.filter(ImageFilter.BoxBlur(param))
        elif filter_name in ['gray', 'grey', 'grayscale']:
            self._img = ImageOps.grayscale(self._img)
        elif filter_name == 'opaque':
            self._img.putalpha(255)
        elif filter_name == 'invert':
            self._img = ImageOps.invert(self._img)
        elif filter_name == 'posterize':
            nbits = 0
            while int(param) != 0:
                param = param >> 1
                nbits = nbits + 1
            nbits = constrain(nbits, 1, 8)
            self._img = ImageOps.posterize(self._img, nbits)
        elif filter_name == 'threshold':
            dat = np.asarray(ImageOps.grayscale(self._img)).copy()
            dat[dat < int(128 * param)] = 0
            dat[dat >= int(128 * param)] = 255
            self._img = Image.fromarray(dat)
        elif filter_name in ['erode', 'dilate']:
            raise NotImplementedError
        else:
            raise ValueError("Unknown filter")

        self._reload = True

    def copy(self, *args):
        raise NotImplementedError

    def blend(self, *args):
        raise NotImplementedError

    def save(self, file_name):
        """Save the image into a file

        """
        raise NotImplementedError


def image(img, location, size=None):
    """Display the given image.

    :param img: the image to be displayed.
    :type img: p5.Image

    :param location: location of the image on the screen (depending on the
        current image mode, 'corner', 'center', 'corners', this could
        represent the coordinate of the top-left corner, center,
        top-left corner respectively.)
    :type location: tuple | list | np.ndarray | p5.Vector

    :param size: target size of the image or the bottom-right image
        corner when the image mode is set to 'corners'. By default,
        the value is set according to the current image size.

    :type size: tuple | list

    """
    if size is None:
        size = img.size

    lx, ly = location
    sx, sy = size

    if _image_mode == 'center':
        lx = int(lx - (sx / 2))
        ly = int(ly - (sy / 2))

    if _image_mode == 'corners':
        sx = sx - lx
        sy = sy - ly

    sketch.render_image(img, (lx, ly), (sx, sy))

def image_mode(mode):
    """Modifies the locaton from which the images are drawn.

    :param mode: should be one of {'corner', 'center', 'corners'}
    :type mode: str

    """
    global _image_mode

    if mode.lower() not in ['corner', 'center', 'corners']:
        raise ValueError("Unknown image mode!")
    _image_mode = mode.lower()

def load_image(filename):
    """Load an image from the given filename.

    :param filename: Filename of the given image. The file-extennsion
        is automatically inferred.
    :type filename: str

    """
    # TODO: Add URL support.
    img = Image.open(filename)
    w, h = img.size
    pimg = PImage(w, h)
    pimg._img = img
    return pimg

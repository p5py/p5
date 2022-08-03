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
import contextlib
import functools

import builtins

import io
import re
import urllib

import numpy as np
from PIL import Image
from PIL import ImageFilter
from PIL import ImageChops
from PIL import ImageOps
from . import p5

from . import color
from ..pmath import constrain
from ..pmath.utils import _is_numeric
from .structure import push_style

__all__ = ["PImage", "image", "load_image", "image_mode", "load_pixels"]

_image_mode = "corner"


def _ensure_loaded(func):
    """Reloads the image if required before calling the function."""

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
    color.color_mode("RGB", 255, 255, 255, 255)

    yield

    color.color_mode(old_mode, *old_range)


class PImage:
    """Image class for p5.

    Note that the image "behaves" like a 2-D list and hence, doesn't
    expose special methods for copying / pasting / cropping. All of
    these operations can be done by using appropriate indexing into
    the array. See the :meth:`p5.PImage.__getitem__` and
    :meth:`p5.PImage.__setitem__` methods for details.

    :param width: width of the image.
    :type width: int

    :param height: height of the image.
    :type height:

    :param fmt: color format to use for the image. Should be one of
        {'RGB', 'RGBA', 'ALPHA'}. Defaults to 'RGBA'

    :type fmt: str

    """

    def __init__(self, width, height, fmt="RGBA"):
        self._width = width
        self._height = height

        format_map = {
            "rgb": "RGB",
            "rgba": "RGBA",
            "alpha": "L",
        }

        self._reload = False
        self._img = None
        self._img_format = format_map[fmt.lower()]
        self._img_texture = None
        self._img_data = None

    @property
    @_ensure_loaded
    def width(self):
        """The width of the image

        :rtype: int
        """
        return self._width

    @width.setter
    def width(self, new_width):
        self.size = (new_width, self._height)

    @property
    @_ensure_loaded
    def height(self):
        """The height of the image

        :rtype: int
        """
        return self._height

    @height.setter
    def height(self, new_height):
        self.size = (self._width, new_height)

    @property
    @_ensure_loaded
    def size(self):
        """The size of the image

        :rtype: (int, int) tuple
        """
        return self._size

    @size.setter
    def size(self, new_size):
        self._img = self._img.resize(new_size)
        self._reload = True

    @property
    @_ensure_loaded
    def aspect_ratio(self):
        """Return the aspect ratio of the image.

        :rtype: float | int
        """
        return self._width / self._height

    @property
    @_ensure_loaded
    def _texture(self):
        if self._img_texture is None:
            texdata = self._data.astype(np.float32) / 255.0
            if builtins.current_renderer == "vispy":
                from vispy.gloo import Texture2D

                self._img_texture = Texture2D(texdata, interpolation="linear")
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

        self._channels = len(self._img.getbands())

        self._img_data = data.reshape((height, width, self._channels))
        self._img_texture = None
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
            patch_data = self._img_data[yidx, xidx]
        else:
            patch_data = self._img_data[yidx, xidx, :]

        patch_width = patch_data.shape[1]
        patch_height = patch_data.shape[0]

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
            except TypeError:
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
        """Paste the given patch in the image."""
        # we first ensure that both the source patch and the target
        # image (self) have the same color modes, if not, convert the
        # target.
        target_mode = self._img.mode
        source_mode = patch._img.mode

        kx, ky = key

        if target_mode != source_mode:
            patch._img.convert(target_mode)

        if self._channels == 1:
            self._img_data[ky, kx] = patch._data[:, :]
        else:
            self._img_data[ky, kx, :] = patch._data[:, :, :]

        self._img = Image.fromarray(self._img_data, self._img.mode)

    def __setitem__(self, key, patch):
        """Paste the given `patch` into the current image."""
        if len(key) != 2:
            raise KeyError("Invalid image index")
        if _is_numeric(key[0]) and _is_numeric(key[1]):
            self._set_pixel(key, patch)
        else:
            self._set_patch(key, patch)
        self._reload = True

    def load_pixels(self):
        """Load internal pixel data for the image.

        By default image data is only loaded lazily, i.e., right
        before displaying an image on the screen. Use this method to
        manually load the internal image data.

        """
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
                "threshold": 0.5,
                "blur": 1.0,
                "gaussian_blur": 1.0,
                "box_blur": 1.0,
                "posterize": 1,
                "opacity": 0.5,
            }
            param = default_values.get(filter_name, None)

        if filter_name in ["blur", "gaussian_blur"]:
            fim = self._img.filter(ImageFilter.GaussianBlur(radius=param))
            self._img = fim
        elif filter_name == "box_blur":
            self._img = self._img.filter(ImageFilter.BoxBlur(param))
        elif filter_name in ["gray", "grey", "grayscale"]:
            self._img = ImageOps.grayscale(self._img)
        elif filter_name == "opaque":
            self._img.putalpha(255)
        elif filter_name == "opacity":
            self._img.putalpha(int(param * 255))
        elif filter_name == "invert":
            self._img = ImageOps.invert(self._img)
        elif filter_name == "posterize":
            nbits = 0
            while int(param) != 0:
                param = param >> 1
                nbits = nbits + 1
            nbits = constrain(nbits, 1, 8)
            self._img = ImageOps.posterize(self._img, nbits)
        elif filter_name == "threshold":
            dat = np.asarray(ImageOps.grayscale(self._img)).copy()
            dat[dat < int(128 * param)] = 0
            dat[dat >= int(128 * param)] = 255
            self._img = Image.fromarray(dat)
        elif filter_name in ["erode", "dilate"]:
            raise NotImplementedError
        else:
            raise ValueError("Unknown filter")

        self._reload = True

    def blend(self, other, mode):
        """Blend the specified image using the given blend mode.

        :param other: The image to be blended to the current image.
        :type other: p5.PImage

        :param mode: Blending mode to use. Should be one of { 'BLEND',
            'ADD', 'SUBTRACT', 'LIGHTEST', 'DARKEST', 'MULTIPLY',
            'SCREEN',}
        :type mode: str

        :raises AssertionError: When the dimensions of img do not
            match the dimensions of the current image.

        :raises KeyError: When the blend mode is invalid.

        """
        mode = mode.lower()
        assert self.size == other.size, "Images are of different sizes!"

        if self._img.mode != "RGBA":
            self._img = self._img.convert("RGBA")
            self._reload = True

        if other._img.mode != "RGBA":
            other_img = other._img.convert("RGBA")
        else:
            other_img = other._img

        # todo: implement missing filters -- abhikpal (2018-08-14)
        if mode == "blend":
            self._img = ImageChops.composite(self._img, other_img, self._img)
        elif mode == "add":
            self._img = ImageChops.add(self._img, other_img)
        elif mode == "subtract":
            self._img = ImageChops.subtract(self._img, other_img)
        elif mode == "lightest":
            self._img = ImageChops.lighter(self._img, other_img)
        elif mode == "darkest":
            self._img = ImageChops.darker(self._img, other_img)
        elif mode == "difference":
            raise NotImplementedError
        elif mode == "exclusion":
            raise NotImplementedError
        elif mode == "multiply":
            self._img = ImageChops.multiply(self._img, other_img)
        elif mode == "screen":
            self._img = ImageChops.screen(self._img, other_img)
        elif mode == "overlay":
            raise NotImplementedError
        elif mode == "hard_light":
            raise NotImplementedError
        elif mode == "soft_light":
            raise NotImplementedError
        elif mode == "dodge":
            raise NotImplementedError
        elif mode == "burn":
            raise NotImplementedError
        else:
            raise KeyError("'{}' blend mode not found".format(mode.upper()))

        self._reload = True
        return self

    @_ensure_loaded
    def save(self, file_name):
        """Save the image into a file

        :param file_name: Filename to save the image as.
        :type file_name: str

        """
        self._img.save(file_name)


def image(*args, size=None):
    """Draw an image to the display window.

    Images must be in the same folder as the sketch (or the image path
    should be explicitly mentioned). The color of an image may be
    modified with the :meth:`p5.tint` function.

    :param x: x-coordinate of the image by default
    :type float:

    :param y: y-coordinate of the image by default
    :type float:

    :param w: width to display the image by default
    :type float:

    :param h: height to display the image by default
    :type float:

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
    if len(args) == 2:
        img, location = args
    elif len(args) == 3:
        img, location = args[0], args[1:]
    elif len(args) == 5:
        img, location, size = args[0], args[1:3], args[3:]
    else:
        raise ValueError("Unexpected number of arguments passed to image()")

    if size is None:
        size = img.size
    # Add else statement below to resize the img._img first,
    #   or it will take much time to render large image,
    #   even when small size is specified to the image
    else:
        if size != img.size:
            img.size = size

    lx, ly = location
    sx, sy = size

    if _image_mode == "center":
        lx = int(lx - (sx / 2))
        ly = int(ly - (sy / 2))

    if _image_mode == "corners":
        sx = sx - lx
        sy = sy - ly

    p5.renderer.render_image(img, (lx, ly), (sx, sy))


def image_mode(mode):
    """Modify the locaton from which the images are drawn.

    Modifies the location from which images are drawn by changing the
    way in which parameters given to :meth:`p5.image` are intepreted.

    The default mode is ``image_mode('corner')``, which interprets the
    second parameter of ``image()`` as the upper-left corner of the
    image. If an additional parameter is specified, it is used to set
    the image's width and height.

    ``image_mode('corners')`` interprets the first parameter of
    ``image()`` as the location of one corner, and the second
    parameter as the opposite corner.

    ``image_mode('center')`` interprets the first parameter of
    ``image()`` as the image's center point. If an additional
    parameter is specified, it is used to set the width and height of
    the image.

    :param mode: should be one of ``{'corner', 'center', 'corners'}``
    :type mode: str

    :raises ValueError: When the given image mode is not understood.
        Check for typoes.

    """
    global _image_mode

    if mode.lower() not in ["corner", "center", "corners"]:
        raise ValueError("Unknown image mode!")
    _image_mode = mode.lower()


def load_image(filename):
    """Load an image from the given filename (or URL).

    Loads an image into a variable of type PImage. Four types of
    images may be loaded.

    In most cases, load all images in setup() or outside the draw()
    call to preload them at the start of the program. Loading images
    inside draw() will reduce the speed of a program.

    :param filename: Filename (or path or URL) of the given image. The
        file-extennsion is automatically inferred.
    :type filename: str

    :returns: An :class:`p5.PImage` instance with the given image data
    :rtype: :class:`p5.PImage`

    """
    if re.match(r"\w+://", filename):
        with urllib.request.urlopen(filename) as url:
            f = io.BytesIO(url.read())
            img = Image.open(f)
    else:
        img = Image.open(filename)
    w, h = img.size
    pimg = PImage(w, h)
    pimg._img = img

    return pimg


@contextlib.contextmanager
def load_pixels():
    """Load a snapshot of the display window into the ``pixels`` Image.

    This context manager loads data into the global ``pixels`` Image.
    Once the program execution leaves the context manager, all changes
    to the image are written to the main display.

    """
    pixels = PImage(builtins.width, builtins.height, "RGB")
    # sketch.renderer.flush_geometry()
    pixel_data = p5.renderer.fbuffer.read(mode="color", alpha=False)

    pixels._img = Image.fromarray(pixel_data)
    builtins.pixels = pixels

    pixels._load()

    yield

    with push_style():
        image_mode("corner")
        p5.renderer.style.tint_enabled = False
        image(builtins.pixels, (0, 0))

    builtins.pixels = None


def save_frame(filename=None):
    if filename:
        p5.sketch.screenshot(filename)
    else:
        p5.sketch.screenshot("Screen.png")

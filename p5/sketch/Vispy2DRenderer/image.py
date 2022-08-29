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
from p5.core import p5

from p5.core import color
from p5.pmath import constrain
from p5.pmath.utils import _is_numeric
from p5.core.structure import push_style

from p5.core import constants
from p5.core.image import PImage


def _ensure_loaded(func):
    """Reloads the image if required before calling the function."""

    @functools.wraps(func)
    def rfunc(self, *args, **kwargs):
        if self._img_data is None or self._reload:
            self._load()
        return func(self, *args, **kwargs)

    return rfunc


@contextlib.contextmanager
def _restore_color_mode():
    old_mode = p5.renderer.style.color_parse_mode
    old_range = p5.renderer.style.color_range
    color.color_mode(constants.RGB, 255, 255, 255, 255)

    yield

    color.color_mode(old_mode, *old_range)


class VispyPImage(PImage):
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

        patch = VispyPImage(patch_width, patch_height)
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

    def update_pixels(self):
        pass

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

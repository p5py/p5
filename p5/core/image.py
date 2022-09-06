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
from . import p5
from abc import ABC, abstractmethod

__all__ = [
    "PImage",
    "image",
    "load_image",
    "image_mode",
    "load_pixels",
    "update_pixels",
    "create_image",
    "save_canvas",
]


class PImage(ABC):
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

    @property
    @abstractmethod
    def width(self):
        """The width of the image

        :rtype: int
        """
        pass

    @width.setter
    @abstractmethod
    def width(self, new_width):
        pass

    @property
    @abstractmethod
    def height(self):
        """The height of the image

        :rtype: int
        """
        pass

    @height.setter
    @abstractmethod
    def height(self, new_height):
        pass

    @property
    @abstractmethod
    def size(self):
        """The size of the image

        :rtype: (int, int) tuple
        """
        pass

    @size.setter
    @abstractmethod
    def size(self, new_size):
        """
        set or resize the PImage
        :param size: size of the image
        :type size: tuple
        """
        pass

    @property
    @abstractmethod
    def aspect_ratio(self):
        """Return the aspect ratio of the image.

        :rtype: float | int
        """
        pass

    @abstractmethod
    def load_pixels(self):
        """Load internal pixel data for the image.

        By default image data is only loaded lazily, i.e., right
        before displaying an image on the screen. Use this method to
        manually load the internal image data.

        """
        pass

    @abstractmethod
    def update_pixels(self):
        """
        Updates the display window with the data in the pixels[] array.
        Use in conjunction with loadPixels()
        """

    @abstractmethod
    def mask(self, image):
        raise NotImplementedError

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def save(self, file_name):
        pass


def image(img, x, y, w=None, h=None):
    """Draw an image to the display window.

    Images must be in the same folder as the sketch (or the image path
    should be explicitly mentioned). The color of an image may be
    modified with the :meth:`p5.tint` function.

    :param img: PImage | Graphics object to be displayed.
    :type img: PImage or Graphics

    :param x: x-coordinate of the image by default
    :type x: float

    :param y: y-coordinate of the image by default
    :type y: float

    :param w: width to display the image by default
    :type w: float

    :param h: height to display the image by default
    :type h: float

    """
    p5.renderer.image(img, x, y, w, h)


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
        Check for types.

    """

    if mode.lower() not in ["corner", "center", "corners"]:
        raise ValueError("Unknown image mode!")
    p5.renderer.style.image_mode = mode.lower()


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

    :returns: An :class:`PImage` instance with the given image data
    :rtype: :class:`PImage`

    """
    return p5.renderer.load_image(filename)


def load_pixels():
    """Load a snapshot of the display window into the ``pixels`` Image.

    This context manager loads data into the global ``pixels`` Image.
    Once the program execution leaves the context manager, all changes
    to the image are written to the main display.

    """
    p5.renderer.load_pixels()


def update_pixels():
    """
    Updates the display window with the data in the pixels[] array.
    Use in conjunction with loadPixels()
    """
    p5.renderer.update_pixels()


def save_canvas(filename=None, canvas=None):
    """
    Saves the given Canvas as an image with filename
    :param filename: filename/path for the image
    :type filename: str

    :param canvas: Canvas to be saved. If not specified default canvas is used
    :type canvas: PGraphics
    """
    p5.renderer.save_canvas(filename, canvas)


def create_image(width, height):
    """
    Creates a new p5.Image (the datatype for storing images). This provides a fresh buffer of pixels to play with.
    Set the size of the buffer with the width and height parameters.

    :param width: Width in pixels
    :type width: int

    :param height: Height in pixels
    :type height: int
    """
    return p5.renderer.create_image(width, height)

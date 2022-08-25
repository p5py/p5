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

from . import constants

__all__ = ["PImage", "image", "load_image", "image_mode", "load_pixels"]


class PImage:
    pass


def image(*args, size=None):
    """Draw an image to the display window.

    Images must be in the same folder as the sketch (or the image path
    should be explicitly mentioned). The color of an image may be
    modified with the :meth:`p5.tint` function.

    :param img: the image to be displayed.
    :type img: p5.Image

    :param x: x-coordinate of the image by default
    :type float:

    :param y: y-coordinate of the image by default
    :type float:

    :param w: width to display the image by default
    :type float:

    :param h: height to display the image by default
    :type float:

    """
    p5.renderer.image(*args)


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

    :returns: An :class:`p5.PImage` instance with the given image data
    :rtype: :class:`p5.PImage`

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
    Updates the display window with the data in the pixels[] array. Use in conjunction with loadPixels(). If you're only reading pixels from the array, there's no need to call updatePixels() — updating is only necessary to apply changes. updatePixels() should be called anytime the pixels array is manipulated or set() is called, and only changes made with set() or direct changes to pixels[] will occur.
    """
    p5.renderer.update_pixels()


def save_frame(filename=None):
    p5.renderer.save_frame(filename)

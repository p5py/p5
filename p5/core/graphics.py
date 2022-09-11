from abc import ABC
from . import constants
from . import p5

__all__ = ["create_graphics"]


class Graphics(ABC):
    """
    Thin wrapper around a renderer, to be used for creating a graphics buffer object.
    Use this class if you need to draw into an off-screen graphics buffer.
    The two parameters define the width and height in pixels.
    The fields and methods for this class are extensive, but mirror the normal drawing API for p5.

    Graphics object are not meant to be used directly in sketches.
    User should always use create_graphics to make an offscreen buffer
    """

    pass


def create_graphics(width, height, renderer=constants.P2D):
    """
    Creates and returns a new off-screen graphics buffer that you can draw on

    :param width: width of the offscreen graphics buffer in pixels
    :type width: int

    :param height: height of the offscreen graphics buffer in pixels
    :type height: int

    :param renderer: Default P2D, and only available in skia renderer
    :type renderer: constant

    :returns: Off screen graphics buffer
    :rtype: Graphics

    """
    return p5.renderer.create_graphics(width, height, renderer)

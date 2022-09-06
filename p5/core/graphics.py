from abc import ABC
from . import constants
from . import p5

__all__ = ["create_graphics"]


class Graphics(ABC):
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

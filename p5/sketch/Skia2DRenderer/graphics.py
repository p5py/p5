import skia

from p5.core.graphics import Graphics
from . import renderer2d
from p5.core import p5

import p5 as p5_lib

def setup_default_renderer_dec(func):
    def helper(*args, **kwargs):
        current_renderer = p5.renderer
        p5.renderer = args[0].renderer
        return_value = func(*args, **kwargs)
        p5.renderer = current_renderer
        return return_value

    return helper

def wrap_instance_helper(func):
    def helper(*args, **kwargs):
        """
        Ignore the first argument passed and call the function. First argument would be reference to graphics object
        of the method
        """
        return func(*args[1:], **kwargs)

    return helper


class SkiaGraphics(Graphics):
    def __init__(self, width, height):
        """
        Creates a Skia based Graphics object

        :param width: width in pixels
        :type width: int

        :param height: height in pixels
        :type height: int
        """
        self.width = width
        self.height = height
        # TODO: Try creating a GPU backed surface for better results
        self.surface = skia.Surface(width, height)
        self.canvas = self.surface.getCanvas()
        self.path = skia.Path()
        self.paint = skia.Paint()
        self.renderer = renderer2d.SkiaRenderer()

        self.renderer.initialize_renderer(self.canvas, self.paint, self.path)


def bind(instance, func, as_name=None):
    """
    Bind the function *func* to *instance*, with either provided name *as_name*
    or the existing name of *func*. The provided *func* should accept the
    instance as the first argument, i.e. "self".
    """
    if as_name is None:
        as_name = func.__name__
    bound_method = func.__get__(instance, instance.__class__)
    setattr(instance, as_name, bound_method)
    return bound_method


methods = [p5_lib.circle, p5_lib.background]


def create_graphics_helper(width, height):
    graphics = SkiaGraphics(width, height)
    for method in methods:
        bind(graphics, setup_default_renderer_dec(wrap_instance_helper(method)), method.__name__)

    return graphics

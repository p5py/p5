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


methods = [
    # Setting
    p5_lib.background,
    p5_lib.clear,
    p5_lib.color_mode,
    p5_lib.fill,
    p5_lib.no_fill,
    p5_lib.no_stroke,
    p5_lib.stroke,
    # Shape
    p5_lib.arc,
    p5_lib.ellipse,
    p5_lib.circle,
    p5_lib.point,
    p5_lib.quad,
    p5_lib.rect,
    p5_lib.line,
    p5_lib.square,
    p5_lib.rect,
    # Attributes
    p5_lib.ellipse_mode,
    p5_lib.rect_mode,
    p5_lib.stroke_cap,
    p5_lib.stroke_join,
    p5_lib.stroke_weight,
    # Curves
    p5_lib.bezier,
    p5_lib.bezier_detail,
    p5_lib.bezier_point,
    p5_lib.curve,
    p5_lib.curve_detail,
    p5_lib.curve_tightness,
    p5_lib.curve_point,
    p5_lib.curve_tangent,
    # Vertex
    p5_lib.begin_contour,
    p5_lib.begin_shape,
    p5_lib.bezier_vertex,
    p5_lib.curve_vertex,
    p5_lib.end_contour,
    p5_lib.end_shape,
    p5_lib.quadratic_vertex,
    p5_lib.vertex,
    # Structure
    p5_lib.push,
    p5_lib.pop,
    p5_lib.push_matrix,
    p5_lib.pop_matrix,
    p5_lib.push_style,
    p5_lib.pop_style,
    # Transform
    p5_lib.apply_matrix,
    p5_lib.reset_matrix,
    p5_lib.rotate,
    p5_lib.scale,
    p5_lib.shear_x,
    p5_lib.shear_y,
    p5_lib.translate,
    # Local Storage
    p5_lib.get_item,
    p5_lib.clear_storage,
    p5_lib.remove_item,
    p5_lib.set_item,
    # Image
    p5_lib.save_canvas,
    p5_lib.image,
    p5_lib.tint,
    p5_lib.no_tint,
    p5_lib.image_mode,
    p5_lib.load_pixels,
    p5_lib.update_pixels,
    p5_lib.noise,
    p5_lib.noise_detail,
    p5_lib.noise_seed,
    # Random
    p5_lib.random_seed,
    p5_lib.random_uniform,
    p5_lib.random_gaussian,
    # Typography
    p5_lib.text_align,
    p5_lib.text_leading,
    p5_lib.text_size,
    p5_lib.text_style,
    p5_lib.text_width,
    p5_lib.text_ascent,
    p5_lib.text_descent,
    p5_lib.text_wrap,
    p5_lib.text,
    p5_lib.text_font,
]


def create_graphics_helper(width, height):
    graphics = SkiaGraphics(width, height)
    for method in methods:
        bind(
            graphics,
            setup_default_renderer_dec(wrap_instance_helper(method)),
            method.__name__,
        )

    return graphics

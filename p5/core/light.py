from . import p5
from ..sketch.util import ensure_p3d, scale_tuple
import numpy as np

__all__ = [
    "lights",
    "ambient_light",
    "directional_light",
    "point_light",
    "light_falloff",
    "light_specular",
]


def lights():
    """Sets the default ambient light, directional light, falloff, and specular values.

    The defaults are ambientLight(128, 128, 128), directionalLight(128, 128, 128, 0, 0, -1), and lightFalloff(1, 0, 0).
    """
    ambient_light(128, 128, 128)
    directional_light(128, 128, 128, 0, 0, -1)
    light_falloff(1, 0, 0)


def ambient_light(r, g, b):
    """Adds an ambient light.

    Ambient light comes from all directions towards all directions.
    Ambient lights are almost always used in combination with other types of lights.

    :param r: red channel
    :type r: float

    :param g: green channel
    :type g: float

    :param b: blue channel
    :type b: float
    """
    ensure_p3d("ambient_light")
    p5.renderer.add_ambient_light(*scale_tuple((r, g, b)))


def directional_light(r, g, b, x, y, z):
    """Adds a directional light.
    Directional light comes from one direction: it is stronger when hitting a surface squarely,
    and weaker if it hits at a gentle angle.
    After hitting a surface, directional light scatters in all directions.

    :param r: red channel
    :type r: float

    :param g: green channel
    :type g: float

    :param b: blue channel
    :type b: float

    :param x: x component of the direction vector
    :type x: float

    :param y: y component of the direction vector
    :type y: float

    :param z: z component of the direction vector
    :type z: float
    """
    ensure_p3d("directional_light")
    p5.renderer.add_directional_light(*scale_tuple((r, g, b)), x, y, z)


def point_light(r, g, b, x, y, z):
    """Adds a point light.
    Point light comes from one location and emits to all directions.

    :param r: red channel
    :type r: float

    :param g: green channel
    :type g: float

    :param b: blue channel
    :type b: float

    :param x: x component of the location vector
    :type x: float

    :param y: y component of the location vector
    :type y: float

    :param z: z component of the location vector
    :type z: float
    """
    ensure_p3d("point_light")
    p5.renderer.add_point_light(*scale_tuple((r, g, b)), x, y, z)


def light_falloff(constant, linear, quadratic):
    """Sets the falloff rates for point lights. Affects only the elements which are created after it in the code.

    d = distance from light position to vertex position

    falloff = 1 / (constant + d * linear + (d*d) * quadratic)

    If the coefficient is 0, then that term is ignored.
    The P3D renderer defaults to (0, 0, 0), i.e. no falloff.

    :param constant: coefficient for the constant term
    :type constant: float

    :param linear: coefficient for the linear term
    :type linear: float

    :param quadratic: coefficient for the quadratic term
    :type quadratic: float
    """
    ensure_p3d("light_falloff")
    p5.renderer.curr_constant_falloff = constant
    p5.renderer.curr_linear_falloff = linear
    p5.renderer.curr_quadratic_falloff = quadratic


def light_specular(r, g, b):
    """Sets the specular color for lights. Only visible with :any:`p5.blinn_phong_material`. Is set to (0 ,0, 0) by default.
    Affects only the elements which are created after it in the code.

    Specular refers to light which bounces off a surface in a preferred direction
    (rather than bouncing in all directions like a diffuse light) and is used for
    creating highlights. The specular quality of a light interacts with the specular
    material qualities set through the `specular()` and `shininess()` functions.

    :param r: red channel
    :type r: float

    :param g: green channel
    :type g: float

    :param b: blue channel
    :type b: float
    """
    ensure_p3d("light_specular")
    p5.renderer.light_specular = np.array(scale_tuple((r, g, b)))

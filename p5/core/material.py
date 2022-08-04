from . import p5, fill
from ..sketch.util import ensure_p3d, scale_tuple
import numpy as np

__all__ = [
    "normal_material",
    "basic_material",
    "blinn_phong_material",
    "ambient",
    "emissive",
    "diffuse",
    "shininess",
    "specular",
]


class BasicMaterial:
    def __init__(self, color):
        self.color = color


class NormalMaterial:
    pass


class BlinnPhongMaterial:
    def __init__(self, ambient, diffuse, specular, shininess):
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess


def normal_material():
    """The color is determined by the normal vector of a surface. Does not respond to lights.

    Useful for debugging.
    """
    ensure_p3d("normal_material")
    p5.renderer.style.material = NormalMaterial()


def basic_material(r, g, b):
    """The default material. Always displays a solid color.

    :param r: red channel
    :type r: float

    :param g: green channel
    :type g: float

    :param b: blue channel
    :type b: float
    """
    ensure_p3d("basic_material")
    fill(r, g, b)
    p5.renderer.style.material = BasicMaterial(p5.renderer.style.fill_color)


def blinn_phong_material():
    """Material based on the Blinn-Phong reflection model. This is the most "realistic" material in p5py.

    Blinn-Phong shading can be decomposed into three parts:
    ambient, diffuse, and specular.

    The ambient component is essentially a constant term that is alway present.
    We calculate it by summing all the ambient lights in a scene and multiplying it
    with the normalized ambient coefficent set by ambient.

    The diffuse component takes the normal vector of a surface into account and
    varies how much light is reflected depending on the angle that the surface
    makes with the incoming light.

    The specular component not only accounts for the direction of the light
    (like the diffuse component) but also the direction of the viewer. If the
    viewer is not on the path of the reflected light, the specular component
    falls off quickly, producing the glossy reflections we see on some materials.

    The color shown on the user's screen is the sum of all three components.
    """
    ensure_p3d("blinn_phong_material")
    rend = p5.renderer.style
    p5.renderer.style.material = BlinnPhongMaterial(
        rend.ambient, rend.diffuse, rend.specular, rend.shininess
    )


def ambient(r, g, b):
    """Sets the ambient light color reflected by the next :any:`blinn_phong_material`.

    :param r: red channel
    :type r: float

    :param g: green channel
    :type g: float

    :param b: blue channel
    :type b: float
    """
    ensure_p3d("ambient")
    p5.renderer.style.ambient = np.array(scale_tuple((r, g, b)), dtype=np.float32)


def emissive(r, g, b):
    """This function is the same as diffuse.

    :param r: red channel
    :type r: float

    :param g: green channel
    :type g: float

    :param b: blue channel
    :type b: float
    """
    ensure_p3d("emissive")
    return diffuse(*scale_tuple((r, g, b)))


def diffuse(r, g, b):
    """Sets the diffuse light color reflected by the next :any:`blinn_phong_material`.

    :param r: red channel
    :type r: float

    :param g: green channel
    :type g: float

    :param b: blue channel
    :type b: float
    """
    ensure_p3d("diffuse")
    p5.renderer.style.diffuse = np.array(scale_tuple((r, g, b)), dtype=np.float32)


def shininess(p):
    """Sets how glossy the next :any:`blinn_phong_material` is. This only affects the specular term.

    Should be used together with :any:`light_specular` and :any:`specular`.

    :param p: exponent of the cosine term in the `Blinn-Phong Reflection Model <https://en.wikipedia.org/wiki/Blinn%E2%80%93Phong_reflection_model>`_
    :type p: float
    """
    ensure_p3d("shininess")
    p5.renderer.style.shininess = p


def specular(r, g, b):
    """Sets the specular light color reflected by the next :any:`blinn_phong_material`.

    Should be used together with :any:`light_specular`.
    """
    ensure_p3d("specular")
    p5.renderer.style.specular = np.array(scale_tuple((r, g, b)), dtype=np.float32)


# TODO: Document default values for material functions in renderer3D

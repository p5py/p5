from . import p5, fill
from ..sketch.util import ensure_p3d
import numpy as np

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
    ensure_p3d("normal_material")
    p5.renderer.material = NormalMaterial()


def basic_material(r, g, b):
    ensure_p3d("basic_material")
    fill(r, g, b)
    p5.renderer.material = BasicMaterial(p5.renderer.fill_color)


def blinn_phong_material():
    ensure_p3d("blinn_phong_material")
    rend = p5.renderer
    p5.renderer.material = BlinnPhongMaterial(rend.ambient, rend.diffuse, rend.specular, rend.shininess)


def ambient(r, g, b):
    ensure_p3d('ambient')
    p5.renderer.ambient = np.array((r, g, b), dtype=np.float32)


def emissive(r, g, b):
    ensure_p3d('emissive')
    return diffuse(r, g, b)


def diffuse(r, g, b):
    ensure_p3d('diffuse')
    p5.renderer.diffuse = np.array((r, g, b), dtype=np.float32)


def shininess(p):
    ensure_p3d('shininess')
    p5.renderer.shininess = p


def specular(r, g, b):
    ensure_p3d('specular')
    p5.renderer.specular = np.array((r, g, b), dtype=np.float32)

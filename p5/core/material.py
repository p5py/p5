from . import p5
from . import fill


class BasicMaterial:
    def __init__(self, color):
        self.color = color


class NormalMaterial:
    pass


class BlinnPhongMaterial:
    def __init__(self, color, ambient, diffuse, specular, shininess):
        self.color = color
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess


def ensure_p3d(name):
    assert p5.mode == 'P3D', name + "is only available in P3D renderer"


def normal_material():
    ensure_p3d("normal_material")
    p5.renderer.material = NormalMaterial()


def basic_material(r, g, b):
    ensure_p3d("basic_material")
    fill(r, g, b)
    p5.renderer.material = BasicMaterial(p5.renderer.fill_color)


def blinn_phong_material(r, g, b):
    ensure_p3d("blinn_phong_material")
    fill(r, g, b)
    r = p5.renderer
    p5.renderer.material = BlinnPhongMaterial(r.fill_color, r.ambient, r.diffuse, r.specular, r.shininess)

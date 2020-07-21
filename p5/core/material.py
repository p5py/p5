from . import p5
from ..sketch.renderer3d import Shader
from . import fill

__all__ = ['normal_material', 'basic_material']


def ensure_p3d(name):
    assert p5.mode == 'P3D', name + "is only available in P3D renderer"


def normal_material():
    ensure_p3d("normal_material")
    p5.renderer.shader = Shader.NORMAL


def basic_material(r, g, b):
    ensure_p3d("basic_material")
    p5.renderer.shader = Shader.BASIC
    fill(r, g, b)

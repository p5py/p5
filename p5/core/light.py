from . import p5
from ..sketch.util import ensure_p3d

__all__ = ['lights', 'ambient_light', 'directional_light', 'point_light', 'light_falloff']


def lights():
    ambient_light(128, 128, 128)
    directional_light(128, 128, 128, 0, 0, -1)
    light_falloff(1, 0, 0)


def ambient_light(r, g, b):
    ensure_p3d('ambient_light')
    p5.renderer.add_ambient_light(r, g, b)


def directional_light(r, g, b, x, y, z):
    ensure_p3d('directional_light')
    p5.renderer.add_directional_light(r, g, b, x, y, z)


def point_light(r, g, b, x, y, z):
    ensure_p3d('point_light')
    p5.renderer.add_point_light(r, g, b, x, y, z)


def light_falloff(constant, linear, quadratic):
    ensure_p3d('light_falloff')
    raise NotImplementedError()

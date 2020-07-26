from . import p5, Color
from ..pmath import Point, Vector
from ..sketch.util import ensure_p3d


class Light:
    def __init__(self, color):
        self.color = color


class AmbientLight(Light):
    pass


class DirectionalLight(Light):
    def __init__(self, color, direction):
        super(DirectionalLight, self).__init__(color)
        self.direction = direction


class PointLight(Light):
    def __init__(self, color, position):
        super(PointLight, self).__init__(color)
        self.position = position


def lights():
    ambient_light(128, 128, 128)
    directional_light(128, 128, 128, 0, 0, -1)
    light_falloff(1, 0, 0)


def ambient_light(r, g, b):
    ensure_p3d('ambient_light')
    p5.renderer.add_light(AmbientLight(Color(r, g, b)))


def directional_light(r, g, b, x, y, z):
    ensure_p3d('directional_light')
    p5.renderer.add_light(DirectionalLight(Color(r, g, b), Vector(x, y, z).normalize()))


def point_light(r, g, b, x, y, z):
    ensure_p3d('point_light')
    p5.renderer.add_light(PointLight(Color(r, g, b), Point(x, y, z)))


def light_falloff(constant, linear, quadratic):
    ensure_p3d('light_falloff')
    raise NotImplementedError()

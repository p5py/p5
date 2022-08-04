import pkgutil
import os
from ..core import p5
import builtins


def read_shader(filename):
    """Reads a shader in string mode and returns the content"""

    return pkgutil.get_data("p5", os.path.join("sketch/", filename)).decode()


def ensure_p3d(name):
    assert p5.mode == "P3D", name + "is only available in P3D renderer"


def scale_tuple(t, scale=255):
    """Divides each element of tuple by scale"""
    return tuple(x / scale for x in t)

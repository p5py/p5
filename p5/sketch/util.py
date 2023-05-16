import pkgutil
import os
from typing import Tuple
from ..core import p5
import builtins


def read_shader(filename: str):
    """Reads a shader in string mode and returns the content"""

    return pkgutil.get_data("p5", os.path.join("sketch/", filename)).decode()


def ensure_p3d(name: str):
    assert p5.mode == "P3D", f"{name}is only available in P3D renderer"


def scale_tuple(t: Tuple[float, ...], scale: float = 255):
    """Divides each element of tuple by scale"""
    return tuple(x / scale for x in t)

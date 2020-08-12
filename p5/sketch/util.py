import pkgutil
import os
from ..core import p5

def read_shader(filename):
    """Reads a shader in string mode and returns the content
    """
    return pkgutil.get_data('p5', os.path.join('sketch/shaders/',filename)).decode()

def ensure_p3d(name):
    assert p5.mode == 'P3D', name + "is only available in P3D renderer"

def scale_colors(r, g, b):
    """Divides each channel by 255
    """
    return (r / 255.0, g / 255.0, b / 255.0)

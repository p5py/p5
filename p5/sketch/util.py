import pkgutil
import os
from ..core import p5
import builtins


def read_shader(filename):
    """Reads a shader in string mode and returns the content
    """
    renderer_name = ""
    if builtins.current_renderer == "vispy":
        if p5.mode == 'P2D':
            renderer_name = "Vispy2DRenderer"
        elif p5.mode == 'P3D':
            renderer_name = "Vispy3DRenderer"

    # This check could be skipped, it is only present to debug tests
    if renderer_name == "":
        raise ValueError("Renderer Name is not defined. \nValues : p5.mode = {} builtins.renderer = {}"
                         .format(p5.mode, builtins.current_renderer))

    return pkgutil.get_data('p5', os.path.join(
        'sketch/' + renderer_name + '/shaders/', filename)).decode()


def ensure_p3d(name):
    assert p5.mode == 'P3D', name + "is only available in P3D renderer"


def scale_tuple(t, scale=255):
    """Divides each element of tuple by scale
    """
    return tuple(x / scale for x in t)

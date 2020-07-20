import pkgutil
import os

def read_shader(filename):
    """Reads a shader in string mode and returns the content
    """
    return pkgutil.get_data('p5', os.path.join('sketch/shaders/',filename)).decode()

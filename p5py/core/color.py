from pyglet.gl import *

from .. import _p5_attrs
from .. import p5
from .. import _affects

def _get_color(*args, **kwargs):
    """
    Returns a (r, g, b, a) color tuple based on the args and kwargs.

    The args take care of the overloading in Processing.

    (rgb)               -- color varibale or hex value (NOT IMPLEMENTED)
    (rgb, alpha)        -- (NOT IMPLEMENTED)
    (gray)
    (gray, alpha)
    (v1, v2, v3)        -- (r, g, b) or (h, s, v) color values. For now,
                            we only have (r, g, b) support
    (v1, v2, v3, alpha)

    Maybe:
        * `mode` kwarg selects color mode (RGB/HSV)
        * `range` kwargs selects color range (i.e., what counts as max)
    """

    r = g = b = a = 255

    if len(args) == 1:
        r = g = b = args[0]
    elif len(args) == 2:
        r = g = b = args[0]
        a = args[1]
    elif len(args) == 3:
        r, g, b = args
    elif len(args) == 4:
        r, g, b, a = args

    if 'gray' in kwargs:
        r = g = b = kwargs['gray']
    if 'alpha' in kwargs:
        a = kwargs['alpha']
    if all(c in kwargs for c in ['r', 'g', 'b']):
        r = kwargs['r']
        g = kwargs['g']
        b = kwargs['b']

    return (r/255.0, g/255.0, b/255.0, a/255.0)

def fill(*args, **kwargs):
    _p5_attrs['fill_enabled'] = True
    _p5_attrs['fill_color'] = _get_color(*args, **kwargs)

def no_fill():
    _p5_attrs['fill_enabled'] = False

def stroke(*args, **kwargs):
    _p5_attrs['stroke_enabled'] = True
    _p5_attrs['stroke_color'] = _get_color(*args, **kwargs)

def stroke_weight(weight):
    _p5_attrs['stroke_weight'] = int(weight)

def no_stroke():
    _p5_attrs['stroke_enabled'] = False

@_affects
def background(*args, **kwargs):
    _p5_attrs['background'] = _get_color(*args, **kwargs)
    glClearColor(*_p5_attrs['background'])
    glClear(GL_COLOR_BUFFER_BIT)

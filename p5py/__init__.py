import math
from time import sleep
import __main__

from pyglet.gl import *

from .core.constants import *


_p5_attrs = {
    'background': (0.8, 0.8, 0.8, 1),
    'fill_color': (1, 1, 1, 1),
    'fill_enabled': True,

    'stroke_color': (0, 0, 0, 1),
    'stroke_enabled': True,
    'stroke_weight': 1,

    'smooth_enabled': True
}

width = 800
height = 600

config = Config(sample_buffers=1, samples=4, depth_size=24, alpha_size=8, \
                double_buffer=True)
p5 = pyglet.window.Window(width=width, height=height, caption="p5py", \
                            config=config)

glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
glEnable(GL_LINE_SMOOTH)
glEnable(GL_POINT_SMOOTH)
glEnable(GL_POLYGON_SMOOTH)

glViewport(0, 0, p5.width, p5.height)
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
glOrtho(0, p5.width, p5.height, 0, -1, 1)
glMatrixMode(GL_MODELVIEW)

# Set default colors and line widths
glColor4f(*_p5_attrs['fill_color'])
glLineWidth(_p5_attrs['stroke_weight'])
glClearColor(*_p5_attrs['background'])
glClear(GL_COLOR_BUFFER_BIT)
p5.flip()

def _affects(func):
    """
    Checks what mode p5py is running in and then decides if the buffers
    should be flipped after every function call that "affects" the main
    canvas.

    Since the event loop causes a buffer flip on every iteration, we
    need to do p5.flip() only while running in interactive mode.
    """
    def flipper(*args, **kwargs):
        func_return = func(*args, **kwargs)
        p5.flip()
        return func_return

    # __main__ doens't have the __file__ attr when Python is in the 
    # interactive mode.
    if not hasattr(__main__, '__file__'):
        return flipper
    else:
        raise NotImplementedError

from .core.primitives import *
from .core.color import *
from .core.pmath import *

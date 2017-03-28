import math
from time import sleep
from pyglet import app
from pyglet.app import EventLoop
from pyglet.gl import *
from pyglet.window import Window

_attr_color_background = (0.8, 0.8, 0.8, 1)
_attr_color_fill = (1, 1, 1, 1)
_attr_color_stroke = (0, 0, 0, 1)
_attr_stroke = True
_attr_stroke_weight = 1
_attr_fill = True

WIDTH = 800
HEIGHT = 600
PI = math.pi
HALF_PI = math.pi / 2.0
THIRD_PI = math.pi / 3.0
QUARTER_PI = math.pi / 4.0
TWO_PI = 2.0 * math.pi
TAU = TWO_PI
DEG_TO_RAD = PI/180
RAD_TO_DEG = 180/PI

config = Config(sample_buffers=1, samples=4, depth_size=24, alpha_size=8, \
                double_buffer=True)
p5 = Window(config=config, width=WIDTH, height=HEIGHT, caption="p5py")
glEnable (GL_BLEND)
glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
glViewport(0, 0, p5.width, p5.height)
glMatrixMode(gl.GL_PROJECTION)
glLoadIdentity()
glOrtho(0, p5.width, p5.height, 0, -1, 1)
glMatrixMode(gl.GL_MODELVIEW)

# Set default colors and line widths
glColor4f(*_attr_color_fill)
glLineWidth(_attr_stroke_weight)
glClearColor(*_attr_color_background)
glClear(GL_COLOR_BUFFER_BIT)
p5.flip()

@p5.event
def on_resize(width, height):
    global WIDTH, HEIGHT
    WIDTH = width
    HEIGHT = height
    glViewport(0, 0, width, height)
    glMatrixMode(gl.GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, width, height, 0, -1, 1)
    glMatrixMode(gl.GL_MODELVIEW)
    p5.flip()

def size(width, height):
    p5.set_size(max(120, width), max(120, height))
    p5.flip()


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
    global _attr_fill
    _attr_fill = True
    global _attr_color_fill
    _attr_color_fill = _get_color(*args, **kwargs)

def no_fill():
    global _attr_fill
    _attr_fill = False

def stroke(*args, **kwargs):
    global _attr_stroke
    _attr_stroke = True
    global _attr_color_stroke
    _attr_color_stroke = _get_color(*args, **kwargs)

def stroke_weight(weight):
    global _attr_stroke_weight
    _attr_stroke_weight = int(weight)

def no_stroke():
    global _attr_stroke
    _attr_stroke = False

def background(*args, **kwargs):
    global _attr_color_background
    _attr_color_background = _get_color(*args, **kwargs)
    glClearColor(*_attr_color_background)
    glClear(GL_COLOR_BUFFER_BIT)
    p5.flip()

def _shape_2d(*points):
    glLoadIdentity()
    if _attr_fill:
        glColor4f(*_attr_color_fill)
        glBegin(GL_POLYGON)
        for point in points:
            glVertex2f(*point)
        glEnd()

    if _attr_stroke:
        glColor4f(*_attr_color_stroke)
        glLineWidth(_attr_stroke_weight)
        glBegin(GL_LINE_LOOP)
        for point in points:
            glVertex2f(*point)
        glEnd()
    p5.flip()

def point(x, y):
    glLoadIdentity()
    global _attr_stroke
    if _attr_stroke:
        glPointSize(_attr_stroke_weight)
        glColor4f(*_attr_color_stroke)
    
        glBegin(GL_POINTS)
        glVertex2f(x, y)
        glEnd()
        p5.flip()

def line(x1, y1, x2, y2):
    glLoadIdentity()
    global _attr_stroke
    if _attr_stroke:
    
        glLineWidth(_attr_stroke_weight)
        glColor4f(*_attr_color_stroke)
        glBegin(GL_LINES)
        glVertex2f(x1, y1)
        glVertex2f(x2, y2)
        glEnd()
        p5.flip()

def triangle(x1, y1, x2, y2, x3, y3):
    p1 = (x1, y1)
    p2 = (x2, y2)
    p3 = (x3, y3)
    _shape_2d(p1, p2, p3)

def quad(x1, y1, x2, y2, x3, y3, x4, y4):
    p1 = (x1, y1)
    p2 = (x2, y2)
    p3 = (x3, y3)
    p4 = (x4, y4)
    _shape_2d(p1, p2, p3, p4)

def rect(x, y, width, height):
    quad(x, y, x + width, y, x + width, y + height, x, y + height)

def ellipse(x, y, width, height):
    ellipse_vertices = [
        ((x + 0.5 * width * math.cos(t * (math.pi/180))),
         (y + 0.5 * height * math.sin(t * (math.pi/180))))
            for t in range(360)]
    _shape_2d(*ellipse_vertices)

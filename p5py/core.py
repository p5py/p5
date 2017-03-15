import math

from OpenGL.GL import *
from OpenGL.GLU import *

from . import globs
from . import _attribs as attr

def _map_point(px, py):
    """
    Map the x-coords form (0, width) to (0, 1), similarly, map
    the y-coords from (0, height) to (0, -1). We put the negative to 
    make the coordinate system similar to Processing's.
    
    OpenGL should have a way of doing this
    """
    return px/globs.WIDTH, py/globs.HEIGHT*(-1)

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
    attr.fill = True
    attr.color_fill = _get_color(*args, **kwargs)

def no_fill():
    attr.fill = False    

def stroke(*args, **kwargs):
    attr.stroke = True
    attr.color_stroke = _get_color(*args, **kwargs)

def stroke_weight(weight):
    attr.stroke_weight = int(weight)

def no_stroke():
    attr.stroke = False

def background(*args, **kwargs):
    # DEBUG: this is causes a whole lot of flickering. 
    attr.color_background = _get_color(*args, **kwargs)
    glClearColor(*attr.color_background)
    glClear(GL_COLOR_BUFFER_BIT)

def point(x, y):
    if attr.stroke:
        glPointSize(attr.stroke_weight)
        glColor4f(*attr.color_stroke)
        glBegin(GL_POINTS)
        glVertex2f(*_map_point(x, y))
        glEnd()

def line(src, dest):
    """
    Draws a line from the point src to the point dest if attr.stroke is
    set to True. src and dest are tuples.
    """
    if attr.stroke:
        glLineWidth(attr.stroke_weight)
        glColor4f(*attr.color_stroke)
        glBegin(GL_LINES)
        glVertex2f(*_map_point(*src))
        glVertex2f(*_map_point(*dest))
        glEnd()

def _shape_2d(*points):
    """
    Draws a 2D shape based on the list of points given as args.
    """
    if attr.fill:
        glColor4f(*attr.color_fill)
        glBegin(GL_POLYGON)
        for point in points:
            glVertex2f(*_map_point(*point))
        glEnd()

    if attr.stroke:
        glColor4f(*attr.color_stroke)
        glLineWidth(attr.stroke_weight)
        glBegin(GL_LINE_LOOP)
        for point in points:
            glVertex2f(*_map_point(*point))
        glEnd()

def triangle(p1, p2, p3):
    _shape_2d(p1, p2, p3)

def quad(p1, p2, p3, p4):
    _shape_2d(p1, p2, p3, p4)

def rect(x, y, width, height):
    quad((x, y), (x + width, y), (x + width, y + height), (x, y + height))

def ellipse(x, y, width, height):
    ellipse_vertices = [
        ((x + 0.5 * width * math.cos(t * (math.pi/180))),
         (y + 0.5 * height * math.sin(t * (math.pi/180))))
            for t in range(360)]

    _shape_2d(*ellipse_vertices)

def size(*args):
    pass

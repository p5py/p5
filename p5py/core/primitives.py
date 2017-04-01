import math
from pyglet.gl import *

from .. import _affects
from .. import p5
from .. import _p5_attrs

@_affects
def _shape_2d(*points):
    if _p5_attrs['fill_enabled']:
        glColor4f(*_p5_attrs['fill_color'])
        glBegin(GL_POLYGON)
        for point in points:
            glVertex2f(*point)
        glEnd()

    if _p5_attrs['stroke_enabled']:
        glColor4f(*_p5_attrs['stroke_color'])
        glLineWidth(_p5_attrs['stroke_weight'])
        glBegin(GL_LINE_LOOP)
        for point in points:
            glVertex2f(*point)
        glEnd()

@_affects
def point(x, y):
    if _p5_attrs['stroke_enabled']:
        glPointSize(_p5_attrs['stroke_weight'])
        glColor4f(*_p5_attrs['stroke_color'])
        glBegin(GL_POINTS)
        glVertex2f(x, y)
        glEnd()

@_affects
def line(x1, y1, x2, y2):
    if _p5_attrs['stroke_enabled']:
        glLineWidth(_p5_attrs['stroke_weight'])
        glColor4f(*_p5_attrs['stroke_color'])
        glBegin(GL_LINES)
        glVertex2f(x1, y1)
        glVertex2f(x2, y2)
        glEnd()

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

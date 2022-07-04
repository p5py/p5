import contextlib, glfw, skia
from dataclasses import dataclass
from OpenGL import GL

from p5 import p5
from p5.pmath.utils import *


@dataclass
class Style2D:
    background_color = (0.8, 0.8, 0.8, 1.0)
    fill_enabled = True
    stroke_enabled = True
    fill_color = (1, 1, 1, 1)
    stroke_color = (0, 0, 0)
    stroke_weight = 1

    tint_color = (0, 0, 0)
    tint_enabled = False
    ellipse_mode = "CENTER"
    rect_mode = "CORNER"
    color_parse_mode = "RGB"
    color_range = (255, 255, 255, 255)


class SkiaRenderer():
    def __init__(self):
        self.canvas = None
        self.paint = None
        self.style = Style2D()
        self.path = None
        self.font = skia.Font()
        self.typeface = skia.Typeface.MakeDefault()
        self.font.setTypeface(self.typeface)

    def _acute_arc_to_bezier(self, start, size):
        alpha = size / 2
        cos_alpha = cos(alpha)
        sin_alpha = sin(alpha)
        cot_alpha = 1 / tan(alpha)

        phi = start + alpha
        cos_phi = cos(phi)
        sin_phi = sin(phi)
        _lambda = (4 - cos_alpha) / 3
        mu = sin_alpha + (cos_alpha - _lambda) * cot_alpha

        return {
            "ax": round(cos(start), 7),
            "ay": round(sin(start), 7),
            "bx": round((_lambda * cos_phi + mu * sin_phi), 7),
            "by": round((_lambda * sin_phi - mu * cos_phi), 7),
            "cx": round((_lambda * cos_phi - mu * sin_phi), 7),
            "cy": round((_lambda * sin_phi + mu * cos_phi), 7),
            "dx": round(cos(start + size), 7),
            "dy": round(sin(start + size), 7)
        }

    def initialize_renderer(self, canvas, paint, path):
        self.canvas = canvas
        self.paint = paint
        self.path = path

        self.canvas.clear(skia.Color4f(*self.style.background_color))

    def rect(self, x, y, w, h):
        self.path.moveTo(x, y)
        self.path.lineTo(x + w, y)
        self.path.lineTo(x + w, y + h)
        self.path.lineTo(x, y + h)
        self.render()

    def render_circle(self, x, y, radius):
        self.path.addCircle(x, y, radius)
        self.render()

    def render_text(self, text, x, y):
        # full path works relative does not
        # assert (typeface is not None), "should not be NULL"
        # handle alignment manually
        if self.style.fill_enabled:
            self.paint.setStyle(skia.Paint.kFill_Style)
            self.paint.setColor(self.style.fill_color)
            self.canvas.drawPath(self.path, self.paint)

        if self.style.stroke_enabled:
            self.paint.setStyle(skia.Paint.kStroke_Style)
            self.paint.setColor(self.style.stroke_color)
            self.paint.setStrokeWidth(self.style.stroke_weight)
            self.canvas.drawPath(self.path, self.paint)
        self.canvas.drawSimpleText(text, x, y, self.font, self.paint)

    def load_font(self, path):
        """
        path: string
        Absolute path of the font file
        returns: skia.Typeface
        """
        typeface = skia.Typeface.MakeFromFile(path)
        return typeface

    def set_font(self, font):
        """
        Sets the current font to be used for rendering text
        """
        self.typeface = font
        self.font.setTypeface(self.typeface)

    def set_font_size(self, size):
        self.font.setSize(size)

    def render_image(self, img, *args):
        self.canvas.drawImage(img, *args)

    def clear(self):
        self.canvas.clear(skia.Color4f(*self.style.background_color))

    def render(self, fill=True, stroke=True):
        """
        Draw the path on current canvas using paint
        """
        # TODO: Check, do we really have to setColor, and setStyle on each render call
        # TODO: Explore ways to do this, such that it works with pGraphics as well
        if self.style.fill_enabled and fill:
            self.paint.setStyle(skia.Paint.kFill_Style)
            self.paint.setColor(skia.Color4f(*self.style.fill_color))
            self.canvas.drawPath(self.path, self.paint)

        if self.style.stroke_enabled and stroke:
            self.paint.setStyle(skia.Paint.kStroke_Style)
            self.paint.setColor(skia.Color4f(*self.style.stroke_color))
            self.paint.setStrokeWidth(self.style.stroke_weight)
            self.canvas.drawPath(self.path, self.paint)

        self.path.rewind()
        # Reset the font size back to default size
        self.reset()

    def reset(self):
        self.font.setSize(15)

    def line(self, path):
        x1, y1, x2, y2 = path[0].x, path[0].y, path[1].x, path[1].y
        self.path.moveTo(x1, y1)
        self.path.lineTo(x2, y2)
        self.render()

    def arc(self, x, y, w, h, start_angle, stop_angle, mode):
        rx = w / 2
        ry = h / 2
        epsilon = 0.00001
        curves = []

        x += rx
        y += ry

        while stop_angle - start_angle >= epsilon:
            arc_to_draw = min(stop_angle - start_angle, HALF_PI)
            curves.append(self._acute_arc_to_bezier(start_angle, arc_to_draw))
            start_angle += arc_to_draw

        if self.style.fill_enabled:
            for index, curve in enumerate(curves, 0):
                if index == 0:
                    self.path.moveTo(x + curve['ax'] * rx, y + curve['ay'] * ry)
                self.path.cubicTo(x + curve['bx'] * rx, y + curve['by'] * ry,
                                  x + curve['cx'] * rx, y + curve['cy'] * ry,
                                  x + curve['dx'] * rx, y + curve['dy'] * ry)
            if mode == 'PIE' or not mode:
                self.path.lineTo(x, y)

            self.path.close()
            self.render(fill=True, stroke=False)

        if self.style.stroke_enabled:
            for index, curve in enumerate(curves, 0):
                if index == 0:
                    self.path.moveTo(x + curve['ax'] * rx, y + curve['ay'] * ry)
                self.path.cubicTo(x + curve['bx'] * rx, y + curve['by'] * ry,
                                  x + curve['cx'] * rx, y + curve['cy'] * ry,
                                  x + curve['dx'] * rx, y + curve['dy'] * ry)
            if mode == 'PIE':
                self.path.lineTo(x, y)
                self.path.close()
            elif mode == 'CHORD':
                self.path.close()
            self.render(fill=False, stroke=True)

    def ellipse(self, x, y, w, h):
        kappa = 0.5522847498
        ox = w / 2 * kappa
        oy = h / 2 * kappa
        xe = x + w
        ye = y + h
        xm = x + w / 2
        ym = y + h / 2

        self.path.moveTo(x, ym)
        self.path.cubicTo(x, ym - oy, xm - ox, y, xm, y)
        self.path.cubicTo(xm + ox, y, xe, ym - oy, xe, ym)
        self.path.cubicTo(xe, ym + oy, xm + ox, ye, xm, ye)
        self.path.cubicTo(xm - ox, ye, x, ym + oy, x, ym)

        self.render()

    def circle(self, x, y, d):
        self.path.addCircle(x, y, d/2)
        self.render()

import numpy as np
import skia
from dataclasses import dataclass

from p5 import p5
from p5.core.attribs import stroke, fill
from p5.core.color import Color
from p5.core import constants
from p5.core.primitives import point, line
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
    ellipse_mode = constants.CENTER
    rect_mode = constants.CORNER
    color_parse_mode = "RGB"
    color_range = (255, 255, 255, 255)

    stroke_cap = skia.Paint.kRound_Cap
    stroke_join = skia.Paint.kMiter_Join

    def set_stroke_cap(self, c):
        if c == constants.ROUND:
            self.stroke_cap = skia.Paint.kRound_Cap
        elif c == constants.SQUARE:
            self.stroke_cap = skia.Paint.kButt_Cap
        elif c == constants.PROJECT:
            self.stroke_cap = skia.Paint.kSquare_Cap

    def set_stroke_join(self, j):
        if j == constants.ROUND:
            self.stroke_join = skia.Paint.kRound_Join
        elif j == constants.MITER:
            self.stroke_join = skia.Paint.kMiter_Join
        elif j == constants.BEVEL:
            self.stroke_join = skia.Paint.kBevel_Join


class SkiaRenderer:
    def __init__(self):
        self.canvas = None
        self.paint = None
        self.style = Style2D()
        self.style_stack = []
        self.path = None
        self.font = skia.Font()
        self.typeface = skia.Typeface.MakeDefault()
        self.font.setTypeface(self.typeface)
        # TODO: Implement curve tightness from curves.py
        #  use curve_tightness from the renderer instance or style object instead of global variable
        self.curve_tightness = 0

    # Transforms functions
    def push_matrix(self):
        self.canvas.save()

    def pop_matrix(self):
        self.canvas.restore()

    def rotate(self, theta):
        # angles are always in radians in p5py
        # TODO: add angle mode
        self.canvas.rotate(theta * 180 / PI)

    def translate(self, x, y, z):
        self.canvas.translate(x, y)

    def scale(self, x, y=None, z=None):
        if not y:
            y = x
        self.canvas.scale(x, y)

    def shear_x(self, theta):
        self.apply_matrix(np.array([1, tan(theta), 0, 0, 1, 0, 0, 0, 1]).reshape(3, 3))

    def shear_y(self, theta):
        self.apply_matrix(np.array([1, 0, 0, tan(theta), 1, 0, 0, 0, 1]).reshape(3, 3))

    def apply_matrix(self, transform_matrix):
        if transform_matrix.shape != (3, 3):
            raise ValueError(
                "Expected a (3,3) shaped matrix instead received",
                transform_matrix.shape,
            )
        curr = np.array([*self.canvas.getTotalMatrix()]).reshape(3, 3)
        self.canvas.setMatrix(skia.Matrix(np.matmul(curr, transform_matrix)))

    def reset_matrix(self):
        self.canvas.resetMatrix()

    # Rendering functions
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
            "dy": round(sin(start + size), 7),
        }

    def initialize_renderer(self, canvas, paint, path):
        self.canvas = canvas
        self.paint = paint
        self.path = path

        self.clear()

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
        # Our screen will go black or all the pixels would be transparent
        self.canvas.clear(skia.Color(0, 0, 0, 0))

    def background(self, *args, **kwargs):
        # TODO: Add if args == pImage check
        # TODO: Add blend mode logic later
        self.push_matrix()
        self.reset_matrix()

        curr_fill = self.style.fill_color
        curr_fill_enabled = self.style.fill_enabled
        curr_stroke_enabled = self.style.stroke_enabled

        self.style.fill_enabled = True
        self.style.stroke_enabled = False
        self.style.fill_color = Color(*args, **kwargs).normalized
        self.rect(0, 0, *p5.sketch.size)
        self.style.fill_color = curr_fill
        self.style.fill_enabled = curr_fill_enabled
        self.style.stroke_enabled = curr_stroke_enabled

        self.pop_matrix()

    def render(self, fill=True, stroke=True, rewind=True):
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
            self.paint.setStrokeCap(self.style.stroke_cap)
            self.paint.setStrokeJoin(self.style.stroke_join)
            self.paint.setStyle(skia.Paint.kStroke_Style)
            self.paint.setColor(skia.Color4f(*self.style.stroke_color))
            self.paint.setStrokeWidth(self.style.stroke_weight)
            self.canvas.drawPath(self.path, self.paint)

        if rewind:
            self.path.rewind()

    def reset(self):
        self.reset_matrix()
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
                    self.path.moveTo(x + curve["ax"] * rx, y + curve["ay"] * ry)
                self.path.cubicTo(
                    x + curve["bx"] * rx,
                    y + curve["by"] * ry,
                    x + curve["cx"] * rx,
                    y + curve["cy"] * ry,
                    x + curve["dx"] * rx,
                    y + curve["dy"] * ry,
                )
            if mode == constants.PIE or not mode:
                self.path.lineTo(x, y)

            self.path.close()
            self.render(fill=True, stroke=False)

        if self.style.stroke_enabled:
            for index, curve in enumerate(curves, 0):
                if index == 0:
                    self.path.moveTo(x + curve["ax"] * rx, y + curve["ay"] * ry)
                self.path.cubicTo(
                    x + curve["bx"] * rx,
                    y + curve["by"] * ry,
                    x + curve["cx"] * rx,
                    y + curve["cy"] * ry,
                    x + curve["dx"] * rx,
                    y + curve["dy"] * ry,
                )
            if mode == constants.PIE:
                self.path.lineTo(x, y)
                self.path.close()
            elif mode == constants.CHORD:
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
        self.path.addCircle(x, y, d / 2)
        self.render()

    def point(self, x, y):
        s = self.style.stroke_color
        f = self.style.fill_color
        fe = self.style.fill_enabled

        # configure the settings beforehand we render
        # We draw an arc, and fill it to simulate a point
        self.style.fill_color = s
        self.style.fill_enabled = True
        self.style.stroke_enabled = False

        # This will render the point
        self.circle(x, y, self.style.stroke_weight)

        self.style.fill_color = f
        self.style.fill_enabled = fe
        self.style.stroke_enabled = True

    def quad(self, x1, y1, x2, y2, x3, y3, x4, y4):
        self.path.moveTo(x1, y1)
        self.path.lineTo(x2, y2)
        self.path.lineTo(x3, y3)
        self.path.lineTo(x4, y4)
        self.path.close()
        self.render()

    def rect(self, *args):
        x, y, w, h = args[:4]
        args = args[4:]
        tl = args[0] if len(args) >= 1 else None
        tr = args[1] if len(args) >= 2 else None
        br = args[2] if len(args) >= 3 else None
        bl = args[3] if len(args) >= 4 else None

        if tl is None:
            self.path.moveTo(x, y)
            self.path.lineTo(x + w, y)
            self.path.lineTo(x + w, y + h)
            self.path.lineTo(x, y + h)
            self.path.close()
            self.render()
            return

        if tr is None:
            tr = tl
        if br is None:
            br = tr
        if bl is None:
            bl = br

        absW = abs(w)
        absH = abs(h)
        hw = absW / 2
        hh = absH / 2
        if absW < 2 * tl:
            tl = hw
        if absH < 2 * tl:
            tl = hh
        if absW < 2 * tr:
            tr = hw
        if absH < 2 * tr:
            tr = hh
        if absW < 2 * br:
            br = hw
        if absH < 2 * br:
            br = hh
        if absW < 2 * bl:
            bl = hw
        if absH < 2 * bl:
            bl = hh

        self.path.moveTo(x + tl, y)
        self.path.arcTo(x + w, y, x + w, y + h, tr)
        self.path.arcTo(x + w, y + h, x, y + h, br)
        self.path.arcTo(x, y + h, x, y, bl)
        self.path.arcTo(x, y, x + w, y, tl)
        self.path.close()

        self.render()

    def triangle(self, *args):
        x1, y1, x2, y2, x3, y3 = args
        self.path.moveTo(x1, y1)
        self.path.lineTo(x2, y2)
        self.path.lineTo(x3, y3)
        self.path.close()

        self.render()

    def _do_fill_stroke_close(self, close_shape):
        if close_shape:
            self.path.close()
        self.render()

    def end_shape(
        self, mode, vertices, is_curve, is_bezier, is_quadratic, is_contour, shape_kind
    ):

        close_shape = mode == constants.CLOSE
        # NOT APPENDING AGAIN
        num_verts = len(vertices)
        if is_curve and shape_kind is None:
            if num_verts > 3:
                s = 1 - self.curve_tightness
                self.path.moveTo(vertices[1][0], vertices[1][1])
                for i in range(1, num_verts - 2):
                    b = []
                    v = vertices[i]
                    # logic for curve tightness is borrowed from
                    # https://github.com/processing/p5.js/blob/9cd186349cdb55c5faf28befff9c0d4a390e02ed/src/core/p5.Renderer2D.js#L767
                    b.append([v[0], v[1]])
                    b.append(
                        [
                            v[0]
                            + (s * vertices[i + 1][0] - s * vertices[i - 1][0]) / 6,
                            v[1]
                            + (s * vertices[i + 1][1] - s * vertices[i - 1][1]) / 6,
                        ]
                    )
                    b.append(
                        [
                            vertices[i + 1][0]
                            + (s * vertices[i][0] - s * vertices[i + 2][0]) / 6,
                            vertices[i + 1][1]
                            + (s * vertices[i][1] - s * vertices[i + 2][1]) / 6,
                        ]
                    )
                    b.append([vertices[i + 1][0], vertices[i + 1][1]])
                    self.path.cubicTo(
                        b[1][0], b[1][1], b[2][0], b[2][1], b[3][0], b[3][1]
                    )
                if close_shape:
                    self.path.lineTo(vertices[i + 1][0], vertices[i + 1][1])
                self._do_fill_stroke_close(close_shape)
        elif is_bezier and shape_kind is None:
            for i in range(num_verts):
                if vertices[i][-1].get("is_vert", None):
                    if (
                        vertices[i][-1].get("move_to", None)
                        or self.path.countVerbs() == 0
                    ):
                        self.path.moveTo(vertices[i][0], vertices[i][1])
                    else:
                        self.path.lineTo(vertices[i][0], vertices[i][1])
                else:
                    self.path.cubicTo(
                        vertices[i][0],
                        vertices[i][1],
                        vertices[i][2],
                        vertices[i][3],
                        vertices[i][4],
                        vertices[i][5],
                    )
            self._do_fill_stroke_close(close_shape)

        elif is_quadratic and shape_kind is None:
            for i in range(num_verts):
                if vertices[i][-1].get("is_vert", None):
                    if (
                        vertices[i][-1].get("move_to", None)
                        or self.path.countVerbs() == 0
                    ):
                        self.path.moveTo(vertices[i][0], vertices[i][1])
                    else:
                        self.path.lineTo(vertices[i][0], vertices[i][1])
                else:
                    self.path.quadTo(
                        vertices[i][0], vertices[i][1], vertices[i][2], vertices[i][3]
                    )
            self._do_fill_stroke_close(close_shape)
        else:
            if shape_kind == constants.POINTS:
                for i in range(num_verts):
                    v = vertices[i]
                    if self.style.stroke_enabled:
                        stroke(*v[6])
                    point(v[0], v[1])
            elif shape_kind == constants.LINES:
                for i in range(0, num_verts - 1, 2):
                    v = vertices[i]
                    if self.style.stroke_enabled:
                        stroke(*vertices[i + 1][6])
                    line(v[0], v[1], vertices[i + 1][0], vertices[i + 1][1])
            elif shape_kind == constants.TRIANGLES:
                for i in range(0, num_verts - 2, 3):
                    v = vertices[i]
                    self.path.moveTo(v[0], v[1])
                    self.path.lineTo(vertices[i + 1][0], vertices[i + 1][1])
                    self.path.lineTo(vertices[i + 2][0], vertices[i + 2][1])
                    self.path.close()
                    if self.style.fill_enabled:
                        fill(*vertices[i + 2][5])
                        self.render(fill=True, stroke=False, rewind=False)
                    if self.style.stroke_enabled:
                        stroke(*vertices[i + 2][6])
                        self.render(fill=False, stroke=True, rewind=True)
            elif shape_kind == constants.TRIANGLE_STRIP:
                for i in range(num_verts - 1):
                    v = vertices[i]
                    self.path.moveTo(vertices[i + 1][0], vertices[i + 1][1])
                    self.path.lineTo(v[0], v[1])
                    if self.style.stroke_enabled:
                        stroke(*vertices[i + 1][6])
                    if self.style.fill_enabled:
                        fill(*vertices[i + 1][5])
                    if i + 2 < num_verts:
                        self.path.lineTo(vertices[i + 2][0], vertices[i + 2][1])
                        if self.style.stroke_enabled:
                            stroke(*vertices[i + 2][6])
                        if self.style.fill_enabled:
                            fill(*vertices[i + 2][5])
                    self._do_fill_stroke_close(close_shape)
            elif shape_kind == constants.TRIANGLE_FAN:
                if num_verts > 2:
                    for i in range(2, num_verts):
                        v = vertices[i]
                        self.path.moveTo(vertices[0][0], vertices[0][1])
                        self.path.lineTo(vertices[i - 1][0], vertices[i - 1][1])
                        self.path.lineTo(v[0], v[1])
                        self.path.lineTo(vertices[0][0], vertices[0][1])

                        if i < num_verts - 1:
                            if (
                                self.style.fill_enabled and v[5] != vertices[i + 1][5]
                            ) or (
                                self.style.stroke_enabled and v[6] != vertices[i + 1][6]
                            ):
                                if self.style.fill_enabled:
                                    fill(*v[5])
                                    self.render(fill=True, stroke=False, rewind=False)
                                    fill(*vertices[i + 1][5])
                                if self.style.stroke_enabled:
                                    stroke(*v[6])
                                    self.render(fill=False, stroke=True, rewind=True)
                                    stroke(*vertices[i + 1][6])
                                self.path.close()
                                self.path.rewind()
                    self._do_fill_stroke_close(close_shape)
            elif shape_kind == constants.QUADS:
                for i in range(0, num_verts - 3, 4):
                    v = vertices[i]
                    self.path.moveTo(v[0], v[1])
                    for j in range(1, 4):
                        self.path.lineTo(vertices[i + j][0], vertices[i + j][1])
                    self.path.lineTo(v[0], v[1])
                    if self.style.fill_enabled:
                        fill(*vertices[i + 3][5])
                    if self.style.stroke_enabled:
                        stroke(*vertices[i + 3][6])
                    self._do_fill_stroke_close(close_shape)
            elif shape_kind == constants.QUAD_STRIP:
                if num_verts > 3:
                    for i in range(0, num_verts - 1, 2):
                        v = vertices[i]
                        if i + 3 < num_verts:
                            self.path.moveTo(vertices[i + 2][0], vertices[i + 2][1])
                            self.path.lineTo(v[0], v[1])
                            self.path.lineTo(vertices[i + 1][0], vertices[i + 1][1])
                            self.path.lineTo(vertices[i + 3][0], vertices[i + 3][1])
                            if self.style.fill_enabled:
                                fill(*vertices[i + 3][5])
                            if self.style.stroke_enabled:
                                stroke(*vertices[i + 3][6])
                        else:
                            self.path.moveTo(v[0], v[1])
                            self.path.lineTo(vertices[i + 1][0], vertices[i + 1][1])
                        self._do_fill_stroke_close(close_shape)
            else:
                self.path.moveTo(vertices[0][0], vertices[0][1])
                for i in range(1, num_verts):
                    v = vertices[i]
                    if v[-1].get("is_vert", None):
                        if v[-1].get("move_to", None) or self.path.countVerbs() == 0:
                            self.path.moveTo(v[0], v[1])
                        else:
                            self.path.lineTo(v[0], v[1])
                self._do_fill_stroke_close(close_shape)

    # Fonts functions

    # Images functions

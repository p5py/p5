import contextlib, glfw, skia
import dataclasses
from OpenGL import GL

from p5 import p5


class StyleClass():
    def __init__(self):
        self.style_stack = []
        self.isFill = True
        self.isStroke = False
        self.stroke_weight = 3
        self.fill_color = skia.ColorBLACK
        self.stroke_color = skia.ColorBLACK
        # other properties


class SkiaRenderer():
    def __init__(self):
        self.canvas = None
        self.paint = None
        self.style = StyleClass()
        self.path = None
        self.font = skia.Font()
        self.typeface = skia.Typeface.MakeDefault()
        self.font.setTypeface(self.typeface)

    def initialize_renderer(self, canvas, paint, path):
        self.canvas = canvas
        self.paint = paint
        self.path = path
        self.canvas.clear(skia.ColorWHITE)

    def render_rectangle(self, x, y, w, h):
        # print("called rectangel")
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
        if self.style.isFill:
            self.paint.setStyle(skia.Paint.kFill_Style)
            self.paint.setColor(self.style.fill_color)
            self.canvas.drawPath(self.path, self.paint)

        if self.style.isStroke:
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
        self.canvas.clear(skia.ColorWHITE)

    def render(self, rewind=True):
        """
        Draw the path on current canvas using paint
        """
        # print(self.path.countVerbs())
        # print(self.canvas)
        # print("RENDER NOW")
        if self.style.isFill:
            self.paint.setStyle(skia.Paint.kFill_Style)
            self.paint.setColor(self.style.fill_color)
            self.canvas.drawPath(self.path, self.paint)

        if self.style.isStroke:
            self.paint.setStyle(skia.Paint.kStroke_Style)
            self.paint.setColor(self.style.stroke_color)
            self.paint.setStrokeWidth(self.style.stroke_weight)
            self.canvas.drawPath(self.path, self.paint)

        if rewind and p5.sketch.resized:
            # print("REWINDED")
            self.path.rewind()

        # Reset the font size back to default size
        self.reset()

    def reset(self):
        self.font.setSize(15)

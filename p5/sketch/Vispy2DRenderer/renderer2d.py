#
# Part of p5: A Python package based on Processing
# Copyright (C) 2017-2019 Abhik Pal
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

import builtins
import io
import math
import re
import textwrap
import urllib
from contextlib import contextmanager

import numpy as np
from PIL import ImageFont, ImageChops, ImageFilter, ImageDraw, Image
from vispy import gloo
from vispy.gloo import Program
from vispy.gloo import Texture2D
from vispy.gloo import VertexBuffer

from p5.core import p5
from p5.core.constants import (
    SType,
    LEFT,
    TOP,
    RIGHT,
    BOTTOM,
    CENTER,
    CORNERS,
    CORNER,
    RGB,
)
from p5.core.image import image, image_mode
from p5.core.structure import push_style
from p5.pmath import matrix
from .image import VispyPImage
from .openglrenderer import OpenGLRenderer, get_render_primitives, COLOR_WHITE
from .shaders2d import src_default, src_fbuffer
from .shaders2d import src_line
from .shaders2d import src_texture
from .shape import PShape, Arc


class VispyRenderer2D(OpenGLRenderer):
    def __init__(self):
        super().__init__(src_fbuffer, src_default)
        self.texture_prog = Program(src_texture.vert, src_texture.frag)
        self.texture_prog["texcoord"] = self.fbuf_texcoords
        self.line_prog = None
        self.modelview_matrix = np.identity(4)

    def reset_view(self):
        self.viewport = (
            0,
            0,
            int(builtins.width * builtins.pixel_x_density),
            int(builtins.height * builtins.pixel_y_density),
        )
        self.texture_viewport = (
            0,
            0,
            builtins.width,
            builtins.height,
        )

        gloo.set_viewport(*self.viewport)  # pylint: disable=no-member

        cz = (builtins.height / 2) / math.tan(math.radians(30))
        self.projection_matrix = matrix.perspective_matrix(
            math.radians(60), builtins.width / builtins.height, 0.1 * cz, 10 * cz
        )
        self.modelview_matrix = matrix.translation_matrix(
            -builtins.width / 2, builtins.height / 2, -cz
        )
        self.modelview_matrix = self.modelview_matrix.dot(
            matrix.scale_transform(1, -1, 1)
        )

        self.transform_matrix = np.identity(4)

        self.default_prog["modelview"] = self.modelview_matrix.T.flatten()
        self.default_prog["projection"] = self.projection_matrix.T.flatten()

        self.texture_prog["modelview"] = self.modelview_matrix.T.flatten()
        self.texture_prog["projection"] = self.projection_matrix.T.flatten()

        self.line_prog = Program(src_line.vert, src_line.frag)

        self.line_prog["modelview"] = self.modelview_matrix.T.flatten()
        self.line_prog["projection"] = self.projection_matrix.T.flatten()
        self.line_prog["height"] = builtins.height

        self.fbuffer_tex_front = Texture2D((builtins.height, builtins.width, 3))
        self.fbuffer_tex_back = Texture2D((builtins.height, builtins.width, 3))

        for buf in [self.fbuffer_tex_front, self.fbuffer_tex_back]:
            self.fbuffer.color_buffer = buf
            with self.fbuffer:
                self.clear()

    def clear(self, color=True, depth=True):
        """Clear the renderer background."""
        gloo.set_state(  # pylint: disable=no-member
            clear_color=self.style.background_color
        )
        gloo.clear(color=color, depth=depth)  # pylint: disable=no-member

    def _comm_toggles(self, state=True):
        gloo.set_state(blend=state)  # pylint: disable=no-member
        gloo.set_state(depth_test=state)  # pylint: disable=no-member

        if state:
            gloo.set_state(  # pylint: disable=no-member
                blend_func=("src_alpha", "one_minus_src_alpha")
            )
            gloo.set_state(depth_func="lequal")  # pylint: disable=no-member

    @contextmanager
    def draw_loop(self):
        """The main draw loop context manager."""

        self.transform_matrix = np.identity(4)

        self.default_prog["modelview"] = self.modelview_matrix.T.flatten()
        self.default_prog["projection"] = self.projection_matrix.T.flatten()

        self.fbuffer.color_buffer = self.fbuffer_tex_back

        with self.fbuffer:
            gloo.set_viewport(*self.texture_viewport)  # pylint: disable=no-member
            self._comm_toggles()
            self.fbuffer_prog["texture"] = self.fbuffer_tex_front
            self.fbuffer_prog.draw("triangle_strip")

            yield

            self.flush_geometry()
            self.transform_matrix = np.identity(4)

        gloo.set_viewport(*self.viewport)  # pylint: disable=no-member
        self._comm_toggles(False)
        self.clear()
        self.fbuffer_prog["texture"] = self.fbuffer_tex_back
        self.fbuffer_prog.draw("triangle_strip")

        self.fbuffer_tex_front, self.fbuffer_tex_back = (
            self.fbuffer_tex_back,
            self.fbuffer_tex_front,
        )

    def _add_to_draw_queue(
        self, stype, vertices, idx, fill, stroke, stroke_weight, stroke_cap, stroke_join
    ):
        """Adds shape of stype to draw queue"""
        if stype == "lines":
            self.draw_queue.append(
                (stype, (vertices, idx, stroke, stroke_weight, stroke_cap, stroke_join))
            )
        else:
            self.draw_queue.append((stype, (vertices, idx, fill)))

    def render(self, shape):
        fill = shape.fill.normalized if shape.fill else None
        stroke = shape.stroke.normalized if shape.stroke else None
        stroke_weight = shape.stroke_weight
        stroke_cap = shape.stroke_cap
        stroke_join = shape.stroke_join

        obj_list = get_render_primitives(shape)
        for obj in obj_list:
            stype, vertices, idx = obj
            # Convert 2D vertices to 3D by adding "0" column, needed for further transformations
            if len(vertices[0]) == 2:
                vertices = np.hstack([vertices, np.zeros((len(vertices), 1))])
            # Transform vertices
            vertices = self._transform_vertices(
                np.hstack([vertices, np.ones((len(vertices), 1))]),
                shape._matrix,
                self.transform_matrix,
            )
            # Add to draw queue
            self._add_to_draw_queue(
                stype,
                vertices,
                idx,
                fill,
                stroke,
                stroke_weight,
                stroke_cap,
                stroke_join,
            )

    def flush_geometry(self):
        """Flush all the shape geometry from the draw queue to the GPU."""
        current_queue = []
        for index, shape in enumerate(self.draw_queue):
            current_shape = self.draw_queue[index][0]
            current_queue.append(self.draw_queue[index][1])

            if current_shape == "lines":
                self.render_line(current_queue)
            else:
                self.render_default(current_shape, current_queue)

            current_queue = []

        self.draw_queue = []

    def render_line(self, queue):
        """
        This rendering algorithm works by tesselating the line into
        multiple triangles.

        Reference: https://blog.mapbox.com/drawing-antialiased-lines-with-opengl-8766f34192dc
        """

        if len(queue) == 0:
            return

        pos = []
        posPrev = []
        posCurr = []
        posNext = []
        markers = []
        side = []

        linewidth = []
        join_type = []
        cap_type = []
        color = []

        stroke_cap_codes = {"PROJECT": 0, "SQUARE": 1, "ROUND": 2}

        stroke_join_codes = {"MITER": 0, "BEVEL": 1, "ROUND": 2}

        for line in queue:
            if len(line[1]) == 0:
                continue

            for segment in line[1]:
                for i in range(
                    len(segment) - 1
                ):  # the data is sent to renderer in line segments
                    for j in [0, 0, 1, 0, 1, 1]:  # all the vertices of triangles
                        if i + j - 1 >= 0:
                            posPrev.append(line[0][segment[i + j - 1]])
                        else:
                            posPrev.append(line[0][segment[i + j]])

                        if i + j + 1 < len(segment):
                            posNext.append(line[0][segment[i + j + 1]])
                        else:
                            posNext.append(line[0][segment[i + j]])

                        posCurr.append(line[0][segment[i + j]])

                    # Is the vertex up/below the line segment
                    markers.extend([1.0, -1.0, -1.0, -1.0, 1.0, -1.0])
                    # Left or right side of the segment
                    side.extend([1.0, 1.0, -1.0, 1.0, -1.0, -1.0])
                    # Left vertex of each segment
                    pos.extend([line[0][segment[i]]] * 6)
                    linewidth.extend([line[3]] * 6)
                    join_type.extend([stroke_join_codes[line[5]]] * 6)
                    cap_type.extend([stroke_cap_codes[line[4]]] * 6)
                    color.extend([line[2]] * 6)

        if len(pos) == 0:
            return

        posPrev = np.array(posPrev, np.float32)
        posCurr = np.array(posCurr, np.float32)
        posNext = np.array(posNext, np.float32)
        markers = np.array(markers, np.float32)
        side = np.array(side, np.float32)
        pos = np.array(pos, np.float32)
        linewidth = np.array(linewidth, np.float32)
        join_type = np.array(join_type, np.float32)
        cap_type = np.array(cap_type, np.float32)
        color = np.array(color, np.float32)

        self.line_prog["pos"] = gloo.VertexBuffer(pos)
        self.line_prog["posPrev"] = gloo.VertexBuffer(posPrev)
        self.line_prog["posCurr"] = gloo.VertexBuffer(posCurr)
        self.line_prog["posNext"] = gloo.VertexBuffer(posNext)
        self.line_prog["marker"] = gloo.VertexBuffer(markers)
        self.line_prog["side"] = gloo.VertexBuffer(side)
        self.line_prog["linewidth"] = gloo.VertexBuffer(linewidth)
        self.line_prog["join_type"] = gloo.VertexBuffer(join_type)
        self.line_prog["cap_type"] = gloo.VertexBuffer(cap_type)
        self.line_prog["color"] = gloo.VertexBuffer(color)

        self.line_prog.draw("triangles")

    def render_image(self, image, location, size):
        """Render the image.

        :param image: image to be rendered
        :type image: builtins.Image

        :param location: top-left corner of the image
        :type location: tuple | list | builtins.Vector

        :param size: target size of the image to draw.
        :type size: tuple | list | builtins.Vector
        """
        self.flush_geometry()

        self.texture_prog["fill_color"] = (
            self.style.tint_color if self.style.tint_enabled else COLOR_WHITE
        )
        self.texture_prog["transform"] = self.transform_matrix.T.flatten()

        x, y = location
        sx, sy = size
        imx, imy = image.size
        data = np.zeros(
            4, dtype=[("position", np.float32, 2), ("texcoord", np.float32, 2)]
        )
        data["texcoord"] = np.array(
            [[0.0, 1.0], [1.0, 1.0], [0.0, 0.0], [1.0, 0.0]], dtype=np.float32
        )
        data["position"] = np.array(
            [[x, y + sy], [x + sx, y + sy], [x, y], [x + sx, y]], dtype=np.float32
        )

        self.texture_prog["texture"] = image._texture
        self.texture_prog.bind(VertexBuffer(data))
        self.texture_prog.draw("triangle_strip")

    def cleanup(self):
        """Run the clean-up routine for the renderer.

        This method is called when all drawing has been completed and the
        program is about to exit.

        """
        OpenGLRenderer.cleanup(self)
        self.line_prog.delete()

    def render_shape(self, shape):
        self.render(shape)
        for child_shape in shape.children:
            self.render_shape(child_shape)

    def line(self, *args):
        path = args[0]
        self.render_shape(PShape(vertices=path, shape_type=SType.LINES))

    def bezier(self, *args):
        vertices = args[0]
        self.render_shape(PShape(vertices=vertices, shape_type=SType.LINE_STRIP))

    def curve(self, *args):
        vertices = args[0]
        self.render_shape(PShape(vertices=vertices, shape_type=SType.LINE_STRIP))

    def triangle(self, *args):
        path = args[0]
        self.render_shape(PShape(vertices=path, shape_type=SType.TRIANGLES))

    def quad(self, *args):
        path = args[0]
        self.render_shape(PShape(vertices=path, shape_type=SType.QUADS))

    def arc(self, *args):
        center = args[0]
        dim = args[1]
        start_angle = args[2]
        stop_angle = args[3]
        mode = args[4]

        self.render_shape(Arc(center, dim, start_angle, stop_angle, mode))

    def shape(self, vertices, contours, shape_type, *args):
        """Render a Pshape"""
        self.render_shape(
            PShape(vertices=vertices, contours=contours, shape_type=shape_type)
        )

    def create_font(self, name, size=10):
        """Create the given font at the appropriate size.

        :param name: Filename of the font file (only pil, otf and ttf
            fonts are supported.)
        :type name: str

        :param size: Font size (only required when `name` refers to a
            truetype font; defaults to None)
        :type size: int | None

        """

        if name.endswith("ttf") or name.endswith("otf"):
            font = ImageFont.truetype(name, size)
        elif name.endswith("pil"):
            font = ImageFont.load(name)
        else:
            raise NotImplementedError("Font type not supported.")
        return font

    def load_font(self, font_name):
        """Loads the given font into a font object"""
        return self.create_font(font_name)

    def text(self, text_string, position, wrap_at):

        multiline = False
        if not (wrap_at is None):
            text_string = textwrap.fill(text_string, wrap_at)
            size = self.style.font_family.getsize_multiline(text_string)
            multiline = True
        elif "\n" in text_string:
            multiline = True
            size = list(self.style.font_family.getsize_multiline(text_string))
            size[1] += self.style.text_leading * text_string.count("\n")
        else:
            size = self.style.font_family.getsize(text_string)

        is_stroke_valid = False  # True when stroke_weight != 0
        is_min_filter = False  # True when stroke_weight <0
        if self.style.stroke_enabled:
            stroke_weight = self.style.stroke_weight
            if stroke_weight < 0:
                stroke_weight = abs(stroke_weight)
                is_min_filter = True

            if stroke_weight > 0:
                if stroke_weight % 2 == 0:
                    stroke_weight += 1
                is_stroke_valid = True

        if is_stroke_valid:
            new_size = list(map(lambda x: x + 2 * stroke_weight, size))
            is_stroke_valid = True
            text_xy = (stroke_weight, stroke_weight)
        else:
            new_size = size
            text_xy = (0, 0)

        canvas = Image.new("RGBA", new_size, color=(0, 0, 0, 0))
        canvas_draw = ImageDraw.Draw(canvas)

        if multiline:
            canvas_draw.multiline_text(
                text_xy,
                text_string,
                font=self.style.font_family,
                spacing=self.style.text_leading,
            )
        else:
            canvas_draw.text(text_xy, text_string, font=self.style.font_family)

        text_image = VispyPImage(*new_size)
        text_image._img = canvas

        if is_stroke_valid:
            if is_min_filter:
                canvas_dilate = canvas.filter(ImageFilter.MinFilter(stroke_weight))
            else:
                canvas_dilate = canvas.filter(ImageFilter.MaxFilter(stroke_weight))
            canvas_stroke = ImageChops.difference(canvas, canvas_dilate)
            text_stroke_image = VispyPImage(*new_size)
            text_stroke_image._img = canvas_stroke

        width, height = new_size
        position = list(position)
        if self.style.text_align_x == LEFT:
            position[0] += 0
        elif self.style.text_align_x == RIGHT:
            position[0] -= width
        elif self.style.text_align_x == CENTER:
            position[0] -= width / 2

        if self.style.text_align_y == TOP:
            position[1] += 0
        elif self.style.text_align_y == BOTTOM:
            position[1] -= height
        elif self.style.text_align_y == CENTER:
            position[1] -= height / 2

        with push_style():
            if self.style.fill_enabled:
                self.style.tint_enabled = True
                self.style.tint_color = self.style.fill_color
                image(text_image, *position)
            if self.style.stroke_enabled and is_stroke_valid:
                self.style.tint_enabled = True
                self.style.tint_color = self.style.stroke_color
                image(text_stroke_image, *position)

        return text_string

    def text_font(self, font, size):
        self.style.font_family = font
        if size:
            self.text_size(size)

    def text_size(self, size):
        if hasattr(self.style.font_family, "path"):
            if self.style.font_family.path.endswith(
                "ttf"
            ) or self.style.font_family.path.endswith("otf"):
                self.style.font_family = ImageFont.truetype(
                    self.style.font_family.path, size
                )
        else:
            raise ValueError("text_size is not supported for Bitmap Fonts")

    def text_width(self, text):
        return self.style.font_family.getsize(text)[0]

    def text_ascent(self):
        ascent, descent = self.style.font_family.getmetrics()
        return ascent

    def text_descent(self):
        ascent, descent = self.style.font_family.getmetrics()
        return descent

    def text_style(self):
        raise NotImplementedError("Not Implemented in Vispy")

    def text_wrap(self, text_wrap_style):
        raise NotImplementedError("Not Implemented in Vispy")

    def image(self, img, x, y, w, h):

        location = (x, y)
        if w is None:
            w = img.size[0]
        if h is None:
            h = img.size[1]

        size = (w, h)
        # Add else statement below to resize the img._img first,
        #   or it will take much time to render large image,
        #   even when small size is specified to the image
        if size != img.size:
            img.size = size

        lx, ly = location
        sx, sy = size

        if self.style.image_mode == CENTER:
            lx = int(lx - (sx / 2))
            ly = int(ly - (sy / 2))

        if self.style.image_mode == CORNERS:
            sx = sx - lx
            sy = sy - ly

        self.render_image(img, (lx, ly), (sx, sy))

    def load_image(self, filename):
        if re.match(r"\w+://", filename):
            with urllib.request.urlopen(filename) as url:
                f = io.BytesIO(url.read())
                img = Image.open(f)
        else:
            img = Image.open(filename)
        w, h = img.size
        pimg = VispyPImage(w, h)
        pimg._img = img
        return pimg

    def load_pixels(self):
        pixels = VispyPImage(builtins.width, builtins.height, RGB)
        # sketch.renderer.flush_geometry()
        pixel_data = self.fbuffer.read(mode="color", alpha=False)

        pixels._img = Image.fromarray(pixel_data)
        builtins.pixels = pixels

        pixels._load()

    def update_pixels(self):
        with push_style():
            image_mode(CORNER)
            self.style.tint_enabled = False
            image(builtins.pixels, *(0, 0))

        builtins.pixels = None

    def save_canvas(self, filename, canvas):
        if filename:
            p5.sketch.screenshot(filename)
        else:
            p5.sketch.screenshot("Screen.png")

    def create_graphics(self, width, height, renderer):
        raise NotImplementedError(
            "Vispy Renderer does not support offscreen buffers yet, use 'skia' as your backend renderer"
        )

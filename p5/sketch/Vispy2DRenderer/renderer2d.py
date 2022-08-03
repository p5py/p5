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

import numpy as np
import math
from p5.pmath import matrix
from .shaders2d import src_default, src_fbuffer

import builtins

from vispy import gloo
from vispy.gloo import Program
from vispy.gloo import Texture2D
from vispy.gloo import VertexBuffer

from contextlib import contextmanager
from .shaders2d import src_texture
from .shaders2d import src_line
from .openglrenderer import OpenGLRenderer, get_render_primitives, COLOR_WHITE
from .shape import PShape, Arc
from p5.core.constants import SType


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

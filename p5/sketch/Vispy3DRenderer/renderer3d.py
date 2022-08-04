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

from numpy.linalg import inv
from dataclasses import dataclass
from sys import stderr
import numpy as np
import math

import builtins

from vispy import gloo
from vispy.gloo import Texture2D, Program

from contextlib import contextmanager

from p5.core.constants import Z_EPSILON
from p5.core.geometry import Geometry
from ..Vispy2DRenderer.shape import PShape
from ..Vispy2DRenderer.openglrenderer import Style2D

from p5.pmath.matrix import translation_matrix
from p5.pmath import matrix
from ..Vispy2DRenderer.openglrenderer import (
    OpenGLRenderer,
    get_render_primitives,
    to_3x3,
    COLOR_WHITE,
)
from .shaders3d import src_default, src_fbuffer, src_normal, src_phong
from p5.core.material import BasicMaterial, NormalMaterial, BlinnPhongMaterial

from p5.core import p5


class GlslList:
    """List of objects to be used in glsl"""

    def __init__(self, max_size, obj_size, dtype):
        """Initialize GlslList
        max_size: The maximum size of the list
        obj_size: The length of an individual object
        dtype: The data type of this list
        """
        list_shape = (max_size, obj_size)
        self.data = np.zeros(list_shape, dtype=dtype)
        self.size = 0
        self.max_size = max_size

    def add(self, obj):
        if self.size == self.max_size:
            print(
                "Too many instances of {} are added. Max size {}.".format(
                    type(obj), self.max_size
                ),
                file=stderr,
            )
            return
        self.data[self.size] = obj
        self.size += 1

    def clear(self):
        self.data = np.zeros_like(self.data)
        self.size = 0


@dataclass
class Style3D(Style2D):
    ambient = np.array([0.2] * 3)
    diffuse = np.array([0.6] * 3)
    specular = np.array([0.8] * 3)
    shininess = 8
    material = BasicMaterial(COLOR_WHITE)


class Renderer3D(OpenGLRenderer):
    def __init__(self):
        super().__init__(src_fbuffer, src_default)
        self.style = Style3D()
        self.normal_prog = Program(src_normal.vert, src_normal.frag)
        self.phong_prog = Program(src_phong.vert, src_phong.frag)
        self.lookat_matrix = np.identity(4)

        # Camera position
        self.camera_pos = np.zeros(3)
        # Lights
        self.MAX_LIGHTS_PER_CATEGORY = 8
        self.ambient_light_color = GlslList(self.MAX_LIGHTS_PER_CATEGORY, 3, np.float32)
        self.directional_light_dir = GlslList(
            self.MAX_LIGHTS_PER_CATEGORY, 3, np.float32
        )
        self.directional_light_color = GlslList(
            self.MAX_LIGHTS_PER_CATEGORY, 3, np.float32
        )
        self.directional_light_specular = GlslList(
            self.MAX_LIGHTS_PER_CATEGORY, 3, np.float32
        )
        self.point_light_color = GlslList(self.MAX_LIGHTS_PER_CATEGORY, 3, np.float32)
        self.point_light_pos = GlslList(self.MAX_LIGHTS_PER_CATEGORY, 3, np.float32)
        self.point_light_specular = GlslList(
            self.MAX_LIGHTS_PER_CATEGORY, 3, np.float32
        )
        self.const_falloff = GlslList(self.MAX_LIGHTS_PER_CATEGORY, 1, np.float32)
        self.linear_falloff = GlslList(self.MAX_LIGHTS_PER_CATEGORY, 1, np.float32)
        self.quadratic_falloff = GlslList(self.MAX_LIGHTS_PER_CATEGORY, 1, np.float32)
        (
            self.curr_linear_falloff,
            self.curr_quadratic_falloff,
            self.curr_constant_falloff,
        ) = (0.0, 0.0, 0.0)
        self.light_specular = np.array([0.0] * 3)

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

        self.transform_matrix = np.identity(4)
        self._update_shader_transforms()

        self.fbuffer_tex_front = Texture2D((builtins.height, builtins.width, 3))
        self.fbuffer_tex_back = Texture2D((builtins.height, builtins.width, 3))
        self.fbuffer.depth_buffer = gloo.RenderBuffer((builtins.height, builtins.width))

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

    def clear_lights(self):
        self.ambient_light_color.clear()
        self.directional_light_color.clear()
        self.directional_light_dir.clear()
        self.directional_light_specular.clear()
        self.point_light_color.clear()
        self.point_light_pos.clear()
        self.point_light_specular.clear()
        self.const_falloff.clear()
        self.linear_falloff.clear()
        self.quadratic_falloff.clear()

    def _comm_toggles(self, state=True):
        gloo.set_state(blend=state)  # pylint: disable=no-member
        gloo.set_state(depth_test=state)  # pylint: disable=no-member

        if state:
            gloo.set_state(  # pylint: disable=no-member
                blend_func=("src_alpha", "one_minus_src_alpha")
            )
            gloo.set_state(depth_func="lequal")  # pylint: disable=no-member

    def _update_shader_transforms(self):
        # Default shader
        self.default_prog["projection"] = self.projection_matrix.T.flatten()
        self.default_prog["perspective_matrix"] = self.lookat_matrix.T.flatten()

        # Normal shader
        self.normal_prog["projection"] = self.projection_matrix.T.flatten()
        self.normal_prog["perspective"] = self.lookat_matrix.T.flatten()
        # This is a no-op, meaning that the normals stay in world space, which
        # matches the behavior in p5.js
        normal_transform = np.identity(3)
        # I think the transformation below takes the vertices to camera space, but
        # the results are funky, so it's probably incorrect? - ziyaointl, 2020/07/20
        # normal_transform = np.linalg.inv(self.projection_matrix[:3, :3] @ self.lookat_matrix[:3, :3])
        self.normal_prog["normal_transform"] = normal_transform.flatten()

        # Blinn-Phong Shader
        self.phong_prog["projection"] = self.projection_matrix.T.flatten()
        self.phong_prog["perspective"] = self.lookat_matrix.T.flatten()

    @contextmanager
    def draw_loop(self):
        """The main draw loop context manager."""

        self.transform_matrix = np.identity(4)
        self._update_shader_transforms()
        self.fbuffer.color_buffer = self.fbuffer_tex_back

        with self.fbuffer:
            gloo.set_viewport(*self.texture_viewport)  # pylint: disable=no-member
            self._comm_toggles()
            self.fbuffer_prog["texture"] = self.fbuffer_tex_front
            self.fbuffer_prog.draw("triangle_strip")
            self.clear(color=False, depth=True)
            self.clear_lights()

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

    def _add_to_draw_queue_simple(self, stype, vertices, idx, color):
        """Adds shape of stype to draw queue"""
        self.draw_queue.append((stype, (vertices, idx, color, None, None)))

    def tnormals(self, shape):
        """Obtain a list of vertex normals in world coordinates"""
        if isinstance(shape.material, BasicMaterial):  # Basic shader doesn't need this
            return None
        return shape.vertex_normals @ np.linalg.inv(
            to_3x3(self.transform_matrix) @ to_3x3(shape.matrix)
        )

    def render(self, shape):
        if isinstance(shape, Geometry):
            n = len(shape.vertices)
            # Perform model transform
            # TODO: Investigate moving model transform from CPU to the GPU
            tverts = self._transform_vertices(
                np.hstack([shape.vertices, np.ones((n, 1))]),
                shape.matrix,
                self.transform_matrix,
            )
            tnormals = self.tnormals(shape)

            edges = shape.edges
            faces = shape.faces

            self.add_to_draw_queue(
                "poly",
                tverts,
                edges,
                faces,
                self.style.fill_color,
                self.style.stroke_color,
                tnormals,
                self.style.material,
            )

        elif isinstance(shape, PShape):
            fill = shape.fill.normalized if shape.fill else None
            stroke = shape.stroke.normalized if shape.stroke else None

            obj_list = get_render_primitives(shape)
            for obj in obj_list:
                stype, vertices, idx = obj
                # Transform vertices
                vertices = self._transform_vertices(
                    np.hstack([vertices, np.ones((len(vertices), 1))]),
                    shape._matrix,
                    self.transform_matrix,
                )
                # Add to draw queue
                self._add_to_draw_queue_simple(
                    stype, vertices, idx, stroke if stype == "lines" else fill
                )

    def add_to_draw_queue(
        self,
        stype,
        vertices,
        edges,
        faces,
        fill=None,
        stroke=None,
        normals=None,
        material=None,
    ):
        """Add the given vertex data to the draw queue.

        :param stype: type of shape to be added. Should be one of {'poly',
                'path', 'point'}
        :type stype: str

        :param vertices: (N, 3) array containing the vertices to be drawn.
        :type vertices: np.ndarray

        :param edges: (N, 2) array containing edges as tuples of indices
                into the vertex array. This can be None when not appropriate
                (eg. for points)
        :type edges: None | np.ndarray

        :param faces: (N, 3) array containing faces as tuples of indices
                into the vertex array. For 'point' and 'path' shapes, this can
                be None
        :type faces: np.ndarray

        :param fill: Fill color of the shape as a normalized RGBA tuple.
                When set to `None` the shape doesn't get a fill (default: None)
        :type fill: None | tuple

        :param stroke: Stroke color of the shape as a normalized RGBA
                tuple. When set to `None` the shape doesn't get stroke
                (default: None)
        :type stroke: None | tuple
        // TODO: Update documentation
        // TODO: Unite style-related attributes for both 2D and 3D under one material class
        """

        fill_shape = self.style.fill_enabled and not (fill is None)
        stroke_shape = self.style.stroke_enabled and not (stroke is None)

        if fill_shape and stype not in ["point", "path"]:
            idx = np.array(faces, dtype=np.uint32).ravel()
            self.draw_queue.append(
                ["triangles", (vertices, idx, fill, normals, material)]
            )

        if stroke_shape:
            if stype == "point":
                idx = np.arange(0, len(vertices), dtype=np.uint32)
                self.draw_queue.append(
                    ["points", (vertices, idx, stroke, normals, material)]
                )
            else:
                idx = np.array(edges, dtype=np.uint32).ravel()
                self.draw_queue.append(
                    ["lines", (vertices, idx, stroke, normals, material)]
                )

    def render_with_shaders(self, draw_type, draw_obj):
        vertices, idx, color, normals, material = draw_obj
        """Like render_default but is aware of shaders other than the basic one"""
        # 0. If material does not need normals nor extra info, strip them out
        # and use the method from superclass
        if (
            material is None
            or isinstance(material, BasicMaterial)
            or draw_type in ["points", "lines"]
        ):
            OpenGLRenderer.render_default(self, draw_type, [draw_obj[:3]])
            return

        # 1. Get the number of vertices
        num_vertices = len(vertices)

        # 2. Create empty buffers based on the number of vertices.
        #
        data = np.zeros(
            num_vertices, dtype=[("position", np.float32, 3), ("normal", np.float32, 3)]
        )

        # 3. Loop through all the shapes in the geometry queue adding
        # it's information to the buffer.
        #
        draw_indices = []
        data["position"][
            0:num_vertices,
        ] = np.array(vertices)
        draw_indices.append(idx)
        data["normal"][
            0:num_vertices,
        ] = np.array(normals)
        self.vertex_buffer.set_data(data)
        self.index_buffer.set_data(np.hstack(draw_indices))

        if isinstance(material, NormalMaterial):
            # 4. Bind the buffer to the shader.
            #
            self.normal_prog.bind(self.vertex_buffer)

            # 5. Draw the shape using the proper shape type and get rid of
            # the buffers.
            #
            self.normal_prog.draw(draw_type, indices=self.index_buffer)
        elif isinstance(material, BlinnPhongMaterial):
            self.phong_prog.bind(self.vertex_buffer)
            self.phong_prog["u_cam_pos"] = self.camera_pos
            # Material attributes
            self.phong_prog["u_ambient_color"] = material.ambient
            self.phong_prog["u_diffuse_color"] = material.diffuse
            self.phong_prog["u_specular_color"] = material.specular
            self.phong_prog["u_shininess"] = material.shininess
            # Directional lights
            self.phong_prog[
                "u_directional_light_count"
            ] = self.directional_light_color.size
            self.phong_prog["u_directional_light_dir"] = self.directional_light_dir.data
            self.phong_prog[
                "u_directional_light_color"
            ] = self.directional_light_color.data
            self.phong_prog[
                "u_directional_light_specular"
            ] = self.directional_light_specular.data
            # Ambient lights
            self.phong_prog["u_ambient_light_count"] = self.ambient_light_color.size
            self.phong_prog["u_ambient_light_color"] = self.ambient_light_color.data
            # Point lights
            self.phong_prog["u_point_light_count"] = self.point_light_color.size
            self.phong_prog["u_point_light_color"] = self.point_light_color.data
            self.phong_prog["u_point_light_pos"] = self.point_light_pos.data
            self.phong_prog["u_point_light_specular"] = self.point_light_specular.data
            # Point light falloffs
            self.phong_prog["u_const_falloff"] = self.const_falloff.data
            self.phong_prog["u_linear_falloff"] = self.linear_falloff.data
            self.phong_prog["u_quadratic_falloff"] = self.quadratic_falloff.data
            # Draw
            self.phong_prog.draw(draw_type, indices=self.index_buffer)
        else:
            raise NotImplementedError("Material not implemented")

    def flush_geometry(self):
        """Flush all the shape geometry from the draw queue to the GPU."""
        for index, shape in enumerate(self.draw_queue):
            current_shape, current_obj = (
                self.draw_queue[index][0],
                self.draw_queue[index][1],
            )
            # If current_shape is lines, bring it to the front by epsilon
            # to resolve z-fighting
            if current_shape == "lines":
                # line_transform is used whenever we render lines to break ties in depth
                # We transform the points to camera space, move them by
                # Z_EPSILON, and them move them back to world space
                line_transform = inv(self.lookat_matrix).dot(
                    translation_matrix(0, 0, Z_EPSILON).dot(self.lookat_matrix)
                )
                vertices = current_obj[0]
                current_obj = (
                    np.hstack([vertices, np.ones((vertices.shape[0], 1))]).dot(
                        line_transform.T
                    )[:, :3],
                    *current_obj[1:],
                )
            self.render_with_shaders(current_shape, current_obj)

        self.draw_queue = []

    def cleanup(self):
        super(Renderer3D, self).cleanup()
        self.normal_prog.delete()
        self.phong_prog.delete()

    def add_ambient_light(self, r, g, b):
        self.ambient_light_color.add(np.array((r, g, b)))

    def add_directional_light(self, r, g, b, x, y, z):
        self.directional_light_color.add(np.array((r, g, b)))
        self.directional_light_dir.add(np.array((x, y, z)))
        self.directional_light_specular.add(self.light_specular)

    def add_point_light(self, r, g, b, x, y, z):
        self.point_light_color.add(np.array((r, g, b)))
        self.point_light_pos.add(np.array((x, y, z)))
        self.point_light_specular.add(self.light_specular)
        self.const_falloff.add(self.curr_constant_falloff)
        self.linear_falloff.add(self.curr_linear_falloff)
        self.quadratic_falloff.add(self.curr_quadratic_falloff)

    def rotate_x(self, theta):
        self.rotate(theta, axis=np.array([1, 0, 0]))

    def rotate_y(self, theta):
        self.rotate(theta, axis=np.array([0, 1, 0]))

    def rotate_z(self, theta):
        self.rotate(theta, axis=np.array([0, 0, 1]))

    def camera(self, *args, **kwargs):
        def real_camera(
            position=(0, 0, p5.sketch.size[1] / math.tan(math.pi / 6)),
            target_position=(0, 0, 0),
            up_vector=(0, 1, 0),
        ):
            self.lookat_matrix = matrix.look_at(
                np.array(position), np.array(target_position), np.array(up_vector)
            )
            self.camera_pos = np.array(position)

        if len(args) == 9:  # If using non-tuple arguments
            kwargs["position"] = args[:3]
            kwargs["target_position"] = args[3:6]
            kwargs["up_vector"] = args[6:]
        elif len(args) <= 3:  # If using tuple arguments
            if len(args) >= 1:
                kwargs["position"] = args[0]
            if len(args) >= 2:
                kwargs["target_position"] = args[1]
            if len(args) >= 3:
                kwargs["up_vector"] = args[2]
        else:
            raise ValueError("Unexpected number of arguments passed to camera()")

        real_camera(**kwargs)

    def perspective(self, fovy, aspect, near, far):
        self.projection_matrix = matrix.perspective_matrix(fovy, aspect, near, far)

    def ortho(self, left, right, bottom, top, near, far):
        self.projection_matrix = np.array(
            [
                [2 / (right - left), 0, 0, -(right + left) / (right - left)],
                [0, 2 / (top - bottom), 0, -(top + bottom) / (top - bottom)],
                [0, 0, -2 / (far - near), -(far + near) / (far - near)],
                [0, 0, 0, 1],
            ]
        )

    def frustum(self):
        raise NotImplementedError

    def shape(self, vertices, contours, shape_type, *args):
        """Render a PShape"""
        self.render(PShape(vertices=vertices, contours=contours, shape_type=shape_type))

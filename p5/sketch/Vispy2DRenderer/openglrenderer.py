from abc import ABC
import numpy as np

from p5.core import p5
from p5.core.constants import SType, ROUND, MITER
from p5.pmath import matrix
from .shape import Arc, PShape

from dataclasses import dataclass
from vispy.gloo import Program, VertexBuffer, FrameBuffer, IndexBuffer
from OpenGL.GLU import (
    gluTessBeginPolygon,
    gluTessBeginContour,
    gluTessEndPolygon,
    gluTessEndContour,
    gluTessVertex,
)

# Useful constants
COLOR_WHITE = (1, 1, 1, 1)
COLOR_BLACK = (0, 0, 0, 1)


def to_3x3(mat):
    """Returns the upper left 3x3 corner of an np.array"""
    return mat[:3, :3]


def _tess_new_contour(vertices):
    """Given a list of vertices, evoke gluTess to create a contour"""
    gluTessBeginContour(p5.tess.tess)
    for v in vertices:
        gluTessVertex(p5.tess.tess, v, v)
    gluTessEndContour(p5.tess.tess)


def _vertices_to_render_primitive(gl_name, vertices):
    """Returns a render primitive of gl_type with vertices in sequential order"""
    return [gl_name, np.asarray(vertices), np.arange(len(vertices), dtype=np.uint32)]


def _get_line_from_verts(vertices):
    """Given a list of vertices, chain them sequentially in a line rendering primitive"""
    n_vert = len(vertices)
    return _get_line_from_indices(
        vertices,
        np.arange(n_vert - 1, dtype=np.uint32),
        np.arange(1, n_vert, dtype=np.uint32),
    )


def _get_line_from_indices(vertices, start, end):
    """Given two columns of indices that represent edges, return a line rendering primitive

    :param vertices: List of vertices
    :type vertices: list

    :param start: Array of start positions of edges in vertex indices
    :type start: np.ndarray

    :param end: Array of end positions fo edges in vertex indices
    :type end: np.ndarray
    """
    start = np.asarray(start, dtype=np.uint32)
    end = np.asarray(end, dtype=np.uint32)
    return [
        "lines",
        np.asarray(vertices),
        np.hstack((np.vstack(start), np.vstack(end))),
    ]


def _add_edges_to_primitive_list(primitive_list, vertices, start, end):
    """Adds edges to a list of render primitives, given their start and end positions (in vertex indices)

    :param start: Array of start positions of edges in vertex indices
    :type start: np.ndarray

    :param end: Array of end positions fo edges in vertex indices
    :type end: np.ndarray
    """
    primitive_list.append(_get_line_from_indices(vertices, start, end))


def _not_enough_vertices(shape, n):
    """Returns an error string that describes how many vertices are needed"""
    return "Need at least {} vertices for {}".format(n, shape)


def _wrong_multiple(shape, n):
    """Returns an error string that describes the # of vertices is not a multiple of n"""
    return "{} requires the number of vertices to be a multiple of {}".format(
        shape.shape_type, n
    )


def _check_shape(shape):
    """Checks if the shape is valid using assertions"""
    n_vert = len(shape.vertices)
    if shape.shape_type in [SType.TRIANGLES, SType.TRIANGLE_FAN, SType.TRIANGLE_STRIP]:
        assert n_vert >= 3, _not_enough_vertices(shape, 3)
    elif shape.shape_type in [SType.LINES, SType.LINE_STRIP]:
        assert n_vert >= 2, _not_enough_vertices(shape, 2)
    elif shape.shape_type in [SType.QUADS, SType.QUAD_STRIP]:
        assert n_vert >= 4, _not_enough_vertices(shape, 4)

    if shape.shape_type == SType.TRIANGLES:
        assert n_vert % 3 == 0, _wrong_multiple(shape, 3)
    if shape.shape_type == SType.QUADS:
        assert n_vert % 4 == 0, _wrong_multiple(shape, 4)


def _get_borders(shape):
    """Generates the render primitives for the borders of a given shape

    :returns: ['lines', vertices, idx]
    """
    render_primitives = []
    n_vert = len(shape.vertices)
    if shape.shape_type == SType.TRIANGLES:
        start = np.arange(n_vert)
        end = np.arange(n_vert) + np.tile([1, 1, -2], n_vert // 3)
        _add_edges_to_primitive_list(render_primitives, shape.vertices, start, end)
    elif shape.shape_type == SType.TRIANGLE_STRIP:
        start = np.concatenate((np.arange(n_vert - 1), np.arange(n_vert - 2)))
        end = np.concatenate((np.arange(1, n_vert), np.arange(2, n_vert)))
        _add_edges_to_primitive_list(render_primitives, shape.vertices, start, end)
    elif shape.shape_type == SType.TRIANGLE_FAN:
        start = np.concatenate((np.repeat([0], n_vert - 1), np.arange(1, n_vert - 1)))
        end = np.concatenate((np.arange(1, n_vert), np.arange(2, n_vert)))
        _add_edges_to_primitive_list(render_primitives, shape.vertices, start, end)
    elif shape.shape_type == SType.QUADS:
        start = np.arange(n_vert)
        end = np.arange(n_vert) + np.tile([1, 1, 1, -3], n_vert // 4)
        _add_edges_to_primitive_list(render_primitives, shape.vertices, start, end)
    elif shape.shape_type == SType.QUAD_STRIP:
        start = np.concatenate((np.arange(0, n_vert, 2), np.arange(n_vert - 2)))
        end = np.concatenate((np.arange(1, n_vert, 2), np.arange(2, n_vert)))
        _add_edges_to_primitive_list(render_primitives, shape.vertices, start, end)
    elif shape.shape_type == SType.LINES:
        start = np.arange(0, n_vert, 2)
        end = np.arange(1, n_vert, 2)
        _add_edges_to_primitive_list(render_primitives, shape.vertices, start, end)
    elif shape.shape_type == SType.LINE_STRIP:
        render_primitives.append(_get_line_from_verts(shape.vertices))
    elif shape.shape_type == SType.TESS:
        render_primitives.append(_get_line_from_verts(shape.vertices))
        for contour in shape.contours:
            render_primitives.append(_get_line_from_verts(contour))
    return render_primitives


def _get_meshes(shape):
    """Generates the rendering primitives for the meshes of a given shape

    :returns: [shape_type, vertices, idx]
    """
    render_primitives = []
    n_vert = len(shape.vertices)
    if shape.shape_type in [
        SType.TRIANGLES,
        SType.TRIANGLE_STRIP,
        SType.TRIANGLE_FAN,
        SType.QUAD_STRIP,
    ]:
        gl_name = shape.shape_type.name.lower()
        if gl_name == "quad_strip":  # vispy does not support quad_strip
            gl_name = "triangle_strip"  # but it can be drawn using triangle_strip
        render_primitives.append(_vertices_to_render_primitive(gl_name, shape.vertices))
    elif shape.shape_type == SType.QUADS:
        n_quad = len(shape.vertices) // 4
        render_primitives.append(
            [
                "triangles",
                np.asarray(shape.vertices),
                np.repeat(np.arange(0, n_vert, 4, dtype=np.uint32), 6)
                + np.tile(np.array([0, 1, 2, 0, 2, 3], dtype=np.uint32), n_quad),
            ]
        )
    elif shape.shape_type == SType.TESS:
        gluTessBeginPolygon(p5.tess.tess, None)
        _tess_new_contour(shape.vertices)
        if len(shape.contours) > 0:
            for contour in shape.contours:
                _tess_new_contour(contour)
        gluTessEndPolygon(p5.tess.tess)
        render_primitives += p5.tess.get_result()
    return render_primitives


def get_render_primitives(shape):
    """Given a shape, return a list of render primitives in the form of [type, vertices, indices]"""
    _check_shape(shape)
    render_primitives = []
    if isinstance(shape, Arc):
        # Render meshes
        if p5.renderer.style.fill_enabled:
            render_primitives.extend(_get_meshes(shape))
        # Render borders
        if p5.renderer.style.stroke_enabled:
            if shape.arc_mode in ["CHORD", "OPEN"]:  # Implies shape.shape_type == TESS
                render_primitives.extend(_get_borders(shape))
            elif shape.arc_mode is None:  # Implies shape.shape_type == TRIANGLE_FAN
                render_primitives.append(_get_line_from_verts(shape.vertices[1:]))
            elif shape.arc_mode == "PIE":  # Implies shape.shape_type == TRIANGLE_FAN
                render_primitives.append(_get_line_from_verts(shape.vertices))
    else:
        # Render points
        if shape.shape_type == SType.POINTS:
            render_primitives.append(
                _vertices_to_render_primitive(render_primitives, "points")
            )
        # Render meshes
        if p5.renderer.style.fill_enabled:
            render_primitives.extend(_get_meshes(shape))
        # Render borders
        if p5.renderer.style.stroke_enabled:
            render_primitives.extend(_get_borders(shape))
    return render_primitives


@dataclass
class Style2D:
    background_color = (0.8, 0.8, 0.8, 1.0)
    fill_color = COLOR_WHITE
    fill_enabled = True
    stroke_color = COLOR_BLACK
    stroke_enabled = True
    stroke_weight = 1
    tint_color = COLOR_BLACK
    tint_enabled = False
    ellipse_mode = "CENTER"
    rect_mode = "CORNER"
    color_parse_mode = "RGB"
    color_range = (255, 255, 255, 255)
    stroke_cap = ROUND
    stroke_join = MITER

    def set_stroke_cap(self, c):
        self.stroke_cap = c

    def set_stroke_join(self, j):
        self.stroke_join = j


# Abstract class that contains common code for OpenGL renderers
class OpenGLRenderer(ABC):
    def __init__(self, src_fbuffer, src_default):
        self.fbuffer_prog = Program(src_fbuffer.vert, src_fbuffer.frag)
        self.default_prog = Program(src_default.vert, src_default.frag)

        self.fbuffer = FrameBuffer()
        self.fbuffer_tex_front = None
        self.fbuffer_tex_back = None

        vertices = np.array(
            [[-1.0, -1.0], [+1.0, -1.0], [-1.0, +1.0], [+1.0, +1.0]], np.float32
        )
        texcoords = np.array(
            [[0.0, 0.0], [1.0, 0.0], [0.0, 1.0], [1.0, 1.0]], dtype=np.float32
        )

        self.fbuf_vertices = VertexBuffer(data=vertices)
        self.fbuf_texcoords = VertexBuffer(data=texcoords)

        self.fbuffer_prog["texcoord"] = self.fbuf_texcoords
        self.fbuffer_prog["position"] = self.fbuf_vertices

        self.vertex_buffer = VertexBuffer()
        self.index_buffer = IndexBuffer()

        # Renderer Globals
        # VIEW MATRICES, ETC
        #
        self.viewport = None
        self.texture_viewport = None
        self.transform_matrix = np.identity(4)
        self.projection_matrix = np.identity(4)

        # Renderer Globals: RENDERING
        self.draw_queue = []

        self.style = Style2D()
        self.style_stack = []
        self.matrix_stack = []

    def render_default(self, draw_type, draw_queue):
        # 1. Get the maximum number of vertices persent in the shapes
        # in the draw queue.
        #
        if len(draw_queue) == 0:
            return

        num_vertices = 0
        for vertices, _, _ in draw_queue:
            num_vertices = num_vertices + len(vertices)

        # 2. Create empty buffers based on the number of vertices.
        #
        data = np.zeros(
            num_vertices, dtype=[("position", np.float32, 3), ("color", np.float32, 4)]
        )

        # 3. Loop through all the shapes in the geometry queue adding
        # it's information to the buffer.
        #
        sidx = 0
        draw_indices = []
        for vertices, idx, color in draw_queue:
            num_shape_verts = len(vertices)

            data["position"][
                sidx : (sidx + num_shape_verts),
            ] = np.array(vertices)

            color_array = np.array([color] * num_shape_verts)
            data["color"][sidx : sidx + num_shape_verts, :] = color_array

            draw_indices.append(sidx + idx)

            sidx += num_shape_verts

        self.vertex_buffer.set_data(data)
        self.index_buffer.set_data(np.hstack(draw_indices))

        # 4. Bind the buffer to the shader.
        #
        self.default_prog.bind(self.vertex_buffer)

        # 5. Draw the shape using the proper shape type and get rid of
        # the buffers.
        #
        self.default_prog.draw(draw_type, indices=self.index_buffer)

    def cleanup(self):
        """Run the clean-up routine for the renderer.

        This method is called when all drawing has been completed and the
        program is about to exit.

        """
        self.default_prog.delete()
        self.fbuffer_prog.delete()
        self.fbuffer.delete()

    def _transform_vertices(self, vertices, local_matrix, global_matrix):
        """Applies `local_matrix` then `global_matrix` to `vertices`"""
        product = np.dot(np.dot(vertices, local_matrix.T), global_matrix.T)
        # dehomogenize coordinates
        # need np.newaxis to broadcast the vector because each row represents a vertex
        dehomogenized = product / product[:, 3][:, np.newaxis]
        return dehomogenized[:, :3]  # Return the first three rows of the result

    def push_matrix(self):
        """Pushes the current transformation matrix onto the matrix stack."""
        self.matrix_stack.append(self.transform_matrix.copy())

    def pop_matrix(self):
        """Pops the current transformation matrix off the matrix stack."""
        assert len(self.matrix_stack) > 0, "No matrix to pop"
        self.transform_matrix = self.matrix_stack.pop()

    def scale(self, sx, sy=None, sz=None):
        if sy is None and sz is None:
            sy = sx
            sz = sx
        elif sz is None:
            sz = 1
        tmat = matrix.scale_transform(sx, sy, sz)
        self.transform_matrix = self.transform_matrix.dot(tmat)
        return tmat

    def apply_matrix(self, transform_matrix):
        tmatrix = np.array(transform_matrix)
        self.transform_matrix = self.transform_matrix.dot(tmatrix)

    def reset_matrix(self):
        self.transform_matrix = np.identity(4)

    def print_matrix(self):
        print(self.transform_matrix)

    def shear_x(self, theta):
        shear_mat = np.identity(4)
        shear_mat[0, 1] = np.tan(theta)
        self.transform_matrix = self.transform_matrix.dot(shear_mat)
        return shear_mat

    def shear_y(self, theta):
        shear_mat = np.identity(4)
        shear_mat[1, 0] = np.tan(theta)
        self.transform_matrix = self.transform_matrix.dot(shear_mat)
        return shear_mat

    def reset_transforms(self):
        """Reset all transformations to their default state."""
        self.transform_matrix = np.identity(4)

    def translate(self, x, y, z=0):
        tmat = matrix.translation_matrix(x, y, z)
        self.transform_matrix = self.transform_matrix.dot(tmat)
        return tmat

    def rotate(self, theta, axis=np.array([0, 0, 1])):
        axis = np.array(axis[:])
        tmat = matrix.rotation_matrix(axis, theta)
        self.transform_matrix = self.transform_matrix.dot(tmat)
        return tmat

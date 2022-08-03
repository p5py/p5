import unittest

import numpy as np
from p5.core.geometry import Geometry
from p5.core import p5
import builtins

builtins.current_renderer = "vispy"
p5.mode = "P3D"
from p5.sketch.Vispy3DRenderer.renderer3d import Renderer3D

p5.renderer = Renderer3D()

box = Geometry(1, 1)
cube_indices = [
    [0, 4, 2, 6],  # -1, 0, 0],// -x
    [1, 3, 5, 7],  # +1, 0, 0],// +x
    [0, 1, 4, 5],  # 0, -1, 0],// -y
    [2, 6, 3, 7],  # 0, +1, 0],// +y
    [0, 2, 1, 3],  # 0, 0, -1],// -z
    [4, 5, 6, 7],  # 0, 0, +1] // +z
]

box.stroke_indices = [
    [0, 1],
    [1, 3],
    [3, 2],
    [6, 7],
    [8, 9],
    [9, 11],
    [14, 15],
    [16, 17],
    [17, 19],
    [18, 19],
    [20, 21],
    [22, 23],
]

for i in range(len(cube_indices)):
    cube_index = cube_indices[i]
    v = i * 4
    for j in range(4):
        d = cube_index[j]

        octant = [((d & 1) * 2 - 1) / 2, ((d & 2) - 1) / 2, ((d & 4) / 2 - 1) / 2]

        box.vertices.append(octant)
        box.uvs.extend([j & 1, (j & 2) / 2])

    box.faces.append([v, v + 1, v + 2])
    box.faces.append([v + 2, v + 1, v + 3])


class TestBoxGeometry(unittest.TestCase):
    def test_vertices(self):
        vertices = [
            [-0.5, -0.5, -0.5],
            [-0.5, -0.5, 0.5],
            [-0.5, 0.5, -0.5],
            [-0.5, 0.5, 0.5],
            [0.5, -0.5, -0.5],
            [0.5, 0.5, -0.5],
            [0.5, -0.5, 0.5],
            [0.5, 0.5, 0.5],
            [-0.5, -0.5, -0.5],
            [0.5, -0.5, -0.5],
            [-0.5, -0.5, 0.5],
            [0.5, -0.5, 0.5],
            [-0.5, 0.5, -0.5],
            [-0.5, 0.5, 0.5],
            [0.5, 0.5, -0.5],
            [0.5, 0.5, 0.5],
            [-0.5, -0.5, -0.5],
            [-0.5, 0.5, -0.5],
            [0.5, -0.5, -0.5],
            [0.5, 0.5, -0.5],
            [-0.5, -0.5, 0.5],
            [0.5, -0.5, 0.5],
            [-0.5, 0.5, 0.5],
            [0.5, 0.5, 0.5],
        ]

        self.assertTrue(np.allclose(np.array(vertices), np.array(box.vertices)))

    def test_normals(self):
        box.compute_normals()

        normals = [
            [-1.0, 0.0, 0.0],
            [-1.0, 0.0, 0.0],
            [-1.0, 0.0, 0.0],
            [-1.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [0.0, -1.0, 0.0],
            [0.0, -1.0, 0.0],
            [0.0, -1.0, 0.0],
            [0.0, -1.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, -1.0],
            [0.0, 0.0, -1.0],
            [0.0, 0.0, -1.0],
            [0.0, 0.0, -1.0],
            [0.0, 0.0, 1.0],
            [0.0, 0.0, 1.0],
            [0.0, 0.0, 1.0],
            [0.0, 0.0, 1.0],
        ]

        self.assertTrue(np.allclose(np.array(normals), np.array(box.vertex_normals)))

    def test_triangle_edges(self):
        box.make_triangle_edges()
        edges = [
            [0, 1],
            [1, 2],
            [2, 0],
            [2, 1],
            [1, 3],
            [3, 2],
            [4, 5],
            [5, 6],
            [6, 4],
            [6, 5],
            [5, 7],
            [7, 6],
            [8, 9],
            [9, 10],
            [10, 8],
            [10, 9],
            [9, 11],
            [11, 10],
            [12, 13],
            [13, 14],
            [14, 12],
            [14, 13],
            [13, 15],
            [15, 14],
            [16, 17],
            [17, 18],
            [18, 16],
            [18, 17],
            [17, 19],
            [19, 18],
            [20, 21],
            [21, 22],
            [22, 20],
            [22, 21],
            [21, 23],
            [23, 22],
        ]

        self.assertEqual(edges, box.edges)


if __name__ == "__main__":
    unittest.main()

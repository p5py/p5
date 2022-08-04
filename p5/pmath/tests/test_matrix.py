import unittest
import numpy as np

from p5.pmath import matrix
from p5.pmath.utils import PI

v = np.array([3, 4])


class TestMatrix(unittest.TestCase):
    def test_magnitude(self):
        self.assertEqual(matrix._magnitude(v), 5.0)

    def test_normalize(self):
        self.assertTrue(np.array_equal(matrix._normalize(v), v / 5.0))

    def test_scale_transform(self):
        T = matrix.scale_transform(1, 2, 3)
        R = np.array([[1, 0, 0, 0], [0, 2, 0, 0], [0, 0, 3, 0], [0, 0, 0, 1]])
        self.assertTrue(np.array_equal(T, R))

    def test_translation_matrix(self):
        T = matrix.translation_matrix(5, 6, 7)
        R = np.array([[1, 0, 0, 5], [0, 1, 0, 6], [0, 0, 1, 7], [0, 0, 0, 1]])
        self.assertTrue(np.array_equal(T, R))

    def test_rotation_matrix(self):
        axis = np.array([1, 1, 1])
        T = matrix.rotation_matrix(axis, PI / 2)
        R = np.array(
            [
                [0.33333333, -0.24401694, 0.9106836, 0],
                [0.9106836, 0.33333333, -0.24401694, 0],
                [-0.24401694, 0.9106836, 0.33333333, 0],
                [0, 0, 0, 1],
            ]
        )
        self.assertTrue(np.allclose(T, R))

    def test_triple_axis_rotation_matrix(self):
        x = np.array([1, 1, 0])
        y = np.array([0, 1, 0])
        z = np.array([0, 1, 1])

        T = matrix.triple_axis_rotation_matrix(x, y, z)
        R = np.array(
            [
                [1, 1, 0, 0],
                [0, 1, 0, 0],
                [0, 1, 1, 0],
                [0, 0, 0, 1],
            ]
        )
        self.assertTrue(np.array_equal(T, R))

    def test_look_at(self):
        eye = np.array([0, 0, 10])
        at = np.array([0, 0, 0])
        up = np.array([0, 1, 0])

        T = matrix.look_at(eye, at, up)
        R = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, -10], [0, 0, 0, 1]])
        self.assertTrue(np.array_equal(T, R))

    def test_perspective_matrix(self):
        fov = 2 / 3 * PI
        aspect = 3 / 4
        near_plane = 0.1
        far_plane = 100

        T = matrix.perspective_matrix(fov, aspect, near_plane, far_plane)
        R = np.array(
            [
                [0.769800, 0, 0, 0],
                [0, 0.5773502, 0, 0],
                [0, 0, -1.00200, -0.200200],
                [0, 0, -1, 0],
            ]
        )

        self.assertTrue(np.allclose(T, R))


if __name__ == "__main__":
    unittest.main()

import unittest
import numpy as np

from p5.sketch.Vispy2DRenderer.shape import PShape
from p5.core.color import Color
from p5.pmath import PI

vertices = [(0, 0), (1, 0), (1, 1), (0, 1)]

quad = PShape(
    vertices=vertices,
    fill_color=Color(255),
    stroke_color=Color(0),
    stroke_weight=2,
    stroke_join=1,
    stroke_cap=1,
)

contour_shape = PShape(
    vertices=[(0, 0), (100, 0), (100, 100), (0, 100)],
    fill_color=Color(255),
    stroke_color=Color(0),
    stroke_weight=2,
    stroke_join=1,
    stroke_cap=1,
    contours=[[25, 25], [75, 25], [75, 75], [25, 75]],
)


class TestPShape(unittest.TestCase):
    def test_properties(self):
        self.assertTrue(
            np.array_equal(quad.vertices, np.array([(0, 0), (1, 0), (1, 1), (0, 1)]))
        )
        self.assertEqual(quad._fill, Color(255))
        self.assertEqual(quad._stroke, Color(0))
        self.assertEqual(quad._stroke_weight, 2)
        self.assertEqual(quad._stroke_cap, 1)
        self.assertEqual(quad._stroke_join, 1)

    def test_transforms(self):
        quad.translate(100, 100, 100)
        self.assertTrue(
            np.array_equal(
                quad._matrix,
                np.array(
                    [
                        [1.0, 0.0, 0.0, 100.0],
                        [0.0, 1.0, 0.0, 100.0],
                        [0.0, 0.0, 1.0, 100.0],
                        [0.0, 0.0, 0.0, 1.0],
                    ]
                ),
            )
        )
        quad.reset_matrix()

        quad.rotate_x(PI / 2)
        self.assertTrue(
            np.allclose(
                quad._matrix,
                np.array(
                    [
                        [1.0, 0.0, 0.0, 0.0],
                        [0.0, 0.0, -1.0, 0.0],
                        [0.0, 1.0, 0.0, 0.0],
                        [0.0, 0.0, 0.0, 1.0],
                    ]
                ),
            )
        )
        quad.reset_matrix()

        quad.rotate_y(PI / 2)
        self.assertTrue(
            np.allclose(
                quad._matrix,
                np.array(
                    [
                        [0.0, 0.0, 1.0, 0.0],
                        [0.0, 1.0, 0.0, 0.0],
                        [-1.0, 0.0, 0.0, 0.0],
                        [0.0, 0.0, 0.0, 1.0],
                    ]
                ),
            )
        )
        quad.reset_matrix()

        quad.rotate_z(PI / 2)
        self.assertTrue(
            np.allclose(
                quad._matrix,
                np.array(
                    [
                        [0.0, -1.0, 0.0, 0.0],
                        [1.0, 0.0, 0.0, 0.0],
                        [0.0, 0.0, 1.0, 0.0],
                        [0.0, 0.0, 0.0, 1.0],
                    ]
                ),
            )
        )
        quad.reset_matrix()

        quad.scale(2, 2)
        self.assertTrue(
            np.allclose(
                quad._matrix,
                np.array(
                    [
                        [2.0, 0.0, 0.0, 0.0],
                        [0.0, 2.0, 0.0, 0.0],
                        [0.0, 0.0, 1.0, 0.0],
                        [0.0, 0.0, 0.0, 1.0],
                    ]
                ),
            )
        )
        quad.reset_matrix()

        quad.shear_x(PI / 4)
        self.assertTrue(
            np.allclose(
                quad._matrix,
                np.array(
                    [
                        [1.0, 1.0, 0.0, 0.0],
                        [0.0, 1.0, 0.0, 0.0],
                        [0.0, 0.0, 1.0, 0.0],
                        [0.0, 0.0, 0.0, 1.0],
                    ]
                ),
            )
        )
        quad.reset_matrix()

        quad.shear_y(PI / 4)
        self.assertTrue(
            np.allclose(
                quad._matrix,
                np.array(
                    [
                        [1.0, 0.0, 0.0, 0.0],
                        [1.0, 1.0, 0.0, 0.0],
                        [0.0, 0.0, 1.0, 0.0],
                        [0.0, 0.0, 0.0, 1.0],
                    ]
                ),
            )
        )
        quad.reset_matrix()


if __name__ == "__main__":
    unittest.main()

import unittest
import numpy as np

from p5.core.shape import PShape
from p5.core.color import Color
from p5.pmath import PI

vertices = [(0, 0), (1, 0), (1, 1), (0, 1)]

quad = PShape(vertices=vertices, fill_color=Color(255),
        stroke_color=Color(0), stroke_weight=2,
        stroke_join=1, stroke_cap=1, attribs="closed")

contour_shape = PShape(vertices=[(0, 0), (100, 0), (100, 100), (0, 100)], 
        fill_color=Color(255), stroke_color=Color(0), stroke_weight=2,
        stroke_join=1, stroke_cap=1, attribs="closed",
        contour=[[25, 25], [75, 25], [75, 75], [25, 75]])

class TestPShape(unittest.TestCase):
    def test_properties(self):
        self.assertTrue(np.array_equal(
            quad.vertices, 
            np.array([(0, 0), (1, 0), (1, 1), (0, 1)])))
        self.assertEqual(quad._fill, Color(255))
        self.assertEqual(quad._stroke, Color(0))
        self.assertEqual(quad._stroke_weight, 2)
        self.assertEqual(quad._stroke_cap, 1)
        self.assertEqual(quad._stroke_join, 1)

    def test_transforms(self):
        quad.translate(100, 100, 100)
        self.assertTrue(np.array_equal(
            quad._matrix, 
            np.array([
                [1.0, 0.0, 0.0, 100.0],
                [0.0, 1.0, 0.0, 100.0],
                [0.0, 0.0, 1.0, 100.0],
                [0.0, 0.0, 0.0, 1.0],
                ])))
        quad.reset_matrix()


        quad.rotate_x(PI/2)
        self.assertTrue(np.allclose(
            quad._matrix, 
            np.array([
                [1.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, -1.0, 0.0],
                [0.0, 1.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 1.0],
                ])))
        quad.reset_matrix()


        quad.rotate_y(PI/2)
        self.assertTrue(np.allclose(
            quad._matrix, 
            np.array([
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 1.0, 0.0, 0.0],
                [-1.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 1.0],
                ])))
        quad.reset_matrix()


        quad.rotate_z(PI/2)
        self.assertTrue(np.allclose(
            quad._matrix, 
            np.array([
                [0.0, -1.0, 0.0, 0.0],
                [1.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 1.0],
                ])))
        quad.reset_matrix()


        quad.scale(2, 2)
        self.assertTrue(np.allclose(
            quad._matrix, 
            np.array([
                [2.0, 0.0, 0.0, 0.0],
                [0.0, 2.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 1.0],
                ])))
        quad.reset_matrix()


        quad.shear_x(PI/4)
        self.assertTrue(np.allclose(
            quad._matrix, 
            np.array([
                [1.0, 1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 1.0],
                ])))
        quad.reset_matrix()


        quad.shear_y(PI/4)
        self.assertTrue(np.allclose(
            quad._matrix, 
            np.array([
                [1.0, 0.0, 0.0, 0.0],
                [1.0, 1.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 1.0],
                ])))
        quad.reset_matrix()

    def test_edges(self):
        self.assertTrue(
            np.array_equal(quad._compute_poly_edges(), 
            np.array([[0, 1], [1, 2], [2, 3], [3, 0]])))
        self.assertTrue(
            np.array_equal(quad._compute_outline_edges(), 
            np.array([[0, 1], [1, 2], [2, 3]])))

    def test_triangulation(self):
        quad._retriangulate()
        self.assertTrue(
            np.array_equal(quad._tri_edges, 
            np.array([[1, 0], [2, 1], [3, 2], [0, 3]])))

        self.assertTrue(
            np.array_equal(quad._tri_faces, 
            np.array([[3, 0, 1], [1, 2, 3]])))

        self.assertTrue(
            np.array_equal(quad._tri_vertices, 
            np.array([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]])))

        contour_shape._retriangulate()
        self.assertTrue(
            np.array_equal(contour_shape._tri_edges, 
            np.array([[1, 0], [2, 1], [3, 2], [0, 3], [4, 5], [6, 5], [7, 6], [4, 7]])))

        self.assertTrue(
            np.array_equal(contour_shape._tri_faces, 
            np.array([[0, 4, 7], [4, 0, 1], [3, 7, 6], [7, 3, 0], [5, 1, 2], [1, 5, 4], [6, 2, 3], [2, 6, 5]])))

        self.assertTrue(
            np.array_equal(contour_shape._tri_vertices, 
            np.array([[0.0, 0.0], [100.0, 0.0], [100.0, 100.0], [0.0, 100.0], [25.0, 25.0], [75.0, 25.0], [75.0, 75.0], [25.0, 75.0]])))  


if __name__ == "__main__":
    unittest.main()
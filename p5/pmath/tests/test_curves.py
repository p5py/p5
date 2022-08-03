import unittest

from p5.pmath.curves import (
    bezier_point,
    bezier_tangent,
    curve_point,
    curve_tangent,
    quadratic_point,
)
from p5.pmath.vector import Point


class TestCurves(unittest.TestCase):
    def test_bezier_point(self):
        p1 = (30, 20)
        p2 = (80, 5)
        p3 = (80, 75)
        p4 = (30, 75)

        self.assertEqual(bezier_point(p1, p2, p3, p4, 0.5), (67.5, 41.875))

        self.assertEqual(bezier_point(p1, p2, p3, p4, 0.9), (43.5, 73.055))

        self.assertEqual(bezier_point(30, 80, 80, 30, 0.5), 67.5)

    def test_bezier_tangent(self):
        p1 = (30, 20)
        p2 = (80, 5)
        p3 = (80, 75)
        p4 = (30, 75)

        self.assertEqual(bezier_tangent(p1, p2, p3, p4, 0.5), (0.0, 93.75))

        self.assertEqual(bezier_tangent(p1[0], p2[0], p3[0], p4[0], 0.5), 0.0)

    def test_curve_point(self):
        p1 = (73, 24)
        p2 = (73, 61)
        p3 = (15, 65)
        p4 = (15, 65)
        self.assertEqual(curve_point(p1, p2, p3, p4, 0.5), (44.0, 65.3125))

    def test_curve_tangent(self):
        p1 = (73, 24)
        p2 = (73, 61)
        p3 = (15, 65)
        p4 = (15, 65)
        self.assertEqual(curve_tangent(p1, p2, p3, p4, 0.5), (-72.5, 0.375))

    def test_quadratic_point(self):
        p1 = (20, 20)
        p2 = (80, 20)
        p3 = (50, 50)
        self.assertEqual(quadratic_point(p1, p2, p3, 0.5), (57.5, 27.5))


if __name__ == "__main__":
    unittest.main()

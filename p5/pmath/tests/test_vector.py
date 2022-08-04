import unittest

import numpy as np
from p5.pmath.vector import Vector
from p5.pmath.utils import PI

a = Vector(2, 3, 4)
b = Vector(5, 6, 7)
c = Vector(1, 1)


class TestVector(unittest.TestCase):
    def test_properties(self):
        self.assertEqual(a.x, 2)
        self.assertEqual(a.y, 3)
        self.assertEqual(a.z, 4)

    def test_distance(self):
        self.assertTrue(np.allclose(a.distance(b), 5.196152))

    def test_lerp(self):
        self.assertEqual(a.lerp(b, 0.5), Vector(3.5, 4.5, 5.5))

    def test_arithmetic(self):
        self.assertEqual(a + b, Vector(7, 9, 11))
        self.assertEqual(a - b, Vector(-3, -3, -3))
        self.assertEqual(a * 2, Vector(4, 6, 8))
        self.assertEqual(-a, Vector(-2, -3, -4))

    def test_dot(self):
        self.assertEqual(a.dot(b), 56)

    def test_cross(self):
        self.assertEqual(a.cross(b), Vector(-3, 6, -3))

    def test_angle(self):
        self.assertTrue(np.allclose(c.angle, PI / 4))

    def test_angle_between(self):
        self.assertTrue(np.allclose(a.angle_between(b), 0.13047689))


if __name__ == "__main__":
    unittest.main()

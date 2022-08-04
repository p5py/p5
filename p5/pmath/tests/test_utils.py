import unittest

from p5.pmath.utils import constrain, lerp, remap, normalize, magnitude, distance, sq


class TestUtils(unittest.TestCase):
    def test_constrain(self):
        self.assertEqual(constrain(5, 0, 10), 5)
        self.assertEqual(constrain(-10, 0, 10), 0)
        self.assertEqual(constrain(20, 0, 10), 10)

    def test_lerp(self):
        self.assertEqual(lerp(0, 100, 0.5), 50)

    def test_remap(self):
        self.assertEqual(remap(50, (0, 100), (0, 10)), 5.0)

    def test_normalize(self):
        self.assertEqual(normalize(50, 0, 100), 0.5)

    def test_magnitude(self):
        self.assertEqual(magnitude(3, 4), 5)

    def test_distance(self):
        self.assertEqual(distance((0, 0, 0), (2, 3, 6)), 7)

    def test_sq(self):
        self.assertEqual(sq(4), 16)


if __name__ == "__main__":
    unittest.main()

import unittest
from p5.core.color import Color


class TestColor(unittest.TestCase):
    def test_parser(self):
        # RGB
        self.assertEqual(Color(100, 150, 200).red, 100)
        self.assertEqual(Color(100, 150, 200).green, 150)
        self.assertEqual(Color(100, 150, 200).blue, 200)
        self.assertEqual(Color(100, 150, 200).alpha, 255)

        # Greyscale
        self.assertEqual(Color(255), Color(255, 255, 255, 255))
        self.assertEqual(Color(0), Color(0, 0, 0, 255))

        # Grey Alpha
        self.assertEqual(Color(255, 100), Color(255, 255, 255, 100))
        self.assertEqual(Color(0, 100), Color(0, 0, 0, 100))

        # HEX
        self.assertEqual(Color("#fcba03"), Color(252, 186, 3))

        # Name
        self.assertEqual(Color("crimson"), Color(220, 20, 60))


if __name__ == "__main__":
    unittest.main()

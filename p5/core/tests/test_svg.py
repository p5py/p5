import unittest
import numpy as np

import xml.etree.ElementTree as etree
from p5.core.svg import get_style, parse_rect, parse_line
from p5.core.color import Color

svg = '<?xml version="1.0" encoding="utf-8"?> <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20010904//EN" "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd"> \
    <svg width="400px" height="300px" xml:lang="fr" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"> \
        <line x1="100" x2="20" y1="20" y2="200" style="fill:none;stroke:springgreen;stroke-width:2px;"/> \
        <ellipse cx="200" cy="150" rx="50" ry="130" style="fill:none;stroke:lightsteelblue;stroke-width:30px;stroke-opacity:0.5;"/> \
        <circle cx="200" cy="150" r="50"/> \
        <rect x="0" y="0" width="300" height="100"/> \
    </svg>'

tree = etree.fromstring(svg)
elements = []
for e in tree:
    elements.append(e)

line = elements[0]
rect = elements[3]

# not tested because they use Renderer() class while creation of PShape()
ellipse = elements[1]
circle = elements[2]


class TestSVG(unittest.TestCase):
    def test_get_style(self):
        self.assertEqual(get_style(line, "stroke"), "springgreen")
        self.assertEqual(get_style(line, "stroke-width"), 2)

        self.assertEqual(get_style(ellipse, "stroke"), "lightsteelblue")
        self.assertEqual(get_style(ellipse, "stroke-width"), 30)
        self.assertEqual(get_style(ellipse, "stroke-opacity"), 0.5)

    def test_parse_rect(self):
        parsed = parse_rect(rect)
        self.assertTrue(
            np.array_equal(
                parsed.vertices, np.array([(0, 0), (300, 0), (300, 100), (0, 100)])
            )
        )
        self.assertTrue(np.array_equal(parsed._fill, Color(0.0, 0.0, 0.0, 0.0)))
        self.assertTrue(np.array_equal(parsed.stroke_weight, 1))
        self.assertTrue(np.array_equal(parsed.stroke, Color(0.0, 0.0, 0.0, 0.0)))
        self.assertTrue(np.array_equal(parsed.stroke_join, 0))

    def test_parse_line(self):
        parsed = parse_line(line)

        self.assertTrue(
            np.array_equal(parsed.vertices, np.array([(100, 20), (20, 200)]))
        )
        self.assertTrue(np.array_equal(parsed._fill, Color("none")))
        self.assertTrue(np.array_equal(parsed.stroke_weight, 2))
        self.assertTrue(np.array_equal(parsed.stroke, Color("springgreen")))


if __name__ == "__main__":
    unittest.main()

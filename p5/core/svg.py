#
# Part of p5: A Python package based on Processing
# Copyright (C) 2017-2019 Abhik Pal
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

import xml.etree.ElementTree as etree
import math
import re
import numpy as np

from . import Color
from ..sketch.Vispy2DRenderer.shape import PShape
from . import primitives
from . import transforms
from ..pmath import matrix
from .constants import ROUND

default_values = {  # default values of SVG attributes
    "stroke-width": 1,
    "stroke-color": Color(0, 0, 0),
    "stroke-join": 0,
    "stroke-cap": 1,
    "stroke": "none",
    "fill": "none",
}


def get_style(element, style):
    # style parser for svg
    values = element.get("style")

    if element.get(style):
        return element.get(style)

    if values:
        for s in values.split(";"):
            if style in s:
                value = s.split(":")[1]

                if style == "stroke" or style == "fill":
                    return value
                if style == "stroke-width":
                    return int(value.replace("px", ""))
                if style == "stroke-opacity":
                    return float(value)

    if style in default_values.keys():
        return default_values[style]
    else:
        return None


def parse_rect(element):
    width = float(element.get("width"))
    height = float(element.get("height"))
    x = float(element.get("x"))
    y = float(element.get("y"))

    fill = Color(get_style(element, "fill"))
    stroke_weight = get_style(element, "stroke-width")
    stroke = Color(get_style(element, "stroke"))
    stroke_cap = get_style(element, "stroke-cap")

    return PShape(
        vertices=[(x, y), (x + width, y), (x + width, y + height), (x, y + height)],
        children=[],
        fill_color=fill,
        stroke_weight=stroke_weight,
        stroke_color=stroke,
        stroke_cap=stroke_cap,
        stroke_join=default_values["stroke-join"],
    )


def parse_circle(element):
    cx = float(element.get("cx"))
    cy = float(element.get("cy"))
    r = float(element.get("r"))

    fill = Color(get_style(element, "fill"))
    stroke_weight = get_style(element, "stroke-width")
    stroke = Color(get_style(element, "stroke"))
    stroke_cap = get_style(element, "stroke-cap")

    return primitives.Arc(
        (cx, cy),
        (r / 2, r / 2),
        0,
        2 * math.pi,
        "CHORD",
        fill_color=fill,
        stroke_weight=stroke_weight,
        stroke_color=stroke,
        stroke_cap=ROUND,
    )


def parse_line(element):
    x1 = float(element.get("x1"))
    y1 = float(element.get("y1"))
    x2 = float(element.get("x2"))
    y2 = float(element.get("y2"))

    fill = Color(get_style(element, "fill"))
    stroke_weight = get_style(element, "stroke-width")
    stroke = Color(get_style(element, "stroke"))
    stroke_cap = get_style(element, "stroke-cap")

    return PShape(
        vertices=[(x1, y1), (x2, y2)],
        fill_color=fill,
        stroke_weight=stroke_weight,
        stroke_color=stroke,
        stroke_cap=stroke_cap,
        stroke_join=default_values["stroke-join"],
    )


def parse_ellipse(element):
    cx = float(element.get("cx"))
    cy = float(element.get("cx"))
    rx = float(element.get("rx"))
    ry = float(element.get("ry"))

    fill = Color(get_style(element, "fill"))
    stroke_weight = get_style(element, "stroke-width")
    stroke = Color(get_style(element, "stroke"))
    stroke_cap = get_style(element, "stroke-cap")

    return primitives.Arc(
        (cx, cy),
        (rx / 2, ry / 2),
        0,
        2 * math.pi,
        "CHORD",
        fill_color=fill,
        stroke_weight=stroke_weight,
        stroke_color=stroke,
        stroke_cap=ROUND,
        stroke_join=default_values["stroke-join"],
    )


parser_function = {
    # tag: parser
    "rect": parse_rect,
    "circle": parse_circle,
    "line": parse_line,
    "ellipse": parse_ellipse,
    # "path": parse_path
}


def load_shape(filename):
    """
    Loads the given .svg file and converts it into
    PShape object.

    :param filename: link to .svg file
    :type filename: str

    """
    tree = etree.parse(filename)

    root = tree.getroot()
    if root.tag != "{http://www.w3.org/2000/svg}svg":
        raise TypeError("file %s does not seem to be a valid SVG file", filename)

    width = root.get("width")
    height = root.get("height")

    svg = transform_shape(parser(root))

    return svg


def transform_shape(element):
    # apply to current element
    element.apply_transform_matrix(element._transform_matrix)

    # apply to all its children
    for child in element.children:
        transform_shape(child)

    return element


def parser(element):
    shape = PShape([(0, 0)], children=[])

    transform = element.get("transform")
    transform_matrix = np.identity(4)
    if transform:
        properties = re.findall(r"(\w+)\(([\w\.]+)[,\s]*([^(]*)\)", transform)
        for p in properties:
            if p[0] == "scale":
                mat = matrix.scale_transform(float(p[1]), float(p[2]))
                transform_matrix = transform_matrix.dot(mat)
            elif p[0] == "translate":
                mat = matrix.translation_matrix(float(p[1]), float(p[2]))
                transform_matrix = transform_matrix.dot(mat)

    shape.transform_matrix(transform_matrix)

    for e in element:
        tag = e.tag.replace("{http://www.w3.org/2000/svg}", "")
        if tag in parser_function.keys():
            shape.add_child(parser_function[tag](e))
        elif tag == "g":
            shape.add_child(parser(e))
        else:
            continue

    return shape


def shape(shape, x=0, y=0):
    """
    Draws shapes to the display window

    :param shape: shape object
    :type shape: PShape

    :param x: x-coordinate of the shape
    :type x: float

    :param y: y-coordinate of the shape
    :type y: float
    """
    with transforms.push_matrix():
        transforms.translate(x, y)
        primitives.draw_shape(shape)

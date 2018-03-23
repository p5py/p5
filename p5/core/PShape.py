#py#
# Part of p5: A Python package based on Processing
# Copyright (C) 2017 Abhik Pal
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

from . import primitives
from ..pmath import Point, Vector
import warnings

MIN_POINT_ACCURACY = 20
MAX_POINT_ACCURACY = 200
POINT_ACCURACY_FACTOR = 10

OPEN, CLOSE = 1, 2
GROUP = 0  # createShape()
POINT = 2  # primitive
POINTS = 3  # vertices
LINE = 4  # primitive
LINES = 5  # beginShape(), createShape()
LINE_STRIP = 50  # beginShape()
LINE_LOOP = 51
TRIANGLE = 8  # primitive
TRIANGLES = 9  # vertices
TRIANGLE_STRIP = 10  # vertices
TRIANGLE_FAN = 11  # vertices
QUAD = 16  # primitive
QUADS = 17  # vertices
QUAD_STRIP = 18  # vertices
POLYGON = 20  # in the end, probably cannot
PATH = 21  # separate these two
RECT = 30  # primitive
ELLIPSE = 31  # primitive
ARC = 32  # primitive
SPHERE = 40  # primitive
BOX = 41  # primitive


class PShape():
    def __init__(self, vertices, kind='POLY', p=None):
        # super().__init__(vertices, kind=kind)
        self._stroke = True
        self._stroke_color = (1,1,1)
        self._filled = True
        self._fill = (0, 0, 0)
        self._visible = True
        self._openShape = False
        self._kind = type
        self._p = p
        self._vertices = []
        self.close = False

    def beginShape(self, kind = None):
        self._vertices = []
        if type is not None:
            self._kind = type
        self._openShape = True

    def endShape(self, mode=OPEN):
        if self._kind == GROUP:
            warnings.warn("Cannot end GROUP shape")
            return
        if not self._openShape:
            warnings.warn("Need to call beginShape() first")
            return
        self.close = (mode == CLOSE)
        self._openShape = False

    def vertex(self, *args):
        if len(args) == 1:
            if isinstance(args[0], Vector):
                self._vertices.append(args[0])
            else:
                self._vertices.append(Vector(*args))
        else:
            self._vertices.append(Vector(*args))

    def setVertex(self, index, *args):
        try:
            if len(args) == 1:
                if isinstance(args[0], Vector):
                    self._vertices[index] = args[0]  # Vector/point tuple
                    # self._vertices[index] = Vector(*args)  # Vector/point tuple
            elif len(args) == 2:
                self._vertices[index] = Vector(*args)  # x, y
            elif len(args) == 3:
                self._vertices[index] = Vector(*args)  # x, y, z
            else:
                raise ValueError("Please enter valid arguments")
        except IndexError:
            raise IndexError("PShape does not have a vertex at index " + index)

    def shape(self):
        if len(self._vertices) >= 0:
            vertices = [Point(v.x, v.y, v.z, flag=None) for v in self._vertices]
            if self._visible:
                return primitives.Shape(vertices)

        else:
            raise AttributeError("PShape does not have any vertex!")

    def getVertex(self, index):
        try:
            return self._vertices[index]
        except IndexError:
            raise IndexError("This PShape does not have a vertex at index " + index)

    def getVertexCount(self):
        return len(self._vertices)

    # def loadShape(self):
    #     raise NotImplementedError()
    #
    # def attachChild(self):
    #     raise NotImplementedError()

    def __repr__(self):
        return "PShape: type={}".format(self._kind)
    __str__ = __repr__

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, is_visible):
        self._visible = is_visible
        if is_visible:
            if not self._openShape:
                self.shape()
            # else:
            #     warnings.warn("PShape has not been 'ended'")

    @property
    def stroke(self):
        return self._stroke

    @stroke.setter
    def stroke(self, is_stroked):
        self._stroke = is_stroked

    @property
    def fill(self):
        return self._filled

    @fill.setter
    def fill(self, is_filled):
        self._filled = is_filled


def createShape(kind=POLYGON, p=None):
    return PShape(kind, p)

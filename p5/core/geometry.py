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

"""
3D geometry class for p5py
"""

from . import p5
import numpy as np
import math


class Geometry:
    """
        Geometry class for all 3D shapes

    :param detail_x: number of triangle subdivisions in x-dimension
    :type detail_x: integer

    :param detail_y: number of triangle subdivisions in y-dimension
    :type detail_y: integer

    """

    def __init__(self, detail_x=1, detail_y=1):
        self.vertices = []

        self.line_vertices = []

        self.line_normals = []

        self.vertex_normals = []

        self.faces = []

        self.uvs = []
        # a 2D array containing edge connectivity pattern for create line vertices
        # based on faces for most objects
        self.edges = []
        self.detail_x = detail_x
        self.detail_y = detail_y

        self.stroke_indices = []

        self.matrix = np.identity(4)
        self.material = p5.renderer.style.material

    def reset(self):
        """
        Reset geometry parameters
        """
        self.vertices = []
        self.line_vertices = []
        self.line_normals = []
        self.vertex_normals = []
        self.faces = []
        self.uvs = []
        self.edges = []

    def compute_faces(self):
        """
        Adds the faces for the geometry for predefined order of vertices
        """
        self.faces = []
        sliceCount = self.detail_x + 1
        for i in range(self.detail_y):
            for j in range(self.detail_x):
                a = i * sliceCount + j
                b = i * sliceCount + j + 1
                c = (i + 1) * sliceCount + j + 1
                d = (i + 1) * sliceCount + j
                self.faces.append([a, b, d])
                self.faces.append([d, b, c])

    def make_triangle_edges(self):
        """
        Adds the edges to the geometry based on the faces
        """
        self.edges = []
        for j in range(len(self.faces)):
            self.edges.append([self.faces[j][0], self.faces[j][1]])
            self.edges.append([self.faces[j][1], self.faces[j][2]])
            self.edges.append([self.faces[j][2], self.faces[j][0]])

    def get_face_normal(self, faceId):
        """
        Returns the normal for a given face
        """
        face = self.faces[faceId]
        vA = np.array(self.vertices[face[0]])
        vB = np.array(self.vertices[face[1]])
        vC = np.array(self.vertices[face[2]])
        ab = vB - vA
        ac = vC - vA
        n = np.cross(ab, ac)
        ln = np.linalg.norm(n)

        sinAlpha = ln / (np.linalg.norm(ab) * np.linalg.norm(ac))
        if sinAlpha > 1:
            sinAlpha = 1

        return n * math.sin(sinAlpha) / ln

    def compute_normals(self):
        """
        Compute normals for every vertex
        """
        self.vertex_normals = []
        for iv in range(len(self.vertices)):
            self.vertex_normals.append([0, 0, 0])

        for f in range(len(self.faces)):
            face = self.faces[f]
            face_normal = self.get_face_normal(f)

            for fv in range(3):
                vertex_index = face[fv]
                self.vertex_normals[vertex_index] += face_normal

        for iv in range(len(self.vertices)):
            self.vertex_normals[iv] = self.vertex_normals[iv] / np.linalg.norm(
                self.vertex_normals[iv]
            )

    def edges_to_vertices(self):
        self.line_vertices = []
        self.line_normals = []

        for i in range(len(self.edges)):
            begin = self.vertices[self.edges[i][0]]
            end = self.vertices[self.edges[i][1]]

            direction = np.array(end) - np.array(begin)
            direction = direction / np.linalg.norm(direction)
            direction = direction.tolist()

            a = begin
            b = begin
            c = end
            d = end
            dirAdd = direction
            dirSub = direction
            dirAdd.append(1)
            dirSub.append(-1)

            self.line_normals.extend([dirAdd, dirSub, dirAdd, dirAdd, dirSub, dirSub])
            self.line_vertices.extend([a, b, c, c, b, d])

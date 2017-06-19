#
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

class Matrix:
    """Represents a 4x4 matrix."""
    def __init__(self, *v):
        self.values = v
        self._inverse = None

    @property
    def values(self):
        return tuple(self._values)

    @values.setter
    def values(self, v):
        if len(v) == 0:
            self._values = [
                1, 0, 0, 0,
                0, 1, 0, 0,
                0, 0, 1, 0,
                0, 0, 0, 1
            ]            
        elif len(values) == 6:
            self._values = [
                v[0], v[1], v[2],   0,
                v[3], v[4], v[5],   0,
                   0,    0,    1,   0,
                   0,    0,    0,   1
            ]
        elif len(values) == 9:
            self._values = [
                v[0], v[1], v[2],   0,
                v[3], v[4], v[5],   0,
                v[6], v[7], v[8],   0,
                   0,    0,    0,   1
            ]
        elif len(values) == 16:
            self._values = list(v)
        else:
            raise ArithmeticError("Couldn't set Matrix values."
                                  "Wrong number of arguments.")

        self._inverse = None

    def reset(self):
        self.values = []

    @staticmethod
    def identity():
        return Matrix()

    def __add__(self, other):
        computed = [ sum(c) for c in zip(self.values, other.values) ]
        return Matrix(*computed)

    def __mult__(self, other):
        computed = [ si*oi for si, oi in zip(self.values, other.values) ]
        return Matrix(*computed)
        
    def __getitem__(self, idx):
        return self._values[4*idx[0] + idx[1]]

    def __setitem__(self, idx, val):
        self._values[4*idx[0] + idx[1]] = val

    def __repr__(self):
        return "Matrix(\n[" + \
               " ]\n[".join(["".join(" {}".format(i)
                                     for i in self._values[k:k+4])
                             for k in range(4)]) + \
                " ]\n)"

    __str__ = __repr__

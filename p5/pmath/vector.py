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
from __future__ import annotations
from typing import Optional, NamedTuple
import numpy as np
from numpy.typing import NDArray
from numpy.random import random

__all__ = ["Vector", "Point"]

# Floating point precision for vectors.
EPSILON = 1e-8


class Point(NamedTuple):
    x: float = None
    y: float = None
    z: float = 0


class Vector(Point):
    """Describes a vector in two or three dimensional space.

    A Vector -- specifically an Euclidean (or geometric) vector -- in
    two or three dimensional space is a geometric entity that has some
    magnitude (or length) and a direction.

    Examples::

        >>> vec_2d = Vector(3, 4)
        >>> vec_2d
        Vector(3.00, 4.00, 0.00)

        >>> vec_3d = Vector(2, 3, 4)
        >>> vec_3d
        Vector(2.00, 3.00, 4.00)

    :param x: The x-component of the vector.

    :param y: The y-component of the vector.

    :param z: The z-component of the vector (0 by default; only
        required for 3D vectors; )

    """

    def __init__(self, x: float, y: float, z: float = 0):
        self._array: NDArray[np.float32] = np.array([x, y, z], dtype=np.float32)

    @property
    def x(self) -> float:
        """The x-component of the point."""
        return self._array[0]

    @x.setter
    def x(self, value: float):
        self._array[0] = value

    @property
    def y(self) -> float:
        """The y-component of the point."""
        return self._array[1]

    @y.setter
    def y(self, value: float):
        self._array[1] = value

    @property
    def z(self) -> float:
        """The z-component of the point."""
        return self._array[2]

    @z.setter
    def z(self, value: float):
        self._array[2] = value

    def distance(self, other: Vector) -> float:
        """Return the distance between two points.

        :returns: The distance between the current point and the given
            point.

        """
        return np.sqrt(((self._array - other._array) ** 2).sum())

    dist = distance

    def lerp(self, other: Vector, amount: float) -> Vector:
        """Linearly interpolate from one point to another.

        :param other: Point to be interpolate to.

        :param amount: Amount by which to interpolate.
        :type amount: float

        :returns: Vector obtained by linearly interpolating this
            vector to the other vector by the given amount.

        """
        x, y, z = self._array + amount * (other._array - self._array)
        return self.__class__(x, y, z)

    def __add__(self, other: Vector):
        """Add the location of one point to that of another.

        Examples::

            >>> p = Vector(2, 3, 6)
            >>> q = Vector(3, 4, 5)
            >>> p + q
            Vector(5.00, 7.00, 11.00)

        :param other:

        :returns: The point obtained by adding the corresponding
            components of the two vectors.

        """
        x, y, z = self._array + other._array
        return self.__class__(x, y, z)

    def __sub__(self, other: Vector):
        """Subtract the location of one point from that of another.

        Examples::

            >>> p = Vector(2, 3, 6)
            >>> q = Vector(3, 4, 5)
            >>> p - q
            Vector(-1.00, -1.00, 1.00)

        :param other:
        :returns: The vector obtained by subtracteing  the corresponding
            components of the vector from those of another.

        """
        x, y, z = self._array - other._array
        return self.__class__(x, y, z)

    def __mul__(self, k: float):
        """Multiply the point by a scalar.

        Examples::

            >>> p = Vector(2, 3, 6)
            >>> p * 2
            Vector(4.00, 6.00, 12.00)

            >>> 2 * p
            Vector(4.00, 6.00, 12.00)

            >>> p * p
            Traceback (most recent call last):
                ...
            TypeError: Can't multiply/divide a point by a non-numeric.

            >>> p = Vector(2, 3, 6)
            >>> -p
            Vector(-2.00, -3.00, -6.00)

            >>> p = Vector(2, 3, 6)
            >>> p / 2
            Vector(1.00, 1.50, 3.00)

        :param k:
        :returns: The vector obtained by multiplying each component of
            `self` by k.

        :raises TypeError: When `k` is non-numeric.

        """
        if isinstance(k, (int, float)):
            x, y, z = k * self._array
            return self.__class__(x, y, z)
        raise TypeError("Can't multiply/divide a point by a non-numeric.")

    def __rmul__(self, other):
        return self * other

    def __neg__(self):
        """Negate the vector."""
        return (-1) * self

    def __truediv__(self, other):
        """Divide the vector by a scalar."""
        return self * (1 / other)

    def cross(self, other: Vector) -> Vector:
        """Return the cross product of the two vectors.

        Examples::

            >>> i = Vector(1, 0, 0)
            >>> j = Vector(0, 1, 0)
            >>> i.cross(j)
            Vector(0.00, 0.00, 1.00)

        :param other:
        :returns: The vector perpendicular to both `self` and `other`
            i.e., the vector obtained by taking the cross product of
            `self` and `other`.

        """
        x, y, z = np.cross(self._array, other._array)
        return self.__class__(x, y, z)

    def dot(self, other: Vector) -> float:
        """Compute the dot product of two vectors.

        Examples::

            >>> p = Vector(2, 3, 6)
            >>> q = Vector(3, 4, 5)
            >>> p.dot(q)
            48
            >>> p @ q
            48

        :param other:
        :returns: The dot product of the two vectors.

        """
        return np.dot(self._array, other._array)

    @property
    def angle(self):
        """The angle of rotation of the vector (in radians).

        This attribute isn't available for three dimensional vectors.


        Examples::

            >>> from math import pi, isclose
            >>> p = Vector(1, 0, 0)
            >>> isclose(p.angle, 0)
            True

            >>> p = Vector(0, 1, 0)
            >>> isclose(p.angle, pi/2)
            True

            >>> p = Vector(1, 1, 1)
            >>> p.angle
            Traceback (most recent call last):
                ...
            ValueError: Can't compute the angle for a 3D vector.

            >>> p = Vector(1, 1)
            >>> isclose(p.angle, pi/4)
            True
            >>> p.angle = pi/2
            >>> isclose(p.angle, pi/2)
            True

            >>> p = Vector(1, 1)
            >>> isclose(p.angle, pi/4)
            True
            >>> p.rotate(pi/4)
            >>> isclose(p.angle, pi/2)
            True

        :raises ValueError: If the vector is three-dimensional

        """
        if np.abs(self.z) > EPSILON:
            raise ValueError("Can't compute the angle for a 3D vector.")
        return np.arctan2(self.y, self.x)

    @angle.setter
    def angle(self, theta):
        self.rotate(theta - self.angle)

    def rotate(self, theta: float):
        """Rotates the vector by an angle.

        :param theta: Angle (in radians).

        """
        x = self.x * np.cos(theta) - self.y * np.sin(theta)
        y = self.x * np.sin(theta) + self.y * np.cos(theta)
        self.x = x
        self.y = y

    def angle_between(self, other: Vector) -> float:
        """Calculate the angle between two vectors.

        Examples::

            >>> from math import degrees
            >>> k = Vector(0, 1)
            >>> j = Vector(1, 0)
            >>> degrees(k.angle_between(j))
            90.0

        :param other:

        :returns: The angle between `self` and `other` (in radians)

        """
        return np.arccos(
            (np.dot(self._array, other._array)) / (self.magnitude * other.magnitude)
        )

    @property
    def magnitude(self) -> float:
        """The magnitude of the vector.

        Examples::

            >>> p = Vector(2, 3, 6)
            >>> p.magnitude
            7.0

            >>> abs(p)
            7.0

            >>> p.magnitude = 14
            >>> p
            Vector(4.00, 6.00, 12.00)

            >>> p.normalize()
            >>> print(p)
            Vector(0.29, 0.43, 0.86)

        """
        return np.sqrt(np.dot(self._array, self._array))

    @magnitude.setter
    def magnitude(self, new_magnitude):
        current_magnitude = self.magnitude
        self._array = (new_magnitude * self._array) / current_magnitude

    def mag(self) -> float:
        return self.magnitude

    @property
    def magnitude_sq(self) -> float:
        """The squared magnitude of the vector."""
        return np.dot(self._array, self._array)

    @magnitude_sq.setter
    def magnitude_sq(self, new_magnitude_sq):
        self.magnitude = np.sqrt(new_magnitude_sq)

    def __abs__(self):
        """Return the magnitude of the vector."""
        return self.magnitude

    def normalize(self):
        """Set the magnitude of the vector to one."""
        if self.magnitude == 0.0:
            raise ValueError("Vector has magnitude 0; can't normalize.")
        self.magnitude = 1
        return self

    def limit(
        self, upper_limit: Optional[float] = None, lower_limit: Optional[float] = None
    ):
        """Limit the magnitude of the vector to the given range.

        :param upper_limit: The upper limit for the limiting range
            (defaults to None).

        :param lower_limit: The lower limit for the limiting range
            (defaults to None).

        """
        magnitude = self.magnitude
        if upper_limit is None:
            upper_limit = magnitude
        if lower_limit is None:
            lower_limit = magnitude

        if magnitude < lower_limit:
            self.magnitude = lower_limit
        elif magnitude > upper_limit:
            self.magnitude = upper_limit

    def __matmul__(self, other):
        return self.dot(other)

    @classmethod
    def from_angle(cls, angle: float):
        """Return a new unit vector with the given angle.

        :param angle: Angle to be used to create the vector (in
            radians).
        """
        vec = cls.random_2D()
        vec.angle = angle
        return vec

    @classmethod
    def random_2D(cls):
        """Return a random 2D unit vector."""
        x, y = 2 * (random(2) - 0.5)
        vec = cls(x, y)
        vec.normalize()
        return vec

    @classmethod
    def random_3D(cls):
        """Return a new random 3D unit vector."""
        x, y, z = random(3)
        vec = cls(x, y, z)
        vec.normalize()
        return vec

    def copy(self) -> Vector:
        """Return a copy of the current point.

        :returns: A copy of the current point.

        """
        x, y, z = self._array
        return self.__class__(x, y, z)

    def __setitem__(self, key: int, value: float):
        self._array[key] = value

    def __getitem__(self, key: int):
        return self._array[key]

    def __iter__(self):
        """Return the components of the vector as an iterator.

        Examples::

            >>> p = Vector(2, 3, 4)
            >>> print([ c for c in p])
            [2, 3, 4]

        """
        yield from self._array

    def __eq__(self, other):
        if hasattr(other, "_array") and self._array.shape == other._array.shape:
            return np.all(np.absolute(self._array - other._array) < EPSILON)
        return False

    def __neq__(self, other):
        if hasattr(other, "_array") and self._array.shape == other._array.shape:
            return not np.all(np.absolute(self._array - other._array) < EPSILON)
        return True

    def __repr__(self):
        class_name = self.__class__.__name__
        return f"{class_name}({self.x:.2f}, {self.y:.2f}, {self.z:.2f})"

    __str__ = __repr__

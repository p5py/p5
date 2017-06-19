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

import math

class Vector:
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

    :type x: int or float
    :type y: int or float
    :type z: int or float

    """

    def __init__(self, x, y, z=0):
        #: The x-component of the vector.
        self.x = x

        #: The y-component of the vector.
        self.y = y

        #: The z-component of the vector.
        #:
        #: This attribute is only required for three dimensional
        #: vectors. Defaults to 0.
        self.z = z

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
            AssertionError: Can't compute the angle for a 3D vector.

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

        :raises AssertionError: If the vector is three-dimensional

        """
        # TODO (abhikpal, 2017-05-25):
        #    An assertion error when the value is undefined doens't
        #    sound "right". Raise some other error instead?
        assert self.z == 0, "Can't compute the angle for a 3D vector."
        return math.atan2(self.y, self.x)

    @angle.setter
    def angle(self, theta):
        self.rotate(theta -  self.angle)

    def rotate(self, theta):
        """Rotates the vector by an angle.
        
        :param theta: Angle (in radians).
        :type theta: float or int

        """
        self.x = self.x * math.cos(theta) - self.y * math.sin(theta)
        self.y = self.x * math.sin(theta) + self.y * math.cos(theta)

    def angle_between(self, other):
        """Calculate the angle between two vectors."""
        # TODO (abhikpal, 2017-05-25):
        #     Use a @ b == abs(a) * abs(b) * cos(theta) to get the req. angle.
        raise NotImplementedError

    @property
    def magnitude(self):
        """The magnitude of the vector.

        Examples::

            >>> p = Vector(2, 3, 6)
            >>> p.magnitude
            7.0

            >>> abs(p)
            7.0

            >>> p.magnitude = 14
            >>> p
            Vector(4.0, 6.0, 12.0)

            >>> p.normalize()
            >>> print(p)
            Vector(0.29, 0.43, 0.86)

        """
        return math.sqrt(self.dot(self))

    @magnitude.setter
    def magnitude(self, new_magnitude):
        current_magnitude = self.magnitude
        self.x = (self.x / current_magnitude) * new_magnitude
        self.y = (self.y / current_magnitude) * new_magnitude
        self.z = (self.z / current_magnitude) * new_magnitude

    @property
    def magnitude_sq(self):
        """The squared magnitude of the vector."""
        return self.dot(self)

    @magnitude_sq.setter
    def magnitude(self, new_magnitude_sq):
        self.magnitude = math.sqrt(new_magnitude_sq)

    def __abs__(self):
        """Return the magnitude of the vector."""
        return self.magnitude

    def normalize(self):
        """Set the magnitude of the vector to one."""
        self.magnitude = 1

    def __iter__(self):
        """Return the components of the vector as an iterator.

        Examples::

            >>> p = Vector(2, 3, 4)
            >>> print([ c for c in p])
            [2, 3, 4]

        """
        yield self.x
        yield self.y
        yield self.z

    def __add__(self, other):
        """Add two vectors.

        Examples::

            >>> p = Vector(2, 3, 6)
            >>> q = Vector(3, 4, 5)
            >>> p + q
            Vector(5.00, 7.00, 11.00)

        :param other:
        :type other: Vector
        :returns: The vector obtained by adding the corresponding
            components of the two vectors.
        :rtype: Vector

        """
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        """Subtract one vector from another.

        Examples::

            >>> p = Vector(2, 3, 6)
            >>> q = Vector(3, 4, 5)
            >>> p - q
            Vector(-1.00, -1.00, 1.00)

        :param other:
        :type other: Vector
        :returns: The vector obtained by subtracteing  the corresponding
            components of the vector from those of another.
        :rtype: Vector

        """
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, k):
        """Multiply the vector by a scalar.

        Examples::

            >>> p = Vector(2, 3, 6)
            >>> p * 2
            Vector(4.00, 6.00, 12.00)

            >>> 2 * p
            Vector(4.00, 6.00, 12.00)

            >>> p * p
            Traceback (most recent call last):
                ...
            TypeError: Can't multiply/divide a vector by a non-numeric.

            >>> p = Vector(2, 3, 6)
            >>> -p
            Vector(-2.00, -3.00, -6.00)

            >>> p = Vector(2, 3, 6)
            >>> p / 2
            Vector(1.00, 1.50, 3.00)

        :param k:
        :type k: int, float
        :returns: The vector obtained by multiplying each component of
            `self` by k.
        :rtype: Vector
        :raises TypeError: When `k` is non-numeric.

        """
        if isinstance(k, int) or isinstance(k, float):
            return Vector(self.x * k, self.y * k, self.z * k)
        raise TypeError("Can't multiply/divide a vector by a non-numeric.")

    def __rmul__(self, other):
        return self * other

    def __neg__(self):
        """Negate the vector."""
        return -1 * self

    def __truediv__(self, other):
        """Divide the vector by a scalar."""
        return self * (1 / other)

    def cross(self, other):
        """Return the cross product of the two vectors.

        Examples::

            >>> i = Vector(1, 0, 0)
            >>> j = Vector(0, 1, 0)
            >>> i.cross(j)
            Vector(0.00, 0.00, 1.00)

        :param other:
        :type other: Vector
        :returns: The vector perpendicular to both `self` and `other`
            i.e., the vector obtained by taking the cross product of
            `self` and `other`.
        :rtype: Vector

        """
        return Vector(self.y * other.z - self.z * other.y,
                      self.z * other.x - self.x * other.z,
                      self.x * other.y - self.y * other.x)

    def dot(self, other):
        """Compute the dot product of two vectors.

        Examples::

            >>> p = Vector(2, 3, 6)
            >>> q = Vector(3, 4, 5)
            >>> p.dot(q)
            48
            >>> p @ q
            48

        :param other:
        :type other: Vector
        :returns: The dot product of the two vectors.
        :rtype: int or float

        """
        return sum(sc*oc for sc, oc in zip(self, other))

    def __matmul__(self, other):
        return self.dot(other)

    def __repr__(self):
        return "Vector({:.2f}, {:.2f}, {:.2f})".format(self.x, self.y, self.z)

    __str__ = __repr__

    # TODO (abhikpal, 2017-05-26):
    #    - comparison magic methods (__eq__, etc)
    #    - limit -- limit the magnitude of the vector
    #    - lerp -- Linearly interpolate one vec to another.
    #    - random_2d
    #    - random_3d

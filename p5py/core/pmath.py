import math
import random as rnd

TAU = math.pi * 2
HALF_TAU = math.pi

TWO_PI = TAU
PI = HALF_TAU
HALF_PI = PI / 2.0
QUARTER_PI = PI / 4.0

class Vector:
    def __init__(self, x, y, z = 0):
        """
        >>> Vector(3, 4)
        Vector(3, 4, 0)
        >>> Vector(2, 3, 4)
        Vector(2, 3, 4)
        """
        self.x = x
        self.y = y
        self.z = z

    @property
    def magnitude(self):
        """
        Return the magnitude of the vector.

        >>> p = Vector(2, 3, 6)
        >>> p.magnitude
        7.0
        """
        return math.sqrt(self @ self)

    @magnitude.setter
    def magnitude(self, value):
        """
        Set the magnitude of the vector.

        >>> p = Vector(2, 3, 6)
        >>> p.magnitude
        7.0
        >>> p.magnitude = 14
        >>> p
        Vector(4, 6, 12)
        """
        m = self.magnitude
        self.x = (self.x / m) * value
        self.y = (self.y / m) * value
        self.z = (self.z / m) * value

    def __abs__(self):
        """
        Return the magnitude of the vector.

        >>> p = Vector(2, 3, 6)
        >>> abs(p)
        7.0
        """
        return self.magnitude
        
    def normalize(self):
        """
        Set the magnitude of the vector to one.

        >>> p = Vector(2, 3, 6)
        >>> p.normalize()
        >>> print(p)
        Vector(0.29, 0.43, 0.86)
        """
        self.magnitude = 1
    
    def __iter__(self):
        """
        Return an the components of the vector as an iterator.

        >>> p = Vector(2, 3, 4)
        >>> list(p)
        [2, 3, 4]
        >>> for c in p:
        ...     print(c)
        2
        3
        4
        """
        yield self.x
        yield self.y
        yield self.z

    def __add__(self, other):
        """
        Add two vectors.

        >>> p = Vector(2, 3, 6)
        >>> q = Vector(3, 4, 5)
        >>> p + q
        Vector(5, 7, 11)
        """
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        """
        Subtract one vector from another.

        >>> p = Vector(2, 3, 6)
        >>> q = Vector(3, 4, 5)
        >>> p - q
        Vector(-1, -1, 1)
        """
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        """
        If other is a vector, return the cross product else
        return the vector obtained by performing scalar
        multiplication.

        >>> p = Vector(2, 3, 6)
        >>> p * 2
        Vector(4, 6, 12)
        >>> 2 * p
        Vector(4, 6, 12)
        >>> i = Vector(1, 0, 0)
        >>> j = Vector(0, 1, 0)
        >>> i * j
        Vector(0, 0, 1)
        """
        if type(other) == type(self):
            return Vector(self.y * other.z - self.z * other.y,
                          self.z * other.x - self.x * other.z,
                          self.x * other.y - self.y * other.x)
        return other * self      

    def __rmul__(self, other):
        """
        Multiply a vector by a scalar.
        """
        return Vector(self.x * other, self.y * other, self.z * other)        

    def __matmul__(self, other):
        return sum(sc*oc for sc, oc in zip(self, other))
    
    def __neg__(self):
        """
        >>> p = Vector(2, 3, 6)
        >>> -p
        Vector(-2, -3, -6)
        """
        return (-1 * self)
        
    def __truediv__(self, other):
        """
        >>> p = Vector(2, 3, 6)
        >>> p / 2
        Vector(1.0, 1.5, 3.0)
        >>> q = Vector(3, 4, 0)
        >>> p / q
        Traceback (most recent call last):
            ...
        TypeError: Cannot divide two vectors
        """
        if type(self) == type(other):
            raise TypeError("Cannot divide two vectors")
        return Vector(self.x / other, self.y / other, self.z / other)

    
    def dot(self, other):
        """
        >>> p = Vector(2, 3, 6)
        >>> q = Vector(3, 4, 5)
        >>> p.dot(q)
        48
        """
        return self @ other

    def cross(self, other):
        return self * other

    def limit(self):
        """
        Limit the magnitude of this vector.
        """
        pass

    @property
    def heading(self):
        """Calculate the angle of rotation for this Vector"""
        pass

    @heading.setter
    def heading(self, angle):
        """
        """
        pass
    
    def rotate(self):
        """Rotate the given vector by an angle"""
        pass

    def lerp(self, other, amount):
        """
        Linearly interpolate one vector to another
        """
        return lerp(self, other)

    def angle_between(self, other, amount):
        """Calculate the angle between two vectors."""
        pass

    def random_2d(self):
        raise NotImplementedError

    def random_3d(self):
        raise NotImplementedError
    
    def __repr__(self):
        return "Vector({}, {}, {})".format(self.x, self.y, self.z)

    def __str__(self):
        return "Vector({:.2f}, {:.2f}, {:.2f})".format(self.x, self.y, self.z)


# A lot of these just wrap around their respective functions in the math
# module. We do this so that
#   1. we get to have custom doc strings
#   2. we don't have to -- in other files -- import from math (we could
#       do also do this by hacking the __all__, but we want our 
#       doc-strings and changing the __doc__ manually looks ugly. )


# def abs():
#     raise NotImplementedError

# def ceil():
#     raise NotImplementedError

# def constrain():
#     raise NotImplementedError

# def dist():
#     raise NotImplementedError

# def exp():
#     raise NotImplementedError

# def floor():
#     raise NotImplementedError

def lerp(start, stop, amount):
    """
    Linearly interpolate start to stop.

    >>> lerp(0, 100, 0.5)
    50.0

    """
    return start + (stop - start) * amount

# def log():
#     raise NotImplementedError

# def mag():
#     raise NotImplementedError

# def map():
#     raise NotImplementedError

# def max():
#     raise NotImplementedError

# def min():
#     raise NotImplementedError

# def norm():
#     raise NotImplementedError

# def pow():
#     raise NotImplementedError

# def round():
#     raise NotImplementedError

# def sq(n):
#     """Squares a number."""
#     return n**2

# def sqrt():
#     raise NotImplementedError

# def acos():
#     raise NotImplementedError

# def asin():
#     raise NotImplementedError

# def atan():
#     raise NotImplementedError

# def atan2():
#     raise NotImplementedError

# def cos():
#     raise NotImplementedError

# def degrees():
#     raise NotImplementedError

# def radians():
#     raise NotImplementedError

# def sin():
#     raise NotImplementedError

# def tan():
#     raise NotImplementedError


# def noise():
#     raise NotImplementedError

# def noiseDetail():
#     raise NotImplementedError

# def noiseSeed():
#     raise NotImplementedError

# def random():
#     raise NotImplementedError

# def randomGaussian():
#     raise NotImplementedError

# def randomSeed():
#     raise NotImplementedError

# def ceil():
#     raise NotImplementedError

# def constrain():
#     raise NotImplementedError

# def dist():
#     raise NotImplementedError

# def exp():
#     raise NotImplementedError

# def floor():
#     raise NotImplementedError

# def lerp():
#     raise NotImplementedError

# def random(high=1, low=0):
#     return rnd.uniform(low, high)

# def random_seed(seed):
#     return rnd.seed(seed)

# def random_gaussian(mean=0, sdev=1):
#     return rnd.gauss(mu=mean, sigma=sdev)

# def radians(angle):
#     """Returns the angle in radians for angle given in degrees"""
#     return math.radians(angle)

# def degrees(angle):
#     """Returns the angle in degrees for angle given in radians"""
#     return math.degrees(angle)

# def sin(angle, angle_mode='radians'):
#     """Returns the sin value for angle; angle_mode specifies the unit of
#     the angle."""
#     assert angle_mode in ['radians', 'degrees']
#     if angle_mode == 'degrees':
#         return math.sin(radians(angle))
#     return math.sin(angle)

# def cos(angle, angle_mode='radians'):
#     """Returns the cos value for angle; angle_mode specifies the unit of
#     the angle."""
#     assert angle_mode in ['radians', 'degrees']
#     if angle_mode == 'degrees':
#         return math.cos(radians(angle))
#     return math.cos(angle)

# def tan(angle, angle_mode='radians'):
#     """Returns the tan value for angle; angle_mode specifies the unit of
#     the angle."""
#     assert angle_mode in ['radians', 'degrees']
#     if angle_mode == 'degrees':
#         return math.tan(radians(angle))
#     return math.tan(angle)

# def asin(angle):
#     """Returns the asin value (in radians) for given sin value."""
#     return math.asin(angle)

# def acos(angle):
#     """Returns the acos value (in radians) for given cos value."""
#     return math.acos(angle)

# def atan(angle):
#     """Returns the atan value (in radians) for given tan value."""
#     return math.atan(angle)

# def atan2(angle):
#     """Returns the atan2 value (in radians) for given tan value."""
#     return math.atan2(angle)

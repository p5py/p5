# This file adds Processing API compatibility

from .curves import (
    bezier_detail,
    bezier_point,
    bezier_tangent,
    curve_point,
    curve_tightness,
    curve_detail,
    curve_tangent,
    quadratic_point,
)
from .rand import noise_detail, noise_seed, random_uniform, random_seed, random_gaussian


def bezierDetail(detailValue):
    """Change the resolution used to draw bezier curves.

    :param detailValue: New resolution to be used.
    :type detailValue: int
    """
    bezier_detail(detailValue)


def bezierPoint(start, control1, control2, stop, parameter):
    """Return the coordinate of a point along a bezier curve.

    :param start: The start point of the bezier curve
    :type start: float or n-tuple

    :param control1: The first control point of the bezier curve
    :type control1: float or n-tuple

    :param control2: The second control point of the bezier curve
    :type control2: float or n-tuple

    :param stop: The end point of the bezier curve
    :type stop: float or n-tuple

    :param parameter: The parameter for the required location along
        the curve. Should be in the range [0.0, 1.0] where 0 indicates
        the start of the curve and 1 indicates the end of the curve.
    :type parameter: float

    :returns: The coordinate of the point along the bezier curve.
    :rtype: float or n-tuple

    """
    return bezier_point(start, control1, control2, stop, parameter)


def bezierTangent(start, control1, control2, stop, parameter):
    """Return the tangent at a point along a bezier curve.

    :param start: The start point of the bezier curve
    :type start: float or n-tuple.

    :param control1: The first control point of the bezier curve
    :type control1: float or n-tuple.

    :param control2: The second control point of the bezier curve
    :type control2: float or n-tuple.

    :param stop: The end point of the bezier curve
    :type stop: float or n-tuple.

    :param parameter: The parameter for the required tangent location
        along the curve. Should be in the range [0.0, 1.0] where 0
        indicates the start of the curve and 1 indicates the end of
        the curve.
    :type parameter: float

    :returns: The tangent at the required point along the bezier
        curve.
    :rtype: float or n-tuple

    """
    return bezier_tangent(start, control1, control2, stop, parameter)


def curveDetail(detailValue):
    """Change the resolution used to draw bezier curves.

    :param detailValue: New resolution to be used.
    :type detailValue: int
    """
    curve_detail(detailValue)


def curveTightness(amount):
    """Change the curve tightness used to draw curves.

    :param amount: new curve tightness amount.
    :type amount: int
    """
    curve_tightness(amount)


def curvePoint(point1, point2, point3, point4, parameter):
    """Return the coordinates of a point along a curve.

    :param point1: The first control point of the curve.
    :type point1: float or n-tuple.

    :param point2: The second control point of the curve.
    :type point2: float or n-tuple.

    :param point3: The third control point of the curve.
    :type point3: float or n-tuple.

    :param point4: The fourth control point of the curve.
    :type point4: float or n-tuple.

    :param parameter: The parameter for the required point location
        along the curve. Should be in the range [0.0, 1.0] where 0
        indicates the start of the curve and 1 indicates the end of
        the curve.
    :type parameter: float

    :returns: The coordinate of the point at the required location
        along the curve.
    :rtype: float or n-tuple

    """
    return curve_point(point1, point2, point3, point4, parameter)


def curveTangent(point1, point2, point3, point4, parameter):
    """Return the tangent at a point along a curve.

    :param point1: The first control point of the curve.
    :type point1: float or n-tuple.

    :param point2: The second control point of the curve.
    :type point2: float or n-tuple.

    :param point3: The third control point of the curve.
    :type point3: float or n-tuple.

    :param point4: The fourth control point of the curve.
    :type point4: float or n-tuple.

    :param parameter: The parameter for the required tangent location
        along the curve. Should be in the range [0.0, 1.0] where 0
        indicates the start of the curve and 1 indicates the end of
        the curve.
    :type parameter: float

    :returns: The tangent at the required point along the curve.
    :rtype: float or n-tuple

    """
    return curve_tangent(point1, point2, point3, point4, parameter)


def quadraticPoint(start, control, stop, parameter):
    """Return the coordinates of a point along a bezier curve.

    :param point1: The start point of the curve.
    :type point1: float or n-tuple.

    :param point3: The control point of the curve.
    :type point3: float or n-tuple.

    :param point4: The end point of the curve.
    :type point4: float or n-tuple.

    :param parameter: The parameter for the required point location
        along the curve. Should be in the range [0.0, 1.0] where 0
        indicates the start of the curve and 1 indicates the end of
        the curve.
    :type parameter: float

    :returns: The coordinate of the point at the required location
        along the curve.
    :rtype: float or n-tuple

    """
    return quadratic_point(start, control, stop, parameter)


def noiseDetail(octaves=4, falloff=0.5):
    """Adjust the level of noise detail produced by noise().

    :param octaves: The number of octaves to compute the noise for
        (defaults to 4).
    :type octaves: int

    :param falloff:
    :type falloff: float

    :note: For :code:`falloff` values greater than 0.5,
        :code:`noise()` will return values greater than 1.0.

    """
    noise_detail(octaves, falloff)


def noiseSeed(seed):
    """Set the seed value for :code:`noise()`

    By default :code:`noise()` produes different values each time the
    sketch is run. Setting the :code:`seed` parameter to a constant
    will make :code:`noise()` return the same values each time the
    sketch is run.

    :param seed: The required seed value.
    :type seed: int

    """
    noise_seed(seed)


def randomUniform(high=1, low=0):
    """Return a uniformly sampled random number.

    :param high: The upper limit on the random value (defaults to 1).
    :type high: float

    :param low: The lowe limit on the random value (defaults to 0).
    :type low: float

    :returns: A random number between :code:`low` and :code:`high`.
    :rtype: float

    """
    return random_uniform(high, low)


def randomGaussian(mean=0, stdDev=1):
    """Return a normally sampled random number.

    :param mean: The mean value to be used for the normal distribution
        (defaults to 0).
    :type mean: float

    :param std_dev: The standard deviation to be used for the normal
        distribution (defaults to 1).
    :type std_dev: float

    :returns: A random number selected from a normal distribution with
        the given :code:`mean` and :code:`std_dev`.
    :rtype: float

    """
    return random_gaussian(mean, stdDev)


def randomSeed(seed):
    """Set the seed used to generate random numbers.

    :param seed: The required seed value.
    :type seed: int
    """
    random_seed(seed)

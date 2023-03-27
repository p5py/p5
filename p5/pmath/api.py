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
from ..p5types import FloatOrNTuple


def bezierDetail(detailValue: int):
    """Change the resolution used to draw bezier curves.

    :param detailValue: New resolution to be used.
    """
    bezier_detail(detailValue)


def bezierPoint(
    start: FloatOrNTuple,
    control1: FloatOrNTuple,
    control2: FloatOrNTuple,
    stop: FloatOrNTuple,
    parameter: float,
) -> FloatOrNTuple:
    """Return the coordinate of a point along a bezier curve.

    :param start: The start point of the bezier curve

    :param control1: The first control point of the bezier curve

    :param control2: The second control point of the bezier curve

    :param stop: The end point of the bezier curve

    :param parameter: The parameter for the required location along
        the curve. Should be in the range [0.0, 1.0] where 0 indicates
        the start of the curve and 1 indicates the end of the curve.

    :returns: The coordinate of the point along the bezier curve.

    """
    return bezier_point(start, control1, control2, stop, parameter)


def bezierTangent(
    start: FloatOrNTuple,
    control1: FloatOrNTuple,
    control2: FloatOrNTuple,
    stop: FloatOrNTuple,
    parameter: float,
) -> FloatOrNTuple:
    """Return the tangent at a point along a bezier curve.

    :param start: The start point of the bezier curve

    :param control1: The first control point of the bezier curve

    :param control2: The second control point of the bezier curve

    :param stop: The end point of the bezier curve

    :param parameter: The parameter for the required tangent location
        along the curve. Should be in the range [0.0, 1.0] where 0
        indicates the start of the curve and 1 indicates the end of
        the curve.

    :returns: The tangent at the required point along the bezier
        curve.

    """
    return bezier_tangent(start, control1, control2, stop, parameter)


def curveDetail(detailValue: int):
    """Change the resolution used to draw bezier curves.

    :param detailValue: New resolution to be used.
    """
    curve_detail(detailValue)


def curveTightness(amount: int):
    """Change the curve tightness used to draw curves.

    :param amount: new curve tightness amount.
    """
    curve_tightness(amount)


def curvePoint(
    point1: FloatOrNTuple,
    point2: FloatOrNTuple,
    point3: FloatOrNTuple,
    point4: FloatOrNTuple,
    parameter: float,
) -> FloatOrNTuple:
    """Return the coordinates of a point along a curve.

    :param point1: The first control point of the curve.

    :param point2: The second control point of the curve.

    :param point3: The third control point of the curve.

    :param point4: The fourth control point of the curve.

    :param parameter: The parameter for the required point location
        along the curve. Should be in the range [0.0, 1.0] where 0
        indicates the start of the curve and 1 indicates the end of
        the curve.

    :returns: The coordinate of the point at the required location
        along the curve.

    """
    return curve_point(point1, point2, point3, point4, parameter)


def curveTangent(
    point1: FloatOrNTuple,
    point2: FloatOrNTuple,
    point3: FloatOrNTuple,
    point4: FloatOrNTuple,
    parameter: float,
) -> FloatOrNTuple:
    """Return the tangent at a point along a curve.

    :param point1: The first control point of the curve.

    :param point2: The second control point of the curve.

    :param point3: The third control point of the curve.

    :param point4: The fourth control point of the curve.

    :param parameter: The parameter for the required tangent location
        along the curve. Should be in the range [0.0, 1.0] where 0
        indicates the start of the curve and 1 indicates the end of
        the curve.

    :returns: The tangent at the required point along the curve.

    """
    return curve_tangent(point1, point2, point3, point4, parameter)


def quadraticPoint(
    start: FloatOrNTuple, control: FloatOrNTuple, stop: FloatOrNTuple, parameter: float
) -> FloatOrNTuple:
    """Return the coordinates of a point along a bezier curve.

    :param point1: The start point of the curve.

    :param point3: The control point of the curve.

    :param point4: The end point of the curve.

    :param parameter: The parameter for the required point location
        along the curve. Should be in the range [0.0, 1.0] where 0
        indicates the start of the curve and 1 indicates the end of
        the curve.

    :returns: The coordinate of the point at the required location
        along the curve.

    """
    return quadratic_point(start, control, stop, parameter)


def noiseDetail(octaves: int = 4, falloff: float = 0.5):
    """Adjust the level of noise detail produced by noise().

    :param octaves: The number of octaves to compute the noise for
        (defaults to 4).

    :param falloff:

    :note: For :code:`falloff` values greater than 0.5,
        :code:`noise()` will return values greater than 1.0.

    """
    noise_detail(octaves, falloff)


def noiseSeed(seed: int):
    """Set the seed value for :code:`noise()`

    By default :code:`noise()` produes different values each time the
    sketch is run. Setting the :code:`seed` parameter to a constant
    will make :code:`noise()` return the same values each time the
    sketch is run.

    :param seed: The required seed value.

    """
    noise_seed(seed)


def randomUniform(high: float = 1, low: float = 0) -> float:
    """Return a uniformly sampled random number.

    :param high: The upper limit on the random value (defaults to 1).

    :param low: The lowe limit on the random value (defaults to 0).

    :returns: A random number between :code:`low` and :code:`high`.

    """
    return random_uniform(high, low)


def randomGaussian(mean: float = 0, stdDev: float = 1) -> float:
    """Return a normally sampled random number.

    :param mean: The mean value to be used for the normal distribution
        (defaults to 0).

    :param std_dev: The standard deviation to be used for the normal
        distribution (defaults to 1).

    :returns: A random number selected from a normal distribution with
        the given :code:`mean` and :code:`std_dev`.

    """
    return random_gaussian(mean, stdDev)


def randomSeed(seed: int):
    """Set the seed used to generate random numbers.

    :param seed: The required seed value.
    """
    random_seed(seed)

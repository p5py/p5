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

import random

from ..pmath import constrain
from .utils import SINCOS_LENGTH
from .utils import PRE_COS

__all__ = [
    # PERLIN NOISE FUNCTIONS
    "noise",
    "noise_detail",
    "noise_seed",
    # RANDOM NUMBER GENERATION
    "random_uniform",
    "random_gaussian",
    "random_seed",
]

# Most of the perlin noise code is based on the original Processing
# implementation of the noise function. toxi (+ other folks) put a
# bunch of comments on the Processing version, and I've added them
# here too for context.
#
# All commets that were ported from Processing are prefixed with
# "#P:"
#
#         --- abhikpal (2017-08-04)

# P: PERLIN NOISE
# P:
# P: [toxi 040903]
# P: octaves and amplitude amount per octave are now user controlled via
# P: the noiseDetail() function.
# P:
# P: [toxi 030902]
# P: cleaned up code and now using bagel's cosine table to speed up
# P:
# P: [toxi 030901]
# P: implementation by the german demo group farbrausch as used in their
# P: demo "art": http://www.farb-rausch.de/fr010src.zip

# P: Default to medium smooth
PERLIN_OCTAVES = 4

# P: 50% redution per octave
PERLIN_FALLOFF = 0.5

PERLIN_YWRAPB = 4
PERLIN_YWRAP = 1 << PERLIN_YWRAPB
PERLIN_ZWRAPB = 8
PERLIN_ZWRAP = 1 << PERLIN_ZWRAPB
PERLIN_SIZE = 4095

# P: [toxi 031112]
# P: new vars needed due to recent change of cos table in PGraphics
PERLIN_COS_TABLE = PRE_COS
PERLIN_TWO_PI = SINCOS_LENGTH
PERLIN_PI = PERLIN_TWO_PI
PERLIN_PI >>= 1

PERLIN = None


def noise(x, y=0, z=0):
    """Return perlin noise value at the given location.

    :param x: x-coordinate in noise space.
    :type x: float

    :param y: y-coordinate in noise space.
    :type y: float

    :param z: z-coordinate in noise space.
    :type z: float

    :returns: The perlin noise value.
    :rtype: float

    """
    # TODO (abhikpal, 2017-08-04)
    #
    # REFACTOR THIS MESS.

    global PERLIN

    # P: [toxi 031112]
    # P: now adjusts to the size of the cosLUT used via
    # P: the new variables, defined above
    def noise_fsc(i):
        # P: using bagel's cosine table instead
        return 0.5 * (1 - PERLIN_COS_TABLE[int(i * PERLIN_PI) % PERLIN_TWO_PI])

    # P: [toxi 031112]
    # P: noise broke due to recent change of cos table in PGraphics
    # P: this will take care of it
    if PERLIN is None:
        PERLIN = [random.random() for _ in range(PERLIN_SIZE + 1)]

    x = (-1 * x) if x < 0 else x
    xi = int(x)
    xf = x - xi

    y = (-1 * y) if y < 0 else y
    yi = int(y)
    yf = y - yi

    z = (-1 * z) if z < 0 else z
    zi = int(z)
    zf = z - zi

    r = 0
    ampl = 0.5

    for i in range(PERLIN_OCTAVES):
        rxf = noise_fsc(xf)
        ryf = noise_fsc(yf)

        of = int(xi + (yi << PERLIN_YWRAPB) + (zi << PERLIN_ZWRAPB))
        n1 = PERLIN[of % PERLIN_SIZE]
        n1 += rxf * (PERLIN[(of + 1) % PERLIN_SIZE] - n1)
        n2 = PERLIN[(of + PERLIN_YWRAP) % PERLIN_SIZE]
        n2 += rxf * (PERLIN[(of + PERLIN_YWRAP + 1) & PERLIN_SIZE] - n2)
        n1 += ryf * (n2 - n1)

        of += PERLIN_ZWRAP
        n2 = PERLIN[of & PERLIN_SIZE]
        n2 += rxf * (PERLIN[(of + 1) % PERLIN_SIZE] - n2)
        n3 = PERLIN[(of + PERLIN_YWRAP) % PERLIN_SIZE]
        n3 += rxf * (PERLIN[(of + PERLIN_YWRAP + 1) % PERLIN_SIZE] - n3)

        n2 += ryf * (n3 - n2)
        n1 += noise_fsc(zf) * (n2 - n1)

        r += n1 * ampl
        ampl *= PERLIN_FALLOFF

        xi *= 2
        xf *= 2

        yi *= 2
        yf *= 2

        zi *= 2
        zf *= 2

        if xf >= 1:
            xi = xi + 1
            xf = xf - 1

        if yf >= 1:
            yi = yi + 1
            yf = yf - 1

        if zf >= 1:
            zi = zi + 1
            zf = zf - 1

    return r


def noise_detail(octaves=4, falloff=0.5):
    """Adjust the level of noise detail produced by noise().

    :param octaves: The number of octaves to compute the noise for
        (defaults to 4).
    :type octaves: int

    :param falloff:
    :type falloff: float

    :note: For :code:`falloff` values greater than 0.5,
        :code:`noise()` will return values greater than 1.0.

    """
    global PERLIN_OCTAVES
    global PERLIN_FALLOFF

    if octaves > 0:
        PERLIN_OCTAVES = octaves
    PERLIN_FALLOFF = constrain(falloff, 0, 1)


def noise_seed(seed):
    """Set the seed value for :code:`noise()`

    By default :code:`noise()` produes different values each time the
    sketch is run. Setting the :code:`seed` parameter to a constant
    will make :code:`noise()` return the same values each time the
    sketch is run.

    :param seed: The required seed value.
    :type seed: int

    """
    global PERLIN
    random_seed(seed)
    PERLIN = None


def random_uniform(high=1, low=0):
    """Return a uniformly sampled random number.

    :param high: The upper limit on the random value (defaults to 1).
    :type high: float

    :param low: The lowe limit on the random value (defaults to 0).
    :type low: float

    :returns: A random number between :code:`low` and :code:`high`.
    :rtype: float

    """
    return random.uniform(low, high)


def random_gaussian(mean=0, std_dev=1):
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
    return random.gauss(mean, std_dev)


def random_seed(seed):
    """Set the seed used to generate random numbers.

    :param seed: The required seed value.
    :type seed: int
    """
    random.seed(seed)

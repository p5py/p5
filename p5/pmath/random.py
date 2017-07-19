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

import random

__all__ = ['noise', 'noise_detail', 'noise_seed', 'random_uniform',
           'random_gaussian', 'random_seed']

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
    raise NotImplementedError()

# TODO: Double check the default falloff.
#
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
    raise NotImplementedError()

def noise_seed(seed):
    """Set the seed value for :code:`noise()`

    By default :code:`noise()` produes different values each time the
    sketch is run. Setting the :code:`seed` parameter to a constant
    will make :code:`noise()` return the same values each time the
    sketch is run.

    :param seed: The required seed value.
    :type seed: int

    """
    raise NotImplementedError()

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

import math
import random as rnd

# A lot of these just wrap around their respective functions in the math
# module. We do this so that
#   1. we get to have custom doc strings
#   2. we don't have to -- in other files -- import from math (we could
#       do also do this by hacking the __all__, but we want our 
#       doc-strings and changing the __doc__ manually looks ugly. )

def random(high=1, low=0):
    return rnd.uniform(low, high)

def random_seed(seed):
    return rnd.seed(seed)

def random_gaussian(mean=0, sdev=1):
    return rnd.gauss(mu=mean, sigma=sdev)

def radians(angle):
    """Returns the angle in radians for angle given in degrees"""
    return math.radians(angle)

def degrees(angle):
    """Returns the angle in degrees for angle given in radians"""
    return math.degrees(angle)

def sin(angle, angle_mode='radians'):
    """Returns the sin value for angle; angle_mode specifies the unit of
    the angle."""
    assert angle_mode in ['radians', 'degrees']
    if angle_mode == 'degrees':
        return math.sin(radians(angle))
    return math.sin(angle)

def cos(angle, angle_mode='radians'):
    """Returns the cos value for angle; angle_mode specifies the unit of
    the angle."""
    assert angle_mode in ['radians', 'degrees']
    if angle_mode == 'degrees':
        return math.cos(radians(angle))
    return math.cos(angle)

def tan(angle, angle_mode='radians'):
    """Returns the tan value for angle; angle_mode specifies the unit of
    the angle."""
    assert angle_mode in ['radians', 'degrees']
    if angle_mode == 'degrees':
        return math.tan(radians(angle))
    return math.tan(angle)

def asin(angle):
    """Returns the asin value (in radians) for given sin value."""
    return math.asin(angle)

def acos(angle):
    """Returns the acos value (in radians) for given cos value."""
    return math.acos(angle)

def atan(angle):
    """Returns the atan value (in radians) for given tan value."""
    return math.atan(angle)

def atan2(angle):
    """Returns the atan2 value (in radians) for given tan value."""
    return math.atan2(angle)

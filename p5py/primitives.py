from . import _p5

# we will pass around these shape objects internally to draw and
# render stuff. A Shape will contain attributes for changing its shape
# type -- POLY, LINE, etc -- and its shape attributes -- color,
# stroke, etc --.
class Shape:
    def __init__(self):
        raise NotImplementedError


@_p5.artist
def point(*args):
    """Returns a point Shape"""
    raise NotImplementedError

@_p5.artist
def line(*args):
    """Returns a line Shape"""

@_p5.artist
def rect(*args):
    """Returns a rect object."""
    raise NotImplementedError

# etc...

@_p5.attribute
def fill(*args):
    """Returns a new fill color for the sketch."""
    raise NotImplementedError

# etc...

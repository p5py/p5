#
# Part of p5py: A Python package based on Processing
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

from .backends import OpenGLRenderer

# The Sketch is the main state machine for the p5py application. It
# contains a `window` object and a `renderer` object that control,
# respectively, the window events and the low-level rendering for the
# sketch.
# 
class Sketch:
    def __init__(self, *args):
        raise NotImplementedError

    # render calls the sketch's renderer and asks it to draw the input
    # shape.
    def render(self, *args):
        # check what surface we are rendering onto (i.e., are we
        # drawing on the primary surface or on a secondary surface
        # created using create_graphics()).

        # check if we are using translate() and rotate() and then
        # apply the required transformations to the shape.

        # check if the shape has style attributes. if not, give it the
        # correct style attributes and/or fill in the missing ones.
        raise NotImplementedError

    def run(self, *args):
        # set up required handlers depending on how the sketch is
        # being run (i.e., are we running from a standalone script, or
        # are we running inside the REPL?)
        raise NotImplementedError

    # a decorator that will wrap around the "attribute setters" for
    # the sketch like fill, background, etc and modify internal state
    # variables.
    #
    #     @_p5.attribute
    #     def fill(*args, **kwargs):
    #         # code that returns a new color (after converting it
    #         # to the appropriate internal color object)
    def attribute(self, f):
        # take the function's return value and use the function's name
        # to change the required state variable.
        raise NotImplementedError

    # a decorator that will wrap around the the "artists" in the
    # sketch -- these are functions that draw stuff on the screen like
    # rect(), line(), etc.
    #
    #    @_p5.artist
    #    def rect(*args, **kwargs):
    #        # code that creates a rectangular Shape object and
    #        # returns it.
    def artist(self, f):
        # modify the function such that we first render the Shape
        # object before returning it.
        raise NotImplementedError

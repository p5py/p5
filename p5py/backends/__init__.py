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

#
# TODO (abhikpal, 2017-06-06);
#
# - Fill in the missing args for all methods (maybe after
#   OpenGLRenderer is done?)
#

class BaseRenderer:
    """Base abstraction layer for all renderers."""
    def __init__(self):
        raise NotImplementedError("Abstract")

    def initialize(self):
        """Initilization routine for the renderer."""
        raise NotImplementedError("Abstract")

    def check_support(self):
        """Check if the the system supports the current renderer.

        :returns: True if the renderer is supported.
        :rtype: bool

        :raises RuntimeError: if the renderer is not supported.
        """
        raise NotImplementedError("Abstract")

    def pre_render(self):
        """Run the pre-render routine(s).

        The pre_render is called before the renderer is used to draw
        anything in the current iteration of the draw*() loop. This
        method could, for instance:

        - reset the transformations for the viewport
        - clear the screen,
        - etc.
        """
        pass

    def render(self, shape):
        """Use the renderer to render the given shape.

        :param shape: The shape that needs to be rendered.
        :type shape: Shape
        """
        raise NotImplementedError("Abstract")

    def post_render(self):
        """Run the post-render routine(s).

        The post_render is called when we are done drawing things for
        the current iteration of the draw call. Any draw-loop specific
        cleanup steps should go here.
        """
        pass

    def clear(self):
        """Clear the screen."""
        raise NotImplementedError("Abstract")

    def cleanup(self):
        """Run the cleanup routine for the renderer.

        This is the FINAL cleanup routine for the renderer and would
        ideally be called when the program is about to exit.
        """
        pass

    def test_render(self):
        """Render the renderer's default test drawing.

        The render() methods requires a Shape object. In the absence
        of such an object/class the user should be able to check that
        the renderer is working by calling this method.
        """
        raise NotImplementedError("Abstract")

    def __repr__(self):
        print("{}( version: {} )".format(self.__class__.__name__, self.version))

    __str__ = __repr__

from .opengl import *

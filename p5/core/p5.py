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

"""Environment Variables for P5 sketches"""
from OpenGL.GLU import gluNewTess, gluTessCallback, GLU_TESS_VERTEX, GLU_TESS_BEGIN, GLU_TESS_END, GLU_TESS_ERROR, gluErrorString

sketch = None
renderer = None

# Tessellation
tess_callback_factory = lambda y: lambda x: print(y, x)
tess = gluNewTess()
gluTessCallback(tess, GLU_TESS_VERTEX, tess_callback_factory("Vertex"))
gluTessCallback(tess, GLU_TESS_END, lambda: print("End"))
gluTessCallback(tess, GLU_TESS_ERROR, lambda x: print("Error", gluErrorString(x)))
gluTessCallback(tess, GLU_TESS_BEGIN, tess_callback_factory("Begin"))

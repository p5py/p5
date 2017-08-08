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
"""Shader sources.
"""

# Default vertex and fragment shaders.
vertex_default = """
attribute vec3 position;
attribute vec4 color;

varying vec4 frag_color;

uniform mat4 modelview;
uniform mat4 projection;

void main()
{
    gl_Position = projection * modelview * vec4(position, 1.0);
    frag_color = color;
}
"""

fragment_default = """
varying vec4 frag_color;

void main()
{
    gl_FragColor = frag_color;
}
"""

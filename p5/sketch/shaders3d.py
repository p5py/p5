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
"""Shaders used by the main program"""

from collections import namedtuple
from .util import read_shader

ShaderSource = namedtuple('ShaderSource', 'vert frag')

# vertex shader
default_vertex_source = """
attribute vec3 position;
attribute vec4 color;

varying vec4 frag_color;

uniform mat4 projection;
uniform mat4 perspective_matrix;

void main()
{
    gl_Position = projection * perspective_matrix * vec4(position, 1.0);
    frag_color = color;
}
"""

default_fragment_source = """
varying vec4 frag_color;

void main()
{
    gl_FragColor = frag_color;
}
"""


# Shader sources to draw framebuffers textues.
fbuffer_vertex_source = """
attribute vec2 position;
attribute vec2 texcoord;

varying vec2 vert_tex_coord;

void main() {
    gl_Position = vec4(position, 0, 1);
    vert_tex_coord = texcoord;
}
"""

fbuffer_fragment_source = """
uniform sampler2D texture;
varying vec2 vert_tex_coord;

void main() {
    gl_FragColor = texture2D(texture, vert_tex_coord.st);
}
"""

src_default = ShaderSource(default_vertex_source, default_fragment_source)
src_fbuffer = ShaderSource(fbuffer_vertex_source, fbuffer_fragment_source)
src_normal = ShaderSource(read_shader('normal.vert'), read_shader('normal.frag'))

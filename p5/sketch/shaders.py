#
# Part of p5: A Python package based on Processing
# Copyright (C) 2017-2018 Abhik Pal
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

ShaderSource = namedtuple('ShaderSource', 'vert frag')

# vertex shader
default_vertex_source = """
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

default_fragment_source = """
varying vec4 frag_color;

void main()
{
    gl_FragColor = frag_color;
}
"""

# texture vertex shader
texture_vertex_source = """
attribute vec2 position;
attribute vec2 texcoord;

uniform mat4 transform;
uniform mat4 modelview;
uniform mat4 projection;

varying vec4 vertex_texcoord;

void main()
{
    gl_Position = projection * modelview * transform * vec4(position, 0.0, 1.0);
    vertex_texcoord = vec4(texcoord, 1.0, 1.0);
}
"""

# texture fragment shader
texture_fragment_source = """
uniform vec4 fill_color;
uniform sampler2D texture;

varying vec4 vertex_texcoord;

void main()
{
    gl_FragColor = texture2D(texture, vertex_texcoord.st) * fill_color;
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

# vertex shader
stroke_vertex_source = """
attribute vec3 pos;
attribute vec3 posPrev;
attribute vec3 posCurr;
attribute vec3 posNext;

attribute float marker;
attribute float cap;
attribute float join;
attribute float linewidth;
attribute float side;
attribute float join_type;
attribute float cap_type;

uniform vec4 color;

uniform mat4 modelview;
uniform mat4 projection;
uniform float height;

varying vec4 frag_color;
varying float v_linejoin;
varying float v_linecap;
varying float v_linewidth;
varying float v_join_type;
varying float v_cap_type;
varying float v_length;
varying float v_join; // > 1 if the vertex is stroke join
varying float v_cap;  // > 1 if the vertex is stroke cap 

varying vec3 v_tangentNext; // tangents for stroke join and cap methods
varying vec3 v_tangentPrev; // tangents for stroke join and cap methods

varying vec3 v_pos;

void main()
{   
    v_linejoin = 1.0;
    v_linecap = 1.0;

    float width = 1.0;

    bool join = false;
    bool cap = false;

    float pi = 3.1415926535897;

    if(linewidth > 1){
        width = linewidth;
    }

    vec3 tangentPrev = posPrev - posCurr;
    vec3 tangentNext = posNext - posCurr;
    vec3 lineTangent;
    vec3 outsideTangent;

    if(side > 0.0){
        lineTangent = normalize(tangentNext);
        outsideTangent = normalize(tangentPrev);
    } else{
        lineTangent = normalize(tangentPrev);
        outsideTangent = normalize(tangentNext);
    }

    // calculate a vector perpendicular to the line
    vec3 perpendicular = normalize(vec3(lineTangent.y, -lineTangent.x, 0.0));

    float angle = acos(dot(lineTangent, outsideTangent));
    vec3 bisector = normalize(lineTangent + outsideTangent);
    float alignment = dot(perpendicular, outsideTangent);

    float factor = 1; // multiplication factor to scale the length of bisector

    if(side > 0.0){ // left side
        if(alignment > 0.0){
            if(marker > 0.0){
                perpendicular = bisector;
                factor = cos(pi/2 - angle/2);
            } else{
                perpendicular = bisector;
                factor = cos(pi/2 - angle/2);
            }
        } else{
            if(marker > 0.0){
                perpendicular = -bisector;
                factor = cos(pi/2 - angle/2);
            } else{
                perpendicular = -bisector;
                factor = cos(pi/2 - angle/2);
            }
        }
    } else{ // right side
        if(alignment > 0.0){
            if(marker > 0.0){
                perpendicular = bisector;
                factor = cos(pi/2 - angle/2);
            } else{
                perpendicular = bisector;
                factor = cos(pi/2 - angle/2);
            }
        } else{
            if(marker > 0.0){
                perpendicular = -bisector;
                factor = cos(pi/2 - angle/2);
            } else{
                perpendicular = -bisector;
                factor = cos(pi/2 - angle/2);
            }
        }
    }

    // Cap or straight edge
    vec3 offset = vec3(0.0, 0.0, 0.0);
    if(tangentPrev.x == 0 && tangentPrev.y == 0){
        factor = 1.0;
        v_cap = 1.0;
        perpendicular = normalize(vec3(lineTangent.y, -lineTangent.x, 0.0));
        offset = -width/2*lineTangent;
    } else if(tangentNext.x == 0 && tangentNext.y == 0){
        factor = 1.0;
        v_cap = 1.0;
        perpendicular = normalize(vec3(lineTangent.y, -lineTangent.x, 0.0));
        offset = -width/2*lineTangent;
    } else if(length(bisector) == 0.0){
        v_cap = -1.0;
        factor = 1.0;
        perpendicular = normalize(vec3(lineTangent.y, -lineTangent.x, 0.0));
    } else{
        v_cap = -1.0;
    }

    gl_Position = projection * modelview * vec4(posCurr + offset + marker*width*perpendicular/2/factor, 1.0);
    frag_color = color;

    //Set vertex shader variables
    v_linewidth = width;
    v_cap_type = cap_type;
    v_join_type = join_type;
    v_pos = pos;

    if(side > 0.0){ // left side
        v_tangentNext = posNext - posCurr;
        v_tangentPrev = posPrev - posCurr;
        v_length = length(v_tangentNext);
    } else{ // right side
        v_tangentNext = posCurr - posPrev;
        v_tangentPrev = posCurr - posNext;
        v_length = length(v_tangentNext);
    }    
}
"""

stroke_fragment_source = """
varying vec4 frag_color;
varying float v_linejoin;
varying float v_linecap;
varying float v_linewidth;
varying float v_cap;

varying float v_join_type;
varying float v_cap_type;
varying vec3 v_pos;

varying vec3 v_tangentNext; // tangents for stroke join and cap methods
varying vec3 v_tangentPrev; // tangents for stroke join and cap methods
varying float v_length;

uniform float height;

void main()
{
    vec2 uv = gl_FragCoord.xy;
    float inside;

    vec3 p; // vector from fragment to vertex
    p = vec3(
            uv.x - v_pos.x,
            (height - uv.y) - v_pos.y,
            1.0
        );

    if(dot(v_tangentNext, p) < 0.0){
        // do nothing
    } else if(dot(v_tangentNext, p)/length(v_tangentNext) > v_length){
        // shift coordinates of p to next vertex
        p = vec3(
            uv.x - (v_pos.x + v_tangentNext.x),
            (height - uv.y) - (v_pos.y + v_tangentNext.y),
            1.0
        );
    } else{
        gl_FragColor = frag_color;
        return;
    }

    if(v_cap > 0.0){
        // render stroke cap
        if(v_cap_type == 0.0){ // PROJECT
            inside = 1.0;
        } else if(v_cap_type == 1.0){ // SQUARE
            inside = -1.0;
        }
        else if(v_cap_type == 2.0){ // ROUND
            inside = v_linewidth/2 - length(p);
        }
    } else{
        // render stroke join
        if(v_join_type == 0.0){ // MITER
            inside = 1.0;
        } else if(v_join_type == 1.0){ // BEVEL
            vec3 bisector = -normalize(normalize(v_tangentPrev) + normalize(v_tangentNext));
            inside = v_linewidth/2 - dot(p, bisector);

            if(inside > 0.0){
                inside = v_linewidth/2 - dot(p, -bisector);
            }
        }
        else if(v_join_type == 2.0){ // ROUND
            inside = v_linewidth/2 - length(p);
        }
    }

    if(inside > 0.0){
        gl_FragColor = frag_color;
    } else{
        // discard the fragment
        discard;
    }    
}
"""


src_default = ShaderSource(default_vertex_source, default_fragment_source)
src_texture = ShaderSource(texture_vertex_source, texture_fragment_source)
src_fbuffer = ShaderSource(fbuffer_vertex_source, fbuffer_fragment_source)
src_line = ShaderSource(stroke_vertex_source, stroke_fragment_source)

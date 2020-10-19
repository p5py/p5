attribute vec3 pos;
attribute vec3 posPrev;
attribute vec3 posCurr;
attribute vec3 posNext;
attribute vec4 color;

attribute float marker;
attribute float linewidth;
attribute float side;
attribute float join_type;
attribute float cap_type;

uniform mat4 modelview;
uniform mat4 projection;

varying vec4 frag_color;
varying float v_linewidth;
varying float v_join_type;
varying float v_cap_type;
varying float v_length;
varying float v_join; // > 1 if the vertex is stroke join
varying float v_cap;  // > 1 if the vertex is stroke cap 

varying vec3 v_tangentNext;
varying vec3 v_tangentPrev;

varying vec3 v_pos;

void main()
{   

    float width = 1.0;

    bool join = false;
    bool cap = false;

    float pi = 3.1415926535897;

    if(linewidth > 1){ // if width of line < 1, render line of width 1
        width = linewidth;
    }

    vec3 tangentPrev = posPrev - posCurr;
    vec3 tangentNext = posNext - posCurr;
    vec3 lineTangent;
    vec3 outsideTangent;

    if(side > 0.0){ // is this left/right side of line segment
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

    // For cap or straight edge
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

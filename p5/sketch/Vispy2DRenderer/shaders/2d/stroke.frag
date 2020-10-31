varying vec4 frag_color;
varying float v_linewidth;
varying float v_cap; // render cap or join

varying float v_join_type;
varying float v_cap_type;
varying vec3 v_pos;

varying vec3 v_tangentNext; // tangents for stroke join and cap methods
varying vec3 v_tangentPrev; // tangents for stroke join and cap methods
varying float v_length;


// The origin of fragment coordinates is located at bottom left .
// Hence, to convert it to top left, we need to know the height.
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

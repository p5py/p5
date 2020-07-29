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

// TODO: Unify default3d.vert and default2d.vert

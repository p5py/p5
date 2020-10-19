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

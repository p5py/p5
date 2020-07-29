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

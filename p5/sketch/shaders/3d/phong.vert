attribute vec3 normal;
attribute vec3 position;

varying vec3 v_normal;
varying vec3 v_position;

uniform mat4 projection;
uniform mat4 perspective;

void main()
{
    v_normal = normalize(normal);
    v_position = position;
    mat4 transform = projection * perspective;
    gl_Position = transform * vec4(position, 1.0);
}

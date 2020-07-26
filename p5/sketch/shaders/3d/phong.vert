attribute vec3 normal;
attribute vec3 position;

varying vec3 v_normal;
varying vec3 v_position;

uniform mat4 projection;
uniform mat4 perspective;
uniform mat3 normal_transform;

void main()
{
    v_normal = normal_transform * normal;
    v_position = position;
    mat4 transform = projection * perspective;
    gl_Position = transform * vec4(position, 1.0);
}

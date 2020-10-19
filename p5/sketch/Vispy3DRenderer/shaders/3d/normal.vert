attribute vec3 position;
attribute vec3 normal;

varying vec3 v_normal;

uniform mat4 projection;
uniform mat4 perspective;
uniform mat3 normal_transform;

void main()
{
    mat4 transform = projection * perspective;
    gl_Position = transform * vec4(position, 1.0);
    v_normal = normal_transform * normal;
}

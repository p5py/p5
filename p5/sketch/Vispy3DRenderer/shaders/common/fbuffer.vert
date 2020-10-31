attribute vec2 position;
attribute vec2 texcoord;

varying vec2 vert_tex_coord;

void main() {
    gl_Position = vec4(position, 0, 1);
    vert_tex_coord = texcoord;
}

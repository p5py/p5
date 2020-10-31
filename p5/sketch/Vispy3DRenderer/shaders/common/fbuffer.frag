uniform sampler2D texture;
varying vec2 vert_tex_coord;

void main() {
    gl_FragColor = texture2D(texture, vert_tex_coord.st);
}

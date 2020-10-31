uniform vec4 fill_color;
uniform sampler2D texture;

varying vec4 vertex_texcoord;

void main()
{
    gl_FragColor = texture2D(texture, vertex_texcoord.st) * fill_color;
}

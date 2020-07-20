precision mediump float;
varying vec3 v_normal;

void main()
{
    gl_FragColor = vec4(normalize(v_normal), 1.0);
}

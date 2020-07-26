precision mediump float;

uniform vec4 u_color;
uniform vec3 u_cam_pos;
uniform vec3 u_light_pos;
uniform vec3 u_light_intensity;

varying vec3 v_normal;
varying vec3 v_position;

void main() {
  vec3 temp = 0.05 * u_light_intensity; // ambient_coeff = 0.05
  vec3 d = u_light_pos - v_position.xyz;
  vec3 h = normalize(u_light_pos + u_cam_pos - 2 * v_position.xyz);
  // diffuse_coeff = 0.6
  temp += 0.6 * u_light_intensity / length(d) / length(d) * max(0, dot(v_normal.xyz, normalize(d))); // diffuse
  // specular_coeff = 0.8, p = 4
  temp += 0.8 * u_light_intensity / length(d) / length(d) * pow(max(dot(v_normal.xyz, h), 0), 4);
  gl_FragColor = vec4(temp, 1);
}

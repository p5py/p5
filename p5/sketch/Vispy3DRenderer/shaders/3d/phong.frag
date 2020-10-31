precision mediump float;

uniform vec3 u_cam_pos; // Camera position in world coordinates
uniform vec3 u_ambient_color; // Color of the material reflected when hit by ambient light
uniform vec3 u_diffuse_color; // Color of the material used when calculating the diffuse component of point or directional lights
uniform vec3 u_specular_color; // Color of the material used when calculating the specular component of point or directional lights
uniform float u_shininess; // Power of the cosine term in specular component

// Directional lights
uniform int u_directional_light_count;
uniform vec3 u_directional_light_dir[8];
uniform vec3 u_directional_light_color[8];
uniform vec3 u_directional_light_specular[8];

// Ambient lights
uniform int u_ambient_light_count;
uniform vec3 u_ambient_light_color[8];

// Point lights
uniform int u_point_light_count;
uniform vec3 u_point_light_pos[8];
uniform vec3 u_point_light_color[8];
uniform vec3 u_point_light_specular[8];
// Falloffs for point lights
uniform float u_const_falloff[8];
uniform float u_linear_falloff[8];
uniform float u_quadratic_falloff[8];

varying vec3 v_normal;
varying vec3 v_position;

vec3 fall_off(vec3 col, float d, int i) {
  if (u_const_falloff[i] != .0)
    col /= u_const_falloff[i];
  if (u_linear_falloff[i] != .0)
    col /= u_linear_falloff[i] * d;
  if (u_quadratic_falloff[i] != .0)
    col /= u_quadratic_falloff[i] * d * d;
  return col;
}

vec3 specular(vec3 light_color, vec3 l_dir) {
  if (dot(l_dir, v_normal) < 0.0) {
    return vec3(0, 0, 0);
  }
  vec3 h = normalize(l_dir + normalize(u_cam_pos - v_position));
  return u_specular_color * light_color * pow(max(dot(v_normal, h), 0), u_shininess);
}

vec3 diffuse(vec3 light_color, vec3 l_dir) {
  return u_diffuse_color * light_color * max(0, dot(v_normal, l_dir));
}

void main() {
  // Don't display anything if on the wrong side of normal
  if (dot(v_normal, u_cam_pos - v_position) < 0.0) {
    gl_FragColor = vec4(0, 0, 0, 0);
    return;
  }

  vec3 col = vec3(0, 0, 0);
  // Add ambient light contributions
  for (int i = 0; i < 8; i++) {
    if (i == u_ambient_light_count)
      break;
    col += u_ambient_color * u_ambient_light_color[i];
  }

  // Add directional light contributions
  for (int i = 0; i < 8; i++) {
    if (i == u_directional_light_count)
      break;
    vec3 l_dir = normalize(-u_directional_light_dir[i]);
    col += diffuse(u_directional_light_color[i], l_dir);
    col += specular(u_directional_light_specular[i], l_dir);
  }

  // Add point light contributions
  for (int i = 0; i < 8; i++) {
    if (i == u_point_light_count)
      break;
    vec3 l_delta = u_point_light_pos[i] - v_position;
    float d = length(l_delta);
    vec3 l_dir = normalize(l_delta);
    col += fall_off(diffuse(u_point_light_color[i], l_dir), d, i);
    col += fall_off(specular(u_point_light_specular[i], l_dir), d, i);
  }
  gl_FragColor = vec4(col, 1);
}

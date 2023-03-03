#version 330 core

out vec4 final_colors;

uniform vec2 u_resolution;
uniform float u_time_total_elapsed_s;
uniform vec3 u_sphere_position;
uniform vec3 u_light_position;

// ro = ray_origin = camera_position
// rd = ray_direction

int MAX_STEPS = 1000;
float MIN_DISTANCE = 0.001;
float MAX_DISTANCE = 10000;
float SHADOW_POINT_OFFSET = 0.002;

// ================================
// SDF functions

float sdf_sphere( vec3 sample_point, vec3 sphere_position, float sphere_radius )
{
    return length(sample_point - sphere_position) - sphere_radius;
}

float sdf_ground_plane( vec3 sample_point )
{
    return sample_point.y;
}

// ================================
// Scene definition

float get_scene_distance(vec3 sample_point )
{
    float scene_distance = sdf_sphere( sample_point, u_sphere_position, 1);
    scene_distance = min(scene_distance, sdf_ground_plane(sample_point));

    return scene_distance;
}

// ================================
// Common ray marching boilerplate

float ray_march( vec3 ray_origin, vec3 ray_direction )
{
    float marched_distance = 0;
    for( int i = 0; i < MAX_STEPS; i++ )
    {
        vec3 sample_point = ray_origin + marched_distance * ray_direction;
        float sampled_distance = get_scene_distance(sample_point );
        marched_distance += sampled_distance;
        if ( sampled_distance < MIN_DISTANCE || marched_distance > MAX_DISTANCE )
        {
            break;
        }
    }
    return marched_distance;
}

vec3 get_normal( vec3 surface_point )
{
    float scene_distance = get_scene_distance( surface_point );
    vec2 epsilon = vec2( 0.01, 0 );

    // Use epsilon to get differences in x, y, z dimensions
    // The xyy swizzling is just a briefer syntax for writing out the epsilon per dimension
    vec3 normal = scene_distance - vec3(
        get_scene_distance( surface_point - epsilon.xyy ), // x
        get_scene_distance( surface_point - epsilon.yxy ), // y
        get_scene_distance( surface_point - epsilon.yyx )  // z
    );

    return normalize( normal );
}

float get_diffuse_lighting( vec3 surface_point )
{
    vec3 light_position = u_light_position;
    vec3 light_vector = normalize( light_position - surface_point );
    vec3 surface_normal = get_normal(surface_point);
    float diffuse_lighting = dot( surface_normal, light_vector );
    // domain is now [-1, 1]
    // clamp to make [0,1]
    diffuse_lighting = clamp( diffuse_lighting, 0., 1. );

    float light_distance = length(light_position - surface_point);
    // To prevent the ray march from terminating too soon,
    // as it starts super close to the surface
    // we offset the starting point
    vec3 shadow_point = surface_point + surface_normal * SHADOW_POINT_OFFSET;
    float scene_distance_towards_light = ray_march( shadow_point, light_vector );
    if (scene_distance_towards_light < light_distance)
    {
        // line between surface point and light is obstructed
        // we still add some lighting though, call it ambient lighting.
        diffuse_lighting *= 0.1;
    }

    return diffuse_lighting;
}

void main()
{
    vec2 uv = (gl_FragCoord.xy - 0.5 * u_resolution) / u_resolution.y;

    vec3 camera_position    = vec3(0, 1, 0);
    vec3 ray_origin         = camera_position;
    vec3 ray_direction      = normalize(vec3( uv.x, uv.y, 1 ));

    float scene_distance    = ray_march( ray_origin, ray_direction );
    vec3 surface_point      = ray_origin + ray_direction * scene_distance;

    float diffuse_lighting = get_diffuse_lighting( surface_point );

    vec3 color = vec3( diffuse_lighting );

    final_colors = vec4( color, 1 );
}

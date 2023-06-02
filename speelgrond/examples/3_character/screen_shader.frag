#version 330 core

// https://www.shadertoy.com/view/4tByz3

const float INFINITY = 1. / 0.;
const vec3 DEBUG_COLOR = vec3( 1., 0., 1. );

// ----------------------------------------------------------------
// Materials

const int MATERIAL_NONE = 0;
const int MATERIAL_TERRAIN = 1;
const int MATERIAL_CHARACTER = 2;

struct Material
{
    vec3 color;

};

Material get_material_by_id( int material_id )
{
    if ( material_id == MATERIAL_TERRAIN )
    {
        return Material( vec3( 3./255., 116./255., 156./255. ) );
    }
    else if( material_id == MATERIAL_CHARACTER )
    {
        return Material( vec3( 245./255., 110/255., 2./255. ) );
    }
    else
    {
        return Material( DEBUG_COLOR );
    }
}

// ----------------------------------------------------------------
// Primitives

struct RayCastResult
{
    float d;
    int material_id;
};

// ----------------------------------------------------------------
// Out

out vec4 final_colors;

// ----------------------------------------------------------------
// Uniforms and respective Classes

struct Character
{
    vec3 head_center_p;
    float head_radius;

    vec3 body_center_p;
    float body_radius;

    float limb_radius;

    vec3 arm_left_p1;
    vec3 arm_left_p2;

    vec3 arm_right_p1;
    vec3 arm_right_p2;

    vec3 leg_left_p1;
    vec3 leg_left_p2;

    vec3 leg_right_p1;
    vec3 leg_right_p2;
};

uniform Character u_character;

uniform vec2 u_resolution;
uniform float u_time_total_elapsed_s;
uniform vec3 u_light_position;

// ----------------------------------------------------------------
// Constants

int MAX_STEPS = 1000;
float MIN_DISTANCE = 0.001;
float MAX_DISTANCE = 10000;
float SHADOW_POINT_OFFSET = 0.002;

// ----------------------------------------------------------------
// SDF functions

float sdf_sphere( vec3 sample_point, vec3 sphere_position, float sphere_radius )
{
    return length(sample_point - sphere_position) - sphere_radius;
}

float sdf_ground_plane( vec3 sample_point )
{
    return sample_point.y;
}

float sdf_line_3d( vec3 sample_point, vec3 line_point_1, vec3 line_point_2, float radius )
{
    vec3 p1_to_s = sample_point - line_point_1;
    vec3 p1_to_p2 = line_point_2 - line_point_1;
    float h = clamp( dot( p1_to_s, p1_to_p2 ) / dot( p1_to_p2, p1_to_p2 ), 0., 1. );
    return length( p1_to_s - p1_to_p2 * h ) - radius;
}

// ----------------------------------------------------------------
// Scene Elements

RayCastResult raycast_terrain( vec3 sample_point )
{
    float d = sdf_ground_plane( sample_point );
    return RayCastResult( d, MATERIAL_TERRAIN );
}

RayCastResult raycast_character( vec3 sample_point )
{
    float d = sdf_sphere( sample_point, u_character.head_center_p, u_character.head_radius );
    d = min( d, sdf_sphere( sample_point, u_character.head_center_p, u_character.head_radius ) );
    d = min( d, sdf_sphere( sample_point, u_character.body_center_p, u_character.body_radius ) );
    d = min( d, sdf_line_3d( sample_point, u_character.arm_left_p1, u_character.arm_left_p2, u_character.limb_radius) );
    d = min( d, sdf_line_3d( sample_point, u_character.arm_right_p1, u_character.arm_right_p2, u_character.limb_radius) );
    d = min( d, sdf_line_3d( sample_point, u_character.leg_left_p1, u_character.leg_left_p2, u_character.limb_radius) );
    d = min( d, sdf_line_3d( sample_point, u_character.leg_right_p1, u_character.leg_right_p2, u_character.limb_radius) );
    return RayCastResult( d, MATERIAL_CHARACTER );
}

// ----------------------------------------------------------------
// Scene definition

RayCastResult raycast_scene(vec3 sample_point )
{
    RayCastResult result = RayCastResult( INFINITY, MATERIAL_NONE );

    // Terrain
    {
        RayCastResult tmp = raycast_terrain( sample_point );
        if ( tmp.d < result.d )
        {
            result = tmp;
        }
    }

    // Character
    {
        RayCastResult tmp = raycast_character( sample_point );
        if ( tmp.d < result.d )
        {
            result = tmp;
        }
    }

    return result;
}

// ----------------------------------------------------------------
// Common ray marching boilerplate

RayCastResult ray_march( vec3 ray_origin, vec3 ray_direction )
{
    RayCastResult result = RayCastResult( 0, MATERIAL_NONE );
    for( int i = 0; i < MAX_STEPS; i++ )
    {
        vec3 sample_point = ray_origin + result.d * ray_direction;
        RayCastResult scene_cast_result = raycast_scene(sample_point );
        if ( scene_cast_result.d < MIN_DISTANCE )
        {
            break;
        }
        // update the result by summing the distance, and setting the material id
        result.d += scene_cast_result.d;
        result.material_id = scene_cast_result.material_id;
        if ( result.d > MAX_DISTANCE )
        {
            break;
        }
    }
    return result;
}

vec3 get_normal( vec3 surface_point )
{
    float scene_distance = raycast_scene( surface_point ).d;
    vec2 epsilon = vec2( 0.01, 0 );

    // Use epsilon to get differences in x, y, z dimensions
    // The xyy swizzling is just a briefer syntax for writing out the epsilon per dimension
    vec3 normal = scene_distance - vec3(
        raycast_scene( surface_point - epsilon.xyy ).d, // x
        raycast_scene( surface_point - epsilon.yxy ).d, // y
        raycast_scene( surface_point - epsilon.yyx ).d  // z
    );

    return normalize( normal );
}

// ----------------------------------------------------------------
// Lighting


vec3 get_sun_lighting( vec3 surface_point, vec3 surface_normal )
{
    float sun_lighting_power = 1.8;
    vec3 sun_color = vec3( 212./255., 66./255., 6./255. );
    vec3 sun_position = u_light_position;
    vec3 sun_vector = normalize( sun_position - surface_point );
    float diffuse_coefficient = dot( surface_normal, sun_vector );
    // domain is now [-1, 1]
    // clamp to make [0,1]
    diffuse_coefficient = clamp( diffuse_coefficient, 0., 1. );
    float sun_distance = length(sun_position - surface_point);
    // To prevent the ray march from terminating too soon,
    // as it starts super close to the surface
    // we offset the starting point
    vec3 shadow_point = surface_point + surface_normal * SHADOW_POINT_OFFSET;
    RayCastResult march_result_surface_to_sun = ray_march( shadow_point, sun_vector );
    bool is_light_path_obstructed = march_result_surface_to_sun.d < sun_distance;
    if ( is_light_path_obstructed )
    {
        // line between surface point and light is obstructed
        // we still add some lighting though, call it ambient lighting.
        diffuse_coefficient *= 0.1;
    }

    vec3 sun_lighting = sun_lighting_power * sun_color * diffuse_coefficient;
    return sun_lighting;
}

vec3 get_sky_lighting( vec3 surface_normal )
{
    float sky_lighting_power = 0.8;
    vec3 sky_color = vec3( 128./255., 128./255., 128./255. );
    float diffuse_coefficient = 0.5 + 0.5 * surface_normal.y;
    vec3 sky_lighting = sky_lighting_power * sky_color * diffuse_coefficient;
    return sky_lighting;
}

vec3 get_bounce_lighting( vec3 surface_normal )
{
    float bounce_lighting_power = 0.4;
    vec3 bounce_light_color = vec3( 92./255., 212./255., 239./255. );
    float diffuse_coefficient = clamp( 0.5 - 0.5 * surface_normal.y, 0.0, 1.0 );
    vec3 bounce_lighting = bounce_lighting_power * bounce_light_color * diffuse_coefficient;
    return bounce_lighting;
}

vec3 get_color( vec3 surface_point, vec3 surface_normal, int material_id )
{
    Material material = get_material_by_id( material_id );

    vec3 sun_lighting = get_sun_lighting( surface_point, surface_normal );
    vec3 sky_lighting = get_sky_lighting( surface_normal );
    vec3 bounce_lighting = get_bounce_lighting( surface_normal );

    vec3 lighting = sun_lighting + sky_lighting + bounce_lighting;
    vec3 color = material.color * lighting;
    return color;
}

void main()
{
    vec2 uv = (gl_FragCoord.xy - 0.5 * u_resolution) / u_resolution.y;

    vec3 camera_position    = vec3(0, 1, 0);
    vec3 ray_origin         = camera_position;
    vec3 ray_direction      = normalize(vec3( uv.x, uv.y, 1 ));

    RayCastResult march_result_camera_to_scene = ray_march( ray_origin, ray_direction );
    vec3 surface_point = ray_origin + ray_direction * march_result_camera_to_scene.d;
    vec3 surface_normal = get_normal( surface_point );
    vec3 color = get_color( surface_point, surface_normal, march_result_camera_to_scene.material_id );

    final_colors = vec4( color, 1 );
}

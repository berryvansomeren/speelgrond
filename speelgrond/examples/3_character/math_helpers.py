import math
import pyglet.math as pm
from typing import Any


def lengthdir_x( l, d ) -> float:
    return l * math.cos( d * math.pi / -180 )

def lengthdir_y( l, d ) -> float:
    return l * math.sin( d * math.pi / -180 )


def lerp( v1, v2, t ) -> Any:
    t_ = pm.clamp( t, 0, 1 )
    result = v1 * ( 1 - t_ ) + v2 * t_
    return result


def angle_lerp_radians( v1, v2, t ) -> Any:
    v1 = normalize_angle( v1 )
    v2 = normalize_angle( v2 )
    if abs( v1 - v2 ) >= math.pi:
        if v1 > v2:
            v1 -= 2.0 * math.pi
        else :
            v2 -= 2.0 * math.pi
    return lerp( v1, v2, t )


def normalize_angle( a : Any ) -> Any:
    # return value will be in range [ 0, 2PI ]
    return a % ( 2 * math.pi )


def vec3_zero() -> pm.Vec3:
    return pm.Vec3( 0., 0., 0. )

def vec3_xz( x, z ) -> pm.Vec3:
    return pm.Vec3( x, 0, z )


def vec2_to_radians( v : pm.Vec2 ) -> float:
    return math.atan2( v.y, v.x )

def radians_to_vec2( a : float ) -> pm.Vec2:
    return pm.Vec2( math.cos( a ), math.sin( a ) )
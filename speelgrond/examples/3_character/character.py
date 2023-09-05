import math
import pyglet.math as pm
from pyglet.window import key
import math_helpers as mh


WALKING_VELOCITY = 2
STEP_TIME = 0.2

FEET_WIDTH = 0.2 # 0.8
BODY_BOB_FACTOR = 0.25 # 0.5
HAND_BOB_FACTOR = 0.25 # 1.25


class Foot:
    def __init__( self, position : pm.Vec3 ):
        self.position = position
        self.previous_position = position
        self.target_position = position
        self.t = 0.


class Character:

    def __init__( self, game_window ):
        self.body_base_height = 1
        self.position = pm.Vec3( 0, 0, 6 )
        self.game_window = game_window
        self.moving = False
        self.step_timer = 0
        self.step_foot_index = 0

        self.heading_radians = 0
        self._update_direction( pm.Vec3( 0, 0, -1 ) )

        self.feet = []
        for foot_index in range( 2 ):
            side = foot_index * 2 - 1
            foot_position = pm.Vec3(
                self.position.x + self.direction_right.x * FEET_WIDTH * side + self.direction_forward.x * 0.1,
                0,
                self.position.z + self.direction_right.z * FEET_WIDTH * side + self.direction_forward.z * 0.1
            )
            self.feet.append( Foot( foot_position ) )

        self.arms_positions = [ mh.vec3_zero(), mh.vec3_zero() ]

        self.body_height_offset = 0

    def update( self, dt : float ) -> None:
        self.moving = False
        self._handle_input( dt )
        self._handle_steps( dt )
        self._handle_body_bob()
        self._handle_arms()
        self._set_feet_positions( dt )

    def _handle_input( self, dt : float ) -> None:
        direction = pm.Vec3( 0., 0., 0. )
        direction_per_key = [
            ( key.UP,       pm.Vec3(  0., 0.,  1. ) ),
            ( key.DOWN,     pm.Vec3(  0., 0., -1. ) ),
            ( key.LEFT,     pm.Vec3( -1., 0.,  0. ) ),
            ( key.RIGHT,    pm.Vec3(  1., 0.,  0. ) ),
        ]
        for keyboard_key, keyboard_direction in direction_per_key :
            if self.game_window.keyboard.is_down( keyboard_key ) :
                direction += keyboard_direction

        if direction != pm.Vec3( 0, 0, 0 ):
            self._update_direction( direction )
            self.position += self.direction_forward * WALKING_VELOCITY * dt
            self.moving = True

    def _update_direction( self, new_direction : pm.Vec3 ) -> None:
        # note that the side_vector_2d is basically a top-down view vector,
        # but the y-dimension in that view matches the z-dimension in our 3D space.

        self.direction_forward = new_direction.normalize()
        self.target_heading_radians = mh.vec2_to_radians( pm.Vec2( self.direction_forward.x, self.direction_forward.z ) )

        self.heading_radians = mh.angle_lerp_radians( self.heading_radians, self.target_heading_radians, 0.2 )

        side_angle_radians = self.heading_radians + (math.pi / 2)
        side_vector_2d = mh.radians_to_vec2( side_angle_radians )
        self.direction_right = mh.vec3_xz( side_vector_2d.x, side_vector_2d.y )

    def _handle_steps( self, dt ) -> None:
        if self.moving:
            self.step_timer += dt

        if self.step_timer > STEP_TIME:
            self._step_foot( self.step_foot_index )
            self.step_foot_index = 1 - self.step_foot_index
            self.step_timer -= STEP_TIME

    def _step_foot( self, step_foot_index ) -> None:
        foot = self.feet[ step_foot_index ]
        foot.previous_position = foot.position
        side = step_foot_index * 2 - 1
        foot.target_position = pm.Vec3(
            self.position.x + self.direction_right.x * FEET_WIDTH * side + self.direction_forward.x * 0.1,
            0,
            self.position.z + self.direction_right.z * FEET_WIDTH * side + self.direction_forward.z * 0.1
        )
        foot.t = 0

    def _handle_body_bob( self ) -> None:
        max_foot_height = max( foot.position.y for foot in self.feet )
        self.position.y = self.body_base_height + max_foot_height * BODY_BOB_FACTOR

    def _handle_arms( self ) -> None:
        for arm_index in range( len( self.arms_positions ) ):
            side = arm_index * 2 - 1
            self.arms_positions[ arm_index ] = (
                    self.position +
                    self.direction_right * 1. * side +
                    pm.Vec3( 0, -0.1, 0 )
            )
            max_foot_height = max( foot.position.y for foot in self.feet )
            self.arms_positions[ arm_index ].y += max_foot_height * HAND_BOB_FACTOR

    def _set_feet_positions( self, dt : float ) -> None:
        for foot in self.feet:
            foot.position.x = mh.lerp( foot.previous_position.x, foot.target_position.x, foot.t )
            foot.position.z = mh.lerp( foot.previous_position.z, foot.target_position.z, foot.t )
            foot.position.y = -mh.lengthdir_y( 0.5, foot.t * 180 )

            if foot.t < 1:
                foot.t += 0.1
from dataclasses import dataclass
import pyglet.math as pm

from character import Character


@dataclass
class CharacterUniformValues:
    head_center_p : pm.Vec3
    head_radius : float

    body_center_p : pm.Vec3
    body_radius : float

    limb_radius : float

    arm_left_p1 : pm.Vec3
    arm_left_p2 : pm.Vec3

    arm_right_p1 : pm.Vec3
    arm_right_p2 : pm.Vec3

    leg_left_p1 : pm.Vec3
    leg_left_p2 : pm.Vec3

    leg_right_p1 : pm.Vec3
    leg_right_p2 : pm.Vec3


def get_character_uniform_values( character : Character ) -> CharacterUniformValues:
    body_radius = 0.5

    body_center_p = character.position

    head_radius = 0.3
    head_above_body = -0.1
    head_center_p = body_center_p + pm.Vec3( 0., body_radius + head_radius + head_above_body, 0. )

    limb_radius = 0.1

    arm_left_p1 = body_center_p
    arm_left_p2 = character.arms_positions[0]

    arm_right_p1 = body_center_p
    arm_right_p2 = character.arms_positions[1]

    leg_left_p1 = body_center_p
    leg_left_p2 = character.feet[0].position

    leg_right_p1 = body_center_p
    leg_right_p2 = character.feet[1].position

    character = CharacterUniformValues(
        head_center_p = head_center_p,
        head_radius = head_radius,

        body_center_p = body_center_p,
        body_radius = body_radius,
        limb_radius = limb_radius,

        arm_left_p1 = arm_left_p1,
        arm_left_p2 = arm_left_p2,
        arm_right_p1 = arm_right_p1,
        arm_right_p2 = arm_right_p2,

        leg_left_p1 = leg_left_p1,
        leg_left_p2 = leg_left_p2,
        leg_right_p1 = leg_right_p1,
        leg_right_p2 = leg_right_p2,
    )

    return character
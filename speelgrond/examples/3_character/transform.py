from __future__ import annotations

import pyglet.math as pm


class Transform:
    def __init__( self ):
        self.mat4 = pm.Mat4()

    # ----------------------------------------------------------------
    # Targeting

    def look_at_position( self, target_position : pm.Vec3 ) -> None:
        position = self.get_translation()
        up = self.get_world_up()
        self.mat4 = pm.Mat4.look_at( position, target_position, up )

    def look_in_direction( self, target_direction : pm.Vec3 ) -> None:
        position = self.get_translation()
        target_position = position + target_direction
        up = self.get_world_up()
        self.mat4 = pm.Mat4.look_at( position, target_position, up )

    # ----------------------------------------------------------------
    # Translation

    def get_translation( self ) -> pm.Vec3:
        return pm.Vec3( *self.mat4.column( 3 ) )

    def set_translation( self, translation : pm.Vec3 ) -> None:
        self.mat4 = pm.Mat4((
            *self.mat4.column( 0 ),
            *self.mat4.column( 1 ),
            *self.mat4.column( 2 ),
            *translation
        ))

    def translate( self, translation : pm.Vec3 ) -> None:
        self.mat4.translate( translation )

    # ----------------------------------------------------------------
    # Scale

    def get_scale( self ) -> pm.Vec3:
        return pm.Vec3(
            pm.Vec3( *self.mat4.column( 0 ) ).mag,
            pm.Vec3( *self.mat4.column( 1 ) ).mag,
            pm.Vec3( *self.mat4.column( 2 ) ).mag,
        )

    def set_scale( self, scale : float | pm.Vec3 ) -> None:
        if isinstance( scale, float ):
            self.mat4[ 0 ][ 0 ] = scale
            self.mat4[ 1 ][ 1 ] = scale
            self.mat4[ 2 ][ 2 ] = scale
        else:
            self.mat4[ 0 ][ 0 ] = scale.x
            self.mat4[ 1 ][ 1 ] = scale.y
            self.mat4[ 2 ][ 2 ] = scale.z

    def scale( self, scale : float | pm.Vec3 ) -> None:
        if isinstance( scale, float ):
            self.mat4.scale( pm.Vec3( scale, scale, scale ) )
        else:
            self.mat4.scale( scale )

    # ----------------------------------------------------------------
    # Rotation

    def rotate( self, axis : pm.Vec3, degrees : float ) -> None:
        self.mat4.rotate( vector = axis, angle = degrees)

    def rotate_pitch_relative( self, degrees : float ) -> None:
        self.rotate( self.get_relative_right(), degrees )

    def rotate_yaw_relative( self, degrees: float ) -> None :
        self.rotate( self.get_relative_up(), degrees )

    def rotate_roll_relative( self, degrees: float ) -> None :
        self.rotate( self.get_relative_forward(), degrees )

    def rotate_pitch_world( self, degrees : float ) -> None:
        self.rotate( self.get_world_right(), degrees )

    def rotate_yaw_world( self, degrees: float ) -> None :
        self.rotate( self.get_world_up(), degrees )

    def rotate_roll_world( self, degrees: float ) -> None :
        self.rotate( self.get_world_forward(), degrees )

    # ----------------------------------------------------------------
    # Getters

    def get_matrix( self ) -> pm.Mat4:
        return self.mat4

    # Model space getters

    def get_relative_right( self ) -> pm.Vec3:
        return pm.Vec3( 1, 0, 0 )

    def get_relative_forward( self ) -> pm.Vec3:
        return pm.Vec3( 0, 1, 0 )

    def get_relative_up( self ) -> pm.Vec3:
        return pm.Vec3( 0, 0, 1 )

    def get_relative_left( self ) -> pm.Vec3:
        return -self.get_relative_right()

    def get_relative_backward( self ) -> pm.Vec3:
        return -self.get_relative_forward()

    def get_relative_down( self ) -> pm.Vec3:
        return -self.get_relative_up()

    # World space getters

    def get_world_right( self ) -> pm.Vec3:
        return pm.Vec3( *self.mat4.row( 0 ) ).normalize()

    def get_world_forward( self ) -> pm.Vec3:
        return pm.Vec3( *self.mat4.row( 1 ) ).normalize()

    def get_world_up( self ) -> pm.Vec3:
        return pm.Vec3( *self.mat4.row( 2 ) ).normalize()

    def get_world_left( self ) -> pm.Vec3:
        return -self.get_world_right()

    def get_world_backward( self ) -> pm.Vec3:
        return -self.get_world_forward()

    def get_world_down( self ) -> pm.Vec3:
        return -self.get_world_up()




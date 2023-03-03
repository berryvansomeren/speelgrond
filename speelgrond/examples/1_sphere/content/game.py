import math
import numpy as np
import pyglet.window.key as key
import speelgrond as sg


class Game:

    def __init__( self, game_window: sg.GameWindow ):
        self.game_window = game_window
        self.sphere_position = ( 0., 1., 6. )
        self.total_time = 0.

    def update( self, dt ) :
        self._update_sphere_position( dt )
        self._update_light_position( dt )

    def _update_sphere_position( self, dt ):
        velocity = dt * 5
        modifiers = [
            ( key.LEFT, ( -velocity, 0, 0 ) ),
            ( key.RIGHT, ( velocity, 0, 0 ) ),
            ( key.UP, ( 0, velocity, 0 ) ),
            ( key.DOWN, ( 0, -velocity, 0 ) ),
        ]
        for keyboard_key, position_delta in modifiers:
            if self.game_window.keyboard.is_down(keyboard_key):
                self.sphere_position = np.add( self.sphere_position, position_delta )

        self.game_window.set_uniform( 'u_sphere_position', self.sphere_position )

    def _update_light_position( self, dt ):
        self.total_time += dt
        light_position = ( 0, 5, 6 )
        light_position_delta = np.array(( math.sin( self.total_time ), 0, math.cos( self.total_time ) )) * 3
        light_position = np.add( light_position, light_position_delta )
        self.game_window.set_uniform( 'u_light_position', light_position )

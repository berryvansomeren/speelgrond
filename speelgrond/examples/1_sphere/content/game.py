import math
import numpy as np
import pyglet.window.key as key
import speelgrond as sg


def modify_tuple( t, i, v ):
    l = list(t)
    l[i] += v
    return tuple(l)


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
            ( key.LEFT, 0, -velocity ),
            ( key.RIGHT, 0, velocity ),
            ( key.UP, 1, velocity ),
            ( key.DOWN, 1, -velocity ),
        ]
        for keyboard_key, dimension, value in modifiers:
            if self.game_window.keyboard.is_down(keyboard_key):
                self.sphere_position = modify_tuple( self.sphere_position, dimension, value )

        self.game_window.set_uniform( 'u_sphere_position', self.sphere_position )

    def _update_light_position( self, dt ):
        self.total_time += dt
        light_position = ( 0, 5, 6 )
        light_position_delta = np.array(( math.sin( self.total_time ), 0, math.cos( self.total_time ) )) * 3
        light_position = np.add( light_position, light_position_delta )
        self.game_window.set_uniform( 'u_light_position', light_position )

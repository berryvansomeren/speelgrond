import speelgrond as sg
import pyglet.window.key as key


def modify_tuple( t, i, v ):
    l = list(t)
    l[i] += v
    return tuple(l)


class Game:

    def __init__( self, game_window: sg.GameWindow ):
        self.game_window = game_window
        self.sphere_position = ( 0., 1., 6. )

    def update( self, dt ) :
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

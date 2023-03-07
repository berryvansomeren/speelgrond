import pyglet.window.key as key
import speelgrond as sg


class Game:

    def __init__( self, game_window: sg.GameWindow ):
        self.game_window = game_window
        self.camera_time_along_path = 0

    def update( self, dt ) -> None:
        velocity = dt * 100
        if self.game_window.keyboard.is_down( key.UP ):
            self.camera_time_along_path += velocity
        if self.game_window.keyboard.is_down( key.DOWN ):
            self.camera_time_along_path -= velocity
        self.game_window.set_uniform( 'u_camera_time_along_path', self.camera_time_along_path )
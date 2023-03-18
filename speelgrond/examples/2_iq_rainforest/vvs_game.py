import logging
import pyglet.window.key as key
import speelgrond as sg
from ververser import ReloadStatus
from speelgrond import host_this_folder


if __name__ == '__main__':
    logging.basicConfig( level = logging.INFO )
    host_this_folder()


class VVSGame:

    def __init__( self, game_window: sg.GameWindow ):
        self.game_window = game_window
        self.camera_time_along_path = 0

    def vvs_update( self, dt ) -> None:
        if self.game_window.screen_shader.reload_status == ReloadStatus.RELOADED:
            self.camera_time_along_path = 0

        velocity = dt * 100
        modifiers = [
            ( key.UP, velocity ),
            ( key.DOWN, -velocity ),
        ]
        for keyboard_key, key_velocity in modifiers:
            if self.game_window.keyboard.is_down( keyboard_key ) :
                self.camera_time_along_path += key_velocity
        self.game_window.set_uniform( 'u_camera_time_along_path', self.camera_time_along_path )
from pathlib import Path
from time import time
from typing import Any

import ververser
from ververser import LoadStatus

from speelgrond.keyboard import _Keyboard
from speelgrond.screen_shader.screen_shader import load_screen_shader


EXPECTED_SHADER_NAME = 'screen_shader.frag'


class GameWindow( ververser.GameWindow ):

    def __init__( self, content_folder : Path ):
        super().__init__( content_folder )

        self.keyboard = _Keyboard()
        self.push_handlers( self.keyboard.get_handler() )

        def _load_screen_shader( path : Path ) -> Any:
            return load_screen_shader( path, self.width, self.height )

        self.content_manager.register_asset_loader( '.frag', _load_screen_shader )
        self.time_start = time()

    # --------
    # Convenience Functions

    def set_uniform( self, name: str, v, raise_if_unavailable = False ) :
        # uniforms are only set if available
        # uniforms that are declared but not used are optimized out
        # so they are not available then.
        # Check the log to see what uniforms and attributes are available
        shader = self.screen_shader.shader
        if name in shader.uniforms :
            shader[ name ] = v
        else:
            if raise_if_unavailable:
                raise ValueError( f'Uniform with name "{name}" not available.' )

    # --------
    # Main Game Functions

    def init( self ) -> None:
        self.screen_shader = self.content_manager.load( EXPECTED_SHADER_NAME )
        assert self.screen_shader

        # super init comes last,
        # as code invoked by the main script's init() might already expect the screen shader to be available
        super().init()

    def update( self, dt ) -> None:
        if self.screen_shader.reload_status == LoadStatus.RELOADED:
            self.time_start = time()

        self.set_uniform( 'u_resolution', (self.width, self.height) )
        self.set_uniform( 'u_time_total_elapsed_s', time() - self.time_start )
        self.set_uniform( 'u_time_delta_s', dt )
        self.set_uniform( 'u_frames_total', self.fps_counter.total_frames )
        self.set_uniform( 'u_frames_per_second', self.fps_counter.fps )

        super().update( dt )

    def draw( self ) -> None:
        self.screen_shader.draw()
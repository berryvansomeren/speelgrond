from dataclasses import fields
import logging
import math
import numpy as np
import speelgrond as sg
from speelgrond import host_this_folder

from ververser import import_script
from character_uniform_values import get_character_uniform_values


if __name__ == '__main__':
    logging.basicConfig( level = logging.INFO )
    host_this_folder()


module_character = import_script( 'character.py' )


class VVSGame:

    def __init__( self, game_window: sg.GameWindow ):
        self.game_window = game_window
        self.sphere_position = ( 0., 1., 6. )
        self.total_time = 0.

        self.character = module_character.Character( game_window )

    def vvs_update( self, dt : float ) -> None:
        self._update_light_position( dt )
        self._update_character( dt )

    def _update_light_position( self, dt ) -> None:
        self.total_time += dt
        light_position = ( 2, 5, 3 )
        light_position_delta = np.array(( math.sin( self.total_time ), 0, math.cos( self.total_time ) )) * 3
        light_position = np.add( light_position, light_position_delta )
        self.game_window.set_uniform( 'u_light_position', light_position )

    def _update_character( self, dt : float ):
        self.character.update( dt )
        character_model = get_character_uniform_values( self.character )
        for field in fields( character_model ) :
            self.game_window.set_uniform(
                f'u_character.{field.name}',
                getattr( character_model, field.name ),
                raise_if_unavailable = True
            )

from copy import deepcopy
import pyglet.window.key as key
from pyglet.window.key import KeyStateHandler


class _Keyboard:

    def __init__( self ):
        self._previous_key_states = KeyStateHandler()
        self._current_key_states = KeyStateHandler()

    def get_handler( self ):
        return self._current_key_states

    def update( self ):
        self._previous_key_states = deepcopy( self._current_key_states )

    def is_down( self, key ):
        return self._current_key_states[ key ]

    def is_up( self, key ):
        return not self._current_key_states[ key ]

    def is_pressed( self, key ):
        current_is_down = self._current_key_states[ key ]
        previous_is_down = self._previous_key_states[ key ]
        return current_is_down and not previous_is_down

    def is_released( self, key ):
        current_is_down = self._current_key_states[ key ]
        previous_is_down = self._previous_key_states[ key ]
        return not current_is_down and previous_is_down

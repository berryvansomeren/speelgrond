from typing import Optional
import speelgrond as sg
from ververser import import_script

game = import_script( 'game.py' )
Game = game.Game

# --------
# This is just some boilerplate that makes it easier to use a custom Game class

_GAME : Optional[ Game ] = None

def vvs_init( game_window : sg.GameWindow ):
    global _GAME
    _GAME = Game( game_window )

def vvs_update( dt ):
    _GAME.update( dt )


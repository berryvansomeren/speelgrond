from speelgrond.game_window import GameWindow
from ververser.global_game_window import set_global_game_window


def make_global_game_window( *args, **kwargs ) -> GameWindow:
    game_window = GameWindow( *args, **kwargs )
    set_global_game_window( game_window )
    return game_window
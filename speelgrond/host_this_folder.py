from pathlib import Path
from speelgrond.game_window import GameWindow
import ververser


def make_game_window( content_folder_path : Path ) -> GameWindow:
    return GameWindow( content_folder_path = content_folder_path )


# This function should be used instead of ververser.host_this_folder when using speelgrond
# What this does is that it will instantiate a speelgrond.GameWindow, instead of a ververser.GameWindow
def host_this_folder( f_make_window = make_game_window ) -> None:
    ververser.host_this_folder( f_make_window = f_make_window, n_frames_back = 2 )

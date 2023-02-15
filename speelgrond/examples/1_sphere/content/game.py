import speelgrond as sg


class Game:

    def __init__( self, game_window: sg.GameWindow ) :
        self.game_window = game_window

    def update( self, dt ) :
        ...

import pyglet
import arcade
from game_view import GameView

pyglet.options.dpi_scaling = "real"

#
#
def main():
    """ Creates a Window for the game """

    # The Window for this game
    window = arcade.Window(*arcade.get_display_size(), fullscreen=False)
    
    # A View inside of the Window
    game_view = GameView()
    
    
    # Show the View
    window.show_view(game_view)


    # Run the game
    arcade.run()
    
    
#
#
if __name__ == "__main__":
    main()
import arcade
from game_view import GameView

#
#
def main():
    """ Creates a Window for the game """

    # The Window for this game
    window = arcade.Window(*arcade.get_display_size(), fullscreen=True)
    
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
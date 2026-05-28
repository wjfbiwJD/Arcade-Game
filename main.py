import logging
import pyglet
import arcade
from game_view import GameView

pyglet.options.dpi_scaling = "real"

#
#
def main():
    """ Creates a Window for the game """
    arcade.configure_logging(level=logging.INFO)
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s", filename="game.log", filemode="w")
    logger = logging.getLogger("arcade")
    logger.info("Initializing window")

    # The Window for this game
    window = arcade.Window(*arcade.get_display_size(), fullscreen=False)
    logger.info("Initializing game view")
    # A View inside of the Window
    game_view = GameView()
    
    
    # Show the View
    window.show_view(game_view)

    logger.info("Starting game loop")
    # Run the game
    arcade.run()
    
    
#
#
if __name__ == "__main__":
    main()
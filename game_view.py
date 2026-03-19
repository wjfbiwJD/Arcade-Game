import arcade

class GameView(arcade.View):
    """ Represents a view inside of a Window """

    def __init__(self):
        """ Handles what to do when this view is created """
        super().__init__()

        
        
        
    # 
    #
    def on_show_view(self):
        """ Handles what to do when the window switches to this view """
        self.background_color = arcade.color.AMAZON
        
    #
    #
    def on_hide_view(self):
        """ Handles what to do when the window switches away from this view """
        
        
    #
    #
    def on_draw(self):
        """ Handles drawing object each frame """

        self.clear()

        
    #
    #
    def on_update(self, delta_time):
        """ Handles updating objects each frame """
        
        
    #
    #
    def on_key_press(self, symbol: int, modifiers: int):
        """ Handles what to do when a key is initially pressed """
        
        
    #
    #
    def on_key_release(self, symbol: int, modifiers: int):
        """ Handles what to do when a key is released. See arcade.key """
        
        
    #
    #
    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        """ Handles what to do when the mouse is moved. See arcade.key """
        
        
    #
    #
    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        """ Handles what to do when a button on the mouse is pressed. """
        
        
    #
    #
    def on_mouse_released(self, x: int, y: int, button: int, modifiers: int):
        """ Handles what to do when a button on the mouse is released """
        
        
    #
    #
    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int):
        """ Handles what to do when the scroll wheel is used """
        
        
    #
    #
    def on_mouse_enter(self, x: int, y: int):
        """ Handles what to do when the mouse enters the window area """
        
        
    #
    #
    def on_mouse_leave(self, x: int, y: int):
        """ Handles what to do when the mouse leaves the window area """
        
        
        
        
        

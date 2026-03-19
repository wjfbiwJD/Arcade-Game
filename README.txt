===============================

Arcade Project Template

    A minimal starting point for building games with the Arcade library in Python on CodePad.

    Be sure to hit the full-screen button above the GUI window when testing your creation.


===============================

Project Structure
    ~/
    │
    ├── main.py        # Creates the window and starts the game
    └── game_view.py   # Contains the GameView class (a subclass of arcade.View)


===============================

Arcade's Documentation

    Whatever you're looking to do, you can probably find an example of it here:
        https://api.arcade.academy/en/stable/

    Important Links:

    1. Built-in Resources:
        https://api.arcade.academy/en/stable/api_docs/resources.html

        A collection of built-in sprites, images, videos, etc. that you can use (for free!)
        
        To use images:
            a. Create a Sprite using arcade.Sprite(). 
                The first argument inside of the parentheses to arcade.Sprite(...) should be a filename.

            b. Use a built-in image from the link above or a custom image.
            
            -> For custom images, just upload it to CodePad and use its filename in a string.
            -> For built-in images from the link above, read the 'How Do I Use These?' section at the top.
                Hover over the name of the image and click the square copy button that appears.
                Paste the text into arcade.Sprite

            Example:
                    self.player = arcade.Sprite(":resources:/logo.png")

                    # be sure to add self.player to a SpriteList then draw() the SpriteList inside of on_draw()

    2. Example Projects / Tutorials: 
        https://api.arcade.academy/en/stable/example_code/index.html

        This link contains simple games and example projects with arcade.

    3. Which keyboard keys correspond to which numbers:
        https://api.arcade.academy/en/stable/api_docs/arcade.key.html

        Keyboard keys are really just numbers sent to the computer.
            e.g.,  arcade.key.SPACE  is really an alias for the number  32

        Use arcade.key.KEYNAME inside of GameView methods like on_key_press / on_key_release


    4. How colors work with Arcade:
        https://api.arcade.academy/en/stable/api_docs/arcade.color.html

        You can use arcade.color.COLORNAME to obtain a color

    5. Quick Index / API Reference:

        https://api.arcade.academy/en/stable/api_docs/quick_index.html#

        https://api.arcade.academy/en/stable/api_docs/arcade.html

        Use these links to search up how different classes in arcade work.
        You can find out how to create an object of a class, and how to use different methods (abilities) of arcade-specific classes


===============================

How It Works

    Arcade is a 2D game framework.
    
    Games are built using four main data types:

        a. arcade.Window — the main application window. Normally, you wont need to touch this except to switch the view being shown.

        b. arcade.View — a "screen" shown inside a window (like a main menu, level, or the entire game for small games).
            TIP: Inside of the GameView class, you can reference the window using `self.window`

        c. arcade.Sprite — an object or character in the game

        d. arcade.SpriteList — a collection of related Sprite objects used for batch drawing/updating

=========

Description Of The Code Inside Of The `main.py` File

    1. Creates the Window.

    2. Creates the GameView (your main game screen).
        * This runs the code inside of the GameView's __init__ method

    3. Displays it with window.show_view(game_view).
        * This runs the code inside of the GameView's on_show_view method

    4. Calls arcade.run() to start the main event loop (see below).

=========

Description Of The GameView Class

    This is where the logic for your game should go.
    For simple games, you'll only need this class.

    For more complex games (with main menu screens, different levels, etc.), 
    you'll probably want to create another Python file with a new subclass of View.

    From there, you can construct an instance of your new view and display it using `window.show_view(your_new_view)`

=========

The Main Event Loop
    When arcade.run() is called, the Window will automatically call methods of the GameView class.
    
    The following methods from the GameView will run continously in a loop:

        a. on_update() — Handles movement and other logic
        b. on_draw() — Erases the screen and draws objects (in their new positions)
        c. Any other 'event' methods prefixed with 'on_', if the event they correspond to occurs.
            Examples:
                on_key_press, on_key_release, on_mouse_press, on_mouse_release,
                on_mouse_motion, on_mouse_scroll, on_show_view, on_hide_view,
                on_mouse_enter, on_mouse_leave, etc.

    Each iteration of this loop represents a single 'frame'.
    By default, the frame rate is 60 FPS.

=====

GameView Methods:

    Method Name                             Called When
    ---------------------------------      ------------------------------------------------

    __init__(self)                          GameView() is called in main.py

    on_show_view(self)                      window.show_view() is called in main.py

    on_hide_view(self)                      window.hide_view() is called somewhere

    on_draw(self)                           Each frame

    on_update(self, 
              delta_time):                  Each frame
                                            (delta_time -> time since the last update, in seconds)

    on_key_press(self, 
                 symbol: int, 
                 modifiers: int):           When a key on the keyboard is initially pressed
                                            (symbol ->
                                             modifiers -> extra keys held at the same time. see arcade's docs. 
                                                          This works a little differently than you might expect)

    on_key_release(self, 
                   symbol: int, 
                   modifiers: int):         When a key on the keyboard is released

    on_mouse_motion(self, 
                    x: int, 
                    y: int, 
                    dx: int, 
                    dy: int):               Each frame the mouse moves 
                                            (dx/dy -> how much the mouse's position has changed)


    on_mouse_press(self, 
                    x: int, 
                    y: int, 
                    button: int, 
                    modifiers: int):        When a mouse button is initially pressed 
                                            (button -> either arcade.MOUSE_BUTTON_LEFT, arcade.MOUSE_BUTTON_MIDDLE, or arcade.MOUSE_BUTTON_RIGHT)

    on_mouse_released(self, 
                      x: int, 
                      y: int, 
                      button: int, 
                      modifiers: int):      When a mouse button is released

    on_mouse_scroll(self, 
                    x: int, 
                    y: int, 
                    scroll_x: int, 
                    scroll_y: int):         When the mouse wheel is scrolled. Note: Does not work well with touchscreens.
                                            (scroll_x/y -> How much the mouse has scrolled; usually only the scroll_y is used)

    on_mouse_enter(self, 
                   x: int, 
                   y: int):                 When the mouse enters the window area

    on_mouse_leave(self, 
                   x: int, 
                   y: int):                 When the mouse exits the window area

    clear(self)                             Inside of on_draw().
                                            Do not delete the 'self.clear()' line and do not call clear() anywhere else in your code.

=====

Notable Properties of GameView:
    Note: Access these from any method inside of the code for the GameView class using 'self.ATTRIBUTE_NAME_HERE'
    You'll likely add your own attributes like the player Sprite, a SpriteList of enemies, a number representing the player's score, etc.
    
    background_color       RGBOrA255                          The color of the background.
                                                                See https://api.arcade.academy/en/stable/api_docs/arcade.color.html
                                                                Or use a hex string or RGB color tuple.
    center                 tuple[float, float]                The position in the center of the screen. 
                                                              Equivalent to saying (self.center_x, self.center_y) or (self.width/2, self.height/2)
    center_x               float                              The X component of the window's center
    center_y               float                              The Y component of the window's center
    width                  float                              The width of the screen, in pixels
    height                 float                              The height of the screen, in pixels
    size                   tuple[float, float]                A tuple in the format (width, height)


=========

Notable Classes of Arcade:
    Main:
        Camera2D                        Represents a 2D camera
        Sprite                          Represents a character or an object in the game
        SpriteList                      Organizes groups of sprites together
        View                            Represents a view inside of the window
        Window                          Represents the window for the game

    Rectangles:
        LBWH()                          Creates a rectangle from the left (x), bottom (y), width and height
        LRBT()                          Creates a rectangle from the left (x), right (x), bottom (y), and top (y)
        XYWH()                          Creates a rectangle from the center x, center y, width and height

    Physics Engines:
        PhysicsEngineSimple             A simple physics engine useful for top-down games
        PhysicsEnginePlatformer         A physics engine useful for platformer games
        PymunkPhysicsEngine             A physics engine used for advanced physics
        PymunkPhysicsObject             An object used with the PymunkPhysicsEngine

    Drawable Objects:
        shape_list.Shape                A primitive shape object
        shape_list.ShapeElementList     A collection of shape objects
        SpriteCircle                    A simple circular sprite
        SpriteSolidColor                A simple rectangular sprite
        Text                            Represents drawable text

    Misc:
        AStarBarrierList                A list of sprites that act as obstacles for the A* pathfinding algorithm
        Sound                           Represents a sound file
        Texture                         Represents image data used by classes like arcade.Sprite
        TileMap                         Useful for importing maps made with the Tiled map editor


=========
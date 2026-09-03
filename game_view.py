import arcade
import arcade.gui
import math
import logging

import ai_car
import car
import tracking_car
from action import Action
from constants import DAMPING, MASS, FRICTION, MAX_VELOCITY, ACCELERATION, CAR_SCALE, TURN_SENSITIVITY, BRAKE_FORCE_MULTIPLIER

logger = logging.getLogger("arcade")

import os
d = os.path.dirname(os.path.abspath(__file__))

class GameView(arcade.View):
    """ Represents a view inside of a Window """

    def __init__(self):
        """ Handles what to do when this view is created """
        super().__init__()

        self.tilemap:arcade.TileMap = None
        self.player:tracking_car.TrackingCar = None
        self.player_list:arcade.SpriteList = None
        self.spawnpoints:list = None
        self.camera:arcade.Camera2D = None
        
        
    # 
    #
    def on_show_view(self):
        """ Handles what to do when the window switches to this view """
        self.background_color = arcade.color.AMAZON
        layer_options = {

            "Walls":{
                "hit_box_algorithm":arcade.hitbox.PymunkHitBoxAlgorithm()
            }

        }
        self.tilemap = arcade.TileMap(os.path.join(d, "Assets/tilemaps/mymap.tmx"), use_spatial_hash=True, layer_options=layer_options)
        self.physics = arcade.PymunkPhysicsEngine(damping=DAMPING, gravity=(0, 0))
        car.Car.set_physics_engine(self.physics)
        self.spawnpoints = [tile.position for tile in self.tilemap.sprite_lists["Spawns"]]

        self.player = tracking_car.TrackingCar(os.path.join(d, "Assets/racing-pack/PNG/Cars/car_black_1.png"), CAR_SCALE)
        self.player.position = self.spawnpoints[0]
        self.start_point = self.player.position
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

        aicar1 = ai_car.AICar(os.path.join(d, "Assets/racing-pack/PNG/Cars/car_red_1.png"), CAR_SCALE)
        aicar1.position = self.spawnpoints[1]
        self.player_list.append(aicar1)

        self.keys = set()
        self.camera = arcade.Camera2D(position=self.player.position)
        for car_ in self.player_list:
            self.physics.add_sprite(car_, mass=MASS, friction=FRICTION, collision_type="player", max_horizontal_velocity=MAX_VELOCITY, max_vertical_velocity=MAX_VELOCITY)
        self.physics.add_sprite_list(self.tilemap.sprite_lists["Walls"], collision_type="wall", body_type=arcade.PymunkPhysicsEngine.STATIC)

        self.ui_manager = arcade.gui.UIManager()
        self.ui_manager.enable()
        self.ui_layout = arcade.gui.UIBoxLayout(space_between=20)

        resume_button = arcade.gui.UIFlatButton(text="Resume", width=max(200, self.window.width // 8))
        self.ui_layout.add(resume_button)
        @resume_button.event("on_click")
        def on_click_resume(event):
            self.toggle_gui()

        self.ui_manager
        logger.info("Switched to GameView")
    #
    #
    def on_hide_view(self):
        """ Handles what to do when the window switches away from this view """
        
        
    #
    #
    def on_draw(self):
        """ Handles drawing object each frame """

        self.clear()

        self.camera.use()

        for layer in self.tilemap.sprite_lists:
            if layer in ["Spawns", "WallsA"]:
                continue

            self.tilemap.sprite_lists[layer].draw()

          

            

        self.player_list.draw()

        self.ui_manager.draw()

        
    #
    #
    def on_update(self, delta_time):
        """ Handles updating objects each frame """
        if arcade.key.W in self.keys:
            if arcade.key.LSHIFT in self.keys:
                self.player.move_forward(ACCELERATION, boost=True) 
            else:   
                self.player.move_forward(ACCELERATION)

        if arcade.key.SPACE in self.keys:
            self.player.ebrake(BRAKE_FORCE_MULTIPLIER)

        if arcade.key.S in self.keys:
            self.player.move_backward(ACCELERATION)        

        if arcade.key.A in self.keys:
            self.player.turn_left(TURN_SENSITIVITY)
            
        elif arcade.key.D in self.keys:
            self.player.turn_right(TURN_SENSITIVITY)


        self.player.end_frame()
        for car in self.player_list:
            if car.replay_movements:
                car.update(delta_time)
            
        self.physics.step(delta_time)


        self.camera.position = self.player.position
        angle = math.degrees(-self.player.body.angle) % 360

        if self.camera.angle < 180 and angle > 270:
            angle -= 360
        elif self.camera.angle > 270 and angle < 90:
            angle += 360
            
        self.camera.angle = arcade.math.lerp(self.camera.angle, angle, 0.1)
        
    #
    #
    def on_key_press(self, key: int, modifiers: int):
        """ Handles what to do when a key is initially pressed """
        self.keys.add(key)

        if arcade.key.F == key:
            filename = os.path.join(d, "Data", "paths", "path1.json")
            self.player.save_movements(filename)

        elif arcade.key.L == key:
            filename = os.path.join(d, "Data", "paths", "path1.json")
            self.player.load_movements(filename)
            self.physics.set_position(self.player, self.start_point)
            self.physics.set_rotation(self.player, 0)
            self.physics.set_velocity(self.player, (0, 0))
            self.physics.set_horizontal_velocity(self.player, 0)

        elif arcade.key.ESCAPE == key:
            self.toggle_gui()

    #
    #
    #
    def on_key_release(self, key: int, modifiers: int):
        """ Handles what to do when a key is released. See arcade.key """
        self.keys.discard(key)
        
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
        
        
    def toggle_gui(self):
        if self.ui_manager.is_enabled():
            self.ui_manager.disable()
        else:
            self.ui_manager.enable()
        
        
if __name__ == "__main__":
    import main
    main.main()
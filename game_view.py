import arcade
import math
import logging

logger = logging.getLogger("arcade")

class GameView(arcade.View):
    """ Represents a view inside of a Window """

    def __init__(self):
        """ Handles what to do when this view is created """
        super().__init__()

        self.tilemap:arcade.TileMap = None
        self.player:arcade.Sprite = None
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
        self.tilemap = arcade.TileMap("Assets/tilemaps/mymap.tmx", use_spatial_hash=True, layer_options=layer_options)
        self.spawnpoints = [tile.position for tile in self.tilemap.sprite_lists["Spawns"]]

        self.player = arcade.Sprite("Assets/racing-pack/PNG/Cars/car_black_1.png", 0.5)
        self.player.position = self.spawnpoints[0]
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

        self.keys = set()
        self.camera = arcade.Camera2D(position=self.player.position)
        self.physics = arcade.PymunkPhysicsEngine(damping=0.5, gravity=(0, 0))
        self.physics.add_sprite(self.player, mass=1, friction=0.6, collision_type="player", max_horizontal_velocity=600, max_vertical_velocity=600)
        self.physics.add_sprite_list(self.tilemap.sprite_lists["Walls"], collision_type="wall", body_type=arcade.PymunkPhysicsEngine.STATIC)
    
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

        
    #
    #
    def on_update(self, delta_time):
        """ Handles updating objects each frame """
        body = self.physics.get_physics_object(self.player).body
        
        if arcade.key.W in self.keys:
            angle_rads = math.radians(self.player.angle+90)
            fx = 1000 * math.cos(angle_rads)
            fy = 1000 * math.sin(angle_rads)
            logger.debug(f"Applying forward force ({fx}, {fy}) to player")
            body.apply_force_at_local_point((fx, fy), (0, 0))

        if arcade.key.S in self.keys:
            angle_rads = math.radians(self.player.angle+90)
            fx = 1000 * math.cos(angle_rads)
            fy = 1000 * math.sin(angle_rads)
            logger.debug(f"Applying backward force ({-fx}, {-fy}) to player")
            body.apply_force_at_local_point((-fx, -fy), (0, 0))
        if arcade.key.A in self.keys:
            logger.debug("Rotating player left")
            v = body.velocity

            if v.x != 0 or v.y != 0:
                body.angular_velocity -= math.radians(100)*delta_time
        if arcade.key.D in self.keys:
            logger.debug("Rotating player right")
            v = body.velocity
            if v.x != 0 or v.y != 0:
                body.angular_velocity += math.radians(100)*delta_time

        vx, vy = body.velocity
        speed = math.hypot(vx, vy)
        if speed > 0:
            vel_angle = math.atan2(vy, vx)
            facing_angle = math.radians(self.player.angle+90)
            new_angle = vel_angle + (facing_angle - vel_angle) * 0.1
            body.apply_force_at_local_point((speed * math.cos(new_angle), speed * math.sin(new_angle)), (0,0))


        self.physics.step(delta_time)
        self.camera.position = self.player.position
        
    #
    #
    def on_key_press(self, key: int, modifiers: int):
        """ Handles what to do when a key is initially pressed """
        self.keys.add(key)

    #
    #
    #
    def on_key_release(self, key: int, modifiers: int):
        """ Handles what to do when a key is released. See arcade.key """
        self.keys.remove(key)
        
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
        
        
        
        
        
if __name__ == "__main__":
    import main
    main.main()
import arcade
import math

class Car(arcade.Sprite):
    physics_engine:arcade.PymunkPhysicsEngine = None        
    def set_physics_engine(physics_engine:arcade.PymunkPhysicsEngine):
        """ Sets the physics engine for the car """
        Car.physics_engine = physics_engine

        old = physics_engine.add_sprite
        def _add_sprite_(sprite, *args, **kwargs):
            old(sprite, *args, **kwargs)
            if isinstance(sprite, Car):
                sprite.init_body()
        physics_engine.add_sprite = _add_sprite_

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

        if Car.physics_engine is None:
            raise ValueError("Physics engine not set for Car class. Call Car.set_physics_engine() before creating instances.")
        
    def init_body(self):
        
        self.body = Car.physics_engine.get_physics_object(self).body


    def move_forward(self, speed:float):
        """ Moves the car forward """
        self.radians = self.body.angle
        angle_rads = self.body.angle + math.pi/2
        fx = speed * math.cos(angle_rads)
        fy = speed * math.sin(angle_rads)
        self.body.apply_force_at_world_point((fx, fy), self.body.position)

    def turn_left(self, angle:float):
        """ Turns the car left """

        speed = math.hypot(self.body.velocity.x, self.body.velocity.y)
        
        if speed > 10:
            self.body.angular_velocity = math.radians(angle)
        
        else:
            self.body.angular_velocity = 0


    def turn_right(self, angle:float):
        """ Turns the car right """
        speed = math.hypot(self.body.velocity.x, self.body.velocity.y)
        
        if speed > 10:
            self.body.angular_velocity = -math.radians(angle) 
        
        else:
            self.body.angular_velocity = 0
    def move_backward(self, speed:float):
        """ Moves the car backward """
        self.radians = self.body.angle
        angle_rads = self.body.angle + math.pi/2
        fx = speed * math.cos(angle_rads)
        fy = speed * math.sin(angle_rads)
        self.body.apply_force_at_world_point((-fx, -fy), self.body.position)

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        """ Called when the car is moved by the physics engine """
        # print(f"Car moved by physics engine: dx={dx}, dy={dy}, d_angle={d_angle}")
        vx, vy = self.body.velocity
        fwd_x = math.cos(self.body.angle + math.pi/2)
        fwd_y = math.sin(self.body.angle + math.pi/2)
        fwd_spd = vx * fwd_x + vy * fwd_y
        lateral_spd = vx * -fwd_y + vy * fwd_x
        lateral_spd *= .8
        self.body.velocity = (
            fwd_x * fwd_spd + -fwd_y * lateral_spd,
            fwd_y * fwd_spd + fwd_x * lateral_spd
        )
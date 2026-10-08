import logging
from car import Car
from tracking_car import TrackingCar
import random
import arcade

logger = logging.getLogger("arcade")


class AICar(TrackingCar):
    counter = 0

    # Modification #1
    def __init__(self, cur_checkpoint, checkpoints, *args, num_movements=100, position=None, **kwargs):
        super().__init__(*args, **kwargs)
        
        if checkpoints is None:
            self.checkpoints = {}
        else:
            self.checkpoints = checkpoints

        self.cur_checkpoint = cur_checkpoint if cur_checkpoint is not None else None
        if position is not None:
            self.position = position

        self.replay_movements = True  # AI car always replays movements
        self.record_movements = True # AI car always records movements
        self.num_movements = num_movements

        self.movements = self.generate_movements(num_movements)  # Generate movements for 1000 frames
        self.rng = random.Random(AICar.counter)
        self.initial_state = self.rng.getstate()
        self.car_number = AICar.counter
        AICar.counter += 1

    def generate_movements(self, num_frames: int):
        """ Generates random movements for the AI car """
        
        for _ in range(num_frames):
            frame = []

            fb_move =self.rng.choice([0, 1, 2, 3, 6])
            if fb_move != 0:
                frame.append(fb_move)
           
            rl_move = self.rng.choice([0, 4, 5])
            if rl_move != 0:
                frame.append(rl_move)

            if len(frame) == 0:
                frame.append(0)  # Ensure at least one action per frame
            
            yield frame 

    # Modification #6
    def check_checkpoint(self):
        if str(self.cur_checkpoint) in self.checkpoints:
            if self.check_distance() < self.checkpoints["0"][0].width:
                self.cur_checkpoint += 1
                if str(self.cur_checkpoint) not in self.checkpoints:
                    self.cur_checkpoint = int(min(self.checkpoints.keys()))
                print("New checkpoint:", self.cur_checkpoint)
                return True
        return False

    def check_distance(self):
        if str(self.cur_checkpoint) in self.checkpoints:
            min_distance = float('inf')
            for tile in self.checkpoints[str(self.cur_checkpoint)]:
                distance = arcade.math.get_distance(*self.position, *tile.position)
                if distance < min_distance:
                    min_distance = distance
            return min_distance
        return float('inf')  # Return infinity if no current checkpoint

    # Modification #7
    def reset(self, position_to_reset_to=(0,0), angle_to_reset_to=0):
        """ Resets the car to a given position and resets its checkpoint """
        self.rng.setstate(self.initial_state)  # Reset the random number generator to iawts initial state
        self.movements = [k for k in self.recorded_movements]
        self.recorded_movements.clear()

        self.cur_checkpoint = 0
        self.replay_movements = True
        self.record_movements = True

        Car.physics_engine.set_position(self, position_to_reset_to)
        Car.physics_engine.set_rotation(self, angle_to_reset_to)
        Car.physics_engine.set_velocity(self, (0, 0))
        Car.physics_engine.set_horizontal_velocity(self, 0)

    def update(self, delta_time:float):
        super().update(delta_time)
        if self.check_checkpoint():
            logger.info(f"AI Car #{self.car_number} reached checkpoint {self.cur_checkpoint}.")


    

from tracking_car import TrackingCar
import random
rng = random.Random(42)

class AICar(TrackingCar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.replay_movements = True  # AI car always replays movements
        self.generate_movements(1000)  # Generate movements for 1000 frames

    def generate_movements(self, num_frames: int):
        """ Generates random movements for the AI car """
        movements = []
        for _ in range(num_frames):
            frame = []

            fb_move =rng.choice([0, 1, 2, 3, 6])
            if fb_move != 0:
                frame.append(fb_move)
           
            rl_move = rng.choice([0, 4, 5])
            if rl_move != 0:
                frame.append(rl_move)

            if len(frame) == 0:
                frame.append(0)  # Ensure at least one action per frame
            
            movements.append(frame)
        self.movements = movements  
   
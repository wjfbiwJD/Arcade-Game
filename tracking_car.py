import arcade
from car import Car
from action import Action
from constants import ACCELERATION, BRAKE_FORCE_MULTIPLIER, TURN_SENSITIVITY
import json

class TrackingCar(Car):
    
    """ A car that can be tracked by the camera """
    def __init__(self, *args, movements=None, **kwargs):
        super().__init__(*args, **kwargs)
        if movements is None:
            self.movements = []
        else:
            self.movements = movements
        self.replay_movements = len(self.movements) > 0
        self.current_frame = []

    def move_backward(self, speed:float):
        """ Moves the car backward """
        super().move_backward(speed)
        if not self.replay_movements:
            self.current_frame.append(Action.MOVE_BACKWARD.value)
        
    def move_forward(self, speed:float, boost:bool=False):
        """ Moves the car forward """
        super().move_forward(speed, boost=boost)
        if not self.replay_movements:
            self.current_frame.append(Action.MOVE_FORWARD.value if not boost else Action.MOVE_FORWARD_BOOST.value)

    def turn_left(self, speed:float):
        """ Turns the car left """
        super().turn_left(speed)
        if not self.replay_movements:
            self.current_frame.append(Action.TURN_LEFT.value)

    def turn_right(self, speed:float):
        """ Turns the car right """
        super().turn_right(speed)
        if not self.replay_movements:
            self.current_frame.append(Action.TURN_RIGHT.value)

    def update(self, delta_time:float):
        """ Updates the car's position based on its movements """
        if self.replay_movements and self.movements:
            frame = self.movements.pop(0)
            for num in frame:
                action = Action(num)
                if action == Action.MOVE_FORWARD:
                    self.move_forward(ACCELERATION)
                elif action == Action.MOVE_FORWARD_BOOST:
                    self.move_forward(ACCELERATION, boost=True)
                elif action == Action.MOVE_BACKWARD:
                    self.move_backward(ACCELERATION)
                elif action == Action.TURN_LEFT:
                    self.turn_left(TURN_SENSITIVITY)
                elif action == Action.TURN_RIGHT:
                    self.turn_right(TURN_SENSITIVITY)
                elif action == Action.EBRAKE:
                    self.ebrake(BRAKE_FORCE_MULTIPLIER)

    def ebrake(self, brake_force_multiplier:float=BRAKE_FORCE_MULTIPLIER):
        """ Applies an emergency brake to the car """
        super().ebrake(brake_force_multiplier)
        if not self.replay_movements:
            self.current_frame.append(Action.EBRAKE.value)

    def save_movements(self, filename:str):
        """ Saves the movements to a JSON file """
        with open(filename, 'w') as f:
            json.dump(self.movements, f)

    def load_movements(self, filename:str):
        """ Loads the movements from a JSON file """
        with open(filename, 'r') as f:
            self.movements = json.load(f)
            self.replay_movements = True

    def end_frame(self):
        """ Ends the current frame and appends it to the movements list """
        if not self.replay_movements:
            if not self.current_frame:
                self.movements.append([Action.IDLE.value])
            else:
                self.movements.append(self.current_frame.copy())
            self.current_frame.clear()

    

    
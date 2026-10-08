import arcade
from car import Car
from action import Action
from constants import ACCELERATION, BRAKE_FORCE_MULTIPLIER, TURN_SENSITIVITY
import json

class TrackingCar(Car):
    
    """ A car that can be tracked by the camera """
    def __init__(self, *args, movements=None, record_movements=False, **kwargs):
        super().__init__(*args, **kwargs)
        if movements is None:
            self.movements = []
        else:
            self.movements = movements

        self.record_movements = record_movements
        self.replay_movements = len(self.movements) > 0
        self.current_frame = []
        self.recorded_movements = []

    def move_backward(self, speed:float):
        """ Moves the car backward """
        super().move_backward(speed)
        if self.record_movements:
            self.current_frame.append(Action.MOVE_BACKWARD.value)
        
    def move_forward(self, speed:float, boost:bool=False):
        """ Moves the car forward """
        super().move_forward(speed, boost=boost)
        if self.record_movements:
            self.current_frame.append(Action.MOVE_FORWARD.value if not boost else Action.MOVE_FORWARD_BOOST.value)

    def turn_left(self, speed:float):
        """ Turns the car left """
        super().turn_left(speed)
        if self.record_movements:
            self.current_frame.append(Action.TURN_LEFT.value)

    def turn_right(self, speed:float):
        """ Turns the car right """
        super().turn_right(speed)
        if self.record_movements:
            self.current_frame.append(Action.TURN_RIGHT.value)

    def update(self, delta_time:float):
        """ Updates the car's position based on its movements """
        if self.replay_movements and self.movements:
            if isinstance(self.movements, list):
                frame = self.movements.pop(0)
            else:
                try:
                    frame = next(self.movements)
                except StopIteration:
                    self.replay_movements = False
                    self.record_movements = False
                    self.movements = []
                    return
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
            if self.record_movements:
                self.end_frame()  # End the frame after processing all actions

    def ebrake(self, brake_force_multiplier:float=BRAKE_FORCE_MULTIPLIER):
        """ Applies an emergency brake to the car """
        super().ebrake(brake_force_multiplier)
        if self.record_movements:
            self.current_frame.append(Action.EBRAKE.value)

    def save_movements(self, filename:str):
        """ Saves the movements to a JSON file """
        with open(filename, 'w') as f:
            json.dump(self.movements, f)

    def load_movements(self, filename:str, record_movements:bool = False):
        """ Loads the movements from a JSON file """
        with open(filename, 'r') as f:
            self.movements = json.load(f)
            self.replay_movements = True
            self.record_movements = record_movements
            self.recorded_movements.clear()
            self.current_frame = []

    def end_frame(self):
        """ Ends the current frame and appends it to the movements list """
        if self.record_movements:
            if not self.current_frame:
                self.recorded_movements.append([Action.IDLE.value])
            else:
                self.recorded_movements.append(self.current_frame.copy())
            self.current_frame.clear()

    def start_replay(self, record_movements:bool = False):
        """ Starts replaying the recorded movements """
        self.movements = [movement for movement in self.recorded_movements]
        self.replay_movements = True
        self.record_movements = record_movements
        self.recorded_movements.clear()
        self.current_frame = []
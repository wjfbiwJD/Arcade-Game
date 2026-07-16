import arcade
from car import Car
from action import Action
from constants import SPEED, TURN_SENSITIVITY

class TrackingCar(Car):
    
    """ A car that can be tracked by the camera """
    def __init__(self, *args, movements=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.movements = movements if movements is not None else []
        self.replay_movements = len(self.movements) > 0

    def move_backward(self, speed:float):
        """ Moves the car backward """
        super().move_backward(speed)
        if self.replay_movements:
            self.movements.append(Action.MOVE_BACKWARD)
        
    def move_forward(self, speed:float):
        """ Moves the car forward """
        super().move_forward(speed)
        if self.replay_movements:
            self.movements.append(Action.MOVE_FORWARD)

    def turn_left(self, speed:float):
        """ Turns the car left """
        super().turn_left(speed)
        if self.replay_movements:
            self.movements.append(Action.TURN_LEFT)

    def turn_right(self, speed:float):
        """ Turns the car right """
        super().turn_right(speed)
        if self.replay_movements:
            self.movements.append(Action.TURN_RIGHT)

    def update(self, delta_time:float):
        """ Updates the car's position based on its movements """
        if self.replay_movements and self.movements:
            action = self.movements.pop(0)
            if action == Action.MOVE_FORWARD:
                self.move_forward(SPEED)
            elif action == Action.MOVE_BACKWARD:
                self.move_backward(SPEED)
            elif action == Action.TURN_LEFT:
                self.turn_left(TURN_SENSITIVITY)
            elif action == Action.TURN_RIGHT:
                self.turn_right(TURN_SENSITIVITY)

    

    
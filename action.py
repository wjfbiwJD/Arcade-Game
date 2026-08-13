from enum import Enum

class Action(Enum):
    IDLE = 0
    MOVE_FORWARD = 1
    MOVE_FORWARD_BOOST = 2
    MOVE_BACKWARD = 3
    TURN_LEFT = 4
    TURN_RIGHT = 5
    EBRAKE = 6
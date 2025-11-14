from pico2d import load_image

import game_framework
from state_machine import StateMachine

class Run:
    pass

class Idle:
    pass

class Punch:
    def __init__(self, player_id = 1, start_x = 100, start_y = 180):
        pass
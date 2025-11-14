from pico2d import load_image

import game_framework
from state_machine import StateMachine

class Run:
    pass

class Idle:
    pass

class Punch:
    image_ia1 = None
    image_ia2 = None
    image_ia3 = None
    def __init__(self, player_id = 1, start_x = 100, start_y = 180):
        if Punch.image_ia1 == None:
            Punch.image_ia1 = load_image('Punch0101-sheet.png')
        if Punch.image_ia2 == None:
            Punch.image_ia2 = load_image('Punch0201-sheet.png')
        if Punch.image_ia3 == None:
            Punch.image_ia3 = load_image('Punch0301-sheet.png')
        self.player_id = player_id
        self.x, self.y = start_x, start_y
        self.frame = 0
        self.face_dir = 1 if player_id == 1 else -1

    def update(self):
        pass

    def handle_event(self, event):
        pass

    def draw(self):
        pass

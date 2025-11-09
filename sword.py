from pico2d import load_image

import game_framework
from state_machine import StateMachine

class Run:
    pass

class Idle:
    pass

class Sword:
    image_idle = None
    image_run = None
    image_ia = None
    image_ra = None

    def __init__(self):
        if Sword.image_idle == None:
            Sword.image_idle = load_image('SwordIdle01-sheet.png')
        if Sword.image_run == None:
            Sword.image_run = load_image('SwordRun01_right.png')
        if Sword.image_ia == None:
            Sword.image_ia = load_image('swordcombo.png')
        if Sword.image_ra == None:
            Sword.image_ra = load_image('SwordRunSlash01_right.png')
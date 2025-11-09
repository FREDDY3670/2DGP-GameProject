from pico2d import load_image
from sdl2 import SDL_KEYDOWN, SDLK_LEFT, SDLK_RIGHT, SDL_KEYUP, SDLK_SPACE

import game_framework
from state_machine import StateMachine

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT

def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT

def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

class Run:
    def __init__(self,Sword):
        pass

class Idle:
    def __init__(self,Sword):
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

        self.x, self.y = 100, 180
        self.frame = 0
        self.face_dir = 1

        self.IDLE = Idle(self)
        self.RUN = Run(self)

        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {},
                self.RUN: {}
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()
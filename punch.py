from pico2d import load_image
from sdl2 import SDLK_SPACE, SDL_KEYDOWN, SDLK_RETURN, SDLK_a, SDLK_LEFT, SDLK_RIGHT, SDLK_d, SDLK_w, SDLK_UP, \
    SDL_KEYUP, SDLK_DOWN, SDLK_s

import game_framework
from state_machine import StateMachine

def space_down(e):
    return (e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and
            (e[1].key == SDLK_SPACE or e[1].key == SDLK_RETURN))

def left_down(e):
    return (e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and
            (e[1].key == SDLK_LEFT or e[1].key == SDLK_a))

def right_down(e):
    return (e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and
            (e[1].key == SDLK_RIGHT or e[1].key == SDLK_d))

def right_up(e):
    return (e[0] == 'INPUT' and e[1].type == SDL_KEYUP and
            (e[1].key == SDLK_RIGHT or e[1].key == SDLK_d))

def left_up(e):
    return (e[0] == 'INPUT' and e[1].type == SDL_KEYUP and
            (e[1].key == SDLK_LEFT or e[1].key == SDLK_a))

def up_down(e):
    return (e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and
            (e[1].key == SDLK_w) or e[1].key == SDLK_UP)

def up_up(e):
    return (e[0] == 'INPUT' and e[1].type == SDL_KEYUP and
            (e[1].key == SDLK_w) or e[1].key == SDLK_UP)

def down_down(e):
    return (e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and
            (e[1].key == SDLK_s) or e[1].key == SDLK_DOWN)

def down_up(e):
    return (e[0] == 'INPUT' and e[1].type == SDL_KEYUP and
            (e[1].key == SDLK_s) or e[1].key == SDLK_DOWN)

class Run:
    def __init__(self, Punch):
        self.Punch = Punch
    def enter(self,e):
        pass
    def exit(self,e):
        pass
    def do(self):
        pass
    def draw(self):
        pass

class Idle:
    def __init__(self, Punch):
        self.Punch = Punch

    def enter(self, e):
        pass

    def exit(self, e):
        pass

    def do(self):
        pass

    def draw(self):
        pass

class Punch:
    image_ia1 = None
    image_ia2 = None
    image_ia3 = None
    image_idle = None
    def __init__(self, player_id = 1, start_x = 100, start_y = 180):
        if Punch.image_ia1 == None:
            Punch.image_ia1 = load_image('Punch0101-sheet.png')
        if Punch.image_ia2 == None:
            Punch.image_ia2 = load_image('Punch0201-sheet.png')
        if Punch.image_ia3 == None:
            Punch.image_ia3 = load_image('Punch0301-sheet.png')
        if Punch.image_idle == None:
            Punch.image_idle = load_image('Idle01-sheet.png')
        self.player_id = player_id
        self.x, self.y = start_x, start_y
        self.frame = 0
        self.face_dir = 1 if player_id == 1 else -1

        self.IDLE = Idle(self)
        self.RUN = Run(self)

        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {left_down: self.RUN, right_down: self.RUN, space_down: self.IDLE},
                self.RUN: {left_up: self.IDLE, right_up: self.IDLE, right_down: self.IDLE, left_down: self.IDLE,
                           space_down: self.RUN}
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        if self.player_id == 1:
            if event.type == SDL_KEYDOWN:
                if event.key not in (SDLK_a, SDLK_d, SDLK_SPACE):
                    return
            elif event.type == SDL_KEYUP:
                if event.key not in (SDLK_a, SDLK_d):
                    return
        else:
            if event.type == SDL_KEYDOWN:
                if event.key not in (SDLK_LEFT, SDLK_RIGHT, SDLK_RETURN):
                    return
            elif event.type == SDL_KEYUP:
                if event.key not in (SDLK_LEFT, SDLK_RIGHT):
                    return
        self.state_machine.handle_state_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()

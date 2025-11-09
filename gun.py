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

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 40.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Idle:
    def __init__(self,Gun):
        self.gun = Gun
        self.atk = False
    def enter(self,e):
        self.gun.frame = 0
        if left_up(e):
            self.gun.face_dir = -1
        elif right_up(e):
            self.gun.face_dir = 1
    def exit(self,e):
        pass
    def do(self):
        pass
    def draw(self):
        if self.gun.face_dir == 1:
            self.gun.image_idle.clip_draw(int(self.gun.frame) * 96, 0, 96, 84, self.gun.x, self.gun.y, 200,
                                              200)
        else:
            self.gun.image_idle.clip_composite_draw(int(self.gun.frame) * 96, 0, 96, 84,0,'h', self.gun.x, self.gun.y, 200,
                                              200)

class Run:
    def __init__(self,Gun):
        self.gun = Gun
        self.atk = False
    def enter(self,e):
        if left_down(e):
            self.gun.face_dir = -1
        elif right_down(e):
            self.gun.face_dir = 1
    def exit(self,e):
        pass
    def do(self):
        self.gun.frame = (self.gun.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        self.gun.x += self.gun.face_dir * RUN_SPEED_PPS * game_framework.frame_time
    def draw(self):
        if self.gun.face_dir == 1:
            self.gun.image_run.clip_draw(int(self.gun.frame) * 96, 0, 96, 84, self.gun.x, self.gun.y, 200,
                                              200)
        else:
            self.gun.image_run.clip_composite_draw(int(self.gun.frame) * 96, 0, 96, 84,0,'h', self.gun.x, self.gun.y, 200,
                                              200)

class Gun:
    image_idle = None
    image_run = None
    image_ia = None
    image_ra = None
    def __init__(self):
        if Gun.image_idle == None:
            Gun.image_idle = load_image('GunAim.png')
        if Gun.image_run == None:
            Gun.image_run = load_image('GunRun.png')
        if Gun.image_ia == None:
            Gun.image_ia = load_image('GunFire.png')
        if Gun.image_ra == None:
            Gun.image_ra = load_image('GunRunFire01-sheet.png')

        self.x, self.y = 100, 180
        self.frame = 0
        self.face_dir = 1

        self.IDLE = Idle(self)
        self.RUN = Run(self)

        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {left_down : self.RUN, right_down : self.RUN,space_down : self.IDLE},
                self.RUN: {space_down : self.RUN, left_up : self.IDLE, right_up : self.IDLE, right_down : self.IDLE, left_down : self.IDLE}
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()
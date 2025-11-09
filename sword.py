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

class Run:
    def __init__(self, Sword):
        self.Sword = Sword
        self.atk = False
        self.atk_frame = 8

    def enter(self, e):
        if right_down(e):
            self.Sword.face_dir = 1
        elif left_down(e):
            self.Sword.face_dir = -1
        elif space_down(e):
            self.atk = True
            self.Sword.frame = 0

    def exit(self, e):
        self.atk = False

    def do(self):

        if self.atk == True:
            self.Sword.frame = (self.Sword.frame + 7 * ACTION_PER_TIME * game_framework.frame_time)
            if self.Sword.frame >= self.atk_frame:
                self.atk = False  # 공격 종료
                self.Sword.frame = 0
        else:
            self.Sword.frame = (self.Sword.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        self.Sword.x += self.Sword.face_dir * RUN_SPEED_PPS * game_framework.frame_time

    def draw(self):
        if self.atk == False:
            if self.Sword.face_dir == 1:  # right
                self.Sword.image_run.clip_draw(int(self.Sword.frame) * 96, 0, 96, 84, self.Sword.x, self.Sword.y, 200,
                                               200)
            else:
                self.Sword.image_run.clip_composite_draw(int(self.Sword.frame) * 96, 0, 96, 84, 0, 'h', self.Sword.x,
                                                         self.Sword.y, 200, 200)
        else:
            if self.Sword.face_dir == 1:  # right
                self.Sword.image_ra.clip_draw(int(self.Sword.frame) * 96, 0, 96, 84, self.Sword.x, self.Sword.y, 200,
                                              200)
            else:
                self.Sword.image_ra.clip_composite_draw(int(self.Sword.frame) * 96, 0, 96, 84, 0, 'h', self.Sword.x,
                                                        self.Sword.y, 200, 200)

class Idle:
    def __init__(self,Sword):
        self.Sword = Sword
        self.atk = False
        self.atk_count = 0
        self.combo_timer = 0
        self.COMBO_TIME_LIMIT = 0.7
        self.atk_frame = 0
        self.row = 0

    def enter(self, e):
        if space_down(e):
            self.atk = True
            self.atk_count += 1
            self.combo_timer = 0
            self.Sword.frame = 0

    def exit(self, e):
        pass

    def do(self):
        if self.atk:
            if self.atk_frame == 0:
                self.row = (self.atk_count - 1) % 4
                if self.row == 0:
                    self.atk_frame = 6
                elif self.row == 1 or self.row == 2:
                    self.atk_frame = 5
                elif self.row == 3:
                    self.atk_frame = 6
            self.Sword.frame = (self.Sword.frame + 7 * ACTION_PER_TIME * game_framework.frame_time)
            if self.Sword.frame >= self.atk_frame:
                self.atk = False
                self.atk_frame = 0
                self.combo_timer = 0
                self.Sword.frame = 0
        else:
            self.Sword.frame = (self.Sword.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 7
            if self.atk_count > 0:
                self.combo_timer += game_framework.frame_time
                if self.combo_timer >= self.COMBO_TIME_LIMIT:
                    self.atk_count = 0
                    self.combo_timer = 0
                    self.Sword.frame = 0

    def draw(self):
        if self.atk == False:
            if self.Sword.face_dir == 1:  # right
                self.Sword.image_idle.clip_draw(int(self.Sword.frame) * 96, 0, 96, 84, self.Sword.x, self.Sword.y, 200,
                                                200)
            else:
                self.Sword.image_idle.clip_composite_draw(int(self.Sword.frame) * 96, 0, 96, 84, 0, 'h', self.Sword.x,
                                                          self.Sword.y, 200, 200)
        else:
            if self.Sword.face_dir == 1:
                self.Sword.image_ia.clip_draw(int(self.Sword.frame) * 96, self.row * 84, 96, 84, self.Sword.x,
                                              self.Sword.y, 200, 200)
            else:
                self.Sword.image_ia.clip_composite_draw(int(self.Sword.frame) * 96, self.row * 84, 96, 84, 0, 'h',
                                                        self.Sword.x, self.Sword.y, 200, 200)


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
                self.IDLE: {space_down : self.IDLE},
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
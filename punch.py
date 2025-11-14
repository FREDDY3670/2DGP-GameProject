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

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 40.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Run:
    def __init__(self, Punch):
        self.Punch = Punch

    def enter(self, e):
        if right_down(e):
            self.Punch.face_dir = 1
        elif left_down(e):
            self.Punch.face_dir = -1

    def exit(self, e):
        pass

    def do(self):
        self.Punch.frame = (self.Punch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        self.Punch.x += self.Punch.face_dir * RUN_SPEED_PPS * game_framework.frame_time

    def draw(self):
        if self.Punch.face_dir == 1:
            self.Punch.image_run.clip_draw(int(self.Punch.frame) * 96, 0, 96, 84, self.Punch.x, self.Punch.y, 200, 200)
        else:
            self.Punch.image_run.clip_composite_draw(int(self.Punch.frame) * 96, 0, 96, 84, 0, 'h', self.Punch.x, self.Punch.y, 200, 200)

class Idle:
    def __init__(self, Punch):
        self.Punch = Punch
        self.atk = False
        self.atk_count = 0
        self.combo_timer = 0
        self.COMBO_TIME_LIMIT = 0.75
        self.atk_frame = 0

    def enter(self, e):
        if space_down(e):
            self.atk = True
            self.Punch.frame = 0
            if self.atk_count == 3:
                self.atk_count = 1
            else:
                self.atk_count += 1
            self.combo_timer = 0

    def exit(self, e):
        pass

    def do(self):
        if self.atk == False:
            self.Punch.frame = (self.Punch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 7
            if self.atk_count > 0:
                self.combo_timer += game_framework.frame_time
                if self.combo_timer >= self.COMBO_TIME_LIMIT:
                    self.atk_count = 0
                    self.combo_timer = 0
                    self.Punch.frame = 0
        else:
            if self.atk_frame == 0:
                if self.atk_count == 1:
                    self.atk_frame = 6
                elif self.atk_count == 2:
                    self.atk_frame = 4
                elif self.atk_count == 3:
                    self.atk_frame = 7

            self.Punch.frame = (self.Punch.frame + 7 * ACTION_PER_TIME * game_framework.frame_time)
            if self.Punch.frame >= self.atk_frame:
                self.atk = False
                self.atk_frame = 0
                self.combo_timer = 0
                self.Punch.frame = 0

    def draw(self):
        if self.atk == False:
            if self.Punch.face_dir == 1:
                self.Punch.image_idle.clip_draw(int(self.Punch.frame) * 96, 0, 96, 84, self.Punch.x, self.Punch.y, 200,
                                                200)
            else:
                self.Punch.image_idle.clip_composite_draw(int(self.Punch.frame) * 96, 0, 96, 84, 0, 'h', self.Punch.x,
                                                          self.Punch.y, 200, 200)
        else:
            if self.Punch.face_dir == 1:
                if self.atk_count == 1:
                    self.Punch.image_ia1.clip_draw(int(self.Punch.frame) * 96, 0, 96, 84, self.Punch.x, self.Punch.y,
                                                   200, 200)
                elif self.atk_count == 2:
                    self.Punch.image_ia2.clip_draw(int(self.Punch.frame) * 96, 0, 96, 84, self.Punch.x, self.Punch.y,
                                                   200, 200)
                elif self.atk_count == 3:
                    self.Punch.image_ia3.clip_draw(int(self.Punch.frame) * 96, 0, 96, 84, self.Punch.x, self.Punch.y,
                                                   200, 200)
            else:
                if self.atk_count == 1:
                    self.Punch.image_ia1.clip_composite_draw(int(self.Punch.frame) * 96, 0, 96, 84, 0, 'h',
                                                             self.Punch.x, self.Punch.y, 200, 200)
                elif self.atk_count == 2:
                    self.Punch.image_ia2.clip_composite_draw(int(self.Punch.frame) * 96, 0, 96, 84, 0, 'h',
                                                             self.Punch.x, self.Punch.y, 200, 200)
                elif self.atk_count == 3:
                    self.Punch.image_ia3.clip_composite_draw(int(self.Punch.frame) * 96, 0, 96, 84, 0, 'h', self.Punch.x, self.Punch.y, 200, 200)

class Punch:
    image_ia1 = None
    image_ia2 = None
    image_ia3 = None
    image_idle = None
    image_run = None
    def __init__(self, player_id = 1, start_x = 100, start_y = 180):
        if Punch.image_ia1 == None:
            Punch.image_ia1 = load_image('Punch0101-sheet.png')
        if Punch.image_ia2 == None:
            Punch.image_ia2 = load_image('Punch0201-sheet.png')
        if Punch.image_ia3 == None:
            Punch.image_ia3 = load_image('Punch0301-sheet.png')
        if Punch.image_idle == None:
            Punch.image_idle = load_image('Idle01-sheet.png')
        if Punch.image_run == None:
            Punch.image_run = load_image('Run.png')
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

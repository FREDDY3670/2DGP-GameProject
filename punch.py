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

    def get_bb(self):
        return self.Punch.x - 30, self.Punch.y - 100, self.Punch.x + 30, self.Punch.y

    def enter(self, e):
        if e is None:
            return
        if right_down(e):
            self.Punch.face_dir = 1
        elif left_down(e):
            self.Punch.face_dir = -1

    def exit(self, e):
        pass

    def do(self):
        self.Punch.frame = (self.Punch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

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

    def get_bb(self):
        return self.Punch.x - 30, self.Punch.y - 100, self.Punch.x + 30, self.Punch.y

    def enter(self, e):
        if space_down(e):
            self.atk = True
            self.Punch.frame = 0
            self.atk_frame = 0
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
                self.Punch.frame = 0
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

class Jump:
    def __init__(self, Punch):
        self.Punch = Punch

    def get_bb(self):
        return self.Punch.x - 30, self.Punch.y - 100, self.Punch.x + 30, self.Punch.y

    def enter(self, e):
        if e and up_down(e) and self.Punch.on_ground:
            self.Punch.velocity_y = self.Punch.jump_speed
            self.Punch.on_ground = False

    def exit(self, e):
        self.Punch.velocity_x = 0

    def do(self):
        self.Punch.frame = (self.Punch.frame + 3 * ACTION_PER_TIME * game_framework.frame_time) % 3

    def draw(self):
        if self.Punch.face_dir == 1:
            self.Punch.image_jump.clip_draw(int(self.Punch.frame) * 96, 0, 96, 84, self.Punch.x, self.Punch.y, 200, 200)
        else:
            self.Punch.image_jump.clip_composite_draw(int(self.Punch.frame) * 96, 0, 96, 84, 0, 'h', self.Punch.x, self.Punch.y, 200, 200)

class Punch:
    image_ia1 = None
    image_ia2 = None
    image_ia3 = None
    image_idle = None
    image_run = None
    image_jump = None

    def __init__(self, player_id=1, start_x=100, start_y=180):
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
        if Punch.image_jump == None:
            Punch.image_jump = load_image('Jump01-sheet.png')

        self.player_id = player_id
        self.x, self.y = start_x, start_y
        self.frame = 0
        self.face_dir = 1 if player_id == 1 else -1
        self.prev_x = start_x
        self.prev_y = start_y

        self.velocity_y = 0
        self.velocity_x = 0
        self.gravity = 980
        self.jump_speed = 400
        self.on_ground = False

        self.left_pressed = False
        self.right_pressed = False

        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.JUMP = Jump(self)

        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {left_down: self.RUN, right_down: self.RUN, space_down: self.IDLE, up_down: self.JUMP},
                self.RUN: {left_up: self.IDLE, right_up: self.IDLE, right_down: self.IDLE, left_down: self.IDLE,
                           space_down: self.RUN, up_down: self.JUMP},
                self.JUMP: {right_down: self.JUMP, left_down: self.JUMP, left_up: self.JUMP, right_up: self.JUMP}
            }
        )

    def update(self):
        self.prev_x = self.x
        self.prev_y = self.y

        self.on_ground = False

        self.velocity_y -= self.gravity * game_framework.frame_time
        self.y += self.velocity_y * game_framework.frame_time

        # 상태별 이동 처리
        if isinstance(self.state_machine.cur_state, Jump):
            if self.left_pressed:
                self.velocity_x = -RUN_SPEED_PPS
                self.face_dir = -1
            elif self.right_pressed:
                self.velocity_x = RUN_SPEED_PPS
                self.face_dir = 1
            else:
                self.velocity_x = 0
        elif isinstance(self.state_machine.cur_state, Run):
            if self.left_pressed and self.right_pressed:
                self.velocity_x = 0
            elif self.left_pressed:
                self.velocity_x = -RUN_SPEED_PPS
                self.face_dir = -1
            elif self.right_pressed:
                self.velocity_x = RUN_SPEED_PPS
                self.face_dir = 1
            else:
                self.velocity_x = 0
        else:  # Idle
            self.velocity_x = 0

        self.x += self.velocity_x * game_framework.frame_time
        self.state_machine.update()

    def handle_event(self, event):
        if self.player_id == 1:
            if event.type == SDL_KEYDOWN:
                if event.key == SDLK_a:
                    self.left_pressed = True
                elif event.key == SDLK_d:
                    self.right_pressed = True
                elif event.key not in (SDLK_SPACE,):
                    return
            elif event.type == SDL_KEYUP:
                if event.key == SDLK_a:
                    self.left_pressed = False
                elif event.key == SDLK_d:
                    self.right_pressed = False
                elif event.key not in (SDLK_a, SDLK_d):
                    return
        else:
            if event.type == SDL_KEYDOWN:
                if event.key == SDLK_LEFT:
                    self.left_pressed = True
                elif event.key == SDLK_RIGHT:
                    self.right_pressed = True
                elif event.key not in (SDLK_RETURN,):
                    return
            elif event.type == SDL_KEYUP:
                if event.key == SDLK_LEFT:
                    self.left_pressed = False
                elif event.key == SDLK_RIGHT:
                    self.right_pressed = False
                elif event.key not in (SDLK_LEFT, SDLK_RIGHT):
                    return

        if isinstance(self.state_machine.cur_state, Run):
            if not self.left_pressed and not self.right_pressed:
                self.state_machine.cur_state.exit(('INPUT', event))
                self.state_machine.cur_state = self.IDLE
                self.state_machine.cur_state.enter(('INPUT', event))
                return

        self.state_machine.handle_state_event(('INPUT', event))

    def handle_collision(self, group, other):
        if group == 'player:tile':
            punch_left, punch_bottom, punch_right, punch_top = self.get_bb()
            tile_left, tile_bottom, tile_right, tile_top = other.get_bb()

            prev_left = self.prev_x - 30
            prev_right = self.prev_x + 30
            prev_bottom = self.prev_y - 100
            prev_top = self.prev_y

            overlap_x = min(punch_right - tile_left, tile_right - punch_left)
            overlap_y = min(punch_top - tile_bottom, tile_top - punch_bottom)

            was_above = prev_bottom >= tile_top
            was_below = prev_top <= tile_bottom
            was_left = prev_right <= tile_left
            was_right = prev_left >= tile_right

            if overlap_y < overlap_x:
                if was_above:
                    self.y = tile_top + 100
                    self.velocity_y = 0
                    self.on_ground = True
                    return
                if was_below and self.velocity_y > 0:
                    self.y = tile_bottom
                    self.velocity_y = 0
                    return

            else:
                if was_left:
                    self.x = tile_left - 30
                    self.velocity_x = 0
                    return

                if was_right:
                    self.x = tile_right + 30
                    self.velocity_x = 0
                    return

    def draw(self):
        self.state_machine.draw()

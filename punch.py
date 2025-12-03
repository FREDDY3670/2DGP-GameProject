from pico2d import load_image, draw_rectangle
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
        self.atk = False
        self.atk_timer = 0
        self.slide_speed = 0
        self.INITIAL_SLIDE_SPEED = 800.0
        self.SLIDE_FRICTION = 400.0

    def get_bb(self):
        if self.atk == False:
            if self.Punch.face_dir == 1:
                return self.Punch.x - 30, self.Punch.y - 100, self.Punch.x + 25, self.Punch.y - 10
            else:
                return self.Punch.x - 25, self.Punch.y - 100, self.Punch.x + 30, self.Punch.y - 10
        else:
            if self.Punch.face_dir == 1:
                return self.Punch.x - 45, self.Punch.y - 100, self.Punch.x + 50, self.Punch.y - 40
            else:
                return self.Punch.x - 50, self.Punch.y - 100, self.Punch.x + 45, self.Punch.y - 40
    def get_weapon_bb(self):
        if self.atk:
            if self.Punch.face_dir == 1:
                return self.Punch.x, self.Punch.y - 100, self.Punch.x + 50, self.Punch.y - 80
            else:
                return self.Punch.x - 50, self.Punch.y - 100, self.Punch.x, self.Punch.y - 80
        else:
            return None

    def enter(self, e):
        if e is None:
            return
        if right_down(e):
            self.Punch.face_dir = 1
        elif left_down(e):
            self.Punch.face_dir = -1
        elif space_down(e):
            self.atk = True
            self.atk_timer = 0
            self.slide_speed = self.INITIAL_SLIDE_SPEED
            self.Punch.frame = 0

    def exit(self, e):
        self.atk = False
        self.atk_timer = 0
        self.slide_speed = 0

    def do(self):
        if self.atk:
            self.atk_timer += game_framework.frame_time
            self.slide_speed -= self.SLIDE_FRICTION * game_framework.frame_time
            if self.slide_speed < 0:
                self.slide_speed = 0

            self.Punch.x += self.slide_speed * self.Punch.face_dir * game_framework.frame_time
            if self.atk_timer >= 0.2:
                self.atk = False
                self.atk_timer = 0
                self.Punch.frame = 0
            else:
                self.Punch.frame = (self.Punch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 1
        else:
            self.Punch.frame = (self.Punch.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

    def draw(self):
        draw_rectangle(*self.get_bb())
        weapon = self.get_weapon_bb()
        if weapon:
            draw_rectangle(*weapon)
        if self.atk == False:
            if self.Punch.face_dir == 1:
                self.Punch.image_run.clip_draw(int(self.Punch.frame) * 96, 0, 96, 84, self.Punch.x, self.Punch.y, 200, 200)
            else:
                self.Punch.image_run.clip_composite_draw(int(self.Punch.frame) * 96, 0, 96, 84, 0, 'h', self.Punch.x, self.Punch.y, 200, 200)
        else:
            if self.Punch.face_dir == 1:
                self.Punch.image_slide.clip_draw(int(self.Punch.frame) * 96, 0, 96, 84, self.Punch.x, self.Punch.y, 200, 200)
            else:
                self.Punch.image_slide.clip_composite_draw(int(self.Punch.frame) * 96, 0, 96, 84, 0, 'h', self.Punch.x, self.Punch.y, 200, 200)

class Idle:
    def __init__(self, Punch):
        self.Punch = Punch
        self.atk = False
        self.atk_count = 0
        self.combo_timer = 0
        self.COMBO_TIME_LIMIT = 0.75
        self.atk_frame = 0

    def get_bb(self):
        frame = int(self.Punch.frame)
        if self.Punch.face_dir == 1:
            if self.atk == False:
                return self.Punch.x - 20, self.Punch.y - 100, self.Punch.x + 20, self.Punch.y - 5
            else:
                if self.atk_count == 1:
                    if frame == 0:
                        return self.Punch.x - 30, self.Punch.y - 100, self.Punch.x + 25, self.Punch.y - 7
                    elif frame == 1:
                        return self.Punch.x - 35, self.Punch.y - 100, self.Punch.x + 25, self.Punch.y - 5
                    elif frame == 2:
                        return self.Punch.x - 20, self.Punch.y - 100, self.Punch.x + 70, self.Punch.y - 20
                    else:
                        return self.Punch.x - 15, self.Punch.y - 100, self.Punch.x + 30, self.Punch.y - 10
                elif self.atk_count == 2:
                    if frame == 0:
                        return self.Punch.x - 35, self.Punch.y - 100, self.Punch.x + 20, self.Punch.y - 10
                    elif frame == 1 or frame == 2:
                        return self.Punch.x - 30, self.Punch.y - 100, self.Punch.x + 50, self.Punch.y - 10
                    else:
                        return self.Punch.x - 25, self.Punch.y - 100, self.Punch.x + 20, self.Punch.y - 5
                else:
                    if frame == 0:
                        return self.Punch.x - 40, self.Punch.y - 100, self.Punch.x + 20, self.Punch.y
                    elif frame == 1:
                        return self.Punch.x - 35, self.Punch.y - 100, self.Punch.x + 15, self.Punch.y + 10
                    elif frame == 2:
                        return self.Punch.x - 32, self.Punch.y - 100, self.Punch.x + 45, self.Punch.y + 12
                    elif frame == 3 or frame == 4:
                        return self.Punch.x - 25, self.Punch.y - 100, self.Punch.x + 40, self.Punch.y + 10
                    elif frame == 5:
                        return self.Punch.x - 30, self.Punch.y - 100, self.Punch.x + 40, self.Punch.y - 7
                    elif frame == 6:
                        return self.Punch.x - 20, self.Punch.y - 100, self.Punch.x + 20, self.Punch.y - 10
        else:
            if self.atk == False:
                return self.Punch.x - 20, self.Punch.y - 100, self.Punch.x + 20, self.Punch.y - 5
            else:
                if self.atk_count == 1:
                    if frame == 0:
                        return self.Punch.x - 25, self.Punch.y - 100, self.Punch.x + 30, self.Punch.y - 7
                    elif frame == 1:
                        return self.Punch.x - 25, self.Punch.y - 100, self.Punch.x + 35, self.Punch.y - 5
                    elif frame == 2:
                        return self.Punch.x - 70, self.Punch.y - 100, self.Punch.x + 20, self.Punch.y - 20
                    else:
                        return self.Punch.x - 30, self.Punch.y - 100, self.Punch.x + 15, self.Punch.y - 10
                elif self.atk_count == 2:
                    if frame == 0:
                        return self.Punch.x - 20, self.Punch.y - 100, self.Punch.x + 35, self.Punch.y - 10
                    elif frame == 1 or frame == 2:
                        return self.Punch.x - 50, self.Punch.y - 100, self.Punch.x + 30, self.Punch.y - 10
                    else:
                        return self.Punch.x - 20, self.Punch.y - 100, self.Punch.x + 25, self.Punch.y - 5
                else:
                    if frame == 0:
                        return self.Punch.x - 20, self.Punch.y - 100, self.Punch.x + 40, self.Punch.y
                    elif frame == 1:
                        return self.Punch.x - 15, self.Punch.y - 100, self.Punch.x + 35, self.Punch.y + 10
                    elif frame == 2:
                        return self.Punch.x - 45, self.Punch.y - 100, self.Punch.x + 32, self.Punch.y + 12
                    elif frame == 3 or frame == 4:
                        return self.Punch.x - 40, self.Punch.y - 100, self.Punch.x + 25, self.Punch.y + 10
                    elif frame == 5:
                        return self.Punch.x - 40, self.Punch.y - 100, self.Punch.x + 30, self.Punch.y - 7
                    elif frame == 6:
                        return self.Punch.x - 20, self.Punch.y - 100, self.Punch.x + 20, self.Punch.y - 10

    def get_weapon_bb(self):
        if not self.atk:
            return None

        frame = int(self.Punch.frame)

        if self.Punch.face_dir == 1:
            if self.atk_count == 1:
                if frame == 2:
                    return self.Punch.x + 20, self.Punch.y - 100, self.Punch.x + 70, self.Punch.y - 20
                else:
                    return None
            elif self.atk_count == 2:
                if frame == 1 or frame == 2:
                    return self.Punch.x + 20, self.Punch.y - 100, self.Punch.x + 50, self.Punch.y - 10
                else:
                    return None
            else:
                if frame >= 2 and frame <= 5:
                    return self.Punch.x + 15, self.Punch.y - 100, self.Punch.x + 45, self.Punch.y + 12
                else:
                    return None
        else:
            if self.atk_count == 1:
                if frame == 2:
                    return self.Punch.x - 70, self.Punch.y - 100, self.Punch.x - 20, self.Punch.y - 20
                else:
                    return None
            elif self.atk_count == 2:
                if frame == 1 or frame == 2:
                    return self.Punch.x - 50, self.Punch.y - 100, self.Punch.x - 20, self.Punch.y - 10
                else:
                    return None
            else:
                if frame >= 2 and frame <= 5:
                    return self.Punch.x - 45, self.Punch.y - 100, self.Punch.x - 15, self.Punch.y + 12
                else:
                    return None

    def enter(self, e):
        if e and space_down(e) and not self.atk:
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
        draw_rectangle(*self.get_bb())
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
        self.atk = False
        self.FAST_FALL_SPEED = -800
        self.DASH_SPEED = 400

    def get_bb(self):
        if self.Punch.frame == 0:
            if self.Punch.face_dir == 1:
                return self.Punch.x - 25, self.Punch.y - 100, self.Punch.x + 30, self.Punch.y
            else:
                return self.Punch.x - 30, self.Punch.y - 100, self.Punch.x + 25, self.Punch.y
        elif self.Punch.frame == 1:
            if self.Punch.face_dir == 1:
                return self.Punch.x - 20, self.Punch.y - 80, self.Punch.x + 25, self.Punch.y - 10
            else:
                return self.Punch.x - 25, self.Punch.y - 80, self.Punch.x + 20, self.Punch.y - 10
        else:
            if self.Punch.face_dir == 1:
                return self.Punch.x - 20, self.Punch.y - 110, self.Punch.x + 20, self.Punch.y - 20
            else:
                return self.Punch.x - 50, self.Punch.y - 110, self.Punch.x + 40, self.Punch.y - 40

    def get_weapon_bb(self):
        if self.atk and self.Punch.frame == 2:
            if self.Punch.face_dir == 1:
                return self.Punch.x - 20, self.Punch.y - 110, self.Punch.x + 20, self.Punch.y - 20
            else:
                return self.Punch.x - 50, self.Punch.y - 110, self.Punch.x + 40, self.Punch.y - 40
        return None

    def enter(self, e):
        if e and up_down(e) and self.Punch.on_ground:
            self.Punch.velocity_y = self.Punch.jump_speed
            self.Punch.on_ground = False
            self.atk = False
        elif e and space_down(e) and not self.Punch.on_ground:
            self.atk = True

    def exit(self, e):
        self.Punch.velocity_x = 0
        self.atk = False

    def do(self):
        if self.Punch.velocity_y > 100:
            self.Punch.frame = 0
        elif self.atk:
            self.Punch.frame = 2
        else:
            self.Punch.frame = 1

    def draw(self):
        draw_rectangle(*self.get_bb())
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
    image_slide = None

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
        if Punch.image_slide == None:
            Punch.image_slide = load_image('Slide04.png')

        self.player_id = player_id
        self.x, self.y = start_x, start_y
        self.frame = 0
        self.face_dir = 1 if player_id == 1 else -1
        self.prev_x = start_x
        self.prev_y = start_y

        self.velocity_y = 0
        self.velocity_x = 0
        self.gravity = 980
        self.jump_speed = 450
        self.on_ground = False

        self.left_pressed = False
        self.right_pressed = False

        self.knockback_velocity = 0
        self.knockback_friction = 1500.0

        self.hp = 6
        self.max_hp = 6

        self.hit_cooldown = 0.5  # 0.5초 쿨타임
        self.last_hit_time = 0.0  # 마지막으로 맞은 시간

        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.JUMP = Jump(self)

        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {left_down: self.RUN, right_down: self.RUN, space_down: self.IDLE, up_down: self.JUMP},
                self.RUN: {left_up: self.IDLE, right_up: self.IDLE, right_down: self.IDLE, left_down: self.IDLE,
                           space_down: self.RUN, up_down: self.JUMP},
                self.JUMP: {right_down: self.JUMP, left_down: self.JUMP, left_up: self.JUMP, right_up: self.JUMP,space_down : self.JUMP}
            }
        )

    def update(self):
        self.prev_x = self.x
        self.prev_y = self.y

        self.on_ground = False

        self.velocity_y -= self.gravity * game_framework.frame_time

        if isinstance(self.state_machine.cur_state, Jump) and self.state_machine.cur_state.atk:
            if self.velocity_y > self.state_machine.cur_state.FAST_FALL_SPEED:
                self.velocity_y = self.state_machine.cur_state.FAST_FALL_SPEED

        self.y += self.velocity_y * game_framework.frame_time

        # 상태별 이동 처리
        if isinstance(self.state_machine.cur_state, Jump):
            if self.state_machine.cur_state.atk:
                # 점프 공격 시 전방 대시
                self.velocity_x = self.state_machine.cur_state.DASH_SPEED * self.face_dir
            elif self.left_pressed:
                self.velocity_x = -RUN_SPEED_PPS
                self.face_dir = -1
            elif self.right_pressed:
                self.velocity_x = RUN_SPEED_PPS
                self.face_dir = 1
            else:
                self.velocity_x = 0
        elif isinstance(self.state_machine.cur_state, Run):
            if not self.state_machine.cur_state.atk:
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
            else:
                self.velocity_x = 0
        else:  # Idle
            self.velocity_x = 0

        if not isinstance(self.state_machine.cur_state, Run) or not self.state_machine.cur_state.atk:
            self.x += self.velocity_x * game_framework.frame_time

        # 넉백 처리
        if self.knockback_velocity != 0:
            self.x += self.knockback_velocity * game_framework.frame_time
            # 넉백 감속
            if self.knockback_velocity > 0:
                self.knockback_velocity -= self.knockback_friction * game_framework.frame_time
                if self.knockback_velocity < 0:
                    self.knockback_velocity = 0
            else:
                self.knockback_velocity += self.knockback_friction * game_framework.frame_time
                if self.knockback_velocity > 0:
                    self.knockback_velocity = 0

        punch_left, _, punch_right, _ = self.get_bb()
        left_offset = self.x - punch_left
        right_offset = punch_right - self.x

        if punch_left < 0:
            self.x = left_offset
            self.velocity_x = 0
        elif punch_right > 1600:
            self.x = 1600 - right_offset
            self.velocity_x = 0

        self.state_machine.update()

    def handle_event(self, event):
        if self.player_id == 1:
            if event.type == SDL_KEYDOWN:
                if event.key == SDLK_a:
                    self.left_pressed = True
                elif event.key == SDLK_d:
                    self.right_pressed = True
                elif event.key not in (SDLK_SPACE, SDLK_w):
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
                elif event.key not in (SDLK_RETURN, SDLK_UP):
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
        if group == 'weapon:bullet':
            # bullet:player에서 넉백 처리를 하므로 여기서는 아무것도 하지 않음
            pass

        if group == 'weapon:player':
            if self.player_id == other.player_id:
                return

            # play_mode의 round_state 확인
            import play_mode
            if hasattr(play_mode, 'round_state') and play_mode.round_state != 'playing':
                return

            weapon_bb = other.get_weapon_bb()
            if weapon_bb:
                weapon_left, weapon_bottom, weapon_right, weapon_top = weapon_bb
                my_left, my_bottom, my_right, my_top = self.get_bb()

                if weapon_left < my_right and weapon_right > my_left and \
                   weapon_bottom < my_top and weapon_top > my_bottom:
                    # 쿨타임 체크
                    current_time = game_framework.get_time()
                    if current_time - self.last_hit_time >= self.hit_cooldown:
                        if self.hp > 0:
                            self.hp -= 1
                            self.last_hit_time = current_time
                            print(f'Player {other.player_id} hit Player {self.player_id}! HP: {self.hp}')

        if group == 'player:tile':
            punch_left, punch_bottom, punch_right, punch_top = self.get_bb()
            tile_left, tile_bottom, tile_right, tile_top = other.get_bb()

            # 현재 바운딩 박스 기준으로 이전 위치의 바운딩 박스 계산
            current_left_offset = self.x - punch_left
            current_right_offset = punch_right - self.x
            current_bottom_offset = self.y - punch_bottom

            prev_left = self.prev_x - current_left_offset
            prev_right = self.prev_x + current_right_offset
            prev_bottom = self.prev_y - current_bottom_offset
            prev_top = self.prev_y

            overlap_x = min(punch_right - tile_left, tile_right - punch_left)
            overlap_y = min(punch_top - tile_bottom, tile_top - punch_bottom)

            was_above = prev_bottom >= tile_top
            was_below = prev_top <= tile_bottom
            was_left = prev_right <= tile_left
            was_right = prev_left >= tile_right

            if overlap_y < overlap_x:
                if was_above:
                    if isinstance(self.state_machine.cur_state, Jump):
                        self.y = tile_top + 100
                    else:
                        self.y = tile_top + current_bottom_offset

                    self.velocity_y = 0
                    self.on_ground = True
                    if isinstance(self.state_machine.cur_state, Jump):
                        self.state_machine.cur_state.exit(None)
                        if self.left_pressed or self.right_pressed:
                            self.state_machine.cur_state = self.RUN
                        else:
                            self.state_machine.cur_state = self.IDLE
                        self.state_machine.cur_state.enter(None)
                    return
                if was_below and self.velocity_y > 0:
                    self.y = tile_bottom
                    self.velocity_y = 0
                    return

            else:
                if was_left:
                    self.x = tile_left - current_right_offset
                    self.velocity_x = 0
                    return

                if was_right:
                    self.x = tile_right + current_left_offset
                    self.velocity_x = 0
                    return

    def get_bb(self):
        return self.state_machine.cur_state.get_bb()

    def get_weapon_bb(self):
        return self.state_machine.cur_state.get_weapon_bb()

    def draw(self):
        self.state_machine.draw()

from pico2d import load_image, draw_rectangle
from sdl2 import SDL_KEYDOWN, SDLK_LEFT, SDLK_RIGHT, SDL_KEYUP, SDLK_SPACE, SDLK_a, SDLK_d, SDLK_RETURN

import game_framework
from state_machine import StateMachine
import game_world

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
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 40.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


class Bullet:
    def __init__(self, x, y, direction):
        self.x, self.y = x , y-25
        self.direction = direction
        self.speed = 750

    def update(self):
        self.x += self.direction * self.speed * game_framework.frame_time
        # 화면 밖으로 나가면 제거
        if self.x < 0 or self.x > 1600:
            game_world.remove_object(self)

    def draw(self):
        Gun.bullet_image.draw(self.x, self.y,200,200)

class Idle:
    def __init__(self,Gun):
        self.gun = Gun
        self.atk = False
        self.atk_frame = 5

    def get_bb(self):
        if self.atk == False:
            return self.gun.x - 30, self.gun.y - 100, self.gun.x + 30, self.gun.y
        else:
            return self.gun.x - 35, self.gun.y - 100, self.gun.x + 35, self.gun.y
    def enter(self,e):
        self.gun.frame = 0
        if left_up(e):
            self.gun.face_dir = -1
        elif right_up(e):
            self.gun.face_dir = 1
        elif space_down(e):
            self.atk = True
            self.gun.shoot()
    def exit(self,e):
        self.atk = False
    def do(self):
        if self.atk == True:
            self.gun.frame = (self.gun.frame + 7 * ACTION_PER_TIME * game_framework.frame_time)
            if self.gun.frame >= self.atk_frame:  # ← 이제 8 이상이 될 수 있음
                self.atk = False
                self.gun.frame = 0
    def draw(self):
        draw_rectangle(*self.get_bb())
        if self.atk == False:
            if self.gun.face_dir == 1:
                self.gun.image_idle.clip_draw(int(self.gun.frame) * 96, 0, 96, 84, self.gun.x, self.gun.y, 200,
                                                  200)
            else:
                self.gun.image_idle.clip_composite_draw(int(self.gun.frame) * 96, 0, 96, 84,0,'h', self.gun.x, self.gun.y, 200,
                                                  200)
        else:
            if self.gun.face_dir == 1:
                self.gun.image_ia.clip_draw(int(self.gun.frame) * 96, 0, 96, 84, self.gun.x, self.gun.y, 200,
                                                200)
            else:
                self.gun.image_ia.clip_composite_draw(int(self.gun.frame) * 96, 0, 96, 84,0,'h', self.gun.x, self.gun.y, 200,
                                                  200)

class Jump:
    def __init__(self,Gun):
        self.gun = Gun
    def enter(self,e):
        pass
    def exit(self,e):
        pass
    def do(self):
        pass
    def draw(self):
        pass

class Run:
    def __init__(self,Gun):
        self.gun = Gun
        self.atk = False
        self.atk_frame = 8

    def get_bb(self):
        if self.gun.face_dir == 1:
            return self.gun.x - 40, self.gun.y - 100, self.gun.x + 50, self.gun.y
        else:
            return self.gun.x - 50, self.gun.y - 100, self.gun.x + 40, self.gun.y
    def enter(self,e):
        if left_down(e):
            self.gun.face_dir = -1
        elif right_down(e):
            self.gun.face_dir = 1
        elif space_down(e):
            self.atk = True
            self.gun.frame = 0
            self.gun.shoot()
    def exit(self,e):
        self.atk = False
    def do(self):
        if self.atk == True:
            self.gun.frame = (self.gun.frame + 7 * ACTION_PER_TIME * game_framework.frame_time)
            if self.gun.frame >= self.atk_frame:  # ← 이제 8 이상이 될 수 있음
                self.atk = False
                self.gun.frame = 0
        else:
            self.gun.frame = (self.gun.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

        self.gun.x += self.gun.face_dir * RUN_SPEED_PPS * game_framework.frame_time
    def draw(self):
        draw_rectangle(*self.get_bb())
        if self.atk == False:
            if self.gun.face_dir == 1:
                self.gun.image_run.clip_draw(int(self.gun.frame) * 96, 0, 96, 84, self.gun.x, self.gun.y, 200,
                                                  200)
            else:
                self.gun.image_run.clip_composite_draw(int(self.gun.frame) * 96, 0, 96, 84,0,'h', self.gun.x, self.gun.y, 200,
                                                  200)
        else:
            if self.gun.face_dir == 1:
                self.gun.image_ra.clip_draw(int(self.gun.frame) * 96, 0, 96, 84, self.gun.x, self.gun.y, 200,
                                                200)
            else:
                self.gun.image_ra.clip_composite_draw(int(self.gun.frame) * 96, 0, 96, 84,0,'h', self.gun.x, self.gun.y, 200,
                                                  200)

class Gun:
    image_idle = None
    image_run = None
    image_ia = None
    image_ra = None
    bullet_image = None
    def __init__(self, player_id = 1, start_x = 100, start_y = 180):
        if Gun.image_idle == None:
            Gun.image_idle = load_image('GunAim.png')
        if Gun.image_run == None:
            Gun.image_run = load_image('GunRun.png')
        if Gun.image_ia == None:
            Gun.image_ia = load_image('GunFire.png')
        if Gun.image_ra == None:
            Gun.image_ra = load_image('GunRunFire01-sheet.png')
        if Gun.bullet_image == None:
            Gun.bullet_image = load_image('Bullet02.png')
        self.player_id = player_id
        self.x, self.y = start_x, start_y
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
        pass

    def draw(self):
        self.state_machine.draw()

    def shoot(self):
        bullet = Bullet(self.x, self.y, self.face_dir)
        game_world.add_object(bullet,1)
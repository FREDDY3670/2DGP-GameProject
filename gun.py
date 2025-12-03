from pico2d import load_image, draw_rectangle
from sdl2 import SDL_KEYDOWN, SDLK_LEFT, SDLK_RIGHT, SDL_KEYUP, SDLK_SPACE, SDLK_a, SDLK_d, SDLK_RETURN, SDLK_w, SDLK_UP

import game_framework
from state_machine import StateMachine
import game_world

def up_down(e):
    return (e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and
            (e[1].key == SDLK_w or e[1].key == SDLK_UP))

def up_up(e):
    return (e[0] == 'INPUT' and e[1].type == SDL_KEYUP and
            (e[1].key == SDLK_w or e[1].key == SDLK_UP))

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
    def __init__(self, x, y, direction, shooter_id):
        self.x, self.y = x , y-25
        self.direction = direction
        self.speed = 750
        self.shooter_id = shooter_id

    def update(self):
        self.x += self.direction * self.speed * game_framework.frame_time
        # 화면 밖으로 나가면 제거
        if self.x < 0 or self.x > 1600:
            game_world.remove_object(self)

    def draw(self):
        Gun.bullet_image.draw(self.x, self.y,200,200)

    def get_bb(self):
        return self.x - 20, self.y - 20, self.x + 20, self.y + 20

    def handle_collision(self, group, other):
        if group == 'bullet:player':
            if self.shooter_id == other.player_id:
                return

            # 상대방이 무기로 막고 있는지 확인
            weapon_bb = other.get_weapon_bb()
            knockback_force = 300

            if weapon_bb:
                weapon_left, weapon_bottom, weapon_right, weapon_top = weapon_bb
                bullet_left, bullet_bottom, bullet_right, bullet_top = self.get_bb()

                # 무기와 총알이 충돌하면 절반만 밀림
                if weapon_left < bullet_right and weapon_right > bullet_left and \
                   weapon_bottom < bullet_top and weapon_top > bullet_bottom:
                    # 무기로 막았을 때는 절반의 넉백
                    other.knockback_velocity = self.direction * knockback_force * 0.5
                    print(f'Player {other.player_id} deflected bullet!')
                    game_world.remove_object(self)
                    return

            # 무기로 막지 못했으면 전체 넉백 적용
            other.knockback_velocity = self.direction * knockback_force

            print(f'Bullet from Player {self.shooter_id} hit Player {other.player_id}!')
            game_world.remove_object(self)

class Idle:
    def __init__(self,Gun):
        self.gun = Gun
        self.atk = False
        self.atk_frame = 5

    def get_weapon_bb(self):
        return None

    def get_bb(self):
        if self.atk == False:
            return self.gun.x - 30, self.gun.y - 100, self.gun.x + 30, self.gun.y
        else:
            return self.gun.x - 35, self.gun.y - 100, self.gun.x + 35, self.gun.y

    def enter(self, e):
        self.gun.frame = 0
        if e is None:
            return
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
    def __init__(self, Gun):
        self.gun = Gun

    def get_weapon_bb(self):
        return None

    def get_bb(self):
        if self.gun.face_dir == 1:
            return self.gun.x - 30, self.gun.y - 100, self.gun.x + 30, self.gun.y
        else:
            return self.gun.x - 30, self.gun.y - 100, self.gun.x + 30, self.gun.y

    def enter(self, e):
        if e and up_down(e) and self.gun.on_ground:
            self.gun.velocity_y = self.gun.jump_speed
            self.gun.on_ground = False

    def exit(self, e):
        self.gun.velocity_x = 0

    def do(self):
        self.gun.frame = (self.gun.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 14

    def draw(self):
        draw_rectangle(*self.get_bb())
        if self.gun.face_dir == 1:
            self.gun.image_jump.clip_draw(int(self.gun.frame) * 96, 0, 96, 84, self.gun.x, self.gun.y, 200, 200)
        else:
            self.gun.image_jump.clip_composite_draw(int(self.gun.frame) * 96, 0, 96, 84, 0, 'h', self.gun.x, self.gun.y, 200, 200)

class Run:
    def __init__(self,Gun):
        self.gun = Gun
        self.atk = False
        self.atk_frame = 8

    def get_weapon_bb(self):
        return None

    def get_bb(self):
        if self.gun.face_dir == 1:
            return self.gun.x - 40, self.gun.y - 100, self.gun.x + 50, self.gun.y
        else:
            return self.gun.x - 50, self.gun.y - 100, self.gun.x + 40, self.gun.y

    def enter(self, e):
        if e is None:
            return
        if right_down(e):
            self.gun.face_dir = 1
        elif left_down(e):
            self.gun.face_dir = -1
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
        else:
            self.gun.frame = (self.gun.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

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
    image_jump = None

    def __init__(self, player_id=1, start_x=100, start_y=180):
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
        if Gun.image_jump == None:
            Gun.image_jump = load_image('FrontFlip01-sheet.png')

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

        # 맵 경계 제한 (0 ~ 1600)
        gun_left, _, gun_right, _ = self.get_bb()
        left_offset = self.x - gun_left
        right_offset = gun_right - self.x

        if gun_left < 0:
            self.x = left_offset
            self.velocity_x = 0
        elif gun_right > 1600:
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
                elif event.key not in (SDLK_UP, SDLK_RETURN):
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

    def get_bb(self):
        return self.state_machine.cur_state.get_bb()

    def get_weapon_bb(self):
        return self.state_machine.cur_state.get_weapon_bb()

    def handle_collision(self, group, other):
        if group == 'weapon:player':
            if self.player_id == other.player_id:
                return

            weapon_bb = other.get_weapon_bb()
            if weapon_bb:
                weapon_left, weapon_bottom, weapon_right, weapon_top = weapon_bb
                my_left, my_bottom, my_right, my_top = self.get_bb()

                if weapon_left < my_right and weapon_right > my_left and \
                   weapon_bottom < my_top and weapon_top > my_bottom:
                    print(f'Player {other.player_id} weapon hit Player {self.player_id}!')

        if group == 'player:tile':
            gun_left, gun_bottom, gun_right, gun_top = self.get_bb()
            tile_left, tile_bottom, tile_right, tile_top = other.get_bb()

            current_left_offset = self.x - gun_left
            current_right_offset = gun_right - self.x
            current_bottom_offset = self.y - gun_bottom

            prev_left = self.prev_x - current_left_offset
            prev_right = self.prev_x + current_right_offset
            prev_bottom = self.prev_y - current_bottom_offset
            prev_top = self.prev_y

            overlap_x = min(gun_right - tile_left, tile_right - gun_left)
            overlap_y = min(gun_top - tile_bottom, tile_top - gun_bottom)

            was_above = prev_bottom >= tile_top
            was_below = prev_top <= tile_bottom
            was_left = prev_right <= tile_left
            was_right = prev_left >= tile_right

            if overlap_y < overlap_x:
                if was_above:
                    self.y = tile_top + 100  # Jump 클래스의 바운딩 박스 높이에 맞춤
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

    def draw(self):
        self.state_machine.draw()

    def shoot(self):
        bullet = Bullet(self.x, self.y, self.face_dir, self.player_id)
        game_world.add_object(bullet,1)
        game_world.add_collision_pair('bullet:player', bullet, None)
        game_world.add_collision_pair('weapon:bullet', None, bullet)
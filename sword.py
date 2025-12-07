from pico2d import load_image, draw_rectangle, load_wav
from sdl2 import SDL_KEYDOWN, SDLK_LEFT, SDLK_RIGHT, SDL_KEYUP, SDLK_SPACE, SDLK_d, SDLK_a, SDLK_RETURN, SDLK_w, \
    SDLK_UP, SDLK_s, SDLK_DOWN

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
            (e[1].key == SDLK_w or e[1].key == SDLK_UP))

def up_up(e):
    return (e[0] == 'INPUT' and e[1].type == SDL_KEYUP and
            (e[1].key == SDLK_w or e[1].key == SDLK_UP))

def down_down(e):
    return (e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and
            (e[1].key == SDLK_s or e[1].key == SDLK_DOWN))

def down_up(e):
    return (e[0] == 'INPUT' and e[1].type == SDL_KEYUP and
            (e[1].key == SDLK_s or e[1].key == SDLK_DOWN))

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

    def get_bb(self):
        if self.atk == False:
            return self.Sword.x - 30, self.Sword.y - 100, self.Sword.x + 30, self.Sword.y
        else:
            return self.Sword.x - 40, self.Sword.y - 100, self.Sword.x + 40, self.Sword.y

    def get_weapon_bb(self):
        if not self.atk:
            return None

        frame = int(self.Sword.frame)

        # 달리기 공격: 수평 베기
        if self.Sword.face_dir == 1:
            if frame <= 2:
                return self.Sword.x + 10, self.Sword.y - 60, self.Sword.x + 50, self.Sword.y - 10
            elif frame <= 4:
                return self.Sword.x + 30, self.Sword.y - 65, self.Sword.x + 90, self.Sword.y - 15
            elif frame <= 6:
                return self.Sword.x + 40, self.Sword.y - 60, self.Sword.x + 100, self.Sword.y - 20
            else:
                return self.Sword.x + 20, self.Sword.y - 65, self.Sword.x + 70, self.Sword.y - 15
        else:
            if frame <= 2:
                return self.Sword.x - 50, self.Sword.y - 60, self.Sword.x - 10, self.Sword.y - 10
            elif frame <= 4:
                return self.Sword.x - 90, self.Sword.y - 65, self.Sword.x - 30, self.Sword.y - 15
            elif frame <= 6:
                return self.Sword.x - 100, self.Sword.y - 60, self.Sword.x - 40, self.Sword.y - 20
            else:
                return self.Sword.x - 70, self.Sword.y - 65, self.Sword.x - 20, self.Sword.y - 15

        return None

    def enter(self, e):
        if e is None:
            return
        if right_down(e):
            self.Sword.face_dir = 1
        elif left_down(e):
            self.Sword.face_dir = -1
        elif space_down(e):
            self.atk = True
            self.Sword.frame = 0
            Sword.sword_sound.play()  # 공격 시 사운드 재생

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

    def draw(self):
        draw_rectangle(*self.get_bb())
        if self.atk:
            draw_rectangle(*self.get_weapon_bb())
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
        if e and space_down(e) and not self.atk:
            self.atk = True
            self.atk_count += 1
            if self.atk_count > 3:
                self.atk_count = 1
            self.combo_timer = 0
            self.Sword.frame = 0
            Sword.sword_sound.play()  # 공격 시 사운드 재생
    def get_bb(self):
        if self.atk == False:
            return self.Sword.x - 30, self.Sword.y - 100, self.Sword.x + 30, self.Sword.y
        else:
            if self.Sword.face_dir == 1:
                if self.row == 0:
                    return self.Sword.x - 30, self.Sword.y - 100, self.Sword.x + 50, self.Sword.y
                elif self.row == 1:
                    return self.Sword.x - 15, self.Sword.y - 100, self.Sword.x + 55, self.Sword.y
                elif self.row == 2:
                    return self.Sword.x - 30, self.Sword.y - 100, self.Sword.x + 40, self.Sword.y
            else:
                if self.row == 0:
                    return self.Sword.x - 50, self.Sword.y - 100, self.Sword.x + 30, self.Sword.y
                elif self.row == 1:
                    return self.Sword.x - 55, self.Sword.y - 100, self.Sword.x + 15, self.Sword.y
                elif self.row == 2:
                    return self.Sword.x - 40, self.Sword.y - 100, self.Sword.x + 30, self.Sword.y

    def get_weapon_bb(self):
        if not self.atk:
            return None

        frame = int(self.Sword.frame)

        if self.row == 0:
            if self.Sword.face_dir == 1:
                if frame <= 1:
                    return self.Sword.x + 10, self.Sword.y - 60 , self.Sword.x + 30 , self.Sword.y
                elif frame == 2:
                    return self.Sword.x, self.Sword.y - 60, self.Sword.x + 25, self.Sword.y
                elif frame == 3:
                    return self.Sword.x, self.Sword.y - 60, self.Sword.x + 30, self.Sword.y
                else:
                    return self.Sword.x + 20, self.Sword.y - 70, self.Sword.x + 70, self.Sword.y - 40
            else:
                if frame <= 1:
                    return self.Sword.x - 30, self.Sword.y - 60 , self.Sword.x - 10 , self.Sword.y
                elif frame == 2:
                    return self.Sword.x - 25, self.Sword.y - 60, self.Sword.x, self.Sword.y
                elif frame == 3:
                    return self.Sword.x - 30, self.Sword.y - 60, self.Sword.x , self.Sword.y
                else:
                    return self.Sword.x - 70, self.Sword.y - 70, self.Sword.x - 20, self.Sword.y - 40

        elif self.row == 1:
            if self.Sword.face_dir == 1:
                return self.Sword.x + 10, self.Sword.y - 70, self.Sword.x + 100, self.Sword.y - 40
            else:
                return self.Sword.x - 100, self.Sword.y - 70, self.Sword.x - 10, self.Sword.y - 40

        elif self.row == 2:
            if self.Sword.face_dir == 1:
                if frame == 1 or frame == 2:
                    return self.Sword.x + 10, self.Sword.y - 40, self.Sword.x + 100, self.Sword.y - 10
                elif frame == 3:
                    return self.Sword.x - 30, self.Sword.y - 50, self.Sword.x + 90, self.Sword.y + 40
                else:
                    return self.Sword.x - 30, self.Sword.y - 50, self.Sword.x , self.Sword.y + 40
            else:
                if frame == 1 or frame == 2:
                    return self.Sword.x - 100, self.Sword.y - 40, self.Sword.x - 10, self.Sword.y - 10
                elif frame == 3:
                    return self.Sword.x - 90, self.Sword.y - 50, self.Sword.x + 30, self.Sword.y + 40
                else:
                    return self.Sword.x , self.Sword.y - 50, self.Sword.x + 30, self.Sword.y + 40

        return None

    def exit(self, e):
        pass

    def do(self):
        if self.atk:
            if self.atk_frame == 0:
                self.row = 3 - self.atk_count
                if self.row == 0:
                    self.atk_frame = 8
                elif self.row == 1 or self.row == 2:
                    self.atk_frame = 5
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
        draw_rectangle(*self.get_bb())
        if self.atk:
            draw_rectangle(*self.get_weapon_bb())
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

class Jump:
    def __init__(self,Sword):
        self.Sword = Sword

    def get_bb(self):
        frame = int(self.Sword.frame)
        if frame == 0 or frame == 1:
            return self.Sword.x - 30, self.Sword.y - 100, self.Sword.x + 30, self.Sword.y
        elif frame == 2 or frame == 3:
            return self.Sword.x - 40, self.Sword.y - 100, self.Sword.x + 30, self.Sword.y
        else:
            return self.Sword.x - 30, self.Sword.y - 100, self.Sword.x + 40, self.Sword.y

    def get_weapon_bb(self):
        frame = int(self.Sword.frame)
        if frame == 3:
            return self.Sword.x - 80, self.Sword.y - 100, self.Sword.x + 35, self.Sword.y + 70
        else:
            return None

    def enter(self, e):
        if e and up_down(e) and self.Sword.on_ground:
            self.Sword.velocity_y = self.Sword.jump_speed
            self.Sword.on_ground = False

    def exit(self,e):
        self.Sword.velocity_x = 0
    def do(self):
        self.Sword.frame = (self.Sword.frame + 6 * ACTION_PER_TIME * game_framework.frame_time) % 6

    def draw(self):
        draw_rectangle(*self.get_bb())
        weapon_bb = self.get_weapon_bb()
        if weapon_bb:
            draw_rectangle(*weapon_bb)
        if self.Sword.face_dir == 1:
            self.Sword.image_air.clip_draw(int(self.Sword.frame) * 96, 84, 96, 84, self.Sword.x, self.Sword.y, 200,
                                           200)
        else:
            self.Sword.image_air.clip_composite_draw(int(self.Sword.frame) * 96, 84, 96, 84, 0, 'h', self.Sword.x,
                                                     self.Sword.y, 200, 200)

class Sword:
    image_idle = None
    image_run = None
    image_ia = None
    image_ra = None
    image_air = None
    sword_sound = None

    def __init__(self, player_id = 1, start_x = 100, start_y = 180):
        if Sword.image_idle == None:
            Sword.image_idle = load_image('SwordIdle01-sheet.png')
        if Sword.image_run == None:
            Sword.image_run = load_image('SwordRun01_right.png')
        if Sword.image_ia == None:
            Sword.image_ia = load_image('swordcombo.png')
        if Sword.image_ra == None:
            Sword.image_ra = load_image('SwordRunSlash01_right.png')
        if Sword.image_air == None:
            Sword.image_air = load_image('Air_Slash.png')
        if Sword.sword_sound == None:
            Sword.sword_sound = load_wav('sword.wav')
            Sword.sword_sound.set_volume(32)

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

        # 능력 보너스
        self.speed_bonus = 1.0
        self.attack_bonus = 1.0

        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.JUMP = Jump(self)

        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {left_down : self.RUN, right_down : self.RUN,space_down : self.IDLE, up_down : self.JUMP},
                self.RUN: {space_down : self.RUN, up_down : self.JUMP},
                self.JUMP: {right_down : self.JUMP, left_down : self.JUMP, left_up : self.JUMP, right_up : self.JUMP}
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
                self.velocity_x = -RUN_SPEED_PPS * self.speed_bonus
                self.face_dir = -1
            elif self.right_pressed:
                self.velocity_x = RUN_SPEED_PPS * self.speed_bonus
                self.face_dir = 1
            else:
                self.velocity_x = 0
        elif isinstance(self.state_machine.cur_state, Run):
            if self.left_pressed and self.right_pressed:
                self.velocity_x = 0
            elif self.left_pressed:
                self.velocity_x = -RUN_SPEED_PPS * self.speed_bonus
                self.face_dir = -1
            elif self.right_pressed:
                self.velocity_x = RUN_SPEED_PPS * self.speed_bonus
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

        sword_left, _, sword_right, _ = self.get_bb()
        left_offset = self.x - sword_left
        right_offset = sword_right - self.x

        if sword_left < 0:
            self.x = left_offset
            self.velocity_x = 0
        elif sword_right > 1600:
            self.x = 1600 - right_offset
            self.velocity_x = 0
        self.state_machine.update()

    def get_bb(self):
        return self.state_machine.cur_state.get_bb()

    def get_weapon_bb(self):
        return self.state_machine.cur_state.get_weapon_bb()

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

    def draw(self):
        self.state_machine.draw()

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

                    # 상성 체크: 상대가 점프공격 중이고 내가 슬라이딩 중이면 회피
                    from punch import Punch as PunchClass
                    from sword import Jump as SwordJump

                    # 상대가 Sword의 점프공격 중인지 체크
                    other_is_jump_attack = False
                    if hasattr(other, 'state_machine'):
                        if isinstance(other.state_machine.cur_state, SwordJump):
                            if other.get_weapon_bb() is not None:  # 점프공격 중
                                other_is_jump_attack = True

                    # 내가 슬라이딩 중인지 체크 (Punch의 Run상태에서 atk=True)
                    my_is_sliding = False
                    if isinstance(self.state_machine.cur_state, Run):
                        if self.state_machine.cur_state.atk:
                            my_is_sliding = True

                    # 상대 점프공격 vs 내 슬라이딩 = 회피 성공
                    if other_is_jump_attack and my_is_sliding:
                        print(f'Player {self.player_id} dodged jump attack with sliding!')
                        return

                    # 쿨타임 체크
                    current_time = game_framework.get_time()
                    if current_time - self.last_hit_time >= self.hit_cooldown:
                        if self.hp > 0:
                            self.hp -= 1
                            self.last_hit_time = current_time
                            print(f'Player {other.player_id} hit Player {self.player_id}! HP: {self.hp}')

        if group == 'player:tile':
            sword_left, sword_bottom, sword_right, sword_top = self.state_machine.cur_state.get_bb()
            tile_left, tile_bottom, tile_right, tile_top = other.get_bb()

            prev_left = self.prev_x - 30
            prev_right = self.prev_x + 30
            prev_bottom = self.prev_y - 100
            prev_top = self.prev_y

            overlap_x = min(sword_right - tile_left, tile_right - sword_left)
            overlap_y = min(sword_top - tile_bottom, tile_top - sword_bottom)

            was_above = prev_bottom >= tile_top
            was_below = prev_top <= tile_bottom
            was_left = prev_right <= tile_left
            was_right = prev_left >= tile_right

            if overlap_y < overlap_x:
                if was_above:
                    self.y = tile_top + 100
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
                    self.x = tile_left - 30
                    self.velocity_x = 0
                    return

                if was_right:
                    self.x = tile_right + 30
                    self.velocity_x = 0
                    return

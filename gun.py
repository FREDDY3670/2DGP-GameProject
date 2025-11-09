from pico2d import load_image

from state_machine import StateMachine

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
    def enter(self,e):
        pass
    def exit(self,e):
        pass
    def do(self):
        pass
    def draw(self):
        self.gun.image_idle.clip_draw(int(self.gun.frame) * 96, 0, 96, 84, self.gun.x, self.gun.y, 200,
                                              200)

class Run:
    def __init__(self,Gun):
        pass
    def enter(self,e):
        pass
    def exit(self,e):
        pass
    def do(self):
        pass
    def draw(self):
        pass

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
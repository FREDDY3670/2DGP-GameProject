from pico2d import load_image

class Idle:
    pass

class Run:
    pass

class Gun:
    def __init__(self):
        image_idle = None
        image_run = None
        image_ia = None
        image_ra = None
        if Gun.image_idle == None:
            Gun.image_idle = load_image('GunAim.png')
        if Gun.image_run == None:
            Gun.image_run = load_image('GunRun.png')
        if Gun.image_ia == None:
            Gun.image_ia = load_image('GunFire.png')
        if Gun.image_ra == None:
            Gun.image_ra = load_image('GunRunFire01-sheet.png')
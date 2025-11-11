from pico2d import *

import game_framework
import play_mode

player1_weapon = 0
player2_weapon = 0

def init():
    image_p = None
    image_s = None
    image_b = None
    image_g = None
    global image_p, image_s, image_b, image_g
    if image_p == None:
        image_p = load_image('Punch0101-sheet.png')
    if image_s == None:
        image_s = load_image('swordcombo.png')
    if image_b == None:
        image_b = load_image('BowFire01-sheet.png')
    if image_g == None:
        image_g = load_image('GunFire.png')
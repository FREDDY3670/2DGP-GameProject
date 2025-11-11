from pico2d import *

import game_framework
import play_mode

player1_weapon = 0
player2_weapon = 0
frame_1 = 0
frame_2 = 0
frame_3 = 0
frame_4 = 0

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
image_p = None
image_s = None
image_b = None
image_g = None
bg = None

def init():
    global image_p, image_s, image_b, image_g,bg
    if image_p == None:
        image_p = load_image('Punch0101-sheet.png')
    if image_s == None:
        image_s = load_image('swordcombo.png')
    if image_b == None:
        image_b = load_image('BowFire01-sheet.png')
    if image_g == None:
        image_g = load_image('GunFire.png')
    if bg == None:
        bg = load_image('Gray-BG.png')

def update():
    global frame_1, frame_2, frame_3, frame_4
    frame_1 = (frame_1 + 6 * ACTION_PER_TIME * game_framework.frame_time) % 6
    frame_2 = (frame_2 + 6 * ACTION_PER_TIME * game_framework.frame_time) % 6
    frame_3 = (frame_3 + 5 * ACTION_PER_TIME * game_framework.frame_time) % 5
    frame_4 = (frame_4 + 5 * ACTION_PER_TIME * game_framework.frame_time) % 5

def finish():
    pass

def draw():
    clear_canvas()
    bg.draw(800,450)
    image_p.clip_draw(int(frame_1) * 96, 0, 96, 84, 200, 400, 150, 150)
    image_s.clip_draw(int(frame_2) * 96, 0, 96, 84, 400, 400, 150, 150)
    image_b.clip_draw(int(frame_3) * 96, 0, 96, 84, 600, 400, 150, 150)
    image_g.clip_draw(int(frame_4) * 96, 0, 96, 84, 800, 400, 150, 150)
    update_canvas()

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()

def pause():
    pass
def resume():
    pass
from pico2d import *

import game_framework
import play_mode

player1_weapon = None
player2_weapon = None
frame_1 = 0
frame_2 = 0
frame_3 = 0

TIME_PER_ACTION = 0.6
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
image_p = None
image_s = None
image_g = None
bg = None
select = 0

def init():
    global image_p, image_s, image_g, bg, player1_weapon, player2_weapon, select
    # 무기 선택 초기화
    player1_weapon = None
    player2_weapon = None
    select = 0

    if image_p == None:
        image_p = load_image('Punch0101-sheet.png')
    if image_s == None:
        image_s = load_image('swordcombo.png')
    if image_g == None:
        image_g = load_image('GunFire.png')
    if bg == None:
        bg = load_image('Gray-BG.png')

def update():
    global frame_1, frame_2, frame_3
    if player1_weapon != None and player2_weapon != None:
        game_framework.change_mode(play_mode)
        return
    frame_1 = (frame_1 + 6 * ACTION_PER_TIME * game_framework.frame_time) % 6
    frame_2 = (frame_2 + 6 * ACTION_PER_TIME * game_framework.frame_time) % 6
    frame_3 = (frame_3 + 5 * ACTION_PER_TIME * game_framework.frame_time) % 5

def finish():
    global image_p, image_s, image_g, bg
    image_p = None
    image_s = None
    image_g = None
    bg = None

def draw():
    clear_canvas()
    bg.draw(800,450)
    if select == 0:
        draw_rectangle(100,250,300,550,255,0,0)
    elif select == 1:
        draw_rectangle(650,250,850,550,255,0,0)
    elif select == 2:
        draw_rectangle(1200,250,1400,550,255,0,0)
    image_p.clip_draw(int(frame_1) * 96, 0, 96, 84, 200, 400, 150, 150)
    image_s.clip_draw(int(frame_2) * 96, 0, 96, 84, 750, 400, 150, 150)
    image_g.clip_draw(int(frame_3) * 96, 0, 96, 84, 1300, 400, 150, 150)
    update_canvas()

def handle_events():
    global select, player1_weapon, player2_weapon
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_1:
                select = 0
            elif event.key == SDLK_2:
                select = 1
            elif event.key == SDLK_3:
                select = 2
            elif event.key == SDLK_LEFT or event.key == SDLK_a:
                select = (select - 1) % 3
            elif event.key == SDLK_RIGHT or event.key == SDLK_d:
                select = (select + 1) % 3
            elif event.key == SDLK_RETURN or event.key == SDLK_SPACE:
                if player1_weapon == None:
                    if select == 0:
                        player1_weapon = 'Punch'
                    elif select == 1:
                        player1_weapon = 'Sword'
                    elif select == 2:
                        player1_weapon = 'Gun'
                    print(player1_weapon)
                    select = 0
                elif player2_weapon == None:
                    if select == 0:
                        player2_weapon = 'Punch'
                    elif select == 1:
                        player2_weapon = 'Sword'
                    elif select == 2:
                        player2_weapon = 'Gun'
                    print(player2_weapon)
                    select = 0



def pause():
    pass
def resume():
    pass
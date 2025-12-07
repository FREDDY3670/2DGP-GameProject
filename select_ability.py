from pico2d import *
import game_framework
import play_mode

bg = None
image_run = None
image_attack = None
frame_run = 0
frame_attack = 0

TIME_PER_ACTION = 0.6
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION

def init():
    global bg, image_run, image_attack
    if bg == None:
        bg = load_image('Gray-BG.png')
    if image_run == None:
        image_run = load_image('Run.png')
    if image_attack == None:
        image_attack = load_image('Punch0101-sheet.png')

def update():
    global frame_run, frame_attack
    frame_run = (frame_run + 8 * ACTION_PER_TIME * game_framework.frame_time) % 8
    frame_attack = (frame_attack + 6 * ACTION_PER_TIME * game_framework.frame_time) % 6

def finish():
    global bg, image_run, image_attack
    bg = None
    image_run = None
    image_attack = None

def draw():
    clear_canvas()
    bg.draw(800, 450)
    # 왼쪽에 달리는 이미지
    image_run.clip_draw(int(frame_run) * 96, 0, 96, 84, 500, 450, 200, 200)
    # 오른쪽에 공격하는 이미지
    image_attack.clip_draw(int(frame_attack) * 96, 0, 96, 84, 1100, 450, 200, 200)
    update_canvas()

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()

def pause():
    pass

def resume():
    pass

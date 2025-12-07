from pico2d import *
import game_framework
import play_mode

bg = None

def init():
    global bg
    if bg == None:
        bg = load_image('Gray-BG.png')

def update():
    pass

def finish():
    global bg
    bg = None

def draw():
    clear_canvas()
    bg.draw(800, 450)
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


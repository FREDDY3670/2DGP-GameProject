from pico2d import *
from map import Map
import game_framework
import game_world

select_map = 0

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
def init():
    pass

def update():
    pass

def draw():
    pass

def finish():
    pass

def pause():
    pass

def resume():
    pass
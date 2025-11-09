from pico2d import *
from map import Map
import game_framework
import game_world
from sword import Sword

select_map = 0

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            for layer in game_world.world:
                for o in layer:
                    if hasattr(o, 'handle_event'):
                        o.handle_event(event)
def init():
    map = Map()
    game_world.add_object(map, 0)

    sword = Sword()
    game_world.add_object(sword, 1)

def update():
    game_world.update()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def finish():
    game_world.clear()

def pause():
    pass

def resume():
    pass
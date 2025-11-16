from pico2d import *
from map import Map
import game_framework
import game_world
from gun import Gun
from punch import Punch
from sword import Sword
from tile import Tile
import select_weapon

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
    p1_w = select_weapon.player1_weapon
    p2_w = select_weapon.player2_weapon
    print(p1_w, p2_w)

    map = Map()
    game_world.add_object(map, 0)

    tile = Tile()
    game_world.add_object(tile, 0)
    player1 = None
    if p1_w == 'Gun':
        player1 = Gun(player_id=1, start_x=200, start_y=180)
    elif p1_w == 'Sword':
        player1 = Sword(player_id=1, start_x=200, start_y=180)
    # elif select_weapon.player1_weapon == 'Bow':
    #     player1 = Bow(player_id=1, start_x=200, start_y=180)
    elif select_weapon.player1_weapon == 'Punch':
        player1 = Punch(player_id=1, start_x=200, start_y=180)
    if player1:
        game_world.add_object(player1, 1)

    player2 = None
    if p2_w == 'Gun':
        player2 = Gun(player_id=2, start_x=1400, start_y=180)
    elif p2_w == 'Sword':
        player2 = Sword(player_id=2, start_x=1400, start_y=180)
    elif select_weapon.player2_weapon == 'Punch':
        player2 = Punch(player_id=2, start_x=1400, start_y=180)
    if player2:
        game_world.add_object(player2, 1)

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
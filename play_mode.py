import random
from pico2d import *
from map import Map
import game_framework
import game_world
from gun import Gun
from punch import Punch
from sword import Sword
from tile import Tile
import select_weapon
from draw_hp_bar import HPBar

select_map = random.randint(0, 4)
hp_bar = None
player1 = None
player2 = None

round_state = 'playing'
round_timer = 0.0
ROUND_DELAY = 2.0
current_round = 1
player1_loses = 0
player2_loses = 0

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
    global hp_bar, player1, player2, current_round, player1_loses, player2_loses, round_state

    current_round = 1
    player1_loses = 0
    player2_loses = 0
    round_state = 'playing'

    p1_w = select_weapon.player1_weapon
    p2_w = select_weapon.player2_weapon
    print(p1_w, p2_w)

    map = Map(select_map)
    game_world.add_object(map, 0)

    hp_bar = HPBar()

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

    game_world.add_collision_pair('player:tile', player1, None)
    game_world.add_collision_pair('player:tile', player2, None)

    for tile in map.tiles:
        game_world.add_collision_pair('player:tile', None, tile)

    game_world.add_collision_pair('weapon:player', player1, player2)

    game_world.add_collision_pair('bullet:player', None, player1)
    game_world.add_collision_pair('bullet:player', None, player2)

    game_world.add_collision_pair('weapon:bullet', player1, None)
    game_world.add_collision_pair('weapon:bullet', player2, None)

def reset_players():
    global round_state, current_round, player1_loses, player2_loses

    for layer in game_world.world:
        for obj in layer[:]:
            if hasattr(obj, 'shooter_id'):
                game_world.remove_object(obj)

    if player1:
        player1.hp = 6
        player1.x = 200
        player1.y = 180
        player1.velocity_x = 0
        player1.velocity_y = 0
        player1.knockback_velocity = 0
        player1.on_ground = False
        player1.left_pressed = False
        player1.right_pressed = False

    if player2:
        player2.hp = 6
        player2.x = 1400
        player2.y = 180
        player2.velocity_x = 0
        player2.velocity_y = 0
        player2.knockback_velocity = 0
        player2.on_ground = False
        player2.left_pressed = False
        player2.right_pressed = False

    current_round += 1
    if player1_loses >= 3 or player2_loses >= 3:
        if player1_loses < player2_loses:
            print(f"Player 1 WINS THE GAME!")
        else:
            print(f"Player 2 WINS THE GAME!")
        current_round = 1
        player1_loses = 0
        player2_loses = 0

    round_state = 'playing'

def update():
    global round_state, round_timer, player1_loses, player2_loses

    if round_state == 'playing':
        game_world.update()
        game_world.handle_collisions()

        # HP가 0 이하가 되면 즉시 라운드 종료
        if player1 and player1.hp <= 0:
            player1.hp = 0  # HP를 0으로 고정
            round_state = 'round_end'
            round_timer = 0.0
            player1_loses += 1  # player1이 죽으면 player1_loses 증가
            print(f"Player 2 wins round {current_round}! (P1 loses: {player1_loses}, P2 loses: {player2_loses})")

        elif player2 and player2.hp <= 0:
            player2.hp = 0  # HP를 0으로 고정
            round_state = 'round_end'
            round_timer = 0.0
            player2_loses += 1  # player2가 죽으면 player2_loses 증가
            print(f"Player 1 wins round {current_round}! (P1 loses: {player1_loses}, P2 loses: {player2_loses})")

    elif round_state == 'round_end':
        round_timer += game_framework.frame_time
        if round_timer >= ROUND_DELAY:
            reset_players()

def draw():
    clear_canvas()
    game_world.render()

    if hp_bar:
        p1_current_hp = player1.hp if player1 else 0
        p2_current_hp = player2.hp if player2 else 0
        hp_bar.draw(player1_loses, player2_loses, p1_current_hp, p2_current_hp)

    update_canvas()

def finish():
    game_world.clear()

def pause():
    pass

def resume():
    pass
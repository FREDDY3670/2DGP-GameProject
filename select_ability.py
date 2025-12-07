from pico2d import *
import game_framework
import play_mode

bg = None
image_run = None
image_attack = None
frame_run = 0
frame_attack = 0
select = 0  # 0: 왼쪽(달리기), 1: 오른쪽(공격)

# 선택한 능력 저장 (play_mode에서 사용)
selected_ability = None  # 'speed' or 'attack'
ability_player = None  # 어떤 플레이어가 능력을 받는지 (라운드 패배자)

TIME_PER_ACTION = 0.6
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION

def init():
    global bg, image_run, image_attack, select, selected_ability
    select = 0  # 기본 선택은 왼쪽
    selected_ability = None
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
    # 선택 박스 그리기
    if select == 0:
        draw_rectangle(400, 350, 600, 550)  # 왼쪽 선택
    else:
        draw_rectangle(1000, 350, 1200, 550)  # 오른쪽 선택
    # 왼쪽에 달리는 이미지
    image_run.clip_draw(int(frame_run) * 96, 0, 96, 84, 500, 450, 200, 200)
    # 오른쪽에 공격하는 이미지
    image_attack.clip_draw(int(frame_attack) * 96, 0, 96, 84, 1100, 450, 200, 200)
    update_canvas()

def handle_events():
    global select, selected_ability
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_LEFT or event.key == SDLK_a:
                select = 0
            elif event.key == SDLK_RIGHT or event.key == SDLK_d:
                select = 1
            elif event.key == SDLK_RETURN or event.key == SDLK_SPACE:
                # 선택 확정
                if select == 0:
                    selected_ability = 'speed'  # 이동속도 증가
                else:
                    selected_ability = 'attack'  # 공격속도 증가
                # play_mode에서 능력 선택 후 돌아온 것임을 알림
                play_mode.from_ability_select = True
                game_framework.change_mode(play_mode)

def pause():
    pass

def resume():
    pass

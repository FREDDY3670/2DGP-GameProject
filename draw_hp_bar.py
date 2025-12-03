from pico2d import load_image

class HPBar:
    image = None

    def __init__(self):
        if HPBar.image == None:
            HPBar.image = load_image('hp.png')

    def draw(self, player1_loses, player2_loses, p1_current_hp, p2_current_hp):
        # 라운드별 HP를 계산 (각 플레이어가 잃은 라운드 수를 기반으로)

        # Player1 라운드별 HP 계산
        player1_round_hp = [6, 6, 6]  # 기본값: 모든 라운드 만피

        # 잃은 라운드들은 0으로 설정 (가운데에서 가까운 순서대로)
        for i in range(min(player1_loses, 3)):
            player1_round_hp[i] = 0

        # 현재 진행중인 라운드의 HP 반영 (라운드가 진행 중일 때만)
        # play_mode.round_state를 확인해서 'playing' 상태일 때만 현재 HP 반영
        import play_mode
        if hasattr(play_mode, 'round_state') and play_mode.round_state == 'playing':
            if player1_loses < 3:
                current_round_index = player1_loses
                player1_round_hp[current_round_index] = max(0, p1_current_hp)

        # Player2 라운드별 HP 계산
        player2_round_hp = [6, 6, 6]  # 기본값: 모든 라운드 만피

        # 잃은 라운드들은 0으로 설정 (가운데에서 가까운 순서대로)
        for i in range(min(player2_loses, 3)):
            player2_round_hp[i] = 0

        # 현재 진행중인 라운드의 HP 반영 (라운드가 진행 중일 때만)
        if hasattr(play_mode, 'round_state') and play_mode.round_state == 'playing':
            if player2_loses < 3:
                current_round_index = player2_loses
                player2_round_hp[current_round_index] = max(0, p2_current_hp)

        p1_hp_0 = max(0, min(6, player1_round_hp[0]))
        p1_hp_1 = max(0, min(6, player1_round_hp[1]))
        p1_hp_2 = max(0, min(6, player1_round_hp[2]))

        p2_hp_0 = max(0, min(6, player2_round_hp[0]))
        p2_hp_1 = max(0, min(6, player2_round_hp[1]))
        p2_hp_2 = max(0, min(6, player2_round_hp[2]))

        p1_round1_frame = 12 - (p1_hp_0 * 2)
        p1_round2_frame = 12 - (p1_hp_1 * 2)
        p1_round3_frame = 12 - (p1_hp_2 * 2)

        p2_round1_frame = 12 - (p2_hp_0 * 2)
        p2_round2_frame = 12 - (p2_hp_1 * 2)
        p2_round3_frame = 12 - (p2_hp_2 * 2)

        # Player1 (왼쪽 화면) : 가운데에 가까운 것부터 소모 -> 오른쪽(가까운 쪽)부터 소모되므로
        # 화면에서는 왼쪽에서부터 그리지만 매핑은 round3(왼쪽), round2(중앙), round1(오른쪽)
        HPBar.image.clip_draw(p1_round3_frame * 16, 0, 16, 18, 50, 870, 32, 36)   # left (round3)
        HPBar.image.clip_draw(p1_round2_frame * 16, 0, 16, 18, 90, 870, 32, 36)   # center (round2)
        HPBar.image.clip_draw(p1_round1_frame * 16, 0, 16, 18, 130, 870, 32, 36)  # right (round1 = 가운데에 가까운)

        # Player2 (오른쪽 화면) : 가운데에 가까운 것부터 소모 -> 왼쪽(가까운 쪽)부터 소모되므로
        # 화면의 오른쪽 영역에서는 왼쪽에서부터 그리되 round1을 왼쪽에 매핑
        HPBar.image.clip_draw(p2_round1_frame * 16, 0, 16, 18, 1600 - 130, 870, 32, 36)  # left (round1 = 가운데에 가까운)
        HPBar.image.clip_draw(p2_round2_frame * 16, 0, 16, 18, 1600 - 90, 870, 32, 36)   # center (round2)
        HPBar.image.clip_draw(p2_round3_frame * 16, 0, 16, 18, 1600 - 50, 870, 32, 36)   # right (round3)

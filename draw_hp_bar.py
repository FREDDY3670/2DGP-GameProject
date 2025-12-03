from pico2d import load_image

class HPBar:
    image = None

    def __init__(self):
        if HPBar.image == None:
            HPBar.image = load_image('hp.png')

    def draw(self, player1_round_hp, player2_round_hp):
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

        HPBar.image.clip_draw(p1_round1_frame * 26, 0, 16, 18, 50, 870, 32, 36)
        HPBar.image.clip_draw(p1_round2_frame * 26, 0, 16, 18, 90, 870, 32, 36)
        HPBar.image.clip_draw(p1_round3_frame * 26, 0, 16, 18, 130, 870, 32, 36)

        HPBar.image.clip_draw(p2_round1_frame * 26, 0, 16, 18, 1600 - 50, 870, 32, 36)
        HPBar.image.clip_draw(p2_round2_frame * 26, 0, 16, 18, 1600 - 90, 870, 32, 36)
        HPBar.image.clip_draw(p2_round3_frame * 26, 0, 16, 18, 1600 - 130, 870, 32, 36)

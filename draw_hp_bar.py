from pico2d import load_image

class HPBar:
    image = None

    def __init__(self):
        if HPBar.image == None:
            HPBar.image = load_image('hp.png')

    def draw(self, player1_hp, player2_hp):
        HPBar.image.clip_draw(0, 0, 208, 18, 104, 900 - 9, 208, 18)
        HPBar.image.clip_draw(0, 0, 208, 18, 1600 - 104, 900 - 9, 208, 18)

from pico2d import load_image

class HPBar:
    image = None

    def __init__(self):
        if HPBar.image == None:
            HPBar.image = load_image('hp.png')

    def draw(self, player1_hp, player2_hp):
        HPBar.image.clip_draw(0, 0, 16, 18, 50, 870, 32, 36)
        HPBar.image.clip_draw(0, 0, 16, 18, 1600 - 50, 870, 32, 36)
        HPBar.image.clip_draw(0, 0, 16, 18, 90, 870, 32, 36)
        HPBar.image.clip_draw(0, 0, 16, 18, 1600 - 90, 870, 32, 36)
        HPBar.image.clip_draw(0, 0, 16, 18, 130, 870, 32, 36)
        HPBar.image.clip_draw(0, 0, 16, 18, 1600 - 130, 870, 32, 36)

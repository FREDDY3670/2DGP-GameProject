from pico2d import load_image

class Tile:
    def __init__(self, select_map=0):
        self.tile_image = load_image('tile_map1.png')

    def draw(self):
        for x in range(32):
            self.tile_image.draw(x*50,50,50,50)

    def update(self):
        pass
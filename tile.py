from pico2d import load_image, draw_rectangle


class Tile:
    tile_image = None
    def __init__(self, select_map=0):
        if Tile.tile_image == None:
            Tile.tile_image = load_image('tile_map1.png')
        self.x, self.y = 100,100

    def get_bb(self):
        return self.x - 25, self.y - 25, self.x + 25, self.y + 25

    def draw(self):
        draw_rectangle(*self.get_bb())
        self.tile_image.draw(self.x, self.y,50,50)

    def update(self):
        pass
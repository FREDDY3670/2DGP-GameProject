from pico2d import *
from tile import Tile
import random

class Map:
    MAP_TILES = {
        0: [
            *[(x, 50) for x in range(0, 1650, 50)],
            (350, 150), (450, 250),
            *[(x, 350) for x in range(500, 700, 50)],
            *[(x, 450) for x in range(700, 900, 50)],
            *[(x, 350) for x in range(900, 1100, 50)],
            (1150, 250), (1250, 150)
        ],

        1: [
            *[(x, 50) for x in range(0, 1650, 50)],
            *[(x, 150) for x in range(300, 500, 50)],
            *[(x, 250) for x in range(400, 600, 50)],
            *[(x, 150) for x in range(700, 900, 50)],
            *[(x, 250) for x in range(1000, 1200, 50)],
            *[(x, 150) for x in range(1100, 1300, 50)]
        ],

        2: [
            *[(x, 50) for x in range(0, 1650, 50)],
            *[(x, 250) for x in range(400, 600, 50)],
            *[(x, 150) for x in range(700, 900, 50)],
            *[(x, 250) for x in range(1000, 1200, 50)],
        ],

        3: [
            *[(x, 50) for x in range(0, 1650, 50)],
            *[(x, 150) for x in range(300, 450, 50)],
            *[(x, 250) for x in range(500, 650, 50)],
            *[(x, 350) for x in range(750, 850, 50)],
            *[(x, 250) for x in range(950, 1100, 50)],
            *[(x, 150) for x in range(1150, 1300, 50)]
        ],

        4: [
            *[(x, 50) for x in range(0, 1650, 50)],
            *[(x, 150) for x in range(350, 450, 50)],
            *[(x, 250) for x in range(550, 650, 50)],
            *[(x, 150) for x in range(750, 850, 50)],
            *[(x, 250) for x in range(950, 1050, 50)],
            *[(x, 150) for x in range(1150, 1250, 50)]
        ]
    }
    def __init__(self,select_map = 0):
        self.bg_image = load_image('Gray-BG.png')

        if select_map is None:
            self.map_type = 1#random.randint(0, 4)
        else:
            self.map_type = select_map

        self.tiles = []
        for x, y in Map.MAP_TILES[self.map_type]:
            self.tiles.append(Tile(x, y))
    def draw(self):
        self.bg_image.draw(800,450)
        for tile in self.tiles:
            tile.draw()

    def update(self):
        for tile in self.tiles:
            tile.update()

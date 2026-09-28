import pygame as pg
from settings import *
from math import floor

# establish Map class to import a map to display on the screen
class Map:
    def __init__(self, filename):
        self.data = []
        # opens a filename
        with open(filename, "rt") as f:
            for line in f:
                self.data.append(line.strip())
        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE
        print("map instantiated")

# establish Spritesheet class to import a sheet with all sprites in it
class Spritesheet:
    def __init__(self, filename):
        # loads an image (sprite) and converts it to a format pygame can use
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x, y, width, height))
        new_image = pg.transform.scale(image, (width, height))
        image = new_image
        return image
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
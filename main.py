# This file was created by Dylan Handy.
# Code inspired by game developer Chris Bradfield, who was inspired by Notch

import pygame as pg
from os import path
from sprites import *
from settings import *
from utils import *

"""
Why are we making game a class?
Why is it capitalized?
What is init?
What is pass?

Data Types: boolean, JSON, string, integer, float, etc.

Input (events): keyboard, mouse (e.g. right click), voice, power button, 
eye tracking, camera, gyroscoping (VR), electrostatic, location, volume, microphone, etc.

Process: cursor position, player position, score, enemy position, velocity, aim, etc.

Output: graphics (things that are drawn), sound, haptics, etc.
"""

class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        print("game initialized...")
        pg.display.set_caption(TITLE)
        self.running = True
        self.playing = True
        # establishes the Clock class as self.clock
        self.clock = pg.time.Clock()

    def load_data(self, map):
        self.game_dir = path.dirname(__file__)
        # image directory
        self.img_dir = path.join(self.game_dir, "images")
        # sound (audio) directory
        self.snd_dir = path.join(self.game_dir, "audio")
        self.map = Map(path.join(self.game_dir, map))

    def new(self):
        self.load_data("level1.txt")
        print(self.map.data)
        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()

        # goes through all the rows and their tiles of self.map
        for row, tiles in enumerate(self.map.data):
            # goes through all the columns and their tiles of self.map
            for col, tile in enumerate(tiles):
                # detects if the tile in the selected column and row is "1"
                if tile == "1":
                    # creates a wall wherever the tile is "1"
                    Wall(self, col, row)
                # detects if the tile in the selected column and row is "M"
                if tile == "M":
                    # creates a mob wherever the tile is "M"
                    Mob(self, col, row)
        # does the same thing as above but for "P" the player
        # separate from the previous loops because the player shouldn't
        # be able to be "underneath" any walls or mobs
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == "P":
                    Player(self, col, row)

    def run(self):
        self.playing = True
        # detects when self.playing is True and runs the code it it is
        while self.playing:
            # dt = delta t = change in time
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    # input
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    # process
    def update(self):
        # updates the sprites
        self.all_sprites.update()

    # output (drawing everything)
    def draw(self):
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        pg.display.flip()

if __name__ == "__main__":
    # g instantiates Game so that we can instantiate it???
    g = Game()

while g.running:
    g.new()
    g.run()
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
        # print("game initialized...")
        pg.display.set_caption(TITLE)
        self.running = True
        self.playing = True
        # establishes the Clock class as self.clock
        self.clock = pg.time.Clock()
        self.high_score = 0
        self.score = 0

    def load_data(self, map):
        self.game_dir = path.dirname(__file__)
        self.game_save_file = path.join(self.game_dir, "highscore.txt")
        # image directory
        self.img_dir = path.join(self.game_dir, "images")
        # sound handling
        # sound (audio) directory
        self.snd_dir = path.join(self.game_dir, "audio")
        self.pickup_snd = pg.mixer.Sound(path.join(self.snd_dir, "odd_coin.mp3"))
        self.map = Map(path.join(self.game_dir, map))
        try:
            # "x" creates a file but won't override an existing file
            with open(self.game_save_file, "x", encoding="utf-8") as file:
                file.write("hello world!")
            print("file created successfully!")
        # detects if the file already exists and distributes an error
        except FileExistsError:
            print("file already exists")
        
        with open(self.game_save_file, "r") as file:
            try:
                # sets high score as what the file reads
                # must be integer
                self.high_score = int(file.read())
            except:
                # if file can't be opened, sets high score to 0
                # self.high_score = 0
                print("high score not read")
            
    def new(self):
        self.load_data("level1.txt")
        # print(self.map.data)
        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        self.all_collectibles = pg.sprite.Group()

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
                if tile == "C":
                    # creates a collectible wherever the tile is "C"
                    Collectible(self, col, row)
        # does the same thing as above but for "P" the player
        # separate from the previous loops because the player shouldn't
        # be able to be "underneath" any walls or mobs
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == "P":
                    self.player = Player(self, col, row)
        
        pg.mixer.music.load(path.join(self.snd_dir, "dungeon_theme.mp3"))
        pg.mixer.music.play(loops=-1)

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
                # try and except allows to write specifc messages
                # for specifc errors (error handling)
                try:
                    # only change the high score if the new score has increased it
                    if self.score > self.high_score:
                        # with open allows for file handling, including
                        # "w" creates or writes a new file (can override old)
                        with open(path.join(self.game_dir, self.game_save_file), "w") as file:
                            # tells the file to write hello world inside
                            # must be string in order to be writable
                            file.write(str(self.score))
                # detects if there is a type error
                except TypeError:
                    # alerts the user using custom error message
                    print("incorrect type")
                
                if self.playing:
                    self.playing = False
                self.running = False

    def draw_text(self, text, size, color, x, y):
        # establishes the font as arial
        font_name = pg.font.match_font("arial")
        # Font is a class that takes the font name and the size
        font = pg.font.Font(font_name, size)
        # render method establishes the given text with a given color
        # and the already created font
        # True is for antialiasing
        text_surface = font.render(text, True, color)
        # gets the value of a rectangle of the text_surface
        text_rect = text_surface.get_rect()
        # establishes where the text will be drawn using x and y coordinates
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

    # process
    def update(self):
        # updates the sprites
        self.all_sprites.update()

    # output (drawing everything)
    def draw(self):
        # the order matters: the first things are on the bottom because
        # they are the first to be drawn - last things are drawn on top or last
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        # calls draw_text funciton to display frames per second as text on screen
        self.draw_text("Frames per second: " + str(floor(1/self.dt)), 24, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text(f"Coins: {self.player.collectibles}", 24, WHITE, WIDTH/2, HEIGHT/3)
        self.draw_text(f"Score: {self.score}", 24, WHITE, WIDTH/2, HEIGHT/2.5)
        self.draw_text(f"High Score: {self.high_score}", 24, WHITE, WIDTH/2, HEIGHT/10)
        pg.display.flip()

if __name__ == "__main__":
    # g instantiates Game so that we can instantiate it???
    g = Game()

while g.running:
    g.new()
    g.run()
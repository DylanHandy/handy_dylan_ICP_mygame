import pygame as pg

WIDTH = 1024
HEIGHT = 768
TITLE = "Best game ever!!!"
# establishes how many pixels are there for each tile
TILESIZE = 32
FPS = 30

# colors
BGCOLOR = (0, 100, 100)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# player settings
PLAYER_SPEED = 300
# TILESIZE - 5 so that if it grazes the edge, it doesn't take effect
PLAYER_HIT_RECT = pg.Rect(0,0, TILESIZE-5, TILESIZE-5)

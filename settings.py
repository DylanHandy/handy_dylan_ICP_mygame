import pygame as pg

WIDTH = 1024
HEIGHT = 768
ROWS, COLS = 32, 24
TITLE = "Best game ever!!!"
# establishes how many pixels are there for each tile
TILESIZE = WIDTH // COLS
FPS = 30

# colors
BGCOLOR = (255, 100, 100)
WHITE = (255, 255, 255)
GREEN = (46, 204, 113)
RED = (231, 76, 60)
BLACK = (0, 0, 0)
YELLOW = (241, 196, 15)
BLUE = (52, 152, 219)
BLACKISH = (30, 30, 30)
ORANGE = (230, 126, 34)
GRAY = (200, 200, 200)

# player settings
PLAYER_SPEED = 1
# TILESIZE - 5 so that if it grazes the edge, it doesn't take effect
PLAYER_HIT_RECT = pg.Rect(0,0, TILESIZE-5, TILESIZE-5)
PLAYER_JUMP = 50
PLAYER_FRIC = -0.1

# mob settings
MOB_HIT_RECT = pg.Rect(0,0, TILESIZE-5, TILESIZE-5)
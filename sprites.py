import pygame as pg
from settings import *
from pygame.sprite import Sprite
from utils import *

# os = operating system, which on this device, is Windows
from os import path

# creates a vector
vec = pg.math.Vector2

def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)

def collide_with_walls(sprite, group, dir):
    # checks if the direction is x for x collisions
    if dir == "x":
        # checks to see if we hav ecollide with hitrects
        # False means don't delete the object after colliding
        # collide_hit_rect is the argument that determines that the 
        # sprites actually collided
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            # checks to see if we are to the left of the wall
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                # reposition the player (sprite) to the left side of wall
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    # checks if the direction is y for y collisions
    if dir == "y":
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            # checks to see if we are above the wall
            if hits[0].rect.centery > sprite.hit_rect.centery:
                # reposition the player (sprite) to the top of wall
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

class Player(Sprite):
    # game is a parameter so that we can pass things between files
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        # pass self.groups in Sprite so that game can leverage groups
        Sprite.__init__(self, self.groups)
        self.game = game
        self.spritesheet = Spritesheet(path.join(self.game.img_dir, "sprite_sheet.png"))
        self.load_images()
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = self.spritesheet.get_image(0,0,TILESIZE,TILESIZE)
        # self.image.set_colorkey(BLACK)
        # colors the rectangle with the designated color WHITE
        # self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        # establishes velocity as a vector with no magnitude or direction
        self.vel = vec(0,0)
        # establishes position as a vector with x and y
        self.pos = vec(x*TILESIZE,y*TILESIZE)
        # self.vx, self.vy = 0,0
        # self.x = x*TILESIZE
        # self.y = y*TILESIZE
        self.last_update = 0
        self.current_frame = 0
        # print("player initialized...")
        # print(self.rect.x)
        # print(self.rect.y)
    # creating player controls by key presses
    def get_keys(self):
        # reset velocity to 0 again because init only runs once
        self.vel = vec(0,0)
        # self.vx, self.vy = 0,0
        self.dir = "none"
        # listen for events; detects if the key is pressed
        keys = pg.key.get_pressed()
        # change velocity based on which key is pressed
        # move to the left at the player speed if left arrow or a is pressed
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            # prints this so that we can detect whether the game registers the input or not
            # print("trying to go left...")
            self.dir = "left"
            # changes the velocity (x-axis) to be the player speed to the left (negative)
            self.vel.x = -PLAYER_SPEED
            # self.vx = -PLAYER_SPEED
        # move to the right at the player speed if right arrow or d is pressed
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            # prints this so that we can detect whether the game registers the input or not
            # print("trying to go right...")
            # changes the velocity (x-axis) to be the player speed to the right (positive)
            self.vel.x = PLAYER_SPEED
            # self.vx = PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            # prints this so that we can detect whether the game registers the input or not
            # print("trying to go down...")
            # changes the velocity (y-axis) to be the player speed down (positive)
            self.vel.y = PLAYER_SPEED
            # self.vy = PLAYER_SPEED
        # move to the right at the player speed if right arrow or d is pressed
        if keys[pg.K_UP] or keys[pg.K_w]:
            # prints this so that we can detect whether the game registers the input or not
            # print("trying to go up...")
            # changes the velocity (y-axis) to be the player speed up (negative)
            self.vel.y = -PLAYER_SPEED
            # self.vy = -PLAYER_SPEED
        # detects if the player is moving in both x and y directions (diagonally)
        if self.vel.x != 0 and self.vel.y != vec(0,0):
            self.vel *= 0.7071
            # self.vel.normalize()
        # if self.vx != 0 and self.vy != 0:
        #     # changes the speed in the x and y directions so that moving diagonally is not faster
        #     # than moving in one direction
        #     # 0.7071 ~= 1/sqrt(2)
        #     self.vx *= 0.7071
        #     self.vy *= 0.7071
        # print(keys[pg.K_LEFT])
    def animate(self):
        # use the time element to get now
        now = pg.time.get_ticks()
        if self.dir == "none":
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
                bottom = self.rect.bottom
                self.image = self.idle_frames[self.current_frame]
                self.image.set_colorkey(NEARLY_BLACK)
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        elif self.dir == "left":
            pass
    def load_images(self):
        self.idle_frames = [self.spritesheet.get_image(0,0,TILESIZE, TILESIZE),
                            self.spritesheet.get_image(TILESIZE,0,TILESIZE, TILESIZE)
                            ]
    def update(self):
        # calls the get_keys function
        self.get_keys()
        self.animate()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.all_walls, "x")
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.all_walls, "y")
        self.rect.center = self.hit_rect.center


           
class Wall(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        # colors the rectangle with the designated color GREEN
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0,0
        self.x = x*TILESIZE
        self.y = y*TILESIZE
        self.rect.x = self.x
        self.rect.y = self.y
        # print("wall initialized")
        # print(self.rect.x)
        # print(self.rect.y)



class Mob(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_mobs
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.speed = 1
        self.vx, self.vy = 500,0
        self.x = x*TILESIZE
        self.y = y*TILESIZE
        self.rect.x = self.x
        self.rect.y = self.y
        # print("mob initialized")
        # print(self.rect.x)
        # print(self.rect.y)
        
    def update(self):
        # detects if the right of the mob has hit the edge of the right 
        # or the left of the mob has hit the left wall
        if self.rect.right > WIDTH or self.rect.x < 0:
            # print("i've broken out!")
            # changes speed to -1 to switch the direction of the velocity
            self.speed *= -1
            # makes the mob go down (y-value up) one unit after colliding with the edge
            self.y += TILESIZE
        self.x += self.vx * self.game.dt * self.speed
        self.rect.x = self.x
        self.y += self.vy * self.game.dt * self.speed
        self.rect.y = self.y
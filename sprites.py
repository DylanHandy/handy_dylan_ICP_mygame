import pygame as pg
from settings import *
from pygame.sprite import Sprite
from utils import *

from random import randint

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
            # checks to see if we are below the wall
            if hits[0].rect.centery < sprite.hit_rect.centery:
                # reposition the player (sprite) to the bottom of wall
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            # sets the y velocity to 0 to stop the player from continuing moving
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

class Player(Sprite):
    # game is a parameter so that we can pass things between files
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        # pass self.groups in Sprite so that game can leverage groups
        Sprite.__init__(self, self.groups)
        self.game = game
        # creates a spritesheet using sprite_sheet.png
        self.spritesheet = Spritesheet(path.join(self.game.img_dir, "sprite_sheet.png"))
        # calls the load_images function through self
        self.load_images()
        # establishes the size of the image to have dimensions of TILESIZE
        self.image = pg.Surface((TILESIZE, TILESIZE))
        # gets the image from self.spritesheet to display it onscreen
        self.image = self.spritesheet.get_image(0,0,TILESIZE,TILESIZE)
        # self.image.set_colorkey(BLACK)
        # colors the rectangle with the designated color WHITE
        # self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        # establishes velocity as a vector
        self.vel = vec(0,0)
        # establishes acceleration as a vector
        self.acc = vec(0,0)
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
        self.collectibles = 0
        self.jumping = False
    # creating player controls by key presses
    def get_keys(self):
        # reset velocity to 0 again because init only runs once
        # self.vel = vec(0,0)
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
            # self.vel.x = -PLAYER_SPEED
            self.acc.x = -PLAYER_SPEED
            # self.vx = -PLAYER_SPEED
        # move to the right at the player speed if right arrow or d is pressed
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            # prints this so that we can detect whether the game registers the input or not
            # print("trying to go right...")
            # changes the velocity (x-axis) to be the player speed to the right (positive)
            # self.vel.x = PLAYER_SPEED
            self.acc.x = PLAYER_SPEED
            # self.vx = PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            # prints this so that we can detect whether the game registers the input or not
            # print("trying to go down...")
            # changes the velocity (y-axis) to be the player speed down (positive)
            # self.vel.y = PLAYER_SPEED
            self.acc.y = PLAYER_SPEED
            # self.vy = PLAYER_SPEED
        # move to the right at the player speed if right arrow or d is pressed
        if keys[pg.K_UP] or keys[pg.K_w]:
            # prints this so that we can detect whether the game registers the input or not
            # print("trying to go up...")
            # changes the velocity (y-axis) to be the player speed up (negative)
            # self.vel.y = -PLAYER_SPEED
            self.acc.y = -PLAYER_SPEED
            # self.vy = -PLAYER_SPEED
        # if spacebar is pressed
        if keys[pg.K_SPACE]:
            # run jump function
            self.jump()
        # detects if the player is moving in both x and y directions (diagonally)
        # if self.vel.x != 0 and self.vel.y != vec(0,0):
        #     self.vel *= 0.7071
            # self.vel.normalize()
        # if self.vx != 0 and self.vy != 0:
        #     # changes the speed in the x and y directions so that moving diagonally is not faster
        #     # than moving in one direction
        #     # 0.7071 ~= 1/sqrt(2)
        #     self.vx *= 0.7071
        #     self.vy *= 0.7071
        # print(keys[pg.K_LEFT])
    
    def jump(self):
        # jump only if standing on a platform
        self.rect.y += 2
        # detects collision with blocks being jumped on
        hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
        self.rect.y -= 2
        if hits and not self.jumping:
            # plays the jumping sound
            self.game.jump_sound.play()
            self.jumping = True
            # falling down from jump
            self.vel.y = -PLAYER_JUMP
    
    def is_jumping(self):
        if self.vel.y > 0:
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                self.jumping = False

    def animate(self):
        # use the time element to get now
        now = pg.time.get_ticks()
        # checks if the direction the player has been changed from "none"
        if dir == "none":
            # checks whether 350ms have elapsed between the last update and now
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
                bottom = self.rect.bottom
                self.image = self.idle_frames[self.current_frame]
                # establishes BLACK as the color that will be filtered out of the sprite
                self.image.set_colorkey(BLACK)
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        # checks if the direction the player is moving in is "left"
        elif dir == "left":
            # if it is, the sprite won't animate between frames and will remain still
            pass
    
    def load_images(self):
        self.idle_frames = [self.spritesheet.get_image(0,0,TILESIZE, TILESIZE),
                            self.spritesheet.get_image(TILESIZE,0,TILESIZE, TILESIZE)
                            ]
    
    def update(self):
        self.acc = vec(0,1)
        # calls the get_keys function
        self.animate()
        self.is_jumping
        self.get_keys()
        self.acc.x += self.vel.x * PLAYER_FRIC
        self.acc.y += self.vel.y * PLAYER_FRIC
        self.vel += self.acc
        self.rect.center = self.pos
        self.pos += self.vel + 0.5 * self.acc
        # hits detects if the player has made contact with a collectible
        hits = pg.sprite.spritecollide(self, self.game.all_collectibles, True, collide_hit_rect)
        # if the player has hit a collectible
        if hits:
            # runs 10 times
            for i in range(10):
                # creates ten particles where the hit was detected
                # (spot of the coin)
                Particle(self.game, hits[0].pos.x, hits[0].pos.y)
            self.collectibles += 1
            self.game.score += 1
            # plays the pickup_snd audio
            self.game.pickup_snd.play()
        # self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.all_walls, "x")
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.all_walls, "y")
        self.rect.center = self.hit_rect.center
        if collide_with_walls(self, self.game.all_walls, 'y'):
            self.jumping = False

           
class Wall(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)
        self.game = game
        # creates a spritesheet using sprite_sheet.png
        self.spritesheet = Spritesheet(path.join(self.game.img_dir, "sprite_sheet.png"))
        # calls the load_images function through self
        self.load_images()
        self.image = pg.Surface((TILESIZE, TILESIZE))
        # gets the image from self.spritesheet to display it onscreen
        self.image = self.spritesheet.get_image(0,0,TILESIZE,TILESIZE)
        # colors the rectangle with the designated color GREEN
        # self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.speed = 0
        self.vx, self.vy = 0,0
        self.x = x*TILESIZE
        self.y = y*TILESIZE
        self.rect.x = self.x
        self.rect.y = self.y
        # print("wall initialized")
        # print(self.rect.x)
        # print(self.rect.y)
        self.last_update = 0
        self.current_frame = 0
    
    # the same animate and load_images function are repeatedly used for all the classes
    # maybe a parent class that already has it???
    def animate(self):
        # use the time element to get now
        now = pg.time.get_ticks()
        # checks whether 350ms have elapsed between the last update and now
        if now - self.last_update > 350:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
            bottom = self.rect.bottom
            self.image = self.idle_frames[self.current_frame]
            # establishes BLACK as the color that will be filtered out of the sprite
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom

    def load_images(self):
        self.idle_frames = [self.spritesheet.get_image(4*TILESIZE,0,TILESIZE, TILESIZE)
                            ]

    def update(self):
        self.animate()
        self.x += self.vx * self.game.dt * self.speed
        self.rect.x = self.x
        self.y += self.vy * self.game.dt * self.speed
        self.rect.y = self.y

class Particle(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_particles
        Sprite.__init__(self, self.groups)
        self.game = game
        # creates a spritesheet using sprite_sheet.png
        self.spritesheet = Spritesheet(path.join(self.game.img_dir, "sprite_sheet.png"))
        # sets the size of the image as a surface an eighth of the tilesize
        self.image = pg.Surface((TILESIZE/8, TILESIZE/8))
        # colors the rectangle with the designated color GREEN
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.vel = vec(randint(-180, 180), randint(-180,180))
        self.pos = vec(x,y)
        # establishes the speed as a random integer between 1 and 3
        self.speed = randint(1,3)
        # creates countdown variable as a Cooldown class
        self.countdown = Timer()
        self.countdown.event_time = floor(pg.time.get_ticks()/1000)
        # print(self.pos.x)
        # print(self.pos.y)

    def update(self):
        # print(self.countdown.get_delta())
        # updates the position based on the speed and velocity
        self.pos += self.vel * self.speed * self.game.dt
        # if the countdown exceeds 1 second, executes the kill function
        if self.countdown.get_delta() > 1:
            # kills the particle
            self.kill()
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

class Mob(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_mobs
        Sprite.__init__(self, self.groups)
        self.game = game
        # creates a spritesheet using sprite_sheet.png
        self.spritesheet = Spritesheet(path.join(self.game.img_dir, "sprite_sheet.png"))
        # calls the load_images function through self
        self.load_images()
        # establishes the size of the image to have dimensions of TILESIZE
        self.image = pg.Surface((TILESIZE, TILESIZE))
        # gets the image from self.spritesheet to display it onscreen
        self.image = self.spritesheet.get_image(0,0,TILESIZE,TILESIZE)
        self.rect = self.image.get_rect()
        self.speed = 100
        self.hit_rect = MOB_HIT_RECT
        # establishes velocity as a vector with no magnitude or direction
        self.vel = vec(0,0)
        # establishes position as a vector with x and y
        self.pos = vec(x*TILESIZE,y*TILESIZE)
        # print("mob initialized")
        # print(self.rect.x)
        # print(self.rect.y)
        self.last_update = 0
        self.current_frame = 0

    def load_images(self):
        self.idle_frames = [self.spritesheet.get_image(2*TILESIZE,0,TILESIZE, TILESIZE),
                            self.spritesheet.get_image(3*TILESIZE,0,TILESIZE, TILESIZE)
                            ]

    def animate(self):
        # use the time element to get now
        now = pg.time.get_ticks()
        # checks whether 350ms have elapsed between the last update and now
        if now - self.last_update > 350:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
            bottom = self.rect.bottom
            self.image = self.idle_frames[self.current_frame]
            # establishes BLACK as the color that will be filtered out of the sprite
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom

    # used autocomplete by creating a chase method using pos vectors
    # and obj as a parameter
    def chase(self, obj):
        if self.pos.x < obj.pos.x:
            self.vel.x = self.speed
            self.dir = "right"
        elif self.pos.x > obj.pos.x:
            self.vel.x = -self.speed
            self.dir = "left"
        else:
            self.vel.x = 0

        if self.pos.y < obj.pos.y:
            self.vel.y = self.speed
        elif self.pos.y > obj.pos.y:
            self.vel.y = -self.speed
        else:
            self.vel.y = 0
    
    def update(self):
        self.animate()
        # detects if the right of the mob has hit the edge of the right 
        # or the left of the mob has hit the left wall
        # if self.rect.right > WIDTH or self.rect.x < 0:
        #     # print("i've broken out!")
        #     # changes speed to -1 to switch the direction of the velocity
        #     self.speed *= -1
        #     # makes the mob go down (y-value up) one unit after colliding with the edge
        #     self.y += TILESIZE
        # self.x += self.vx * self.game.dt * self.speed
        # self.rect.x = self.x
        # self.y += self.vy * self.game.dt * self.speed
        # self.rect.y = self.y
        self.chase(self.game.player)
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.all_walls, "x")
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.all_walls, "y")
        self.rect.center = self.hit_rect.center



class Collectible(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_collectibles
        Sprite.__init__(self, self.groups)
        self.game = game
        # creates a spritesheet using sprite_sheet.png
        self.spritesheet = Spritesheet(path.join(self.game.img_dir, "sprite_sheet.png"))
        # calls the load_images function through self
        self.load_images()
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        # gets the image from self.spritesheet to display it onscreen
        self.image = self.spritesheet.get_image(0,0,TILESIZE, TILESIZE)
        # colors the rectangle with the designated color GREEN
        # self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.pos = vec(x*TILESIZE, y*TILESIZE)
        # self.x = x*TILESIZE
        # self.y = y*TILESIZE
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        # print("collectible initialized")
        # print(self.rect.x)
        # print(self.rect.y)
        self.last_update = 0
        self.current_frame = 0

    def load_images(self):
        self.idle_frames = [self.spritesheet.get_image(5*TILESIZE,0,TILESIZE, TILESIZE),
                            ]

    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 350:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
            bottom = self.rect.bottom
            self.image = self.idle_frames[self.current_frame]
            # establishes BLACK as the color that will be filtered out of the sprite
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
    
    def update(self):
        self.animate()
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

class Node(Sprite):
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.is_wall = False
        self.is_start = False
        self.is_end = False
        self.visited = False
        self.in_queue = False
        # when a new node is discovered, its parent becomes the
        # node it came from
        self.parent = None

    # draws the nodes on the grid
    def draw(self, surface):
        # converts the map to gridlike rows and columns
        rect = (self.col*TILESIZE, self.row*TILESIZE, TILESIZE, TILESIZE)
        # if a node has the given attribute, sets its color to be drawn
        # categorizes the nodes visually
        if self.is_wall:
            color = BLACKISH
        elif self.is_start:
            color = GREEN
        elif self.is_end:
            color = RED
        elif self.visited:
            color = YELLOW
        elif self.in_queue:
            color = BLUE
        # detects if the node is in the path, hasn't been visited, and
        # isn't the end, so it must be the current tracing node
        elif self.parent and not self.visited and not self.is_end:
            color = ORANGE
        else:
            color = WHITE
        # draws the nodes and their outlines using their color and gray
        pg.draw.rect(surface, color, rect)
        pg.draw.rect(surface, GRAY, rect, 1)

    # gets the node's neighbors in the orthogonal directions
    def get_neighbors(self, grid):
        neighbors = []
        # orthogonal directions
        directions = [(-1,0), (1,0), (0,-1), (0,1)]
        # selects directions to find neighbors
        for dr, dc in directions:
            # adds the current node's position to the directions to get
            # the neighbor node's position
            r, c = self.row + dr, self.col + dc
        if 0 <= r < ROWS and 0 <= c < COLS:
            neighbor = grid[r][c]
            # detects if the node is an actually accessible tile and 
            # not just a wall
            if not neighbor.is_wall:
                # adds neighbor to the neighbors list to compile all the neighbors
                neighbors.append(neighbor)
        return neighbors

    def create_grid():
        # nested list comprehension
        # provides a compact way to create a 2D grid
        return [[Node(r, c) for c in range(COLS)] for r in range(ROWS)]

    def draw_all(surface, grid):
        # clears screen before each new frame is drawn
        surface.fill(WHITE)
        # draws all nodes in all rows
        for row in grid:
            for node in row:
                node.draw(surface)
        # updates the display surface to the screen so that the drawings
        # appear on screen
        pg.display.flip()
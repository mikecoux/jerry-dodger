import pygame
from pygame.locals import (K_UP, K_DOWN, K_LEFT, K_RIGHT, K_SPACE)
import sys
sys.path.append('..')
import config

# Create sprite objects
# Sprites are a 2D representation of something on the screen. Essentially, a picture.
# Pygame provides a sprite class, we create a new class that extends Sprite giving it access to the built in methods
# The surface drawn on the screen is now an attribute of 'player'

player_imgs = [pygame.image.load("../assets/skier-mike.png"), pygame.image.load("../assets/skier-mike-skiing.png")]

class Player(pygame.sprite.Sprite):
    def __init__(self):
        #Super keyword gives the instance all the props of the parent
        super(Player, self).__init__()

        # Create bitmask for pixel perfect collisions
        self.surf = player_imgs[0].convert_alpha()
        self.mask = pygame.mask.from_surface(self.surf)
        self.rect = self.surf.get_rect()

        # self.direction = pygame.math.Vector2(0,0)

        self.y_velocity = 10
        self.jump = False

        self.last = pygame.time.get_ticks()
        self.cooldown = 300


    # def update(self, pressed_keys):
    #     if pressed_keys[K_RIGHT]:
    #         self.direction.x = 1
    #     elif pressed_keys[K_LEFT]:
    #         self.direction.x = -1
    #     elif pressed_keys[K_DOWN]:
    #         self.direction.y = 1
    #     elif pressed_keys[K_UP]:
    #         self.direction.y = -1
    #     elif pressed_keys[K_SPACE]:
    #         self.direction.y = -16
    #     else:
    #         self.direction.x = 0
    #         self.direction.y = 0

    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        # move up
        if pressed_keys[K_UP]:
            self.rect.y -= 5
            self.surf = player_imgs[1].convert_alpha()

        # move down
        elif pressed_keys[K_DOWN]:
            self.rect.y += 5
            self.surf = player_imgs[1].convert_alpha()

        # move left
        elif pressed_keys[K_LEFT]:
            self.rect.x -= 5
            self.surf = player_imgs[1].convert_alpha()
            self.surf = pygame.transform.flip(self.surf, True, False)

        # move right
        elif pressed_keys[K_RIGHT]:
            self.rect.x += 5
            self.surf = player_imgs[1].convert_alpha()

        # jump
        elif pressed_keys[K_SPACE]:
            
            self.y_pos = self.rect.y


            if self.jump == False:
                self.jump = True
            if self.jump:
                self.y_pos -= self.y_velocity
                self.rect = pygame.Rect(self.rect.x, self.y_pos, self.rect[2], self.rect[3])
                self.y_velocity -= 1
                if self.y_velocity < -10:
                    self.jump = False
                    self.y_velocity = 10

        else:
            self.surf = player_imgs[0].convert_alpha()
    
        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > config.SCREEN_WIDTH:
            self.rect.right = config.SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= config.SCREEN_HEIGHT:
            self.rect.bottom = config.SCREEN_HEIGHT
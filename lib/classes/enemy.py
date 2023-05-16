import pygame
import random
import sys
sys.path.append('..')
import config

# Define the enemy object by extending pygame.sprite.Sprite
# The surface you draw on the screen is now an attribute of 'enemy'
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((20, 10))
        self.surf.fill((255, 255, 255))
        # Updates rect to be a random location along the right side of the screen
        # The center is off the screen, located between 20 and 100 px off the right edge and between the top and bottom edges
        self.rect = self.surf.get_rect(
            center=(
                random.randint(config.SCREEN_WIDTH + 20, config.SCREEN_WIDTH + 100),
                random.randint(0, config.SCREEN_HEIGHT),
            )
        )
        # Set speed to a random number between specified values
        self.speed = random.randint(1, 3)

    # update() takes no arguments because the movement is automatic
    # Remove the sprite when it passes the left edge of the screen with .kil()
    # .kill() removes the sprite from every 'group' that it belongs to
    # .kill() allows Python's garbage collector to reclaim the memory as necessary
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
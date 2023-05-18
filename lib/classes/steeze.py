import pygame
from pygame.locals import RLEACCEL
import random
import sys
sys.path.append('..')
import config

class Steeze(pygame.sprite.Sprite):
    def __init__(self, steeze_input, font, color):
        super(Steeze, self).__init__()
        self.steeze_input = steeze_input
        self.font = font
        self.color = color
        self.surf = self.font.render(self.steeze_input, True, self.color)
        self.rect = self.surf.get_rect(
            center = (
                random.randint(config.SCREEN_WIDTH + 20, config.SCREEN_WIDTH + 100),
                random.randint(0, config.SCREEN_HEIGHT),
            )
        )

        self.speed = random.randint(5, 10)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

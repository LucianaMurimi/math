import pygame
import random
from globals import *


class Bubbles(pygame.sprite.Sprite):
    def __init__(self):
        super(Bubbles, self).__init__()
        self.surf = pygame.image.load("bubbles.png").convert()
        self.surf.set_colorkey((0, 0, 0), pygame.RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    # Move the cloud based on a constant speed
    # Remove the cloud when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()

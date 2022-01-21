import pygame
import random
from globals import *


class Bubbles(pygame.sprite.Sprite):
    def __init__(self):
        super(Bubbles, self).__init__()
        self.surf = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        self.surf = pygame.image.load("./assets/images/bubbles/bubble.png").convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (56, 56))

        # starting position is randomly generated
        self.rect = self.surf.get_rect(
            # center=(
            #     random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
            #     random.randint(0, SCREEN_HEIGHT),
            # )
            center=(
                random.randint(100, SCREEN_WIDTH - 100),
                random.randint(0, 0),
            )
        )

    # move the bubbles at constant speed
    # remove the bubble when it passes the left edge of the screen
    def update(self):
        # self.rect.move_ip(-5, 0)
        self.rect.move_ip(0, 5)
        if self.rect.right < 0:
            self.kill()

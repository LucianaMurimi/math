import pygame
from globals import *

pygame.init()


class Background:
    def __init__(self):
        self.bg_x = 0
        self.bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.bg_image = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        self.bg_image = pygame.image.load("./assets/images/underwater.png").convert()
        self.bg_menu = pygame.image.load("./assets/images/water_bg.jpg").convert()

    def set_background(self, screen, is_screen):
        if is_screen == "screen_1":
            self.bg.fill(SKY_BLUE)
            screen.blit(self.bg_image, (0, 0))

        elif is_screen == "menu":
            self.bg.fill(SKY_BLUE)
            screen.blit(self.bg_menu, (0, 0))

        else:
            rel_x = self.bg_x % self.bg_image.get_rect().width
            screen.blit(self.bg_image, (rel_x - self.bg_image.get_rect().width, 0))
            if rel_x < SCREEN_WIDTH:
                screen.blit(self.bg_image, (rel_x, 0))
            self.bg_x -= 1
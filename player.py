import pygame
from globals import *
from pygame.locals import *


pygame.init()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        # create a surface object, image is drawn on it.
        self.surf = pygame.display.set_mode((65, 65))
        self.image = pygame.image.load("./assets/images/fish sprite.png").convert()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.image.set_colorkey((255,255,255), pygame.RLEACCEL)
        # self.rect = self.surf.get_rect()
        self.rect = self.surf.get_rect()

    def update(self, pressed_key):
        # if pressed_key == K_UP:
        #     self.rect.move_ip(0, -20)
        # if pressed_key == K_DOWN:
        #     self.rect.move_ip(0, 20)
        # if pressed_key == K_LEFT:
        #     self.rect.move_ip(-20, 0)
        # if pressed_key == K_RIGHT:
        #     self.rect.move_ip(20, 0)
        if pressed_key[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_key[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_key[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_key[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


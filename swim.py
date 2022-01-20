import pygame.sprite
from pygame.locals import *
from globals import *


class Swim(pygame.sprite.Sprite):
    def __init__(self):
        super(Swim, self).__init__()
        # adding all the images to sprite array
        self.images = []
        self.images.append(pygame.image.load('./assets/images/swim_to_right/1.png'))
        self.images.append(pygame.image.load('./assets/images/swim_to_right/2.png'))
        self.images.append(pygame.image.load('./assets/images/swim_to_right/3.png'))
        self.images.append(pygame.image.load('./assets/images/swim_to_right/4.png'))
        self.images.append(pygame.image.load('./assets/images/swim_to_right/5.png'))
        self.images.append(pygame.image.load('./assets/images/swim_to_right/6.png'))

        # index value to get the image from the array
        # initially it is 0
        self.index = 0

        # now the image that we will display will be the index from the image array
        self.image = self.images[self.index]

        # creating a rect at position x,y (5,5) of size (150,198) which is the size of sprite
        self.rect = pygame.Rect(50, 50, 100, 100)

    def update(self):
        # when the update method is called, we will increment the index
        self.index += 1

        # if the index is larger than the total images
        if self.index >= len(self.images):
            # we will make the index to 0 again
            self.index = 0

        # finally we will update the image that will be displayed
        self.image = self.images[self.index]

    def move(self, pressed_key):
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




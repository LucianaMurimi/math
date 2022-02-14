import pygame.sprite
from pygame.locals import *
from globals import *


class BeeSprite(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(BeeSprite, self).__init__()
        # adding all the images to sprite array
        self.images = []
        # self.images.append(pygame.image.load('./assets/images/bee/1.png'))
        # self.images.append(pygame.image.load('./assets/images/bee/2.png'))
        # self.images.append(pygame.image.load('./assets/images/bee/3.png'))
        # self.images.append(pygame.image.load('./assets/images/bee/4.png'))
        # self.images.append(pygame.image.load('./assets/images/bee/5.png'))
        # self.images.append(pygame.image.load('./assets/images/bee/6.png'))

        self.images.append(pygame.image.load('./assets/images/bee/1_.png'))
        self.images.append(pygame.image.load('./assets/images/bee/2_.png'))
        self.images.append(pygame.image.load('./assets/images/bee/3_.png'))
        self.images.append(pygame.image.load('./assets/images/bee/4_.png'))
        self.images.append(pygame.image.load('./assets/images/bee/5_.png'))
        self.images.append(pygame.image.load('./assets/images/bee/6_.png'))

        # index value to get the image from the array
        # initially it is 0
        self.index = 0

        # now the image that we will display will be the index from the image array
        self.image = self.images[self.index]
        self.x = x
        self.y = y
        # creating a rect at position x,y (5,5) of size (150,198) which is the size of sprite
        self.rect = pygame.Rect(self.x, self.y, 64, 64)

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        # when the update method is called, we will increment the index
        self.index += 1

        # if the index is larger than the total images
        if self.index >= len(self.images):
            # we will make the index to 0 again
            self.index = 0

        # finally, update the image that will be displayed
        self.image = self.images[self.index]

        return self.index

    def fly(self, pressed_key):
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


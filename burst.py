import pygame.sprite
from pygame.locals import *
from globals import *


class Burst(pygame.sprite.Sprite):
    def __init__(self):
        super(Burst, self).__init__()
        # adding all the images to sprite array
        self.images = []
        # self.images.append(pygame.image.load('./assets/images/bubbles/bubble-100px.png'))
        self.images.append(pygame.image.load('./assets/images/bubbles/bubble_64px.png'))
        self.images.append(pygame.image.load('./assets/images/bubbles/bubble_pop_2.png'))
        # self.images.append(pygame.image.load('./assets/images/bubbles/bubble_pop_3.png'))
        self.images.append(pygame.image.load('./assets/images/bubbles/bubble_pop_4.png'))
        # self.images.append(pygame.image.load('./assets/images/bubbles/bubble_pop_5.png'))
        self.images.append(pygame.image.load('./assets/images/bubbles/bubble_pop_6.png'))
        self.images.append(pygame.image.load('./assets/images/bubbles/bubble_pop_7.png'))
        self.images.append(pygame.image.load('./assets/images/bubbles/bubble_pop_8.png'))

        # index value to get the image from the array
        # initially it is 0
        self.index = 0

        # now the image that we will display will be the index from the image array
        self.image = self.images[self.index]
        self.x = SCREEN_WIDTH / 2 - 32
        self.y = 278
        # creating a rect at position x,y (5,5) of size (150,198) which is the size of sprite
        self.rect = pygame.Rect(self.x, self.y, 100, 100)

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        # when the update method is called, we will increment the index
        self.index += 1

        # if the index is larger than the total images
        if self.index >= len(self.images):
            # we will make the index to 0 again
            self.index = 0

        # finally we will update the image that will be displayed
        self.image = self.images[self.index]


        return self.index


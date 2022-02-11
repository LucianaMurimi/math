import pygame.sprite
from pygame.locals import *
from globals import *


class BoySprite(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(BoySprite, self).__init__()
        # adding all the images to sprite array
        self.images = []
        self.images.append(pygame.image.load('./assets/images/boy/1_summer_Run_001.png'))
        self.images.append(pygame.image.load('./assets/images/boy/1_summer_Run_002.png'))
        self.images.append(pygame.image.load('./assets/images/boy/1_summer_Run_003.png'))
        self.images.append(pygame.image.load('./assets/images/boy/1_summer_Run_004.png'))
        self.images.append(pygame.image.load('./assets/images/boy/1_summer_Run_005.png'))
        self.images.append(pygame.image.load('./assets/images/boy/1_summer_Run_006.png'))
        self.images.append(pygame.image.load('./assets/images/boy/1_summer_Run_007.png'))
        self.images.append(pygame.image.load('./assets/images/boy/1_summer_Run_008.png'))
        self.images.append(pygame.image.load('./assets/images/boy/1_summer_Run_009.png'))

        # index value to get the image from the array
        # initially it is 0
        self.index = 0

        # now the image that we will display will be the index from the image array
        self.image = self.images[self.index]
        self.x = x
        self.y = y
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

        # finally, update the image that will be displayed
        self.image = self.images[self.index]

        return self.index


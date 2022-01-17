import pygame
import random
from globals import *


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, number):
        super(Button, self).__init__()
        # (x, y) -> center coordinates of the circle
        self.x = x + (width / 2)
        self.y = y + (height / 2)
        # self.x = random.randint(100, 700)
        # self.y = random.randint(150, 380)
        self.radius = width / 2

        self.rect = pygame.Rect(x, y, width, height)

        self.font = pygame.font.Font(None, 48)
        self.text = self.font.render(str(number), True, BLACK)
        self.number = number
        self.background_color = SKY_BLUE

    def draw(self, screen):
        # fill the screen with the background color
        pygame.draw.rect(screen, self.background_color, self.rect)

        # draw the edges of the button
        # pygame.draw.rect(screen,BLACK,self.rect,3)
        pygame.draw.circle(screen, (254, 0, 154), (self.x, self.y), self.radius, 3)
        # Get the width and height of the text surface
        width = self.text.get_width()
        height = self.text.get_height()
        # Calculate the posX and posY
        posX = self.rect.centerx - (width / 2)
        posY = self.rect.centery - (height / 2)
        # Draw the image into the screen
        screen.blit(self.text, (posX, posY))

    def isPressed(self):
        # return true if the mouse is on the button
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            return True
        else:
            return False

    def set_color(self, color):
        # set the background color
        self.background_color = color

    def get_number(self):
        # return the number of the button
        return self.number
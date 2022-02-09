import pygame
from globals import *


class ButtonSignIn(object):
    def __init__(self, x, y, value):
        self.width = 64
        self.height = 64
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.font = pygame.font.Font("./assets/fonts/Sniglet-Regular.ttf", 28)

        if isinstance(value, str):
            self.value = value
            self.isString = True
        else:
            self.value = str(value)
            self.isInt = True

        self.text = self.font.render(self.value, True, BLACK)

        self.background_color = SKY_BLUE

    def draw(self, screen):
        """ This method will draw the button to the screen """
        # First fill the screen with the background color
        pygame.draw.rect(screen, self.background_color, self.rect)
        # Draw the edges of the button
        pygame.draw.rect(screen, (192, 192, 192), self.rect, 2)
        # Get the width and height of the text surface
        width = self.text.get_width()
        height = self.text.get_height()

        # Calculate the posX and posY
        posX = self.rect.centerx - (width / 2)
        posY = self.rect.centery - (height / 2)

        # Draw the image into the screen
        screen.blit(self.text, (posX, posY))

    def isPressed(self):
        """ Return true if the mouse is on the button """
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            global USERNAME
            USERNAME = USERNAME + self.value
            print(USERNAME)
            return USERNAME
        else:
            pass

    def set_color(self, color):
        """ Set the background color """
        self.background_color = color

    def get_btn_value(self):
        """ Return the number of the button."""
        return self.value
import pygame
from globals import *
from db import *

db = DB()

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

        if self.value == "clear":
            font = pygame.font.Font("./assets/fonts/Sniglet-Regular.ttf", 16)
            self.text = font.render(self.value, True, (255, 0, 0))

        elif self.value == "enter":
            font = pygame.font.Font("./assets/fonts/Sniglet-Regular.ttf", 16)
            self.text = font.render(self.value, True, (0, 0, 255))

        else:
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
            global PASSWORD
            global USERNAME
            global SET_PASSWORD

            if self.value == "clear":
                if SET_PASSWORD:
                    PASSWORD = PASSWORD[:-1]
                else:
                    USERNAME = USERNAME[:-1]
            elif self.value == "enter":
                if USERNAME != "":
                    SET_PASSWORD = not SET_PASSWORD

                if USERNAME != "" and PASSWORD != "":
                    res = db.SignIn(USERNAME, PASSWORD)
                    if res:
                        table
            else:
                if SET_PASSWORD:
                    PASSWORD = PASSWORD + self.value
                else:
                    USERNAME = USERNAME + self.value

            return {"username": USERNAME, "password": PASSWORD}

    def set_color(self, color):
        """ Set the background color """
        self.background_color = color

    def get_btn_value(self):
        """ Return the number of the button."""
        return self.value
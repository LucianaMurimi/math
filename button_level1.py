import pygame
from globals import *
from ball_sprite import *


class ButtonLevel1(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, number):
        super(ButtonLevel1, self).__init__()
        # (x, y) -> center coordinates of the circle
        self.x = x + (width / 2)
        self.y = y + (height / 2)

        self.radius = width / 2

        self.text_color = (2, 83, 147)

        self.rect = pygame.Rect(x, y, width, height)

        self.font = pygame.font.Font("./assets/fonts/Sniglet-Regular.ttf", 36)
        self.text = self.font.render(str(number), True, self.text_color)
        self.number = number

        self.background_color = SKY_BLUE
        self.check_background_color = False

        # self.surf = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.image = pygame.image.load("./assets/images/bubbles/bubble-64px.png").convert_alpha()

        #
        self.burst = BallSprite(x, y)
        self.bursting = pygame.sprite.Group()
        self.bursting.add(self.burst)

    def draw(self, screen):
        # width and height of the text surface
        width = self.text.get_width()
        height = self.text.get_height()

        pos_x = self.rect.centerx - (width / 2)
        pos_y = self.rect.centery - (height / 2)

        self.bursting.draw(screen)
        screen.blit(self.text, (pos_x, pos_y))

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
        self.check_background_color = not self.check_background_color

    def get_number(self):
        # return the number of the button
        return self.number


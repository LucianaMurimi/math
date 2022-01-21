import pygame
from globals import *
from swim import *


class ScreenOne:
    def __init__(self, ttf_font="./assets/fonts/Sniglet.ttf", font_size=64):
        self.font = pygame.font.Font(ttf_font, font_size)

    def display_screen_one(self, screen):
        label1 = self.font.render("Ma", True, (255, 0, 0))
        label2 = self.font.render("th", True, (15, 157, 8))
        label3 = self.font.render("Bu", True, (254, 0, 154))
        label4 = self.font.render("bb", True, (244, 160, 0))
        label5 = self.font.render("le", True, (128, 85, 51))
        label6 = self.font.render("s", True, (255, 255, 255))

        width1 = label1.get_width()
        width2 = label2.get_width()
        width3 = label3.get_width()
        width4 = label4.get_width()
        width5 = label5.get_width()
        width6 = label6.get_width()

        height = label1.get_height()

        pos_x1 = (SCREEN_WIDTH / 2) - ((width1 + width2 + width3 + width4 + width5 + width6) / 2)
        pos_x2 = pos_x1 + width1
        pos_x3 = pos_x2 + width2
        pos_x4 = pos_x3 + width3
        pos_x5 = pos_x4 + width4
        pos_x6 = pos_x5 + width5
        pos_y = (SCREEN_HEIGHT / 2) - (height / 2) - 40

        screen.blit(label1, (pos_x1, pos_y))
        screen.blit(label2, (pos_x2, pos_y))
        screen.blit(label3, (pos_x3, pos_y))
        screen.blit(label4, (pos_x4, pos_y))
        screen.blit(label5, (pos_x5, pos_y))
        screen.blit(label6, (pos_x6, pos_y))

        pygame.display.flip()

        return False


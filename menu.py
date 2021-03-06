import pygame
from globals import *


class Menu(object):
    state = -1
    text_colors = [(254, 0, 154), (255, 165, 0), (252, 252, 252), (117, 0, 92), (255, 255, 0)]
    select_color = (0, 255, 0)

    def __init__(self, menu_items, ttf_font=None, font_size=24):
        self.menu_items = menu_items
        self.font = pygame.font.Font(ttf_font, font_size)

        # a list containing the rect for each item
        self.rect_list = self.get_rect_list(menu_items)

    def get_rect_list(self, menu_items):
        rect_list = []
        for index, menu_item in enumerate(menu_items):
            # amount of space needed to render text
            size = self.font.size(menu_item)
            # get the width and height of the text
            width = size[0]
            height = size[1]

            # top-left coordinates of the menu_items
            pos_x = (SCREEN_WIDTH / 2) - (width / 2)
            total_height = len(menu_items) * height
            pos_y = (SCREEN_HEIGHT / 2) - (total_height / 2) + (index * 1.2 * height)

            # append rect to the list
            rect = pygame.Rect(pos_x, pos_y, width, height)
            rect_list.append(rect)

        return rect_list

    def display_frame(self, screen):
        for index, menu_item in enumerate(self.menu_items):
            if self.state == index:
                label = self.font.render(menu_item, True, self.select_color)
            else:
                label = self.font.render(menu_item, True, self.text_colors[index])
            width = label.get_width()
            height = label.get_height()

            # top-left coordinates of the menu_items
            pos_x = (SCREEN_WIDTH / 2) - (width / 2)
            total_height = len(self.menu_items) * height
            pos_y = (SCREEN_HEIGHT / 2) - (total_height / 2) + (index * 1.2 * height)

            screen.blit(label, (pos_x, pos_y))

    def collide_points(self):
        index = -1
        mouse_pos = pygame.mouse.get_pos()
        for i, rect in enumerate(self.rect_list):
            if rect.collidepoint(mouse_pos):
                index = i

        return index

    def update(self, key_press=False, options=None):
        if not key_press:
            # assign collide_points to state
            self.state = self.collide_points()
        elif key_press == pygame.K_DOWN:
            if self.state >= options:
                self.state = options
            else:
                self.state = self.state + 1
        elif key_press == pygame.K_UP:
            if self.state <= 0:
                self.state = 0
            else:
                self.state = self.state - 1




from spritesheet import *


class Menu(object):
    state = -1
    text_colors = [(255, 0, 0), (15, 157, 8), (254, 0, 154), (244, 160, 0)]
    select_color = (128, 85, 51)

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

    def update(self):
        # assign collide_points to state
        self.state = self.collide_points()

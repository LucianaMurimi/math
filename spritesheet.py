import pygame
from globals import *

pygame.init()


class Spritesheet:
    def __init__(self, filename, cols, rows):
        self.filename = filename
        self.surf = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        self.sprite_sheet = pygame.image.load(filename).convert_alpha()
        # self.sprite_sheet.set_colorkey((0, 0, 0), pygame.RLEACCEL)

        self.cols = cols
        self.rows = rows
        self.total_cell_count = cols * rows

        self.rect = self.sprite_sheet.get_rect()
        w = self.cell_width = self.rect.width / cols
        h = self.cell_height = self.rect.height / rows
        hw, hh = self.cell_center = (w / 2, h / 2)

        self.cells = list([(index % cols * w, index / cols * h) for index in range(self.total_cell_count)])
        # print(self.cells)
        self.handle = list([
            (0, 0), (-hw, 0), (-w, 0),
            (0, -hh), (-hw, -hh), (-w, -hh),
            (0, -h), (-hw, -h), (-w, -h)
        ])

    def draw(self, surface, cell_index, x, y, handle=0):
        # print(cell_index)
        # surface.blit(self.sprite_sheet, (x+self.handle[handle][0], y+self.handle[handle][1]), self.cells[cell_index])
        l = (0, 100)[cell_index % 2 == 0]
        surface.blit(self.sprite_sheet, (x, y), (0, l, self.cell_width, self.cell_height))

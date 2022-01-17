import pygame

from game import Game
from globals import *

pygame.init()

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
screen.fill(SKY_BLUE)

# window caption
pygame.display.set_caption("Math Bubbles")

# GAME LOOP

# game object
game = Game()

# run until the user asks to quit
running = True
clock = pygame.time.Clock()

while running:
    running = game.process_events()
    game.run_logic()
    game.display_frame(screen)

    clock.tick(30)

pygame.quit()

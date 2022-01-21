import pygame
from globals import *
from game import Game


pygame.init()

# default display
pygame.display.set_caption("Math Bubbles")
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
screen.fill(SKY_BLUE)

# GAME LOOP
# game object
game = Game()

# run until the user asks to quit
running = True

clock = pygame.time.Clock()

while running:
    running = game.process_events(screen)
    game.run_logic()
    game.display_frame(screen)

    clock.tick(15)

pygame.quit()
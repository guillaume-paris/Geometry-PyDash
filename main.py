import pygame
from settings.config import *
from states.game_state import GameState

# pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

game_state = GameState(screen)
game_state.set_state("started")

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("black")

    pygame.display.flip()
    clock.tick(FRAME_RATE)

pygame.quit()
import pygame
from settings.config import *
from states.GameStates import GameState

# pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

game_state = GameState(screen)

while game_state.is_running():
    # Core game

    game_state.run()

    pygame.display.flip()
    clock.tick(FRAME_RATE)

pygame.quit()

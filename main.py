import pygame
from settings.config import *
from states.GameStates import GameState
from utils.inputs import listen_common_inputs

# pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

game_state = GameState(screen)

running = True

while running:
    # Common inputs
    running = listen_common_inputs(running)

    # Core game
    game_state.run()

    pygame.display.flip()
    clock.tick(FRAME_RATE)

pygame.quit()

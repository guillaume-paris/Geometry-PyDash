import pygame

from settings.config import *


def listen_common_inputs(running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            return running
    return running

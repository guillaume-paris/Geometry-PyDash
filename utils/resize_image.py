import pygame


def resize(img, size=(32, 32)):
    resized = pygame.transform.smoothscale(img, size)
    return resized

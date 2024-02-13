import pygame


class Sprite(pygame.sprite.Sprite):

    def __init__(self, image, pos, *groups):
        super().__init__(*groups)
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
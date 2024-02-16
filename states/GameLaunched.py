import pygame
import os

from game.Player import Player
from settings.config import *
from settings.constants import *
from utils.level import init_level


class GameLaunched:
    def __init__(self, screen, set_running):
        self.screen = screen
        self.set_running = set_running

        # Level
        self.level = []
        self.level_width = 0
        self.level_height = 0

        # Sprite groups
        self.elements = pygame.sprite.Group()
        self.player_sprites = pygame.sprite.Group()

        # Stats
        self.orbs_coords = []

        # Image load
        self.bg = pygame.image.load(os.path.join("assets/images", "bg.png"))
        avatar = pygame.image.load(os.path.join("assets/images", "avatar.png"))  # load the main character
        pygame.display.set_icon(avatar)

        # Player
        self.player = Player(screen, avatar, self.elements, (150, 150), self.player_sprites)

    def set_level(self, level: [str]):
        self.level = level
        self.level_width = len(level * 32)
        self.level_height = len(level) * 32
        init_level(self.level, self.elements, self.orbs_coords)

    def move_camera(self):
        for sprite in self.elements:
            sprite.rect.x -= PlAYER_SPEED

    def run(self):
        self.move_camera()
        self.handle_inputs()
        self.draw()

    def draw(self):
        self.player_sprites.update()
        self.screen.blit(self.bg, (0, 0))
        if self.player.isJump:
            self.player.draw_player_jump()
        else:
            self.player_sprites.draw(self.screen)
        self.elements.draw(self.screen)

    def handle_inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.set_running(False)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.set_running(False)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            self.player.jump()

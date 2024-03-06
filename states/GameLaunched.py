import pygame
import os

from game.Player import Player
from settings.config import *
from settings.constants import *
from utils.level import init_level
from utils.sprites_load import coin
from pygame.draw import rect


class GameLaunched:
    def __init__(self, screen, set_running, set_state, level_selected: int):
        self.screen = screen
        self.set_running = set_running
        self.set_state = set_state
        self.CameraX = 0

        # Level
        self.level_selected = level_selected
        self.level = []
        self.level_width = 0
        self.level_height = 0

        # Sprite groups
        self.elements = pygame.sprite.Group()
        self.player_sprites = pygame.sprite.Group()

        # Stats
        self.font_stats = pygame.font.Font("assets/fonts/PUSAB___.otf", 18)
        self.orbs_coords = []
        self.attempts = 0
        self.progression_bar = 0

        # Image load
        self.bg = pygame.image.load(os.path.join("assets/images", "bg.png"))
        self.avatar = pygame.image.load(
            os.path.join("assets/images/character", "character_1.png"))  # Character 1 by default
        pygame.display.set_icon(self.avatar)

        # Player
        self.player = Player(screen, self.avatar, self.elements, (150, 150), self.player_sprites)

    def set_level(self, level: [str]):
        self.level = level
        self.level_width = len(level * 32)
        self.level_height = len(level) * 32
        init_level(self.level, self.elements, self.orbs_coords)

    def set_character(self, character_selected: str):
        print(character_selected)
        self.avatar = pygame.image.load(
            os.path.join("assets/images/character", character_selected))
        self.reset()  # reset with the new character

    def move_camera(self):
        self.player.vel.x = 6
        self.CameraX = self.player.vel.x
        for sprite in self.elements:
            sprite.rect.x -= self.CameraX

    def draw_end_screen(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(200)
        self.screen.blit(overlay, (0, 0))

        pydash_logo = pygame.image.load(os.path.join("assets/fonts", "logo - PyDash.png"))
        font_title = pygame.font.Font("assets/fonts/PUSAB___.otf", 56)
        font_interactions = pygame.font.Font("assets/fonts/PUSAB___.otf", 20)

        if self.player.died:
            text_title = font_title.render("You died", True, (225, 28, 10, 1))
            text_interactions = font_interactions.render("Press ESC to return to the menu or SPACE to restart", True,
                                                         (255, 255, 255))
        elif self.player.win:
            text_title = font_title.render("You won", True, (255, 255, 255))
            text_interactions = font_interactions.render("Press ENTER to return to the menu", True, (255, 255, 255))
        else:
            return

        pydash_logo_rect = pydash_logo.get_rect(center=(SCREEN_WIDTH / 2, 100))
        self.screen.blit(pydash_logo, pydash_logo_rect)
        text_title_rect = text_title.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50))
        self.screen.blit(text_title, text_title_rect)
        text_interactions_rect = text_interactions.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 30))
        self.screen.blit(text_interactions, text_interactions_rect)

    def run(self):
        if not self.player.died and not self.player.win:
            self.move_camera()
        self.handle_inputs()
        self.draw()

        if self.player.died or self.player.win:
            self.draw_end_screen()

    def reset(self):
        self.player_sprites = pygame.sprite.Group()
        self.elements = pygame.sprite.Group()
        self.player = Player(self.screen, self.avatar, self.elements, (150, 150), self.player_sprites)
        self.set_level(self.level)
        self.attempts += 1
        self.progression_bar = 0

    def draw_stats(self, money=0):
        progress_colors = [pygame.Color("red"), pygame.Color("orange"), pygame.Color("yellow"),
                           pygame.Color("lightgreen"),
                           pygame.Color("green")]

        tries = self.font_stats.render(f" Attempt {str(self.attempts)}", True, WHITE)
        BAR_LENGTH = 600
        BAR_HEIGHT = 10
        player_position_percentage = 0.8 / self.level_width
        if (self.progression_bar + player_position_percentage * BAR_LENGTH) <= BAR_LENGTH:
            self.progression_bar += player_position_percentage * BAR_LENGTH

        for i in range(1, money):
            self.screen.blit(coin, (BAR_LENGTH, 25))

        outline_rect = pygame.Rect(5, 5, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(5, 5, self.progression_bar, BAR_HEIGHT)
        color_index = int(player_position_percentage * len(progress_colors))
        col = progress_colors[min(color_index, len(progress_colors) - 1)]
        rect(self.screen, col, fill_rect, 0, 4)
        rect(self.screen, WHITE, outline_rect, 3, 4)
        self.screen.blit(tries, (BAR_LENGTH + 8, 3))

    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        self.player_sprites.update()
        self.draw_stats(self.player.get_coins())
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
                if self.player.died or self.player.win:
                    if event.key == pygame.K_ESCAPE or (event.key == pygame.K_RETURN and self.player.win):
                        self.set_state("menu")
                        self.reset()
                    elif event.key == pygame.K_SPACE and self.player.died:
                        self.reset()
                else:
                    if event.key == pygame.K_ESCAPE:
                        self.set_state("menu")
                        self.attempts = 0
                        self.reset()
                    if event.key == pygame.K_r:
                        self.reset()

        keys = pygame.key.get_pressed()
        if not self.player.died and not self.player.win:
            if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
                self.player.isJump = True

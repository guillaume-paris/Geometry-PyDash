import os

import pygame

from settings.config import SCREEN_WIDTH, SCREEN_HEIGHT


class CharacterSelection:
    def __init__(self, screen, set_state, set_menu_state, set_running, set_character, character_selected):
        self.screen = screen
        self.set_state = set_state
        self.set_menu_state = set_menu_state
        self.set_running = set_running
        self.set_character = set_character
        self.character_selected = character_selected

        self.font_title = pygame.font.Font("assets/fonts/PUSAB___.otf", 56)
        self.font_informations = pygame.font.Font("assets/fonts/PUSAB___.otf", 24)

        self.character_1 = pygame.image.load(os.path.join("assets/images/character", "character_1.png"))
        self.character_2 = pygame.image.load(os.path.join("assets/images/character", "character_2.png"))
        self.character_3 = pygame.image.load(os.path.join("assets/images/character", "character_3.png"))

        self.character_selection = 0
        self.characters = [self.character_1, self.character_2, self.character_3]
        self.character_positions = [
            (SCREEN_WIDTH / 2 / 2, 300),
            (SCREEN_WIDTH / 2, 300),
            (SCREEN_WIDTH / 2 + (SCREEN_WIDTH / 2 / 2), 300)
        ]

    def select_character(self, character_selected):
        self.character_selected = character_selected
        if self.character_selected == 0:
            self.set_character("character_1.png")
        elif self.character_selected == 1:
            self.set_character("character_2.png")
        elif self.character_selected == 2:
            self.set_character("character_3.png")
        else:
            exit(-42)

    def get_character_image_and_rect(self, image, x, y, scale):
        zoomed_image = pygame.transform.rotozoom(image, 0, scale)
        character_rect = zoomed_image.get_rect(center=(x, y))
        return zoomed_image, character_rect

    def draw(self):
        text_title = self.font_title.render("Characters", True, (225, 225, 225))
        text_title_rect = text_title.get_rect(center=(SCREEN_WIDTH / 2, 50))
        self.screen.blit(text_title, text_title_rect)
        close_button = self.font_title.render("X", True, (225, 28, 10, 1))
        close_button_rect = close_button.get_rect(center=(30, 30))
        self.screen.blit(close_button, close_button_rect)
        close_info = self.font_informations.render("ESC", True, (225, 225, 225))
        close_info_rect = close_button.get_rect(center=(80, 40))
        self.screen.blit(close_info, close_info_rect)
        character_1_rect = self.character_1.get_rect(center=(SCREEN_WIDTH / 2 / 2, 300))
        character_2_rect = self.character_2.get_rect(center=(SCREEN_WIDTH / 2, 300))
        character_3_rect = self.character_3.get_rect(center=(SCREEN_WIDTH / 2 + (SCREEN_WIDTH / 2 / 2), 300))
        self.screen.blit(self.character_1, character_1_rect.topleft)
        self.screen.blit(self.character_2, character_2_rect.topleft)
        self.screen.blit(self.character_3, character_3_rect.topleft)

        scale = 1 + 0.1 * 1.5

        for i, character in enumerate(self.characters):
            x, y = self.character_positions[i]
            zoomed_image, character_rect = self.get_character_image_and_rect(character, x, y, scale if i == self.character_selection else 1)

            if i == self.character_selected:
                highlight_rect = pygame.Rect(character_rect.left - 10, character_rect.top - 10, character_rect.width + 20, character_rect.height + 20)
                pygame.draw.rect(self.screen, (47, 2, 91), highlight_rect, border_radius=10)

            self.screen.blit(zoomed_image, character_rect.topleft)
            setattr(self, f'{character}_button_rect', character_rect)


    def handle_inputs(self, event):
        if event.key == pygame.K_RIGHT:
            self.character_selection = (self.character_selection + 1) % len(self.characters)
        elif event.key == pygame.K_LEFT:
            self.character_selection = (self.character_selection - 1) % len(self.characters)
        elif event.key == pygame.K_RETURN:
            self.select_character(self.character_selection)
        elif event.key == pygame.K_ESCAPE:
            self.set_menu_state("main")

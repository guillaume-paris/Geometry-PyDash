import os

import pygame

from settings.config import SCREEN_WIDTH, SCREEN_HEIGHT


class LevelSelection:
    def __init__(self, screen, set_state, set_menu_state, set_running, set_level, level_selected):
        self.screen = screen
        self.set_state = set_state
        self.set_menu_state = set_menu_state
        self.set_running = set_running

        self.set_level = set_level
        self.level_selected = level_selected

        self.font_title = pygame.font.Font("assets/fonts/PUSAB___.otf", 56)
        self.font_informations = pygame.font.Font("assets/fonts/PUSAB___.otf", 24)
        self.font_levels = pygame.font.Font("assets/fonts/PUSAB___.otf", 44)

        self.levels = ["Level 1", "Level 2", "Level 3"]
        self.level_selection = 0

    def select_level(self, level_selected):
        self.level_selected = level_selected
        self.set_level(level_selected)

    def draw(self):
        text_title = self.font_title.render("Levels", True, (225, 225, 225))
        text_title_rect = text_title.get_rect(center=(SCREEN_WIDTH / 2, 50))
        self.screen.blit(text_title, text_title_rect)
        close_button = self.font_title.render("X", True, (225, 28, 10, 1))
        close_button_rect = close_button.get_rect(center=(30, 30))
        self.screen.blit(close_button, close_button_rect)
        close_info = self.font_informations.render("ESC", True, (225, 225, 225))
        close_info_rect = close_button.get_rect(center=(80, 40))
        self.screen.blit(close_info, close_info_rect)

        for i, level_name in enumerate(self.levels):
            y_pos = 220 + i * 70
            text_level = self.font_levels.render(level_name, True, (225, 225, 225))

            if i == self.level_selected:
                text_level_rect = text_level.get_rect(center=(SCREEN_WIDTH / 2, y_pos))
                if i == self.level_selection:
                    highlight_rect = pygame.Rect(text_level_rect.left - 55, text_level_rect.top - 15,
                                                 text_level_rect.width + 110, text_level_rect.height + 30)
                else:
                    highlight_rect = pygame.Rect(text_level_rect.left - 10, text_level_rect.top - 5,
                                                 text_level_rect.width + 20, text_level_rect.height + 10)
                pygame.draw.rect(self.screen, (47, 2, 91), highlight_rect, border_radius=10)
            if i == self.level_selection:
                scale = 1.5  # Facteur de zoom pour le niveau sélectionné
                zoomed_text_level = pygame.transform.rotozoom(text_level, 0, scale)
                text_level_rect = zoomed_text_level.get_rect(center=(SCREEN_WIDTH / 2, y_pos))
            else:
                scale = 1.0  # Pas de zoom pour les niveaux non sélectionnés
                text_level_rect = text_level.get_rect(center=(SCREEN_WIDTH / 2, y_pos))

            self.screen.blit(text_level if scale == 1.0 else zoomed_text_level, text_level_rect.topleft)

    def handle_inputs(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.level_selection = (self.level_selection + 1) % len(self.levels)
            elif event.key == pygame.K_UP:
                self.level_selection = (self.level_selection - 1) % len(self.levels)
            elif event.key == pygame.K_RETURN:
                self.select_level(self.level_selection)
            elif event.key == pygame.K_ESCAPE:
                self.set_menu_state("main")
import os

import pygame

from settings.config import SCREEN_WIDTH, SCREEN_HEIGHT


class MainMenu:
    def __init__(self, screen, set_state, set_menu_state, set_running):
        self.screen = screen
        self.set_state = set_state
        self.set_menu_state = set_menu_state
        self.set_running = set_running

        self.font_title = pygame.font.Font("assets/fonts/PUSAB___.otf", 56)
        self.font_informations = pygame.font.Font("assets/fonts/PUSAB___.otf", 24)

        # Main menu images
        self.pydash_logo = pygame.image.load(os.path.join("assets/fonts", "logo - PyDash.png"))
        self.play_button = pygame.image.load(os.path.join("assets/images/menu", "play-button.png"))
        self.characters_button = pygame.image.load(os.path.join("assets/images/menu", "characters-button.png"))
        self.levels_button = pygame.image.load(os.path.join("assets/images/menu", "levels-button.png"))

        # Main menu navigation
        self.selected_button = 0  # 0: play, 1: characters, 2: levels
        self.buttons = ["play", "characters", "levels"]
        self.button_images = {
            "play": self.play_button,
            "characters": self.characters_button,
            "levels": self.levels_button
        }
        self.button_positions = {
            "play": (SCREEN_WIDTH / 2, 350),
            "characters": (SCREEN_WIDTH / 2 / 2, 350),
            "levels": (SCREEN_WIDTH / 2 + (SCREEN_WIDTH / 2 / 2), 350)
        }

    def activate_selected_button(self):
        selected = self.buttons[self.selected_button]
        if selected == "play":
            self.set_state("launched")
        elif selected == "characters":
            self.set_menu_state("characters")
        elif selected == "levels":
            self.set_menu_state("levels")

    def handle_inputs(self, event):
        if event.key == pygame.K_RIGHT:
            self.selected_button = (self.selected_button - 1) % len(self.buttons)
        elif event.key == pygame.K_LEFT:
            self.selected_button = (self.selected_button + 1) % len(self.buttons)
        elif event.key == pygame.K_RETURN:
            self.activate_selected_button()
        elif event.key == pygame.K_ESCAPE:
            self.set_running(False)

    def draw_logo(self):
        """Draw the game's logo."""
        pydash_logo_rect = self.pydash_logo.get_rect(center=(SCREEN_WIDTH / 2, 100))
        self.screen.blit(self.pydash_logo, pydash_logo_rect)

    def draw_buttons(self):
        """Draw all the menu buttons with zoom effect on the selected one."""
        scale = 1 + 0.1 * 1.5  # Oscillating scale factor for zoom effect

        for i, button_name in enumerate(self.buttons):
            button_image = self.button_images[button_name]
            x, y = self.button_positions[button_name]
            zoomed_image, button_rect = self.get_button_image_and_rect(button_image, x, y, scale if i == self.selected_button else 1)
            self.screen.blit(zoomed_image, button_rect.topleft)
            setattr(self, f'{button_name}_button_rect', button_rect)

    def get_button_image_and_rect(self, image, x, y, scale):
        zoomed_image = pygame.transform.rotozoom(image, 0, scale)
        button_rect = zoomed_image.get_rect(center=(x, y))
        return zoomed_image, button_rect

    def draw_quit_text(self):
        """Draw the text to quit the game."""
        text_quit = self.font_informations.render("Press ESC to quit the game", True, (0, 0, 0))
        text_quit_rect = text_quit.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 30))
        self.screen.blit(text_quit, text_quit_rect)

    def draw(self):
        self.draw_logo()
        self.draw_buttons()
        self.draw_quit_text()
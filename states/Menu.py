import os

import pygame

from settings.config import SCREEN_WIDTH, SCREEN_HEIGHT
from states.menu.CharacterSelection import CharacterSelection
from states.menu.LevelSelection import LevelSelection
from states.menu.MainMenu import MainMenu


class Menu:
    def __init__(self, screen, set_running, set_state, set_character, character_selected, set_level, level_selected):
        self.screen = screen
        self.set_running = set_running
        self.set_state = set_state
        self.menu_state = "main"

        self.bg = pygame.image.load(os.path.join("assets/images", "bg.png"))

        self.mainMenu = MainMenu(self.screen, self.set_state, self.set_menu_state, self.set_running)
        self.CharacterSelection = CharacterSelection(self.screen, self.set_state, self.set_menu_state, self.set_running, set_character, character_selected)
        self.LevelSelection = LevelSelection(self.screen, self.set_state, self.set_menu_state, self.set_running, set_level, level_selected)

    def run(self):
        self.handle_inputs()
        self.draw()

    def set_menu_state(self, state):
        self.menu_state = state

    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        if self.menu_state == "main":
            self.mainMenu.draw()
        elif self.menu_state == "characters":
            self.CharacterSelection.draw()
        elif self.menu_state == "levels":
            self.LevelSelection.draw()
        else:
            exit(-42)

    def handle_inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.set_running(False)
            if event.type == pygame.KEYDOWN:
                if self.menu_state == "main":
                    self.mainMenu.handle_inputs(event)
                elif self.menu_state == "characters":
                    self.CharacterSelection.handle_inputs(event)
                elif self.menu_state == "levels":
                    self.LevelSelection.handle_inputs(event)
                else:
                    exit(-42)

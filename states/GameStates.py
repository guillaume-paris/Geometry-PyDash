import pygame

from settings.config import *
from settings.constants import *
from states.GameLaunched import GameLaunched
from states.Menu import Menu
from utils.level import load_levels


class GameState:
    def __init__(self, screen):
        self.state = "menu"
        self.running = True
        self.screen = screen
        self.level_selected = 0
        self.character_selected = 0
        self.levels = load_levels(["level_maps/level_test.csv", "level_maps/level_1.csv", "level_maps/level_2.csv"])
        self.gameLaunched = GameLaunched(self.screen, self.set_running, self.set_state, self.level_selected)
        self.menu = Menu(self.screen, self.set_running, self.set_state, self.set_character, self.character_selected, self.set_level, self.level_selected)
        self.gameLaunched.set_level(self.levels[self.level_selected])

    def set_character(self, character_selected):
        self.character_selected = character_selected
        self.gameLaunched.set_character(character_selected)

    def set_level(self, level_selected):
        self.level_selected = level_selected
        self.gameLaunched.set_level(self.levels[level_selected])

    def init_level(self):
        self.gameLaunched.set_level(self.levels[self.level_selected])

    def is_running(self):
        return self.running

    def set_running(self, running):
        self.running = running

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def run(self):
        if self.state == "menu":
            self.menu.run()
        elif self.state == "launched":
            self.gameLaunched.run()
        else:
            exit(-42)

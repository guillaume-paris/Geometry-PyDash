import pygame

from settings.config import *
from settings.constants import *
from states.GameLaunched import GameLaunched
from utils.level import load_levels


class GameState:
    def __init__(self, screen):
        self.state = "started"
        self.screen = screen
        self.level = 1
        self.levels = load_levels(["level_maps/level_1.csv", "level_maps/level_2.csv"])
        self.gameLaunched = GameLaunched(self.screen)
        self.gameLaunched.set_level(self.levels[0])

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def run(self):
        if self.state == "not_started":
            # self.gameLaunched.draw()
            pass
        elif self.state == "started":
            self.gameLaunched.run()
        else:
            exit(-42)

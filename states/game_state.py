import pygame

from settings.config import *
from settings.constants import *


class GameState:
    def __init__(self, screen):
        self.state = "not_started"
        self.screen = screen
        self.level = 1

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

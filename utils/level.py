import csv
import os

import pygame

from game.Sprites.Coin import Coin
from game.Sprites.End import End
from game.Sprites.Orb import Orb
from game.Sprites.Platform import Platform
from game.Sprites.Spike import Spike
from game.Sprites.Trick import Trick
from utils.sprites_load import *


def load_levels(levels_file_path: [str]):
    levels = []
    for file_path in levels_file_path:
        levels.append(load_level(file_path))
    return levels


def load_level(file_path: str):
    with open(file_path, newline='') as csvfile:
        level_data = csv.reader(csvfile, delimiter=',')
        return list(level_data)


def init_level(map_level: [str], elements, orbs_coords):

    x = 0
    y = 0

    for row in map_level:
        for col in row:

            if col == "0":
                Platform(block, (x, y), elements)

            if col == "Coin":
                Coin(coin, (x, y), elements)

            if col == "Spike":
                Spike(spike, (x, y), elements)
            if col == "Orb":
                orbs_coords.append([x, y])

                Orb(orb, (x, y), elements)

            if col == "T":
                Trick(trick, (x, y), elements)

            if col == "End":
                End(avatar, (x, y), elements)
            x += 32
        y += 32
        x = 0

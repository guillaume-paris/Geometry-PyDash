import csv
import pygame


def load_level(file_path):
    with open(file_path, newline='') as csvfile:
        level_data = csv.reader(csvfile, delimiter=',')
        return list(level_data)


def create_level(level_data):
    level_sprites = pygame.sprite.Group()

    for y, row in enumerate(level_data):
        for x, cell in enumerate(row):
            if cell == '1':
                sprite = Obstacle(x * OBSTACLE_WIDTH, y * OBSTACLE_WIDTH, OBSTACLE_WIDTH, OBSTACLE_WIDTH, "assets/images/platform1.png")
                level_sprites.add(sprite)
            elif cell == '2':
                sprite = Obstacle(x * OBSTACLE_WIDTH, y * OBSTACLE_WIDTH, OBSTACLE_WIDTH, OBSTACLE_WIDTH, "assets/images/platform2.png")
                level_sprites.add(sprite)
    return level_sprites


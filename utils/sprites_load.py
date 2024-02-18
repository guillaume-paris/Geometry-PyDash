import os
import pygame

# Load the images
spike = pygame.image.load(os.path.join("assets/images", "obj-spike.png"))
spike = pygame.transform.smoothscale(spike, (32, 32))
coin = pygame.image.load(os.path.join("assets/images", "coin.png"))
coin = pygame.transform.smoothscale(coin, (32, 32))
block = pygame.image.load(os.path.join("assets/images", "block_1.png"))
block = pygame.transform.smoothscale(block, (32, 32))
orb = pygame.image.load((os.path.join("assets/images", "orb-yellow.png")))
orb = pygame.transform.smoothscale(orb, (32, 32))
trick = pygame.image.load((os.path.join("assets/images", "obj-breakable.png")))
trick = pygame.transform.smoothscale(trick, (32, 32))
avatar = pygame.image.load(os.path.join("assets/images/character", "character_1.png"))
import pygame

from pygame.draw import rect

from game.Sprites.Coin import Coin
from game.Sprites.End import End
from game.Sprites.Orb import Orb
from game.Sprites.Platform import Platform
from game.Sprites.Spike import Spike
from settings.constants import *
from utils.sprites_load import *


class Player(pygame.sprite.Sprite):

    def __init__(self, image, platforms, pos, *groups):
        super().__init__(*groups)
        self.onGround = False
        self.platforms = platforms
        self.died = False
        self.win = False

        self.image = pygame.transform.smoothscale(image, (32, 32))
        self.rect = self.image.get_rect(center=pos)
        self.jump_amount = 10
        self.particles = []
        self.isJump = False
        self.vel = GRAVITY
        self.coins = 0

    def jump(self):
        self.vel.y = -self.jump_amount

    def collide(self, axisPos, platforms):
        keys = pygame.key.get_pressed()

        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                """pygame sprite builtin collision method,
                sees if player is colliding with any obstacles"""
                if isinstance(p, Orb) and (keys[pygame.K_UP] or keys[pygame.K_SPACE]):
                    # pygame.draw.circle(alpha_surf, (255, 255, 0), p.rect.center, 18)
                    # screen.blit(pygame.image.load("images/editor-0.9s-47px.gif"), p.rect.center)
                    self.jump_amount = 12  # gives a little boost when hit orb
                    self.jump()
                    self.jump_amount = 10  # return jump_amount to normal

                if isinstance(p, End):
                    self.win = True

                if isinstance(p, Spike):
                    self.died = True  # die on spike

                if isinstance(p, Coin):
                    # keeps track of all coins throughout the whole game(total of 6 is possible)
                    self.coins += 1

                    # erases a coin
                    p.kill()

                if isinstance(p, Platform):  # these are the blocks (may be confusing due to self.platforms)

                    if axisPos > 0:
                        """if player is going down(yvel is +)"""
                        self.rect.bottom = p.rect.top  # dont let the player go through the ground
                        self.vel.y = 0  # rest y velocity because player is on ground

                        # set self.onGround to true because player collided with the ground
                        self.onGround = True

                        # reset jump
                        self.isJump = False
                    elif axisPos < 0:
                        """if yvel is (-),player collided while jumping"""
                        self.rect.top = p.rect.bottom  # player top is set the bottom of block like it hits it head
                    else:
                        """otherwise, if player collides with a block, he/she dies."""
                        self.vel.x = 0
                        self.rect.right = p.rect.left  # dont let player go through walls
                        self.died = True
    def update(self):
        if self.isJump:
            if self.onGround:
                self.jump()

        if not self.onGround:
            self.vel += GRAVITY

            if self.vel.y > 100:
                self.vel.y = 100

        # do x-axis collisions
        self.collide(0, self.platforms)

        # increment in y direction
        self.rect.top += self.vel.y

        # assuming player in the air, and if not it will be set to inversed after collide
        self.onGround = False

        # do y-axis collisions
        self.collide(self.vel.y, self.platforms)

        # check if we won or if player won
        # eval_outcome(self.win, self.died)

import random
import pygame

from pygame.draw import rect

from game.Sprites.Coin import Coin
from game.Sprites.End import End
from game.Sprites.Orb import Orb
from game.Sprites.Platform import Platform
from game.Sprites.Spike import Spike
from settings.config import SCREEN_WIDTH, SCREEN_HEIGHT
from settings.constants import *
from utils.sprites_load import *


class Player(pygame.sprite.Sprite):

    def __init__(self, screen, image, platforms, pos, *groups):
        super().__init__(*groups)
        self.onGround = False
        self.platforms = platforms
        self.died = False
        self.win = False

        self.alpha_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.screen = screen
        self.image = pygame.transform.smoothscale(image, (32, 32))
        self.rect = self.image.get_rect(center=pos)
        self.jump_amount = 10
        self.particles = []
        self.isJump = False
        self.vel = pygame.math.Vector2(0, 0)
        self.coins = 0

    def jump(self):
        if self.onGround:
            self.isJump = True
            self.onGround = False
            self.vel.y = -self.jump_amount

    def blitRotate(self, surf, image, pos, originpos: tuple, angle: float):
        w, h = image.get_size()
        box = [Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
        box_rotate = [p.rotate(angle) for p in box]

        # make sure the player does not overlap, uses a few lambda functions(new things that we did not learn about number1)
        min_box = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
        max_box = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])
        # calculate the translation of the pivot
        pivot = Vector2(originpos[0], -originpos[1])
        pivot_rotate = pivot.rotate(angle)
        pivot_move = pivot_rotate - pivot

        # calculate the upper left origin of the rotated image
        origin = (
            pos[0] - originpos[0] + min_box[0] - pivot_move[0], pos[1] - originpos[1] - max_box[1] + pivot_move[1])

        # get a rotated image
        rotated_image = pygame.transform.rotozoom(image, angle, 1)

        # rotate and blit the image
        surf.blit(rotated_image, origin)

    def draw_player_jump(self):
        angle = 0
        angle -= 8.1712
        self.blitRotate(self.screen, self.image, self.rect.center, (16, 16), angle)

    def draw_particle_trail(self, x, y, color=(255, 255, 255)):
        """draws a trail of particle-rects in a line at random positions behind the player"""

        self.particles.append(
            [[x - 5, y - 8], [random.randint(0, 25) / 10 - 1, random.choice([0, 0])],
             random.randint(5, 8)])

        for particle in self.particles:
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]
            particle[2] -= 0.5
            particle[1][0] -= 0.4
            rect(self.alpha_surf, color,
                 ([int(particle[0][0]), int(particle[0][1])], [int(particle[2]) for i in range(2)]))
            if particle[2] <= 0:
                self.particles.remove(particle)

    def collide(self, axisPos, platforms):
        keys = pygame.key.get_pressed()

        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                """pygame sprite builtin collision method,
                sees if player is colliding with any obstacles"""
                if isinstance(p, Orb) and (keys[pygame.K_UP] or keys[pygame.K_SPACE]):
                    pygame.draw.circle(self.alpha_surf, (255, 255, 0), p.rect.center, 18)
                    self.screen.blit(pygame.image.load("images/editor-0.9s-47px.gif"), p.rect.center)
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
                        self.rect.bottom = p.rect.top
                        self.vel.y = 0
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
        self.alpha_surf.fill((255, 255, 255, 1), special_flags=pygame.BLEND_RGBA_MULT)

        if not self.onGround:
            self.vel += GRAVITY

            if self.vel.y > 100:
                self.vel.y = 100

        # do x-axis collisions
        self.collide(0, self.platforms)

        # increment in y direction
        self.rect.top += self.vel.y

        # do y-axis collisions
        self.collide(self.vel.y, self.platforms)

        self.draw_particle_trail(self.rect.left - 1, self.rect.bottom + 2, WHITE)

        # check if we won or if player won
        # eval_outcome(self.win, self.died)
        self.screen.blit(self.alpha_surf, (0, 0))  # Blit the alpha_surf onto the screen.

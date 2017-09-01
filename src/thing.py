import pygame
from vector import Vector 
import math

class Thing(pygame.sprite.Sprite):
    """ A thing with mass and physical properties """

    def __init__(self):
        """ Construcz """
        super().__init__()
        self.pos = Vector(0, 0)
        self.vel = Vector(0, 0)
        self.rpos = 0
        self.rvel = 0.1
        self.mass = 0

    def update(self):
        self.pos.add(self.vel)
        self.rpos += self.rvel
        self.rpos = self.rpos % 2*math.pi

        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        self.image = pygame.transform.rotate(self.original_image, self.rpos)

    def update_gravity(self, masses):
        acc = Vector(0,0)
        for thing in masses:
            separation = thing.pos.sub(self.pos)
            m = separation.mag()
            acc.add(thing.mass * separation.normalise()/(m*m))
        self.vel.add(acc)

    def show(self, screen):
        pygame.draw.ellipse(screen, WHITE, [x, 20, 250, 100], 2)

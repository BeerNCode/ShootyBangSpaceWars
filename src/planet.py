import pygame

class Planet():
    """ A large object which can impart gravity onto stuff """

    def __init__(self, radius, mass, pos):
        self.pos = pos
        self.radius = radius
        self.mass = mass

    def show(self, screen):
        pygame.draw.ellipse(screen, (0, 0, 0), [self.pos.x - self.radius, self.pos.y - self.radius, self.radius*2, self.radius*2],0)

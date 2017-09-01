import pygame

class Planet():
    """ A large object which can impart gravity onto stuff """

    def __init__(self, radius, mass, pos):
        self.pos = pos
        self.radius = radius
        self.mass = mass

    def show(self, screen):
        print("showing planet at "+str(self.pos.x)+" "+str(self.pos.y))
        pygame.draw.ellipse(screen, (255, 255, 255), [self.pos.x, self.pos.y, self.radius, self.radius], 2)

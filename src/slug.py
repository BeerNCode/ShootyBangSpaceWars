from vector import Vector 
from thing import Thing
import math
import pygame

WHITE = (255, 255, 255)

class Slug(Thing):
    """ Slugs Motherfuckers """

    def __init__(self, pos, vel):
        """ Construcz """
        Thing.__init__(self)
        self.pos = pos
        self.vel = vel
        self.original_image = pygame.image.load("../LaserShot.png").convert()
        self.original_image.set_colorkey(WHITE)
        self.image = self.original_image
        self.rect = self.image.get_rect()

    def update(self):
        super().update()

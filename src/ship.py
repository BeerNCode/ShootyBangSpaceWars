from vector import Vector 
from thing import Thing
import math
import pygame

WHITE = (255, 255, 255)

class Ship(Thing):
    """ Ship It """

    def __init__(self):
        """ Construcz """
        Thing.__init__(self)
        self.original_image = pygame.image.load("ship.png").convert()
        self.original_image.set_colorkey(WHITE)
        self.image = self.original_image
        self.rect = self.original_image.get_rect()

    def update(self):
        super().update()

        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        self.image = pygame.transform.rotate(self.original_image, self.rpos * math.pi / 180)

    def update_gravity(self, masses):
        self.force.add(Vector(0, 0))
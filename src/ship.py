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
        self.rect = self.image.get_rect()

    def update(self):
        super().update()
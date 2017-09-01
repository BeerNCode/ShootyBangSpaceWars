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
        self.original_image = pygame.image.load("../base spaceship.png").convert()
        self.original_image = pygame.transform.rotate(self.original_image, -90)
        self.original_image.set_colorkey(WHITE)
        self.image = self.original_image
        self.rect = self.image.get_rect()

    def update(self):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rpos -= 0.1
        if keys[pygame.K_RIGHT]:
            self.rpos += 0.1
        if keys[pygame.K_UP]:
            thrust = Vector.fromAngle(self.rpos).mult(10)
            self.addForce(thrust)

        super().update()
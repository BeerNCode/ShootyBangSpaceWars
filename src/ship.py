from vector import Vector 
from thing import Thing
from slug import Slug
import math
import pygame

WHITE = (255, 255, 255)

class Ship(Thing):
    """ Ship It """

    def __init__(self):
        """ Construcz """
        Thing.__init__(self)
        self.original_image = pygame.image.load("../img/base spaceship.png").convert()
        self.original_image = pygame.transform.rotate(self.original_image, -90)
        self.original_image.set_colorkey(WHITE)
        self.image = self.original_image
        self.rect = self.image.get_rect()

    def update(self):
        firing = False
        b = None
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rvel -= 0.005
        if keys[pygame.K_RIGHT]:
            self.rvel += 0.005
        if keys[pygame.K_UP]:
            thrust = Vector.fromAngle(self.rpos).mult(10)
            self.addForce(thrust)
        if keys[pygame.K_SPACE]:
            b = Slug(self.pos,self.vel)
            firing = True
        super().update()
        return b
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
        self.sprites = {}
        self.add_sprite("base", "../img/spaceship.png", WHITE)
        self.add_sprite("thrust", "../img/spaceship_thrust.png", WHITE)
        self.set_sprite("base")
        self.image = self.original_image
        self.rect = self.image.get_rect()

    def add_sprite(self, id, filePath, background):
        sp = pygame.image.load(filePath).convert()
        sp = pygame.transform.rotate(sp, -90)
        sp.set_colorkey(background)
        self.sprites[id] = sp

    def set_sprite(self, id):
        self.original_image = self.sprites[id]

    def update(self):
        firing = False
        self.rvel = self.rvel*0.985
        b = []
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rvel -= 0.001
        if keys[pygame.K_RIGHT]:
            self.rvel += 0.001
        if keys[pygame.K_UP]:
            self.set_sprite("thrust")
            thrust = Vector.fromAngle(self.rpos).mult(10)
            self.addForce(thrust)
        else:
            self.set_sprite("base")
        if keys[pygame.K_SPACE]:
            b.append(Slug(self.pos,self.vel.add(Vector.fromAngle(self.rpos).mult(2)), self.rpos))
            firing = True
        super().update()
        return b
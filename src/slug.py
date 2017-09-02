from vector import Vector 
from thing import Thing
import math
import pygame

WHITE = (255, 255, 255)

class Slug(Thing):
    """ Slugs Motherfuckers """

    def __init__(self, pos, vel, rpos):
        """ Construcz """
        print("A bullitz voz made")
        Thing.__init__(self)
        self.life = 1000
        self.pos = pos
        self.vel = vel
        self.rpos = rpos
        self.original_image = pygame.image.load("../img/LaserShot.png").convert()
        self.original_image = pygame.transform.rotate(self.original_image, 90)
        self.original_image = pygame.transform.scale(self.original_image, [100, 100])
        self.original_image.set_colorkey(WHITE)
        self.image = self.original_image
        self.rect = self.image.get_rect()

    def update(self):
<<<<<<< HEAD
        self.rpos = self.vel.angle()
        super().update()
=======
        self.life -= 1
        super().update()
>>>>>>> cc951f4e76dcdde3023b0a3a49de811c8ba71116

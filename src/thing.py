import pygame
from vector import Vector 
import math

class Thing(pygame.sprite.Sprite):
    """A thing with mass and physical properties"""

    def __init__(self):
        """Construcz"""
        super().__init__()
        self.pos = Vector(50, 50)
        self.vel = Vector(0, 0)
        self.rpos = 0
        self.rvel = 0
        self.mass = 100
        self.radius = 16
        self.size = 0
        self.damage = 0

    def update(self):
        """updated the physics of the thing"""
        self.pos = self.pos.add(self.vel)
        self.rpos += self.rvel
        if self.rpos < 0:
            self.rpos = 2*math.pi
        if self.rpos > 2*math.pi:
            self.rpos = 0

        self.image = pygame.transform.rotate(self.original_image, -self.rpos * 180 / math.pi)
        self.rect = self.image.get_rect()
        self.rect.x = self.pos.x-self.rect.width/2
        self.rect.y = self.pos.y-self.rect.height/2

    def update_gravity(self, masses):
        acc = Vector(0,0)
        for thing in masses:
            separation = thing.pos.sub(self.pos)
            m = separation.mag()
            if (m < thing.radius+self.radius):
                m = self.radius+thing.radius
            acc = acc.add(separation.normalise().mult(1/(m*m)).mult(thing.mass))
        self.vel = self.vel.add(acc)

    def show(self, screen):
        pygame.draw.ellipse(screen, WHITE, [x, 20, 250, 100], 2)
        
    def addTorqe(self, torque):
        self.rvel = self.rvel + (torque/self.rmass)
        
    def addForce(self, force):
        self.vel = self.vel.add(force.mult(1/self.mass))

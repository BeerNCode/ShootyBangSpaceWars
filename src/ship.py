from vector import Vector 
from thing import Thing
from slug import Slug
import math
import pygame

WHITE = (255, 255, 255)
ENERGY_COLOUR = (100, 0, 100)
HEALTH_COLOUR = (70, 255, 150)

SLUG_SPEED = 20
SLUG_ENERGY = 5
THRUST_ENERGY = 1
THRUST = 5
RVEL_DECAY = 0.975
TURN_ACC = 0.001
ENERGY_REGEN = 0.5

class Ship(Thing):
    """ Ship It """

    def __init__(self):
        """ Construcz """
        Thing.__init__(self)
        self.id = "Dave"
        self.sprites = {}
        self.add_sprite("base", "../img/BaseSpaceship.png", WHITE)
        self.add_sprite("thrust", "../img/BaseSpaceshipForward.png", WHITE)
        self.add_sprite("thrustClockwise", "../img/BaseSpaceshipLeft.png", WHITE)
        self.add_sprite("thrustAClockwise", "../img/BaseSpaceshipRight.png", WHITE)
        self.set_sprite("base")
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.energy = 50
        self.hull = 100

    def add_sprite(self, id, filePath, background):
        sp = pygame.image.load(filePath).convert()
        sp = pygame.transform.rotate(sp, -90)
        sp.set_colorkey(background)
        self.sprites[id] = sp

    def set_sprite(self, id):
        self.original_image = self.sprites[id]

    def update(self):
        firing = False
        self.rvel = self.rvel*RVEL_DECAY
        b = []
        keys=pygame.key.get_pressed()
        
        self.set_sprite("base")
        
        if keys[pygame.K_LEFT]:
            self.set_sprite("thrustAClockwise")
            self.energy -= THRUST_ENERGY/2
            self.rvel -= TURN_ACC
        if keys[pygame.K_RIGHT]:
            self.set_sprite("thrustClockwise")
            self.energy -= THRUST_ENERGY/2
            self.rvel += TURN_ACC
        if keys[pygame.K_UP]:
            if self.energy >= THRUST_ENERGY:
                self.set_sprite("thrust")
                self.energy -= THRUST_ENERGY
                thrust = Vector.fromAngle(self.rpos).mult(THRUST)
                self.addForce(thrust)
        if keys[pygame.K_SPACE]:
            if (self.energy >= SLUG_ENERGY):
                b.append(Slug(self.pos,self.vel.add(Vector.fromAngle(self.rpos).mult(SLUG_SPEED)), self.rpos))
                self.energy -= SLUG_ENERGY
            firing = True
        if (self.energy < 100):
            self.energy += ENERGY_REGEN
        self.hull = max(0, 100-self.damage)
        super().update()
        return b

    def showStatus(self, screen, index):
        bar_width = 75
        bar_height = 8
        bar_margin = 5
        bar_step = 40 * index + 8
        text_fudge_height = 20;

        font = pygame.font.SysFont('Calibri', 12, True, False)
        screen.blit(font.render(self.id, True, WHITE), [bar_step, 10])
        if self.energy > 0:
            pygame.draw.rect(screen, ENERGY_COLOUR, [bar_step, text_fudge_height + bar_margin, self.energy*bar_width/100, bar_height], 0)
        if self.hull > 0:
            pygame.draw.rect(screen, HEALTH_COLOUR, [bar_step, text_fudge_height + 2 * bar_margin + bar_height, self.hull*bar_width/100, bar_height], 0)
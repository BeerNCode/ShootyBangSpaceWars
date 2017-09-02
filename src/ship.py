from vector import Vector 
from thing import Thing
from slug import Slug
import math
import pygame
import packets

WHITE = (255, 255, 255)
ENERGY_COLOUR = (100, 0, 100)
HEALTH_COLOUR = (70, 255, 150)

SLUG_SPEED = 20
SLUG_ENERGY = 5
THRUST_ENERGY_FACTOR = 0.04
THRUST = 10
RVEL_DECAY = 0.975
TURN_ACC = 0.002
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
        self.add_sprite("Clockwise", "../img/BaseSpaceshipLeft.png", WHITE)
        self.add_sprite("AClockwise", "../img/BaseSpaceshipRight.png", WHITE)
        self.add_sprite("thrustClockwise", "../img/BaseSpaceshipForwardLeft.png", WHITE)
        self.add_sprite("thrustAClockwise", "../img/BaseSpaceshipForwardRight.png", WHITE)
        self.add_sprite("boost", "../img/BaseSpaceshipHalfBurn.png", WHITE)
        self.add_sprite("FULLBURN", "../img/BaseSpaceshipFullBurn.png", WHITE)
        self.set_sprite("base")
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.energy = 50
        self.hull = 100
        self.thrusting = False
        self.boosting = False
        self.portTurn = False
        self.starboardTurn = False
        self.fullBurn = False
        self.firing = False


    def add_sprite(self, id, filePath, background):
        sp = pygame.image.load(filePath).convert()
        sp = pygame.transform.rotate(sp, -90)
        sp.set_colorkey(background)
        self.sprites[id] = sp

    def set_sprite(self, id):
        self.original_image = self.sprites[id]

    def setInputs(self, keys):
        self.key_up = keys["up"]
        self.key_down = keys["down"]
        self.key_left = keys["left"]
        self.key_right = keys["right"]
        self.key_space = keys["space"]

    def getInputs(self):
        keys = pygame.key.get_pressed()
        keys_packet = packets.Controls()
        if keys[pygame.K_UP]:
            keys_packet.up = True
        if keys[pygame.K_DOWN]:
            keys_packet.down = True
        if keys[pygame.K_LEFT]:
            keys_packet.left = True
        if keys[pygame.K_RIGHT]:
            keys_packet.right = True
        if keys[pygame.K_SPACE]:
            keys_packet.space = True
        return keys_packet

    def update(self):
        
        if self.key_left:
            self.portTurn = True
        if self.key_right:
            self.starboardTurn = True
        if self.key_up:
            self.thrusting = True
        if self.key_down:
            self.boosting = True
        if self.key_space:
            self.firing = True

        self.firing = False
        self.rvel = self.rvel*RVEL_DECAY
        newSlugs = []
        if self.firing:
            if (self.energy >= SLUG_ENERGY):
                newSlugs.append(Slug(self.pos,self.vel.add(Vector.fromAngle(self.rpos).mult(SLUG_SPEED)), self.rpos))
                self.energy -= SLUG_ENERGY
            firing = True
        if (self.energy < 100):
            self.energy += ENERGY_REGEN
        self.hull = max(0, 100-self.damage)
        
        if self.portTurn and self.starboardTurn:
            self.portTurn = False
            self.starboardTurn = False
            if self.boosting:
                fullBurn = True
        else:
            fullBurn = False
            
        thrust = Vector(0,0)
        if self.fullBurn:
            thrust = Vector.fromAngle(self.rpos).mult(30)
        elif self.thrusting and self.boosting:
            thrust = Vector.fromAngle(self.rpos).mult(20)
        elif self.thrusting:
            thrust = Vector.fromAngle(self.rpos).mult(10)
            if self.portTurn:
                self.rvel -= TURN_ACC
            elif self.starboardTurn:
                self.rvel += TURN_ACC
        else:
            if self.portTurn:
                self.rvel -= TURN_ACC
                self.energy -= 0.5
            elif self.starboardTurn:
                self.rvel += TURN_ACC
                self.energy -= 0.5
        energyCost = (thrust.mag()**1.3)*THRUST_ENERGY_FACTOR
        if(self.energy >= energyCost):
            self.addForce(thrust)
            self.energy -= energyCost
        
        super().update()
        return newSlugs

    def show(self, screen):
        self.set_sprite("base")
        if self.fullBurn:
            self.set_sprite("FULLBURN")
        elif self.thrusting and self.boosting:
            self.set_sprite("boost")
        elif self.thrusting:
            if self.portTurn:
                self.set_sprite("thrustAClockwise")
            elif self.starboardTurn:
                self.set_sprite("thrustClockwise")
            else:
                self.set_sprite("thrust")
        else:
            if self.portTurn:
                self.set_sprite("AClockwise")
            elif self.starboardTurn:
                self.set_sprite("Clockwise")
            else:
                self.set_sprite("base")

        bar_width = 32
        bar_height = 5
        bar_margin = 1
        font = pygame.font.SysFont('Calibri', 12, True, False)
        screen.blit(font.render(self.id, True, WHITE), [self.pos.x-self.radius, self.pos.y-self.radius-15])
        if self.energy > 0:
            pygame.draw.rect(screen, ENERGY_COLOUR, [self.pos.x-self.radius, self.pos.y+self.radius, self.energy*32/100, bar_height], 0)
        if self.hull > 0:
            pygame.draw.rect(screen, HEALTH_COLOUR, [self.pos.x-self.radius, self.pos.y+self.radius+bar_height+bar_margin, self.hull*32/100, bar_height], 0)
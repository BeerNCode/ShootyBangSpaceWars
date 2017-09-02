from vector import Vector 
from thing import Thing
from slug import Slug
from sounds import Sounds, Sound
import math
import pygame
import globals

WHITE = (255, 255, 255)
ENERGY_COLOUR = (100, 0, 100)
HEALTH_COLOUR = (70, 255, 150)

SLUG_SPEED = 20
SLUG_ENERGY = 5
THRUST_ENERGY_FACTOR = 0.04
THRUST = 10
RVEL_DECAY = 0.975
TURN_ACC = 0.005
ENERGY_REGEN = 0.5
ENERGYCAP = 100

class Ship(Thing):
    """ Ship It """

    def __init__(self):
        """ Construcz """
        Thing.__init__(self)
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
        thrusting = False
        boosting = False
        portTurn = False
        starboardTurn = False
        fullBurn = False
        
        self.set_sprite("base")
        
        if keys[pygame.K_LEFT]:
            portTurn = True
        if keys[pygame.K_RIGHT]:
            starboardTurn = True
        if keys[pygame.K_UP]:
            thrusting = True
        if keys[pygame.K_DOWN]:
            boosting = True
        if keys[pygame.K_SPACE]:
            if (self.energy >= SLUG_ENERGY):
                b.append(Slug(self.pos,self.vel.add(Vector.fromAngle(self.rpos).mult(SLUG_SPEED)), self.rpos))
                self.energy -= SLUG_ENERGY
                globals.sounds.play(Sound.Fire)
            firing = True
        if (self.energy < ENERGYCAP):
            self.energy += ENERGY_REGEN
        self.hull = max(0, 100-self.damage)
        
        if(portTurn and starboardTurn):
            portTurn = False
            starboardTurn = False
            if(boosting):
                fullBurn = True
        else:
            fullBurn = False
            
        if (fullBurn or thrusting or boosting or portTurn or starboardTurn):
            globals.sounds.play(Sound.Thrust)

        thrust = Vector(0,0)
        if (fullBurn):
            thrust = Vector.fromAngle(self.rpos).mult(30)
            self.set_sprite("FULLBURN")
        elif (thrusting and boosting):
            thrust = Vector.fromAngle(self.rpos).mult(20)
            self.set_sprite("boost")
        elif (thrusting):
            thrust = Vector.fromAngle(self.rpos).mult(10)
            if (portTurn):
                self.rvel -= TURN_ACC
                self.set_sprite("thrustAClockwise")
            elif (starboardTurn):
                self.rvel += TURN_ACC
                self.set_sprite("thrustClockwise")
            else:
                self.set_sprite("thrust")
        else:
            if (portTurn):
                self.rvel -= TURN_ACC
                self.energy -= 0.5
                self.set_sprite("AClockwise")
            elif (starboardTurn):
                self.rvel += TURN_ACC
                self.energy -= 0.5
                self.set_sprite("Clockwise")
            else:
                globals.sounds.stop(Sound.Thrust)
                self.set_sprite("base")
                
        energyCost = (thrust.mag()**1.3)*THRUST_ENERGY_FACTOR
        if(self.energy >= energyCost):
            self.addForce(thrust)
            self.energy -= energyCost
        else:
            self.set_sprite("base")
        
        super().update()
        return b
    
    def update_regen(self, lightSources):
        if (self.energy <= ENERGYCAP*2):
            for LightSource in lightSources:
                print("called")
                self.energy = self.energy + LightSource.get_energy(self.pos)
                print("charging",LightSource.get_energy(self.pos))
    

    def showStatus(self, screen, index):
        bar_width = 75
        bar_height = 8
        bar_margin = 5
        bar_step = 40 * index + 8
        text_fudge_height = 20;

        font = pygame.font.SysFont('Calibri', 12, True, False)
        screen.blit(font.render(globals.uname, True, WHITE), [bar_step, 10])
        if self.energy > 0:
            pygame.draw.rect(screen, ENERGY_COLOUR, [bar_step, text_fudge_height + bar_margin, self.energy*bar_width/100, bar_height], 0)
        if self.hull > 0:
            pygame.draw.rect(screen, HEALTH_COLOUR, [bar_step, text_fudge_height + 2 * bar_margin + bar_height, self.hull*bar_width/100, bar_height], 0)
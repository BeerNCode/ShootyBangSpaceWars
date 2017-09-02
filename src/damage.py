import pygame
import math
from vector import Vector

class Damage():

    @staticmethod
    def determineThingThingDamage(thing1,thing2):
        vec = thing1.pos.sub(thing2.pos)
        mag = vec.mag()
        if mag < (thing1.radius + thing2.radius):
            Damage.calculateThingThingDamage(thing1,thing2)

    @staticmethod
    def determineThingPlanetDamage(thing,planet):
        vec = thing.pos.sub(planet.pos)
        mag = vec.mag()
        if mag < (thing.radius + planet.radius):
            Damage.calculateThingPlanetDamage(thing,planet)


    #
    #        1--->
    #     ^ / 
    #     2   
    #

    @staticmethod
    def calculateThingThingDamage(thing1,thing2):
        #determine damage to thing 1
            relativeVelocity = thing1.vel.sub(thing2.vel)
            dir = thing1.pos.sub(thing2.pos)
            thing1VelInDir = relativeVelocity.dot(dir)/(dir.mag())
            thing1VelInDir = max(0,thing1VelInDir)
            #apply damage
            thing1.damage += thingVelInDir*thing2.mass
            thing2.damage += thingVelInDir*thing1.mass
            thing1.vel = thing1.vel.sub(dir.normalise().mult(1*thingVelInDir*(thing2.mass)/(thing1.mass+thing2.mass)))
            thing2.vel = thing2.vel.sub(dir.normalise().mult(-1*thingVelInDir*(thing1.mass)/(thing1.mass+thing2.mass)))

    @staticmethod
    def calculateThingPlanetDamage(thing,planet):
        #determine damage to thing 1
            relativeVelocity = thing.vel;
            dir = planet.pos.sub(thing.pos)
            thingVelInDir = relativeVelocity.dot(dir)/(dir.mag())
            thingVelInDir = max(0,thingVelInDir)
            #apply damage
            thing.damage += thingVelInDir*planet.mass
            thing.vel = thing.vel.sub(dir.normalise().mult(1*thingVelInDir*(planet.mass)/(thing.mass+planet.mass)))
            thing.vel = thing.vel.mult(0.95)
            thing.rvel *= 0.95
          
            
            

        
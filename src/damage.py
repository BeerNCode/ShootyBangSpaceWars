import pygame
import math
from src.vector import Vector

class Damage():

    @staticmethod
    def determineDamage(thing1,thing2):
        vec = thing1.pos.sub(thing2.pos)
        mag = vec.mag()
        if (mag < thing1.size || mag < thing2.size):
            calculateDamage(thing1,thing2)


    #
    #        1--->
    #     ^ / 
    #     2   
    #

    @staticmethod
    def calculateDamage(thing1,thing2):
        #determine damage to thing 1
            relativeVelocity = thing1.vel.sub(thing2.vel)
            dir = thing1.pos.sub(thing2.pos)
            thing1VelInDir = relativeVelocity.dot(dir)/(dir.mag())
            thing1VelInDir = max(0,thing1VelInDir)
            #apply damage
            thing1.damage += velInDir*thing2.mass
            thing2.damage += velInDir*thing1.mass
            thing1.vel = thing1.vel.sub(dir.mult(thing1VelInDir)*(thing2.mass)/(thing1.mass+thing2.mass))
            thing2.vel = thing2.vel.sub(dir.mult(-1*thing1VelInDir)*(thing1.mass)/(thing1.mass+thing2.mass))
            
            

        
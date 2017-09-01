import pygame
from src.vector import Vector

class Damage():

    @staticmethod
    def determineDamage(thing1,thing2):
        vec = thing1.pos.sub(thing2.pos)
        mag = vec.mag()
        if (mag < thing1.size || mag < thing2.size):
            #determine damage
            thing1.vel
            

        
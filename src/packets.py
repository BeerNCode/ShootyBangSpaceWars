
import json

class Map():

class State():
    def __init__(self, ships, bullets):
        

class Ship():
     def __init__(self, pos, id, energy, damage):

class Bullet():
     def __init__(self, pos):

class Position():
     def __init__(self, x, y, angle):
         self.x = x
         self.y = y
         self.angle = angle



class Controls():
    def __init__(self, left = False, right = False, forward = False, shoot = False):
        self.left = left
        self.right = right
        self.forward = forward
        self.shoot = shoot
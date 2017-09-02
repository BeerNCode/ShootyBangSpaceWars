
import json
import random 

class Map():

class State():
    def __init__(self, ships, bullets):
        self.ships = ships
        self.bullets = bullets
        

class Ship():

    @staticmethod
    def toPacket(ship):
        pos = Position.toPacket(ship.pos.x,ship.pos.y, ship.rpos)
        vel = Position.toPacket(ship.vel.x,ship.vel.y, 0)
        id = "a"
        energy = ship.energy
        damage = ship.hull
        return Ship(pos,vel,id,energy,damage)

    def __init__(self, pos, vel, id, energy, damage):
         self.pos = pos
         self.vel = vel
         self.id = id
         self.energy = energy
         self.damage = damage

class Bullet():

    @staticmethod
    def toPacket(slug):
        return Bullet(Position.toPacket(slug.pos,slug.rpos),Position.toPacket(slug.vel,0))

    def __init__(self, pos, vel):
         self.pos = pos
         self.vel = vel


class Position():

    @staticmethod
    def toPacket(pos,rpos):
        return Position(pos.x,pos.y,pos.rpos)

    def __init__(self, x, y, angle):
         self.x = x
         self.y = y
         self.angle = angle

class Planet():

    @staticmethod
    def toPacket(planet):
        pos = Position(planet.pos.x,planet.pos.y,0)
        return Planet(pos,planet.mass,planet.radius,planet.type)

    def __init__(self,pos,mass,radius,type):
        self.pos = pos
        self.mass = mass
        self.radius = radius
        self.type = type

    






class Controls():
    def __init__(self, left=False, right=False, forward=False, shoot=False):
        self.left = left
        self.right = right
        self.forward = forward
        self.shoot = shoot
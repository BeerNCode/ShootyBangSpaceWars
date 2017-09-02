
import json
import random 

class Map():

    def __init__(self, planets):
        self.planets = planets

    @staticmethod
    def toPacket(planets):
        packagePlanets = []
        for planet in planets:
            packagePlanets.append(Planet.toPacket(planet))
        return Map(packagePlanets)

    def toJSON(self):
        return json.JSONEncoder().encode(self)

class State():
    def __init__(self, ships, slugs):
        self.ships = ships
        self.slugs = slugs
        
    def toJSON(self):
        jships = []
        for ship in self.ships:
            jships.append(ship.toJSON())
        jslugs = []
        for slug in self.slugs:
            jslugs.append(slug.toJSON())
        return json.JSONEncoder().encode({"ships":jships, "slugs":jslugs})

class Ship():
    def __init__(self, pos, vel, id, energy, damage):
         self.pos = pos
         self.vel = vel
         self.id = id
         self.energy = energy
         self.damage = damage

    def toJSON(self):
        return json.JSONEncoder().encode(self)

    @staticmethod
    def toPacket(ship):
        id = "a"
        pos = Position.toPacket(ship.pos.x,ship.pos.y, ship.rpos)
        vel = Position.toPacket(ship.vel.x,ship.vel.y, 0)
        energy = ship.energy
        damage = ship.hull
        return Ship(pos,vel,id,energy,damage)


class Slug():

    def __init__(self, pos, vel):
         self.pos = pos
         self.vel = vel

    @staticmethod
    def toPacket(slug):
        return Bullet(Position.toPacket(slug.pos,slug.rpos),Position.toPacket(slug.vel,0))

class Position():
    def __init__(self, x, y, angle):
         self.x = x
         self.y = y
         self.angle = angle

    @staticmethod
    def toPacket(pos,rpos):
        return Position(pos.x,pos.y,pos.rpos)

class Planet():

    def __init__(self,pos,mass,radius,type):
        self.pos = pos
        self.mass = mass
        self.radius = radius
        self.type = type

    @staticmethod
    def toPacket(planet):
        pos = Position(planet.pos.x,planet.pos.y,0)
        return Planet(pos,planet.mass,planet.radius,planet.type)

class Controls():
    def __init__(self, left=False, right=False, forward=False, shoot=False):
        self.left = left
        self.right = right
        self.forward = forward
        self.shoot = shoot

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
        jplanets = []
        for planet in self.planets:
            jplanets.append(planet.toJSON())
        return json.JSONEncoder().encode({"type":"map","planets":jplanets})

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
        return json.JSONEncoder().encode({"type":"update","ships":jships, "slugs":jslugs})

class Ship():
    def __init__(self, pos, vel, name, energy, damage):
         self.pos = pos
         self.vel = vel
         self.name = name
         self.energy = energy
         self.damage = damage

    def toJSON(self):
        return {"pos":self.pos.toJSON(),"vel":self.vel.toJSON(),"name":self.name,"energy":self.energy,"damage":self.damage}

    @staticmethod
    def toPacket(ship):
        name = ship.name
        pos = Position.toPacket(ship.pos, ship.rpos)
        vel = Position.toPacket(ship.vel, 0)
        energy = ship.energy
        damage = ship.hull
        return Ship(pos,vel,name,energy,damage)


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

    def toJSON(self):
        return {"x":self.x,"y":self.y,"r":self.angle}

    @staticmethod
    def toPacket(pos,rpos):
        return Position(pos.x,pos.y,rpos)

class Planet():
    def __init__(self,pos,mass,radius,ptype):
        self.pos = pos
        self.mass = mass
        self.radius = radius
        self.ptype = ptype

    def toJSON(self):
        return {"pos":self.pos.toJSON(),"mass":self.mass,"radius":self.radius,"type":self.ptype}

    @staticmethod
    def toPacket(planet):
        pos = Position(planet.pos.x,planet.pos.y,0)
        return Planet(pos,planet.mass,planet.radius,planet.ptype)

class Controls():
    def __init__(self, left=False, right=False, up=False, down=False, space=False):
        self.left = left
        self.right = right
        self.up = up
        self.down = down
        self.space = space

    def toJSON(self):
        return json.JSONEncoder().encode({"up":self.up, "down":self.down, "left":self.left, "right":self.right, "space":self.space})
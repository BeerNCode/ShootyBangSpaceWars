from vector import Vector 
from thing import Thing

class Spline(Thing):
    """ Reticulatable splines!"""
    
    def __init__(self,thing,gravityObjects):
    """ Construcz """
    self.pos = thing.pos
    self.vel = thing.vel
    self.gravityObjects = thing.gravityObjects
    self.radius = thing.radius
    
    def get_prediction(self,dots)
        count = 0
        tempVel = self.vel
        tempPos =self.pos
        splinePoints = []
        while (count<dots):
            acc = Vector(0,0)
            for thing in self.gravityObjects:
                separation = thing.pos.sub(self.pos)
                m = separation.mag()
                if (m < thing.radius+self.radius):
                    m = self.radius+thing.radius
                acc = acc.add(separation.normalise().mult(1/(m*m)).mult(thing.mass))
            tempVel = tempVel.add(acc)
            tempPos = tempPos.add(tempVel)
            splinePoints.append(tempPos)
        return splinePoints
            
            
            
            
            
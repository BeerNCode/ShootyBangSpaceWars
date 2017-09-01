import math

class Vector:
    """ simple vector class """

    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def add(self, other):
        return Vector(self.x+other.x, self.y+other.y)

    def sub(self, other):
        return Vector(self.x-other.x, self.y-other.y)

    def mult(self, value):
        return Vector(self.x*value, self.y*value)

    def mag(self):
        return math.sqrt(self.x*self.x + self.y*self.y)
    
    def normalise(self):
        return self.mult(self, 1/math.sqrt(self.x*self.x + self.y*self.y))

    def angle(self):
        """ returns the angle between (1, 0) and this vector """
        return math.atan2(self.x, self.y)

    def dot(self,other):
        return self.x*other.x+self.y*other.y

    def cross(self,other):
        return self.x*other.y - self.y*other.x
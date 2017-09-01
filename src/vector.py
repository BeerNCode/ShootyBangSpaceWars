class Vector:
    self.x = 0
    self.y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def add(self, other):
        return Vector(self.x+other.x, self.y+other.y)

    def sub(self, other):
        return Vector(self.x-other.x, self.y-other.y)
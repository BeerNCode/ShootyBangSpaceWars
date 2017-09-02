

class Limits():

    def __init__(min_point, max_point):
        self.min_point = min_point
        self.max_point = max_point

    def contains(self, pos):
        if (pos.x < self.min_point.x):
            return False
        if (pos.y < self.min_point.y):
            return False
        if (pos.x > self.max_point.x):
            return False
        if (pos.y > self.max_point.y):
            return False
        return True
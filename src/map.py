# planets
## mass, radius, atmosphere, density, mineral
## position

# stars
## brightness
## etc

class Map():
    def __init__(self, width, height):
        self.width = width
        self.height = height
    @staticmethod
    def load(filePath):
        f = open(filePath, 'r')
        m = Map(1000, 1000)

from vector import Vector 

class Ship:
    """ Ship It """
    self.pos = Vector(0, 0)
    self.vel = Vector(0, 0)
    self.rpos = 0
    self.rvel = 0

    def __init__(self):
        """ Construcz """

    def update(self):
        self.pos.add(self.vel)

    def update_gravity(self, masses):
        self.force.add(Vector(0, 0))

    def show(self, screen):
        pygame.draw.ellipse(screen, WHITE, [x, 20, 250, 100], 2)

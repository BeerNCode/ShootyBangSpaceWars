

class Planet():
    """ A large object which can impart gravity onto stuff """

    def __init__(self, radius, mass, pos):
        self.pos = pos
        self.radius = radius
        self.mass = mass

    def show(self, screen):
        pygame.draw.ellipse(screen, (182, 52, 18), [100, 100, 250, 100], 2)
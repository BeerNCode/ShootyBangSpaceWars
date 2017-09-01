
class Thing:
    """ A thing with mass and physical properties """

    self.pos = Vector(0, 0)
    self.vel = Vector(0, 0)
    self.rpos = 0
    self.rvel = 0
    self.mass = 0

    def __init__(self):
        """ Construcz """

    def update(self):
        self.pos.add(self.vel)
        self.rpos.add(self.rvel)

    def update_gravity(self, masses):
        acc = vector(0,0)
        for thing in masses:
            separation = thing.pos - self.pos
            acc.add(thing.mass * separation.normalise()/(separation.mag*separation.mag))
        self.vel.add(acc)

    def show(self, screen):
        pygame.draw.ellipse(screen, WHITE, [x, 20, 250, 100], 2)

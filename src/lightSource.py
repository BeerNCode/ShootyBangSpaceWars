from vector import Vector

class LightSource():
    """wow"""

    def __init__(self, pos, intensity):
        self.position = pos
        self.intensity = intensity

    def get_energy(self, shippos):
        separation = (self.position.sub(shippos)).mag()
        energy = self.intensity/(separation*separation)
        return energy
import pygame

WHITE = (255, 255, 255)

class Planet(pygame.sprite.Sprite):
    """ A large object which can impart gravity onto stuff """

    def __init__(self, radius, mass, pos):
        super().__init__()
        self.pos = pos
        self.radius = radius
        self.mass = mass
        self.sprites = {}
        self.add_sprite("base", "../img/sprite.png", WHITE)
        self.set_sprite("base")
        self.image = self.original_image
        self.rect = self.image.get_rect()

    def add_sprite(self, id, filePath, background):
        sp = pygame.image.load(filePath).convert()
        sp = pygame.transform.rotate(sp, -90)
        sp.set_colorkey(background)
        self.sprites[id] = sp

    def set_sprite(self, id):
        self.original_image = self.sprites[id]

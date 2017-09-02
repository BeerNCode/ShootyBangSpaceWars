import pygame

WHITE = (255, 255, 255)
TRANSPARENT = (0,0,0,0)

class Planet(pygame.sprite.Sprite):
    """ A large object which can impart gravity onto stuff """

    def __init__(self, radius, mass, pos):
        super().__init__()
        self.pos = pos
        self.radius = radius
        self.mass = mass
        self.sprites = {}
        self.add_sprite("base", "../img/planets.png",WHITE)
        self.set_sprite("base")
        self.image = self.original_image
        self.rect = self.image.get_rect()

    def add_sprite(self, id, filePath, background):
        sp = pygame.image.load(filePath).convert()
        sp.set_clip(pygame.Rect(5, 70, 60, 60)) #Locate the sprite 
        sp = sp.subsurface(sp.get_clip()) 
        sp = pygame.transform.rotate(sp, -90)
        sp.set_colorkey(background)
        self.sprites[id] = sp

    def set_sprite(self, id):
        self.original_image = self.sprites[id]

    def update(self):
        self.rect = self.image.get_rect()
        self.rect.x = self.pos.x-self.rect.width/2
        self.rect.y = self.pos.y-self.rect.height/2

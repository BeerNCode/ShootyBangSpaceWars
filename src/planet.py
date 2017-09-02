import pygame
import random

WHITE = (255, 255, 255)
TRANSPARENT = (0,0,0,0)
PLANETS = {
    'ASTEROID':pygame.Rect(0,0,65,65),
    'MERCURY':pygame.Rect(65,0,65,65),
    'VENUS':pygame.Rect(135,0,65,65),
    'EARTH':pygame.Rect(0,65,65,65),
    'MARS':pygame.Rect(65,65,65,65),
    'JUPITER':pygame.Rect(135,65,65,65),
    'SUN': pygame.Rect(200,0,130,130),
    'P1': pygame.Rect(0,135,65,65),
    'P2': pygame.Rect(65,135,65,65),
    'P3': pygame.Rect(135,135,65,65),
    'P4': pygame.Rect(0,135,65,65),
    'P5': pygame.Rect(65,135,65,65),
    'P6': pygame.Rect(135,135,65,65)
}


class Planet(pygame.sprite.Sprite):
    """ A large object which can impart gravity onto stuff """

    def __init__(self, radius, mass, pos):
        super().__init__()
        self.pos = pos
        self.radius = radius
        self.mass = mass
        self.type = random.choice(list(PLANETS.keys()))
        self.sprites = {}
        self.add_sprite("base", "../img/planets_transparent.png",WHITE)
        self.set_sprite("base")
        self.image = self.original_image
        self.rect = self.image.get_rect()

    def add_sprite(self, id, filePath, background):
        sp = pygame.image.load(filePath).convert_alpha()
        sp.set_clip(PLANETS[self.type]) #Locate the sprite
        sp = sp.subsurface(sp.get_clip()) 
        #sp = pygame.transform.rotate(sp, 0)
        sp = pygame.transform.scale(sp,[int(round(self.radius * 2)),int(round(self.radius * 2))])
        sp.set_colorkey(background)
        self.sprites[id] = sp

    def render(self, viewport):
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.x = (self.pos.x-self.rect.width/2) - viewport.getMidPoint().x + viewport.width/2
        self.rect.y = (self.pos.y-self.rect.height/2) - viewport.getMidPoint().y + viewport.height/2

    def set_sprite(self, id):
        self.original_image = self.sprites[id]

    def update(self):
        self.rect = self.image.get_rect()
        self.rect.x = self.pos.x - self.rect.width / 2
        self.rect.y = self.pos.y - self.rect.height / 2

import pygame
from vector import Vector 

class RenderablePoint(pygame.sprite.Sprite):
    """A thing with mass and physical properties"""

    def __init__(self,pos):
        """Construcz"""
        super().__init__()
        self.pos = pos
        self.original_image = pygame.image.load("../img/whitepixel.png").convert()



    def render(self, viewport):
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.x = (self.pos.x-self.rect.width/2) - viewport.getMidPoint().x + viewport.width/2
        self.rect.y = (self.pos.y-self.rect.height/2) - viewport.getMidPoint().y + viewport.height/2
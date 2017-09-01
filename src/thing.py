import pygame

class Thing(pygame.sprite.Sprite):
    """ A thing with mass and physical properties """
    
    def __init__(self):
        super().__init__()
        
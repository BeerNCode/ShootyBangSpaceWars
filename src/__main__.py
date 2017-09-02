import pygame
import time
import math
import random
import sys
from ship import Ship
from planet import Planet
from vector import Vector
from time import sleep
from damage import Damage
from slug import Slug
from limits import Limits

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

pygame.init()

FONTS = {}
FONTS["title"] = pygame.font.SysFont('Calibri', 25, True, False)
font = pygame.font.SysFont('Calibri', 25, True, False) # This will be deprecated and replaced with a dictionary of fonts for the theme

clock = pygame.time.Clock()
pygame.display.set_caption("Shooty Bang Space Wars")
size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(size, pygame.RESIZABLE)

class Program():

    def __init__(self, server):
        if server:
            print("Running in SERVER mode")
        else:
            print("Running in CLIENT mode")
        self.server = server
        self.ships = []
        self.slugs = []
        self.planets = []
        self.frames = 0
        self.map_limits = Limits(Vector(0, 0), Vector(5000, 5000))
        self.running = True
        
        if server:
            for i in range(0,3):
                self.planets.append(Planet(20, 400, Vector(random.random()*SCREEN_WIDTH, random.random()*SCREEN_HEIGHT)))
        else:
            self.player = Ship()
            self.ships.append(self.player)

    def run(self):
        while self.running:
            print("Loop: "+str(self.frames))
            self.updateEvents()    
            self.updateShips()
            self.updateSlugs()
            self.render()
            
            if not self.server:
                screen.blit(font.render(str(self.frames), True, WHITE), [SCREEN_WIDTH-100, 10])
                screen.blit(font.render(str(self.player.damage), True, WHITE), [SCREEN_WIDTH-100, 20])

            pygame.display.flip()
            self.frames+=1
            clock.tick(30)
        pygame.quit()

    def updateEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Quitting the game")
                self.running = False
                screen.fill(WHITE)
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h),
                                                  pygame.RESIZABLE) 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                    screen.fill(WHITE)

    def render(self):
        screen.fill(BLACK)
        sprites = pygame.sprite.Group()
        for ship in self.ships:
            sprites.add(ship)
        for slug in self.slugs:
            sprites.add(slug)
        for planet in self.planets:
            planet.update()
            sprites.add(planet)
        sprites.draw(screen)

    def updateShips(self):
        for ship in self.ships:
            ship.update_gravity(self.planets)
            for planet in self.planets:
                Damage.determineThingPlanetDamage(ship, planet)
            newSlugs = ship.update()
            for slug in newSlugs:
                self.slugs.append(slug)

    def updateSlugs(self):
        for slug in self.slugs:
            slug.update_gravity(self.planets)
            if not self.map_limits.contains(slug.pos):
                self.slugs.remove(slug)
            for planet in self.planets:
                vec = slug.pos.sub(planet.pos)
                mag = vec.mag()
                if mag < planet.radius:
                    self.slugs.remove(slug)
            slug.update()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        server = sys.argv[1] == "server"
    else:
        server = False
    p = Program(server)
    p.run()
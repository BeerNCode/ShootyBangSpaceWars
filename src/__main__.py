import pygame
import time
import math
import random
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
 
size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("Shooty Bang Space Wars")

clock = pygame.time.Clock()
done = False
planets = []
for i in range(0,3):
    planets.append(Planet(20, 100, Vector(random.random()*SCREEN_WIDTH, random.random()*SCREEN_HEIGHT)))

ships = []
slugs = []
map_limits = Limits(Vector(0, 0), Vector(5000, 5000))

ship = Ship()
ships.append(ship)
for i in range(0,2):
    planets.append(Planet(random.random()*50+50, 100, Vector(random.random()*SCREEN_WIDTH, random.random()*SCREEN_HEIGHT)))

frames = 0
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            screen.fill(WHITE)
    
    # Update the game physics
    # for ship in ships:
        # ship.update_gravity()

    # Update the game state and prepare the sprites
    screen.fill(BLACK)
    sprites = pygame.sprite.Group()
    for ship in ships:
        ship.update_gravity(planets)
        for planet in planets:
            Damage.determineThingPlanetDamage(ship,planet)
        ship.update()
        newSlugs = ship.update()
        for slug in newSlugs:
            slugs.append(slug)
        # pygame.draw.line(screen, GREEN, [ship.pos.x, ship.pos.y], [ship.pos.x+math.cos(ship.rpos)*100, ship.pos.y+math.sin(ship.rpos)*100])
        sprites.add(ship)

    for slug in slugs:
        slug.update_gravity(planets)

        if not map_limits.contains(slug.pos):
            slugs.remove(slug)
        for planet in planets:
            vec = slug.pos.sub(planet.pos)
            mag = vec.mag()
            if mag < planet.radius:
                slugs.remove(slug)
        slug.update()
        sprites.add(slug)

    for planet in planets:
        planet.update()
        sprites.add(planet)

    sprites.draw(screen)

    font = pygame.font.SysFont('Calibri', 25, True, False)
    screen.blit(font.render(str(frames), True, WHITE), [SCREEN_WIDTH-100, 10])
    screen.blit(font.render(str(ship.damage), True, WHITE), [SCREEN_WIDTH-100, 20])

    pygame.display.flip()
    frames+=1
    clock.tick(30)
 
pygame.quit()
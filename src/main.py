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

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

pygame.init()
 
size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(size, pygame.RESIZABLE)
 
pygame.display.set_caption("Shooty Bang Space Wars")


clock = pygame.time.Clock()

x = 0

done = False

planets = []
for i in range(0,2):
    planets.append(Planet(50, 1000, Vector(random.random()*SCREEN_WIDTH, random.random()*SCREEN_HEIGHT)))

ships = []
slugs = []
ship = Ship()
ships.append(ship)

frames = 0
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            screen.fill(WHITE)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
                screen.fill(WHITE)
        if event.type == pygame.VIDEORESIZE:
            # The main code that resizes the window:
            # (recreate the window with the new size)
            screen = pygame.display.set_mode((event.w, event.h),
                                              pygame.RESIZABLE)
            
    
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
        pygame.draw.line(screen, GREEN, [ship.pos.x, ship.pos.y], [ship.pos.x+math.cos(ship.rpos)*100, ship.pos.y+math.sin(ship.rpos)*100])
        sprites.add(ship)

    for slug in slugs:
        slug.update_gravity(planets)
        slug.update()
        sprites.add(slug)

    for planet in planets:
        planet.show(screen)

    sprites.draw(screen)

    font = pygame.font.SysFont('Calibri', 25, True, False)
    text = font.render(str(frames), True, WHITE)
    screen.blit(text, [SCREEN_WIDTH-100, 10])

    pygame.display.flip()
    frames+=1
    clock.tick(30)
 
pygame.quit()
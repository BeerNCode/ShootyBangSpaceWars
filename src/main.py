import pygame
import time
import random
from ship import Ship
from planet import Planet
from vector import Vector
from time import sleep

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

pygame.init()
 
size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("Shooty Bang Space Wars")

clock = pygame.time.Clock()

x = 0

done = False

planets = []
for i in range(0,10):
    planets.append(Planet(100, 10, Vector(random.random()*SCREEN_WIDTH, random.random()*SCREEN_HEIGHT)))

ships = []
ship = Ship()
ships.append(ship)

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
    group = pygame.sprite.Group()
    for ship in ships:
        ship.update()
        group.add(ship)

    for planet in planets:
        planet.show(screen)

    group.draw(screen)

    font = pygame.font.SysFont('Calibri', 25, True, False)
    text = font.render(str(frames), True, WHITE)
    screen.blit(text, [SCREEN_WIDTH-100, 10])

    pygame.display.flip()
    frames+=1
    clock.tick(30)
 
pygame.quit()
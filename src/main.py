import pygame
import time
from ship import Ship
from planet import Planet
from vector import Vector
from time import sleep

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

pygame.init()
 
size = (700, 500)
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("Shooty Bang Space Wars")

clock = pygame.time.Clock()

x = 0

done = False

planets = []
for i in range(0,10):
    planets.append(Planet(10, 10, Vector(500, 500)))

ships = []
ships.append(Ship())

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            screen.fill(WHITE)
    
    screen.fill(BLACK)

    # Update the game physics
    # for ship in ships:
        # ship.update_gravity()

    # Update the game state and prepare the sprites
    group = pygame.sprite.Group()
    for ship in ships:
        ship.update()
        group.add(ship)

    for planet in planets:
        planet.show(screen)

    group.draw(screen)

    # font = pygame.font.SysFont('Calibri', 25, True, False)
    # text = font.render("Shooter Bang Space Wars", True, WHITE)
    # screen.blit(text, [250, 250])

    # pygame.draw.ellipse(screen, WHITE, [x, 20, 250, 100], 2)
    # x += 1
    pygame.display.flip()
    # sleep(0.2)
 
    clock.tick(30)
 
pygame.quit()
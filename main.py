import pygame
from ship import Ship

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
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            screen.fill(WHITE)
    
    pygame.draw.line(screen, GREEN, [0, 0], [100, 100], 5)

    font = pygame.font.SysFont('Calibri', 25, True, False)
    text = font.render("Shooter Bang Space Wars", True, WHITE)
    screen.blit(text, [250, 250])

    pygame.draw.ellipse(screen, WHITE, [x, 20, 250, 100], 2)
    x += 1
    pygame.display.flip()
 
    clock.tick(60)
 
pygame.quit()
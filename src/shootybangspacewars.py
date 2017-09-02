import pygame
from pygame.locals import*
import os
import subprocess
import time
img = pygame.image.load('..' + os.sep + 'img' + os.sep +  'MenuBackdropWithButtons.png')


screen = pygame.display.set_mode((img.get_width(), img.get_height()))
pygame.display.set_caption("Shooty Bang Space Wars")

running = 1
baseCommand = "pythonw"

while running:
    screen.blit(img,(0,0))
    pygame.display.flip()
    ev = pygame.event.get()

    for event in ev:
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()

            if (pos[0] > 422 and pos[0] < 557 and pos[1] > 338 and pos[1] < 387):
				#host
                print("Host da game!")
                p = subprocess.Popen([baseCommand, '__main__.py' ,'server'])
                quit()
            if (pos[0] > 422 and pos[0] < 557 and pos[1] > 451 and pos[1] < 500):
				#join
                p = subprocess.Popen([baseCommand, '__main__.py'])
                quit()
        if event.type == pygame.QUIT:
                quit()
    time.sleep(.1);
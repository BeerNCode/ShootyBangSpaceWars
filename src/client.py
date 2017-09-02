# client.py
# Shooty Bang Space Wars - Client

import socket
import pygame
import random
from threading import Thread

HOST = 'localhost'              
PORT = 50007                 
SCREEN_WIDTH = 800              
SCREEN_HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

pygame.init()
size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
font = pygame.font.SysFont('Calibri', 25, True, False)
planets = []
ships = []
slugs = []
frames = 0

pygame.display.set_caption("Shooty Bang Space Wars")
# Connect to the server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
def update():
    """ Listens to the server for updates to the world """
    while True:
        data = s.recv(1024)
        print('Received:', str(repr(data)))
updateThread = Thread(target=update)
connected = False
quit = False

while not quit:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           quit = True
           screen.fill(WHITE)
           pygame.quit()
           sock.close()
           break
    if quit:
        break

    # If not connected, connect
    if not connected:
        screen.blit(font.render("NOT CONNECTED", True, WHITE), [SCREEN_WIDTH-100, 10])
        try:
            sock.connect((HOST, PORT))
            screen.blit(font.render("CONNECTED (:", True, WHITE), [SCREEN_WIDTH-100, 10])
            connected = True
        except:
            screen.blit(font.render("AH SHEEETZ CANNEE CUNECT", True, WHITE), [random.random()*SCREEN_WIDTH, random.random()*SCREEN_HEIGHT])
    else:
        # Handle user input
        keys=pygame.key.get_pressed()
        sock.send(bytes('SHIT SON', 'UTF-8'))
        # Render the screen
        
        screen.fill(BLACK)
        sprites = pygame.sprite.Group()
        for slug in slugs:
            sprites.add(slug)
        for planet in planets:
            planet.show(screen)
            sprites.draw(screen)
    
    text = font.render(str(frames), True, WHITE)
    screen.blit(text, [SCREEN_WIDTH-100, 10])
    pygame.display.flip()
    frames+=1
    clock.tick(30)



    
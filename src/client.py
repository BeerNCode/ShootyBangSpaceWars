# client.py
# Shooty Bang Space Wars - Client

import socket
import pygame


HOST = 'localhost'              
PORT = 50007                 
SCREEN_WIDTH = 800              
SCREEN_HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect():
    s.connect((HOST, PORT))
    s.send(bytes('Hello, world', 'UTF-8'))

    while True:
        data = s.recv(1024)
        print('Received', repr(data))

def disconnect():
    s.close()

connect()
# pygame.init()
# size = (SCREEN_WIDTH, SCREEN_HEIGHT)
# screen = pygame.display.set_mode(size)
# pygame.display.set_caption("Shooty Bang Space Wars")
# clock = pygame.time.Clock()

# planets = []
# ships = []
# frames = 0
# while not done:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             done = True
#             screen.fill(WHITE)

#     for bullet in bullets:
#         sprites.add(bullet)

#     for planet in planets:
#         planet.show(screen)

#     sprites.draw(screen)

#     font = pygame.font.SysFont('Calibri', 25, True, False)
#     text = font.render(str(frames), True, WHITE)
#     screen.blit(text, [SCREEN_WIDTH-100, 10])

#     pygame.display.flip()
#     frames+=1
#     clock.tick(30)
 
# pygame.quit()

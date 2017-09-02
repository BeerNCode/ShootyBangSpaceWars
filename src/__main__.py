import pygame
import time
import math
import random
import sys
import socket
from client import Client
from threading import Thread
from ship import Ship
from planet import Planet
from vector import Vector
from time import sleep
from damage import Damage
from slug import Slug
from limits import Limits

pygame.init()

class Colours:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)

class Fonts:
    pygame.font.init()
    TITLE = pygame.font.SysFont('Calibri', 25, True, False)

class Program:

    SCREEN_WIDTH = 1024
    SCREEN_HEIGHT = 768

    pygame.display.set_caption("Shooty Bang Space Wars")

    def __init__(self, server):
        if server:
            print("Running in SERVER mode")
        else:
            print("Running in CLIENT mode")
        self.clock = pygame.time.Clock()
        size = (Program.SCREEN_WIDTH, Program.SCREEN_HEIGHT)
        self.screen = pygame.display.set_mode(size, pygame.RESIZABLE)
        self.server = server
        self.ships = []
        self.slugs = []
        self.planets = []
        self.frames = 0
        self.map_limits = Limits(Vector(0, 0), Vector(5000, 5000))
        self.running = True
        
        if self.server:
            self.loadMap()
            self.clients = []
            self.newClientsThread = Thread(target=self.listenForNewClients)
            self.newClientsThread.start()
        else:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.listenThread = Thread(target=self.listenToServer)
            self.listenThread.start()
            self.player = Ship()
            self.ships.append(self.player)
            # Need to get the map from the server
    def loadMap(self):
            for iq in range(0,3):
                self.planets.append(Planet(random.random()*100+50, 400, Vector(random.random()*Program.SCREEN_WIDTH, random.random()*Program.SCREEN_HEIGHT)))

    def run(self):
        while self.running:

            print("Step: "+str(self.frames))
            self.updateEvents()    
            if not self.running:
                break
            self.updateShips()
            self.updateSlugs()
            self.render()
            
            if not self.server:
                self.screen.blit(Fonts.TITLE.render(str(self.frames), True, Colours.WHITE), [Program.SCREEN_WIDTH-100, 10])
                self.screen.blit(Fonts.TITLE.render(str(self.player.damage), True, Colours.WHITE), [Program.SCREEN_WIDTH-100, 20])

            pygame.display.flip()
            self.frames+=1
            self.clock.tick(30)
        pygame.quit()

    def listenToServer(self):
        """ Listens to the server for updates to the world """
        while True:
            data = self.sock.recv()
            print('Received:', str(repr(data)))
            # Update the model with other
            # add new ships
            # update positions
            # 

    def listenForNewClients(self):
        while True:
            conn, addr = self.socket.accept()
            clients.append(Client(conn, addr))
            print("Connection from [",addr,"]")
            while True:
                data = conn.recv(1024)
                if not data: 
                    break

    def updateClients(self):
        """ Send packets to the clients """
        # for client in self.clients:


    def updateEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Quitting the game")
                self.running = False
                self.screen.fill(Colours.WHITE)
            if event.type == pygame.VIDEORESIZE:
                self.screen = pygame.display.set_mode((event.w, event.h),
                                                  pygame.RESIZABLE) 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                    self.screen.fill(Colours.WHITE)

    def render(self):
        self.screen.fill(Colours.BLACK)
        sprites = pygame.sprite.Group()
        for ship in self.ships:
            ship.show(self.screen)
            sprites.add(ship)
        for slug in self.slugs:
            sprites.add(slug)
        for planet in self.planets:
            planet.update()
            sprites.add(planet)
        sprites.draw(self.screen)

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
                Damage.determineThingPlanetDamage(slug, planet)
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
import pygame
import time
import math
import random
import sys
import socket
from client import Client
from threading import Thread
from ship import Ship
from spline import Spline
from planet import Planet
from lightSource import LightSource
from vector import Vector
from time import sleep
from damage import Damage
from slug import Slug
from limits import Limits
from viewport import Viewport
import globals

pygame.init()

class Program:

    SCREEN_WIDTH = 1024
    SCREEN_HEIGHT = 768
    GAME_SPEED = 30
    HOST = "localhost"
    PORT = 15007

    pygame.display.set_caption("Shooty Bang Space Wars")

    screenSize = (SCREEN_WIDTH, SCREEN_HEIGHT)
    screen = pygame.display.set_mode(screenSize, pygame.RESIZABLE)

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
        self.lightSources = []
        self.frames = 0
        self.map_limits = Limits(Vector(0, 0), Vector(globals.MAP_WIDTH, globals.MAP_HEIGHT))
        self.running = True
        self.viewport = Viewport(Vector(self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT/2), self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        globals.MAP_WIDTH = self.SCREEN_WIDTH
        globals.MAP_HEIGHT = self.SCREEN_HEIGHT
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        if self.server:
            for iq in range(0,3):
                self.planets.append(Planet(20, 400, Vector(random.random()*globals.MAP_WIDTH, random.random()*globals.MAP_HEIGHT)))
            self.loadMap()
            self.clients = []
            self.newClientsThread = Thread(target=self.listenForNewClients)
            self.newClientsThread.start()
        else:
            self.listenThread = Thread(target=self.listenToServer)
            self.listenThread.start()
            self.player = Ship()
            self.ships.append(self.player)
            for iq in range(0,3):
                self.planets.append(Planet(random.random()*100+50, 400, Vector(random.random()*Program.SCREEN_WIDTH, random.random()*Program.SCREEN_HEIGHT)))
            self.lightSources.append(LightSource(Vector(300,300),1000))
            # Need to get the map from the server
    def loadMap(self):
            for iq in range(0,3):
                self.planets.append(Planet(random.random()*100+50, 400, Vector(random.random()*Program.SCREEN_WIDTH, random.random()*Program.SCREEN_HEIGHT)))
            self.lightSources.append(LightSource(Vector(100,100),1))

    def run(self):
        while self.running:
            print("Step: "+str(self.frames))
            self.updateEvents()
            if not self.running:
                break
            
            if (self.server):
                self.updateClients()
            self.updateShips()
            self.updateSlugs()
            self.render()
            
            if not self.server:
                self.screen.blit(globals.Fonts.TITLE.render(str(self.frames), True, globals.WHITE), [self.SCREEN_WIDTH-100, 10])
                self.screen.blit(globals.Fonts.TITLE.render(str(self.player.damage), True, globals.WHITE), [self.SCREEN_WIDTH-100, 40])

            pygame.display.flip()
            self.frames+=1
            self.clock.tick(Program.GAME_SPEED)
        pygame.quit()

    def listenToServer(self):
        """ Listens to the server for updates to the world """
        print("CLIENT: Listening to server for updates")
        self.socket.connect((Program.HOST, Program.PORT))
        while True:
            data = self.socket.recv(1024)
            if not data == None:
                print('Received data from SERVER:', str(data.decode("utf-8")))

    def listenForNewClients(self):
        self.socket.bind((Program.HOST, Program.PORT))
        self.socket.listen(5)
        while True:
            conn, addr = self.socket.accept()
            self.clients.append(Client(conn, addr))
            print("Just had a connection from [",addr,"]")

    def updateClients(self):
        """ Send packets to the clients """
        for client in self.clients:
            print("Pretending to send a packet to client BOOP")

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
        self.screen.fill(globals.BLACK)
        sprites = pygame.sprite.Group()
        self.viewport.updateMidPoint(self.player.pos)
        for idx, ship in enumerate(self.ships):
            ship.render(self.viewport)
            path = Spline(ship,self.planets)
            splinePoints = path.get_prediction(60)
            for Vector in splinePoints:
                pygame.draw.rect(self.screen, globals.WHITE, [Vector.x, Vector.y, 1, 1], 0)
            ship.showStatus(self.screen, idx)
            sprites.add(ship)
        for slug in self.slugs:
            slug.render(self.viewport)
            sprites.add(slug)
        for planet in self.planets:
            planet.render(self.viewport)
            planet.update()
            sprites.add(planet)
        sprites.draw(self.screen)

    def updateShips(self):
        for ship in self.ships:
            ship.update_gravity(self.planets)
            ship.update_regen(self.lightSources)
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
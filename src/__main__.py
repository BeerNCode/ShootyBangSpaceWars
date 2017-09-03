import json
import pygame
import time
import math
import random
import sys
import socket
import traceback
from sys import stdin
from client import Client
from threading import Thread
from ship import Ship
from planet import Planet
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
import packets
from spline import Spline
from lightSource import LightSource
from viewport import Viewport
import globals

pygame.init()

DEBUG = False

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
        self.map_limits = Limits(Vector(0, 0), Vector(globals.MAP_WIDTH, globals.MAP_HEIGHT))
        self.frames = 0
        self.running = True
        self.viewport = Viewport(Vector(self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT/2), self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        globals.MAP_WIDTH = self.SCREEN_WIDTH
        globals.MAP_HEIGHT = self.SCREEN_HEIGHT
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        if self.server:
            self.loadMap()
            self.clients = []
            self.newClientsThread = Thread(target=self.listenForNewClients)
            self.newClientsThread.start()
        else:
            self.player = Ship()
            self.listenThread = Thread(target=self.listenToServer)
            self.listenThread.start()
            self.lightSources.append(LightSource(Vector(300,300),1000))

    def loadMap(self):
            for iq in range(0,3):
                self.planets.append(Planet(20, 40, Vector(0.1*globals.MAP_WIDTH, 0.1*globals.MAP_HEIGHT)))
            self.lightSources.append(LightSource(Vector(100,100),1))

    def run(self):
        while self.running:
            try:
                self.updateEvents()
                if not self.running:
                    print("Breaking out the main loop")
                    break

                if self.server:
                    self.updateShips()
                    self.updateSlugs()
                    self.sendClientsUpdate()
                else:
                    self.sendServerUpdate()

                self.render()

                if not self.server:
                    self.screen.blit(globals.Fonts.TITLE.render(str(self.frames), True, globals.WHITE), [Program.SCREEN_WIDTH-100, 10])
                    self.screen.blit(globals.Fonts.TITLE.render(str(self.player.damage), True, globals.WHITE), [Program.SCREEN_WIDTH-100, 20])

                pygame.display.flip()
            except Exception:
                self.running = False
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback)
                return
            self.frames+=1
            self.clock.tick(Program.GAME_SPEED)

    def listenToServer(self):
        """ Listens to the server for updates to the world """
        print("Connecting...")
        self.socket.connect((Program.HOST, Program.PORT))
        ss = self.socket.getsockname()
        print("Listening to server for updates: ["+str(ss[0])+"]")
        self.player.name = str(ss[0])
        print("Setting ship name to :"+self.player.name)
        self.ships.append(self.player)

        while self.running:
            data = Program.readJSON(self.socket)
            if not data == None:
                decoded_data = json.JSONDecoder().decode(data)
                if decoded_data["type"] == "map":
                    self.planets.clear()
                    for jplanet in decoded_data["planets"]:
                        jpos = Vector(jplanet["pos"]["x"], jplanet["pos"]["y"])
                        self.planets.append(Planet(jplanet["radius"], jplanet["mass"],jpos, jplanet["type"]))
                elif decoded_data["type"] == "update":
                    print("Update recieved from server.")
                    jships = decoded_data["ships"]
                    newShips = []
                    for jship in jships:
                        ship = next((s for s in self.ships if s.name == jship["name"]), None)
                        if ship is None:
                            ship = Ship()
                            ship.name = jship['name']
                        else:
                            ship.pos.x = jship['pos']['x']
                            ship.pos.y = jship['pos']['y']
                            ship.rpos = jship['pos']['r']
                        newShips.append(ship)
                    self.ships = newShips

    def listenForNewClients(self):
        self.socket.bind(("localhost", Program.PORT))
        self.socket.listen(5)

        while self.running:
            self.socket.settimeout(1000)
            conn, addr = self.socket.accept()
            ship = Ship()
            ship.name = addr           
            ship.pos = Vector(random.random()*1000, random.random()*1000)
            self.ships.append(ship)
            client = Client(conn, addr, ship)
            client.listenThread = Thread(target=self.listenToClient, args=(client,))
            client.listenThread.start()
            self.clients.append(client)

            print("Just had a connection from [",addr,"]")
            data = packets.Map.toJSON(packets.Map.toPacket(self.planets))
            data = Program.sendJSON(client.conn, data)

    def listenToClient(self, client):
        print("SERVER: Listneing to clint")
        while self.running:
            data = Program.readJSON(client.conn)
            if not data is None:
                if DEBUG:
                    print(data)
                decoded_data = json.JSONDecoder().decode(data)
                client.keys = decoded_data

    def sendClientsUpdate(self):
        """ Send packets to the clients """
        packet_ships = []
        for ship in self.ships:
            packet_ships.append(packets.Ship.toPacket(ship))
        packet_slugs = []
        for slug in self.slugs:
            packet_slugs.append(packets.Slug.toPacket(slug))
        state = packets.State(packet_ships, packet_slugs)
        data = state.toJSON()
        for client in self.clients:
            Program.sendJSON(client.conn, data)

    @staticmethod
    def sendJSON(socket, data):
        try:
            db = bytes(data, "utf-8")
            l = len(db)
            lb = l.to_bytes(4, byteorder='big', signed=False)
            socket.send(lb+db)
        except:
            if DEBUG:
                print("Failed send action")

    @staticmethod
    def readJSON(socket):
        try:
            lb = socket.recv(4)
            l = int.from_bytes(lb, byteorder='big', signed=False)
            data = socket.recv(l).decode("utf-8")
            return data
        except:
            if DEBUG:
                print("Failed read action")

    def sendServerUpdate(self):
        """ Send packets from client to server """
        keys = self.player.getInputs()
        data = keys.toJSON()
        Program.sendJSON(self.socket, data)

    def updateEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Quitting the game")
                self.running = False
                self.screen.fill(globals.WHITE)
            if event.type == pygame.VIDEORESIZE:
                self.screen = pygame.display.set_mode((event.w, event.h),
                                                  pygame.RESIZABLE) 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                    self.screen.fill(globals.WHITE)

    def render(self):
        self.screen.fill(globals.BLACK)
        sprites = pygame.sprite.Group()
        if not self.server:
            self.viewport.updateMidPoint(self.player.pos)
        for idx, ship in enumerate(self.ships):
            ship.render(self.viewport)
            path = Spline(ship,self.planets)
            splinePoints = path.get_prediction(30)
            for RenderablePoint in splinePoints:
                RenderablePoint.render(self.viewport)
                sprites.add(RenderablePoint)
            sprites.add(ship)
        for slug in self.slugs:
            slug.render(self.viewport)
            sprites.add(slug)
        for planet in self.planets:
            planet.render(self.viewport)
            sprites.add(planet)
        sprites.draw(self.screen)

    def updateShips(self):
        for client in self.clients:
            ship = client.ship
            ship.setInputs(client.keys)
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

pygame.quit()
print("DONE AND DUSTED")

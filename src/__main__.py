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

    screenSize = (SCREEN_WIDTH, SCREEN_HEIGHT)
    screen = pygame.display.set_mode(screenSize, pygame.RESIZABLE)

    def __init__(self, server):
        if server:
            pygame.display.set_caption("Shooty Bang Space Wars - SERVER")
            print("Running in SERVER mode")
        else:
            pygame.display.set_caption("Shooty Bang Space Wars")
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
        self.connected = False
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
                 self.planets.append(Planet(random.random()*100+50, 100, Vector(random.random()*Program.SCREEN_WIDTH, random.random()*Program.SCREEN_HEIGHT)))
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

                if not self.server and self.frames > 1 and self.ships != None:
                    for ship in self.ships:
                        self.updateShip(ship,json.JSONDecoder().decode(self.player.getInputs().toJSON()))
                    self.updateSlugs()

                self.render()

                line = 0
                if not self.server:
                    self.screen.blit(globals.Fonts.INFO.render("Energy: "+"{:10.4f}".format(self.player.energy), True, globals.WHITE), [Program.SCREEN_WIDTH-150, line*20])
                    line+=1
                    self.screen.blit(globals.Fonts.INFO.render("Pos: "+"{:10.2f}".format(self.player.pos.x)+" "+"{:10.2f}".format(self.player.pos.y), True, globals.WHITE), 
                    [Program.SCREEN_WIDTH-150, line*20])
                    line+=1
                else:
                    for client in self.clients:    
                        self.screen.blit(globals.Fonts.INFO.render(client.addr, True, globals.WHITE), [Program.SCREEN_WIDTH-150, line*30])
                        line+=1
                self.screen.blit(globals.Fonts.INFO.render("Frame: "+str(self.frames), True, globals.WHITE), [Program.SCREEN_WIDTH-150, line*30])
                line+=1

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
        self.socket.connect((globals.network.serverIp, globals.PORT))
        #         break
        #     except:
        #         attempts+=1
        ss = self.socket.getsockname()
        print("Listening to server for updates: ["+str(ss[0])+"]")
        self.player.name = str(ss[0])
        print("Setting ship name to :"+self.player.name)
        self.ships.append(self.player)

        duffpackets = 0
        while self.running:
            try:
                data = Program.readJSON(self.socket)
                if not data == None:
                    decoded_data = json.JSONDecoder().decode(data)
                    if decoded_data["type"] == "map":
                        self.planets.clear()
                        for jplanet in decoded_data["planets"]:
                            jpos = Vector(jplanet["pos"]["x"], jplanet["pos"]["y"])
                            self.planets.append(Planet(jplanet["radius"], jplanet["mass"],jpos, jplanet["type"]))
                    elif decoded_data["type"] == "update":
                        if DEBUG:
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
                                ship.energy = jship['energy']
                            newShips.append(ship)
                        self.ships = newShips
            except Exception:
                duffpackets+=1
                print("Server sent me its "+duffpackets+" duff packet...")

    def listenForNewClients(self):
        self.socket.bind(("0.0.0.0", globals.PORT))
        self.socket.listen(5)
        self.socket.settimeout(1000)
        while self.running:
            try:
                conn, addr = self.socket.accept()
                ship = Ship()
                ship.name = addr           
                ship.pos = Vector(random.random()*1000, random.random()*1000)
                self.ships.append(ship)
                client = Client(conn, addr, ship)
                client.conn.settimeout(1000)
                client.listenThread = Thread(target=self.listenToClient, args=(client,))
                client.listenThread.start()
                self.clients.append(client)

                print("Just had a connection from [",addr,"]")
                data = packets.Map.toJSON(packets.Map.toPacket(self.planets))
                data = Program.sendJSON(client.conn, data)
            except:
                print("socket threw an exception")

    def listenToClient(self, client):
        print("SERVER: Listneing to client")
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
                Program.SCREEN_HEIGHT = event.h
                Program.SCREEN_WIDTH = event.w
                self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE) 
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
            ship.show(self.screen, not self.server)
            path = Spline(ship, self.planets)
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
            self.updateShip(client.ship,client.keys)

    def updateShip(self,ship,keys):
        ship.setInputs(keys)
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
if p.server:
    p.socket.close()
    for client in p.clients:
        client.conn.close()
print("DONE AND DUSTED")
sys.exit(0)
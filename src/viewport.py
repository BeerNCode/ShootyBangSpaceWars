from vector import Vector 
from thing import Thing
from slug import Slug
from limits import Limits
import math
import pygame
import globals

class Viewport(Limits):
        def __init__(self, midPoint, width, height):
            """Construcz"""
            self.min_point = Vector(midPoint.x - width/2, midPoint.y - height/2)
            self.max_point = Vector(midPoint.x + width/2, midPoint.y + height/2)
            super().__init__(self.min_point, self.max_point)
            self.width = width
            self.height = height
            self.unExceedify()

        def updateMidPoint(self, midPoint):
            self.min_point.x = midPoint.x - self.width/2
            self.min_point.y = midPoint.y - self.height/2
            self.max_point.x = midPoint.x + self.width/2
            self.max_point.y = midPoint.y + self.height/2
            self.unExceedify()

        def updateWidthHeight(self, width, height):
            self.width = width
            self.height = height
            self.unExceedify()

        def getMidPoint(self):
            x = (self.min_point.x + self.max_point.x) / 2
            y = (self.min_point.y + self.max_point.y) / 2
            return Vector(x,y)

        def unExceedify(self):
            
            if self.min_point.x < 0:
                self.max_point.x = self.width
                self.min_point.x = 0

            if self.min_point.y < 0:
                self.max_point.y = self.height
                self.min_point.y = 0

            if self.min_point.x > globals.MAP_WIDTH:
                self.max_point.x = globals.MAP_WIDTH
                self.min_point.x = globals.MAP_WIDTH - self.width

            if self.min_point.x > globals.MAP_HEIGHT:
                self.max_point.x = globals.MAP_HEIGHT
                self.min_point.x = globals.MAP_HEIGHT - self.height


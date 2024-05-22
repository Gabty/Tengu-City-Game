import pygame
import random as ran
from vector import Vector
from math import cos, sin


class Entity:
    
    def __init__(self,win, vector, radius,color,speed, friendly=False) -> None:
        self.radius = radius
        self.vector = vector
        self.win = win
        self.color = color
        self.speed = speed

        self.state = False # False = still / True = moving /
        self.target = None
        self.friendly = friendly 
    
    def draw(self):
        pygame.draw.circle(self.win, self.color, (self.vector.x, self.vector.y), self.radius)
        #pygame.draw.line(self.win, self.color, (self.vector.x, self.vector.y), (self.vector.x-20*self.angle, self.vector.y-20*self.angle))
    
    def shoot(self, pos):
        if self.state:
            return
        self.target = Vector(pos[0], pos[1])
        self.angle = self.vector.get_angle(self.target.get_pos())
        self.state = True
    
    def is_collision(self, vector, radius):
        dist = ((self.vector.x - vector.x)**2 + (self.vector.y - vector.y)**2)**0.5
        return dist < self.radius + radius

    def rect_collision(self, rect):
        closest_x = max(rect.vector.x, min(self.vector.x, rect.vector.x + rect.width))
        closest_y = max(rect.vector.y, min(self.vector.y, rect.vector.y + rect.width))

        dist = ((closest_x - self.vector.x)**2+(closest_y - self.vector.y)**2)**0.5
        return dist < self.radius

    def disable(self):
        self.target = None
        self.angle = None
        self.state = None
        if not self.friendly:
            self.vector.x = ran.randint(0,600)
            self.vector.y = -200
        else:
            self.vector.x = 350
            self.vector.y = 900
    def update(self):
        if self.target:
            self.vector.x += cos(self.angle) * self.speed
            self.vector.y += sin(self.angle) * self.speed
            if self.vector.get_distance(self.target.get_pos()) < 5:
                self.target = None
                self.angle = None
                self.state = None
                if not self.friendly:
                    self.vector.x = ran.randint(0,600)
                    self.vector.y = -200
                else:
                    self.vector.x = 350
                    self.vector.y = 900
        self.draw()
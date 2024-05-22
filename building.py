import pygame

class Building:
    def __init__(self,win,vector, width, height,color, health):
        self.vector = vector
        self.width = width
        self.height = height
        self.win = win
        self.color = color

        self.health = health

    def draw(self):
        pygame.draw.rect(self.win, self.color, (self.vector.x, self.vector.y, self.width, self.height))
    
    def update(self):
        if self.health > 0:
            self.draw()
    
    def midpoint(self):
        return (self.width/2, self.height/2)
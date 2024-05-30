from math import *

class Vector:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def get_pos(self):
        return self.x, self.y
    
    def get_distance(self, pos):
        return sqrt((self.x - pos[0])**2 + (self.y - pos[1])**2)

    def get_angle(self, pos):
        dx = pos[0] - self.x
        dy =  pos[1] - self.y
        angle = atan2(-dy, dx) # in radians only
        return angle
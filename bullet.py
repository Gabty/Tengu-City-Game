import pygame
from math import cos, sin, degrees


# Common Bullet
class Missile(pygame.sprite.Sprite):
    def __init__(self, image_path, speed,angle, vector,bullet_group):
        super().__init__()
        self.__image = pygame.image.load(image_path).convert_alpha()
        self.image = self.__image
        self.speed = speed
        self.vector = vector
        self.angle = angle

        self.rect = self.__image.get_rect()


        self.starting_pos = self.vector.get_pos()
        bullet_group.add(self)
    
    def draw(self, win):
        image = pygame.transform.rotate(self.__image, degrees(self.angle))
        win.blit(image, self.vector.get_pos())

    def update(self, win):
        self.vector.x += self.speed * cos(self.angle)
        self.vector.y -= self.speed * sin(self.angle)
        if self.vector.get_distance(self.starting_pos) > 400:
            self.kill()
        self.draw(win)
    
class CuteMissile(Missile):
    def __init__(self, image_path, speed, angle, vector, bullet_group):
        super().__init__(image_path, speed, angle, vector, bullet_group)




# Enemy Missile

class EnemyMissile(pygame.sprite.Sprite):
    def __init__(self):
        pass
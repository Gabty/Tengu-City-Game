import pygame
from math import cos, sin, degrees, radians
from vector import Vector
import os

import random as ran

import ship


class Explosion(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__()
        self.images = [pygame.image.load('images/explosion/'+img).convert_alpha() for img in os.listdir('images/explosion') if img.endswith('.png')]
        self.frame = 0
        self.rect = self.images[0].get_rect()
        self.rect.center = pos
        
        group.add(self)
    def draw(self, win):
        win.blit(self.images[self.frame-1], (self.rect.x, self.rect.y))
    
    def update(self, win):
        self.frame += 1
        if self.frame > len(self.images):
            self.frame = 1
            self.kill()
        self.draw(win)

class BigExplosion(Explosion):
    def __init__(self, pos, group):
        super().__init__(pos, group)
        self.images = [pygame.image.load('images/explosion2/'+img).convert_alpha() for img in os.listdir('images/explosion') if img.endswith('.png')]


# Missile
class Missile(pygame.sprite.Sprite):
    def __init__(self, speed,angle,target, vector,bullet_group, sound, game):
        super().__init__()
        self.__image = pygame.image.load('images/Missile1.png').convert_alpha()
        self.image = self.__image
        self.speed = speed
        self.vector = vector
        self.angle = angle
        self.target = target
        self.sound = sound
        self.game = game

        self.rect = self.__image.get_rect()
        self.rect.center = self.vector.get_pos()


        self.starting_pos = self.vector.get_pos()
        bullet_group.add(self)
    
    def draw(self, win):
        image = pygame.transform.rotate(self.__image, degrees(self.angle))
        pygame.draw.line(win, (255,0,0), self.starting_pos, (self.rect.centerx-5, self.rect.centery))
        win.blit(image, (self.rect.x, self.rect.y))
        #pygame.draw.rect(win, (255,255,255), (self.rect.x+5, self.rect.y+5,2,2))

    def update(self, win):
        self.vector.x += self.speed * cos(self.angle)
        self.vector.y -= self.speed * sin(self.angle)

        self.rect.x = self.vector.x
        self.rect.y = self.vector.y
        if self.vector.get_distance(self.target) < 5:
            self.sound.play()
            self.explosion()
            self.kill()
        if self.vector.get_distance(self.starting_pos) > 1000:
            self.kill()
        self.draw(win)
    
    def explosion(self):
        BigExplosion(self.vector.get_pos(),self.game.miscellaneous)
        for enemy in self.game.enemyGroup:
            if self.vector.get_distance(enemy.vector.get_pos()) < 50:
                if isinstance(enemy, ship.Ship):
                    self.game.add_score(20)
                else:
                    self.game.add_score(10)
                enemy.kill_on_spot()

# Enemy Missile
class EnemyMissile(pygame.sprite.Sprite):
    def __init__(self, speed, angle, vector, enemy_group, game):
        super().__init__()
        self.image = pygame.image.load('images/Missile2.png').convert_alpha()
        self.speed = speed
        self.angle = angle
        self.vector = vector
        self.game = game

        self.rect = self.image.get_rect()
        self.rect.center = self.vector.get_pos()
        
        self.is_stunned = False
        self.cd = 0

        enemy_group.add(self)
    
    def draw(self, win):
        image = pygame.transform.rotate(self.image, degrees(self.angle))
        win.blit(image, (self.rect.x, self.rect.y))

    def update(self, win):
        if self.is_stunned:
            self.cd -= 1
            if self.cd == 0:
                self.is_stunned = False
            self.draw(win)
            return
        self.vector.x += self.speed * cos(self.angle)
        self.vector.y -= self.speed * sin(self.angle)

        self.rect.x = self.vector.x
        self.rect.y = self.vector.y

        if self.vector.y > 700:
            self.kill_on_spot()

        self.draw(win)
    
    def getStunned(self):
        self.is_stunned = True
        self.cd = 50

    def kill_on_spot(self):
        Explosion(self.vector.get_pos(), self.game.miscellaneous)
        self.kill()


class SplitMissile(EnemyMissile):
    def __init__(self, speed, vector, enemy_group, game):
        self.ANGLE = -1.5708
        super().__init__(speed, self.ANGLE, vector, enemy_group, game)
        self.image = pygame.image.load('images/Missile3.png').convert_alpha()
        self.time = ran.randint(50,100)
    
    def draw(self, win):
        image = pygame.transform.rotate(self.image, degrees(self.ANGLE))
        win.blit(image, (self.rect.x, self.rect.y))

    def update(self, win):
        if self.is_stunned:
            self.cd -= 1
            if self.cd == 0:
                self.is_stunned = False
            self.draw(win)
            return
        self.vector.y += self.speed

        self.rect.y = self.vector.y
        self.rect.x = self.vector.x

        if self.time > 0:
            self.time -= 1
        
        if self.time == 0:
            self.split()
            self.kill_on_spot()

        if self.vector.y > 700:
            self.kill_on_spot()

        self.draw(win)
    
    def split(self):
        for i in range(-1,2):
            angle = radians(degrees(self.ANGLE) + (i * 15))
            SPEED = 4
            spawn = Vector(self.vector.x, self.vector.y)
            EnemyMissile(SPEED, angle, spawn, self.game.enemyGroup, self.game)

class HardSplitMissile(EnemyMissile):
    def __init__(self, speed, vector, enemy_group, game):
        self.ANGLE = -1.5708
        super().__init__(speed, self.ANGLE, vector, enemy_group, game)
        self.image = pygame.image.load('images/Missile3_1.png').convert_alpha()
        self.time = ran.randint(50,100)
    
    def draw(self, win):
        image = pygame.transform.rotate(self.image, degrees(self.ANGLE))
        win.blit(image, (self.rect.x, self.rect.y))

    def update(self, win):
        if self.is_stunned:
            self.cd -= 1
            if self.cd == 0:
                self.is_stunned = False
            self.draw(win)
            return
        self.vector.y += self.speed

        self.rect.y = self.vector.y
        self.rect.x = self.vector.x

        if self.time > 0:
            self.time -= 1
        
        if self.time == 0:
            self.split()
            self.kill_on_spot()

        if self.vector.y > 700:
            self.kill_on_spot()

        self.draw(win)
    
    def split(self):
        for i in range(-3,4):
            angle = radians(degrees(self.ANGLE) + (i * 10))
            SPEED = 8
            spawn = Vector(self.vector.x, self.vector.y)
            EnemyMissile(SPEED, angle, spawn, self.game.enemyGroup, self.game)

class ADMissile(EnemyMissile):
    def __init__(self, speed, angle, vector, enemy_group, game):
        
        super().__init__(speed, angle, vector, enemy_group, game)
        self.image = pygame.image.load('images/Missile0.png').convert_alpha()

class ADSplitMissile(SplitMissile):
    def __init__(self, speed, vector, enemy_group, game):
        super().__init__(speed, vector, enemy_group, game)
        self.image = pygame.image.load('images/ADSplit.png').convert_alpha()
        self.time = ran.randint(25,50)
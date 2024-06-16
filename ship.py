import pygame
import random as ran
import missile

import buff

from vector import Vector
#from math import cos, sin, degrees

# green ship

class Ship(pygame.sprite.Sprite):
    def __init__(self, velocity, vector, ship_group, game):
        super().__init__()
        self.image = pygame.image.load('images/Green Ship.png').convert_alpha()
        self.vector = vector
        self.game = game
        if self.vector.x > 0:
            self.velocity = -velocity
            self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.velocity = velocity
        self.rect = self.image.get_rect()
        self.rect.x = self.vector.x
        self.rect.y = self.vector.y
        self.starting = self.vector
        self.is_stunned = False
        self.cd = 20
        self.group = ship_group
        self.time = 0
        self.fire_rate = 25
        ship_group.add(self)
    
    def draw(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y))
    
    def update(self, win):
        if self.is_stunned:
            self.cd -= 1
            if self.cd == 0:
                self.is_stunned = False
            self.draw(win)
            return
        self.time += 1
        self.vector.x += self.velocity
        self.rect.x = self.vector.x
        self.rect.y = self.vector.y
        if self.rect.x < -70 and self.velocity < 0:
            self.kill()
        elif self.rect.x > 700 and self.velocity > 0:
            self.kill()
        self.drop_missile()
        self.draw(win)
    
    def getStunned(self):
        self.is_stunned = True
        self.cd = 50

    def drop_missile(self):
        if self.time % self.fire_rate == 0:  # Adjust this probability as needed
            starting = self.vector.get_pos()
            target = (ran.randint(15,585), 700)
            angle = self.vector.get_angle(target)
            SPEED = 4
            missile.ADMissile(SPEED, angle, Vector(starting[0], starting[1]), self.group, self.game)
    
    def drop_buff(self):
        buffList = [("heal", 70), ("stun", 20), ("kill", 10)]

        random = ran.randint(0,100)
        cum_value = 0
        for loot, weight in buffList: # called loot because buff is an imported file
            cum_value += weight
            if random <= cum_value:
                if loot == 'heal':
                    buff.Buff(Vector(self.vector.x, self.vector.y), self.game.buffGroup, self.game)
                elif loot == 'stun':
                    buff.stunbuff(Vector(self.vector.x, self.vector.y), self.game.buffGroup, self.game)
                elif loot == 'kill':
                    buff.Killbuff(Vector(self.vector.x, self.vector.y), self.game.buffGroup, self.game)
                break

    def kill_on_spot(self):
        missile.Explosion(self.vector.get_pos(), self.game.miscellaneous)
        self.drop_buff()
        self.kill()

class MechanizedShip(Ship):
    def __init__(self, velocity, vector, ship_group, game):
        super().__init__(velocity, vector, ship_group, game)
        self.image = pygame.image.load('images/Dark Red Ship.png')
        if self.vector.x > 0:
            self.velocity = -velocity
            self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.velocity = velocity
        self.fire_rate = 50
    
    def drop_missile(self):
        if self.time % self.fire_rate == 0:
            SPEED = 4
            SPAWN = Vector(self.vector.x, self.vector.y)
            missile.ADSplitMissile(SPEED, SPAWN, self.game.enemyGroup, self.game)
import pygame
from math import cos, sin, degrees


# Common Bullet
class Missile(pygame.sprite.Sprite):
    def __init__(self, image_path, speed,angle,target, vector,bullet_group, sound):
        super().__init__()
        self.__image = pygame.image.load(image_path).convert_alpha()
        self.image = self.__image
        self.speed = speed
        self.vector = vector
        self.angle = angle
        self.target = target
        self.sound = sound

        self.rect = self.__image.get_rect()


        self.starting_pos = self.vector.get_pos()
        bullet_group.add(self)
    
    def draw(self, win):
        image = pygame.transform.rotate(self.__image, degrees(self.angle))
        pygame.draw.line(win, (255,0,0), self.starting_pos, (self.rect.x+(5*sin(self.angle)), self.rect.y+(5*cos(self.angle))))
        win.blit(image, (self.rect.x, self.rect.y))

    def update(self, win, enemies, game):
        self.vector.x += self.speed * cos(self.angle)
        self.vector.y -= self.speed * sin(self.angle)

        self.rect.x = self.vector.x
        self.rect.y = self.vector.y
        if self.vector.get_distance(self.target) < 5:
            self.sound.play()
            self.explosion(enemies, game)
            self.kill()
        self.draw(win)
    
    def explosion(self, enemies, game):
        print(enemies)
        for enemy in enemies:
            if self.vector.get_distance(enemy.vector.get_pos()) < 50:
                print(self.vector.get_distance(enemy.vector.get_pos()))
                game.add_score(10)
                enemy.kill()
class CuteMissile(Missile):
    def __init__(self, image_path, speed, angle,target, vector, bullet_group, sound):
        super().__init__(image_path, speed, angle,target, vector, bullet_group,sound)


# Enemy Missile
class EnemyMissile(pygame.sprite.Sprite):
    def __init__(self, image, speed, angle, vector, enemy_group):
        super().__init__()
        self.image = image
        self.speed = speed
        self.angle = angle
        self.vector = vector

        self.rect = image.get_rect()
        

        enemy_group.add(self)
    
    def draw(self, win):
        image = pygame.transform.rotate(self.image, degrees(self.angle))
        win.blit(image, (self.rect.x, self.rect.y))

    def update(self, win):
        self.vector.x += self.speed * cos(self.angle)
        self.vector.y -= self.speed * sin(self.angle)

        self.rect.x = self.vector.x
        self.rect.y = self.vector.y

        self.draw(win)
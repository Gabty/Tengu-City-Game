import pygame
import os


class Building(pygame.sprite.Sprite):
    def __init__(self, health, buildgroup, vector):
        super().__init__()
        self.health = health
        self.state = True # alive
        self.vector = vector
        
        buildgroup.add(self)

    def update(self):
        pass

    def draw(self):
        pass

class UtilityBuilding(Building):
    def __init__(self, health, group, vector):
        super().__init__(health, group, vector)
        self.image = pygame.image.load('images/Utility.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = self.vector.get_pos()
        self.frame = 0
    
    def draw(self,screen):
        if self.health > 0 and self.state:
            screen.blit(self.image, (self.rect.x, self.rect.y))
        else:
            screen.blit(self.animation[self.frame], (self.rect.x, self.rect.y))
    
    def update(self, screen):
        if self.health <= 0:
            self.collapse()
        if self.state == False and self.frame != 7:
            self.frame += 1
        
        self.draw(screen)
    
    def heal(self, points):
        self.health = min(self.health+points, 100)
    
    def collapse(self):
        self.animation = [pygame.image.load('images/Collapse/'+img).convert_alpha() for img in os.listdir('images/Collapse') if img.endswith('.png')]
        self.state = False

class ArtilleryBuilding(Building):
    def __init__(self, health, group, vector):
        super().__init__(health, group, vector)
        self.image = pygame.image.load('images/Artillery.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = self.vector.get_pos()
        self.frame = 0
    
    def draw(self,screen):
        if self.health >0 and self.state:
            screen.blit(self.image, (self.rect.x, self.rect.y))
        else:
            screen.blit(self.animation[self.frame], (self.rect.x, self.rect.y))
        #print(self.rect)

    def update(self, screen):
        if self.health <= 0 and self.state == True:
            self.collapse()
        if self.state == False and self.frame != 7:
            self.frame += 1
        
        self.draw(screen)

    def heal(self, points):
        self.health = min(self.health+points, 100)

    def collapse(self):
        self.animation = [pygame.image.load('images/Collapse2/'+img).convert_alpha() for img in os.listdir('images/Collapse') if img.endswith('.png')]
        self.state = False
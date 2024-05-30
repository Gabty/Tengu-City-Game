import pygame


class Building(pygame.sprite.Sprite):
    def __init__(self, health, buildgroup, vector):
        super().__init__()
        self.health = health
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
    
    def draw(self,screen):
        screen.blit(self.image, self.vector.get_pos())
    
    def update(self, screen):
        self.draw(screen)
    
    def help(self):
        pass

class ArtilleryBuilding(Building):
    def __init__(self, health, group, vector):
        super().__init__(health, group, vector)

        self.image = pygame.image.load('images/Artillery.png').convert_alpha()
    
    def draw(self,screen):
        screen.blit(self.image, self.vector.get_pos())
    
    def update(self, screen):
        self.draw(screen)
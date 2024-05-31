import pygame
#from math import cos, sin, degrees

# green ship
class Ship(pygame.sprite.Sprite):
    def __init__(self, image,velocity, vector, ship_group):
        super().__init__()
        self.image = pygame.image.load(image).convert_alpha()
        self.vector = vector

        if self.vector.x > 0:
            self.velocity = -velocity
            self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.velocity = velocity
        self.starting = self.vector

        self.rect = self.image.get_rect()

        ship_group.add(self)
    
    def draw(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y))
    
    def update(self, win):
        self.vector.x += self.velocity

        self.rect.x = self.vector.x
        self.rect.y = self.vector.y
        self.draw(win)

class Red_Ship(Ship):
    def __init__(self, image, velocity, vector, ship_group,):
        super().__init__(image, velocity, vector, ship_group)
        self.aggressive = True
    
    def update(self):
        super().update()
        if self.aggressive and not self.target:
            # Add aggressive behavior
            pass

class Yellow_ship(Ship):
    def __init__(self, image, velocity, vector, ship_group,):
        super().__init__(image, velocity, vector, ship_group)
        self.mechanized = True
    
    def update(self):
        super().update()
        if self.mechanized and not self.target:
            # Add mechanized behavior
            pass

class Dark_Green(Ship):
    def __init__(self, image, velocity, vector, ship_group):
        super().__init__(image, velocity, vector, ship_group,)
        self.stronger = True
    
    def update(self):
        super().update()
        if self.stronger:
            # Add stronger behavior
            pass

class Dark_Red(Ship):
    def __init__(self, image, velocity, vector, ship_group):
        super().__init__(image, velocity, vector, ship_group)
        self.more_aggressive = True
    
    def update(self):
        super().update()
        if self.more_aggressive:
            # Add more aggressive behavior
            pass
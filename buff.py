import pygame

import building

# health
class Buff(pygame.sprite.Sprite):
    def __init__(self, vector, group, game):
        super().__init__()
        self.vector = vector
        self.image = pygame.image.load('images/buff/Buff1.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = self.vector.get_pos()
        self.game = game

        group.add(self)
    
    def draw(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y))
    
    def update(self, win):
        self.vector.y += 1
        self.rect.y = self.vector.y
        self.rect.x = self.vector.x

        self.draw(win)
    
    def buff_start(self):
        for build in self.game.buildingGroup:
            build.heal(10)


class Killbuff(Buff):
    def __init__(self, vector, group, game):
        super().__init__(vector, group, game)
        self.image = pygame.image.load('images/buff/Buff2.png').convert_alpha()
    
    def buff_start(self):
        for enemy in self.game.enemyGroup:
            self.game.add_score(5)
            enemy.kill_on_spot()


class stunbuff(Buff):
    def __init__(self, vector, group, game):
        super().__init__(vector, group, game)
        self.image = pygame.image.load('images/buff/Buff3.png').convert_alpha()

    def buff_start(self):
        for enemy in self.game.enemyGroup:
            enemy.getStunned()

import pygame

import bullet
import ship
import building

from math import *
from vector import Vector
import time
import random as ran

pygame.init()

WIDTH, HEIGHT  = 600,700

class Main():
    def __init__(self):
        self.screen = pygame.display.set_mode((600,700))
        self.clock = pygame.time.Clock()

        self.run = False
        # game scene
        self.gameScene = gameScene('main')
        self.mainmenu = MainMenu(self.screen, self.gameScene)
        self.game = Game(self.screen, self.gameScene, self.clock)
        self.checkpoint = Checkpoint(self.screen, self.gameScene)
        self.leaderboard = Leaderboard(self.screen, self.gameScene)
        self.state = {'main': self.mainmenu, 'game': self.game, 'check': self.checkpoint, 'leaderboard': self.leaderboard}
    
    def play(self):
        self.run = True
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if self.gameScene.getState() == 'check':
                    self.checkpoint.event(event)
                if self.gameScene.getState() == 'game':
                    self.game.event(event)
            self.state[self.gameScene.getState()].run()

            self.clock.tick(30)
            pygame.display.update()

class gameScene:
    def __init__(self, state):
        self.__state = state
    def getState(self):
        return self.__state
    def setState(self, newState):
        self.__state = newState

class MainMenu:
    def __init__(self, screen, gamescene):
        self.screen = screen
        self.gamescene = gamescene

        self.font = pygame.font.Font('fonts/INVASION2000.TTF', 100)


    def run(self):
        mouse = pygame.mouse
        self.screen.fill((0,0,0))
        rect = pygame.Rect((200,200,200,75))
        pygame.draw.rect(self.screen, (255,255,255), (300-100,200,200,75))
        if rect.collidepoint(mouse.get_pos()) and mouse.get_pressed()[0]:
            pygame.draw.rect(self.screen, (255,0,0), (300-100,200,200,75))
            self.gamescene.setState('check')
            time.sleep(0.005)
        
        rect2 = pygame.Rect((200,300,200,75))
        pygame.draw.rect(self.screen, (255,255,255), (300-100,300,200,75))
        if rect2.collidepoint(mouse.get_pos()) and mouse.get_pressed()[0]:
            pygame.draw.rect(self.screen, (255,0,0), rect2)
            self.gamescene.setState('leaderboard')
        pygame.draw.rect(self.screen, (255,255,255), (300-100,400,200,75))

class Checkpoint:
    def __init__(self, screen, gamescene):
        self.screen = screen
        self.gamescene = gamescene

        self.user_input = ''
        self.base_font = pygame.font.Font("fonts/ARCADECLASSIC.TTF", 64)

        self.input_rect = pygame.Rect(220,200, 150,75)
        self.start_rect = pygame.Rect(220,300, 150,75)

        self.input_state = False
    def event(self, event):
        if event.type == pygame.KEYDOWN and self.input_state:
            if event.key == pygame.K_BACKSPACE:
                self.user_input = self.user_input[:-1]
            else:
                if len(self.user_input) < 13:
                    self.user_input += event.unicode
        
        if event.type == pygame.MOUSEBUTTONUP:
            pos = event.pos
            if self.button_pressed(self.input_rect, pos) and not self.input_state:
                self.input_state = True
            else:
                self.input_state = False
            
            if self.button_pressed(self.start_rect,pos):
                self.gamescene.setState('game')
    
    def button_pressed(self,rect, pos):
        return rect.collidepoint(pos)
    
    def run(self):
        self.screen.fill((100,100,100))
        text = self.base_font.render(self.user_input, True, (255,255,255))
        pygame.draw.rect(self.screen, (255,0,255), self.input_rect, 5)
        pygame.draw.rect(self.screen, (0,0,255), self.start_rect)
        self.screen.blit(text, ((WIDTH//2)-(text.get_width()/2), self.input_rect.y+5))
        
        if len(self.user_input) > 3:
            self.input_rect.x = (WIDTH//2) - text.get_width()/2 - 10
            self.input_rect.w = text.get_width() + 15

class Leaderboard:
    def __init__(self, screen, gamescene):
        self.screen = screen
        self.gamescene = gamescene
        self.font = pygame.font.Font("fonts/INVASION2000.TTF", 32)
        self.large_font = pygame.font.Font("fonts/ARCADECLASSIC.TTF", 44)
        
        # Sample 
        self.scores = [
            ("Player1", 1500),
            ("Player2", 1400),
            ("Player3", 1300),
            ("Player4", 1200),
            ("Player5", 1100),
            ("Player6", 1000),
            ("Player7", 900),
            ("Player8", 800),
            ("Player9", 700),
            ("Player10", 600)
        ]

    def draw_text(self, text, font, color, surface, center_x, center_y):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect(center=(center_x, center_y))
        surface.blit(textobj, textrect)

    def draw_box(self, center_x, center_y, w, h, border_color, surface):
        box_rect = pygame.Rect(0, 0, w, h)
        box_rect.center = (center_x, center_y)
        pygame.draw.rect(surface, border_color, box_rect, 2)
        return box_rect

    def run(self):
        self.screen.fill((0, 0, 0))
        
        screen_width, screen_height = self.screen.get_size()
        
        title_box = self.draw_box(screen_width // 2, 50, 500, 50, (255, 0, 0), self.screen)
        self.draw_text("Leaderboard", self.large_font, (255, 255, 255), self.screen, title_box.centerx, title_box.centery)
        
        header_box = self.draw_box(screen_width // 2, 120, 500, 50, (255, 0, 0), self.screen)
        self.draw_text("Rank", self.font, (255, 255, 255), self.screen, header_box.left + 60, header_box.centery)
        self.draw_text("Name", self.font, (255, 255, 255), self.screen, header_box.centerx, header_box.centery)
        self.draw_text("Scores", self.font, (255, 255, 255), self.screen, header_box.right - 60, header_box.centery)
        
        y_offset = 190
        for idx, (name, score) in enumerate(self.scores, start=1):
            score_box = self.draw_box(screen_width // 2, y_offset, 500, 40, (255, 0, 0), self.screen)
            self.draw_text(str(idx), self.font, (255, 255, 255), self.screen, score_box.left + 60, score_box.centery)
            self.draw_text(name, self.font, (255, 255, 255), self.screen, score_box.centerx, score_box.centery)
            self.draw_text(str(score), self.font, (255, 255, 255), self.screen, score_box.right - 60, score_box.centery)
            y_offset += 50

class Game:
    def __init__(self, screen, gamescene, clock):
        self.screen = screen
        self.gamescene = gamescene
        self.clock = clock
        self.time = 0

        self.__score = 0

        self.missileGroup = pygame.sprite.Group()
        self.shipGroup = pygame.sprite.Group()
        self.buildingGroup = pygame.sprite.Group()
        # Initialized the buildings Artillery
        building.ArtilleryBuilding(100, self.buildingGroup, Vector(270,600)) # middile
        building.ArtilleryBuilding(100, self.buildingGroup, Vector(90,600)) # left
        building.ArtilleryBuilding(100, self.buildingGroup, Vector(450,600)) # right
        # Initialize the building Utility
        building.UtilityBuilding(100, self.buildingGroup, Vector(15,610))
        building.UtilityBuilding(100, self.buildingGroup, Vector(180,610))
        building.UtilityBuilding(100, self.buildingGroup, Vector(360,610))
        building.UtilityBuilding(100, self.buildingGroup, Vector(525,610))
    
    def update(self):
        self.missileGroup.update(self.screen)
        self.shipGroup.update(self.screen)
        self.buildingGroup.update(self.screen)
        
        self.time += self.clock.get_rawtime()
        
        if self.time % 50 == 0:
            self.spawn_ship()


    def draw(self):
        self.screen.fill((0,0,0))
        pygame.draw.line(self.screen, (255,255,255), (300,0), (300,700))
    def event(self, event):
        mouse = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONUP:
            dis = 9999 # initialized to 9999 determines the selection
            build = None # initialized to None for selection
            for i in self.buildingGroup:
                if isinstance(i, building.ArtilleryBuilding):
                    if i.vector.get_distance(mouse) < dis:
                        dis = i.vector.get_distance(mouse)
                        build = i
            
            self.shoot(build,mouse)

    
    def spawn_ship(self):
        rangeY = ran.randint(100,200)
        spawnX = [-20,720]
        ship.Green_Ship('images/Missile_1.png', 4, Vector(ran.choice(spawnX), rangeY), self.shipGroup)
    
    def shoot(self, building, target):
        angle = Vector(building.vector.x+30, building.vector.y).get_angle(target)
        print(degrees(angle))
        bullet.CuteMissile('images/Missile1.png',5, angle, Vector(building.vector.x+30, building.vector.y), self.missileGroup)
        pygame.draw.line(self.screen, (255,255,255), Vector(building.vector.x+30, building.vector.y).get_pos(), target)
    def run(self):
        self.draw()
        self.update()

        print(len(self.missileGroup))


if __name__ == "__main__":
    game = Main()
    game.play()
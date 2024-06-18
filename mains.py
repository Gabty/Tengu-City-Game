import pygame

import missile
import ship
import building


from math import *
from vector import Vector
import random as ran
import os

import json

from abc import ABC, abstractmethod

pygame.init()
pygame.display.set_caption('Tengu City')
img = pygame.image.load('images/Icon.png')
pygame.display.set_icon(img)

WIDTH, HEIGHT  = 600,700

class Main:
    def __init__(self):
        self.screen = pygame.display.set_mode((600,700))
        self.clock = pygame.time.Clock()

        self.run = False
        self.isGameOver = False
        # game scene
        self.gameScene = gameScene('main')
        self.mainmenu = MainMenu(self.screen, self.gameScene)
        self.game = Game(self.screen, self.gameScene, self)
        self.checkpoint = Checkpoint(self.screen, self.gameScene, self)
        self.leaderboard = Leaderboard(self.screen, self.gameScene)
        self.gameover = GameOver(self.screen, self.gameScene, self)
        self.state = {'main': self.mainmenu, 'game': self.game, 'check': self.checkpoint, 'leaderboard': self.leaderboard, 'gameover': self.gameover}

        self.user = None

        self.bg_music = pygame.mixer.Sound('sounds/bgmusic.mp3')
        self.bg_music.set_volume(0.75)
        self.bg_music.play(-1)
    
    def get_score(self):
        return self.game.get_score()
    
    def set_name(self, user):
        self.user = user

    def get_name(self):
        return self.user

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
                if self.gameScene.getState() == 'leaderboard':
                    self.leaderboard.event(event)
                if self.gameScene.getState() == 'quit':
                    self.run = False
                if self.gameScene.getState() == 'gameover':
                    self.bg_music.set_volume(0.2)
                    self.gameover.event(event)
                if self.gameScene.getState() == 'main':
                    self.mainmenu.event(event)
            if self.gameScene.getState() != 'quit':
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

class Scene(ABC):
    def draw(self):
        pass
    @abstractmethod
    def run(self):
        pass
    @abstractmethod
    def event(self, event):
        pass

class MainMenu(Scene):
    def __init__(self, screen, gamescene):
        self.screen = screen
        self.gamescene = gamescene

        self.background = pygame.image.load('images/Background.png')

        title_font = pygame.font.Font('fonts/INVASION2000.TTF', 72)
        self.title = title_font.render("Tengu City", True, (255,255,255))

        self.buttons = []

        self.start_button = pygame.image.load('images/start1.png')
        self.start_hover = pygame.image.load('images/start2.png')

        self.start_rect = self.start_button.get_rect()
        self.start_rect.center = ((WIDTH//2), 300)
        self.buttons.append((self.start_rect, 'check'))

        self.leaderboard_button = pygame.image.load('images/leaderboard1.png')
        self.leaderboard_hover = pygame.image.load('images/leaderboard2.png')

        self.leaderboard_rect = self.leaderboard_button.get_rect()
        self.leaderboard_rect.center = ((WIDTH//2), 400)
        self.buttons.append((self.leaderboard_rect, 'leaderboard'))

        self.quit_button = pygame.image.load('images/quit1.png')
        self.quit_hover = pygame.image.load('images/quit2.png')

        self.quit_rect = self.start_button.get_rect()
        self.quit_rect.center = ((WIDTH//2), 500)
        self.buttons.append((self.quit_rect, 'quit'))

        self.mouse = pygame.mouse

    def draw(self):
        self.screen.blit(self.background, (0,0))
        self.screen.blit(self.title, (WIDTH//2 - self.title.get_width()//2, 100))
        self.button(self.start_rect, self.start_button, self.start_hover)
        self.button(self.leaderboard_rect, self.leaderboard_button, self.leaderboard_hover)
        self.button(self.quit_rect, self.quit_button, self.quit_hover)

    def run(self):
        self.draw()
        #self.button(self.start_rect, self.start_button, self.start_hover, 'quit')
    def button(self,rect, image, hover):
        mouse = pygame.mouse
        self.screen.blit(image, (rect.x, rect.y))
        if rect.collidepoint(mouse.get_pos()):
            self.screen.blit(hover, (rect.x, rect.y))
    
    def event(self, event):
        for button, state in self.buttons:
            if event.type == pygame.MOUSEBUTTONUP and button.collidepoint(self.mouse.get_pos()):
                self.gamescene.setState(state)

class Checkpoint(Scene):
    def __init__(self, screen, gamescene,game):
        self.screen = screen
        self.gamescene = gamescene
        self.game = game

        self.background = pygame.image.load('images/Dawn2.png')

        self.user_input = ''
        self.base_font = pygame.font.Font("fonts/ARCADECLASSIC.TTF", 64)
        self.base2_font = pygame.font.Font("fonts/ARCADECLASSIC.TTF", 32)
        self.error_font = pygame.font.Font("fonts/INVASION2000.TTF", 24)
        self.username_text = self.base2_font.render('Gamer Name', True, (255,255,255))

        self.input_rect = pygame.Rect(220,200, 150,75)
        self.start_rect = pygame.Rect(220,300, 150,75)

        self.play_button = pygame.image.load('images/start1.png').convert_alpha()
        self.play_hover = pygame.image.load('images/start2.png').convert_alpha()

        self.play_rect = self.play_button.get_rect()
        self.play_rect.center = (WIDTH//2,400)

        self.input_state = False
        self.mouse = pygame.mouse
        self.need_user_text = self.error_font.render("Please enter gamer name.", True, (255,0,0))
        self.need_user = False
    def event(self, event):
        if event.type == pygame.KEYDOWN and self.input_state:
            if event.key == pygame.K_RETURN:
                self.input_state = False
                return
            if event.key == pygame.K_BACKSPACE:
                self.user_input = self.user_input[:-1]
            else:
                if len(self.user_input) < 13:
                    self.user_input += event.unicode
        
        if event.type == pygame.MOUSEBUTTONDOWN and self.input_rect.collidepoint(self.mouse.get_pos()):
            if self.input_state:
                self.input_state = False
            else:
                self.input_state = True
        
        if event.type == pygame.MOUSEBUTTONUP and self.play_rect.collidepoint(self.mouse.get_pos()):
            if len(self.user_input) > 0:
                self.game.user = self.user_input
                self.gamescene.setState('game')
            else:
                self.need_user = True
    
    def run(self):
        self.screen.blit(self.background, (0,0))
        self.screen.blit(self.username_text, (WIDTH//2-self.username_text.get_width()//2, 200-self.username_text.get_height()))
        text = self.base_font.render(self.user_input, True, (255,255,255))
        if self.input_state:
            pygame.draw.rect(self.screen, (255,255,255), self.input_rect, 5)
        else:
            pygame.draw.rect(self.screen, (100,100,100), self.input_rect, 5)
        self.screen.blit(self.play_button, (self.play_rect.x, self.play_rect.y))
        if self.play_rect.collidepoint(self.mouse.get_pos()):
            self.screen.blit(self.play_hover, (self.play_rect.x, self.play_rect.y))
        self.screen.blit(text, ((WIDTH//2)-(text.get_width()/2), self.input_rect.y+5))

        if self.need_user:
            self.screen.blit(self.need_user_text, ((WIDTH//2)-self.need_user_text.get_width()/2, 300))
        
        if len(self.user_input) > 3:
            self.input_rect.x = (WIDTH//2) - text.get_width()/2 - 10
            self.input_rect.w = text.get_width() + 15

class Leaderboard(Scene):
    def __init__(self, screen, gamescene):
        self.screen = screen
        self.gamescene = gamescene
        self.background = pygame.image.load('images/Leaderboards.png')
        self.font = pygame.font.Font("fonts/INVASION2000.TTF", 32)
        self.large_font = pygame.font.Font("fonts/ARCADECLASSIC.TTF", 44)
        
        # Sample 
        with open('score.json', 'r+') as file:
            data = json.load(file)
            self.scores = list(data.items())

        self.scores = list(sorted(self.scores, key=lambda x: x[1], reverse=True))

    def draw_text(self, text, font, color, surface, center_x, center_y):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect(center=(center_x, center_y))
        surface.blit(textobj, textrect)
    
    def event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.gamescene.setState('main')

    def draw_box(self, center_x, center_y, w, h, border_color, surface):
        box_rect = pygame.Rect(0, 0, w, h)
        box_rect.center = (center_x, center_y)
        pygame.draw.rect(surface, border_color, box_rect, 2)
        return box_rect

    def run(self):
        self.screen.blit(self.background, (0,0))
        
        screen_width, screen_height = self.screen.get_size()
        
        title_box = self.draw_box(screen_width // 2, 50, 500, 50, (255, 0, 0), self.screen)
        self.draw_text("Leaderboard", self.large_font, (255, 255, 255), self.screen, title_box.centerx, title_box.centery)
        
        header_box = self.draw_box(screen_width // 2, 120, 500, 50, (255, 0, 0), self.screen)
        self.draw_text("Rank", self.font, (255, 255, 255), self.screen, header_box.left + 60, header_box.centery)
        self.draw_text("Name", self.font, (255, 255, 255), self.screen, header_box.centerx, header_box.centery)
        self.draw_text("Scores", self.font, (255, 255, 255), self.screen, header_box.right - 60, header_box.centery)
        
        y_offset = 190
        for idx, (name, score) in enumerate(self.scores[0:10], start=1):
            score_box = self.draw_box(screen_width // 2, y_offset, 500, 40, (255, 0, 0), self.screen)
            self.draw_text(str(idx), self.font, (255, 255, 255), self.screen, score_box.left + 60, score_box.centery)
            self.draw_text(name, self.font, (255, 255, 255), self.screen, score_box.centerx, score_box.centery)
            self.draw_text(str(score), self.font, (255, 255, 255), self.screen, score_box.right - 60, score_box.centery)
            y_offset += 50

class Game(Scene):
    def __init__(self, screen, gamescene, game):
        self.screen = screen
        self.gamescene = gamescene
        self.game = game
        self.time = 0

        self.__score = 0

        self.missileGroup = pygame.sprite.Group()
        self.buildingGroup = pygame.sprite.Group()
        self.enemyGroup = pygame.sprite.Group()
        self.miscellaneous = pygame.sprite.Group()
        self.buffGroup = pygame.sprite.Group()
        # Initialized the buildings Artillery
        building.ArtilleryBuilding(100, self.buildingGroup, Vector(300,650)) # middile
        building.ArtilleryBuilding(100, self.buildingGroup, Vector(120,650)) # left
        building.ArtilleryBuilding(100, self.buildingGroup, Vector(480,650)) # right
        # Initialize the building Utility
        building.UtilityBuilding(100, self.buildingGroup, Vector(45,655))
        building.UtilityBuilding(100, self.buildingGroup, Vector(210,655))
        building.UtilityBuilding(100, self.buildingGroup, Vector(390,655))
        building.UtilityBuilding(100, self.buildingGroup, Vector(555,655))

        self.scoreFont = pygame.font.Font("fonts/INVASION2000.TTF", 24)

        self.explosionsfx = pygame.mixer.Sound('sounds/explode.wav')
        self.launchsfx = pygame.mixer.Sound('sounds/launching.wav')
        self.GOsfx = pygame.mixer.Sound('sounds/gameover.wav')

        self.background = pygame.image.load('images/Dawn2.png')
    
    def add_score(self, score):
        self.__score += score
    
    def get_score(self):
        return self.__score

    def update(self):
        self.missileGroup.update(self.screen)
        self.buildingGroup.update(self.screen)
        self.miscellaneous.update(self.screen)
        self.buffGroup.update(self.screen)
        self.enemyGroup.update(self.screen)

        buildingCollision = pygame.sprite.groupcollide(self.enemyGroup, self.buildingGroup, False, False)
        buffCollision = pygame.sprite.groupcollide(self.buffGroup, self.missileGroup, True, False)
        

        if buildingCollision:
            for keys, values in buildingCollision.items():
                if values[0].state == True:
                    keys.kill_on_spot()
                values[0].health -= 10
        
        if buffCollision:
            for buffs, _ in buffCollision.items():
                buffs.buff_start()
                
        
        self.time += 1

        if all(obj.state == False for obj in self.buildingGroup if isinstance(obj, building.ArtilleryBuilding)):
            self.GOsfx.play(1)
            self.gamescene.setState('gameover')
        
        spawn_ship = max(50, 100-int(self.__score // 100))
        spawn_missile = max(10, 30-int(self.__score // 100))
        util_rate = max(500, 1000-int(self.__score // 50)) # to achieve 500 need 25000 score points lol
        if self.time % util_rate == 0:
            self.utility()

        if self.time % spawn_ship == 0:
            self.spawn_ship()
        
        if self.time % spawn_missile == 0:
            self.enemy_shoot()
    def draw(self):
        self.screen.blit(self.background, (0,0))
        text = self.scoreFont.render("Score: "+str(self.__score), True, (255,255,255))
        self.screen.blit(text, (((WIDTH//2)-(text.get_width()/2), text.get_height())))
    
    def event(self, event):
        mouse = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                dis = 9999 # initialized to 9999 determines the selection
                build = None # initialized to None for selection
                for i in self.buildingGroup:
                    if i.state:
                        if isinstance(i, building.ArtilleryBuilding):
                            if i.vector.get_distance(mouse) < dis:
                                dis = i.vector.get_distance(mouse)
                                build = i
                
                self.shoot(build,mouse)

    def spawn_ship(self):
        rangeY = ran.randint(100,200)
        spawnX = [-60,720]
        SPEED = 4
        if self.__score < 1000:
            ship.Ship(SPEED, Vector(ran.choice(spawnX), rangeY), self.enemyGroup, self) # only this
        else:
            if ran.random() < 0.5:
                ship.Ship(SPEED, Vector(ran.choice(spawnX), rangeY), self.enemyGroup, self)
            else:
                ship.MechanizedShip(SPEED, Vector(ran.choice(spawnX), rangeY), self.enemyGroup, self)
    
    def shoot(self, building, target):
        angle = Vector(building.rect.center[0], building.rect.y).get_angle(target)
        SPEED = 10
        missile.Missile(SPEED, angle,target, Vector(building.rect.center[0], building.rect.y), self.missileGroup, self.explosionsfx, self)
        pygame.draw.line(self.screen, (255,255,255), Vector(building.rect.center[0], building.rect.y).get_pos(), target)
        self.launchsfx.play()
    
    def enemy_shoot(self):
        
        # target
        rangeX = ran.randint(15,585)
        targetY = 600
        # spawn
        s_rangeX = ran.randint(-15,615)
        spawnY = -20
        # angle
        target = Vector(rangeX, targetY)
        Espawn = Vector(s_rangeX, spawnY)
        angle = Espawn.get_angle(target.get_pos())
        SPEED = 4
        if ran.random() < 0.5:
            missile.EnemyMissile(SPEED,angle, Espawn, self.enemyGroup, self)
        else:
            s_rangeX = ran.randint(100, 485)
            Espawn = Vector(s_rangeX, spawnY)
            if self.__score > 1000:
                if ran.random() < 0.5:
                    missile.HardSplitMissile(SPEED, Espawn, self.enemyGroup, self)
                else:
                    missile.SplitMissile(SPEED, Espawn, self.enemyGroup, self)
            else:
                missile.SplitMissile(SPEED, Espawn, self.enemyGroup, self)
    
    def utility(self):
        count = [i for i in self.buildingGroup if isinstance(i, building.UtilityBuilding) and i.state == True]
        heal_point = len(count) * 10 # 1 = 10 hp, 2 = 20 hp, 3 = 30 hp, 4 = 40 hp # max hp is 100 for buildin
        for j in self.buildingGroup:
            if isinstance(j, building.ArtilleryBuilding):
                j.heal(heal_point)

    def run(self):
        self.draw()
        self.update()

class GameOver(Scene):
    def __init__(self, screen, gamescene, game):
        self.screen = screen
        self.gamescene = gamescene

        self.background = pygame.image.load('images/game over screen.png')
        self.bg_rect = self.background.get_rect()
        self.bg_rect.center = (WIDTH//2,HEIGHT//2)
        self.is_placed = False

        self.game = game
        self.mouse = pygame.mouse

        self.base_font = pygame.font.Font('fonts/INVASION2000.TTF',80)
        self.base_font2 = pygame.font.Font('fonts/INVASION2000.TTF',40)
        self.base_font3 = pygame.font.Font('fonts/INVASION2000.TTF',35)

        self.quit_button = pygame.image.load('images/quit1.png').convert_alpha()
        self.quit_hover = pygame.image.load('images/quit2.png').convert_alpha()

        self.quit_rect = self.quit_button.get_rect()
        self.quit_rect.center = (WIDTH//2, 500)

        self.gamer_name_text = self.base_font2.render("Gamer Name:", True, (205, 175, 15))

    def draw(self):
        if not self.is_placed:
            self.screen.blit(self.background, (self.bg_rect.x, self.bg_rect.y))
            self.screen.blit(self.gamer_name_text,(WIDTH//2-self.gamer_name_text.get_width()//2, 350))
            user = self.base_font3.render(self.game.get_name(), True, (255, 195, 65))
            score = self.base_font.render(str(self.game.get_score()), True, (255, 195, 65))
            
            self.screen.blit(score, (WIDTH//2-score.get_width()//2, 250))
            self.screen.blit(user, (WIDTH//2-user.get_width()//2, 400))
            self.is_placed = True
        
        
        self.screen.blit(self.quit_button, (self.quit_rect.x, self.quit_rect.y))
        if self.quit_rect.collidepoint(self.mouse.get_pos()):
            self.screen.blit(self.quit_hover, (self.quit_rect.x, self.quit_rect.y))
    def run(self):
        self.draw()
    
    def save(self):
        score = self.game.get_score()
        name = self.game.get_name()

        with open('score.json', 'r') as f:
            data = json.load(f)
        data[name] = score
        with open('score.json', 'w') as w:
            json.dump(data,w)

    def event(self, event):
        if event.type == pygame.MOUSEBUTTONUP and self.quit_rect.collidepoint(self.mouse.get_pos()):
            self.save()
            self.gamescene.setState('quit')

if not os.path.exists('score.json'):
    with open('score.json', 'w') as f:
        json.dump({},f)

if __name__ == "__main__":
    game = Main()
    game.play()
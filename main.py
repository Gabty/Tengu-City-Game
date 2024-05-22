import pygame
from math import *
from vector import Vector
import random as ran

from building import Building
import entity

pygame.init()

WIDTH, HEIGHT = 600,700

win = pygame.display.set_mode((WIDTH, HEIGHT))



# asteroid stats
number_for_asteroids = 16
asteroid_speed = 2
asteroid_radius = 10
ASTEROID_COLOR = (255,0,0)
# bullet stats
bullets_ingame = 8
bullet_radius = 4
bullet_speed = 4
BULLET_COLOR = (255,0,255)

# arrays (reusable lolz) position is automated can be adjust!
asteroids = [entity.Entity(win,Vector(ran.randint(0,600),-100),asteroid_radius,ASTEROID_COLOR, asteroid_speed)for i in range(number_for_asteroids)]
bullets = [entity.Entity(win,Vector(800,350),bullet_radius,BULLET_COLOR,bullet_speed, friendly=True) for i in range(8)]

# BUILDING PRE CONSTRUCTED
buildings = [Building(win, Vector(50,610), 60,90, (255,255,255),10),Building(win, Vector(200,610), 60,90, (255,255,255),10),Building(win, Vector(350,610), 60,90, (255,255,255),10),Building(win, Vector(500,610), 60,90, (255,255,255),10)]

def update():

    for asteroid in asteroids:
        asteroid.update()
    
    for bullet in bullets:
        bullet.update()

    for building in buildings:
        building.update()
    
    # asteroid checks for collision only
    for asteroid in asteroids:
        for object in bullets + buildings:
            if isinstance(object, entity.Entity) and asteroid.is_collision(object.vector, object.radius):
                asteroid.disable()
                object.disable()

            if isinstance(object, Building) and asteroid.rect_collision(object):
                asteroid.disable()
                object.health -= 1
                if object.health < 1 and object in buildings:
                    buildings.remove(object)
                    


    
    

mouse = pygame.mouse
clock = pygame.time.Clock()

# fire rate
fire_rate = 100
shoot = pygame.time.get_ticks()
# asteroid

spawn_clock = 0

run = True
while run:
    if len(buildings) == 0:
        print("GAME OVER")
        break
    win.fill((0,0,0))
    update()
    spawn_clock += clock.get_rawtime()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if mouse.get_pressed()[0] and pygame.time.get_ticks() - shoot > fire_rate:
        bullet = ran.choice(bullets)
        if not bullet.state:
            shoot = pygame.time.get_ticks()
            shooter = ran.choice(buildings)
            midpoint = shooter.midpoint()
            bullet.vector.x = shooter.vector.x + midpoint[0]
            bullet.vector.y = shooter.vector.y + bullet.radius
            bullet.shoot(mouse.get_pos())
            
    
    if int(spawn_clock) % 10 == 0:
        asteroid_time = pygame.time.get_ticks()
        chosen = ran.choice(asteroids)

        target = ran.choice(buildings)
        midpoint = target.midpoint()

        chosen.shoot((target.vector.x + midpoint[0], target.vector.y))
    clock.tick(60)
    pygame.display.update()
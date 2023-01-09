import pygame
import numpy as np
import math

import json

from particle import particle
from universe import universe

WIDTH = 800
HEIGHT = 600
FPS = 60

#initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Gravity')
clock = pygame.time.Clock()

univ = universe(200, 100)
univ.addparticle(particle(100000, 1000, static=True))
univ.ringaround(0, 50, (1.1, 2), FPS)



running = True
paused = True
trail = False
realtime = True

while running:
    if realtime:
        clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            if event.key == pygame.K_r:
                realtime = not realtime
            if event.key == pygame.K_t:
                trail = not trail
                if trail and paused:
                    univ.calcarcs(1/FPS)
        elif event.type == pygame.MOUSEMOTION:
            if event.buttons[0]:
                univ.moveoffset(event.rel)
        elif event.type == pygame.MOUSEWHEEL:
            mp = np.array(pygame.mouse.get_pos())
            univ.moveoffset(tuple(-mp))
            univ.scale *= 0.5 if event.y > 0 else 2
            univ.moveoffset(tuple(mp))

    #update
    if not paused:
        univ.tick(1/FPS)
            
    #render
    screen.fill((0,0,0))
    univ.draw(screen)
    if paused and trail:
        univ.drawarcs(screen)
    pygame.display.flip()       



with open("ke.txt", "w") as text_file:
    for ke in univ.kehistory:
        text_file.write(f'{ke}\n')
pygame.quit()
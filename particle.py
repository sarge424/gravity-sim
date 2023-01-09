import pygame
import numpy as np
import math

def rot90(vec):
    return np.array([-vec[1], vec[0]])

class particle:
    def __init__(self, m, s, x=0, y=0, v=None, static=False):
        self.pos = np.array([x, y], dtype=float)
        if v == None or static:
            self.vel = np.array([0., 0.], dtype=float)
        else:
            self.vel = np.array(list(v), dtype=float)
            
        self.mass = m
        self.size = s
        self.static = static
        
    def orbit(self, other, K):
        #K = G * FPS
        rvec = self.pos - other.pos
        r = np.linalg.norm(rvec)
        dir = rot90(rvec) / r
        self.vel = dir * math.sqrt(K * other.mass / r) + other.vel
        print('r', rvec, 'dir', dir)
        
    def setvel(self, x, y):
        if not self.static:
            self.vel = np.array([x, y], dtype=float)

        
    def update(self, dt):
        if not self.static:
            self.pos += self.vel * dt
            return 0.5 * self.mass * (np.linalg.norm(self.vel) ** 2)
        return 0
        
    def getpos(self):
        return (self.pos[0], self.pos[1])
        
    def draw(self, disp, offset=(0,0), scale=1):
        coord = tuple(np.subtract(self.getpos(), offset) * scale)
        pygame.draw.circle(disp, (255,255,255), coord, max(self.size*scale, 2))
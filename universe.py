import pygame
import numpy as np
import copy
import random
import math

from particle import particle

class universe:
    def __init__(self, G, arclen):
        self.t = -1
        
        self.particles = []
        
        self.G = G
        self.arclen = arclen
        self.arcs = []
        
        self.kehistory = []
        
        self.mass = 0
        self.com = np.zeros(2)
        
        self.offset = np.array([-3000, -2500])
        self.scale = 0.125
    
    def orbit(self, planet, moon, FPS):
        self.particles[moon].orbit(self.particles[planet], self.G * FPS)
        
    def ringaround(self, index, count, spread, FPS):
        planet = self.particles[index]
        for i in range(count):
            height = planet.size * (random.random() * (spread[1] - spread[0]) + spread[0])
            ang = random.randrange(0, 360) * (math.pi / 180)
            
            px = height * math.cos(ang)
            py = height * math.sin(ang)
            
            newp = particle(0, random.randrange(2, 10), px, py)
            self.addparticle(newp)
            newp.orbit(planet, self.G * FPS)
            
        
    def moveoffset(self, delta):
        self.offset[0] -= delta[0] / self.scale
        self.offset[1] -= delta[1] / self.scale
        
    def addparticle(self, p):
        self.particles.append(p)
        
    def tick(self, dt):
        self.t += 1
        self.mass = sum([p.mass for p in self.particles])
        
        self.com = np.zeros(2)
        ke = 0
        for p in self.particles:
            if not p.static:
                others = [q for q in self.particles if q != p]
                #rk4
                k1 = self.samplefield(p.pos, collection=others)
                k2 = self.samplefield(p.pos + (k1 * dt) / 2, collection=others)
                k3 = self.samplefield(p.pos + (k2 * dt) / 2, collection=others)
                k4 = self.samplefield(p.pos + (k3 * dt), collection=others)
                p.vel += (k1 + 2*k2 + 2*k3 + k4)/6
            
            ke += p.update(dt)
            self.com += p.pos * p.mass
            
            
        self.com /= self.mass
        
        if self.t % (1/dt * 5) == 0:
            self.kehistory.append(ke)
        
    def samplefield(self, at, collection=None):
        objects = []
        if collection == None:
            objects = copy.deepcopy(self.particles)
        else:
            objects = copy.deepcopy(collection)
            
        acc = np.zeros(2)
        for p in objects:
            if p.mass == 0:
                continue
            r = at - p.pos
            rmag = np.linalg.norm(r)
            if rmag == 0:
                continue
            rvec = (at - p.pos) / rmag
            acc += -rvec * (self.G * p.mass) / (rmag ** 2)
            
        return acc
            
    def makepath(self, particles):
        for i, p in enumerate(particles):
            self.arcs[i].append(p.getpos())
        
    def simulate(self, particles, dt):
        for p in particles:
            if not p.static:
                others = [q for q in particles if q != p]
                #rk4
                k1 = self.samplefield(p.pos, collection=others)
                k2 = self.samplefield(p.pos + (k1 * dt) / 2, collection=others)
                k3 = self.samplefield(p.pos + (k2 * dt) / 2, collection=others)
                k4 = self.samplefield(p.pos + (k3 * dt), collection=others)
                p.vel += (k1 + 2*k2 + 2*k3 + k4)/6
        
        for p in particles:
            p.update(dt)
        
    def calcarcs(self, dt):
        self.arcs = [[] for _ in self.particles]
        tmp = copy.deepcopy(self.particles)
        for _ in range(self.arclen):
            self.makepath(tmp)
            self.simulate(tmp, dt)
            
    def drawarcs(self, disp):
        for path in self.arcs:
            poffset = [tuple(np.subtract(p, self.offset) * self.scale) for p in path]
            pygame.draw.lines(disp, (0,100,0), False, poffset)
    
        return (self.com[0], self.com[1])
              
    def draw(self, disp):
        for p in self.particles:
            p.draw(disp, self.offset, self.scale)
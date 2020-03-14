

import pygame
from color import GREEN, BLUE

# Enviroment variables
global top_offset
global size
global dist

def set_env_variables(offset, s, d):
    global top_offset, size, dist
    top_offset = offset
    size = s
    dist = d

class Cube():

    def __init__(self, pos=(0,0), xdir=1, ydir=0, color=GREEN):
        self.xdir = xdir
        self.ydir = ydir
        self.pos = pos
        self.color = color
    
    def change_dir(self, xdir, ydir):
        self.xdir = xdir
        self.ydir = ydir

    def move(self):
        # Check borders
        if self.pos[0] <= 0 and self.xdir == -1: self.pos = (size-dist, self.pos[1]) # X border left
        elif self.pos[0] >= size-dist and self.xdir == 1: self.pos = (0, self.pos[1]) # X border right
        elif self.pos[1] <= top_offset and self.ydir == -1: self.pos = (self.pos[0], size-dist+top_offset) # Y border top
        elif self.pos[1] >= size-dist+top_offset and self.ydir == 1: self.pos = (self.pos[0], top_offset) # Y border bottom
        else: self.pos = (self.pos[0] + self.xdir * dist, self.pos[1] + self.ydir * dist)

    def draw(self, surface, eyes):
        pygame.draw.rect(surface, self.color, (self.pos[0]+2, self.pos[1]+2, dist-3, dist-3))
        # Draw the eyes
        if eyes == True:
            var = dist // 2
            center = (self.pos[0] + var, self.pos[1] + var)
            radius = dist // 8
            dist_btw_eyes = var*3//8
            dist_center = var*3//4
            loc1 = (center[0] + dist_btw_eyes*self.ydir + dist_center*self.xdir, 
                    center[1] - dist_btw_eyes*self.xdir + dist_center*self.ydir)
            loc2 = (center[0] - dist_btw_eyes*self.ydir + dist_center*self.xdir, 
                    center[1] + dist_btw_eyes*self.xdir + dist_center*self.ydir)
            pygame.draw.circle(surface, BLUE, loc1, radius)
            pygame.draw.circle(surface, BLUE, loc2, radius)

class Snake():

    rotations = {}

    def __init__(self, pos=(0,0), xdir=1, ydir=0, color=GREEN):
        self.xdir = xdir
        self.ydir = ydir
        self.pos = pos
        self.color = color
        self.head = Cube(pos, xdir, ydir, color)
        self.body = [self.head]
        new_pos = pos[:]
        for i in range(4):
            new_pos = (new_pos[0] - dist, new_pos[1])
            self.body.append(Cube(new_pos, xdir, ydir, color))

    def change_dir(self, xdir, ydir):
        self.rotations[self.head.pos] = (xdir, ydir)
        self.xdir = xdir
        self.ydir = ydir
        self.head.change_dir(xdir, ydir)
    
    def move(self):
        for i,c in enumerate(self.body):
            if c.pos in self.rotations:
                c.change_dir(self.rotations[c.pos][0], self.rotations[c.pos][1])
            if i == len(self.body) - 1 and c.pos in self.rotations:
                self.rotations.pop(c.pos)
            c.move()

    def add_cube(self):
        new_pos = (self.body[-1].pos[0] - self.body[-1].xdir * dist, self.body[-1].pos[1] - self.body[-1].ydir * dist)
        cube = Cube(new_pos, self.body[-1].xdir, self.body[-1].ydir, self.color)
        self.body.append(cube)

    def draw(self, surface):
        for c in self.body: 
            if c == self.head:
                c.draw(surface, True)
            else:
                c.draw(surface, False)

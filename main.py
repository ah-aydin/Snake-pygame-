

import pygame
import random as rnd
from tkinter import messagebox

# Table variables
size = 1000
n_rows = 20
dist = size // n_rows

# Color variables
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)


game_is_running = True
global snack
global has_snack

pygame.init()

window = pygame.display.set_mode((size, size))

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
        if self.pos[0] <= 0 and self.xdir == -1: self.pos = (size-dist, self.pos[1])
        elif self.pos[0] >= size-dist and self.xdir == 1: self.pos = (0, self.pos[1])
        elif self.pos[1] <= 0 and self.ydir == -1: self.pos = (self.pos[0], size-dist)
        elif self.pos[1] >= size-dist and self.ydir == 1: self.pos = (self.pos[0], 0)
        else: self.pos = (self.pos[0] + self.xdir * dist, self.pos[1] + self.ydir * dist)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.pos[0]+2, self.pos[1]+2, dist-3, dist-3))

class Snake():

    rotations = {}

    def __init__(self, pos=(dist * (n_rows // 2), dist * (n_rows // 2)), xdir=1, ydir=0, color=GREEN):
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
        for c in self.body: c.draw(surface)

def check_collisions():
    check_collision()
    check_snack_collision()

def check_collision():
    head = snake.head
    for cube in snake.body:
        if cube == head: continue
        if head.pos == cube.pos:
            pygame.quit()
            messagebox.showinfo("GAME OVER", "GAME OVEnTotal score: BANANAS")
            exit()

def check_snack_collision():
    global snack
    global has_snack
    if snake.head.pos == snack.pos:
        snake.add_cube()
        del snack
        # This solves a bug
        snack = Cube((-100, -100))
        has_snack = False

def spawn_snack(surface):
    global snack
    global has_snack
    has_snack = True
    x = rnd.randint(0, n_rows-1)
    while x == snake.pos[1] // n_rows:
        return
    y = rnd.randint(0, n_rows-1)
    snack = Cube((x*dist,y*dist), 0, 0, RED)

def draw_frame(surface):
    global snack
    surface.fill(BLACK)
    snake.draw(surface)
    snack.draw(surface)
    draw_grid(surface)
    pygame.display.update()

def draw_grid(surface):
    i = 0
    for l in range(n_rows):
        i += dist
        pygame.draw.line(surface, WHITE, (i,0), (i,size))
        pygame.draw.line(surface, WHITE, (0,i), (size,i))

def check_input():

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        snake.change_dir(0, -1)
    elif keys[pygame.K_DOWN]:
        snake.change_dir(0, 1)
    elif keys[pygame.K_RIGHT]:
        snake.change_dir(1, 0)
    elif keys[pygame.K_LEFT]:
        snake.change_dir(-1, 0)

def main():

    global snake
    global has_snack
    has_snack = False
    snake = Snake()

    clock = pygame.time.Clock()

    while game_is_running:
        pygame.time.delay(100)
        clock.tick(120)
        
        check_input()
        if has_snack == False: spawn_snack(window)
        draw_frame(window)
        snake.move()
        check_collisions()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

if __name__ == '__main__':
    main()
    exit()
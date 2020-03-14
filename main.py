

import os
import pygame
import random as rnd
from tkinter import messagebox

import snake as S
from snake import Snake, Cube
from color import GREEN, WHITE, RED, BLACK

# Initialize required pygame modules
pygame.init()
pygame.font.init()

# Enviroment variables
top_offset = 50
size = 600
n_rows = 20
dist = size // n_rows

# Score related variables
score = 0
score_font = pygame.font.SysFont('score_font', 50)

# Set the enviroment variables on snake
S.set_env_variables(top_offset, size, dist)

game_is_running = True
global snack
global has_snack

window = pygame.display.set_mode((size+1, size + top_offset+1))

def update_score():
    global score
    score += 1

def display_score():
    score_surface = score_font.render('Score: {0}'.format(score), False, WHITE)
    window.blit(score_surface, (5, 5))

def check_collisions():
    check_collision()
    check_snack_collision()

def check_collision():
    head = snake.head
    for cube in snake.body:
        if cube == head: continue
        if head.pos == cube.pos:
            pygame.quit()
            high_score = -1
            if(os.path.exists('high_score.txt')):
                file = open('high_score.txt', 'r')
                high_score = int(file.read())
                file.close()
            if score > high_score:
                file = open('high_score.txt', 'w')
                file.write(str(score))
                messagebox.showinfo('GAME OVER', 'GAME OVER\n NEW HIGH SCORE \n\t{}\t'.format(score))
            else:
                messagebox.showinfo("GAME OVER", "GAME OVER\n TOTAL SCORE: {} \n HIGH SCORE: {}".format(score, high_score))
            exit()

def check_snack_collision():
    global snack
    global has_snack
    if snake.head.pos == snack.pos:
        snake.add_cube()
        update_score()
        del snack
        # This solves a bug
        snack = Cube((-100, -100))
        has_snack = False

def spawn_snack(surface):
    global snack
    global has_snack
    has_snack = True
    snack_start_pos = (0,0)
    in_snake = True
    while True:
        x = rnd.randint(0, n_rows-1)
        y = rnd.randint(0, n_rows-1)
        snack_start_pos = (x*dist, y*dist + top_offset)
        in_snake = False
        for c in snake.body:
            if c.pos == snack_start_pos:
                in_snake = True
        if in_snake == False:
            break
    snack = Cube(snack_start_pos, 0, 0, RED)

def draw_frame(surface):
    global snack
    surface.fill(BLACK)
    snake.draw(surface)
    snack.draw(surface)
    display_score()
    draw_grid(surface)
    pygame.display.update()

def draw_grid(surface):
    i = 0
    for l in range(n_rows+2):
        pygame.draw.line(surface, WHITE, (i,top_offset), (i,size+top_offset))
        pygame.draw.line(surface, WHITE, (0,i+top_offset), (size,i+top_offset))
        i += dist

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
    snake = Snake(pos=(dist * (n_rows // 2), dist * (n_rows // 2) + top_offset))

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

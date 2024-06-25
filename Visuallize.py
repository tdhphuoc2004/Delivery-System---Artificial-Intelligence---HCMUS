import pygame
import sys
import numpy as np

cell_size = 50
F1 = (255,240,213)
BLOCKED = (100,118,135)
GOAL = (255,127,131)
START = (213,232,212)
HIGHLIGHT = (173, 216, 230)
WHITE = (255,255,255)
BLACK = (0,0,0)
num_rows, num_cols = 0, 0

#Read Map
def read_file(filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()
    
    rows, cols = map(int, lines[0].strip().split())
    array = np.array([line.strip().split() for line in lines[1:]])
    return array

#Intialize the pygame
pygame.init()

#create the screen
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode ((SCREEN_WIDTH,SCREEN_HEIGHT))

#Caption and Icon
pygame.display.set_caption('Demo')
icon = pygame.image.load('car.png')
pygame.display.set_icon(icon)

#Map
def draw_map():
    for row in range(10):
        for col in range(10):
            rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)
            
#Highlight    
def highlight_BlockedCell(row,col):
    rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
    pygame.draw.rect(screen, BLOCKED, rect)
    pygame.draw.rect(screen, BLACK, rect, 1)
    
def hightlight_SpecialCell(row,col,string,color):
    color_table = [BLOCKED,GOAL,F1,START,HIGHLIGHT] # BLOCKED = 0, GOAL = 1, F1 = 2, START= 3, HIGHTLIGHT = 4
    rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
    pygame.draw.rect(screen, color_table[color], rect)
    pygame.draw.rect(screen, BLACK, rect, 1)
    font = pygame.font.SysFont(None, 24)
    text = font.render(str(string), True, BLACK)
    text_rect = text.get_rect(center=(col * cell_size + cell_size // 2, row * cell_size + cell_size // 2))
    screen.blit(text, text_rect)
    
#Main function   
def main():
    matrix = read_file('input.txt')
    print(matrix)   
    #Game loop
    run = True
    while run:
        for event in pygame.event.get():    
            if event.type == pygame.QUIT:
                run = False
        
        screen.fill((255,255,255))
        draw_map()
        for i in range(10):
            for j in range(10):
                if matrix[i][j] != '0':  
                    value = matrix[i][j]  
                    if value == '-1':
                        highlight_BlockedCell(i,j)
                    elif value.startswith('S'):
                        hightlight_SpecialCell(i,j,value,3)
                    elif value.startswith('G'):
                        hightlight_SpecialCell(i,j,value,1)
                    elif value.startswith('F'):
                        hightlight_SpecialCell(i,j,value,2)
                    else:
                        hightlight_SpecialCell(i,j,value,4)                 
        pygame.display.update()

    pygame.quit
    sys.exit()
    
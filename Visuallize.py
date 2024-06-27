import pygame
import sys
import numpy as np
import time 
cell_size = 50
F1 = (255,240,213)
BLOCKED = (100,118,135)
GOAL = (255,127,131)
START = (213,232,212)
HIGHLIGHT = (173, 216, 230)
WHITE = (255,255,255)
BLACK = (0,0,0)

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
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode ((SCREEN_WIDTH,SCREEN_HEIGHT))

#Caption and Icon
pygame.display.set_caption('Demo')
icon = pygame.image.load('car.png')
pygame.display.set_icon(icon)

#Map
def draw_map(rows, cols): 
    for row in range(rows):
        for col in range(cols):
            rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)
            
#Highlight    
def highlight_BlockedCell(row,col):
    rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
    pygame.draw.rect(screen, BLOCKED, rect)
    pygame.draw.rect(screen, BLACK, rect, 1)
    
def hightlight_SpecialCell(row,col,string,color):
    color_table = [GOAL,F1,START] # GOAL = 0, F1 = 1, START= 2
    rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
    pygame.draw.rect(screen, color_table[color], rect)
    pygame.draw.rect(screen, BLACK, rect, 1)
    font = pygame.font.SysFont(None, 24)
    text = font.render(str(string), True, BLACK)
    text_rect = text.get_rect(center=(col * cell_size + cell_size // 2, row * cell_size + cell_size // 2))
    screen.blit(text, text_rect)

def highlight_path(path):
    for step in path:
        row, col = step
        
        # Highlight cell with color
        rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, HIGHLIGHT, rect)
        pygame.draw.rect(screen, BLACK, rect, 1)
        
        # Optionally, center icon (e.g., car) on the cell if icon is provided
        if icon:
            icon_rect = icon.get_rect(center=(col * cell_size + cell_size // 2, row * cell_size + cell_size // 2))
            screen.blit(icon, icon_rect)
        
        pygame.display.flip()  # Update the display

#Main function   
def start(board, path):

    print(board.matrix)   
    step_index = 0

    #Game loop
    run = True
    while run:
        for event in pygame.event.get():    
            if event.type == pygame.QUIT:
                run = False
        
        screen.fill((255,255,255))
        draw_map(board.rows, board.cols)
        for i in range(board.rows):
            for j in range(board.cols):
                if board.matrix[i][j] != '0':  
                    value = board.matrix[i][j]  
                    if value == '-1':
                        highlight_BlockedCell(i,j)
                    elif value.startswith('S'):
                        hightlight_SpecialCell(i,j,value,2)
                    elif value.startswith('G'):
                        hightlight_SpecialCell(i,j,value,0)
                    elif value.startswith('F'):
                        hightlight_SpecialCell(i,j,value,1)               
        pygame.display.update()

        # Animate car along the path and highlight visited cells using highlight_path
        if step_index < len(path):
            highlight_path(path[:step_index])  # Highlight visited cells up to current step
            row, col = path[step_index]
            car_x = col * cell_size
            car_y = row * cell_size
            screen.blit(icon, (car_x, car_y))  # Draw car icon at calculated position if not visited
            step_index += 1  # Move to the next step in the path
        
        pygame.display.update()
        time.sleep(0.5)  # Adjust delay time for slower motion

    pygame.quit
    sys.exit()
    
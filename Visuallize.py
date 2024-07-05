import pygame
import sys
import numpy as np
import time 

step_index = 0
cell_size = 50
PATH = (237,208,137)
F1 = (255,240,213)
BLOCKED = (100,118,135)
GOAL = (255,127,131)
START = (213,232,212)
TOLL_BOOTH = (173, 216, 230)
WHITE = (255,255,255)
BLACK = (0,0,0)

#Read Map
def read_file(filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()
    
    rows, cols,time,fuel = map(int, lines[0].strip().split())
    array = np.array([line.strip().split() for line in lines[1:]])
    return array,time,fuel

#Intialize the pygame
pygame.init()

# Create the screen based on the board size
def init_screen(rows, cols):
    global SCREEN_WIDTH, SCREEN_HEIGHT,screen
    SCREEN_WIDTH = cols * cell_size
    SCREEN_HEIGHT = rows * cell_size + 150
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    return screen

#Caption and Icon
pygame.display.set_caption('Demo')
icon = pygame.image.load('car.png')
pygame.display.set_icon(icon)

#Map and draw
def draw_map(rows, cols): 
    screen.fill((255,255,255))
    for row in range(rows):
        for col in range(cols):
            rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)
    pygame.display.update()

def draw_board(matrix,rows,cols):
    for i in range(rows):
            for j in range(cols):
                if matrix[i][j] != '0':  
                    value = matrix[i][j] 
                    if value == '-1':
                        highlight_BlockedCell(i,j)
                    elif value.startswith('S'):
                        hightlight_SpecialCell(i,j,value,2)
                    elif value.startswith('G'):
                        hightlight_SpecialCell(i,j,value,0)
                    elif value.startswith('F'):
                        hightlight_SpecialCell(i,j,value,1)   
                    else:
                        hightlight_SpecialCell(i,j,value,3)
    pygame.display.update()

def draw_path(path):
    global step_index 
    # Animate car along the path and highlight visited cells using highlight_path
    if step_index < len(path):
        highlight_path(path[:step_index])  # Highlight visited cells up to current step
        row, col = path[step_index]
        step_index += 1  # Move to the next step in the path
    pygame.display.update()             
    time.sleep(0.005)  # Adjust delay time for slower motion
    
#Write String
def write_String(Y,X,string,cell):
    font = pygame.font.SysFont(None, 26)
    text = font.render(str(string), True, BLACK)
    text_rect = text.get_rect(center=(X + cell_size * cell // 2, Y + cell_size * cell // 2))
    screen.blit(text, text_rect) 
                                
#Highlight    
def highlight_BlockedCell(row,col):
    rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
    pygame.draw.rect(screen, BLOCKED, rect)
    pygame.draw.rect(screen, BLACK, rect, 1)
    
def hightlight_SpecialCell(row,col,string,color):
    color_table = [GOAL,F1,START,TOLL_BOOTH] # GOAL = 0, F1 = 1, START= 2,TOLL_BOTH = 3
    rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
    pygame.draw.rect(screen, color_table[color], rect)
    pygame.draw.rect(screen, BLACK, rect, 1)
    font = pygame.font.SysFont(None, 24)
    text = font.render(str(string), True, BLACK)
    text_rect = text.get_rect(center=(col * cell_size + cell_size // 2, row * cell_size + cell_size // 2))
    screen.blit(text, text_rect)
    
def hightlight_cell(Y,X,color):
    table = ['WHITE', 'GOAL', 'F1', 'START', 'STOP', 'BLOCKED', 'PATH']
    color_table = [WHITE,GOAL,F1,START,TOLL_BOOTH,BLOCKED,PATH] # WHITE = 0 ,GOAL = 1, F1 = 2, START= 3,TOLL_BOTH = 4, BLOCKED = 5, PATH = 6,
    rect = pygame.Rect(X , Y , cell_size, cell_size)
    pygame.draw.rect(screen, color_table[color], rect)
    pygame.draw.rect(screen, BLACK, rect, 1)
    font = pygame.font.SysFont(None, 18)
    text = font.render(table[color], True, BLACK)
    text_rect = text.get_rect(center=(X + cell_size//2 + cell_size, Y + cell_size//2))
    screen.blit(text, text_rect)
    
def highlight_path(path):
    for step in path:
        row, col = step
        
        # Highlight cell with color
        rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, PATH, rect)
        pygame.draw.rect(screen, BLACK, rect, 1)
        
        # Optionally, center icon (e.g., car) on the cell if icon is provided
        if icon:
            icon_rect = icon.get_rect(center=(col * cell_size + cell_size // 2, row * cell_size + cell_size // 2))
            screen.blit(icon, icon_rect)
        
        pygame.display.flip()  # Update the display

#Helper
def calculate_total_cost(board, path):
    total_cost = 0
    for x, y in path:
        total_cost += board.get_cost(x, y)
    return total_cost


#Main function   
def start(board, path):
    a = calculate_total_cost(board,path)
    print(a)
    init_screen(board.rows,board.cols)
    #Game loop
    run = True
    while run:
        for event in pygame.event.get():    
            if event.type == pygame.QUIT:
                run = False
        
        #Animated the path on the screen 
        draw_map(board.rows, board.cols)
        draw_board(board.matrix,board.rows,board.cols)
        if path != None:
            cell = 3      
            draw_path(path)
            X_Str = (board.cols - 3) / 2 * cell_size
            Y_Str = board.rows * cell_size 
            write_String(Y_Str,X_Str,'Cost: ' + str(calculate_total_cost(board, path)),cell) 
            pygame.display.update()
            #The condition to end the loop
            if step_index == len(path):             
                run = False
        else:
            cell = 3
            X_Str = (board.cols - 3) / 2 * cell_size
            Y_Str = board.rows * cell_size 
            write_String(Y_Str,X_Str,'There\'s a no way to get the goal in time.',cell)
            pygame.display.update() 
            run = False
                  
    #Wait
    wait = True
    while wait:
        for event in pygame.event.get():    
            if event.type == pygame.QUIT:
                wait = False
    pygame.quit
    sys.exit()
    
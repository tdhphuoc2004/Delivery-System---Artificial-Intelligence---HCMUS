import pygame
import pygame
import os
import re
import numpy as np
import time 
import sys
from Utils import createState, print_boards, generateNewState
from Board import Board
from Button import Button
from level1 import DFS, UCS, IDS, BFS, GBFS, Asearch,DLS
from level3 import A_star_search,gbfs
from level2 import Asearch2,UCS_2
from level4 import A_star_search_lv4

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

    # Đọc các thông số từ dòng đầu tiên
    rows, cols, time, fuel = map(int, lines[0].strip().split())
    
    # Chuyển đổi các dòng còn lại thành mảng numpy
    array = np.array([line.strip().split() for line in lines[1:]])
    return array, time, fuel

def write_file(filepath, path, algo):
    try:
        with open(filepath, 'a') as file:  
            file.write(f'{algo}:\n')
            if path is None:
                file.write('None\n')
            else:
                file.write('S\n')
                file.write(' '.join(map(str, path)) + '\n')
    except IOError as e:
        print(f"Error writing to file: {e}")
     
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
cars_color = [  
    (0, 148, 82),
    (0, 128, 128),
    (205, 38, 38),
    (214, 239, 77),
    (214, 239, 77),
    (204, 243, 224),
    (252, 184, 170),
    (227, 114, 186),
    (158, 1, 160)
]
#Map and draw
def draw_map(rows, cols): 
    screen.fill((255,255,255))
    for row in range(rows):
        for col in range(cols):
            rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)
    pygame.display.update()

def draw_cell(matrix,row,col):
    
    rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
    pygame.draw.rect(screen, PATH, rect)
    pygame.draw.rect(screen, BLACK, rect, 1)
    font = pygame.font.SysFont(None, 24)
    if matrix[row][col] != '0':
        text = font.render(str(matrix[row][col]), True, BLACK)
        text_rect = text.get_rect(center=(col * cell_size + cell_size // 2, row * cell_size + cell_size // 2))
        screen.blit(text, text_rect)
         
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

def draw_path(board,path):
    global step_index 
    # Animate car along the path and highlight visited cells using highlight_path
    if step_index < len(path):
        highlight_path(board,path[:step_index])  # Highlight visited cells up to current step
        step_index += 1  # Move to the next step in the path
    pygame.display.update()             
    time.sleep(0.05)  # Adjust delay time for slower motion

def draw_result(board,path):
    if path != None:
        for step in path:
            row, col = step
        
            # Highlight cell with color
            draw_cell(board.matrix,row,col)
               
            pygame.display.flip()  # Update the display

def draw_multiple_path(board, list_of_recorded_moves, list_of_recorded_start_goal):
    step_indices = [0] * len(list_of_recorded_moves)  # Initialize step index for each vehicle
    previous_steps = [None] * len(list_of_recorded_moves)  # Store the previous steps

    while not all_paths_completed(step_indices,list_of_recorded_moves):
        draw_map(board.rows, board.cols)
        draw_board(board.matrix, board.rows, board.cols)
        
        for vehicle_index, path in enumerate(list_of_recorded_moves):
            if step_indices[vehicle_index] < len(path):
                current_step = path[step_indices[vehicle_index]]
                
                if current_step is not None:
                    final_step = current_step
                    previous_steps[vehicle_index] = current_step
                else:
                    final_step = previous_steps[vehicle_index]

                if final_step is not None:
                    row, col = final_step
                    color = cars_color[vehicle_index] if vehicle_index < len(cars_color) else None
                    rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                    pygame.draw.rect(screen, color, rect)
                    pygame.draw.rect(screen, BLACK, rect, 1)
                    font = pygame.font.SysFont(None, 24)
                    text = font.render(f'Xe {vehicle_index}', True, BLACK)
                    text_rect = text.get_rect(center=(col * cell_size + cell_size // 2, row * cell_size + cell_size // 2))
                    screen.blit(text, text_rect)
                
                step_indices[vehicle_index] += 1
                # # Check if the vehicle reached its goal
                # if step_indices[vehicle_index] >= len(path):
                #     # Move to the next start-goal pair for the vehicle
                #     current_goal_indices[vehicle_index] = (current_goal_indices[vehicle_index] + 1) % len(goal_lists[vehicle_index])
                #     if len(goal_lists[vehicle_index]) == 0:
                #         continue  # Skip if there are no start-goal pairs

                #     # Get the new start-goal pair
                #     new_start_goal = goal_lists[vehicle_index][current_goal_indices[vehicle_index]]
                    
                #     # Redraw the map with the new start and goal points
                #     draw_map(board.rows, board.cols)
                #     draw_board(board.matrix, board.rows, board.cols)
                    
                #     # Update the path (assuming there's a function to calculate a new path based on start and goal)
                #     list_of_recorded_moves[vehicle_index] = calculate_new_path(new_start_goal[0], new_start_goal[1])
                #     step_indices[vehicle_index] = 0  # Reset step index for the new path       

        pygame.display.update()
        time.sleep(0.5)  # Adjust delay time for slower motion
                                 
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
    color_table = [WHITE,GOAL,F1,START,TOLL_BOOTH,BLOCKED,PATH] # WHITE = 0 ,GOAL = 1, F1 = 2, START= 3,TOLL_BOTH = 4, BLOCKED = 5, PATH = 6,
    rect = pygame.Rect(X , Y , cell_size, cell_size)
    pygame.draw.rect(screen, color_table[color], rect)
    pygame.draw.rect(screen, BLACK, rect, 1)
    
def highlight_path(board,path):
    if not path:
        return

    # Get the final step in the path
    final_step = path[-1]
    if isinstance(final_step, tuple) and len(final_step) == 2:
        row, col = final_step

        # Draw the final cell in the path
        rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, PATH, rect)
        pygame.draw.rect(screen, BLACK, rect, 1)
        if icon:
            icon_rect = icon.get_rect(center=(col * cell_size + cell_size // 2, row * cell_size + cell_size // 2))
            screen.blit(icon, icon_rect)
        
    pygame.display.flip()

#Helper
def calculate_new_path(start, goal):
    # Placeholder for path calculation logic
    path = [start, goal]  # Example path from start to goal
    return path
def get_font(size):
    return pygame.font.Font(None, size)

def calculate_total_cost(board, path):
    if path == None:
        return 0
    total_cost = 0
    for x, y in path:
        total_cost += board.get_cost(x, y)
    total_cost = total_cost - 1 #starting positon
    return total_cost
def write_String(Y,X,string,cell):
    font = pygame.font.SysFont(None, 26)
    text = font.render(str(string), True, BLACK)
    text_rect = text.get_rect(center=(X + cell_size * cell // 2, Y + cell_size * cell // 2))
    screen.blit(text, text_rect) 
      
def count_vehicles(board):
    count = 0
    
    for row in board.matrix:
        for item in row:
            if isinstance(item, str) and item.startswith('S'):
                count += 1
    
    return count            
def all_paths_completed(step_indices, list_of_recorded_moves):
    return all(step_index >= len(path) for step_index, path in zip(step_indices, list_of_recorded_moves))
   

#Menu function
def menu():
    pygame.init()
    window =pygame.display.set_mode((1500,700))
    screen_width = 1500
    screen_height = 800
    pygame.display.set_caption("Menu")
    window.fill("White")
    while True:
        MENU_MOUSE_POS =pygame.mouse.get_pos()
        
        MENU_TEXT = get_font(100).render("Choose the level",True,"Black")
        MENU_RECT = MENU_TEXT.get_rect(center=(screen_width  / 2, screen_height / 8))
        
        button_y_positions = [
            screen_height / 4,         # LVL1 button
            screen_height/ 4 + 100,   # LVL2 button
            screen_height / 4 + 200,   # LVL3 button
            screen_height / 4 + 300,   # LVL4 button
            screen_height / 4 + 400    # Quit button
        ]
        
        
        LVL1_BUTTON = Button(None, pos=(screen_width / 2, button_y_positions[0]), 
                             text_input="Level 1", font=get_font(75), base_color="Black", hovering_color="#8d8d8d")
        LVL2_BUTTON = Button(None, pos=(screen_width / 2, button_y_positions[1]), 
                                text_input="Level 2", font=get_font(75), base_color="Black", hovering_color="#8d8d8d")
        LVL3_BUTTON= Button(None, pos=(screen_width / 2, button_y_positions[2]), 
                        text_input="Level 3", font=get_font(75), base_color="Black", hovering_color="#8d8d8d")
        LVL4_BUTTON = Button(None, pos=(screen_width / 2, button_y_positions[3]), 
                        text_input="Level 4", font=get_font(75), base_color="Black", hovering_color="#8d8d8d")
        QUIT_BUTTON = Button(None, pos=(screen_width / 2, button_y_positions[4]), 
                             text_input="QUIT", font=get_font(75), base_color="Black", hovering_color="#8d8d8d")

        
        window.blit(MENU_TEXT, MENU_RECT)

        for button in [LVL1_BUTTON, LVL2_BUTTON,LVL3_BUTTON, LVL4_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(window)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if LVL1_BUTTON.checkForInput(MENU_MOUSE_POS):
                    lvl1()
                if LVL2_BUTTON.checkForInput(MENU_MOUSE_POS):
                    lvl2()
                if LVL3_BUTTON.checkForInput(MENU_MOUSE_POS):
                    lvl3()
                if LVL4_BUTTON.checkForInput(MENU_MOUSE_POS):
                    lvl4()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()   

SEARCH_STRATEGIES = {
    'Astar': Asearch,
    'BFS': BFS,
    'DFS': DFS,
    'DLS': DLS,
    'GBFS': GBFS,
    'IDS': IDS,
    'UCS': UCS
}

def mod_lvl1(filename, output_suffix,algo):
    matrix, time, fuel = read_file(filename)
    board = Board(matrix, time, fuel)
    
    search_strategy = SEARCH_STRATEGIES.get(algo, Asearch)  
    path = search_strategy(board)
    
    output_file = os.path.join(os.path.dirname(filename), f'output{output_suffix}_level1.txt')
    write_file(output_file, path,algo)
    

    start(board, path)

def lvl1_mini(filename):
    pygame.init()

    # Define screen dimensions
    screen_width = 1500
    screen_height = 800
    window = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Menu")
    window.fill(pygame.Color("White"))

    # Define button properties
    margin_top = 100
    button_height = 75
    title_height = 100  # Adjusted height for the title
    available_height = screen_height - margin_top - title_height  # Available height for buttons
    spacing_y = (available_height - 2 * button_height) / 3  # Space between buttons vertically for 3 rows

    # Define row and column positions
    row1_y = margin_top + title_height
    row2_y = row1_y + button_height + spacing_y
    row3_y = row2_y + button_height + spacing_y

    # Center buttons horizontally for each row
    button_x_positions = [screen_width / 4, screen_width / 2, 3 * screen_width / 4]

    MENU_TEXT = pygame.font.Font(None, 100).render("Now, you need to choose an algorithm", True, pygame.Color("Black"))
    MENU_RECT = MENU_TEXT.get_rect(center=(screen_width / 2, margin_top / 2))

    # Define buttons
    BUTTONS = [
        Button(None, pos=(button_x_positions[0], row1_y), 
            text_input="1.A* search", font=pygame.font.Font(None, 75), base_color="Black", hovering_color="#8d8d8d"),
        Button(None, pos=(button_x_positions[1], row1_y), 
            text_input="2.BFS", font=pygame.font.Font(None, 75), base_color="Black", hovering_color="#8d8d8d"),
        Button(None, pos=(button_x_positions[2], row1_y), 
            text_input="3.DFS", font=pygame.font.Font(None, 75), base_color="Black", hovering_color="#8d8d8d"),
        Button(None, pos=(button_x_positions[0], row2_y), 
            text_input="4.GBFS", font=pygame.font.Font(None, 75), base_color="Black", hovering_color="#8d8d8d"),
        Button(None, pos=(button_x_positions[1], row2_y), 
            text_input="5.IDS", font=pygame.font.Font(None, 75), base_color="Black", hovering_color="#8d8d8d"),
        Button(None, pos=(button_x_positions[2], row2_y), 
            text_input="QUIT", font=pygame.font.Font(None, 75), base_color="Black", hovering_color="#8d8d8d")
    ]
    match = re.search(r'input(\d+)_level1', filename)
    if match:
        file_number = match.group(1)
    else:
        print(f"Filename format incorrect or number not found: {filename}")
        file_number = '0'  # Or handle it as needed
    
    while True:
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        window.fill(pygame.Color("White"))
        window.blit(MENU_TEXT, MENU_RECT)

        for button in BUTTONS:
            button.changeColor(MENU_MOUSE_POS)
            button.update(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BUTTONS[0].checkForInput(MENU_MOUSE_POS):
                    mod_lvl1(filename,file_number,'A* search')
                if BUTTONS[1].checkForInput(MENU_MOUSE_POS):
                    mod_lvl1(filename,file_number,'BFS')
                if BUTTONS[2].checkForInput(MENU_MOUSE_POS):
                   mod_lvl1(filename,file_number,'DFS')
                if BUTTONS[3].checkForInput(MENU_MOUSE_POS):
                    mod_lvl1(filename,file_number,'GBFS')
                if BUTTONS[4].checkForInput(MENU_MOUSE_POS):
                    mod_lvl1(filename,file_number,'IDS')
                if BUTTONS[5].checkForInput(MENU_MOUSE_POS):
                    menu()

        pygame.display.update()

def lvl1():
    pygame.init()

    # Define screen dimensions
    screen_width = 1500
    screen_height = 800
    window = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Menu")
    window.fill(pygame.Color("White"))

    # Define button properties
    margin_top = 100
    button_height = 75
    title_height = 100  # Adjusted height for the title
    available_height = screen_height - margin_top - title_height  # Available height for buttons
    spacing_y = (available_height - 3 * button_height) / 3  # Space between buttons vertically

    # Define row and column positions
    row1_y = margin_top + title_height
    row2_y = row1_y + button_height + spacing_y
    row3_y = row2_y + button_height + spacing_y

    # Center buttons horizontally for each row
    button_x_positions_row1 = [screen_width / 3, 2 * screen_width / 3]
    button_x_positions_row2 = [screen_width / 4, screen_width / 2, 3 * screen_width / 4]
    button_x_position_row3 = screen_width / 2

    MENU_TEXT = pygame.font.Font(None, 100).render("First, you need to choose a map", True, pygame.Color("Black"))
    MENU_RECT = MENU_TEXT.get_rect(center=(screen_width / 2, margin_top / 2))

    # Define buttons
    BUTTONS = [
        Button(None, pos=(button_x_positions_row1[0], row1_y), 
            text_input="Map 1", font=pygame.font.Font(None, 75), base_color="Black", hovering_color="#8d8d8d"),
        Button(None, pos=(button_x_positions_row1[1], row1_y), 
            text_input="Map 2", font=pygame.font.Font(None, 75), base_color="Black", hovering_color="#8d8d8d"),
        Button(None, pos=(button_x_positions_row2[0], row2_y), 
            text_input="Map 3", font=pygame.font.Font(None, 75), base_color="Black", hovering_color="#8d8d8d"),
        Button(None, pos=(button_x_positions_row2[1], row2_y), 
            text_input="Map 4", font=pygame.font.Font(None, 75), base_color="Black", hovering_color="#8d8d8d"),
        Button(None, pos=(button_x_positions_row2[2], row2_y), 
            text_input="Map 5", font=pygame.font.Font(None, 75), base_color="Black", hovering_color="#8d8d8d"),
        Button(None, pos=(button_x_position_row3, row3_y), 
            text_input="QUIT", font=pygame.font.Font(None, 75), base_color="Black", hovering_color="#8d8d8d")
    ]
    
    while True:
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        window.fill(pygame.Color("White"))
        window.blit(MENU_TEXT, MENU_RECT)

        for button in BUTTONS:
            button.changeColor(MENU_MOUSE_POS)
            button.update(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BUTTONS[0].checkForInput(MENU_MOUSE_POS):
                    filename = 'lvl_1/input1_level1.txt'
                    lvl1_mini(filename)
                if BUTTONS[1].checkForInput(MENU_MOUSE_POS):
                    filename = 'lvl_1/input2_level1.txt'
                    lvl1_mini(filename)
                if BUTTONS[2].checkForInput(MENU_MOUSE_POS):
                    filename = 'lvl_1/input3_level1.txt'
                    lvl1_mini(filename)
                if BUTTONS[3].checkForInput(MENU_MOUSE_POS):
                    filename = 'lvl_1/input4_level1.txt'
                    lvl1_mini(filename)
                if BUTTONS[4].checkForInput(MENU_MOUSE_POS):
                    filename = 'lvl_1/input5_level1.txt'
                    lvl1_mini(filename)
                if BUTTONS[5].checkForInput(MENU_MOUSE_POS):
                    menu()

        pygame.display.update()

def lvl2():
    pygame.init()

    # Define screen dimensions
    screen_width = 1500
    screen_height = 800
    window = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Menu")
    window.fill(pygame.Color("White"))

    # Define button properties
    margin_top = 100
    button_height = 75
    title_height = 100  # Adjusted height for the title
    available_height = screen_height - margin_top - title_height  # Available height for buttons
    spacing_y = (available_height - 3 * button_height) / 3  # Space between buttons vertically

    # Define row and column positions
    row1_y = margin_top + title_height
    row2_y = row1_y + button_height + spacing_y
    row3_y = row2_y + button_height + spacing_y

    # Center buttons horizontally for each row
    button_x_positions_row1 = [screen_width / 3, 2 * screen_width / 3]
    button_x_positions_row2 = [screen_width / 4, screen_width / 2, 3 * screen_width / 4]
    button_x_position_row3 = screen_width / 2

    MENU_TEXT = pygame.font.Font(None, 100).render("First, you need to choose a map", True, pygame.Color("Black"))
    MENU_RECT = MENU_TEXT.get_rect(center=(screen_width / 2, margin_top / 2))

    # Define buttons
    BUTTONS = [
        Button(None, pos=(button_x_positions_row1[0], row1_y), 
            text_input="Map 1", font=pygame.font.Font(None, 75), base_color="Black", hovering_color="#8d8d8d"),
        Button(None, pos=(button_x_positions_row1[1], row1_y), 
            text_input="Map 2", font=pygame.font.Font(None, 75), base_color="Black", hovering_color="#8d8d8d"),
        Button(None, pos=(button_x_positions_row2[0], row2_y), 
            text_input="Map 3", font=pygame.font.Font(None, 75), base_color="Black", hovering_color="#8d8d8d"),
        Button(None, pos=(button_x_positions_row2[1], row2_y), 
            text_input="Map 4", font=pygame.font.Font(None, 75), base_color="Black", hovering_color="#8d8d8d"),
        Button(None, pos=(button_x_positions_row2[2], row2_y), 
            text_input="Map 5", font=pygame.font.Font(None, 75), base_color="Black", hovering_color="#8d8d8d"),
        Button(None, pos=(button_x_position_row3, row3_y), 
            text_input="QUIT", font=pygame.font.Font(None, 75), base_color="Black", hovering_color="#8d8d8d")
    ]
    
    while True:
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        window.fill(pygame.Color("White"))
        window.blit(MENU_TEXT, MENU_RECT)

        for button in BUTTONS:
            button.changeColor(MENU_MOUSE_POS)
            button.update(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BUTTONS[0].checkForInput(MENU_MOUSE_POS):
                    filename = 'lvl_2/input1_level2.txt'
                    lvl2_mini(filename)
                if BUTTONS[1].checkForInput(MENU_MOUSE_POS):
                    filename = 'lvl_2/input2_level2.txt'
                    lvl2_mini(filename)
                if BUTTONS[2].checkForInput(MENU_MOUSE_POS):
                    filename = 'lvl_2/input3_level2.txt'
                    lvl2_mini(filename)
                if BUTTONS[3].checkForInput(MENU_MOUSE_POS):
                    filename = 'lvl_2/input4_level2.txt'
                    lvl2_mini(filename)
                if BUTTONS[4].checkForInput(MENU_MOUSE_POS):
                    filename = 'lvl_2/input5_level2.txt'
                    lvl2_mini(filename)
                if BUTTONS[5].checkForInput(MENU_MOUSE_POS):
                    menu()

        pygame.display.update()

def lvl2_mini(filename):
    pygame.init()

    # Define screen dimensions
    screen_width = 1500
    screen_height = 800
    window = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Menu")
    window.fill(pygame.Color("White"))

    button_height = 75
    button_width = 200
    num_buttons = 3
    total_height = num_buttons * button_height
    spacing_y = (screen_height - total_height) // (num_buttons + 1)

    # Calculate positions
    center_x = screen_width // 2
    button_y_positions = [spacing_y + i * (button_height + spacing_y) for i in range(num_buttons)]
    column_x_positions = [center_x]

    MENU_TEXT = pygame.font.Font(None, 100).render("Now choose an algorithm", True, pygame.Color("Black"))
    MENU_RECT = MENU_TEXT.get_rect(center=(screen_width / 2, spacing_y / 2))

    # Define buttons
    BUTTONS = [
        Button(None, pos=(center_x, button_y_positions[0]), 
            text_input="A* search", font=pygame.font.Font(None, 75), base_color="Black", hovering_color="#8d8d8d"),
        Button(None, pos=(center_x, button_y_positions[1]), 
            text_input="UCS", font=pygame.font.Font(None, 75), base_color="Black", hovering_color="#8d8d8d"),
        Button(None, pos=(center_x, button_y_positions[2]), 
            text_input="QUIT", font=pygame.font.Font(None, 75), base_color="Black", hovering_color="#8d8d8d")
    ]

    # Extract number from filename
    match = re.search(r'input(\d+)_level2', filename)
    file_number = match.group(1) if match else '0'

    while True:
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        window.fill(pygame.Color("White"))
        window.blit(MENU_TEXT, MENU_RECT)

        for button in BUTTONS:
            button.changeColor(MENU_MOUSE_POS)
            button.update(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BUTTONS[0].checkForInput(MENU_MOUSE_POS):
                    algo = 'A* search'
                    matrix, time, fuel = read_file(filename)
                    board = Board(matrix, time, fuel)
                    path = Asearch2(board)
                    output_file = os.path.join(os.path.dirname(filename), f'output{file_number}_level2.txt')
                    write_file(output_file, path,algo)
                    start(board, path)
                if BUTTONS[1].checkForInput(MENU_MOUSE_POS):
                    algo = 'UCS'
                    matrix, time, fuel = read_file(filename)
                    board = Board(matrix, time, fuel)
                    path = UCS_2(board)
                    output_file = os.path.join(os.path.dirname(filename), f'output{file_number}_level2.txt')
                    write_file(output_file, path,algo)
                    start(board, path)
                if BUTTONS[2].checkForInput(MENU_MOUSE_POS):
                    menu()  

        pygame.display.update()

def mod_lvl3(filename, output_suffix,algo):
    matrix, time, fuel = read_file(filename)
    board = Board(matrix, time, fuel)
    path = A_star_search(board)
        # Ghi kết quả vào file
    output_file = os.path.join(os.path.dirname(filename), f'output{output_suffix}_level3.txt')
    write_file(output_file, path,algo)
    start(board, path)

def lvl3():
    pygame.init()

    # Define screen dimensions
    screen_width = 1500
    screen_height = 800
    window = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Menu")
    window.fill(pygame.Color("White"))

    # Define button properties
    margin_top = 100
    button_height = 75
    title_height = 100  # Adjusted height for the title
    available_height = screen_height - margin_top - title_height  # Available height for buttons
    spacing_y = (available_height - 3 * button_height) / 3  # Space between buttons vertically

    # Define row and column positions
    row1_y = margin_top + title_height
    row2_y = row1_y + button_height + spacing_y
    row3_y = row2_y + button_height + spacing_y

    # Center buttons horizontally for each row
    button_x_positions_row1 = [screen_width / 3, 2 * screen_width / 3]
    button_x_positions_row2 = [screen_width / 4, screen_width / 2, 3 * screen_width / 4]
    button_x_position_row3 = screen_width / 2

    MENU_TEXT = pygame.font.Font(None, 100).render("First, you need to choose a map", True, pygame.Color("Black"))
    MENU_RECT = MENU_TEXT.get_rect(center=(screen_width / 2, margin_top / 2))

    # Define buttons
    BUTTONS = [
        Button(None, pos=(button_x_positions_row1[0], row1_y), 
            text_input="Map 1", font=pygame.font.Font(None, 75), base_color="Black", hovering_color="#8d8d8d"),
        Button(None, pos=(button_x_positions_row1[1], row1_y), 
            text_input="Map 2", font=pygame.font.Font(None, 75), base_color="Black", hovering_color="#8d8d8d"),
        Button(None, pos=(button_x_positions_row2[0], row2_y), 
            text_input="Map 3", font=pygame.font.Font(None, 75), base_color="Black", hovering_color="#8d8d8d"),
        Button(None, pos=(button_x_positions_row2[1], row2_y), 
            text_input="Map 4", font=pygame.font.Font(None, 75), base_color="Black", hovering_color="#8d8d8d"),
        Button(None, pos=(button_x_positions_row2[2], row2_y), 
            text_input="Map 5", font=pygame.font.Font(None, 75), base_color="Black", hovering_color="#8d8d8d"),
        Button(None, pos=(button_x_position_row3, row3_y), 
            text_input="QUIT", font=pygame.font.Font(None, 75), base_color="Black", hovering_color="#8d8d8d")
    ]
    
    while True:
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        window.fill(pygame.Color("White"))
        window.blit(MENU_TEXT, MENU_RECT)

        for button in BUTTONS:
            button.changeColor(MENU_MOUSE_POS)
            button.update(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate(BUTTONS):
                    if button.checkForInput(MENU_MOUSE_POS):
                        if i == 0:
                            filename = 'lvl_3/input1_level3.txt'
                            match = re.search(r'input(\d+)_level3', filename)
                            file_number = match.group(1) if match else '0'
                            mod_lvl3(filename, file_number,'A* search')
                        elif i == 1:
                            filename = 'lvl_3/input2_level3.txt'
                            match = re.search(r'input(\d+)_level3', filename)
                            file_number = match.group(1) if match else '0'
                            mod_lvl3(filename, file_number,'A* search')
                        elif i == 2:
                            filename = 'lvl_3/input3_level3.txt'
                            match = re.search(r'input(\d+)_level3', filename)
                            file_number = match.group(1) if match else '0'
                            mod_lvl3(filename, file_number,'A* search')
                        elif i == 3:
                            filename = 'lvl_3/input4_level3.txt'
                            match = re.search(r'input(\d+)_level3', filename)
                            file_number = match.group(1) if match else '0'
                            mod_lvl3(filename, file_number,'A* search')
                        elif i == 4:
                            filename = 'lvl_3/input5_level3.txt'
                            match = re.search(r'input(\d+)_level3', filename)
                            file_number = match.group(1) if match else '0'
                            mod_lvl3(filename, file_number,'A* search')
                        elif i == 5:
                            menu()  

        pygame.display.update()
        
def mode_lvl4(filename, output_suffix):
    matrix, time, fuel = read_file(filename)
    board = Board(matrix, time, fuel)
    vehicles = count_vehicles(board)
    initialize_board = board.copy()
    boards = createState(board, vehicles)
    A_star_search_lv4(boards)
     # Collect recorded data
    list_of_recorded_move = [b.recorded_move for b in boards]
    list_of_recorded_start_goal = [b.recorded_start_goal for b in boards]
    output_file = os.path.join(os.path.dirname(filename), f'output{output_suffix}_level4.txt')
    with open(output_file, 'w') as file:
        file.write("Recorded Paths:\n")
        for i, path in enumerate(list_of_recorded_move):
            file.write(f"Vehicle {i + 1} Path:\n")
            if path:
                for step in path:
                    file.write(f"  {step}\n")
            else:
                file.write("  No path recorded\n")
            file.write("\n")

        file.write("Recorded Start-Goal:\n")
        for i, start_goal in enumerate(list_of_recorded_start_goal):
            file.write(f"Vehicle {i + 1} Start-Goal:\n")
            if start_goal:
                for start, goal in start_goal.items():
                    file.write(f"  Start: {start} -> Goal: {goal}\n")
            else:
                file.write("  No start-goal recorded\n")
            file.write("\n")
    start_lv4_clone(boards, initialize_board)
    
def lvl4():
    pygame.init()
    screen_width = 1500
    screen_height = 700
    window = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Menu")
    window.fill(pygame.Color("White"))

    while True:
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("Choose the map", True, pygame.Color("Black"))
        MENU_RECT = MENU_TEXT.get_rect(center=(screen_width / 2, screen_height / 8))

        button_y_positions = [
            screen_height / 4,         # Map 1 button
            screen_height / 4 + 100,   # Map 2 button
            screen_height / 4 + 200,   # Map 3 button
            screen_height / 4 + 300,   # Map 4 button
            screen_height / 4 + 400,   # Map 5 button
            screen_height / 4 + 500    # Quit button
        ]

        LVL1_BUTTON = Button(None, pos=(screen_width / 2, button_y_positions[0]), 
                             text_input="Map 1", font=get_font(75), base_color="Black", hovering_color="#8d8d8d")
        LVL2_BUTTON = Button(None, pos=(screen_width / 2, button_y_positions[1]), 
                             text_input="Map 2", font=get_font(75), base_color="Black", hovering_color="#8d8d8d")
        LVL3_BUTTON = Button(None, pos=(screen_width / 2, button_y_positions[2]), 
                             text_input="Map 3", font=get_font(75), base_color="Black", hovering_color="#8d8d8d")
        LVL4_BUTTON = Button(None, pos=(screen_width / 2, button_y_positions[3]), 
                             text_input="Map 4", font=get_font(75), base_color="Black", hovering_color="#8d8d8d")
        LVL5_BUTTON = Button(None, pos=(screen_width / 2, button_y_positions[4]), 
                             text_input="Map 5", font=get_font(75), base_color="Black", hovering_color="#8d8d8d")
        QUIT_BUTTON = Button(None, pos=(screen_width / 2, button_y_positions[5]), 
                             text_input="QUIT", font=get_font(75), base_color="Black", hovering_color="#8d8d8d")

        window.blit(MENU_TEXT, MENU_RECT)

        for button in [LVL1_BUTTON, LVL2_BUTTON, LVL3_BUTTON, LVL4_BUTTON, LVL5_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if LVL1_BUTTON.checkForInput(MENU_MOUSE_POS):
                    mode_lvl4("lvl_4/input1_level4.txt", "1")
                elif LVL2_BUTTON.checkForInput(MENU_MOUSE_POS):
                    mode_lvl4("lvl_4/input2_level4.txt", "2")
                elif LVL3_BUTTON.checkForInput(MENU_MOUSE_POS):
                    mode_lvl4("lvl_4/input3_level4.txt", "3")
                elif LVL4_BUTTON.checkForInput(MENU_MOUSE_POS):
                    mode_lvl4("lvl_4/input4_level4.txt", "4")
                elif LVL5_BUTTON.checkForInput(MENU_MOUSE_POS):
                    mode_lvl4("lvl_4/input5_level4.txt", "5")
                elif QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    menu()

        pygame.display.update()
#Start function       
def start(board, path):
    pygame.display.set_caption("Start")
    init_screen(board.rows,board.cols)
    #Game loop
    global step_index
    step_index = 0
    run = True
    while run:
        for event in pygame.event.get():    
            if event.type == pygame.QUIT:
                run = False
        
        #Animated the path on the screen 
        draw_map(board.rows, board.cols)
        draw_board(board.matrix,board.rows,board.cols)
        if path != None:
            flag = True
            cell = 3      
            draw_path(board,path)
            X_Str = (board.cols - 3) / 2 * cell_size
            Y_Str = board.rows * cell_size 
            write_String(Y_Str,X_Str,'Cost: ' + str(calculate_total_cost(board, path)),cell) 
            pygame.display.update()
            #The condition to end the loop
            if step_index == len(path):
                draw_result(board,path)             
                run = False
        else:
            cell = 3
            X_Str = (board.cols - 3) / 2 * cell_size
            Y_Str = board.rows * cell_size 
            write_String(Y_Str,X_Str,'There\'s a no way to get the goal in time.',cell)
            pygame.display.update()
            draw_result(board,path) 
            run = False
                  
    #Wait
    wait = True
    while wait:
        for event in pygame.event.get():        
            if event.type == pygame.QUIT:
                wait = False
    menu()


def start_lv4_clone(boards, initialize_board):
    rows = initialize_board.rows
    cols = initialize_board.cols 
    list_of_recorded_move = []
    list_of_recorded_start_goal = []

    num_vehicles = len(boards)
    for i in range(num_vehicles):
        list_of_recorded_move.append(boards[i].recorded_move)
        list_of_recorded_start_goal.append(boards[i].recorded_start_goal)
    
    print("Recorded paths:", list_of_recorded_move)
    print("Recorded start goal:", list_of_recorded_start_goal)

    init_screen(rows, cols)
    draw_map(rows, cols)
    draw_board(initialize_board.matrix, rows, cols)
    
    draw_multiple_path(initialize_board, list_of_recorded_move, list_of_recorded_start_goal)
    
    wait = True
    while wait:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                wait = False
    
    menu()  # Call the menu function to exit

def test():
    pygame.display.set_caption("Start")
    matrix, time, fuel = read_file('lvl_1/input5_level1.txt')
    board = Board(matrix, time, fuel)
    
    init_screen(board.rows,board.cols)
    #Game loop
    global step_index
    step_index = 0
    run = True
    while run:
        for event in pygame.event.get():    
            if event.type == pygame.QUIT:
                run = False
        
        #Animated the path on the screen 
        draw_map(board.rows, board.cols)
        draw_board(board.matrix,board.rows,board.cols)
        run =False
    wait = True
    while wait:
        for event in pygame.event.get():        
            if event.type == pygame.QUIT:
                wait = False    
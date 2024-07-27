import pygame
import pygame
import os
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

def write_file(filepath, path):
    try:
        with open(filepath, 'w') as file:
            file.write(',  '.join(map(str, path)))
        print(f"Output đã được lưu vào {filepath}")
    except IOError as e:
        print(f"Lỗi khi ghi file: {e}")
     
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
    if matrix[row][col] != '0':  
        value = matrix[row][col] 
        if value == '-1':
            highlight_BlockedCell(row,col)
        elif value.startswith('S'):
            hightlight_SpecialCell(row,col,value,2)
        elif value.startswith('G'):
            hightlight_SpecialCell(row,col,value,0)
        elif value.startswith('F'):
            hightlight_SpecialCell(row,col,value,1)   
        else:
            hightlight_SpecialCell(row,col,value,3)
    else:
        rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, PATH, rect)
        pygame.draw.rect(screen, BLACK, rect, 1)
        
    
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
    time.sleep(1)  # Adjust delay time for slower motion

def draw_result(board,path):
    for step in path:
        row, col = step
        
        # Highlight cell with color
        draw_cell(board.matrix,row,col)
               
        pygame.display.flip()  # Update the display
                
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

def count_vehicles(board):
    count = 0
    
    for row in board.matrix:
        for item in row:
            if isinstance(item, str) and item.startswith('S'):
                count += 1
    
    return count            

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

def mod_lvl1(filename, output_suffix):
    matrix, time, fuel = read_file(filename)
    board = Board(matrix, time, fuel)
    path = Asearch(board)
    start(board, path)

    # Ghi kết quả vào file
    output_file = os.path.join(os.path.dirname(filename), f'output_{output_suffix}_lvl1.txt')
    write_file(output_file, path)

def lvl1():
    pygame.init()

    # Define screen dimensions
    screen_width = 1500
    screen_height = 800  # Adjusted screen height
    window = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Menu")
    window.fill(pygame.Color("White"))
    
    margin_top = 100
    button_height = 75
    spacing_y = (screen_height - 2 * margin_top - 4 * button_height) / 3  # Space between buttons vertically
    spacing_x = screen_width / 3  # Space between two columns

    # Column positions
    column_x_positions = [screen_width / 3, 2 * (screen_width / 3)]
    
    # Row positions
    button_y_positions = [margin_top + i * (button_height + spacing_y) for i in range(4)]

    MENU_TEXT = pygame.font.Font(None, 100).render("Choose the algorithm", True, pygame.Color("Black"))
    MENU_RECT = MENU_TEXT.get_rect(center=(screen_width / 2, margin_top / 2))
    
    BUTTONS = [
        Button(None, pos=(column_x_positions[0], button_y_positions[0]), 
               text_input="A* search", font=pygame.font.Font(None, 75), base_color="Black", hovering_color="#8d8d8d"),
        Button(None, pos=(column_x_positions[0], button_y_positions[1]), 
               text_input="BFS", font=pygame.font.Font(None, 75), base_color="Black", hovering_color="#8d8d8d"),
        Button(None, pos=(column_x_positions[0], button_y_positions[2]), 
               text_input="DFS", font=pygame.font.Font(None, 75), base_color="Black", hovering_color="#8d8d8d"),
        Button(None, pos=(column_x_positions[0], button_y_positions[3]), 
               text_input="DLS", font=pygame.font.Font(None, 75), base_color="Black", hovering_color="#8d8d8d"),
        Button(None, pos=(column_x_positions[1], button_y_positions[0]), 
               text_input="GBFS", font=pygame.font.Font(None, 75), base_color="Black", hovering_color="#8d8d8d"),
        Button(None, pos=(column_x_positions[1], button_y_positions[1]), 
               text_input="IDS", font=pygame.font.Font(None, 75), base_color="Black", hovering_color="#8d8d8d"),
        Button(None, pos=(column_x_positions[1], button_y_positions[2]), 
               text_input="UCS", font=pygame.font.Font(None, 75), base_color="Black", hovering_color="#8d8d8d"),
        Button(None, pos=(column_x_positions[1], button_y_positions[3]), 
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
                            mod_lvl1('lvl_1/input_level1_A.txt', 'Astar')
                        elif i == 1:
                            mod_lvl1('lvl_1/input_level1_BFS.txt', 'BFS')
                        elif i == 2:
                            mod_lvl1('lvl_1/input_level1_DFS.txt', 'DFS')
                        elif i == 3:
                            mod_lvl1('lvl_1/input_level1_DLS.txt', 'DLS')
                        elif i == 4:
                            mod_lvl1('lvl_1/input_level1_GBFS.txt', 'GBFS')
                        elif i == 5:
                            mod_lvl1('lvl_1/input_level1_IDS.txt', 'IDS')
                        elif i == 6:
                            mod_lvl1('lvl_1/input_level1_UCS.txt', 'UCS')
                        elif i == 7:
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
    spacing_y = (screen_height - 2 * margin_top - 3 * button_height) / 2  # Space between buttons vertically for 3 rows
    spacing_x = screen_width / 2  # Space between two columns

    # Column positions
    column_x_positions = [screen_width / 3, 2 * (screen_width / 3)]

    # Row positions
    button_y_positions = [margin_top + i * (button_height + spacing_y) for i in range(3)]

    MENU_TEXT = pygame.font.Font(None, 100).render("First, you need to choose a map", True, pygame.Color("Black"))
    MENU_RECT = MENU_TEXT.get_rect(center=(screen_width / 2, margin_top / 2))

    # Define buttons
    BUTTONS = [
        Button(None, pos=(column_x_positions[0], button_y_positions[0]), 
            text_input="Map 1", font=pygame.font.Font(None, 75), base_color="Black", hovering_color="#8d8d8d"),
        Button(None, pos=(column_x_positions[0], button_y_positions[1]), 
            text_input="Map 2", font=pygame.font.Font(None, 75), base_color="Black", hovering_color="#8d8d8d"),
        Button(None, pos=(column_x_positions[0], button_y_positions[2]), 
            text_input="Map 3", font=pygame.font.Font(None, 75), base_color="Black", hovering_color="#8d8d8d"),
        Button(None, pos=(column_x_positions[1], button_y_positions[0]), 
            text_input="Map 4", font=pygame.font.Font(None, 75), base_color="Black", hovering_color="#8d8d8d"),
        Button(None, pos=(column_x_positions[1], button_y_positions[1]), 
            text_input="Map 5", font=pygame.font.Font(None, 75), base_color="Black", hovering_color="#8d8d8d"),
        Button(None, pos=(column_x_positions[1], button_y_positions[2]), 
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
                    filename = 'lvl_2/input_level2_1.txt'
                    lvl2_mini(filename)
                if BUTTONS[1].checkForInput(MENU_MOUSE_POS):
                    filename = 'lvl_2/input_level2_2.txt'
                    lvl2_mini(filename)
                if BUTTONS[2].checkForInput(MENU_MOUSE_POS):
                    filename = 'lvl_2/input_level2_3.txt'
                    lvl2_mini(filename)
                if BUTTONS[3].checkForInput(MENU_MOUSE_POS):
                    filename = 'lvl_2/input_level2_4.txt'
                    lvl2_mini(filename)
                if BUTTONS[4].checkForInput(MENU_MOUSE_POS):
                    filename = 'lvl_2/input_level2_5.txt'
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
            text_input="A search", font=pygame.font.Font(None, 75), base_color="Black", hovering_color="#8d8d8d"),
        Button(None, pos=(center_x, button_y_positions[1]), 
            text_input="UCS", font=pygame.font.Font(None, 75), base_color="Black", hovering_color="#8d8d8d"),
        Button(None, pos=(center_x, button_y_positions[2]), 
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
                    matrix, time, fuel = read_file(filename)
                    board = Board(matrix, time, fuel)
                    path = Asearch2(board)
                    start(board, path)
                    output_file = os.path.join(os.path.dirname(filename), 'output_Asearch2.txt')
                    write_file(output_file, path)
                if BUTTONS[1].checkForInput(MENU_MOUSE_POS):
                    matrix, time, fuel = read_file(filename)
                    board = Board(matrix, time, fuel)
                    path = UCS_2(board)
                    start(board, path)
                    output_file = os.path.join(os.path.dirname(filename), 'output_UCS_2.txt')
                    write_file(output_file, path)
                if BUTTONS[2].checkForInput(MENU_MOUSE_POS):
                    menu()  

        pygame.display.update()

def mod_lvl3(filename, output_suffix):
    matrix, time, fuel = read_file(filename)
    board = Board(matrix, time, fuel)
    path = A_star_search(board)
    start(board, path)

    # Ghi kết quả vào file
    output_file = os.path.join(os.path.dirname(filename), f'output_{output_suffix}_lvl3.txt')
    write_file(output_file, path)

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
    spacing_y = (screen_height - 2 * margin_top - 3 * button_height) / 2  # Space between buttons vertically for 3 rows
    spacing_x = screen_width / 2  # Space between two columns

    # Column positions
    column_x_positions = [screen_width / 3, 2 * (screen_width / 3)]

    # Row positions
    button_y_positions = [margin_top + i * (button_height + spacing_y) for i in range(3)]

    MENU_TEXT = pygame.font.Font(None, 100).render("Choose a map to search with A* search", True, pygame.Color("Black"))
    MENU_RECT = MENU_TEXT.get_rect(center=(screen_width / 2, margin_top / 2))

    # Define buttons
    BUTTONS = [
        Button(None, pos=(column_x_positions[0], button_y_positions[0]), 
            text_input="Map 1", font=pygame.font.Font(None, 75), base_color="Black", hovering_color="#8d8d8d"),
        Button(None, pos=(column_x_positions[0], button_y_positions[1]), 
            text_input="Map 2", font=pygame.font.Font(None, 75), base_color="Black", hovering_color="#8d8d8d"),
        Button(None, pos=(column_x_positions[0], button_y_positions[2]), 
            text_input="Map 3", font=pygame.font.Font(None, 75), base_color="Black", hovering_color="#8d8d8d"),
        Button(None, pos=(column_x_positions[1], button_y_positions[0]), 
            text_input="Map 4", font=pygame.font.Font(None, 75), base_color="Black", hovering_color="#8d8d8d"),
        Button(None, pos=(column_x_positions[1], button_y_positions[1]), 
            text_input="Map 5", font=pygame.font.Font(None, 75), base_color="Black", hovering_color="#8d8d8d"),
        Button(None, pos=(column_x_positions[1], button_y_positions[2]), 
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
                            mod_lvl3('lvl_3/input_level3_1.txt', '1')
                        elif i == 1:
                            mod_lvl3('lvl_3/input_level3_2.txt', '2')
                        elif i == 2:
                            mod_lvl3('lvl_3/input_level3_3.txt', '3')
                        elif i == 3:
                            mod_lvl3('lvl_3/input_level3_4.txt', '4')
                        elif i == 4:
                            mod_lvl3('lvl_3/input_level3_5.txt', '5')
                        elif i == 5:
                            menu()  

        pygame.display.update()            

def mode_lvl4(filename, output_suffix):
    matrix, time, fuel = read_file(filename)
    board = Board(matrix, time, fuel)
    vehicles = count_vehicles(board)
    initialize_board = board.copy()
    Boards = createState(board, vehicles)
    A_star_search_lv4(Boards)
    start_lv4_clone(Boards, initialize_board)
    
    output_file = f'output_{output_suffix}_lvl4.txt'
    with open(output_file, 'w') as file:
        file.write("Results or status for lvl4...\n")

    
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
            screen_height / 4 + 200    # Map 3 button
        ]

        LVL1_BUTTON = Button(None, pos=(screen_width / 2, button_y_positions[0]), 
                             text_input="Map 1", font=get_font(75), base_color="Black", hovering_color="#8d8d8d")
        LVL2_BUTTON = Button(None, pos=(screen_width / 2, button_y_positions[1]), 
                             text_input="Map 2", font=get_font(75), base_color="Black", hovering_color="#8d8d8d")
        LVL3_BUTTON = Button(None, pos=(screen_width / 2, button_y_positions[2]), 
                             text_input="Map 3", font=get_font(75), base_color="Black", hovering_color="#8d8d8d")

        window.blit(MENU_TEXT, MENU_RECT)

        for button in [LVL1_BUTTON, LVL2_BUTTON, LVL3_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if LVL1_BUTTON.checkForInput(MENU_MOUSE_POS):
                    mode_lvl4("lvl_4/input_level4_1.txt", "1")
                elif LVL2_BUTTON.checkForInput(MENU_MOUSE_POS):
                    mode_lvl4("lvl_4/input_level4_2.txt", "2")
                elif LVL3_BUTTON.checkForInput(MENU_MOUSE_POS):
                    mode_lvl4("lvl_4/input_level4_3.txt", "3")

        pygame.display.update()
            
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
    
def draw_multiple_path(board, list_of_recorded_moves, list_of_recorded_start_goal):
    step_indices = [0] * len(list_of_recorded_moves)  # Initialize step index for each vehicle
    current_goal_indices = [0] * len(list_of_recorded_start_goal)  # Track current goal index for each vehicle
    previous_steps = [None] * len(list_of_recorded_moves)  # Store the previous steps
    goal_lists = [list(goals.items()) for goals in list_of_recorded_start_goal]  # Convert dict to list of tuples

    while any(step_index < len(path) for step_index, path in zip(step_indices, list_of_recorded_moves)):
        draw_map(board.rows, board.cols)
        draw_board(board.matrix, board.rows, board.cols)
        
        for vehicle_index, path in enumerate(list_of_recorded_moves):
            if step_indices[vehicle_index] < len(path):
                current_step = path[step_indices[vehicle_index]]
                
                if current_step is not None:
                    # Use the current step as it is not None
                    final_step = current_step
                    previous_steps[vehicle_index] = current_step  # Update the previous step
                else:
                    # Use the previous step as the current step is None
                    final_step = previous_steps[vehicle_index]

                if final_step is not None:
                    # Highlight the final step of the current path
                    row, col = final_step
                    color = cars_color[vehicle_index] if vehicle_index < len(cars_color) else None
                    rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                    pygame.draw.rect(screen, color, rect)
                    pygame.draw.rect(screen, BLACK, rect, 1)
                    font = pygame.font.SysFont(None, 24)
                    text = font.render(f'Xe {vehicle_index}', True, BLACK)
                    text_rect = text.get_rect(center=(col * cell_size + cell_size // 2, row * cell_size + cell_size // 2))
                    screen.blit(text, text_rect)
                
                # Move to the next step in the path
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
        time.sleep(5)  # Adjust delay time for slower motion


def start_lv4_clone(boards, initialize_board):
    rows = initialize_board.rows
    cols = initialize_board.cols 
    list_of_recorded_move =[]
    list_of_recorded_start_goal = []

    numVehicles = len(boards)
    for i in range(numVehicles):
        list_of_recorded_move.append(boards[i].recorded_move)
        list_of_recorded_start_goal.append(boards[i].recorded_start_goal)
    print ("Recorded paths:", list_of_recorded_move)
    print ("recorded start goal:", list_of_recorded_start_goal)

    init_screen(rows, cols)
    run = True
    while run:
        for event in pygame.event.get():    
            if event.type == pygame.QUIT:
                run = False
        draw_map(rows, cols)
        draw_board(initialize_board.matrix, rows, cols)
        if list_of_recorded_move:
            draw_multiple_path(initialize_board,list_of_recorded_move,list_of_recorded_start_goal)
            cell = 3
            X_Str = (cols - 3) / 2 * cell_size
            Y_Str = rows * cell_size 
            write_String(Y_Str,X_Str,str(list_of_recorded_move),cell)
            if all(step_index >= len(path) for path in list_of_recorded_move):
                    run = False
    wait = True
    while wait:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                wait = False
    menu()

                    
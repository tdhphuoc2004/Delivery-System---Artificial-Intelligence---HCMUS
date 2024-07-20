import Visuallize
import pygame
import random
import sys
from Board import Board
from Button import Button
from level1 import DFS, UCS, IDS, BFS, GBFS, Asearch
from level3 import A_star_search,gbfs
from level2 import Asearch2,UCS_2
#Test 1 of gbfs is intial fuel is sufficent to reach the goal due to matthan distances
#Test 2 of gbfs is the same test 1, but the car cant reach the goal due to the obstacles, so it should find another way 
#Test 3 of gbfs is a sample case of lv3 task 
#Test 4 of gbfs is initial fuel is not sufficent to reach the goal, so it find stations but cant reach the goal 
if __name__ == "__main__":
    pygame.init()
    window =pygame.display.set_mode((1500,700))
    screen_width = 1500
    screen_height = 700
    pygame.display.set_caption("Menu")
    window.fill("White")
    while True:
        MENU_MOUSE_POS =pygame.mouse.get_pos()
        
        MENU_TEXT = Visuallize.get_font(100).render("Choose the level",True,"Black")
        MENU_RECT = MENU_TEXT.get_rect(center=(screen_width  / 2, screen_height / 8))
        
        button_y_positions = [
            screen_height / 4,         # LVL1 button
            screen_height/ 4 + 100,   # LVL2 button
            screen_height / 4 + 200,   # LVL3 button
            screen_height / 4 + 300,   # LVL4 button
            screen_height / 4 + 400    # Quit button
        ]
        
        
        LVL1_BUTTON = Button(None, pos=(screen_width / 2, button_y_positions[0]), 
                             text_input="Level 1", font=Visuallize.get_font(75), base_color="Black", hovering_color="#8d8d8d")
        LVL2_BUTTON = Button(None, pos=(screen_width / 2, button_y_positions[1]), 
                                text_input="Level 2", font=Visuallize.get_font(75), base_color="Black", hovering_color="#8d8d8d")
        LVL3_BUTTON= Button(None, pos=(screen_width / 2, button_y_positions[2]), 
                        text_input="Level 3", font=Visuallize.get_font(75), base_color="Black", hovering_color="#8d8d8d")
        LVL4_BUTTON = Button(None, pos=(screen_width / 2, button_y_positions[3]), 
                        text_input="Level 4", font=Visuallize.get_font(75), base_color="Black", hovering_color="#8d8d8d")
        QUIT_BUTTON = Button(None, pos=(screen_width / 2, button_y_positions[4]), 
                             text_input="QUIT", font=Visuallize.get_font(75), base_color="Black", hovering_color="#8d8d8d")

        
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
                    # matrix,time,fuel = Visuallize.read_file("input1_level1.txt")
                    # board = Board(matrix, time, fuel)
                    # path = DFS()
                    # Visuallize.start(board,path)
                    
                    print("lvl1")
                if LVL2_BUTTON.checkForInput(MENU_MOUSE_POS):
                    print("lvl2")
                if LVL3_BUTTON.checkForInput(MENU_MOUSE_POS):
                    print("help")
                if LVL4_BUTTON.checkForInput(MENU_MOUSE_POS):
                    print("credits")
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

    # matrix,time,fuel = Visuallize.read_file("input1_level2.txt")
    # board = Board(matrix, time, fuel)
    # #Call search function here
    # path =  DFS(board)
    # print(path)
    # Visuallize.write_file('output.txt',path)
    # #Visualize map 
    # #print(limit)
    # Visuallize.start(board, path) 

    # matrix,time,fuel = Visuallize.read_file("input1_level2.txt")
    # board = Board(matrix, time, fuel)
    # path =  DFS(board)
    # Visuallize.menu(board,path)

    # matrix,time,fuel = Visuallize.read_file("input1_level2.txt")
    # board = Board(matrix, time, fuel)
    # #Call search function here

    # Visuallize.write_file('output.txt',path)
    # #Visualize map 
    # #print(limit)
    # vehicle = random.randint(1,9)
    # Visuallize.start_lvl4(board, path,vehicle) 
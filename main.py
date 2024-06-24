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
    with open(filepath,'r') as f:
        lines = f.readlines()
    # Tách dòng đầu để lấy số dòng và số cột
    first_line = lines[0].strip().split()
    num_rows = int(first_line[0])
    num_cols = int(first_line[1])

    # Tạo một mảng NumPy để lưu trữ dữ liệu
    matrix = np.zeros((num_rows, num_cols), dtype=int)

    # Duyệt qua các dòng còn lại để điền dữ liệu vào ma trận
    for i in range(1, num_rows + 1):
        row_data = lines[i].strip().split()
        for j in range(num_cols):
            if j < len(row_data):  # Kiểm tra chỉ số j có hợp lệ hay không
                value = row_data[j]
                if value.isdigit() or (value[0] == '-' and value[1:].isdigit()):
                    matrix[i-1, j] = int(value)
                elif value == 'S':
                    matrix[i -1 , j] = 2  # S được xem là 2
                elif value.startswith('S'):
                    matrix[i - 1, j] = int(value[1:]) + 10  # S1, S2, ... được xem là 11, 12, ...
                elif value.startswith('G'):
                    if value == 'G':
                        matrix[i-1,j] = 3
                    else:
                        matrix[i-1, j] = int(value[1:]) + 30  # G1, G2,.... được xem là 31,32,.....
                elif value.startswith('F'):
                    matrix[i-1, j] = int(value[1:]) + 20  # F1, F2, ... được xem là 21, 22, ...
                else:
                    raise ValueError(f"Unexpected value '{value}' in the input data.")
            else:
                raise IndexError(f"Index {j} out of range in row {i}.")
    return matrix

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
    matrix = read_file('input1_level1.txt')
    print(matrix)
    #Game loop
    run = True
    while run:
        for event in pygame.event.get():    
            if event.type == pygame.QUIT:
                run = False
        
        screen.fill((255,255,255))
        draw_map()
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] != 0:
                    if matrix[i][j] < 10:
                        if matrix[i][j] == -1:
                            highlight_BlockedCell(i,j)
                        elif matrix[i][j] == 2:
                            hightlight_SpecialCell(i,j,'S',3)
                        elif matrix[i][j] == 3:
                            hightlight_SpecialCell(i,j,'G',1)
                        else:
                            hightlight_SpecialCell(i,j,matrix[i][j],4)
                    elif matrix[i][j] > 10 and matrix[i][j] <20:
                        num = matrix[i][j] - 10
                        string = 'S' + str(num)
                        hightlight_SpecialCell(i,j,string,3)
                    elif matrix[i][j] > 20 and matrix[i][j] <30:
                        num = matrix[i][j] - 20
                        string = 'F' + str(num)
                        hightlight_SpecialCell(i,j,string,2)
                    else:
                        num = matrix[i][j] - 30
                        string = 'G' + str(num)
                        hightlight_SpecialCell(i,j,string,1)
        pygame.display.update()

    pygame.quit
    sys.exit()
    
if __name__ == "__main__":
    main()
import pygame
import sys

HIGHLIGHT = (173, 216, 230)
WHITE = (255,255,255)
BLACK = (0,0,0)
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

#Player
playerImg = pygame.image.load('car.png')
playerX = 370
playerY = 400

def player():
    screen.blit(playerImg,(playerX,playerY))

#Map
map_size = 50
rows,cols = 10,10
def draw_map():
    for row in range(rows):
        for col in range(cols):
            rect = pygame.Rect(col * map_size, row * map_size, map_size, map_size)
            pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)
#Highlight
selected_cells = [
    (2, 3, 5),
    (4, 5, 8),
    (6, 1, 3),
    (7, 8, 7),
]

def highlight_cell(row, col, number):
    rect = pygame.Rect(col * map_size, row * map_size, map_size, map_size)
    pygame.draw.rect(screen, HIGHLIGHT, rect)
    pygame.draw.rect(screen, BLACK, rect, 1)
    font = pygame.font.SysFont(None, 24)
    text = font.render(str(number), True, BLACK)
    text_rect = text.get_rect(center=(col * map_size + map_size // 2, row * map_size + map_size // 2))
    screen.blit(text, text_rect)
#Game loop
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    screen.fill((255,255,255))
    draw_map()
    player()
    for (row, col, number) in selected_cells:
        highlight_cell(row, col, number)
    pygame.display.update()

pygame.quit
sys.exit()
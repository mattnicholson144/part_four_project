"""
GUI
"""

import pygame
import numpy as np
 
# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
 
# Set the width and height of each grid point
point_width = 5
point_height = 5

# Margin between each grid point
grid_margin = 100

class GridPoint(pygame.sprite.Sprite):
    # Constructor 
    def __init__(self, x, y):
        # Call the parent's constructor
        super().__init__()
 
        # Set height, width
        self.image = pygame.Surface([point_width, point_height])
        self.image.fill(WHITE)
 
        # Make top left corner the passed-in location
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Initialise Pygame library 
pygame.init()

# Create a 16:9 screen
screen_height = 900
screen_width = 1600
screen = pygame.display.set_mode([screen_width, screen_height])

# Set the title of the window
pygame.display.set_caption('Pre-Start Simulator')

# Initialise font
pygame.font.init()
font_size = 24
myfont = pygame.font.SysFont('Calibri', font_size)

# Create arrays
allpointslist = pygame.sprite.Group()
grid_points = []
coords = []

# Populate arrays
npoints_x = 11
npoints_y = 7
for i in range(npoints_y):
    for j in range(npoints_x):
        x = int(j * grid_margin + screen_width / 2 - np.floor(npoints_x / 2) * grid_margin - np.floor(point_width / 2))
        y = int(i * grid_margin + screen_height / 2 - np.floor(npoints_y / 2) * grid_margin - np.floor(point_height / 2))
        point = GridPoint(x, y)
        coords.append((int(x + np.floor(point_width / 2)), int(y + np.floor(point_height / 2))))
        grid_points.append(point)
        allpointslist.add(point)

class Player():
    def __init__(self, x, y):
        self.x = x
        self.y = y

p1 = Player(coords[3][0], coords[3][1])
p2 = Player(coords[7][0], coords[7][1])

# Draw points and players on screen
allpointslist.draw(screen)
pygame.draw.circle(screen, GREEN, (int(p1.x + np.floor(point_width / 2)), int(p1.y + np.floor(point_height / 2))), 10)
pygame.draw.circle(screen, RED, (int(p2.x + np.floor(point_width / 2)), int(p2.y + np.floor(point_height / 2))), 10)

# Update display
pygame.display.update()

# Initialise turn tracking variables
MAX_TURNS = 3
turn = MAX_TURNS

# Execute game until complete
complete = False
while not complete:
    
    # Initialise turns
    player1_turn = True
    player2_turn = True
    
    # Remove old turns remaining
    screen.fill(BLACK, (100, 100, 110, font_size))
    
    # Display new turns remaining
    textsurface = myfont.render('Turns left: %d' % (turn), True, WHITE)
    screen.blit(textsurface, (100, 100))
    pygame.display.update()
    
    
    ######################## need to do this off indices, not coords somehow
    # Player 1 turn
    availablemoves = []
    try:
        availablemoves.append(coords[p1.x - 1][p1.y])
    except:
        print(p1.x - 1, p1.y)
    try:
        availablemoves.append(coords[p1.x + 1][p1.y])
    except:
        print('nope')
    try:
        availablemoves.append(coords[p1.x][p1.y - npoints_x])
    except:
        print('nope')
    try:
        availablemoves.append(coords[p1.x][p1.y + npoints_x])
    except:
        print('nope')
    
    print(availablemoves)
    # don't forget to delete availablemoves
    
    
    
    while player1_turn:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                player1_turn = False
    
    # Player 2 turn
    while player2_turn:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                player2_turn = False
                if (turn == 1):
                    complete = True
                    
    turn -= 1
                
pygame.quit()

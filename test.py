"""
GUI
"""

import pygame
import numpy as np
 
# Colours
WHITE = (255, 255, 255)
GREY = (127, 127, 127)
BLACK = (0, 0, 0)
RED = (255, 63, 63)
GREEN = (31, 223, 31)
BLUE = (0, 127, 255)
YELLOW = (223, 223, 31)
 
# Set the width, height and margin between of each grid point
point_width = 5
point_height = 5
grid_margin = 100

class GridPoint(pygame.sprite.Sprite):
    # Constructor 
    def __init__(self, x, y, colour):
        # Call the parent's constructor
        super().__init__()
 
        # Set height, width
        self.image = pygame.Surface([point_width, point_height])
        self.image.fill(colour)
 
        # Make passed in location the centre of the object
        self.rect = self.image.get_rect()
        self.rect.x = x - np.floor(point_width / 2)
        self.rect.y = y - np.floor(point_height / 2)

# Initialise Pygame library 
pygame.init()

# Create a 16:9 screen
screen_height = 900
screen_width = 1600
screen = pygame.display.set_mode([screen_width, screen_height])

# Set the title of the window
pygame.display.set_caption('America''s Cup Pre-Start Simulator')

# Initialise font
pygame.font.init()
font_size = 24
myfont = pygame.font.SysFont('Calibri', font_size)

# Create arrays
allpointslist = pygame.sprite.Group()
coords = []

# Populate arrays
npoints_x = 11
npoints_y = 7
for i in range(npoints_y):
    for j in range(npoints_x):
        x = int(j * grid_margin + screen_width / 2 - np.floor(npoints_x / 2) * grid_margin)
        y = int(i * grid_margin + screen_height / 2 - np.floor(npoints_y / 2) * grid_margin)
        point = GridPoint(x, y, GREY)
        allpointslist.add(point)
        coords.append((x, y))

class Player():
    def __init__(self, x, y, element):
        self.x = x
        self.y = y
        self.element = element
        self.turn = False
        
    def availableMoves(self, nx, ny, coords, screen, display):
        available_moves = []
        
        # Left (must be same row)
        if (np.floor((self.element - 1) / nx) == np.floor(self.element / nx)):
            available_moves.append(coords[self.element - 1])
        
        # Right (must be same row)
        if (np.floor((self.element + 1) / nx) == np.floor(self.element / nx)):
            available_moves.append(coords[self.element + 1])
        
        # Above (must not be bottom row)
        if (self.element - nx >= 0):
            available_moves.append(coords[self.element - nx])
        
        # Below (must not be top row)
        if (self.element + nx <= nx * ny - 1):
            available_moves.append(coords[self.element + nx])
        
        
        # Add available moves to list (and to override)
        available_points = pygame.sprite.Group()
        points_override = pygame.sprite.Group()
        for i in range(len(available_moves)):
            point = GridPoint(available_moves[i][0], available_moves[i][1], GREEN)
            available_points.add(point)
            point = GridPoint(available_moves[i][0], available_moves[i][1], GREY)
            points_override.add(point)
        
        # Draw available moves on screen
        available_points.draw(screen)
        display.update()
        
        return points_override
    
    def move(self, points, screen, display):
        points.draw(screen)
        display.update()

p1 = Player(coords[3][0], coords[3][1], 3)
p2 = Player(coords[7][0], coords[7][1], 7)

# Draw points and players on screen
allpointslist.draw(screen)
pygame.draw.circle(screen, RED, (p1.x, p1.y), 10)
pygame.draw.circle(screen, BLUE, (p2.x, p2.y), 10)
pygame.display.update()

# Initialise turns
MAX_TURNS = 3
turn = MAX_TURNS

# Display turns remaining
textsurface = myfont.render('Turns left: %d' % (turn), True, WHITE)
screen.blit(textsurface, (100, 100))
pygame.display.update()

# Execute game until complete
game_complete = False
p1.Turn = True
while not game_complete:
    
    
    # Player 1's turn
    while p1.Turn:
        
        # Show available moves
        base_grid_points = p1.availableMoves(npoints_x, npoints_y, coords, screen, pygame.display)
        
        # When user click is within area of available move, perform move
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:        # MOUSEBUTTONDOWN for clicking
                p1.move(base_grid_points, screen, pygame.display)
                p1.Turn = False
                p2.Turn = True
    
    # Player 2's turn
    while p2.Turn:
        
        # Show available moves
        base_grid_points = p2.availableMoves(npoints_x, npoints_y, coords, screen, pygame.display)
        
        # When user click is within area of available move, perform move
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                p2.move(base_grid_points, screen, pygame.display)
                p2.Turn = False
                p1.Turn = True
    
    
    # Number of turns left decrements
    turn -= 1
    
    # Display new turns remaining
    screen.fill(BLACK, (100, 100, 110, font_size))
    textsurface = myfont.render('Turns left: %d' % (turn), True, WHITE)
    screen.blit(textsurface, (100, 100))
    pygame.display.update()
                
    # If no turns left, end game
    if (turn == 0):
        game_complete = True

# Exit simulator
pygame.quit()

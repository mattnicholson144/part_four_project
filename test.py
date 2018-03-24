"""
GUI
"""

import pygame
import numpy as np
from policy import Policy

# ==========================================================================================
# Main GUI Class
class GUI():
    
    # Constants
    WHITE = (255, 255, 255)
    LIGHT_GREY = (253, 253, 253)
    GREY = (95, 95, 95)
    BLACK = (0, 0, 0)
    RED = (255, 63, 63)
    GREEN = (15, 243, 15)
    BLUE = (0, 127, 255)
    YELLOW = (223, 223, 31)
    
    point_width = 5
    point_height = 5
    screen_height = 900
    screen_width = 1600
    
    policy = Policy()
    
    # Constructor
    def __init__(self, npoints_x, npoints_y, grid_margin, max_turns):
        
        # Number of grid points and the distance between them
        self.npoints_x = npoints_x
        self.npoints_y = npoints_y
        self.grid_margin = grid_margin
        self.max_turns = max_turns
        
    # Grid points
    class GridPoint(pygame.sprite.Sprite):
        def __init__(self, x, y, colour):
            super().__init__()
 
            self.image = pygame.Surface([GUI.point_width, GUI.point_height])
            self.image.fill(colour)
 
            self.rect = self.image.get_rect()
            self.rect.x = x - np.floor(GUI.point_width / 2)
            self.rect.y = y - np.floor(GUI.point_height / 2)
    
    class Player():
        def __init__(self, x, y, element, colour, radius):
            self.x = x
            self.y = y
            self.element = element
            self.colour = colour
            self.radius = radius
            self.turn = False
            self.policy = False
             
        def availableMoves(self, nx, ny, coords, screen, display, other_player):
            available_moves = []
            element = []
            
            # Left (must be same row and other player must not be there)
            if (np.floor((self.element - 1) / nx) == np.floor(self.element / nx) and coords[self.element - 1] != (other_player.x, other_player.y)):
                available_moves.append(coords[self.element - 1])
                element.append(self.element - 1)
             
            # Right (must be same row and other player must not be there)
            if (np.floor((self.element + 1) / nx) == np.floor(self.element / nx) and coords[self.element + 1] != (other_player.x, other_player.y)):
                available_moves.append(coords[self.element + 1])
                element.append(self.element + 1)
             
            # Above (must not be bottom row and other player must not be there)
            if (self.element - nx >= 0 and coords[self.element - nx] != (other_player.x, other_player.y)):
                available_moves.append(coords[self.element - nx])
                element.append(self.element - nx)
             
            # Below (must not be top row and other player must not be there)
            if (self.element + nx <= nx * ny - 1 and coords[self.element + nx] != (other_player.x, other_player.y)):
                available_moves.append(coords[self.element + nx])
                element.append(self.element + nx)
             
             
            # Add available moves to list (and to override)
            available_points = pygame.sprite.Group()
            points_override = pygame.sprite.Group()
            for i in range(len(available_moves)):
                point = GUI.GridPoint(available_moves[i][0], available_moves[i][1], GUI.GREEN)
                available_points.add(point)
                point = GUI.GridPoint(available_moves[i][0], available_moves[i][1], GUI.GREY)
                points_override.add(point)
             
            # Draw available moves on screen
            available_points.draw(screen)
            display.update()
             
            return available_moves, element, points_override
         
        def move(self, move, element, points, screen, screen_colour, display):
             
            # Override old position
            old_grid_point = GUI.GridPoint(self.x, self.y, GUI.GREY)
            old_x = self.x
            old_y = self.y
            old_position = pygame.sprite.Group()
            old_position.add(old_grid_point)
             
            # Update player position based on move
            self.x = move[0]
            self.y = move[1]
            self.element = element
             
            # Override grid points back to normal colour and old player position
            pygame.draw.circle(screen, screen_colour, (old_x, old_y), self.radius)
            old_position.draw(screen)
             
            points.draw(screen)
            pygame.draw.circle(screen, self.colour, (self.x, self.y), self.radius)
             
            # Update display
            display.update()
            
        def haveTurn(self, other_player, npoints_x, npoints_y, coords, screen, screen_colour, display):
            
            # Show available moves
            possible_moves, move_element, base_grid_points = self.availableMoves(npoints_x, npoints_y, coords, screen, display, other_player)
            
            # If not a player
            if self.policy:
                
                # Show possible moves before moving (delay in milliseconds)
                if not other_player.policy:
                    pygame.time.delay(2500)
                
                # Array of possible next move coordinates
                i_next = []
                j_next = []
                for i in range(len(possible_moves)):
                    i_next.append(possible_moves[i][0])
                    j_next.append(possible_moves[i][1])
                
                # Other players' current coordinates
                k = other_player.x
                l = other_player.y
                
                # Store other player's coordinates in a list
                GUI.policy.i_history.append(other_player.x)
                GUI.policy.j_history.append(other_player.y)
                
                # Implement policy
                element = GUI.policy.valueFunction(i_next, j_next, k, l)
                
                # Move based on policy's decision
                self.move(possible_moves[element], move_element[element], base_grid_points, screen, screen_colour, display)
                         
                # End turn
                self.Turn = False
                other_player.Turn = True
                
            # If a player
            else:
                
                # When user click is within area of available move, perform move
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                         
                        # Coordinates of mouse click
                        x_click = pygame.mouse.get_pos()[0]
                        y_click = pygame.mouse.get_pos()[1]
                         
                        # Check if mouse click near any possible moves
                        index = -1
                        for i in range(len(possible_moves)):
                            if (np.abs(x_click - possible_moves[i][0]) < 3 * GUI.point_width) and (np.abs(y_click - possible_moves[i][1]) < 3 * GUI.point_height):
                                index = i
                                # Click can not be near to any other possible move
                                break
                         
                        # Move player to selected position (if a position has been selected)
                        if (index != -1):
                            self.move(possible_moves[index], move_element[index], base_grid_points, screen, screen_colour, display)
                         
                            # End turn
                            self.Turn = False
                            other_player.Turn = True
    
    # Create GUI
    def createAndShowGUI(self):
        
        # Initialise 'Pygame'
        pygame.init()
        self.screen = pygame.display.set_mode([GUI.screen_width, GUI.screen_height])
        self.screen_colour = GUI.LIGHT_GREY
        self.screen.fill(self.screen_colour)
        pygame.display.set_caption('America''s Cup Pre-Start Simulator')
        
        # Font setup
        pygame.font.init()
        self.font_size = 24
        self.my_font = pygame.font.SysFont('Calibri', self.font_size)
        
        # Create arrays
        self.all_grid_points = pygame.sprite.Group()
        self.coords = []
        
        # Populate arrays
        for i in range(self.npoints_y):
            for j in range(self.npoints_x):
                x = int(j * self.grid_margin + GUI.screen_width / 2 - np.floor(self.npoints_x / 2) * self.grid_margin)
                y = int(i * self.grid_margin + GUI.screen_height / 2 - np.floor(self.npoints_y / 2) * self.grid_margin)
                point = GUI.GridPoint(x, y, GUI.GREY)
                self.all_grid_points.add(point)
                self.coords.append((x, y))
        
        # Initialise players
        self.p1 = GUI.Player(self.coords[3][0], self.coords[3][1], 3, GUI.RED, 10)
        self.p2 = GUI.Player(self.coords[7][0], self.coords[7][1], 7, GUI.BLUE, 10)
        
        # Show turns remaining
        self.current_turn = self.max_turns
        self.turn_text_colour = GUI.BLACK
        self.text_surface = self.my_font.render('Turns remaining: %d' % (self.current_turn), True, self.turn_text_colour)
        
        # Draw objects on screen
        self.all_grid_points.draw(self.screen)
        pygame.draw.circle(self.screen, self.p1.colour, (self.p1.x, self.p1.y), self.p1.radius)
        pygame.draw.circle(self.screen, self.p2.colour, (self.p2.x, self.p2.y), self.p2.radius)
        self.screen.blit(self.text_surface, (100, 100))
        pygame.display.update()
        
    def playGame(self):
        
        # Play game until complete
        self.game_complete = False
        self.p1.Turn = True
        
        
        
        self.p2.policy = True #===================== somehow get this from user option
        
        
        
        while not self.game_complete:
            
            # Player 1's turn
            while self.p1.Turn:
                self.p1.haveTurn(self.p2, self.npoints_x, self.npoints_y, self.coords, self.screen, self.screen_colour, pygame.display)
                
            # Player 2's turn
            while self.p2.Turn:
                self.p2.haveTurn(self.p1, self.npoints_x, self.npoints_y, self.coords, self.screen, self.screen_colour, pygame.display)
            
            #Number of turns remaining decrements
            self.current_turn -= 1
     
            # Display new turns remaining (MAKE THIS A METHOD)
            self.screen.fill(self.screen_colour, (100, 100, 185, self.font_size))
            self.text_surface = self.my_font.render('Turns remaining: %d' % (self.current_turn), True, self.turn_text_colour)
            self.screen.blit(self.text_surface, (100, 100))
            pygame.display.update()
                         
            # If no turns remaining, end game
            if (self.current_turn == 0):
                self.game_complete = True
         
    def execute(self):
        
        # Execute game methods in order
        self.createAndShowGUI()
        self.playGame()
        
        # Exit simulator (HAVE AN END GAME SCREEN)
        pygame.quit()
# ==========================================================================================


# Create GUI object
gameGUI = GUI(11, 7, 100, 10) # xpoints, ypoints, pointmargin, maxturns
gameGUI.execute()

# Testing
# in playGame(), self.p2.policy = True
# in GUI, Policy is an object

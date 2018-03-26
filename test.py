"""
GUI
"""

import pygame
import numpy as np
<<<<<<< HEAD
from dp_policy import Policy
=======
from policy import Policy
>>>>>>> 8c0937fcf20deb78fc716b1933939e40315fed62

# ==========================================================================================
# Main GUI Class
class GUI():
    
    # Constants
    WHITE = (255, 255, 255)
    LIGHT_GREY = (253, 253, 253)
    GREY = (95, 95, 95)
    BLACK = (0, 0, 0)
    RED = (255, 63, 63)
    LIGHT_GREEN = (63, 243, 63)
    GREEN = (63, 223, 63)
    BLUE = (0, 127, 255)
    YELLOW = (223, 223, 31)
    
    point_width = 5
    point_height = 5
    screen_height = 900
    screen_width = 1600
    
<<<<<<< HEAD
=======
    policy = Policy()
    
>>>>>>> 8c0937fcf20deb78fc716b1933939e40315fed62
    # Constructor
    def __init__(self, npoints_x, npoints_y, grid_margin, max_turns):
        
        # Number of grid points and the distance between them
        self.npoints_x = npoints_x
        self.npoints_y = npoints_y
        self.grid_margin = grid_margin
        self.max_turns = max_turns
<<<<<<< HEAD
        self.policy = Policy()
=======
>>>>>>> 8c0937fcf20deb78fc716b1933939e40315fed62
        
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
<<<<<<< HEAD
            self.turn_history = []
=======
>>>>>>> 8c0937fcf20deb78fc716b1933939e40315fed62
             
        def availableMoves(self, nx, ny, coords, screen, display, other_player):
            available_moves = []
            element = []
            
<<<<<<< HEAD
            # Left (must be same row and other player must not be there and this player can't have been there last move)
            if (np.floor((self.element - 1) / nx) == np.floor(self.element / nx) and 
                    coords[self.element - 1] != (other_player.x, other_player.y) and
                    coords[self.element - 1] != self.turn_history[-1]):
                available_moves.append(coords[self.element - 1])
                element.append(self.element - 1)
             
            # Right (must be same row and other player must not be there and this player can't have been there last move)
            if (np.floor((self.element + 1) / nx) == np.floor(self.element / nx) and 
                    coords[self.element + 1] != (other_player.x, other_player.y) and
                    coords[self.element + 1] != self.turn_history[-1]):
                available_moves.append(coords[self.element + 1])
                element.append(self.element + 1)
             
            # Above (must not be bottom row and other player must not be there and this player can't have been there last move)
            if (self.element - nx >= 0 and 
                    coords[self.element - nx] != (other_player.x, other_player.y) and
                    coords[self.element - nx] != self.turn_history[-1]):
                available_moves.append(coords[self.element - nx])
                element.append(self.element - nx)
             
            # Below (must not be top row and other player must not be there and this player can't have been there last move)
            if (self.element + nx <= nx * ny - 1 and 
                    coords[self.element + nx] != (other_player.x, other_player.y) and
                    coords[self.element + nx] != self.turn_history[-1]):
                available_moves.append(coords[self.element + nx])
                element.append(self.element + nx)
             
=======
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
             
             
>>>>>>> 8c0937fcf20deb78fc716b1933939e40315fed62
            # Add available moves to list (and to override)
            available_points = pygame.sprite.Group()
            points_override = pygame.sprite.Group()
            for i in range(len(available_moves)):
                point = GUI.GridPoint(available_moves[i][0], available_moves[i][1], GUI.LIGHT_GREEN)
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
            
<<<<<<< HEAD
        def haveTurn(self, other_player, policy_table, current_turn, npoints_x, npoints_y, grid_margin, coords, screen, screen_colour, display):
=======
        def haveTurn(self, other_player, npoints_x, npoints_y, coords, screen, screen_colour, display):
>>>>>>> 8c0937fcf20deb78fc716b1933939e40315fed62
            
            # Show available moves
            possible_moves, move_element, base_grid_points = self.availableMoves(npoints_x, npoints_y, coords, screen, display, other_player)
            
            # If not a player
            if self.policy:
                
                # Show possible moves before moving (delay in milliseconds)
<<<<<<< HEAD
                pygame.time.delay(1000)
                
                # Normalise coordinates
                min_x = coords[0][0]
                min_y = coords[0][1]
                possible_grid_points = []
                for i in range(len(possible_moves)):
                    possible_grid_points.append((int((possible_moves[i][0] - min_x) / grid_margin), int((possible_moves[i][1] - min_y) / grid_margin)))
                
                # If this is player 1
                if self.player1 == True:
                    
                    # Define values to call policy table
                    i_vals = []
                    j_vals = []
                    for i in range(len(possible_grid_points)):
                        i_vals.append(possible_grid_points[i][1])
                        j_vals.append(possible_grid_points[i][0])
                    k = int((other_player.y - min_y) / grid_margin)
                    l = int((other_player.x - min_x) / grid_margin)
                    t = current_turn * 2 - 1
                    
                    # Find maximum value and element from table
                    min = np.inf
                    element = -1
                    for ind in range(len(possible_grid_points)):
                        temp = policy_table[t][i_vals[ind]][j_vals[ind]][k][l]
                        if temp < min:
                            min = temp
                            element = ind
                    
                    # Save current position to turn history before moving
                    self.turn_history.append((self.x, self.y))
                    
                    # Move based on maximum policy value
                    self.move(possible_moves[element], move_element[element], base_grid_points, screen, screen_colour, display)
            
                # If this is player 2
                else:
                    
                    # Define values to call policy table
                    k_vals = []
                    l_vals = []
                    for i in range(len(possible_grid_points)):
                        k_vals.append(possible_grid_points[i][1])
                        l_vals.append(possible_grid_points[i][0])
                    i = int((other_player.y - min_y) / grid_margin)
                    j = int((other_player.x - min_x) / grid_margin)
                    t = current_turn * 2 - 2
                    
                    # Find maximum value and element from table
                    max = -np.inf
                    element = -1
                    for ind in range(len(possible_grid_points)):
                        temp = policy_table[t][i][j][k_vals[ind]][l_vals[ind]]
                        if temp > max:
                            max = temp
                            element = ind
                    
                    # Save current position to turn history before moving
                    self.turn_history.append((self.x, self.y))
                    
                    # Move based on maximum policy value
                    self.move(possible_moves[element], move_element[element], base_grid_points, screen, screen_colour, display)
                
=======
                pygame.time.delay(1500)
                
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
                         
>>>>>>> 8c0937fcf20deb78fc716b1933939e40315fed62
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
        
<<<<<<< HEAD
        # Initialise and populate policy table
        self.policy.table = self.policy.initialise_policy_table(self.max_turns * 2, self.npoints_y, self.npoints_x)
        self.policy.table = self.policy.populate_policy_table(self.policy.table, self.max_turns * 2, self.npoints_y, self.npoints_x)
        
=======
>>>>>>> 8c0937fcf20deb78fc716b1933939e40315fed62
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
        
        # Draw grid points on screen
        self.all_grid_points.draw(self.screen)
        pygame.display.update()
    
    def initialiseGameMode(self):
        
        # Game mode text surfaces
        game_mode_text_surface = self.my_font.render('Select game mode', True, GUI.BLACK)
        mode_text_surfaces = []
        mode_text_surfaces.append(self.my_font.render('Person vs. Person', True, GUI.LIGHT_GREY))
        mode_text_surfaces.append(self.my_font.render('Person vs. Policy', True, GUI.LIGHT_GREY))
        mode_text_surfaces.append(self.my_font.render('Policy vs. Policy', True, GUI.LIGHT_GREY))
        
        # Button positions (xpos, ypos, width, height)
        buttons = []
        increment = 50
        for i in range(len(mode_text_surfaces)):
            buttons.append((50, 300 + i * increment, mode_text_surfaces[i].get_size()[0], mode_text_surfaces[i].get_size()[1]))
        
        # Game mode backgrounds
        button_backgrounds = []
        colour_list = [GUI.RED, GUI.BLUE, GUI.GREEN]
        for i in range(len(buttons)):
            button_backgrounds.append(pygame.Surface((buttons[i][2], buttons[i][3])))
            button_backgrounds[i].fill(colour_list[i])
        
        # Draw background and text surfaces
        self.screen.blit(game_mode_text_surface, (50, 250))
        for i in range(len(buttons)):
            self.screen.blit(button_backgrounds[i], (buttons[i][0], buttons[i][1]))
            self.screen.blit(mode_text_surfaces[i], (buttons[i][0], buttons[i][1]))
        pygame.display.update()
        
        # Wait until a game mode has been selected
        game_mode = False
        while not game_mode:
            
            # When user click is within area of button, select game mode
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                     
                    # Coordinates of mouse click
                    x_click = pygame.mouse.get_pos()[0]
                    y_click = pygame.mouse.get_pos()[1]
                     
                    # Check if mouse click inside any game mode button
                    index = -1
                    for i in range(len(buttons)):
                        if (x_click >= buttons[i][0] and x_click <= buttons[i][0] + buttons[i][2] - 1 and y_click >= buttons[i][1] and y_click <= buttons[i][1] + buttons[i][3] - 1):
                            index = i
                            game_mode = True
                            # Click can not be within any other button
                            break
                     
                    # Select game mode (if a game mode has been selected)
                    if (index != -1):
                        
                        # Initialise players
                        p1_pos = int((4.0 / 11.0) * self.npoints_x - 1)
                        p2_pos = self.npoints_x - p1_pos - 1
<<<<<<< HEAD
                        #self.p1 = GUI.Player(self.coords[p1_pos][0], self.coords[p1_pos][1], p1_pos, GUI.RED, 10)
                        self.p1 = GUI.Player(self.coords[34][0], self.coords[34][1], 34, GUI.RED, 20)
                        self.p1.player1 = True
                        self.p1.turn_history.append((self.p1.x, self.p1.y))
                        #self.p2 = GUI.Player(self.coords[p2_pos][0], self.coords[p2_pos][1], p2_pos, GUI.BLUE, 10)
                        self.p2 = GUI.Player(self.coords[24][0], self.coords[24][1], 24, GUI.BLUE, 20)
                        self.p2.player1 = False
                        self.p2.turn_history.append((self.p2.x, self.p2.y))
=======
                        self.p1 = GUI.Player(self.coords[p1_pos][0], self.coords[p1_pos][1], p1_pos, GUI.RED, 10)
                        self.p2 = GUI.Player(self.coords[p2_pos][0], self.coords[p2_pos][1], p2_pos, GUI.BLUE, 10)
>>>>>>> 8c0937fcf20deb78fc716b1933939e40315fed62
                        
                        # Person vs. Policy
                        if (index == 1):
                            self.p2.policy = True
                        
                        # Policy vs. Policy
                        if (index == 2):
                            self.p1.policy = True
                            self.p2.policy = True
        
        # Remove game mode text and buttons
        game_mode_text_surface.fill(self.screen_colour)
        self.screen.blit(game_mode_text_surface, (50, 250))
        
        for i in range(len(buttons)):
            button_backgrounds[i].fill(self.screen_colour)
            self.screen.blit(button_backgrounds[i], (buttons[i][0], buttons[i][1]))
        pygame.display.update()
        
        # Show turns remaining
        self.current_turn = self.max_turns
        self.turn_text_colour = GUI.BLACK
        self.text_surface = self.my_font.render('Turns remaining: %d' % (self.current_turn), True, self.turn_text_colour)
        
        # Draw players and turns remaining on screen
        pygame.draw.circle(self.screen, self.p1.colour, (self.p1.x, self.p1.y), self.p1.radius)
        pygame.draw.circle(self.screen, self.p2.colour, (self.p2.x, self.p2.y), self.p2.radius)
        self.text_x = 50
        self.text_y = 150
        self.screen.blit(self.text_surface, (self.text_x, self.text_y))
        pygame.display.update()
        
    def playGame(self):
        
        # Play game until complete
        self.game_complete = False
        self.p1.Turn = True
        
        while not self.game_complete:
            
            # Player 1's turn
            while self.p1.Turn:
<<<<<<< HEAD
                self.p1.haveTurn(self.p2, self.policy.table, self.current_turn, self.npoints_x, self.npoints_y, self.grid_margin, self.coords, self.screen, self.screen_colour, pygame.display)
                
            # Player 2's turn
            while self.p2.Turn:
                self.p2.haveTurn(self.p1, self.policy.table, self.current_turn, self.npoints_x, self.npoints_y, self.grid_margin, self.coords, self.screen, self.screen_colour, pygame.display)
=======
                self.p1.haveTurn(self.p2, self.npoints_x, self.npoints_y, self.coords, self.screen, self.screen_colour, pygame.display)
                
            # Player 2's turn
            while self.p2.Turn:
                self.p2.haveTurn(self.p1, self.npoints_x, self.npoints_y, self.coords, self.screen, self.screen_colour, pygame.display)
>>>>>>> 8c0937fcf20deb78fc716b1933939e40315fed62
            
            #Number of turns remaining decrements
            self.current_turn -= 1
     
            # Display new turns remaining (MAKE THIS A METHOD)
            self.screen.fill(self.screen_colour, (self.text_x, self.text_y, self.text_surface.get_size()[0], self.font_size))
            self.text_surface = self.my_font.render('Turns remaining: %d' % (self.current_turn), True, self.turn_text_colour)
            self.screen.blit(self.text_surface, (self.text_x, self.text_y))
            pygame.display.update()
                         
            # If no turns remaining, end game
            if (self.current_turn == 0):
                self.game_complete = True
         
    def execute(self):
        
        # Execute game methods in order
        self.createAndShowGUI()
        self.initialiseGameMode()
        self.playGame()
        
        # Exit simulator (HAVE AN END GAME SCREEN)
        pygame.quit()
# ==========================================================================================










# Create GUI object
<<<<<<< HEAD
gameGUI = GUI(11, 7, 100, 4) # xpoints, ypoints, pointmargin, maxturns
gameGUI.execute()

# NOTE: for policy testing, Policy is a class attribute of GUI
#test = Policy()
#test.policy.table = self.policy.initialise_policy_table(6, 7, 11)
#test.policy.table = self.policy.populate_policy_table(test.policy.table, 6, 7, 11)

=======
gameGUI = GUI(11, 7, 100, 5) # xpoints, ypoints, pointmargin, maxturns
gameGUI.execute()

# NOTE: for policy testing, Policy is a class attribute of GUI
>>>>>>> 8c0937fcf20deb78fc716b1933939e40315fed62

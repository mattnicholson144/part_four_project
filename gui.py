"""
GUI
"""

import pygame
import numpy as np
from dp_policy import Policy

# ==========================================================================================
# Main GUI Class
class GUI():
    
    # Constants
    WHITE = (255, 255, 255)
    LIGHT_GREY = (253, 253, 253)
    GREY = (95, 95, 95)
    BLACK = (0, 0, 0)
    RED = (255, 63, 63)
    GREEN = (63, 223, 63)
    BLUE = (0, 127, 255)
    YELLOW = (247, 247, 31)
    
    screen_width = 1600
    screen_height = 900
    game_width = 1240
    game_height = 790
    
    point_width = 6
    point_height = 6
    player_radius = 15

    # Constructor
    def __init__(self, npoints_x, npoints_y, p1_start, p2_start, max_turns):
        
        # Number of grid points and the distance between them
        self.npoints_x = npoints_x
        self.npoints_y = npoints_y
        
        # Initial player positions
        self.p1_start = p1_start
        self.p2_start = p2_start
        
        # Number of turns each player has
        self.max_turns = max_turns
        
        # Policy both players use
        self.policy = Policy()
        
        # Play game
        self.createAndShowGUI()
        self.execute()
        
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
            self.turn_history = []
            self.is_bumped = False
             
        def availableMoves(self, nx, ny, coords, screen, screen_colour, display, my_font, other_player):
            available_moves = []
            element = []
            can_bump = False
            bump_element = -1
            
            # Left (must be same row and other player may be there to bump)
            if (np.floor((self.element - 1) / nx) == np.floor(self.element / nx)):
                available_moves.append(coords[self.element - 1])
                element.append(self.element - 1)
                
                # If other player is there (therefore a bump)
                if coords[self.element - 1] == (other_player.x, other_player.y):
                    can_bump = True
                    bump_element = 0
             
            # Right (must be same row and other player must not be there)
            if (np.floor((self.element + 1) / nx) == np.floor(self.element / nx) 
                and coords[self.element + 1] != (other_player.x, other_player.y)):
                available_moves.append(coords[self.element + 1])
                element.append(self.element + 1)
                
                # If other player has just bumped you, cannot move through them
                if self.is_bumped:
                    available_moves.pop()
                    element.pop()
                
            # Above (must not be bottom row and other player must not be there)
            if (self.element - nx >= 0 
                and coords[self.element - nx] != (other_player.x, other_player.y)):
                available_moves.append(coords[self.element - nx])
                element.append(self.element - nx)
             
            # Below (must not be top row and other player must not be there)
            if (self.element + nx <= nx * ny - 1 
                and coords[self.element + nx] != (other_player.x, other_player.y)):
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
            
            # Draw bump circle and notify on screen if can bump
            if can_bump:
                pygame.draw.circle(screen, GUI.GREEN, available_moves[0], int(np.ceil(max(GUI.point_width, GUI.point_height) / np.sqrt(2))) + 1)
                
                # Draw notification box
                bump_outside_box = pygame.Rect(25, 425, 225, 200)
                bump_inside_box = pygame.Rect(30, 430, 215, 190)
                pygame.draw.rect(screen, GUI.GREEN, bump_outside_box)
                pygame.draw.rect(screen, screen_colour, bump_inside_box)
                
                # If red can bump, red text on top
                if self.player1:
                    red_pos = (95, 455)
                    blue_pos = (87, 555)
                
                # If blue can bump, blue text on top
                else:
                    blue_pos = (87, 455)
                    red_pos = (95, 555)
                
                # Display message
                colour_font = pygame.font.SysFont('Calibri', 48)
                red_surface = colour_font.render('RED', True, GUI.RED)
                blue_surface = colour_font.render('BLUE', True, GUI.BLUE)
                can_bump_surface = my_font.render('can bump', True, GUI.GREY)
                
                screen.blit(can_bump_surface, (90, 515))
                screen.blit(red_surface, red_pos)
                screen.blit(blue_surface, blue_pos)
            
            # Draw available moves on screen
            available_points.draw(screen)
            
            display.update()
             
            return available_moves, element, bump_element, points_override
         
        def move(self, move, element, bump_element, points, screen, screen_colour, display, my_font, other_player):
            
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
            
            # If move is a bump
            if bump_element:
                
                # Override grid points back to normal colour and old player position
                pygame.draw.circle(screen, screen_colour, (old_x, old_y), self.radius)
                old_position.draw(screen)
                 
                points.draw(screen)
                pygame.draw.circle(screen, self.colour, (self.x, self.y), self.radius - 2)
                
                # Draw notification box
                bump_inside_box = pygame.Rect(30, 430, 215, 190)
                pygame.draw.rect(screen, screen_colour, bump_inside_box)
                
                # If red is bumping, blue text on top
                if self.player1:
                    blue_pos = (87, 455)
                    red_pos = (95, 555)
                
                # If blue is bumping, red text on top
                else:
                    red_pos = (95, 455)
                    blue_pos = (87, 555)
                
                # Display message
                colour_font = pygame.font.SysFont('Calibri', 48)
                red_surface = colour_font.render('RED', True, GUI.RED)
                blue_surface = colour_font.render('BLUE', True, GUI.BLUE)
                is_hidden_surface = my_font.render('is bumped under', True, GUI.GREY)
                
                screen.blit(is_hidden_surface, (60, 515))
                screen.blit(red_surface, red_pos)
                screen.blit(blue_surface, blue_pos)
                
                # Other player is now bumped
                other_player.is_bumped = True
            
            # If coming out of a bump
            elif self.is_bumped:
                
                # Override grid points back to normal colour and old player position
                pygame.draw.circle(screen, other_player.colour, (old_x, old_y), other_player.radius)
                 
                points.draw(screen)
                pygame.draw.circle(screen, self.colour, (self.x, self.y), self.radius)
                
                # Remove notification box
                bump_outside_box = pygame.Rect(25, 425, 225, 200)
                pygame.draw.rect(screen, screen_colour, bump_outside_box)
                
                # Not bumped anymore
                self.is_bumped = False
                
            # Move is not related to a bump
            else:
                
                # Override grid points back to normal colour and old player position
                pygame.draw.circle(screen, screen_colour, (old_x, old_y), self.radius)
                old_position.draw(screen)
                 
                points.draw(screen)
                pygame.draw.circle(screen, self.colour, (self.x, self.y), self.radius)
             
            # Update display
            display.update()
            
        def haveTurn(self, other_player, policy_table, current_turn, npoints_x, npoints_y, grid_margin_x, grid_margin_y, coords, screen, screen_colour, my_font, display):
            
            # Show available moves
            possible_moves, move_element, bump_element, base_grid_points = self.availableMoves(npoints_x, npoints_y, coords, screen, screen_colour, display, my_font, other_player)
            
            # If not a person
            if self.policy:
                
                # Show possible moves before moving (delay in milliseconds)
                pygame.time.delay(2000)
                
                # Normalise coordinates
                min_x = coords[0][0]
                min_y = coords[0][1]
                possible_grid_points = []
                for i in range(len(possible_moves)):
                    possible_grid_points.append((int((possible_moves[i][0] - min_x) / grid_margin_x), int((possible_moves[i][1] - min_y) / grid_margin_y)))
                
                # If this is player 1
                if self.player1 == True:
                    
                    # Define values to call policy table
                    i_vals = []
                    j_vals = []
                    for i in range(len(possible_grid_points)):
                        i_vals.append(possible_grid_points[i][1])
                        j_vals.append(possible_grid_points[i][0])
                    k = int((other_player.y - min_y) / grid_margin_y)
                    l = int((other_player.x - min_x) / grid_margin_x)
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
                    self.move(possible_moves[element], move_element[element], (element == bump_element), base_grid_points, screen, screen_colour, display, my_font, other_player)
            
                # If this is player 2
                else:
                    
                    # Define values to call policy table
                    k_vals = []
                    l_vals = []
                    for k in range(len(possible_grid_points)):
                        k_vals.append(possible_grid_points[k][1])
                        l_vals.append(possible_grid_points[k][0])
                    i = int((other_player.y - min_y) / grid_margin_y)
                    j = int((other_player.x - min_x) / grid_margin_x)
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
                    self.move(possible_moves[element], move_element[element], (element == bump_element), base_grid_points, screen, screen_colour, display, my_font, other_player)
                
                # End turn
                self.Turn = False
                other_player.Turn = True
                
            # If a person
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
                            self.move(possible_moves[index], move_element[index], (index == bump_element), base_grid_points, screen, screen_colour, display, my_font, other_player)
                         
                            # End turn
                            self.Turn = False
                            other_player.Turn = True
    
    # Create GUI
    def createAndShowGUI(self):
        
        # Initialise and populate policy table
        self.policy.table = self.policy.initialise_policy_table(self.max_turns * 2, self.npoints_y, self.npoints_x)
        self.policy.table = self.policy.populate_policy_table(self.policy.table, self.max_turns * 2, self.npoints_y, self.npoints_x)
        
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
        self.coords = []
        self.all_grid_points = pygame.sprite.Group()
        self.hidden_grid_points = pygame.sprite.Group()
        
        # Calculate grid margins and offset (due to game screen on right)
        self.grid_margin_x = np.floor(self.game_width / (self.npoints_x - 1))
        self.grid_margin_y = np.floor(self.game_height / (self.npoints_y - 1))
        offset_x = 125
        
        # Populate arrays (grid points are shown after game mode selected)
        x_start = GUI.screen_width / 2 + offset_x - ((self.npoints_x - 1) / 2) * self.grid_margin_x
        y_start = GUI.screen_height / 2 - ((self.npoints_y - 1) / 2) * self.grid_margin_y
        for i in range(self.npoints_y):
            for j in range(self.npoints_x):
                x = int(j * self.grid_margin_x + x_start)
                y = int(i * self.grid_margin_y + y_start)
                self.coords.append((x, y))
                
                # Shown points
                point = GUI.GridPoint(x, y, GUI.GREY)
                self.all_grid_points.add(point)
                
                # Hidden points
                hidden_point = GUI.GridPoint(x, y, self.screen_colour)
                self.hidden_grid_points.add(hidden_point)
                
        # Draw play grid
        grid_box = pygame.Rect(275, 25, 1300, 850)
        inside_box = pygame.Rect(280, 30, 1290, 840)
        pygame.draw.rect(self.screen, GUI.GREY, grid_box)
        pygame.draw.rect(self.screen, GUI.LIGHT_GREY, inside_box)
        
        pygame.display.update()
    
    def initialiseGameMode(self):
        
        # Game mode text surfaces
        game_mode_text_surface = self.my_font.render('Select game mode', True, GUI.GREY)
        mode_text_surfaces = []
        mode_text_surfaces.append(self.my_font.render('Person vs. Person', True, GUI.LIGHT_GREY))
        mode_text_surfaces.append(self.my_font.render('Person vs. Policy', True, GUI.LIGHT_GREY))
        mode_text_surfaces.append(self.my_font.render('Policy vs. Policy', True, GUI.LIGHT_GREY))
        
        # Button positions (xpos, ypos, width, height)
        buttons = []
        increment = 50
        for i in range(len(mode_text_surfaces)):
            buttons.append((50, 150 + i * increment, mode_text_surfaces[i].get_size()[0], mode_text_surfaces[i].get_size()[1]))
        
        # Game mode backgrounds
        button_backgrounds = []
        colour_list = [GUI.RED, GUI.BLUE, GUI.GREEN]
        for i in range(len(buttons)):
            button_backgrounds.append(pygame.Surface((buttons[i][2], buttons[i][3])))
            button_backgrounds[i].fill(colour_list[i])
        
        # Draw background and text surfaces
        self.screen.blit(game_mode_text_surface, (50, 100))
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
                        if (x_click >= buttons[i][0] and x_click <= buttons[i][0] + buttons[i][2] - 1 
                            and y_click >= buttons[i][1] and y_click <= buttons[i][1] + buttons[i][3] - 1):
                            index = i
                            game_mode = True
                            # Click can not be within any other button
                            break
                     
                    # Select game mode (if a game mode has been selected)
                    if (index != -1):
                        
                        # Initialise players
                        p1_pos = self.p1_start[0] * self.npoints_x + self.p1_start[1]
                        p2_pos = self.p2_start[0] * self.npoints_x + self.p2_start[1]

                        self.p1 = GUI.Player(self.coords[p1_pos][0], self.coords[p1_pos][1], p1_pos, GUI.RED, GUI.player_radius)
                        self.p1.player1 = True

                        self.p2 = GUI.Player(self.coords[p2_pos][0], self.coords[p2_pos][1], p2_pos, GUI.BLUE, GUI.player_radius)
                        self.p2.player1 = False
                        
                        # Person vs. Policy
                        if (index == 1):
                            self.p2.policy = True
                        
                        # Policy vs. Policy
                        if (index == 2):
                            self.p1.policy = True
                            self.p2.policy = True
        
        # Remove game mode text and buttons
        game_mode_text_surface.fill(self.screen_colour)
        self.screen.blit(game_mode_text_surface, (50, 100))
        
        for i in range(len(buttons)):
            button_backgrounds[i].fill(self.screen_colour)
            self.screen.blit(button_backgrounds[i], (buttons[i][0], buttons[i][1]))
        
        # Grid points
        self.all_grid_points.draw(self.screen)
        
        # Players
        pygame.draw.circle(self.screen, self.p1.colour, (self.p1.x, self.p1.y), self.p1.radius)
        pygame.draw.circle(self.screen, self.p2.colour, (self.p2.x, self.p2.y), self.p2.radius)
        
        # Turns remaining text
        self.turns_outside_box = pygame.Rect(25, 100, 225, 200)
        self.turns_inside_box = pygame.Rect(30, 105, 215, 190)
        pygame.draw.rect(self.screen, GUI.RED, self.turns_outside_box)
        pygame.draw.rect(self.screen, self.screen_colour, self.turns_inside_box)
        
        self.turn_text_surface = self.my_font.render('Turns remaining', True, GUI.GREY)
        self.screen.blit(self.turn_text_surface, (62, 115))
        
        # Turns remaining number
        self.current_turn = self.max_turns
        
        self.turn_number_font_size = 144
        self.turn_number_font = pygame.font.SysFont('Calibri', self.turn_number_font_size)
        self.turn_number_colour = GUI.GREEN
        
        self.turn_number_string = '0' + str(self.current_turn)
        self.turn_number_string = self.turn_number_string[-2:]
        self.turn_number_surface = self.turn_number_font.render(self.turn_number_string, True, self.turn_number_colour)
        
        self.turn_number_pos = (65, 150)
        self.screen.blit(self.turn_number_surface, self.turn_number_pos)
        
        # Start line message and arrow
        self.start_line_surface = self.my_font.render('Start line', True, GUI.BLUE)
        self.start_line_background = pygame.Surface((120, 21))
        self.start_line_background.fill(GUI.LIGHT_GREY)
        self.sl_pos = (80, 45)
        
        self.screen.blit(self.start_line_background, self.sl_pos)
        pygame.draw.polygon(self.screen, GUI.GREY, ((self.sl_pos[0] + 100, self.sl_pos[1] + 7), (self.sl_pos[0] + 100, self.sl_pos[1] + 13), 
                                                    (self.sl_pos[0] + 110, self.sl_pos[1] + 13), (self.sl_pos[0] + 110, self.sl_pos[1] + 17), 
                                                    (self.sl_pos[0] + 117, self.sl_pos[1] + 10), (self.sl_pos[0] + 110, self.sl_pos[1] + 3), 
                                                    (self.sl_pos[0] + 110, self.sl_pos[1] + 7), (self.sl_pos[0] + 100, self.sl_pos[1] + 7)))
        self.screen.blit(self.start_line_surface, self.sl_pos)
        
        # Wind direction message and arrow
        self.wind_direction_surface = self.my_font.render('Wind direction', True, GUI.LIGHT_GREY)
        self.wind_direction_background = pygame.Surface((141, 125))
        self.wind_direction_background.fill(GUI.GREY)
        self.wd_pos = (65, 750)
        
        self.screen.blit(self.wind_direction_background, self.wd_pos)
        pygame.draw.polygon(self.screen, GUI.YELLOW, ((self.wd_pos[0] + 55, self.wd_pos[1] + 30), (self.wd_pos[0] + 55, self.wd_pos[1] + 80), 
                                                      (self.wd_pos[0] + 35, self.wd_pos[1] + 80), (self.wd_pos[0] + 70, self.wd_pos[1] + 115), 
                                                      (self.wd_pos[0] + 105, self.wd_pos[1] + 80), (self.wd_pos[0] + 85, self.wd_pos[1] + 80), 
                                                      (self.wd_pos[0] + 85, self.wd_pos[1] + 30), (self.wd_pos[0] + 55, self.wd_pos[1] + 30)))
        self.screen.blit(self.wind_direction_surface, (self.wd_pos[0], self.wd_pos[1] + 3))
        
        pygame.display.update()
        
    def playGame(self):
        
        # Play game until complete
        self.game_complete = False
        self.p1.Turn = True
        
        while not self.game_complete:
            
            # Player 1's turn
            while self.p1.Turn:
                self.p1.haveTurn(self.p2, self.policy.table, self.current_turn, self.npoints_x, self.npoints_y, self.grid_margin_x, self.grid_margin_y, self.coords, self.screen, self.screen_colour, self.my_font, pygame.display)
                
            # Player 2's turn
            while self.p2.Turn:
                self.p2.haveTurn(self.p1, self.policy.table, self.current_turn, self.npoints_x, self.npoints_y, self.grid_margin_x, self.grid_margin_y, self.coords, self.screen, self.screen_colour, self.my_font, pygame.display)
                
            # Number of turns remaining decrements
            self.current_turn -= 1
     
            # New turns remaining
            self.screen.fill(self.screen_colour, (self.turn_number_pos[0], self.turn_number_pos[1], 
                                                  self.turn_number_surface.get_size()[0], self.turn_number_surface.get_size()[1]))
            
            self.turn_number_string = '0' + str(self.current_turn)
            self.turn_number_string = self.turn_number_string[-2:]
            self.turn_number_surface = self.turn_number_font.render(self.turn_number_string, True, self.turn_number_colour)
            
            self.screen.blit(self.turn_number_surface, self.turn_number_pos)
            pygame.display.update()
            
            # If no turns remaining, end game
            if (self.current_turn == 0):
                self.game_complete = True
    
    def endGame(self):
        
        # Score box
        score_outside_box = pygame.Rect(25, 325, 225, 400)
        score_inside_box = pygame.Rect(30, 330, 215, 390)
        pygame.draw.rect(self.screen, GUI.GREEN, score_outside_box)
        pygame.draw.rect(self.screen, self.screen_colour, score_inside_box)
        
        # Determine game score
        min_x = self.coords[0][0]
        min_y = self.coords[0][1]
        
        i = int((self.p1.y - min_y) / self.grid_margin_y)
        j = int((self.p1.x - min_x) / self.grid_margin_x)
        k = int((self.p2.y - min_y) / self.grid_margin_y)
        l = int((self.p2.x - min_x) / self.grid_margin_x)
        
        game_score = int(self.policy.table[0][i][j][k][l])
        
        # Score font
        self.score_font_size = 72
        self.score_font = pygame.font.SysFont('Calibri', self.score_font_size)
        
        # Score text position
        self.score_text_pos = (62, 380)
        
        # Player 1 wins
        if (game_score <= -1):
            red_surface = self.score_font.render('RED', True, GUI.RED)
            wins_surface = self.score_font.render('WINS!', True, GUI.GREY)
            self.screen.blit(red_surface, (self.score_text_pos[0] + 18, self.score_text_pos[1]))
            self.screen.blit(wins_surface, (self.score_text_pos[0] - 14, self.score_text_pos[1] + 70))
        
        # Player 2 wins
        elif (game_score >= 1):
            blue_surface = self.score_font.render('BLUE', True, GUI.BLUE)
            wins_surface = self.score_font.render('WINS!', True, GUI.GREY)
            self.screen.blit(blue_surface, self.score_text_pos)
            self.screen.blit(wins_surface, (self.score_text_pos[0] - 14, self.score_text_pos[1] + 70))
            
        # Draw
        elif (game_score == 0):
            draw_surface = self.score_font.render('DRAW!', True, GUI.GREY)
            self.screen.blit(draw_surface, (self.score_text_pos[0] - 27, self.score_text_pos[1] + 35))
        
        # Exit or restart message
        WYL_surface = self.my_font.render('Would you like', True, GUI.GREY)
        TPA_surface = self.my_font.render('to play again?', True, GUI.GREY)
        self.screen.blit(WYL_surface, (self.score_text_pos[0] + 7, self.score_text_pos[1] + 180))
        self.screen.blit(TPA_surface, (self.score_text_pos[0] + 12, self.score_text_pos[1] + 210))
        
        # Yes / No buttons
        yes_surface = self.my_font.render('Yes', True, GUI.LIGHT_GREY)
        yes_background = pygame.Surface((50, 30))
        yes_background.fill(GUI.BLUE)
        yes_pos = (65, 635)
        yes_size = yes_background.get_size()
        
        no_surface = self.my_font.render('No', True, GUI.LIGHT_GREY)
        no_background = pygame.Surface((50, 30))
        no_background.fill(GUI.RED)
        no_pos = (160, 635)
        no_size = no_background.get_size()
        
        self.screen.blit(yes_background, yes_pos)
        self.screen.blit(yes_surface, (yes_pos[0] + 10, yes_pos[1] + 4))
        self.screen.blit(no_background, no_pos)
        self.screen.blit(no_surface, (no_pos[0] + 11, no_pos[1] + 4))
        
        pygame.display.update()
        
        # Wait for end game to be selected
        self.end_game_selected = False
        
        while not self.end_game_selected:
            
            # When user click is within area of button, select end game
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    # Coordinates of mouse click
                    x_click = pygame.mouse.get_pos()[0]
                    y_click = pygame.mouse.get_pos()[1]
                    
                    # Check if mouse click inside yes button
                    if (x_click >= yes_pos[0] and x_click <= yes_pos[0] + yes_size[0] - 1
                        and y_click >= yes_pos[1] and y_click <= yes_pos[1] + yes_size[1] - 1):
                        
                        # Remove game objects
                        self.start_line_background.fill(self.screen_colour)
                        self.screen.blit(self.start_line_background, self.sl_pos)
                        
                        pygame.draw.rect(self.screen, self.screen_colour, self.turns_outside_box)
                        
                        pygame.draw.rect(self.screen, self.screen_colour, score_outside_box)
                        
                        self.wind_direction_background.fill(self.screen_colour)
                        self.screen.blit(self.wind_direction_background, self.wd_pos)
                        
                        self.hidden_grid_points.draw(self.screen)
                        
                        pygame.draw.circle(self.screen, self.screen_colour, (self.p1.x, self.p1.y), self.p1.radius)
                        pygame.draw.circle(self.screen, self.screen_colour, (self.p2.x, self.p2.y), self.p2.radius)
                        
                        # Restart game
                        self.end_game_selected = True
                        self.execute()
                        
                    # Check if mouse click inside no button
                    elif (x_click >= no_pos[0] and x_click <= no_pos[0] + no_size[0] - 1
                        and y_click >= no_pos[1] and y_click <= no_pos[1] + no_size[1] - 1):
                        
                        # Exit game
                        self.end_game_selected = True
                        pygame.quit()
        
    def execute(self):
        
        # Execute game methods in order
        self.initialiseGameMode()
        self.playGame()
        self.endGame()
# ==========================================================================================

# Create GUI object
gameGUI = GUI(5, 5, (0, 0), (0, 4), 10) # xpoints, ypoints, p1_start, p2_start, maxturns, where p1 starts, p1 is red


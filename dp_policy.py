# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 11:10:34 2018

@author: matth
"""

#Import Appropriate libraries
import numpy as np
import pandas as pd
import matplotlib as plt

def initialise_policy_table(turns, n, m):
    print(turns)
    #initialise table
    policy_table = np.zeros(shape = (turns, n, m, n, m))
    
    for i in range(n):
        for j in range(m):
            for k in range(n):
                for l in range(m):
                     policy_table[0][i][j][k][l]=manhattan_dist(i,j) - manhattan_dist(k,l)

    return policy_table


#Create Manhattan Function
def manhattan_dist(i,j):
    #add complexity with triangular regio later
    return i

#create possible moves function
def possible_moves_player(i,j,k,l, I, J, K, L, iORk, n, m):
    #i, j, k, l are the game state for the current turn
    #I, J, are the game state from the previous turn for the moving player
    #n, m, are the dimensions of the board.
    #No 180s 
    #No moving on top of each other
    
    #Create list of possible moves
    states = list([])
    #if the opponent isn't at the point we want to move and if the player 
    #hasn't just come from there and they can move 
    if iORk ==1:
        
        #can the player move up
        if (([i-1, j] != [k, l]) and ([i-1, j] !=[I,J]) and i > 0):
            state1 = [i-1, j, k, l]
            states.append(state1)
        
        #can the player move down
        if (([i+1, j] != [k, l]) and ([i+1, j] !=[I,J]) and i < n):
            state2 = [i+1, j, k, l]
            states.append(state2)
        
        #can the player move left
        if (([i, j-1] != [k, l]) and ([i, j-1] !=[I,J]) and j > 0):
            state3 = [i, j-1, k, l]
            states.append(state3)
    
            
        #can the player move right
        if (([i, j+1] != [k, l]) and ([i, j+1] !=[I,J]) and j < m):
            state3 = [i, j+1, k, l]
            states.append(state3)
    
    elif iORk == -1:
        #can the player move up
        if (([i, j] != [k-1, l]) and ([k-1, l] !=[K,L]) and k > 0):
            state1 = [i, j, k-1, l]
            states.append(state1)
        
        #can the player move down
        if (([i, j] != [k+1, l]) and ([k+1, l] !=[K,L]) and k < n):
            state2 = [i, j, k+1, l]
            states.append(state2)
        
        #can the player move left
        if (([i, j] != [k, l-1]) and ([k, l-1] !=[K,L]) and l > 0):
            state3 = [i, j, k, l-1]
            states.append(state3)
    
            
        #can the player move right
        if (([i, j] != [k, l+1]) and ([k, l+1] !=[K,L]) and l < m):
            state3 = [i, j, k, l+1]
            states.append(state3)
    
    return states

#like a cost function in the dynamic programming example in 760 notes
#calulates the difference in value between 2 states
def value_diff_func(new_state, previous_state): 
    value_previous_state    = manhattan_dist(previous_state[0], previous_state[1]) - (manhattan_dist(previous_state[2], previous_state[3]))
    value_new_state         = manhattan_dist(new_state[0], new_state[1]) - (manhattan_dist(new_state[2], new_state[3]))
    return value_new_state - value_previous_state


def populate_policy_table(policy_table, turns, n, m):
    
    for t in range(1, len(turns)):
        for i in range(n):
            for j in range(m):
                for k in range(n):
                    for l in range(m):
                         policy_table[t][i][j][k][l]=

    return policy_table
    

#i = 1
#j = 1
#k = 1
#l = 3
#I = 1
#J = 0
#K = 1
#L = 2
#n = 4
#m = 5
##gamestate = [i,j,k,l]
#turns = 2
#iORk = -1
#
#score, gamestate = game_function(gamestate, turns, iORk)
#print('End State')
#print(gamestate)
#print('Score')
#print(score)

#possible_moves_p1 = possible_moves_player(i,j,k,l, I, J,K, L, iORk, n, m)
#print(possible_moves_p1)
policy_table = initialise_policy_table(4, 4, 5)
print(policy_table[0])


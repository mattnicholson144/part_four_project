# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 11:10:34 2018

@author: matth
"""

#Import Appropriate libraries
import numpy as np
import pandas as pd
import matplotlib as plt

class Policy():
    def __init__(self):

    def initialise_policy_table(turns, n, m):
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
    def possible_origins(i,j,k,l,t,n,m):
        #i, j, k, l are the game state for the current turn
        #n, m, are the dimensions of the board.
        
        #Create list of possible moves
        states = list()
        if  t % 2 == 0:
            if k > 0:
                states.append([i, j, k-1, l])
            if k < n-1:
                states.append([i, j, k+1, l])
            if l > 0:
                states.append([i, j, k, l-1])
            if l < m-1:
                states.append([i, j, k, l+1])
        else:
            if i > 0:
                states.append([i-1, j, k, l])
            if i < n-1:
                states.append([i+1, j, k, l])
            if j > 0:
                states.append([i, j-1, k, l])
            if j < m-1:
                states.append([i, j+1, k, l])
        return states
    
    #like a cost function in the dynamic programming example in 760 notes
    #calulates the difference in value between 2 states
    def value_diff_func(new_state, previous_state): 
        value_previous_state    = manhattan_dist(previous_state[0], previous_state[1]) - (manhattan_dist(previous_state[2], previous_state[3]))
        value_new_state         = manhattan_dist(new_state[0], new_state[1]) - (manhattan_dist(new_state[2], new_state[3]))
        return (value_new_state - value_previous_state)
    
    
    def populate_policy_table(policy_table, turns, n, m):
        
        for t in range(1, turns):
            for i in range(n):
                for j in range(m):
                    for k in range(n):
                        for l in range(m):
                            value_of_moves = np.array([])
                            current_state = [i,j,k,l]
                            possible_previous_states = possible_origins(i,j,k,l,t,n,m)
    
                            for a in range(len(possible_previous_states)):
                                #print(policy_table[t-1][possible_previous_states[a][0]][possible_previous_states[a][1]][possible_previous_states[a][2]][possible_previous_states[a][3]])
                                value_move_to_current = value_diff_func(current_state, possible_previous_states[a])
                                table_value = policy_table[t-1][possible_previous_states[a][0]][possible_previous_states[a][1]][possible_previous_states[a][2]][possible_previous_states[a][3]]
                                value_of_moves = np.append(value_of_moves,(value_move_to_current + table_value))
                                
                            policy_table[t][i][j][k][l]= np.max(value_of_moves)
    
        return policy_table

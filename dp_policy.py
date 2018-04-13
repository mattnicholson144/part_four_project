# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 11:10:34 2018

@author: matth
"""

#Import Appropriate libraries
import numpy as np

class Policy():
    def __init__(self):
        self.table = None
        
    def initialise_policy_table(self, turns, n, m):
        #initialise table
        policy_table = np.zeros(shape = (turns+2, n, m, n, m))
        policy_table.fill(np.nan)
        for t in range(0,2):
           for i in range(n):
                for j in range(m):
                    for k in range(n):
                        for l in range(m):
                            if t == 0:
                                policy_table[t][i][j][k][l] = self.manhattan_dist(i,j) - self.manhattan_dist(k,l)
                            else:
                                value_moves_init = self.value_function(i,j,k,l,t,n,m, 0, policy_table) #max as k (player 2) moves last
                                policy_table[t][i][j][k][l] = np.max(value_moves_init)
                                
        return policy_table
    
    
    #Create Manhattan Function
    def manhattan_dist(self, i,j):
        #add complexity with triangular region later
        return i
    
    #create possible moves function
    def possible_moves(self,i,j,k,l,t,n,m):
        #i, j, k, l are the game state for the current turn
        #n, m, are the dimensions of the board.
        
        #Create list of possible moves
        #need to add you can only bump from right
        states = list()
        if  t % 2 != 0:
            if k > 0 and not (i==k-1 and j==l):
                states.append([i, j, k-1, l])
            if k < n-1 and not (i==k+1 and j==l): 
                states.append([i, j, k+1, l])
            if l > 0:
                states.append([i, j, k, l-1])
            if l < m-1 and not (i==k and j==l) and not (i==k and j==l+1):
                states.append([i, j, k, l+1])
        else:
            if i > 0 and not (k==i-1 and j==l):
                states.append([i-1, j, k, l])
            if i < n-1 and not (k==i+1 and j==l): 
                states.append([i+1, j, k, l])
            if j > 0:
                states.append([i, j-1, k, l])
            if j < m-1 and not (i==k and j==l) and not (i==k and l==j+1):
                states.append([i, j+1, k, l])
        return states    
    #like a cost function in the dynamic programming example in 760 notes
    #calulates the difference in value between 2 states
    def value_diff_func(self, new_state, previous_state): 
        value_future_state    = self.manhattan_dist(previous_state[0], previous_state[1]) - (self.manhattan_dist(previous_state[2], previous_state[3]))
        value_new_state         = self.manhattan_dist(new_state[0], new_state[1]) - (self.manhattan_dist(new_state[2], new_state[3]))
        return (value_new_state - value_future_state)
    
    def value_function(self, i, j, k, l,  t, n, m, depth, policy_table):

        value_of_moves = np.array([])

        
        if depth == 0:
            possible_future_states = self.possible_moves(i,j,k,l,t,n,m)

            for a in possible_future_states:
                value = policy_table[t-1][a[0]][a[1]][a[2]][a[3]]
                value_of_moves = np.append(value_of_moves,value)
            
            return value_of_moves
    

        elif depth == 1 and t % 2 == 0:

            possible_future_states = self.possible_moves(i,j,k,l,t,n,m)
            max_moves = np.array([])

            for a in possible_future_states:
                max_moves = np.append(max_moves, np.max(self.value_function(a[0], a[1], a[2],a[3], t-1, n, m, depth - 1, policy_table)))

            return max_moves
        
        elif depth == 1 and t % 2 != 0:
            #find possible previous states
            possible_future_states = self.possible_moves(i,j,k,l,t,n,m)
            min_moves = np.array([])
            
            for a in possible_future_states:
                min_moves = np.append(min_moves, np.min(self.value_function(a[0], a[1], a[2],a[3], t-1, n, m, depth - 1, policy_table)))
            
            return min_moves
    
    
    def populate_policy_table(self, policy_table, turns, n, m):
        
        for t in range(2, turns+2):
            for i in range(n):
                for j in range(m):
                    for k in range(n):
                        for l in range(m):
                            if t % 2 != 0:
                                policy_table[t][i][j][k][l]=np.max(self.value_function(i, j, k, l, t, n, m, 1, policy_table))
                            else:
                                policy_table[t][i][j][k][l]=np.min(self.value_function(i, j, k, l, t, n, m, 1, policy_table))
        return policy_table


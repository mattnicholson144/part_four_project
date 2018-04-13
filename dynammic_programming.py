# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 14:38:41 2018

Dynamic Programming for Strategy 

@author: matthnicholson
"""
#Import Appropriate libraries
import numpy as np
import pandas as pd
import matplotlib as plt


#Create Manhattan Function
def manhattan_dist(i,j):
    #add complexity with triangular regio later
    return i

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




#Create value function
def value_function(i, j, k, l, I, J, K, L,depth, iORk):
    #i, j represent position of player 1
    #k, l represent position of player 2
    #I, J represent the previous state 
    #depth controls depth of tree
    #iORk is one if i or j are moving and -1 of k and l are moving
    #game state var
    valuestate=[i,j,k,l]
    
    if depth == 0:
        return (manhattan_dist(k,l) - manhattan_dist(i,j)), valuestate
    elif depth > 0 and iORk == 1:
        
        possible_moves = possible_moves_player(i,j,k,l,I,J, iORk,4,5)
        moveValues = np.array([])
        
        for a in possible_moves:
            print(a)
#            print(a[0])
#            print(possible_moves[a][0])
            moveValues[a] = value_function(possible_moves[a][0], possible_moves[a][1], possible_moves[a][2], possible_moves[a][3], I, J, depth-1, iORk)[0]
            
        index = np.argmax(moveValues)
        return moveValues[index], possible_moves[index]
    
    elif depth > 0 and iORk == -1:
        
        possible_moves = possible_moves_player(i,j,k,l,I,J, iORk,4,5)
        moveValues = np.array([])
        
        for a in possible_moves:
            moveValues[a] = value_function(possible_moves[a][0], possible_moves[a][1], possible_moves[a][2], possible_moves[a][3], I, J, depth-1, iORk)[0]
            
        index = np.argmax(moveValues)
        return moveValues[index], possible_moves[index]
        

        index = np.argmin(moveValues)
        return moveValues[index], movestates[index]
    


def game_function(gamestate, turns_remaining, iORk):
    while turns_remaining > 0:
            #Player 1 plays
            score, gamestate = value_function(gamestate[0], gamestate[1], gamestate[2], gamestate[3], 1, iORk)
            turns_remaining = turns_remaining - 1
            iORk = iORk * - 1
            print('New State P1 Moved')
            print(gamestate)
            print('Turns_remaining')
            print(turns_remaining)
            if turns_remaining > 0:
                #Player 2 plays
                score, gamestate = value_function(gamestate[0], gamestate[1], gamestate[2], gamestate[3], 1, iORk)
                turns_remaining = turns_remaining - 1
                iORk = iORk * - 1
                print('New State P2 Moved')
                print(gamestate)
                print('Turns_remaining')
                print(turns_remaining)
    return score, gamestate

i = 1
j = 1
k = 1
l = 3
I = 1
J = 0
K = 1
L = 2
n = 4
m = 5
#gamestate = [i,j,k,l]
#turns = 6
iORk = -1
#
#score, gamestate = game_function(gamestate, turns, iORk)
#print('End State')
#print(gamestate)
#print('Score')
#print(score)

possible_moves_p1 = possible_moves_player(i,j,k,l, I, J,K, L, iORk, n, m)
print(possible_moves_p1)

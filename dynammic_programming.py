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

#Create grid
n = 4
m = 5
grid = [[[y,x] for x in range(m)] for y in range(n)] 

#Create Manhattan Function
def manhattan_dist(i,j):
    #add complexity with triangular regio later
    return i

def possible_moves_player(i,j,k,l):
    #i, j, k, l are the game state for the current turn
    #I, J, are the game state from the previous turn for the moving player
    #Force players to move
    #No 180s 
    #No moving on top of each other
    movestates = list([])
    if (i!=k and j!= l)
    
    
    return




#Create value function
def value_function(i, j, k, l, depth, iORk):
    #i, j represent position of player 1
    #k, l represent position of player 2 
    #depth controls depth of tree
    #iORk is one if i or j are moving and -1 of k and l are moving
    #game state var
    valuestate=[i,j,k,l]
    if depth == 0:
        return (manhattan_dist(k,l) - manhattan_dist(i,j)), valuestate
    elif depth > 0 and iORk == 1:
        movestates = list([])
        moveValues = np.array([])
        
        if i < 4:
            move1, move1state = value_function(i+1, j, k ,l, depth-1, iORk)
            moveValues = np.append(moveValues, move1)
            movestates.append(move1state)

        if i > 0:
            move2, move2state = value_function(i-1, j, k ,l, depth-1, iORk)
            moveValues = np.append(moveValues, move2)
            movestates.append(move2state)

        if j < 5:
            move3, move3state = value_function(i, j+1, k ,l, depth-1, iORk)
            moveValues = np.append(moveValues, move3)
            movestates.append(move3state)

        if j > 0:
            move4, move4state = value_function(i, j-1, k ,l, depth-1, iORk)
            moveValues = np.append(moveValues, move4)
            movestates.append(move4state)


        index = np.argmax(moveValues)
        return moveValues[index], movestates[index]
    
    elif depth > 0 and iORk == -1:
        movestates = list([])
        moveValues = np.array([])
        if k < 4:
            move1, move1state = value_function(i, j, k+1 ,l, depth-1, iORk)
            moveValues = np.append(moveValues, move1)
            movestates.append(move1state)

        if k > 0:
            move2, move2state = value_function(i, j, k-1 ,l, depth-1, iORk)
            moveValues = np.append(moveValues, move2)
            movestates.append(move2state)

        if l < 5:
            move3, move3state = value_function(i, j, k ,l+1, depth-1, iORk)
            moveValues = np.append(moveValues, move3)
            movestates.append(move3state)

        if l > 0:
            move4, move4state = value_function(i, j, k ,l-1, depth-1, iORk)
            moveValues = np.append(moveValues, move4)
            movestates.append(move4state)
        

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
k = 2
l = 3
gamestate = [i,j,k,l]
turns = 6
iORk = 1

score, gamestate = game_function(gamestate, turns, iORk)
print('End State')
print(gamestate)
print('Score')
print(score)
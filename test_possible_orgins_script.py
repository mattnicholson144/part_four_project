# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 11:59:21 2018

@author: matth
"""

#create possible moves function
def possible_moves(i,j,k,l,t,n,m):
    #i, j, k, l are the game state for the current turn
    #n, m, are the dimensions of the board.
    
    #Create list of possible moves
    states = list()
    if  t % 2 != 0:
        if i == k and j == l and k < n-1:
            states.append([i,j,k+1,l])
            return states
        if k > 0:
            states.append([i, j, k-1, l])
        if k < n-1:
            states.append([i, j, k+1, l])
        if l > 0:
            states.append([i, j, k, l-1])
        if l < m-1:
            states.append([i, j, k, l+1])
    else:
        if i == k and j == l and i < n-1:
            states.append([i+1,j,k,l])
            return states
        if i > 0:
            states.append([i-1, j, k, l])
        if i < n-1:
            states.append([i+1, j, k, l])
        if j > 0:
            states.append([i, j-1, k, l])
        if j < m-1:
            states.append([i, j+1, k, l])
    return states

def possible_moves1(i,j,k,l,t,n,m):
        #i, j, k, l are the game state for the current turn
        #n, m, are the dimensions of the board.
        
        #Create list of possible moves
        #need to add you can only bump from right
        states = list()
        if  t % 2 != 0:
            if k > 0:
                states.append([i, j, k-1, l])
            if k < n-1: 
                states.append([i, j, k+1, l])
            if l > 0:
                states.append([i, j, k, l-1])
            if l < m-1 and not (i==k and j==l) and not (i==k and j==l+1):
                states.append([i, j, k, l+1])
        else:
            if i > 0:
                states.append([i-1, j, k, l])
            if i < n-1: #bumping
                states.append([i+1, j, k, l])
            if j > 0:
                states.append([i, j-1, k, l])
            if j < m-1 and not (i==k and j==l) and not (i==k and l==j+1):
                states.append([i, j+1, k, l])
        return states
 
mv1 = possible_moves1(0,1,2,2,3,3,3)

print("in func", mv1)


#import numpy as np
#x = np.array([[4,4],[5,5]])
#
#for b in x:
#    print(b)
#!/usr/bin/env python3

import sys
import pygame
import numpy as np
import math

board, length = [], 19
for x in range(length):
  board.append(["-"] * length)

coords = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's']

def print_board(board):
    print("  " + " ".join(coords))
    i = 0
    for row in board:
        print(coords[i] + " " + " ".join(row))
        i += 1

print_board(board)

# even for black, odd for white
turn = 0
game_over = False

def choose():
    choice = int(input("0 to choose Black, 1 to choose White: "))
    # validate input
    while choice != 0 and choice != 1:
        choice = int(input("0 to choose Black, 1 to choose White: "))
    turn = choice

first = True

# if anyone knows how to optimize these if statements, please do
def win_state(board, player):
    winning_state = [player] * 6
    for c in range(length):
        for r in range(length):
          
          # continue checks if current cell is player
          if(board[r][c] == player):  
            # check horizontal case
            if c+5 < length and board[r][c:c+6] == winning_state:
                return True
            
            # check vertical case
            if r+5 < length and [board[r+i][c] for i in range(6)] == winning_state:
                return True
          
            # check negative slope case
            if r+5 < length and c+5 < length and [board[r+i][c+i] for i in range(6)] == winning_state:
                return True
            
            # check postive slope case
            if r-5 > -1 and c+5 < length and [board[r-i][c+i] for i in range(6)] == winning_state:
                return True

def valid(board, r, c):
    return board[r][c] == "-"

def play(board, first):
    if first:
        r, c = input().split()
        # validate input
        while (r not in coords or c not in coords): r, c = input().split()
        while (not valid(board, coords.index(r), coords.index(c))): r, c = input().split()
        
        row = coords.index(r)
        col = coords.index(c)
        board[row][col] = "X"

        print_board(board)
    else:
        for i in range(2):
            r, c = input().split()
            # validate input
            while (r not in coords or c not in coords): r, c = input().split()
            while (not valid(board, coords.index(r), coords.index(c))): r, c = input().split()
            
            row = coords.index(r)
            col = coords.index(c)
            if turn%2 == 0: board[row][col] = "X"
            else: board[row][col] = "O"

        print_board(board)

def num_valid(board):
    valids = []
    for i in range(length):
        if (valid(board, coords.index(i), coords.index(i))):
            valids.append(i)
    return valids

def is_terminal(board):
    return win_state(board, player) or len(num_valid(board)) == 0

def score(board, player):
    points = 0
    for c in range(length):
        for r in range(length):
              # continue checks if current cell is player
            if(board[r][c] == player):  
                # check horizontal case
                if c < length and board[r][c:c+5] == [player]*5:
                    points = 5
                    break
                elif c < length and board[r][c:c+4] == [player]*4:
                    points = 4
                    break
                elif c < length and board[r][c:c+3] == [player]*3:
                    points = 3
                    break
                elif c < length and board[r][c:c+2] == [player]*2:
                    points = 2
                    break
                elif c < length and board[r][c:c+1] == [player]:
                    points = 1
                    break

                # check vertical case
                if r < length and [board[r+i][c] for i in range(5)] == [player]*5:
                    points = 5
                    break
                elif r < length and [board[r+i][c] for i in range(4)] == [player]*4:
                    points = 4
                    break
                elif r < length and [board[r+i][c] for i in range(3)] == [player]*3:
                    points = 3
                    break
                elif r < length and [board[r+i][c] for i in range(2)] == [player]*2:
                    points = 2
                    break
                elif r < length and [board[r+i][c] for i in range(4)] == [player]*1:
                    points = 1
                    break
              
                # check negative slope case
                if r < length and c < length and [board[r+i][c+i] for i in range(5)] == [player]*5:
                    points = 5
                    break
                elif r < length and c < length and [board[r+i][c+i] for i in range(4)] == [player]*4:
                    points = 4
                    break
                elif r < length and c < length and [board[r+i][c+i] for i in range(3)] == [player]*3:
                    points = 3
                    break
                elif r < length and c < length and [board[r+i][c+i] for i in range(2)] == [player]*2:
                    points = 2
                    break
                elif r < length and c < length and [board[r+i][c+i] for i in range(1)] == [player]*1:
                    points = 1
                    break
                
                # check postive slope case
                if r > -1 and c < length and [board[r-i][c+i] for i in range(5)] == [player]*5:
                    points = 5
                    break
                elif r > -1 and c < length and [board[r-i][c+i] for i in range(4)] == [player]*4:
                    points = 4
                    break
                elif r > -1 and c < length and [board[r-i][c+i] for i in range(3)] == [player]*3:
                    points = 3
                    break
                elif r > -1 and c < length and [board[r-i][c+i] for i in range(2)] == [player]*2:
                    points = 2
                    break
                elif r > -1 and c < length and [board[r-i][c+i] for i in range(1)] == [player]*1:
                    points = 1
                    break
        break

    return points

def minimax(board, depth, maximizing_player):
    valids = num_valid(board)
    terminal = is_terminal(board)
    if depth == 0:
        # return score() for computer - score() for player
        pass
    elif terminal:
        # if one of them wins, return big # for computer, small # for player
        # if game over / no more valid moves, return 0
        pass
    # maximizing player case
    if maximizing_player:
        pass
    # minimizing player case
    else:
        pass
    # might need to assign separate player and AI variables when assigning turns
    pass

choose()

game_over = False

while not game_over:
    print(score(board, "X"))
    print(score(board, "O"))
    if turn%2 == 0:
        play(board, first)
        turn += 1
    else:
        play(board, first)
        turn += 1
    if win_state(board, "X"):
        print("Black wins!")
        game_over = True
    elif win_state(board, "O"):
        print("White wins!")
        game_over = True
    first = False

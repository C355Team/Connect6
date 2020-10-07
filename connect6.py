#!/usr/bin/env python3

import sys
import pygame
import numpy as np
import math


## --- Global Variables ---
turn   = 0 	# even for black, odd for white
player, computer = '', ''
stones = ['X', 'O']
length = 19
coords = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
		  'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's']
game_over = False
## --- End Global Variables ---


def initialize_board():
	board = []
	for x in range(length):
  		board.append(["-"] * length)
	return board

def print_board(board):
	print("  " + " ".join(coords))
	i = 0
	for row in board:
		print(coords[i] + " " + " ".join(row))
		i += 1

def choose():
	global turn, player, computer
	choice = -1
	# validate input
	while choice != 0 and choice != 1:
		user_input = input("0 to play first, 1 otherwise: ")
		try:
			choice = int(user_input)
		except ValueError:
			continue
	turn = choice
	player = stones[choice]
	computer = stones[choice-1]

def valid(board, r, c):
	return in_range(board, r, c) and empty(board, r, c)

def in_range(board, r, c):
	return r in coords and c in coords

def empty(board, r, c):
	return board[coords.index(r)][coords.index(c)] == "-"

def play(board, stone):
	global turn
	input_accepted = False
	while(not input_accepted):
		try:
			r, c = input("Move (h v): ").split()
			input_accepted = valid(board, r, c)
			if not input_accepted:
				raise ValueError
		except ValueError:
			print("Invalid move. Please try again!")
			continue
	row = coords.index(r)
	col = coords.index(c)
	board[row][col] = stone

	return board 

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

def winner_exists(board, stone):
	if win_state(board, stone):
		if (stone == player):
			print("\n === YOU WIN! === \n")
		else:
			print("\n === Bot wins. Better luck next time! === \n")
		return True

def num_valid(board):
	valids = []
	for i in range(length):
		if (valid(board, coords.index(i), coords.index(i))):
			valids.append(i)
	return valids

def is_terminal(board):
	return win_state(board, player) or len(num_valid(board)) == 0

def minimax(board, depth, maximizing_player):
	valids = num_valid(board)
	terminal = is_terminal(board)
	if depth == 0 or terminal:
		# "heuristic value of node"
		pass
	# maximizing player case
	# minimizing player case
	# might need to assign separate player and AI variables when assigning turns
	pass

def main():
	global turn, player, computer
	# initialization		
	board = initialize_board()
	print_board(board)
	choose()

	# actual play
	x_stone_index = stones.index('X')
	if turn%2 == x_stone_index:
		print("-- Player's turn --")
		board = play(board, player)
	else:
		print("-- Computer's turn --")
		board = play(board, computer)	# TODO: update this line for computer

	while not game_over:
		print_board(board)
		turn += 1
		if turn%2 == x_stone_index:
			print("-- Player's turn --")
			board = play(board, player)
			if winner_exists(board, player): break 
			board = play(board, player)
			if winner_exists(board, player): break 
		else:
			print("-- Computer's turn --")
			board = play(board, computer)	# TODO: update this line for computer
			if winner_exists(board, computer): break 
			board = play(board, computer)
			if winner_exists(board, computer): break 
	print_board(board)
	turn +=1

main()

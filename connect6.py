/usr/bin/env python3

import sys
import pygame
import numpy as np
import math

board = []
for x in range(19):
  board.append(["-"] * 19)

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
	# check horizontal case
	for c in range(7):
		for r in range(7):
			if board[r][c] == player and board[r][c+1] == player and board[r][c+2] == player and board[r][c+3] == player and board[r][c+4] == player and board[r][c+5] == player:
				return True

	# check vertical case
	for c in range(7):
		for r in range(7):
			if board[r][c] == player and board[r+1][c] == player and board[r+2][c] == player and board[r+3][c] == player and board[r+4][c] == player and board[r+5][c] == player:
				return True

	# check positive slope case
	for c in range(7):
		for r in range(7):
			if board[r][c] == player and board[r+1][c+1] == player and board[r+2][c+2] == player and board[r+3][c+3] == player and board[r+4][c+4] == player and board[r+5][c+5] == player:
				return True

	# check negative slope case
	for c in range(7):
		for r in range(7):
			if board[r][c] == player and board[r-1][c+1] == player and board[r-2][c+2] == player and board[r-3][c+3] == player and board[r-4][c+4] == player and board[r-5][c+5] == player:
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
	for i in range(19):
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

choose()

game_over = False

while not game_over:
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

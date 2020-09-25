#!/usr/bin/env python3

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
	while choice != 0 and choice != 1:
		choice = int(input("0 to choose Black, 1 to choose White: "))
	turn = choice

first = True

rows_played = set()
cols_played = set()

def play(board, first):
	if first:
		r, c = input().split()
		while (r not in coords or c not in coords): r, c = input().split()
		while (r in rows_played and c in cols_played): 
			r, c = input().split()
		
		row = coords.index(r)
		col = coords.index(c)
		board[row][col] = "X"
		rows_played.add(coords[row])
		cols_played.add(coords[col])
		print_board(board)
	else:
		for i in range(2):
			r, c = input().split()
			while (r not in coords or c not in coords): r, c = input().split()
			while (r in rows_played and c in cols_played): 
				r, c = input().split()
			
			row = coords.index(r)
			col = coords.index(c)

			if turn%2 == 0: board[row][col] = "X"
			else: board[row][col] = "O"
			rows_played.add(coords[row])
			cols_played.add(coords[col])
		print_board(board)

choose()

#def chk_win(board):


while not game_over:
	print(rows_played)
	print(cols_played)
	if turn%2 == 0:
		play(board, first)
		turn += 1
	else:
		play(board, first)
		turn += 1
	first = False

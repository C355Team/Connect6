#!/usr/bin/env python3

import sys

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

def choose():
	choice = input("0 to choose Black, 1 to choose White: ")
	turn = choice

first = True

def play(board, first):
	if first:
		r, c = input().split()
		row = coords.index(r)
		col = coords.index(c)

		board[row][col] = "X"
		print_board(board)
		first = False
	else:
		for i in range(2):
			r, c = input().split()
			row = coords.index(r)
			col = coords.index(c)

			board[row][col] = "X"
		print_board(board)

choose()

# need to go back and forth between while loops
while turn%2 == 0:
	play(board, first)
	turn += 1
#while turn%2 == 1:
	# call player algorithm
	# turn += 1

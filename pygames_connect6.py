import pygame
import math

pygame.init()

WIN = pygame.display.set_mode((950, 950)) #game window dimensions set

pygame.display.set_caption('Connect 6')

turn = 0 #turn counter initiated
blockSize = 50 #each block size pixel set
for x in range(950): #for loop to draw grid
    for y in range(950):
        rect = pygame.Rect(x*blockSize, y*blockSize,
                           blockSize, blockSize)
        pygame.draw.rect(WIN, (0,255,65), rect, 1)

length = 19
coords = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
          'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's']

max_length = 0
blanks_around = 0

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

run = True

board = initialize_board()
print_board(board)

def win_state(board, player):
    winning_state = [player] * 6
    for c in range(length):
        for r in range(length):

          # continue checks if current cell is player
          if(board[c][r] == player):  
            # check horizontal case
            if c+5 < length and [board[c+i][r] for i in range(6)]  == winning_state:
                return True
            
            # check vertical case
            if r+5 < length and [board[c][r+i] for i in range(6)] == winning_state:
                return True
          
            # check negative slope case
            if r+5 < length and c+5 < length and [board[c+i][r+i] for i in range(6)] == winning_state:
                return True
            
            # check postive slope case
            if r-5 > -1 and c+5 < length and [board[c+i][r-i] for i in range(6)] == winning_state:
                return True

def horiz_score(board, player, max_length, blanks_around):
    for i in range(length):
        row = board[i]
        in_a_row = 0
        blanks = 0

        for j in row:
            if j == "-":
                blanks += 1
            elif j == player:
                in_a_row += 1
            else:
                in_a_row = 0
                blanks = 0

            if in_a_row == 6:
                return 6, 0
            
            if in_a_row >= max_length:
                max_length = in_a_row
                blanks_around = blanks

    return max_length, blanks_around

def vert_score(board, player, max_length, blanks_around):
    for i in range(length):
        in_a_row = 0
        blanks = 0

        for j in range(length):
            if board[j][i] == "-":
                blanks += 1
            elif board[j][i] == player:
                in_a_row += 1
            else:
                in_a_row = 0
                blanks = 0

            if in_a_row == 6:
                return 6, 0

            if in_a_row >= max_length:
                max_length = in_a_row
                blanks_around = blanks

    return max_length, blanks_around

def up_diag_score(board, player, max_length, blanks_around):
    up_diagonals =  [[board[p - q][q]
             for q in range(max(p-length+1,0), min(p+1, length))]
            for p in range(length + length - 1)]

    for diagonal in up_diagonals:
        in_a_row = 0
        blanks = 0
        for j in diagonal:
            if j == "-":
                blanks += 1
            elif j == player:
                in_a_row += 1
            else:
                in_a_row = 0
                blank = 0

            if in_a_row == 6:
                return 6, 0
            
            if in_a_row >= max_length:
                max_length = in_a_row
                blanks_around = blanks

    return max_length, blanks_around

def down_diag_score(board, player, max_length, blanks_around):
    down_diagonals = [[board[length - p + q - 1][q]
             for q in range(max(p-length+1, 0), min(p+1, length))]
            for p in range(length + length - 1)]

    for diagonal in down_diagonals:
        in_a_row = 0
        blanks = 0
        for j in diagonal:
            if j == "-":
                blanks += 1
            elif j == player:
                in_a_row += 1
            else:
                in_a_row = 0
                blank = 0

            if in_a_row == 6:
               return 6, 0
            
            if in_a_row >= max_length:
                max_length = in_a_row
                blanks_around = blanks

    return max_length, blanks_around


def max_score(board, player, max_length, blanks_around):
    horiz_max, horiz_blanks = horiz_score(board, player, max_length, blanks_around)
    vert_max, vert_blanks = vert_score(board, player, max_length, blanks_around)
    # bottom left to top right
    up_diag_max, up_diag_blanks = up_diag_score(board, player, max_length, blanks_around)
    # top left to bottom right
    down_diag_max, down_diag_blanks = down_diag_score(board, player, max_length, blanks_around)
    print(down_diag_max, down_diag_blanks)

while run:
    
    pygame.time.delay(10) #refresh delay

    Red = False
    Yellow = False
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #when user clicks on the x, terminate program
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            position = pygame.mouse.get_pos() #get click pos coordinate
            r = math.floor(position[0]/50) #translate coordinate from pixel to columns 0-18
            c = math.floor(position[1]/50) #translate coordinate from pixel to rows 0-18
            print ('Coordinate Selected:' + '(' + str(r) + ',' + str(c) + ')') #for diagnostic purposes
            if turn <= 0: #starting first gives one tile, then all subsequent turns gets 2 tiles
                pygame.draw.rect(WIN, (255,0,0), (r*50,c*50,45,45), 0) #red tile
                board[c][r] = "X"
                if win_state(board, "X"):
                    Red = True
                    break
                turn+=1
                # print(turn)
                print_board(board)
                max_score(board, "X", max_length, blanks_around)
                # up_diag_score(board, "X", max_length, blanks_around)
            elif turn > 0: #player 2
                pygame.draw.rect(WIN, (204,204,0),(r*50,c*50,45,45), 0) #yellow tile
                board[c][r] = "O"
                if win_state(board, "O"):
                    Yellow = True
                    break
                turn+=1
                # print(turn)
                print_board(board)
                max_score(board, "O", max_length, blanks_around)
                if turn >= 3:
                    turn-=4

        pygame.display.update()
    if Red:
        print("Red wins")
        break
    elif Yellow:
        print("Yellow wins")
        break

pygame.quit()

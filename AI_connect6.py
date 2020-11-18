import pygame
import math
import sys
from random import randrange

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

    for sum in range(length*2-1):
        #print('Sum', sum)           # Leave this line for debugging
        in_a_row = 0
        blanks = 0
        for j in range(sum+1):
            i = sum-j
            if (i<length and j<length):
                tile = board[i][j]
                #print(i, j, tile)   # Leave this line for debugging
                if tile == "-":
                    blanks += 1
                elif tile == player:
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

def down_diag_score(board, player, max_length, blanks_around):

    for sum in range(length*-1+1, length, 1):
        #print('Sum', sum)           # Leave this line for debugging
        in_a_row = 0
        blanks = 0
        for j in range(length):
            i = j-sum
            if (i>= 0 and i<length and j<length):
                tile = board[i][j]
                #print(i, j, tile)   # Leave this line for debugging
                if tile == "-":
                    blanks += 1
                elif tile == player:
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


def max_score(board, player, max_length, blanks_around):
    horiz = horiz_score(board, player, max_length, blanks_around)
    vert = vert_score(board, player, max_length, blanks_around)
    # bottom left to top right
    up_diag = up_diag_score(board, player, max_length, blanks_around)
    # top left to bottom right
    down_diag = down_diag_score(board, player, max_length, blanks_around)

    max_tuple = horiz
    for a_tuple in [vert, up_diag, down_diag]:
        if a_tuple[0]>max_tuple[0]:
            max_tuple = a_tuple
        elif a_tuple[0]==max_tuple[0]:
            if a_tuple[1]>max_tuple[1]:
                max_tuple = a_tuple
    print_board(board)  # for debugging only
    print("MAX SCORE:", max_tuple)
    return max_tuple

def print_all_scores(board, player, max_length, blanks_around):
    print("UP", up_diag_score(board, player, max_length, blanks_around))
    print("DOWN", down_diag_score(board, player, max_length, blanks_around))
    print("Ver", vert_score(board, player, max_length, blanks_around))
    print("Hor", horiz_score(board, player, max_length, blanks_around))

def score_util(board, player, max_length, blanks_around):
    util = 0
    max_length, blanks_around = max_score(board, player, max_length, blanks_around)
    max_length_opp, blanks_around_opp = max_score(board, opponent(player), max_length, blanks_around)
    can_win = (max_length + blanks_around) >= 6
    opp_can_win = (max_length_opp + blanks_around_opp) >= 6

    if can_win:
        if max_length == 6:
            util = 1000
        elif max_length == 5:
            util = 50
        elif max_length == 4:
            util = 40
        elif max_length == 3:
            util = 30
        elif max_length == 2:
            util = 20
        elif max_length == 1:
            util = 10
    
    if opp_can_win:
        if max_length_opp == 6:
            util = -500 if 500 > util else util
        elif max_length_opp == 5:
            util = -55 if 55 > util else util
        elif max_length_opp == 4:
            util = -45 if 45 > util else util
        elif max_length_opp == 3:
            util = -35 if 35 > util else util

# check available moves

def in_range(board, r, c):
    return r in coords and c in coords

def empty(board, r, c):
    return board[coords.index(r)][coords.index(c)] == "-"

def valid(board, r, c):
    return in_range(board, r, c) and empty(board, r, c)

def num_valid(board):
    valids = []
    for i in range(length):
        for j in range(length):
            if (valid(board, coords[i], coords[j])):
                valids.append((i, j))
    return valids

def random_move(board):
    global best_move_x, best_move_y

    valids = num_valid(board)
    random_move = valids[randrange(len(valids))]
    best_move_x = random_move[0]
    best_move_y = random_move[1]

def opponent(player):
    if player == 'X':
        return 'O'
    else:
        return 'X'

best_move_x = 0
best_move_y = 0

def ab_negamax(board, player, depth, max_depth, alpha, beta):
    global best_move_x, best_move_y, max_length, blanks_around

    # previous move created win
    if win_state(board, "X") or win_state(board, "O") or depth == max_depth:
        max_length_copy = max_length
        blanks_around_copy = blanks_around
        score_util(board, player, max_length, blanks_around)
        max_tuple = max_score(board, player, max_length_copy, blanks_around_copy)
        return max_tuple[0] + max_tuple[1]
    
    # board full, tie
    moves = num_valid(board)
    if len(moves) == 0:
        return 0
    
    best = -sys.maxsize
    new_board = board
    for move in moves:
        new_board[move[0]][move[1]] = player
        v = ab_negamax(new_board, opponent(player), depth+1, max_depth, -alpha, -beta)
        best = max(best, -v)
        if best == -v:
            best_move_x = move[0]
            best_move_y = move[1]

        new_board[move[0]][move[1]] = '-'   # reset board to original
        alpha = max(alpha, best)
        if alpha >= beta:
            break

    return best


while run:
    
    pygame.time.delay(10) #refresh delay

    Red = False
    Yellow = False
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #when user clicks on the x, terminate program
            run = False
        if turn <= 0:
            if event.type == pygame.MOUSEBUTTONUP:
                position = pygame.mouse.get_pos() #get click pos coordinate
                r = math.floor(position[0]/50) #translate coordinate from pixel to columns 0-18
                c = math.floor(position[1]/50) #translate coordinate from pixel to rows 0-18
                print ('Coordinate Selected:' + '(' + str(r) + ',' + str(c) + ')') #for diagnostic purposes
                if ((c, r)) in num_valid(board):       
                    pygame.draw.rect(WIN, (255,0,0), (r*50,c*50,45,45), 0) #red tile
                    board[c][r] = "X"
                    if win_state(board, "X"):
                        Red = True
                        break
                    turn+=1
                    # print(turn)
                    print_board(board)
                    
                    print_all_scores(board, "X", max_length, blanks_around)
                    
        else: #player 2
            # random_move(board)
            ab_negamax(board, 'O', 0, 1, -1000, 1000)   # board, player, depth, max_depth, alpha, beta
            board[best_move_x][best_move_y] = "O"
            pygame.draw.rect(WIN, (204,204,0),(best_move_y*50,best_move_x*50,45,45), 0) #yellow tile
            if win_state(board, "O"):
                Yellow = True
                break
            turn+=1
            # print(turn)
            print_board(board)

            print_all_scores(board, "O", max_length, blanks_around)

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

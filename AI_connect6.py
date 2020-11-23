import pygame
import math
import sys
import os
import random

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
max_length = 0
blanks_around = 0
length = 19
coords = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
          'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's']

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

def horiz_score(board, player):

    max_length, multiples = 0, 0
    for row in board:       
        for i in range(length - 5):
            six_tiles = [tile for tile in row[i:i+6]]
            if opponent(player) not in six_tiles:
                player_count = six_tiles.count(player)
                if player_count > max_length:
                    max_length = player_count
                    multiples = 1
                elif player_count == max_length:
                    multiples += 1

    return [max_length, multiples]

def vert_score(board, player):

    max_length, multiples = 0, 0
    for i in range(length):
        for j in range(length - 5):
            six_tiles = []
            for k in range(6):
                six_tiles.append(board[j+k][i])
            if opponent(player) not in six_tiles:
                player_count = six_tiles.count(player)
                if player_count > max_length:
                    max_length = player_count
                    multiples = 1
                elif player_count == max_length:
                    multiples += 1

    return [max_length, multiples]

def up_diag_score(board, player):

    max_length, multiples = 0, 0
    up_diagonals = [[board[p - q][q]
             for q in range(max(p-length+1,0), min(p+1, length))]
            for p in range(length + length - 1)]
    
    for diagonal in up_diagonals:
        if len(diagonal) >= 6:
            for i in range(len(diagonal) - 5):
                six_tiles = [tile for tile in diagonal[i:i+6]]
                if opponent(player) not in six_tiles:
                    player_count = six_tiles.count(player)
                    if player_count > max_length:
                        max_length = player_count
                        multiples = 1
                    elif player_count == max_length:
                        multiples += 1

    return [max_length, multiples]

def down_diag_score(board, player):

    max_length, multiples = 0, 0
    down_diagonals = [[board[length - p + q - 1][q]
             for q in range(max(p-length+1, 0), min(p+1, length))]
            for p in range(length + length - 1)]
    
    for diagonal in down_diagonals:
        if len(diagonal) >= 6:
            for i in range(len(diagonal) - 5):
                six_tiles = [tile for tile in diagonal[i:i+6]]
                if opponent(player) not in six_tiles:
                    player_count = six_tiles.count(player)
                    if player_count > max_length:
                        max_length = player_count
                        blanks_around = 6 - player_count
                        multiples = 1
                    elif player_count == max_length:
                        multiples += 1

    return [max_length, multiples]

def max_score(board, player):
    horiz = horiz_score(board, player)
    vert = vert_score(board, player)
    # bottom left to top right
    up_diag = up_diag_score(board, player)
    # top left to bottom right
    down_diag = down_diag_score(board, player)

    max_tuple = horiz
    for a_tuple in [vert, up_diag, down_diag]:
        if a_tuple[0]>max_tuple[0]:
            max_tuple = a_tuple
        elif a_tuple[0]==max_tuple[0]:
            if a_tuple[1]>max_tuple[1]:
                max_tuple = a_tuple

    # print_board(board)  # for debugging only
    # print("MAX SCORE:", max_tuple)
    return max_tuple

def print_all_scores(board, player):
    print("UP", up_diag_score(board, player))
    print("DOWN", down_diag_score(board, player))
    print("Ver", vert_score(board, player))
    print("Hor", horiz_score(board, player))
    print("MAX", max_score(board,player))
    
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
    global best_move_x, best_move_y

    # previous move created win
    if win_state(board, "X") or win_state(board, "O") or depth == max_depth:
        max_score_player = max_score(board, player)
        max_score_opponent = max_score(board, opponent(player))
        
        # special case where player has connect4 and AI has connect3, then AI should go for block
        if max_score_player[0] == 4 and max_score_opponent[0] == 4:
            max_score_opponent[0] = 0

        # if player max_length > opponent max_length OR player multiples at max_length > opponent multiples at max_length
        if max_score_player[0] > max_score_opponent[0] or (max_score_player[0] == max_score_opponent[0] and max_score_player[1] > max_score_opponent[1]):
            return max_score_player
        else:
            return -max_score_opponent[0], -max_score_opponent[1]

    # board full, tie
    moves = num_valid(board)
    if len(moves) == 0:
        return 0
    
    best = [-sys.maxsize, -sys.maxsize]
    new_board = board
    random.shuffle(moves)
    for move in moves:
        new_board[move[0]][move[1]] = player
        v = ab_negamax(new_board, opponent(player), depth+1, max_depth, [-alpha[0], -alpha[1]], [-beta[0], -beta[1]])
        
        # if -v max_length > best max_length OR -v multiples at max_length > best multiples at max_length   
        if -v[0] > best[0] or (-v[0] == best[0] and -v[1] >= best[1]): 
            best_move_x = move[0]
            best_move_y = move[1]
            best = [-v[0], -v[1]]
        new_board[move[0]][move[1]] = '-'   # reset board to original
        
        if best[0] > alpha[0] or (best[0] == alpha[0] and best[1] > alpha[1]):
            alpha = best
        if alpha[0] > beta[0] or (alpha[0] == beta[0] and alpha[1] > beta[1]):
            break

    return best

def text_objects(text, font):
        if Red:
            textSurface = font.render(text, True, (255,0,0))
        if Yellow:
            textSurface = font.render(text, True, (204,204,0))
        return textSurface, textSurface.get_rect()
    
def winner_message_display(text):
        largeText = pygame.font.Font('freesansbold.ttf',64)
        TextSurf, TextRect = text_objects(text, largeText)
        TextRect.center = ((475),(400))
        WIN.blit(TextSurf, TextRect)
    
        pygame.display.update()
        
def instruction_message_display(text):
        largeText = pygame.font.Font('freesansbold.ttf',48)
        TextSurf, TextRect = text_objects(text, largeText)
        TextRect.center = ((475),(475))
        WIN.blit(TextSurf, TextRect)
    
        pygame.display.update()
        
def reminder_message_display(text):
        largeText = pygame.font.Font('freesansbold.ttf',24)
        TextSurf, TextRect = text_objects(text, largeText)
        TextRect.center = ((475),(600))
        WIN.blit(TextSurf, TextRect)
    
        pygame.display.update()
        
def game_over_screen():
        if Red:
            WIN.fill((0,0,0))
            winner_message_display("Player is the winner!")
            instruction_message_display("Game will return to menu in 10 seconds!")
            reminder_message_display("Press Q anytime during gameplay to quit, and space to return to the main menu.")
            pygame.time.delay(10000)
            
        if Yellow:
            WIN.fill((0,0,0))
            winner_message_display("AI is the winner!")
            instruction_message_display("Game will return to menu in 10 seconds!")
            reminder_message_display("Press Q anytime during gameplay to quit, and space to return to the main menu.")
            pygame.time.delay(10000)
    
while run:
    
    pygame.time.delay(10) #refresh delay

    Red = False
    Yellow = False
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #when user clicks on the x, terminate program
            run = False
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    print("Quitting registered!")
                    run = False
                    pygame.display.quit()
                    pygame.quit()
                elif event.key == pygame.K_SPACE:
                    print("Menu registered!")
                    run = False
                    pygame.display.quit()
                    pygame.quit()
                    import pvp_connect6.py
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
                    turn+=1
                    # print(turn)
                    print_board(board)
                    
                    print("AI max scores")
                    print_all_scores(board, "O")
                    print("Player max scores")
                    print_all_scores(board, "X")
                    
        else: #player 2
            # random_move(board)
            ab_negamax(board, 'O', 0, 1, [-1000, -1000], [1000, 1000])   # board, player, depth, max_depth, alpha, beta
            board[best_move_x][best_move_y] = "O"
            pygame.draw.rect(WIN, (204,204,0),(best_move_y*50,best_move_x*50,45,45), 0) #yellow tile
            if win_state(board, "O"):
                Yellow = True
            turn+=1
            # print(turn)
            print_board(board)

            print("AI max scores")
            print_all_scores(board, "O")
            print("Player max scores")
            print_all_scores(board, "X")

            if turn >= 3:
                turn-=4

        pygame.display.update()
    if Red:
        print("Red wins")
        game_over_screen()
        import pvp_connect6
    elif Yellow:
        print("Yellow wins")
        game_over_screen()
        import pvp_connect6

pygame.quit()
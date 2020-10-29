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
        


run = True

while run:
    
    pygame.time.delay(10) #refresh delay
    
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
                turn+=1
                print(turn)
            elif turn > 0: #player 2
                pygame.draw.rect(WIN, (204,204,0),(r*50,c*50,45,45), 0) #yellow tile
                turn+=1
                print(turn)
                if turn >= 3:
                    turn-=4
         
        pygame.display.update()import pygame
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
    print(winning_state)
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

while run:
    
    pygame.time.delay(10) #refresh delay
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #when user clicks on the x, terminate program
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            position = pygame.mouse.get_pos() #get click pos coordinate
            r = math.floor(position[0]/50) #translate coordinate from pixel to columns 0-18import pygame
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
    print(winning_state)
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
                print(turn)
            elif turn > 0: #player 2
                pygame.draw.rect(WIN, (204,204,0),(r*50,c*50,45,45), 0) #yellow tile
                board[c][r] = "O"
                if win_state(board, "O"):
                    Yellow = True
                    break
                turn+=1
                print(turn)
                if turn >= 3:
                    turn-=4

        print_board(board)
        pygame.display.update()
    if Red:
        print("Red wins")
        break
    elif Yellow:
        print("Yellow wins")
        break

pygame.quit()
            c = math.floor(position[1]/50) #translate coordinate from pixel to rows 0-18
            print ('Coordinate Selected:' + '(' + str(r) + ',' + str(c) + ')') #for diagnostic purposes
            if turn <= 0: #starting first gives one tile, then all subsequent turns gets 2 tiles
                pygame.draw.rect(WIN, (255,0,0), (r*50,c*50,45,45), 0) #red tile
                board[c][r] = "X"
                if win_state(board, "X"):
                    print("WINNER")
                    pygame.quit()
                turn+=1
                print(turn)
            elif turn > 0: #player 2
                pygame.draw.rect(WIN, (204,204,0),(r*50,c*50,45,45), 0) #yellow tile
                board[c][r] = "O"
                if win_state(board, "O"):
                    print("WINNER")
                    pygame.quit()
                turn+=1
                print(turn)
                if turn >= 3:
                    turn-=4
         
        print_board(board)
        pygame.display.update()

pygame.quit()

pygame.quit()

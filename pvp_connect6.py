import pygame
import math
import pygame_menu


pygame.init()

def main_menu():
    WIN = pygame.display.set_mode((950, 950)) #game window dimensions set
   
    def start_the_game_pvp():   
        connect_6_pvp()
    def start_the_game_ai():
        import AI_connect6.py
    
    menu = pygame_menu.Menu(950, 950, 'Connect 6',
                           theme=pygame_menu.themes.THEME_DARK)
    
    menu.add_button('Play Against Another Player', start_the_game_pvp)
    menu.add_button('Play Against An AI', start_the_game_ai)
    menu.add_button('Quit', pygame_menu.events.EXIT)
    pygame.display.set_caption('Connect 6')
    
    menu.mainloop(WIN)

def connect_6_pvp():
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
        
        print("MAX SCORE:", max_tuple)
        return max_tuple
    
    def print_all_scores(board, player, max_length, blanks_around):
        print("UP", up_diag_score(board, player, max_length, blanks_around))
        print("DOWN", down_diag_score(board, player, max_length, blanks_around))
        print("Ver", vert_score(board, player, max_length, blanks_around))
        print("Hor", horiz_score(board, player, max_length, blanks_around))
    
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
    
    def text_objects(text, font):
        if Red:
            textSurface = font.render(text, True, (255,0,0))
        if Yellow:
            textSurface = font.render(text, True, (204,204,0))
        return textSurface, textSurface.get_rect()
    
    def winner_message_display(text):
        largeText = pygame.font.Font('freesansbold.ttf',64)
        TextSurf, TextRect = text_objects(text, largeText)
        TextRect.center = ((950/2),(400))
        WIN.blit(TextSurf, TextRect)
    
        pygame.display.update()
        
    def instruction_message_display(text):
        largeText = pygame.font.Font('freesansbold.ttf',48)
        TextSurf, TextRect = text_objects(text, largeText)
        TextRect.center = ((950/2),(950/2))
        WIN.blit(TextSurf, TextRect)
    
        pygame.display.update()
        
    def reminder_message_display(text):
        largeText = pygame.font.Font('freesansbold.ttf',24)
        TextSurf, TextRect = text_objects(text, largeText)
        TextRect.center = ((950/2),(600))
        WIN.blit(TextSurf, TextRect)
    
        pygame.display.update()
        
    def game_over_screen():
        if Red:
            WIN.fill((0,0,0))
            winner_message_display("Red is the winner!")
            instruction_message_display("Game will restart in 10 seconds!")
            reminder_message_display("Press Q anytime during gameplay to quit, and space to return to the main menu.")
            pygame.time.delay(10000)
            
        if Yellow:
            WIN.fill((0,0,0))
            winner_message_display("Yellow is the winner!")
            instruction_message_display("Game will restart in 10 seconds!")
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
                    main_menu()

            if event.type == pygame.MOUSEBUTTONUP:
                position = pygame.mouse.get_pos() #get click pos coordinate
                r = math.floor(position[0]/50) #translate coordinate from pixel to columns 0-18
                c = math.floor(position[1]/50) #translate coordinate from pixel to rows 0-18
                print ('Coordinate Selected:' + '(' + str(r) + ',' + str(c) + ')') #for diagnostic purposes
                if ((c, r)) in num_valid(board):       
                    if turn <= 0: #starting first gives one tile, then all subsequent turns gets 2 tiles
                        pygame.draw.rect(WIN, (255,0,0), (r*50,c*50,45,45), 0) #red tile
                        board[c][r] = "X"
                        if win_state(board, "X"):
                            Red = True   
                        turn+=1
                        # print(turn)
                        print_board(board)
                        # score_util(board, "X", True, max_length, blanks_around)
                        # max_score(board, "X", max_length, blanks_around)
                        print_all_scores(board, "X", max_length, blanks_around)
                        
                    elif turn > 0: #player 2
                        pygame.draw.rect(WIN, (204,204,0),(r*50,c*50,45,45), 0) #yellow tile
                        board[c][r] = "O"
                        if win_state(board, "O"):
                            Yellow = True
                        turn+=1
                        # print(turn)
                        print_board(board)
                        # score_util(board, "O", False, max_length, blanks_around)
                        # max_score(board, "O", max_length, blanks_around)
                        print_all_scores(board, "O", max_length, blanks_around)
    
                        if turn >= 3:
                            turn-=4
    
            pygame.display.update()
        if Red:
            print("Red wins")
            game_over_screen()
            connect_6_pvp()
        elif Yellow:
            print("Yellow wins")
            game_over_screen()
            connect_6_pvp()
    
    pygame.quit()

main_menu()

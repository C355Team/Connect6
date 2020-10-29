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
         
        pygame.display.update()

pygame.quit()
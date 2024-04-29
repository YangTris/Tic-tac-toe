import pygame
from settings import *

pygame.init()
pygame.display.set_caption("Tic Tac Toe")

matrix = [[0 for _ in range(9)] for _ in range(9)]
winnerMatrix = [[0 for _ in range(3)] for _ in range(3)]
clicked = False
pos = []
player = 1
gameOver = False

def drawGrid():
    screen.fill(backgroundColor)
    for i in range(9):
        if i != 0:
            pygame.draw.line(screen,smallLineColor,(i*80,0),(i*80,720),2)
            pygame.draw.line(screen,smallLineColor,(0,i*80),(720,i*80),2)
            if i%3 == 0:
                pygame.draw.line(screen,lineColor,(i*80,0),(i*80,720),4)
                pygame.draw.line(screen,lineColor,(0,i*80),(720,i*80),4)
    pygame.draw.line(screen, lineColor, (720, 0), (720, 720), 4)
    
def drawMarker():
    x_pos = 0
    for i in matrix:
        y_pos = 0
        for j in i:
            if j == 1:
                pygame.draw.line(screen,XCOLOR,(x_pos*80+15,y_pos*80+15),(x_pos*80+65,y_pos*80+65),5)
                pygame.draw.line(screen,XCOLOR,(x_pos*80+15,y_pos*80+65),(x_pos*80+65,y_pos*80+15),5)
            if j == -1:
                pygame.draw.circle(screen,OCOLOR,(x_pos*80+40,y_pos*80+40),30,5)
            y_pos+=1
        x_pos+=1
    x = 0
    for i in winnerMatrix:
        y = 0
        for j in i:
            if j == 1:
                pygame.draw.line(screen,XCOLOR,(x*240+15,y*240+15),(x*240+225,y*240+225),15)
                pygame.draw.line(screen,XCOLOR,(x*240+225,y*240+15),(x*240+15,y*240+225),15)
            if j == -1:
                pygame.draw.circle(screen,OCOLOR,(x*240+120,y*240+120),100,15)
            y+=1
        x+=1

def check_columns():
    # print("Checking columns")
    result = 0
    for i in range(9):
        if matrix[i][0] == matrix[i][1] == matrix[i][2]:
            result = matrix[i][0]
            if result != 0 and result != 2:
                draw_winner(result,i,0)
        if matrix[i][3] == matrix[i][4] == matrix[i][5]:
            result = matrix[i][3]
            if result != 0 and result != 2:
                draw_winner(result,i,3)
        if matrix[i][6] == matrix[i][7] == matrix[i][8]:
            result = matrix[i][6]
            if result != 0 and result != 2:
                draw_winner(result,i,6)

    return result

def check_rows():
    # print("Checking rows")
    result = 0
    for i in range(9):
        if matrix[0][i] == matrix[1][i] == matrix[2][i]:
            result = matrix[0][i]
            if result != 0 and result != 2:
                draw_winner(result,0,i)
        if matrix[3][i] == matrix[4][i] == matrix[5][i]:
            result = matrix[3][i]
            if result != 0 and result != 2:
                draw_winner(result,3,i)
        if matrix[6][i] == matrix[7][i] == matrix[8][i]:
            result = matrix[6][i]
            if result != 0 and result != 2:
                draw_winner(result,6,i)
    return result

def check_diagonals():
    # print("Checking diagonals")
    result = 0
    for x in [0,3,6,2,5,8]:
        if x%3==0:
            y=x+1
            z=x+2
        else:
            y=x-1
            z=x-2

        if matrix[x][0] == matrix[y][1] == matrix[z][2]:
            result = matrix[x][0]
            if result != 0 and result != 2:
                draw_winner(result,x,0)
        if matrix[x][3] == matrix[y][4] == matrix[z][5]:
            result = matrix[x][3]
            if result != 0 and result != 2:
                draw_winner(result,x,3)
        if matrix[x][6] == matrix[y][7] == matrix[z][8]:
            result = matrix[x][6]
            if result != 0 and result != 2:
                draw_winner(result,x,6)

    return result

def draw_winner(player,x_pos,y_pos):
    x = (x_pos//3)
    y = (y_pos//3)
    for i in range(3):
        for j in range(3):
            if matrix[x*3+i][y*3+j] == 0:
                matrix[x*3+i][y*3+j] = 2
    winnerMatrix[x][y] = player
    print(winnerMatrix)

def check_winner():
    result = 0
    result = check_columns()
    if result == 0:
        result = check_rows()
    if result == 0:
        result = check_diagonals()
    return result


run = True
while run:
    
    drawGrid()
    drawMarker()

    #add event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if gameOver == False:
            if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
                clicked = True
            if event.type == pygame.MOUSEBUTTONUP and clicked == True:
                clicked = False
                pos = pygame.mouse.get_pos()
                mouse_x = pos[0]
                mouse_y = pos[1]
                print(pos)
                #check inside game board
                if pos >= (0,0) and pos <= (720,720):
                    if matrix[mouse_x//80][mouse_y//80] == 0:
                        matrix[mouse_x//80][mouse_y//80] = player
                        print(matrix[mouse_x//80][mouse_y//80])
                        player *= -1
                        check_winner()
                        #if check_winner() != 0:
                            #gameOver = True

    pygame.display.update()

pygame.quit()
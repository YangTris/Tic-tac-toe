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
winner = 0
openMove = True
lastMove = None
nextMove = [-1,-1]
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

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
    
    pygame.draw.rect(screen, (0, 255, 0), (SCREEN_WIDTH - (SCREEN_WIDTH-SCREEN_HEIGHT) + 100, 150, 180, 50))  # Green button
    button_text = pygame.font.Font('freesansbold.ttf', 24).render("Restart Game", True, (0, 0, 0))
    screen.blit(button_text, (SCREEN_WIDTH - (SCREEN_WIDTH-SCREEN_HEIGHT) + 110, 165))

def drawMarker():
    global nextMove,openMove
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
    if openMove == False:
        x= nextMove[0]
        y= nextMove[1]
        pygame.draw.line(screen,OCOLOR,(x*80,y*80),((x+3)*80,y*80),5)
        pygame.draw.line(screen,OCOLOR,(x*80,(y+3)*80),((x+3)*80,(y+3)*80),5)
        pygame.draw.line(screen,OCOLOR,(x*80,y*80),(x*80,(y+3)*80),5)
        pygame.draw.line(screen,OCOLOR,((x+3)*80,y*80),((x+3)*80,(y+3)*80),5)
    else:
        for i in range(4):
            pygame.draw.line(screen,OCOLOR,(i*3*80,0),(i*3*80,720),5)
            pygame.draw.line(screen,OCOLOR,(0,i*3*80),(720,i*3*80),5)
    
def check_columns():
    # print("Checking columns")
    result = 0
    for i in range(9):
        if matrix[i][0] == matrix[i][1] == matrix[i][2]:
            result = matrix[i][0]
            if result != 0 and result != 2:
                add_cell_winner(result,i,0)
        if matrix[i][3] == matrix[i][4] == matrix[i][5]:
            result = matrix[i][3]
            if result != 0 and result != 2:
                add_cell_winner(result,i,3)
        if matrix[i][6] == matrix[i][7] == matrix[i][8]:
            result = matrix[i][6]
            if result != 0 and result != 2:
                add_cell_winner(result,i,6)
    return result

def check_rows():
    # print("Checking rows")
    result = 0
    for i in range(9):
        if matrix[0][i] == matrix[1][i] == matrix[2][i]:
            result = matrix[0][i]
            if result != 0 and result != 2:
                add_cell_winner(result,0,i)
        if matrix[3][i] == matrix[4][i] == matrix[5][i]:
            result = matrix[3][i]
            if result != 0 and result != 2:
                add_cell_winner(result,3,i)
        if matrix[6][i] == matrix[7][i] == matrix[8][i]:
            result = matrix[6][i]
            if result != 0 and result != 2:
                add_cell_winner(result,6,i)
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
                add_cell_winner(result,x,0)
        if matrix[x][3] == matrix[y][4] == matrix[z][5]:
            result = matrix[x][3]
            if result != 0 and result != 2:
                add_cell_winner(result,x,3)
        if matrix[x][6] == matrix[y][7] == matrix[z][8]:
            result = matrix[x][6]
            if result != 0 and result != 2:
                add_cell_winner(result,x,6)

    return result
          
def add_cell_winner(player,x_pos,y_pos):
    x = (x_pos//3)
    y = (y_pos//3)
    for i in range(3):
        for j in range(3):
            if matrix[x*3+i][y*3+j] == 0:
                matrix[x*3+i][y*3+j] = 2
    winnerMatrix[x][y] = player
    print(winnerMatrix)

def check_cell_winner():
    result = 0
    result = check_columns()
    if result == 0:
        result = check_rows()
    if result == 0:
        result = check_diagonals()
    return result
    
def restart_game():
    global matrix, winnerMatrix, player, gameOver,lastMove, openMove,nextMove
    matrix = [[0 for _ in range(9)] for _ in range(9)]
    winnerMatrix = [[0 for _ in range(3)] for _ in range(3)]
    player = 1
    gameOver = False
    lastMove = None
    openMove = True
    nextMove = [-1,-1]

def check_winner():
    winner = 0
    pos = 0
    for i in winnerMatrix:
        #check columns
        if sum(i) == 3:
            winner = 1
            return winner
        if sum(i) == -3:
            winner = -1
            return winner
        #check rows
        if winnerMatrix[0][pos] == winnerMatrix[1][pos] == winnerMatrix[2][pos]:
            if winnerMatrix[0][pos]!=0:
                winner = winnerMatrix[0][pos]
                return winner
        pos+=1
    #check diagonals
    if winnerMatrix[0][0] == winnerMatrix[1][1] == winnerMatrix[2][2]:
        if winnerMatrix[0][0] != 0:
            winner = winnerMatrix[0][0]
    if winnerMatrix[2][0] == winnerMatrix[1][1] == winnerMatrix[0][2]:
        if winnerMatrix[2][0] != 0:
            winner = winnerMatrix[2][0]
            return winner
    #check tie
    count = 0
    for i in range(3):
        for j in range(3):
            if winnerMatrix[i][j] == 0:
                count += 1
    if count == 0: winner = -2
    return winner

def check_next_move():
    global lastMove,nextMove,openMove,player,gameOver,winner
    check_cell_winner()
    winner = check_winner()
    if winner != 0:
        gameOver = True
        if winner == -2:
            print("Tie")
        else:
            print("player ",winner," win")
    else:
        if lastMove != None:
            x = lastMove[0]//80
            y = lastMove[1]//80
            nextMove[0] = (x-x//3*3)*3
            nextMove[1] = (y-y//3*3)*3
            if winnerMatrix[nextMove[0]//3][nextMove[1]//3] == 0:
                openMove = False
                count = 0
                for i in range(3):
                    for j in range(3):
                        if matrix[nextMove[0]+i][nextMove[1]+j] == 0:
                            matrix[nextMove[0]+i][nextMove[1]+j] = -2
                            count+=1
                if count == 0:
                    nextMove = [-1,-1]
                    openMove = True
            else:
                nextMove = [-1,-1]
                openMove = True

def reset_move():
    if nextMove != [-1,-1]:
        for i in range(3):
            for j in range(3):
                if matrix[nextMove[0]+i][nextMove[1]+j] == -2:
                    matrix[nextMove[0]+i][nextMove[1]+j] = 0

run = True
while run:
    drawGrid()
    drawMarker()
    
    #add event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
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
                if gameOver == False:
                    if openMove == True:
                        if matrix[mouse_x//80][mouse_y//80] == 0:
                            matrix[mouse_x//80][mouse_y//80] = player
                            player *= -1
                            lastMove = pos
                            check_next_move()
                    elif openMove == False:
                        if matrix[mouse_x//80][mouse_y//80] == -2:
                            matrix[mouse_x//80][mouse_y//80]  = player
                            player *= -1
                            reset_move()
                            lastMove = pos
                            check_next_move()
            if mouse_x > SCREEN_WIDTH - (SCREEN_WIDTH-SCREEN_HEIGHT) + 100 and mouse_x < SCREEN_WIDTH - (SCREEN_WIDTH-SCREEN_HEIGHT) + 280 and mouse_y > 150 and mouse_y < 200:
                restart_game()
    pygame.display.update()

pygame.quit()
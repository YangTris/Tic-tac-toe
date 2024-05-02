import pygame
from settings import *
import socket
import threading

host='127.0.0.1'
port=12345

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

pygame.init()
pygame.display.set_caption("Tic Tac Toe")

socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socket.connect((host,port))

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

def convert_1d_to_2d(l, cols):
    return [l[i:i + cols] for i in range(0, len(l), cols)]

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
    restart_button = pygame.font.Font('freesansbold.ttf', 24).render("Restart Game", True, (0, 0, 0))
    screen.blit(restart_button, (SCREEN_WIDTH - (SCREEN_WIDTH-SCREEN_HEIGHT) + 110, 165))
    title = pygame.font.Font('freesansbold.ttf', 52).render("TIC TAC TOE", True, titleColor)
    screen.blit(title, (SCREEN_WIDTH - (SCREEN_WIDTH-SCREEN_HEIGHT) + 20, 10))
    #chat box
    pygame.draw.line(screen, lineColor,(720, 240),(SCREEN_WIDTH,240) , 4)
    chat_box=pygame.font.Font('freesansbold.ttf', 24).render("Chat Box", True, titleColor)
    screen.blit(chat_box, (SCREEN_WIDTH - (SCREEN_WIDTH-SCREEN_HEIGHT) + 120, 250))
    if(player==1):
        centerMessage("X's Turn",XCOLOR)
    else:
        centerMessage("O's Turn",OCOLOR)
        
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

def centerMessage(msg, color = titleColor):
    pos = (SCREEN_WIDTH - (SCREEN_WIDTH-SCREEN_HEIGHT) + 110, 110)
    msgRendered = pygame.font.Font('freesansbold.ttf', 36).render(msg, True, color)
    screen.blit(msgRendered, pos)

def receive_message():
    global gameOver
    global matrix
    global winnerMatrix
    global player
    global lastMove
    global openMove
    global nextMove
    while True:
        try:
            data = socket.recv(2048*10).decode('utf-8')
            print(data)
            if data=="Open move: False":
                openMove = False
            if data=="Open move: True":
                openMove = True
            
            if data.count(",")==1:
                matrixRevc = list(map(int, data.split(",")))
                nextMove = matrixRevc

            if data.count(",")==80:
                matrixRevc = list(map(int, data.split(",")))
                matrix = convert_1d_to_2d(matrixRevc,9)

            if data.count(",")==8:
                matrixRevc = list(map(int, data.split(",")))
                winnerMatrix = convert_1d_to_2d(matrixRevc,3)

            if data == "Game has been restarted!":
                matrix = [[0 for _ in range(9)] for _ in range(9)]
                winnerMatrix = [[0 for _ in range(3)] for _ in range(3)]
                player = 1
                gameOver = False
                lastMove = None
                openMove = True
                nextMove = [-1,-1]

            if data == "It's a tie!":
                centerMessage("It's a tie!")

            if data == "Player 1 wins!":
                centerMessage("Player 1 wins!")
            
            if data == "Player -1 wins!":
                centerMessage("Player -1 wins!")
                
            if data == "1" or "-1":
                player = int(data)
                print("Player = ",player)

        except Exception as e:
            print(f"Exception occurred: {e}")
            break

def create_thread():
    t=threading.Thread(target=receive_message)
    t.daemon=True
    t.start()

run = True
while run:
    
    create_thread()
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
            if pos >= (0,0) and pos <= (720,720):
                if gameOver == False:
                    if openMove == True:
                        if matrix[mouse_x//80][mouse_y//80] == 0:
                            matrix[mouse_x//80][mouse_y//80] = player
                            player *= -1
                            socket.send(str.encode(str(mouse_x)+","+str(mouse_y),"utf-8"))
                            # check_next_move()
                    elif openMove == False:
                        if matrix[mouse_x//80][mouse_y//80] == -2:
                            matrix[mouse_x//80][mouse_y//80]  = player
                            player *= -1
                            socket.send(str.encode(str(mouse_x)+","+str(mouse_y),"utf-8"))
                            # reset_move()
                            # check_next_move()
            if mouse_x > SCREEN_WIDTH - (SCREEN_WIDTH-SCREEN_HEIGHT) + 100 and mouse_x < SCREEN_WIDTH - (SCREEN_WIDTH-SCREEN_HEIGHT) + 280 and mouse_y > 150 and mouse_y < 200:
                print("Send restart message to server")
                socket.send(str.encode("restart","utf-8"))
    
    drawMarker()
    pygame.display.update()

pygame.quit()
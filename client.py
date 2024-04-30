import pygame
from settings import *
import socket
import threading

matrix = [[0 for _ in range(9)] for _ in range(9)]
winnerMatrix = [[0 for _ in range(3)] for _ in range(3)]
clicked = False
pos = []
player = 1
gameOver = False
winner = 0

host='127.0.0.1'
port=12345

pygame.init()
pygame.display.set_caption("Tic Tac Toe")

socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socket.connect((host,port))

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

def receive_message():
    global gameOver
    global matrix
    global winnerMatrix
    global player
    while True:
        try:
            data = socket.recv(1024).decode('utf-8')
            print(data)
            if data == "Game has been restarted!":
                matrix = [[0 for _ in range(9)] for _ in range(9)]
                winnerMatrix = [[0 for _ in range(3)] for _ in range(3)]
                player = 1
                gameOver = False
            if data=="Game over!":
                print("Game over!")
                gameOver = True
        except Exception as e:
            print(f"Exception occurred: {e}")
            break

def create_thread():
    t=threading.Thread(target=receive_message)
    t.daemon=True
    t.start()

run = True
while run:
    
    drawGrid()
    drawMarker()
    create_thread()

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
                    if matrix[mouse_x//80][mouse_y//80] == 0:
                        matrix[mouse_x//80][mouse_y//80] = player
                        print(matrix[mouse_x//80][mouse_y//80])
                        player *= -1
                        
                       # data = socket.recv(1024).decode("utf-8")
                        

                        # if data == "Game has been restarted!":
                        #     matrix = [[0 for _ in range(9)] for _ in range(9)]
                        #     winnerMatrix = [[0 for _ in range(3)] for _ in range(3)]
                        #     player = 1
                        #     gameOver = False

                        # if data=="Game over!":
                        #     print("Game over!")
                        #     gameOver = True
                        
                        # check_cell_winner()
                        # winner = check_winner()
                        # if winner != 0:
                        #     gameOver = True
                        #     print("player ",winner," win")
            if mouse_x > SCREEN_WIDTH - (SCREEN_WIDTH-SCREEN_HEIGHT) + 100 and mouse_x < SCREEN_WIDTH - (SCREEN_WIDTH-SCREEN_HEIGHT) + 280 and mouse_y > 150 and mouse_y < 200:
                # restart_game()
                print("Send restart message to server")
                socket.send(str.encode("restart","utf-8"))
    pygame.display.update()

pygame.quit()
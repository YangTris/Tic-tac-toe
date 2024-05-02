from settings import *
import socket

host='127.0.0.1'
port=12345
clients=[]

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

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(2)
    print("Server started")
    try:
        while True:
            conn, addr = server.accept()
            print(f"Connection from {addr} has been established!")
            conn.send(bytes("Welcome to the game!", "utf-8"))
            clients.append(conn)
            handle_client(conn, addr)
    except KeyboardInterrupt:
        print("Server shutting down...")
        server.close()

def handle_client(conn, addr):
    global matrix, winnerMatrix, player, gameOver, lastMove, openMove, nextMove
    player = 1
    gameOver = False
    while True:
        data = conn.recv(2048*10).decode("utf-8")
        if not data:
            break
        print(f"Received: {data}")
        if data == "restart":
            matrix = [[0 for _ in range(9)] for _ in range(9)]
            winnerMatrix = [[0 for _ in range(3)] for _ in range(3)]
            player = 1
            gameOver = False
            lastMove = None
            openMove = True
            nextMove = [-1,-1]
            conn.sendall(bytes("Game has been restarted!", "utf-8"))
        else:
            data = data.split(",")
            x = int(data[0])
            y = int(data[1])
            if matrix[x][y] == 0:
                matrix[x][y] = player
                player = -1 if player == 1 else 1
                check_cell_winner()
                winner = check_winner()
                send_msg("Server matrix= ")
                send_matrix(matrix)
                if winner == -2:
                    gameOver = True
                    conn.send(bytes("Game over!", "utf-8"))
                    conn.send(bytes("It's a tie!", "utf-8"))
                if winner != 0:
                    gameOver = True
                    conn.send(bytes(f"Game over!", "utf-8"))
                    conn.send(bytes(f"Player {winner} wins!", "utf-8"))
            else:
                conn.send(bytes("Invalid move!", "utf-8"))
    conn.close()

def send_msg(message):
    for client in clients:
        client.send(message.encode("utf-8"))

def send_matrix(matrix):
    string = ""
    for i in range(9):
        for j in range(9):
            if i== j == 8:
                string += str(matrix[i][j])
            else:
                string += str(matrix[i][j]) + ","
    send_msg(string)
    
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
    #X,Y,Player
    send_msg(str(x)+","+str(y)+","+str(player))
    send_msg("Server winnerMatrix: "+str(winnerMatrix))
    print(winnerMatrix)

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

def check_cell_winner():
    result = 0
    result = check_columns()
    if result == 0:
        result = check_rows()
    if result == 0:
        result = check_diagonals()
    return result

def check_winner():
    winner = 0
    pos = 0
    for i in winnerMatrix:
        #check columns
        if sum(i) == 3:
            winner = 1
        if sum(i) == -3:
            winner = -1
        #check rows
        if winnerMatrix[0][pos] == winnerMatrix[1][pos] == winnerMatrix[2][pos]:
            if winnerMatrix[0][pos]!=0:
                winner = winnerMatrix[0][pos]
        pos+=1
    
    #check diagonals
    if winnerMatrix[0][0] == winnerMatrix[1][1] == winnerMatrix[2][2]:
        if winnerMatrix[0][0] != 0:
            winner = winnerMatrix[0][0]
    if winnerMatrix[2][0] == winnerMatrix[1][1] == winnerMatrix[0][2]:
        if winnerMatrix[2][0] != 0:
            winner = winnerMatrix[2][0]
        
    return winner

def reset_move():
    if nextMove != [-1,-1]:
        for i in range(3):
            for j in range(3):
                if matrix[nextMove[0]+i][nextMove[1]+j] == -2:
                    matrix[nextMove[0]+i][nextMove[1]+j] = 0

if __name__ == "__main__":
    start_server()

from settings import *
import socket

matrix = [[0 for _ in range(9)] for _ in range(9)]
winnerMatrix = [[0 for _ in range(3)] for _ in range(3)]

host='127.0.0.1'
port=12345
clients=[]


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(2)
    print("Server started")
    try:
        while True:
            conn, addr = server.accept()
            print(f"Connection from {addr} has been established!")
            conn.send(bytes("Welcome to the server!", "utf-8"))
            clients.append(conn)
            handle_client(conn, addr)
    except KeyboardInterrupt:
        print("Server shutting down...")
        server.close()

def handle_client(conn, addr):
    global matrix, winnerMatrix, player, gameOver
    player = 1
    gameOver = False
    while True:
        data = conn.recv(1024).decode("utf-8")
        if not data:
            break
        print(f"Received: {data}")
        if data == "restart":
            matrix = [[0 for _ in range(9)] for _ in range(9)]
            winnerMatrix = [[0 for _ in range(3)] for _ in range(3)]
            player = 1
            gameOver = False
            # conn.sendall(bytes("Game has been restarted!", "utf-8"))
            for client in clients:
                client.send(bytes("Game has been restarted!", "utf-8"))
        else:
            data = data.split(",")
            x = int(data[0])
            y = int(data[1])
            if matrix[x][y] == 0:
                matrix[x][y] = player
                player = -1 if player == 1 else 1
                result = check_cell_winner()
                if result != 0:
                    gameOver = True
                    conn.send(bytes(f"Game over!", "utf-8"))
                    conn.send(bytes(f"Player {result} wins!", "utf-8"))
                else:
                    conn.send(bytes("Move has been made!", "utf-8"))
            else:
                conn.send(bytes("Invalid move!", "utf-8"))
    conn.close()

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

if __name__ == "__main__":
    start_server()

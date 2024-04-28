import socket
import pickle
import time

s = socket.socket()
host = "127.0.0.1"
port = 9999
matrix = [[0 for _ in range(9)] for _ in range(9)]
# print(matrix)

playerOne = 1
playerTwo = 2

playerConn = list()
playerAddr = list()       
restart_requests = [False, False]

#server side validation is disabled to reduce latency
'''
def validate_input(x, y, conn):
    if x > 3 or y > 3:
        print("\nOut of bound! Enter again...\n")
        conn.send("Error".encode())
        return False
    elif matrix[x][y] != 0:
        print("\nAlready entered! Try again...\n")
        conn.send("Error".encode())
        return False
    return True
'''

def get_input(currentPlayer):
    if currentPlayer == playerOne:
        player = "Player One's Turn"
        conn = playerConn[0]
    else:
        player = "Player Two's Turn"
        conn = playerConn[1]
    print(player)
    send_common_msg(player)
    try:
        conn.send("Input".encode())
        data = conn.recv(2048 * 10)
        conn.settimeout(20)
        dataDecoded = data.decode().split(",")
        x = int(dataDecoded[0])
        y = int(dataDecoded[1])
        matrix[x][y] = currentPlayer
        send_common_msg("Matrix")
        send_common_msg(str(matrix))
    except:
        conn.send("Error".encode())
        print("Error occured! Try again..")

def check_rows():
    # print("Checking rows")
    result = 0
    for i in range(9):
        if matrix[i][0] == matrix[i][1] == matrix[i][2]:
            result = matrix[i][0]
            if result != 0:
                break

        if matrix[i][3] == matrix[i][4] == matrix[i][5]:
            result = matrix[i][3]
            if result != 0:
                break
        
        if matrix[i][6] == matrix[i][7] == matrix[i][8]:
            result = matrix[i][6]
            if result != 0:
                break

    return result

def check_columns():
    # print("Checking cols")
    result = 0
    for i in range(9):
        if matrix[0][i] == matrix[1][i] == matrix[2][i]:
            result = matrix[0][i]
            if result != 0:
                break
        if matrix[3][i] == matrix[4][i] == matrix[5][i]:
            result = matrix[3][i]
            if result != 0:
                break
        if matrix[6][i] == matrix[7][i] == matrix[8][i]:
            result = matrix[6][i]
            if result != 0:
                break
    return result

def check_diagonals():
    # print("Checking diagonals")
    result = 0
    # if matrix[0][0] == matrix[1][1] and matrix[1][1] == matrix[2][2]:
    #     result = matrix[0][0]
    # elif matrix[0][2] == matrix[1][1] and matrix[1][1] == matrix[2][0]:
    #     result = matrix[0][2]
    for x in [0,3,6,2,5,8]:
        if x%3==0:
            y=x+1
            z=x+2
        else:
            y=x-1
            z=x-2

        if matrix[x][0] == matrix[y][1] == matrix[z][2]:
            result = matrix[x][0]
            if result != 0:
                break
        if matrix[x][3] == matrix[y][4] == matrix[z][5]:
            result = matrix[x][3]
            if result != 0:
                break
        if matrix[x][6] == matrix[y][7] == matrix[z][8]:
            result = matrix[x][6]
            if result != 0:
                break

    return result

def check_winner():
    result = 0
    result = check_rows()
    if result == 0:
        result = check_columns()
    if result == 0:
        result = check_diagonals()
    return result

#Socket program
def start_server():
    #Binding to port 9999
    #Only two clients can connect 
    try:
        s.bind((host, port))
        print("Tic Tac Toe server started \nBinding to port", port)
        s.listen(2) 
        accept_players()
    except socket.error as e:
        print("Server binding error:", e)
    

#Accept player
#Send player number
def accept_players():
    try:
        for i in range(2):
            conn, addr = s.accept()
            msg = "<<< You are player {} >>>".format(i+1)
            conn.send(msg.encode())

            playerConn.append(conn)
            playerAddr.append(addr)
            print("Player {} - [{}:{}]".format(i+1, addr[0], str(addr[1])))
    
        start_game()
        s.close()
    except socket.error as e:
        print("Player connection error", e)
    except KeyboardInterrupt:
            print("\nKeyboard Interrupt")
            exit()
    except Exception as e:
        print("Error occurred:", e)



def start_game():
    result = 0
    i = 0
    while result == 0 and i < 81 :
        if (i%2 == 0):
            get_input(playerOne)
        else:
            get_input(playerTwo)
        result = check_winner()
        i = i + 1
        # print("Current count", i ,result == 0 and i < 9, "Result = ", result)

    send_common_msg("Over")

    if result == 1:
        lastmsg = "Player One is the winner!!"
    elif result == 2:
        lastmsg = "Player Two is the winner!!"
    else:
        lastmsg = "Draw game!! Try again later!"

    send_common_msg(lastmsg)
    
    wait_for_restart_requests()

    time.sleep(10)
    for conn in playerConn:
        conn.close()
    
def restart_game():
    global matrix, restart_requests
    matrix = [[0 for _ in range(9)] for _ in range(9)]
    # Reset restart requests
    restart_requests = [False, False]
    for conn in playerConn:
        conn.send("Restart".encode())

def wait_for_restart_requests():
    global restart_requests
    while not all(restart_requests):
        time.sleep(1)
    restart_game()

def handle_restart_request(player_number):
    restart_requests[player_number - 1] = True
    # Check if both clients requested a restart
    if all(restart_requests):
        restart_game()

def accept_msg():
    global matrix
    global msg
    global bottomMsg 
    global allow
    global xy
    while True:
        try: 
            recvData = s.recv(2048 * 10)
            recvDataDecode = recvData.decode()

            if recvDataDecode == "RestartAgree":
                handle_restart_request()  

            # Existing code...
            
        except KeyboardInterrupt:
            print("\nKeyboard Interrupt")
            time.sleep(1)
            break

        except:
            print("Error occured")
            break


def send_common_msg(text):
    playerConn[0].send(text.encode())
    playerConn[1].send(text.encode())
    time.sleep(1)

start_server()
import socket
import threading
import time


SIZE = 1024
FORMAT = "utf-8"
IP = socket.gethostbyname(socket.gethostname())
PORT = 5568
ADDR = (IP,PORT)

def takeBoatLocs(c,boats):
    array = []
    for i in range(9):
        a = c.recv(SIZE).decode(FORMAT)
        array.append(int(a))
        if(i==0):
            boats.append(array)
            array.clear()
        elif(i==2):
            boats.append(array)
            array.clear()
        elif(i==4):
            boats.append(array)
            array.clear()
        elif(i==8):
            boats.append(array)
            array.clear()
    return

loc = -1

def handleGame(c1,c2):

    time.sleep(4)

    c1.send("Your Turn".encode(FORMAT))
    c2.send("Opponenets Turn".encode(FORMAT))

    for i in range(9):
        m1 = c1.recv(SIZE)
        c2.send(m1)
        m1 = c2.recv(SIZE)
        c1.send(m1)

    while True:
        msg = c1.recv(SIZE)
        c2.send(msg)
        msg = c2.recv(SIZE)
        c1.send(msg)

    c1.close()
    c2.close()

def main():

    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()

    while True:

        c1,a1 = server.accept()
        print("1👦 ")
        
        c2,a2 = server.accept()
        print(" 🧑2 \n")
        
        playGame = threading.Thread(target=handleGame,args=(c1,c2))
        playGame.start()

if __name__=="__main__":
    main()



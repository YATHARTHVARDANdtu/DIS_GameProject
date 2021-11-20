import socket
import threading

username = {}
SIZE = 1024
FORMAT = "utf-8"
IP = socket.gethostbyname(socket.gethostname())
PORT = 5566
ADDR = (IP,PORT)
one = "1"
two = "2"


def handleAGame(c1,a1,c2,a2):

    c1.send("Your turn".encode(FORMAT))
    c2.send("Opponents turn".encode(FORMAT))
    while True:
        msg = c1.recv(SIZE).decode(FORMAT)
        if(msg == "finish"):
            break
        c2.send(msg.encode(FORMAT))
        msg = c2.recv(SIZE).decode(FORMAT)
        if(msg == "finish"):
            break
        c1.send(msg.encode(FORMAT))
    c1.close()
    c2.close()



def main():
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()


    while True:
        
        c1,a1 = server.accept()
        # c1.send("wait".encode(FORMAT))
        print("\nFirst player joined :- ")

        
        c2,a2 = server.accept()
        # c2.send("play".encode(FORMAT))
        # c1.send("play".encode(FORMAT))

        print("\nSecond player has joined")

        game = threading.Thread(target=handleAGame,args=(c1,a1,c2,a2))
        print("\n\tLet the game begin")
        game.start()

if __name__=="__main__":
    main()    

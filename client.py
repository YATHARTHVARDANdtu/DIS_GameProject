from os import error
import socket
import threading
from tkinter import *
from tkinter import messagebox
import tkinter
from tkinter import font
from typing import ChainMap, Literal
from PIL import Image,ImageTk
from queue import Queue
import time
from tkinter.constants import DISABLED, NORMAL
from tkinter import Canvas
from playsound import playsound


import sys

FORMAT = "utf-8"
SIZE = 1024
IP = socket.gethostbyname(socket.gethostname())
gameServerPort = 5566
ADDR = (IP,gameServerPort)

def stopTkinter():
    window.destroy()

window = Tk()
window.title("Game - Client")
window.geometry("300x300+5+5")


# waitingWindow = Tk()
# waitingWindow.title("Waiting for the second player")
# waitingWindow.geometry("500x500+40+40")

var = StringVar()

client2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#message box for capturing the clicked buttons
one = Queue()

#buttons for input
buttons = []


gameOver = False
#board result checker
checker = [[0,1,2],[0,3,6],[0,4,8],[1,4,7],[2,5,8],[2,4,6],[3,4,5],[6,7,8]]

def checkResult(playerOrder):
    for i in range(len(checker)):
        ex = 0
        os = 0
        flag = False
        for j in range(3):
            if buttons[checker[i][j]].value == 'X':
                ex = ex+1
            elif buttons[checker[i][j]].value=='O':
                os = os+1
            else:
                flag = True
                break

        if not flag:
            if ex==3:
                if(playerOrder):
                    return "win"
                else:
                    return "lose"
            elif os==3:
                if(playerOrder):
                    return "lose"
                else:
                    return "win"
    
    return "continue"

#line creater
class Example(Frame):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        self.master.title("Lines")
        self.pack(fill=BOTH, expand=1)

        canvas = Canvas(self)
        canvas.create_line(105, 8, 105, 170)
        canvas.pack(fill=BOTH, expand=1)         





class button:

    i = 0
    btn = None
    value = ' '
    show = ' '
    response = -1
    pressed = False
    changeState = True

    def __init__(self):
        self.btn = Button(window, width=4,height=1,text=' ',font="monospace",relief=SOLID,borderwidth=1)

    def place(self, left, top,i):
        self.btn.place(x=left,y=top)
        self.btn['command'] = self.change
        self.i = self.i+1
        self.response = i
        self.pressed = False

    def val(self,input):
        self.show = input

    def change(self):
        if var=="Opponents Turn":
            #print("It is working")
            return
        if self.pressed:
            #print("Yup")
            return

        one.put(self.response)
        self.changeState = False
        self.value = self.show
        self.btn['text'] = self.value
        self.btn['foreground'] = "black"
        if(self.i == 1):
            self.btn['bd'] = 0
            self.btn['command'] = None
            #print("Button " + str(self.response)+"\n")
            self.pressed = True

    def state(self):
        return self.changeState

    def updateBoard(self, value):
        if(self.pressed):
            return
        self.btn['bd'] = 0
        self.btn['command'] = None
        self.btn['text'] = value
        self.value = value
        self.pressed = True
        self.btn['foreground'] = "black"

        # print("opponent pressed Button" + str(self.response)+"\n")


def winningSound():
    playsound("win.wav")
    return

def losingSound():
    playsound("lose.wav")
    return

def drawingSound():
    playsound("draw.wav")
    return


win = threading.Thread(target=winningSound)
lose = threading.Thread(target = losingSound)
draw = threading.Thread(target = drawingSound)

def first():
    global moves
    moves = 0

    while True:
        var.set("Your Turn")
        while one.qsize==0:
             if(one.qsize > 0):
                 break
        msg = one.get()

        buttons[0].btn['state'] = DISABLED
        buttons[1].btn['state'] = DISABLED
        buttons[2].btn['state'] = DISABLED
        buttons[3].btn['state'] = DISABLED
        buttons[4].btn['state'] = DISABLED
        buttons[5].btn['state'] = DISABLED
        buttons[6].btn['state'] = DISABLED
        buttons[7].btn['state'] = DISABLED
        buttons[8].btn['state'] = DISABLED

        client2.send(str(msg).encode(FORMAT))
        
        moves = moves+1
        response = checkResult(True)
        if response=="win" or response=="lose":
            if response=="win":
                response = "You Won 😁"
                win.start()
                gameOver = True
            else:
                response = "You Lost 😖"
                lose.start()
                gameOver = True
            
            messagebox.showinfo("Result",response)
            stopTkinter()
            break
        
        if moves==9 and response=="continue":
            response = "Match Drawn 🤯"
            draw.start()
            messagebox.showinfo("Result",response)
            stopTkinter()
            break

        var.set("Opponents Turn")
        msg = client2.recv(SIZE).decode(FORMAT)
        btn = int(msg)
        buttons[btn].updateBoard('O')

        
        moves = moves+1
        response = checkResult(True)
        print(response)
        if response=="win" or response=="lose":
            if response=="win":
                response = "You Won 😁"
                win.start()

            else:
                response = "You Lost 😖"
                lose.start()
            messagebox.showinfo("Result",response)
            stopTkinter()
            break
        
        if moves==9 and response=="continue":
            response = "Match Drawn 🤯"
            draw.start()
            messagebox.showinfo("Result",response)
            stopTkinter()
            break

        buttons[0].btn['state'] = NORMAL
        buttons[1].btn['state'] = NORMAL
        buttons[2].btn['state'] = NORMAL
        buttons[3].btn['state'] = NORMAL
        buttons[4].btn['state'] = NORMAL
        buttons[5].btn['state'] = NORMAL
        buttons[6].btn['state'] = NORMAL
        buttons[7].btn['state'] = NORMAL
        buttons[8].btn['state'] = NORMAL

        # btn = int(msg)
        # buttons[btn].updateBoard('O')
    try:
        client2.send("finish".encode(FORMAT))
    except:
        print("Error")
    client2.close()



def second(): 
    global moves
    moves = 0
    while True:
        buttons[0].btn['state'] = DISABLED
        buttons[1].btn['state'] = DISABLED
        buttons[2].btn['state'] = DISABLED
        buttons[3].btn['state'] = DISABLED
        buttons[4].btn['state'] = DISABLED
        buttons[5].btn['state'] = DISABLED
        buttons[6].btn['state'] = DISABLED
        buttons[7].btn['state'] = DISABLED
        buttons[8].btn['state'] = DISABLED

        var.set("Opponents Turn")
        msg = client2.recv(SIZE).decode(FORMAT)
        btn = int(msg)
        buttons[btn].updateBoard('X')

        moves = moves+1
        response = checkResult(False)
        print(response)
        if response=="win" or response=="lose":
            if response=="win":
                response = "You Won 😁"
                win.start()
            else:
                response = "You Lost 😖"
                lose.start()
            
            messagebox.showinfo("Result",response)
            stopTkinter()
            break
        
        if moves==9 and response=="continue":
            response = "Match Drawn 🤯"
            draw.start()
            messagebox.showinfo("Result",response)
            stopTkinter()
            break
        # if response=="win":
        #     messagebox.showinfo("result","You WIN !!!")
        #     break
        # elif response=="lose":
        #     messagebox.showinfo("result","You Lose :(")
        #     break
        buttons[0].btn['state'] = NORMAL
        buttons[1].btn['state'] = NORMAL
        buttons[2].btn['state'] = NORMAL
        buttons[3].btn['state'] = NORMAL
        buttons[4].btn['state'] = NORMAL
        buttons[5].btn['state'] = NORMAL
        buttons[6].btn['state'] = NORMAL
        buttons[7].btn['state'] = NORMAL
        buttons[8].btn['state'] = NORMAL

        # btn = int(msg)
        # buttons[btn].updateBoard('X')
        var.set("Your Turn")
        while one.qsize==0:
             if(one.qsize > 0):
                 break
        msg = one.get()
        client2.send(str(msg).encode(FORMAT))

       
        moves = moves+1
        response = checkResult(False)
        print(response)
        if response=="win" or response=="lose":
            if response=="win":
                response = "You Won 😁"
                win.start()
            else:
                response = "You Lost 😖"
                lose.start()
            
            messagebox.showinfo("Result",response)
            stopTkinter()
            break
        
        if moves==9 and response=="continue":
            response = "Match Drawn 🤯"
            draw.start()
            messagebox.showinfo("Result",response)
            stopTkinter()
            break
    
    try:
        client2.send("finish".encode(FORMAT))
    except:
        print("Error")
    client2.close()


def main():
    client2.connect(ADDR)
    msg = client2.recv(SIZE).decode(FORMAT)
    # if(msg=="wait"):
        
    #     img = PhotoImage(file="Waiting For Second player.gif")
    #     label = Label(waitingWindow,image=img)
    #     label.place(x=0, y=0)
    #     wait = threading.Thread(target = waitThread)
    #     wait.start()
    #     waitingWindow.mainloop()
    
    flag = False

    # msg = client2.recv(SIZE).decode(FORMAT)
    if(msg=="Your turn"):
        flag = True
        playerOrder = True
    else:
        playerOrder = False
        turn = False


    s = 65
    r = 30
    x = s
    y = r
    for i in range(9):
        if i%3==0:
            x = s
            y = y + 40
        btn = button()
        btn.place(x,y,i)
        if flag:
            btn.val("X")
        else:
            btn.val("O")
        x = x+55
        buttons.append(btn)

    l = Label(window,textvariable=var)
    l.pack()


    if(msg=="Your turn"):
        f = threading.Thread(target=first)
        f.start()

    else:
        s = threading.Thread(target=second)
        s.start()

    

    window.mainloop()
    sys.exit()

if __name__ == "__main__":
    main()
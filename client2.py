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


buttons = []
buttonOpponent = []
canPlay = True
FORMAT = "utf-8"
SIZE = 1024
IP = socket.gethostbyname(socket.gethostname())
gameServerPort = 5568
ADDR = (IP,gameServerPort)
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

window = Tk()
window.title("Battleship")
window.geometry("800x540+20+20")

yBoats = 9
oBoats = 9

def winningSound():
    playsound("win.wav")
    return

def losingSound():
    playsound("lose.wav")
    return

win = threading.Thread(target=winningSound)
lose = threading.Thread(target = losingSound)

displayBoat1 = {
    "l1":Label(window,height=1,width=3,background="green")
}
displayOBoat1 = {
    "l1":Label(window,height=1,width=3,background="green")
}


displayBoat2 = {
    "ls":[Label(window,height=1,width = 3,background="green"),Label(window,height=1,width = 3,background="green")],
    "position":-1
}

displayOBoat2 = {
    "ls":[Label(window,height=1,width = 3,background="green"),Label(window,height=1,width = 3,background="green")],
    "position":-1
}


displayBoat3 = {
    "ls":[Label(window,height=1,width = 3,background="green"),Label(window,height=1,width = 3,background="green")],
    "position":-1
}

displayOBoat3 = {
    "ls":[Label(window,height=1,width = 3,background="green"),Label(window,height=1,width = 3,background="green")],
    "position":-1
}

displayBoat4 = {
    "ls":[Label(window,height=1,width = 3,background="green"),Label(window,height=1,width = 3,background="green"),Label(window,height=1,width = 3,background="green"),Label(window,height=1,width = 3,background="green")],
    "position":-1
}

displayOBoat4 = {
    "ls":[Label(window,height=1,width = 3,background="green"),Label(window,height=1,width = 3,background="green"),Label(window,height=1,width = 3,background="green"),Label(window,height=1,width = 3,background="green")],
    "position":-1
}


def hit():
    playsound("hit.wav")
    return

def miss():
    playsound("miss.wav")
    return

stopPlay = False
 
yourBoats = 9
oppBoats = 9
one = Queue()

#type of boats 
#
#  *       *         *      *
# size1   size1      *      **
#                 size2     size3
#total boats 4

boat1 = {
    "boxNumber":-1,
    "destroyed":False,
    "placed":False
}

boat2 = {
    "boxNumber":[-1,-1],
    "destroyed":False,
    "placed":False
}

boat3={
    "boxNumber":[-1,-1],
    "destroyed":False,
    "placed":False
}

boat4 = {
    "boxNumber":[-1,-1,-1,-1],
    "destroyed":False,
    "placed":False,
    "hor":False,
}

class button:

    i = 0
    btn = None
    value = ' '
    show = ' '
    response = -1
    pressed = False
    changeState = True

    boatNumber = -1

    def __init__(self):
        self.btn = Button(window, width=4,height=1,text=' ',font="monospace",relief=SOLID,borderwidth=1)
    
    def place(self, left, top,i):
        self.btn.place(x=left,y=top)
        self.btn['command'] = self.placeBoat
        self.i = self.i+1
        self.response = i
        self.pressed = False
        self.show = "Miss"


    def placeBoat(self):
        if self.show=='Hit':
            return
        global yourBoats

        if boat1['placed'] == False:
            yourBoats-=1
            boat1['placed'] = True
            boat1['boxNumber'] = self.response
            self.boatNumber = 1
        
        elif boat2['placed'] == False:
            if boat2['boxNumber'][0]==-1:
                yourBoats-=1
                boat2['boxNumber'][0] = self.response
                self.boatNumber = 2
            else:
                prev = boat2['boxNumber'][0]
                if self.response == prev+1 or self.response == prev-1 or self.response == prev-6 or self.response == prev+6:
                    yourBoats-=1
                    boat2['boxNumber'][1] = self.response
                    self.boatNumber = 2
                    boat2['placed'] = True
                else:
                    return
        
        elif boat3['placed'] == False:
            if boat3['boxNumber'][0]==-1:
                yourBoats-=1
                boat3['boxNumber'][0] = self.response
                self.boatNumber = 3
            else:
                prev = boat3['boxNumber'][0]
                if self.response == prev+1 or self.response == prev-1 or self.response == prev-6 or self.response == prev+6:
                    yourBoats-=1
                    boat3['boxNumber'][1] = self.response
                    self.boatNumber = 3
                    boat3['placed'] = True
                else:
                    return
        
        elif boat4['placed'] == False :
            if boat4['boxNumber'][0]==-1:
                yourBoats-=1
                boat4['boxNumber'][0] = self.response
                self.boatNumber = 4

            elif boat4['boxNumber'][1]==-1:
                ar1 = [1,-1,-6,-5,-7,7,6,5]
                prev = boat4['boxNumber'][0]
                
                value = self.response-prev

                exists = value in ar1
                if exists:
                    yourBoats-=1
                    boat4['boxNumber'][1] = self.response
                    self.boatNumber = 4
                else:
                    return
            elif boat4['boxNumber'][2]==-1:
                b = boat4['boxNumber'][1]
                a = boat4['boxNumber'][0]

                x1 = int(a/6)
                y1 = a%6
                x2 = int(b/6)
                y2 = b%6

                x3 = int(self.response/6)
                y3 = self.response%6
                if x1==x2:
                    if abs(x3-x1)==1 and y3>=min(y1,y2) and y3<=max(y1,y2):
                        yourBoats-=1
                        boat4['boxNumber'][2] = self.response
                        self.boatNumber = 4
                    else:
                        return
                elif y1==y2:
                    if abs(y3-y1)==1 and x3>=min(x1,x2) and x3<=max(x1,x2):
                        yourBoats-=1
                        boat4['boxNumber'][2] = self.response
                        self.boatNumber = 4
                    else:
                        return
                else:
                    if x3>=min(x1,x2) and x3<=max(x1,x2) and y3>=min(y1,y2) and y3<=max(y1,y2):
                        yourBoats-=1
                        boat4['boxNumber'][2] = self.response
                        self.boatNumber = 4
                    else:
                        return

            elif boat4['boxNumber'][3]==-1:
                c = boat4['boxNumber'][2]
                b = boat4['boxNumber'][1]
                a = boat4['boxNumber'][0]

                x1 = int(a/6)
                y1 = a%6
                x2 = int(b/6)
                y2 = b%6
                x3 = int(c/6)
                y3 = c%6

                x4 = int(self.response/6)
                y4 = self.response%6

                if x4>=min(x1,x2,x3) and x4<=max(x1,x2,x3) and y4>=min(y1,y2,y3) and y4<=max(y1,y2,y3):
                    yourBoats-=1
                    boat4['boxNumber'][3] = self.response
                    self.boatNumber = 4
                else:
                    return
        self.show = "Hit"
        self.btn['background'] = 'Green'
    
    def changeCommand(self):
        self.btn['command'] = None
    def changeCommand2(self):
        self.btn['command'] = self.change

    def change(self):
        if self.pressed:
            return

        if canPlay==False:
            return
        
        self.changeState = False
        self.value = self.show
        one.put(self.response)

        if(self.value=='Hit'):
            explosion  = threading.Thread(target=hit)
            explosion.start()
        if(self.value=='Miss'):
            shotMiss = threading.Thread(target=miss)
            shotMiss.start()

        self.btn['foreground'] = "black"
        if self.value=="Hit":
            self.btn['background'] = '#D47F7F'
            self.destroy(self.boatNumber)
        else:
            self.btn['background'] = '#D7E4FF'
        if(self.i == 1):
            self.btn['command'] = None
            self.pressed = True

    def destroy(self,bNumber):
        
        global oBoats,stopPlay
        oBoats-=1
        
        if bNumber == 1:            
            displayOBoat1["l1"].config(background="red")
            

        elif bNumber==2:
            displayOBoat2["position"]+=1
            if(displayOBoat2["position"]==1):
                for i in range(2):
                    displayOBoat2["ls"][i].config(background = "red")

            
        
        elif bNumber==3:
            displayOBoat3["position"]+=1

            if(displayOBoat3["position"]==1):
                for i in range(2):
                    displayOBoat3["ls"][i].config(background = "red")
            
        
        elif bNumber==4:
            displayOBoat4["position"]+=1
            if(displayOBoat3["position"]==3):
                for i in range(4):
                    displayOBoat4["ls"][i].config(background = "red")

        if(oBoats == 0):
            print("You Win")
            win.start()
            messagebox.showinfo("Result","You Win (⌐■_■)")
            stopPlay = True





    def damage(self,bNumber):
        global yBoats,stopPlay
        yBoats-=1

        if bNumber == 1:            
            displayBoat1["l1"].config(background="red")


        elif bNumber==2:
            displayBoat2["position"]+=1
            if(displayBoat2["position"]==1):
                for i in range(2):
                    displayBoat2["ls"][i].config(background = "red")

        
        elif bNumber==3:
            displayBoat3["position"]+=1
            if(displayBoat3["position"]==1):
                for i in range(2):
                    displayBoat3["ls"][i].config(background = "red")

        
        elif bNumber==4:
            displayBoat4["position"]+=1
            if(displayBoat4["position"]==3):
                for i in range(4):
                    displayBoat4["ls"][i].config(background = "red")


        if(yBoats == 0):
            print("You Lose")
            lose.start()
            messagebox.showinfo("Result","You Lose (┬┬﹏┬┬)")
            stopPlay = True


    def updateBoard(self):
        if(self.pressed):
            return
        self.btn['command'] = None
        self.value = self.show

        if(self.value=='Hit'):
            explosion  = threading.Thread(target=hit)
            explosion.start()
        if(self.value=='Miss'):
            shotMiss = threading.Thread(target=miss)
            shotMiss.start()
        self.pressed = True
        self.btn['foreground'] = "black"
        if self.value=="Hit":
            self.btn['background'] = '#D47F7F'
            self.damage(self.boatNumber)
        else:
            self.btn['background'] = '#D7E4FF'


def placeBoats():
    banner = StringVar()
    l1 = Label(window,font=("monospace",18),textvariable=banner)
    l1.place(x = 50,y=20)
    l1.pack()

    banner.set("Place 1st boat of size 1")
    while yourBoats>8:
        if yourBoats==8:
            break
    
    banner.set("Place 2nd boat of size 2")
    while yourBoats>6:
        if yourBoats==6:
            break
    
    banner.set("Place 3rd boat of size 2")
    while yourBoats>4:
        if yourBoats==4:
            break
    
    banner.set("Place 4th boat of size 4")
    while yourBoats>0:
        if yourBoats==0:
            break
    l1.destroy()
    for i in range(36):
        buttons[i].btn['command'] = ""
        buttonOpponent[i].btn['command'] = buttonOpponent[i].change
    

    boat2['boxNumber'].sort()
    boat3['boxNumber'].sort()
    boat4['boxNumber'].sort()


# img1 = None
# test = None
# label1 = None

firstMessage = None



def first():
    while yourBoats>0:
        if yourBoats==0:
            break
    global canPlay,oBoats,yBoats,stopPlay

    client.send(str(boat1['boxNumber']).encode(FORMAT))
    a = client.recv(SIZE).decode(FORMAT)
    buttonOpponent[int(a)].show = 'Hit'
    buttonOpponent[int(a)].boatNumber = 1

    client.send(str(boat2['boxNumber'][0]).encode(FORMAT))
    a = client.recv(SIZE).decode(FORMAT)
    buttonOpponent[int(a)].show = 'Hit'
    buttonOpponent[int(a)].boatNumber = 2

    client.send(str(boat2['boxNumber'][1]).encode(FORMAT))
    a = client.recv(SIZE).decode(FORMAT)
    buttonOpponent[int(a)].show = 'Hit'
    buttonOpponent[int(a)].boatNumber = 2
   
    client.send(str(boat3['boxNumber'][0]).encode(FORMAT))
    a = client.recv(SIZE).decode(FORMAT)
    buttonOpponent[int(a)].show = 'Hit'
    buttonOpponent[int(a)].boatNumber = 3
  
    client.send(str(boat3['boxNumber'][1]).encode(FORMAT))
    a = client.recv(SIZE).decode(FORMAT)
    buttonOpponent[int(a)].show = 'Hit'
    buttonOpponent[int(a)].boatNumber = 3
  
    client.send(str(boat4['boxNumber'][0]).encode(FORMAT))
    a = client.recv(SIZE).decode(FORMAT)
    buttonOpponent[int(a)].show = 'Hit'
    buttonOpponent[int(a)].boatNumber = 4
   
    client.send(str(boat4['boxNumber'][1]).encode(FORMAT))
    a = client.recv(SIZE).decode(FORMAT)
    buttonOpponent[int(a)].show = 'Hit'
    buttonOpponent[int(a)].boatNumber = 4
  
    client.send(str(boat4['boxNumber'][2]).encode(FORMAT))
    a = client.recv(SIZE).decode(FORMAT)
    buttonOpponent[int(a)].show = 'Hit'
    buttonOpponent[int(a)].boatNumber = 4
   
    client.send(str(boat4['boxNumber'][3]).encode(FORMAT))
    a = client.recv(SIZE).decode(FORMAT)
    buttonOpponent[int(a)].show = 'Hit'
    buttonOpponent[int(a)].boatNumber = 4


    banner = StringVar()
    l1 = Label(window,font=("monospace",18),textvariable=banner)
    l1.place(x = 50,y=20)
    l1.pack()
    while True:
        banner.set("Your Turn")
        while one.qsize==0:
            if one.qsize>0:
                break
        msg = one.get()
        canPlay = False
        client.send(str(msg).encode(FORMAT))
        if stopPlay:
            window.destroy()
            break
        
        banner.set("Opponents Turn")
        msg = client.recv(SIZE).decode(FORMAT)
        buttons[int(msg)].updateBoard()
        if(stopPlay):
            window.destroy()
            break
        canPlay = True
    
def second():
    while yourBoats>0:
        if yourBoats==0:
            break
    global canPlay,yBoats,oBoats,stopPlay


    
    a = client.recv(SIZE).decode(FORMAT)
    client.send(str(boat1['boxNumber']).encode(FORMAT))
    buttonOpponent[int(a)].show = 'Hit'
    buttonOpponent[int(a)].boatNumber = 1

    
    a = client.recv(SIZE).decode(FORMAT)
    client.send(str(boat2['boxNumber'][0]).encode(FORMAT))
    buttonOpponent[int(a)].show = 'Hit'
    buttonOpponent[int(a)].boatNumber = 2

    
    a = client.recv(SIZE).decode(FORMAT)
    client.send(str(boat2['boxNumber'][1]).encode(FORMAT))
    buttonOpponent[int(a)].show = 'Hit'
    buttonOpponent[int(a)].boatNumber = 2
    
    
    a = client.recv(SIZE).decode(FORMAT)
    client.send(str(boat3['boxNumber'][0]).encode(FORMAT))
    buttonOpponent[int(a)].show = 'Hit'
    buttonOpponent[int(a)].boatNumber = 3
  
    
    a = client.recv(SIZE).decode(FORMAT)
    client.send(str(boat3['boxNumber'][1]).encode(FORMAT))
    buttonOpponent[int(a)].show = 'Hit'
    buttonOpponent[int(a)].boatNumber = 3
    
    
    a = client.recv(SIZE).decode(FORMAT)
    client.send(str(boat4['boxNumber'][0]).encode(FORMAT))
    buttonOpponent[int(a)].show = 'Hit'
    buttonOpponent[int(a)].boatNumber = 4
   
    
    a = client.recv(SIZE).decode(FORMAT)
    client.send(str(boat4['boxNumber'][1]).encode(FORMAT))
    buttonOpponent[int(a)].show = 'Hit'
    buttonOpponent[int(a)].boatNumber = 4
    
    
    a = client.recv(SIZE).decode(FORMAT)
    client.send(str(boat4['boxNumber'][2]).encode(FORMAT))
    buttonOpponent[int(a)].show = 'Hit'
    buttonOpponent[int(a)].boatNumber = 4
   
    a = client.recv(SIZE).decode(FORMAT)
    client.send(str(boat4['boxNumber'][3]).encode(FORMAT))
    buttonOpponent[int(a)].show = 'Hit'
    buttonOpponent[int(a)].boatNumber = 4

    banner = StringVar()
    l1 = Label(window,font=("monospace",18),textvariable=banner)
    l1.place(x = 50,y=20)
    l1.pack()
    while True:
        banner.set("Opponents Turn")
        msg = client.recv(SIZE).decode(FORMAT)
        buttons[int(msg)].updateBoard()
        if(stopPlay):
            window.destroy()
            break

        canPlay = True
        banner.set("Your Turn")
        while one.qsize == 0:
            if one.qsize > 0:
                break
        msg = one.get()
        canPlay = False
        client.send(str(msg).encode(FORMAT))
        if stopPlay:
            window.destroy()
            break
        

def cy():
    global firstMessage,canPlay
    img1 = Image.open("bg.jpg")
    test = ImageTk.PhotoImage(img1)
    label1 = Label(image=test,height=500,width=800)
    label1.place(x=0,y=0)
    firstMessage=client.recv(SIZE).decode(FORMAT)
    label1.destroy()
    window.config(height=550,width=800)

    if firstMessage=="Your Turn":
        canPlay = True
        threading.Thread(target=first).start()
    else:
        canPlay = False
        threading.Thread(target=second).start()
    
    return

    




def main():
    
    
    try:
        client.connect(ADDR)
    except:
        print("Server offline")
        return
    global firstMessage
    

    X = threading.Thread(target=cy)
    X.start()
    
    s = 65
    r = 40
    x = s
    y = r
    for i in range(36):
        if i%6==0:
            x = s
            y = y + 30
        btn = button()
        btn.place(x,y,i)
        buttons.append(btn)
        x = x+40
    
    s = x+100
    r = 40

    x = s
    y = r
    for i in range(36):
        if i%6==0:
            x = s
            y = y + 30
        btn = button()
        btn.place(x,y,i)
        buttonOpponent.append(btn)
        x = x+40
    
    pB = threading.Thread(target = placeBoats)
    pB.start()


    Label(window, text="Status of Your Boats :-",font=('monospace',15)).place(x = 65, y = 300)
    Label(window,text = "Status of Opponents Boats :- ",font=('monospace',15)).place(x = 410,y = 300)

    Label(window,text = "Boat 1 -> ",font = ("monospace",13)).place(x = 65, y = 350)
    Label(window,text = "Boat 1 -> ",font = ("monospace",13)).place(x = 410, y = 350)
    displayBoat1["l1"].place(x = 150,y = 350)
    displayOBoat1["l1"].place(x = 495,y = 350)

    Label(window,text = "Boat 2 -> ",font = ("monospace",13)).place(x = 65, y = 390)
    Label(window,text = "Boat 2 -> ",font = ("monospace",13)).place(x = 410, y = 390)

    displayBoat2["ls"][0].place(x = 150,y = 390)
    displayBoat2["ls"][1].place(x = 180,y = 390)

    displayOBoat2["ls"][0].place(x = 495,y = 390)
    displayOBoat2["ls"][1].place(x = 525,y = 390)

    Label(window,text = "Boat 3 -> ",font = ("monospace",13)).place(x = 65, y = 430)
    Label(window,text = "Boat 3 -> ",font = ("monospace",13)).place(x = 410, y = 430)

    displayBoat3["ls"][0].place(x = 150,y = 430)
    displayBoat3["ls"][1].place(x = 180,y = 430)

    displayOBoat3["ls"][0].place(x = 495,y = 430)
    displayOBoat3["ls"][1].place(x = 525,y = 430)

    Label(window,text = "Boat 4 -> ",font = ("monospace",13)).place(x = 65, y = 480)
    Label(window,text = "Boat 4 -> ",font = ("monospace",13)).place(x = 410, y = 480)

    displayBoat4["ls"][0].place(x = 150,y = 470)
    displayBoat4["ls"][1].place(x = 180,y = 470)
    displayBoat4["ls"][2].place(x = 150,y = 495)
    displayBoat4["ls"][3].place(x = 180,y = 495)

    displayOBoat4["ls"][0].place(x = 495,y = 470)
    displayOBoat4["ls"][1].place(x = 525,y = 470)
    displayOBoat4["ls"][2].place(x = 495,y = 495)
    displayOBoat4["ls"][3].place(x = 525,y = 495)

    window.resizable(False,False)
    window.mainloop()

    
if __name__=="__main__":
    main()
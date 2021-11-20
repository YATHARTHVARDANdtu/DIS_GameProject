import os

def main():
    print("Welcome to Game Board >>> \n Developed by :- YATHARTH VARDAN 2K18/CO/405\n Submitted to:- Dr. Anukriti Kaushal\n")
    print("\nWhat do you want to play\n1. Tic Tac Toe\n2. BattleShip")
    choice = input("\nEnter choice :- ")

    if int(choice)==1:
        os.system('client.py')
        return
    if int(choice)==2:
        os.system('client2.py')
        return

if __name__=="__main__":
    main()
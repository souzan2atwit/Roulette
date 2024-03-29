# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 15:21:20 2024

@author: souzan2
"""

import socket
import threading
import random
import time

# Constants

#Both programs will solely be running on my computer, server adress is 9999
SERVER_ADDRESS = ("localhost", 9999) 

# Number of clients needed to make a guess for program to continue
ClIENT_MAX = 6  

# Global variables to track client guesses and connection status

#Tracks how many clients have joined the game
#Does not currently troubleshoot for disconection 
clients = [] 

#Stores the guesses of the clients
#Either odd or even
#Can implement individual number guesses 
#Can implement colors such as black or red
client_guesses = [[]] 

#number of clients currently connected
num_clients=0

lobbySize=3 # number of players alowed in a lobby
playerInfo={} # saves player info such as name and lobby number
lobbyNumber=0
lobbies=[[]]
lobbyMode=[]
lobbyTime=[]
lobbyText=[]
lobbyWin=[]

# Function to handle each player's connection
def handle_player(player_socket, player_address):
    global clients 
    global client_guesses
    global num_clients
    global lobbies
    global lobbyNumber
    global lobbySize
    global playerInfo
    global lobbyText
    global lobbyMode
    global lobbyTime
    global lobbyWin
    inSession=True
    player_name = player_socket.recv(1024).decode("utf-8")
    print(f"{player_name} joined the game.")
    
    
    # Add the player to the list of clients
    #clients.append(player_socket)
    clients.append(player_name)
    playerInfo[player_name]=[]
    playerInfo[player_name].insert(0,player_socket)
    playerInfo[player_name].insert(1,0)
    num_clients=num_clients+1
    pos=0
    inLobby=False
    while(pos<lobbyNumber):
        if(len(lobbies[pos])<lobbySize):
            lobbies[pos].append(player_name)
            playerInfo[player_name].insert(2,pos)
            inLobby=True
            print(lobbies)
            break
        pos+=1
    if inLobby==False:
        lobbies.append([])
        lobbyMode.append(0)
        lobbyTime.append(time.time())
        lobbyWin.append(40)
        lobbies[len(lobbies)-1].append(player_name)
        playerInfo[player_name].insert(2,pos)
        lobbyNumber+=1
        
        
        
    #print (lobbyMode)
    while(lobbyMode[playerInfo[player_name][2]]!=0):
        lobbyWin[playerInfo[player_name][2]]=40
        player_socket.sendall("\nGame is currently underway please wait untill game has ended")
        time.sleep(5)    
    player_socket.sendall(f"\nHello {player_name}, welcome to Roulette. please wait a minute for people to be connected".encode("utf-8"))
    # Receive the player's guess   
    firstrun=True
    while (inSession):  
        #print(lobbyMode[playerInfo[player_name][2]])
        while (lobbyMode[playerInfo[player_name][2]]==0):  
            #print(lobbyTime[playerInfo[player_name][2]]-time.time())
            if time.time()-lobbyTime[playerInfo[player_name][2]]>=20:
                lobbyMode[playerInfo[player_name][2]]=1
        firstrun=True    
        lobbyText="."
        while (lobbyMode[playerInfo[player_name][2]]==1):  
            if firstrun==True:
                player_socket.sendall( "\nyou can check the socreboard by typing (score) or leave by typing (end) if you dont want to do those things please wait for tenseconds for the game to start then type whatevery you want.".encode("utf-8"))
                firstrun=False
            isbroken=False
            #print(time.time()-lobbyTime[playerInfo[player_name][2]])
            player_socket.settimeout(3)
            try:
                    playerText=player_socket.recv(1024).decode("utf-8")
                    if(playerText=="score"):
                        text=" "
                        sort(clients)
                        for i in clients:
                              text=text+"\n"+i  
                        player_socket.sendall(str("the current rankings are\n"+str(text)).encode("utf-8"))
                    elif(playerText=="end"):
                        num_clients-=1;
                        playerInfo.pop(player_name)
                        clients.remove(player_name)
                        isbroken=True
                        break
                    else:
                        lobbyText+=("\n"+playerText)
            except:
                  print(" ")
           # player_socket.sendall(str("\n"+str(lobbyText)).encode("utf-8"))
            #print(time.time()-lobbyTime[playerInfo[player_name][2]])
            if time.time()-lobbyTime[playerInfo[player_name][2]]>=60:
                lobbyMode[playerInfo[player_name][2]]=2    
            if(isbroken):
                break
        

        player_socket.sendall("Game has begun. I am generating a number between 0 and 36...Make your guess here".encode("utf-8"))
        player_socket.settimeout(30)
        try:
            player_guess = player_socket.recv(1024).decode("utf-8")
            player_socket.sendall("Guess recived".encode("utf-8"))
        except:
            player_socket.sendall("Guess timed out".encode("utf-8"))
            player_guess="none"
        client_guesses[playerInfo[player_name][2]].append(player_guess)
        playerInfo[player_name].insert(3,player_guess)
    
    # Inform the clients if waiting for other users to make their guess
        send_waiting_message(player_name)

    # If all clients have made a guess, proceed to announce the result
            
        announce_result(player_guess, player_socket, player_name)
        for lists in client_guesses:
            lists.clear()
        lobbyTime[playerInfo[player_name][2]]=time.time()
        lobbyMode[playerInfo[player_name][2]]=0  


# Function to send a waiting message to clients if waiting for other users to make their guess
def send_waiting_message(pl):
    global clients
    global client_guesses
    global playerInfo
    if len(client_guesses[playerInfo[pl][2]]) < len(lobbies[playerInfo[pl][2]]):
        waiting_message = "Spinning..."
        for playerInfo[pl] in clients:
            playerInfo[pl][0].sendall(waiting_message.encode("utf-8"))
def sort(clientList):
        n = len(clientList)
        
        for i in range(n-1):
            
         
            swapped = False
            for j in range(0, n-i-1):
                if playerInfo[clientList[j]][1] > playerInfo[clientList[j+1]][1]:
                    swapped = True
                    playerInfo[j], playerInfo[j + 1] = playerInfo[j + 1], playerInfo[j]  
            if not swapped:
                return
# Function to announce the result after all clients have made a guess
def announce_result(answer, sckt,pln):
    global clients
    global client_guesses
    global playerInfo
    global lobbyWin
    
    # Generate a random number between 0 and 36
    if(lobbyWin[playerInfo[pln][2]]==40):
        winning_number = random.randint(0, 36)
        print(winning_number)
    else:
        winning_number = lobbyWin[playerInfo[pln][2]]
    print("work")
    # Notify each client if their guess is correct or incorrect, and provide the correct answer
    
    if answer == str(winning_number):
        playerInfo[pln][1]=playerInfo[pln][1]+5
        sckt.sendall("Congratulations! Your guess is correct.".encode("utf-8"))
    elif "black" in answer.lower() and (winning_number==15 
                                                  or winning_number==4 
                                                  or winning_number==2 
                                                  or winning_number==17 
                                                  or winning_number==6 
                                                  or winning_number==13
                                                  or winning_number==11
                                                  or winning_number==8
                                                  or winning_number==10
                                                  or winning_number==24
                                                  or winning_number==33
                                                  or winning_number==20
                                                  or winning_number==31
                                                  or winning_number==22
                                                  or winning_number==29
                                                  or winning_number==28
                                                  or winning_number==35
                                                  or winning_number==26):
            playerInfo[pln][1]=playerInfo[pln][1]+1
            sckt.sendall("Congratulations! Your guess is correct.".encode("utf-8"))
    elif "red" in answer.lower()and (winning_number==32 
                                                  or winning_number==19 
                                                  or winning_number==21 
                                                  or winning_number==25 
                                                  or winning_number==34
                                                  or winning_number==27
                                                  or winning_number==36
                                                  or winning_number==30
                                                  or winning_number==23
                                                  or winning_number==5
                                                  or winning_number==16
                                                  or winning_number==1
                                                  or winning_number==14
                                                  or winning_number==9
                                                  or winning_number==18
                                                  or winning_number==7
                                                  or winning_number==12
                                                  or winning_number==3):
            playerInfo[pln][1]=playerInfo[pln][1]+1
            sckt.sendall("Congratulations! Your guess is correct.".encode("utf-8"))
    elif "odd" in answer.lower() and winning_number%2==1:
            playerInfo[pln][1]=playerInfo[pln][1]+1
            sckt.sendall("Congratulations! Your guess is correct.".encode("utf-8"))
    elif "even" in answer.lower()and winning_number%2==0:
            playerInfo[pln][1]=playerInfo[pln][1]+1
            sckt.sendall("Congratulations! Your guess is correct.".encode("utf-8"))
    else:
           sckt.sendall("Sorry, your guess is incorrect.".encode("utf-8"))
    sckt.sendall(f"The correct answer was: {winning_number}".encode("utf-8"))
        #client_socket.close()

# Main function to start the server
def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(SERVER_ADDRESS)
    server_socket.listen(ClIENT_MAX)  # Allow up to NUM_CLIENTS players to connect
    print("Roulette server is running.")

    while len(clients) < ClIENT_MAX:
        player_socket, player_address = server_socket.accept()
        player_thread = threading.Thread(target=handle_player, args=(player_socket, player_address))
        player_thread.start()

if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 15:21:20 2024

@author: souzan2
"""

import socket
import threading
import random

# Constants

#Both programs will solely be running on my computer, server adress is 9999
SERVER_ADDRESS = ("localhost", 9999) 

# Number of clients needed to make a guess for program to continue
ClIENT_MAX = 2  

# Global variables to track client guesses and connection status

#Tracks how many clients have joined the game
#Does not currently troubleshoot for disconection 
clients = [] 

#Stores the guesses of the clients
#Either odd or even
#Can implement individual number guesses 
#Can implement colors such as black or red
client_guesses = [] 

#number of clients currently connected
num_clients=0

lobbySize=3 # number of players alowed in a lobby
playerInfo={} # saves player info such as name and lobby number

# Function to handle each player's connection
def handle_player(player_socket, player_address):
    global clients 
    global client_guesses
    global num_clients
    inSession=True
    player_name = player_socket.recv(1024).decode("utf-8")
    print(f"{player_name} joined the game.")
    
    
    # Add the player to the list of clients
    clients.append(player_socket)
    num_clients=num_clients+1
    # Receive the player's guess     
    player_socket.sendall(f"Hello {player_name}, welcome to Roulette. I am generating a number between 0 and 36... ".encode("utf-8"))

    while (inSession):
            player_guess = player_socket.recv(1024).decode("utf-8")
            client_guesses.append(player_guess)
    
    
    # Inform the clients if waiting for other users to make their guess
            send_waiting_message()

    # If all clients have made a guess, proceed to announce the result
            while len(client_guesses) != num_clients:
                print("")
            announce_result()
            client_guesses.clear()

# Function to send a waiting message to clients if waiting for other users to make their guess
def send_waiting_message():
    global clients
    global client_guesses
    
    if len(client_guesses) < num_clients:
        waiting_message = "Spinning..."
        for client_socket in clients:
            client_socket.sendall(waiting_message.encode("utf-8"))

# Function to announce the result after all clients have made a guess
def announce_result():
    global clients
    global client_guesses
    
    # Generate a random number between 0 and 36
    winning_number = random.randint(0, 36)
    #32, 19, 21, 25, 34, 27, 36, 30, 23, 5, 16, 1, 14, 9, 18, 7, 12, 3
    # Notify each client if their guess is correct or incorrect, and provide the correct answer
    for client_socket, player_guess in zip(clients, client_guesses):
        if int(player_guess) == winning_number:
            client_socket.sendall("Congratulations! Your guess is correct.".encode("utf-8"))
        elif "black" in player_guess.lower() and (winning_number==15 
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
            client_socket.sendall("Congratulations! Your guess is correct.".encode("utf-8"))
        elif "red" in player_guess.lower()and (winning_number==32 
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
            client_socket.sendall("Congratulations! Your guess is correct.".encode("utf-8"))
        elif "odd" in player_guess.lower() and winning_number%2==1:
            client_socket.sendall("Congratulations! Your guess is correct.".encode("utf-8"))
        elif "even" in player_guess.lower()and winning_number%2==0:
            client_socket.sendall("Congratulations! Your guess is correct.".encode("utf-8"))
        else:
            client_socket.sendall("Sorry, your guess is incorrect.".encode("utf-8"))
        client_socket.sendall(f"The correct answer is: {winning_number}".encode("utf-8"))
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

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
NUM_CLIENTS = 2  

# Global variables to track client guesses and connection status

#Tracks how many clients have joined the game
#Does not currently troubleshoot for disconection 
clients = [] 

#Stores the guesses of the clients
#Either odd or even
#Can implement individual number guesses 
#Can implement colors such as black or red
client_guesses = [] 

# Function to handle each player's connection
def handle_player(player_socket, player_address):
    global clients 
    global client_guesses
    
    player_name = player_socket.recv(1024).decode("utf-8")
    print(f"{player_name} joined the game.")
    player_socket.sendall(f"Hello {player_name}, welcome to Roulette. I am generating a number between 0 and 36... ".encode("utf-8"))
    
    # Add the player to the list of clients
    clients.append(player_socket)
    
    # Receive the player's guess
    player_guess = player_socket.recv(1024).decode("utf-8")
    client_guesses.append(player_guess)
    
    # Inform the clients if waiting for other users to make their guess
    send_waiting_message()

    # If all clients have made a guess, proceed to announce the result
    if len(client_guesses) == NUM_CLIENTS:
        announce_result()

# Function to send a waiting message to clients if waiting for other users to make their guess
def send_waiting_message():
    global clients
    global client_guesses
    
    if len(client_guesses) < NUM_CLIENTS:
        waiting_message = "Spinning..."
        for client_socket in clients:
            client_socket.sendall(waiting_message.encode("utf-8"))

# Function to announce the result after all clients have made a guess
def announce_result():
    global clients
    global client_guesses
    
    # Generate a random number between 0 and 36
    winning_number = random.randint(0, 36)
    
    # Notify each client if their guess is correct or incorrect, and provide the correct answer
    for client_socket, player_guess in zip(clients, client_guesses):
        if int(player_guess) == winning_number:
            client_socket.sendall("Congratulations! Your guess is correct.".encode("utf-8"))
        else:
            client_socket.sendall("Sorry, your guess is incorrect.".encode("utf-8"))
        client_socket.sendall(f"The correct answer is: {winning_number}".encode("utf-8"))
        client_socket.close()

# Main function to start the server
def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(SERVER_ADDRESS)
    server_socket.listen(NUM_CLIENTS)  # Allow up to NUM_CLIENTS players to connect
    print("Roulette server is running.")

    while len(clients) < NUM_CLIENTS:
        player_socket, player_address = server_socket.accept()
        player_thread = threading.Thread(target=handle_player, args=(player_socket, player_address))
        player_thread.start()

if __name__ == "__main__":
    main()

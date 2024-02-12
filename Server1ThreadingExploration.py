# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 15:21:20 2024

@author: souzan2
"""

import socket
import threading
import random

# Constants
SERVER_ADDRESS = ("localhost", 9999)
NUM_CLIENTS = 2  # Number of clients needed to make a guess

# Global variables to track client guesses and connection status
clients = []
client_guesses = []

# Function to handle each player's connection
def handle_player(player_socket, player_address):
    global clients
    global client_guesses
    
    player_name = player_socket.recv(1024).decode("utf-8")
    print(f"{player_name} joined the game.")
    player_socket.sendall(f"Hello {player_name}, welcome to Roulette. Guess whether the number is even or odd (0 for even, 1 for odd): ".encode("utf-8"))
    
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
        waiting_message = "Waiting for other users to make their guess..."
        for client_socket in clients:
            client_socket.sendall(waiting_message.encode("utf-8"))

# Function to announce the result after all clients have made a guess
def announce_result():
    global clients
    global client_guesses
    
    # Generate a random number (0 for even, 1 for odd)
    winning_number = random.randint(0, 1)
    
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

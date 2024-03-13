# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 15:25:48 2024

@author: souzan2
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 15:57:54 2024

@author: souzan2
"""

import socket

# Function for client to join the game and make a guess
def main():
    inSession=True
    server_address = ("localhost", 9999)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(server_address)
    
    # Send the player's name to the server
    player_name = input("Enter your name: ")
    client_socket.sendall(player_name.encode("utf-8"))
    
    # Receive the welcome message and guessing prompt from the server
    while(inSession):
        message = client_socket.recv(1024).decode("utf-8")
        print(message)
    
        # Make a guess (0 for even, 1 for odd)
        #print("work")
        player_guess = input("Guess what the number will be: ")
        client_socket.sendall(player_guess.encode("utf-8"))
    
        # Receive the result of the guess and the correct answer
        
        result = client_socket.recv(1024).decode("utf-8")
        print(result)
        
            
            
    
    client_socket.close()

if __name__ == "__main__":
    main()

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
import threading
player_guess="nothing"
client_socket=""
inSession=True

# Function for client to join the game and make a guess
def main():
    global player_guess
    global client_socket
    #inSession=True
    server_address = ("localhost", 9999)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(server_address)
    
    # Send the player's name to the server
    player_name = input("Enter your name: ")
    client_socket.sendall(player_name.encode("utf-8"))
    
    # Receive the welcome message and guessing prompt from the server
    t1= threading.Thread(target=send)
    t2= threading.Thread(target=recv)

    t1.start()
    t2.start()
    
    t1.join()
    t2.join()
        
        
            
            
    
    client_socket.close()
def send():
    global client_socket
    global inSession
    while inSession:
        playerText = input(":")
        client_socket.sendall(playerText.encode("utf-8"))
        if playerText=="end":
            inSession=False
def recv():
    global client_socket
    global inSession
    while inSession:
        print(client_socket.recv(1024).decode("utf-8"))

if __name__ == "__main__":
    main()

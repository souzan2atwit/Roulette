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
from threading import Timer
import time
player_guess="nothing"


# Function for client to join the game and make a guess
def main():
    global player_guess
    
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
        
        seconds= time.time()
        while(time.time()-seconds<10):
            playerText = input(":")
            client_socket.sendall(playerText.encode("utf-8"))
            if playerText=="end":
                break
            print(client_socket.recv(1024).decode("utf-8"))
            
        print("5")
        timerG = Timer(5, print, ['sorry you are out of time please input an answer although it no longer matters'])
        timerG.start()
        player_guess = input("\nguess a number: ")
        timerG.cancel()
        
       
       
        
       
        
       
        client_socket.sendall(player_guess.encode("utf-8"))
    
        # Receive the result of the guess and the correct answer
        
        result = client_socket.recv(1024).decode("utf-8")
        print(result)
        
            
            
    
    client_socket.close()

if __name__ == "__main__":
    main()

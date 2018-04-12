#*********************************
# Podchat Registration(client).py
# Author: Kayin Moore
#*********************************

# imports socket and time libaries
from socket import *
import time

# create a socket and connect to the server
serverName = "127.0.0.1"
serverPort = 12120
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

print("Connection successful")
print("\n")

print("Welcome to the registration program-podchat!!")
print("\n")



while 1:
    print("Sending hello to server")
    clientSocket.send("hello".encode())
    while 1:
        print("Waiting for response from server")
        SERVER_INFO = clientSocket.recv(1024).decode('ascii')
        if SERVER_INFO.upper() == "WELCOME":
            print("Enter if statement")
            print(SERVER_INFO)
            clientSocket.close()
        else:
            print("Entering else statement")
            SEND_BACK = input(SERVER_INFO)
            clientSocket.send(SEND_BACK.encode())
    clientSocket.close()
    break

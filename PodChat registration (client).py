#*********************************
# Podchat Registration(client).py
# Author: Kayin Moore
#*********************************

# imports socket and time libaries
from socket import *
import time

# create a socket and connect to the server
serverName = "172.22.203.225"
serverPort = 12116
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

print("Connection successful")
print("\n")

print("Welcome to the registration program!!")
print("\n")

resultMessage = ""


while 1:

    clientSocket.send("hello".encode())

    while 1:


        choice = input(clientSocket.recv(1024).decode('ascii'))
        clientSocket.send(choice.encode())

        #eMail = input(clientSocket.recv(1024).decode('ascii'))
       # clientSocket.send(eMail.encode())
       # userName = input(clientSocket.recv(1024).decode('ascii'))
       # clientSocket.send(userName.encode())
      #  passw= input(clientSocket.recv(1024).decode('ascii'))
      #  clientSocket.send(passw.encode())

      #  print(clientSocket.recv(1024).decode())
      #  clientSocket.send(choice.encode())

       # break
    clientSocket.close()
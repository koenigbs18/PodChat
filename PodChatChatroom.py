#********************************************
# RegisterServer.py
# Server program for registering user profiles
# Created by:   Brett Koenig
# Created on:   2/20/2018
#*********************************************
# https://stackoverflow.com/questions/33434007/python-socket-send-receive-messages-at-the-same-time
from socket import *
from datetime import datetime
from _thread import *

serverPort = 12009
serverSocket = socket(AF_INET,SOCK_STREAM)
#serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind(('172.22.8.147',serverPort))
serverSocket.listen(10)
threadCount = 0
chatrooms = []
currentMessage = ""
sendingMessage = False

class User:
    def __init__(self, chatroom):
        self.chatroom = chatroom

def handle_client(connectionSocket, addr):
    global threadCount
    global chatrooms
    running = True
    while running:
        message = connectionSocket.recv(1024).decode('ascii') # wait for a message
        if(message.upper() == "HELLO WORLD"):
            connectionSocket.send(("connection from " + addr[0]).encode())
        if(message.upper() == "QUIT"):
            connectionSocket.send("goodbye".encode())
            running = False
        if(message.upper() == "CHATROOM"):
            # connect user to chatroom
            chatroom(connectionSocket)
    
    print("Thread Addr " + addr[0] + " has stopped running")
    threadCount = threadCount - 1
    connectionSocket.close()

def chatroom(connectionSocket):
    connectionSocket.send("Connected to chatroom, please send a message or type 'QUIT CHATROOM' to quit.".encode())
    global currentMessage
    global sendingMessage
    global chatrooms
    index = len(chatrooms) # save the index of this chatroom
    chatrooms.append(True)
    start_new_thread(sendChatroomMessage, (connectionSocket, index))
    while chatrooms[index] == True:
        message = connectionSocket.recv(1024).decode('ascii') # wait for a message
        if(message.upper() == "QUIT CHATROOM"):
            print("Quitting chatroom")
            chatrooms[index] = False; # stop chatroom
            break
        if(len(message) > 0):
            sendingMessage = True
            currentMessage = message
            
            
    connectionSocket.send("exiting chatroom".encode())

def sendChatroomMessage(connectionSocket, index):
    global sendingMessage
    global chatrooms
    while(chatrooms[index] == True):
        if(sendingMessage):
            print("attempting to send message to client")
            connectionSocket.send(currentMessage.encode())
            sendingMessage = False
    
    
def main():
    global threadCount
    print("Server is now receiving messages...")
    while 1:
        connectionSocket, addr = serverSocket.accept()
        print("connection from " + addr[0])
        try:
            start_new_thread(handle_client, (connectionSocket, addr))
            threadCount = threadCount + 1
        except:
            print("Unable to start new thread.")
        print("Running threads: " + str(threadCount))
    serverSocket.close()

if __name__ == "__main__":
    main()


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
import time
from enum import Enum

serverPort = 12009
serverSocket = socket(AF_INET,SOCK_STREAM)
#serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind(('172.22.8.147',serverPort))
serverSocket.listen(10)
threadCount = 0
users = []
currentMessage = ""
sendingMessage = False

#unused
class User:
    def __init__(self, chatroom):
        self.chatroom = chatroom
#enums
class LOGIN_STATUS(Enum):
    SUCCESS = 1
    FAILURE_INCORRECT = 2 # Username/password incorrect
    READ_ERROR

def handle_client(connectionSocket, addr):
    global threadCount
    loggedIn = False
    running = True
    while running:
        # send a message containing all possible user options
        connectionSocket.send("Input your choice:\n\tRegister\n\tLogin\n\tQuit\n".encode())
        # receive message
        try:
            message = connectionSocket.recv(1024).decode('ascii') # wait for a message
        except ConnectionResetError:
            print("User: " + str(threadCount-1) + " did not respond in time.")
            break
        if(loggedIn == False):
            # login/register options, initial login
            if(message.upper() == "LOGIN"):
                # connect user to chatroom
                loggedIn = login(connectionSocket)
                print("login protocol")
        else:
            # options after login
            if(message.upper() == "CHATROOM"):
                # connect user to chatroom
                chatroom(connectionSocket)
        # all user options
        if(message.upper() == "HELLO WORLD"):
            connectionSocket.send(("connection from " + addr[0]).encode())
        if(message.upper() == "QUIT"):
            connectionSocket.send("goodbye".encode())
            running = False
        
    
    print("Thread Addr " + addr[0] + " has stopped running")
    threadCount = threadCount - 1
    connectionSocket.close()

def registration(connectionSocket):
       # Registration code goes here
	
def login(connectionSocket):
    connectionSocket.send("Enter username: ".encode())
    USERNAME = connectionSocket.recv(1024).decode('ascii')
    connectionSocket.send("Enter password: ".encode())
    PASSWORD = connectionSocket.recv(1024).decode('ascii')
    #Open the registeredusers.txt file to check the username & password
    try:
         print("Reading from registeredusers.txt")
         RESPONSE = ""
         REASON = ""
         LOGIN_STATUS = ""
         with open('registeredusers.csv', 'r') as USER_FILE:
            READER = csv.reader(USER_FILE)
            for row in READER:
                print("Printing current row: "+str(row))
                if USERNAME == str(row[1]) and PASSWORD == str(row[2]):
                    print("Email: "+str(row[0]))
                    print("Username: "+str(row[1]))
                    print("Password: "+str(row[2]))
                    print("Login successful")
                    LOGIN_STATUS = "Success"
                else:
    except FileNotFoundError:
        print("File Not Found")
        open("UserProfile.txt", 'w') # create the file+
    if(status == LOGIN_STATUS.SUCCESS):
        return True
    else:
        return False
        
def(
#chatroom creates a new user chatroom index, then starts receiving and sending messages in a thread
def chatroom(connectionSocket):
    connectionSocket.send("Connected to chatroom, please send a message or type 'QUIT CHATROOM' to quit.".encode())
    global currentMessage
    global sendingMessage
    global users
    index = len(users) # save the index of this user
    users.append(True)
    start_new_thread(sendChatroomMessage, (connectionSocket, index))
    start_new_thread(receiveChatroomMessage, (connectionSocket, index))
    while users[index] == True:
        time.sleep(.05)
    print("\nuser " + str(index) + " has exited the chatroom.")
    
def receiveChatroomMessage(connectionSocket, index):
    global currentMessage
    global sendingMessage
    global users
    while users[index] == True:
        try:
            message = connectionSocket.recv(1024).decode('ascii') # wait for a message
        except ConnectionResetError:
            print("\nUser: " + str(index) + " did not respond in time.")
            users[index] == True
            break
        if(message.upper() == "QUIT CHATROOM"):
            print("\nQuitting chatroom")
            users[index] = False; # stop chatroom
            break
        if(len(message) > 0):
            sendingMessage = True
            currentMessage = message
    try: 
        connectionSocket.send("exiting chatroom".encode())
    except ConnectionResetError:
        print("Lost connection to user " + str(index))
        users[index] == True
    
def sendChatroomMessage(connectionSocket, index):
    global currentMessage
    global sendingMessage
    global users
    while(users[index] == True):
        if(sendingMessage):
            print("\nattempting to send message to client")
            try:
                connectionSocket.send(currentMessage.encode())
            except ConnectionResetError:
                print("Lost connection to user " + str(index))
                users[index] == True
                break
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


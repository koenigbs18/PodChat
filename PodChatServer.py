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
import csv

serverPort = 12009
serverSocket = socket(AF_INET,SOCK_STREAM)
#serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind(('192.168.1.107',serverPort))
serverSocket.listen(10)
threadCount = 0
users = []
offlineMessages = ["", "", "", "", "", "", "", "", "", ""] # save last 10 messages
currentMessage = ""
sendingMessage = False

#unused
class User:
    def __init__(self, chatroom):
        self.chatroom = chatroom
#enums
class ENUMS(Enum):
    NULL = 0
    SUCCESS = 1
    FAILURE_INCORRECT = 2 # Username/password incorrect (login)
    FAILURE_GENERIC = 3
    READ_ERROR = 4
    CONNECTION_ERROR = 5
    REGISTRATION_REQUIRED = 6
    # Registration errors, if you edit 7-13, edit for loop in registration code
    FAILURE_REG = 7 # general registration error

def handle_client(connectionSocket, addr):
    global threadCount
    loggedIn = False
    running = True
    USERNAME = ""
    while running:
        # send a message containing all possible user options
        # connectionSocket.send("Input your choice:\n\tRegister\n\tLogin\n\tQuit\n".encode())
        # receive message
        try:
            message = connectionSocket.recv(1024).decode('ascii') # wait for a message
        except (ConnectionResetError, TimeoutError) as err:
            print(err)
            print(err.args)
            print("User: " + str(threadCount-1) + " did not respond in time.")
            break
        print("Server Message: " + message)
        if(loggedIn == False):
            print("logged out options")
            # login/register options, initial login
            if(message.upper() == "LOGIN"):
                print("login protocol")
                # connect user to chatroom
                returnMessage = login(connectionSocket).split(',')
                LOGIN_STATUS = returnMessage[0]
                USERNAME = returnMessage[1]
                if(LOGIN_STATUS == str(ENUMS.SUCCESS)):
                    print(USERNAME + " has logged in.")
                    loggedIn = True

                elif(LOGIN_STATUS == ENUMS.CONNECTION_ERROR):
                    break
                continue
            if(message.upper() == "REGISTER"):
                print("Registration protocol")
                if(registration(connectionSocket) == ENUMS.CONNECTION_ERROR):
                    break
                continue
        if(loggedIn == True):
            print("logged in options")
            # options after login
            if(message.upper() == "CHATROOM"):
                # connect user to chatroom
                chatroom(connectionSocket)
                continue
            if(message.upper() == "LOGOUT"):
                print(USERNAME + " has logged out.")
                loggedIn = False
                continue

        # all user options
        if(message.upper() == "HELLO WORLD"):
            connectionSocket.send(("connection from " + addr[0]).encode())
            continue
        if(message.upper() == "QUIT"):
            connectionSocket.send("goodbye".encode())
            running = False
            continue
        print("INVALID RESPONSE: " + message)
        connectionSocket.send(("INVALID RESPONSE" + message).encode())

    print("Thread Addr " + addr[0] + " has stopped running")
    threadCount = threadCount - 1
    connectionSocket.close()

def registration(connectionSocket):
    print("Entering registration code")
    STATUS = ENUMS.NULL
    REASON = ""
    REASONPASS = ""
    connectionSocket.send("REGISTRATION".encode())
    #REGISTRATIONINFO: EMAIL[0],USERNAME[1],PASSWORD[2]
    try:
        REGINFO = connectionSocket.recv(1024).decode('ascii').split(",")
    except ValueError:
        return ENUMS.CONNECTION_ERROR
    #Open the registeredusers.txt file to check the userID
    try:
        print("Reading from registeredusers.csv")
        with open('registeredusers.csv', 'r') as USER_FILE:
            READER = csv.reader(USER_FILE)
            for row in READER:
                print("Printing current row: "+str(row))
                if REGINFO[0] not in row and REGINFO[1] not in row:
                    if len(REGINFO[2]) >= 6:
                        STATUS = ENUMS.REGISTRATION_REQUIRED
                    else:
                        print("Password length is shorter than 6")
                        REASONPASS = "Password length is shorter than 6\n"
                        STATUS = ENUMS.FAILURE_REG
                else:
                    if REGINFO[0] in row:
                        print("The email you entered is already in use")
                        REASON += "The email you entered is already in use\n"
                        STATUS = ENUMS.FAILURE_REG
                    if REGINFO[1] in row:
                        print("The username you entered is already in use")
                        REASON += "The username  you entered is already in use\n"
                        STATUS = ENUMS.FAILURE_REG
                    if len(REGINFO[2]) < 6:
                        print("Password length is shorter than 6")
                        REASONPASS = "Password length is shorter than 6\n"
                        STATUS = ENUMS.FAILURE_REG
                    break
                print("Done with row")
            print("Done reading from registeredusers.csv")
    except FileNotFoundError:
        print("File Not Found")
        open("registeredusers.csv", 'w') #create file
        STATUS = ENUMS.READ_ERROR
    if STATUS == ENUMS.REGISTRATION_REQUIRED:
        print("Entering needs to register code")
        REGISTRATION_RECORD = REGINFO[0]+","+REGINFO[1]+","+REGINFO[2]+"\n"
        with open('registeredusers.csv', 'a') as OUTPUT_FILE:
            OUTPUT_FILE.write(REGISTRATION_RECORD)
            OUTPUT_FILE.close()
            STATUS = ENUMS.SUCCESS
    # Return the enum status
    if STATUS == ENUMS.SUCCESS:
        print("SUCCESS: REGISTRATION SUCCESSFUL")
        connectionSocket.send("SUCCESS: REGISTRATION SUCCESSFUL".encode())
    elif STATUS == ENUMS.READ_ERROR:
        print("FAILURE: SERVER FILE ERROR")
        connectionSocket.send("FAILURE: SERVER FILE ERROR".encode())
    elif STATUS == ENUMS.FAILURE_REG:
        print("FAILURE: REGISTRATION ERROR")
        SEND = "FAILURE: REGISTRATION ERROR\n"
        SEND += REASON
        SEND += REASONPASS
        connectionSocket.send(SEND.encode())
    elif STATUS == ENUMS.NULL:
        print("FAILURE: NULL SERVER RESPONSE")
        connectionSocket.send("FAILURE: NULL SERVER RESPONSE".encode())
    return STATUS

def login(connectionSocket):
    print("login protocol")
    # default status
    STATUS = ENUMS.NULL
    # request login info from client
    connectionSocket.send("USERNAME AND PASSWORD".encode())
    #LOGININFO: USERNAME[0],PASSWORD[1]
    try:
        LOGININFO = connectionSocket.recv(1024).decode('ascii')
    except (ConnectionResetError, TimeoutError) as err:
        print(err)
        print(err.args)
        return ENUMS.CONNECTION_ERROR
    try:
        LOGININFO = LOGININFO.split(",")
    except ValueError as err:
        print(err)
        print(err.args)
        connectionSocket.send("FAILURE: INCORRECT FORMAT".encode())
        return ENUMS.FAILURE_GENERIC
    #Open the registeredusers.txt file to check the username & password
    if(len(LOGININFO) != 2):
        print("LOGIN INFO INVALID")
        connectionSocket.send("FAILURE: INVALID LOGIN PARAMETERS".encode())
        return (str(STATUS) + "," + "")
    try:
         print("Reading from registeredusers.txt")
         with open('registeredusers.csv', 'r') as USER_FILE:
             #login info incorrect by default, set to success when we find a match
            STATUS = ENUMS.FAILURE_INCORRECT
            READER = csv.reader(USER_FILE)
            for row in READER:
                if(len(row) < 3):
                    continue
                if LOGININFO[0] == str(row[1]) and LOGININFO[1] == str(row[2]):
                    STATUS = ENUMS.SUCCESS
                    break
    except FileNotFoundError:
        open("UserProfile.txt", 'w') # create the file+
        STATUS = ENUMS.READ_ERROR

    # Return the enum status
    if(STATUS == ENUMS.SUCCESS):
        print("SUCCESS: LOGIN SUCCESSFUL")
        # return ENUM.STATUS,USERNAME
        connectionSocket.send("SUCCESS: LOGIN SUCCESSFUL".encode())
        return (str(STATUS) + "," + LOGININFO[0])
    elif(STATUS == ENUMS.READ_ERROR):
        print("FAILURE: SERVER FILE ERROR")
        connectionSocket.send("FAILURE: SERVER FILE ERROR".encode())
    elif(STATUS == ENUMS.FAILURE_INCORRECT):
        print("FAILURE: INCORRECT LOGIN INFO")
        connectionSocket.send("FAILURE: INCORRECT LOGIN INFO".encode())
    elif(STATUS == ENUMS.NULL):
        print("FAILURE: NULL SERVER RESPONSE")
        connectionSocket.send("FAILURE: NULL SERVER RESPONSE".encode())

    return (str(STATUS) + "," + "")
        
#chatroom creates a new user chatroom index, then starts receiving and sending messages in a thread
def chatroom(connectionSocket):
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
        except (ConnectionResetError, TimeoutError) as err:
            print(err)
            print(err.args)
            print("\nUser: " + str(index) + " did not respond in time.")
            users[index] == False
            break
        if(message.upper() == "QTCHATROOM"):
            print("\nQuitting chatroom")
            users[index] = False; # stop chatroom thread
            break
        if(len(message) > 0):
            sendingMessage = True
            currentMessage = message
    try: 
        connectionSocket.send("exiting chatroom".encode())
    except (ConnectionResetError, TimeoutError) as err:
        print(err)
        print(err.args)
        print("Lost connection to user " + str(index))
        users[index] == False
    print("\nexiting receiveChatroom thread")

def sendChatroomMessage(connectionSocket, index):
    global currentMessage
    global sendingMessage
    global users
    while(users[index] == True):
        if(sendingMessage):
            print("\nattempting to send message to client")
            try:
                connectionSocket.send(currentMessage.encode())
            except (ConnectionResetError, TimeoutError) as err:
                print(err)
                print(err.args)
                print("Lost connection to user " + str(index))
                users[index] == False
                break
            sendingMessage = False
    print("\nexiting sendChatroom thread")
    
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


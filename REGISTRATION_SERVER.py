#REGISTRATION_SERVER.py
#Server program for registering an account
#Created By: Paul Knisely
#Created on: 2/26/2018

from socket import *
from datetime import datetime

#Create a socket bound at SERVER_PORT
SERVER_PORT = 12116
SERVER_SOCKET = socket(AF_INET, SOCK_STREAM)
SERVER_SOCKET.bind(('172.22.203.225', SERVER_PORT))
SERVER_SOCKET.listen(10)
print("Registration server is ready to receive")
ACCESS_TIME = datetime.now()
print("Access time is ", ACCESS_TIME)

while 1:
    CONNECTION_SOCKET, ADDR = SERVER_SOCKET.accept()
    print("from", ADDR)
    REGISTRATION_STATUS = "Failure"
    LOGIN_STATUS = ""
    while 1:
        RESPONSE = CONNECTION_SOCKET.recv(1024).decode('ascii')
        print("Response message: ", RESPONSE)
        if RESPONSE.upper() == "HELLO":
            CONNECTION_SOCKET.send("Input your choice:\n\tRegister\n\tLogin\n\tQuit\n".encode())
            RESPONSE = CONNECTION_SOCKET.recv(1024).decode('ascii')
        if RESPONSE.upper() == "LOGIN":
            CONNECTION_SOCKET.send("Enter username: ".encode())
            USERNAME = CONNECTION_SOCKET.recv(1024).decode('ascii')
            CONNECTION_SOCKET.send("Enter password: ".encode())
            PASSWORD = CONNECTION_SOCKET.recv(1024).decode('ascii')
            #Open the registeredusers.txt file to check the userID
            try:
                print("Reading from registeredusers.txt")
                REASON = ""
                for line in open("registeredusers.txt", "r"):
                    if USERNAME not in line and PASSWORD not in line:
                        LOGIN_STATUS = "Success"
                    else:
                        print("The username and password you entered are incorrect")
                        REASON += "The username and password you entered are incorrect\n"
                        LOGIN_STATUS = "Failure"
                        break
                    print("Done reading from registeredusers.txt")
            except FileNotFoundError:
                print("File Not Found")
        #Start Registration code
        if RESPONSE.upper() == "REGISTER":
            CONNECTION_SOCKET.send("Enter email: ".encode())
            EMAIL = CONNECTION_SOCKET.recv(1024).decode('ascii')
            CONNECTION_SOCKET.send("Enter username: ".encode())
            USERNAME = CONNECTION_SOCKET.recv(1024).decode('ascii')
            CONNECTION_SOCKET.send("Enter password: ".encode())
            PASSWORD = CONNECTION_SOCKET.recv(1024).decode('ascii')
            #Open the registeredusers.txt file to check the userID
            try:
                print("Reading from registeredusers.txt")
                REASON = ""
                for line in open("registeredusers.txt", "r"):
                    if USERNAME not in line:
                        if USERNAME not in line and EMAIL not in line:
                            if len(PASSWORD) >= 6:
                                REGISTRATION_STATUS = "NEEDS_TO_REGISTER"
                            else:
                                print("Password length is shorter than 6")
                                REASON += "Password length is shorter than 6\n"
                                REGISTRATION_STATUS = "Failure"
                                break
                        else:
                            print("The email you entered is already in use")
                            REASON += "The email you entered is already in use\n"
                            REGISTRATION_STATUS = "Failure"
                            break
                    else:
                        print("The username you entered is already in use")
                        REASON += "The username  you entered is already in use\n"
                        REGISTRATION_STATUS = "Failure"
                        break
                    print("Done reading from registeredusers.txt")
            except FileNotFoundError:
                print("File Not Found")
            if REGISTRATION_STATUS.upper() == "NEEDS_TO_REGISTER":
                ACCESS_TIME = datetime.now()
                STRING_ACCESS_TIME = ACCESS_TIME.strftime('%m/%d/%Y %H:%M:%S')
                print("Access time is ", STRING_ACCESS_TIME)
                REGISTRATION_RECORD = EMAIL+"\t"+USERNAME+"\t"+PASSWORD+"\t\n"
                #REGISTRATION_RECORD += USER_PASSWORD+"\t"+ADDR[0]+"\t"+STRING_ACCESS_TIME+"\n"
                OUTPUT_FILE = open("registeredusers.txt", "a")
                OUTPUT_FILE.write(REGISTRATION_RECORD)
                OUTPUT_FILE.close()
                SEND = "Registration Status: SUCCESS\n"
                SEND += "Input your choice:\n\tRegister\n\tLogin\n\tQuit\n"
                CONNECTION_SOCKET.send(SEND.encode())
            if REGISTRATION_STATUS.upper() == "FAILURE":
                SEND = "Registration Status: FAILED\n"
                SEND += REASON
                SEND += "Input your choice:\n\tRegister\n\tLogin\n\tQuit\n"
                CONNECTION_SOCKET.send(SEND.encode())
            if LOGIN_STATUS.upper() == "SUCCESS":
                CONNECTION_SOCKET.send("Welcome to PodChat!".encode())
    CONNECTION_SOCKET.close()

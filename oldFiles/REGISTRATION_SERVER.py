"""
#REGISTRATION_SERVER.py
#Server program for registering an account
#Created By: Paul Knisely
#Created on: 2/26/2018
"""
from socket import *
from datetime import datetime
import csv

#Create a socket bound at SERVER_PORT
SERVER_PORT = 12120
SERVER_SOCKET = socket(AF_INET, SOCK_STREAM)
SERVER_SOCKET.bind(('127.0.0.1', SERVER_PORT))
SERVER_SOCKET.listen(10)
print("Registration server is ready to receive")
ACCESS_TIME = datetime.now()
print("Access time is ", ACCESS_TIME)

while 1:
    CONNECTION_SOCKET, ADDR = SERVER_SOCKET.accept()
    print("from", ADDR)
    LOGIN_STATUS = ""
    while 1:
        RESPONSE = CONNECTION_SOCKET.recv(1024).decode('ascii')
        print("Response message: ", RESPONSE)
        if RESPONSE.upper() == "HELLO":
            print("Entering hello code")
            RESPONSE = ""
            CONNECTION_SOCKET.send("Input your choice:\n\tRegister\n\tLogin\n\tQuit\n".encode())
            RESPONSE = CONNECTION_SOCKET.recv(1024).decode('ascii')
        if RESPONSE.upper() == "LOGIN":
            print("Entering login code")
            RESPONSE = ""
            CONNECTION_SOCKET.send("Enter username: ".encode())
            USERNAME = CONNECTION_SOCKET.recv(1024).decode('ascii')
            CONNECTION_SOCKET.send("Enter password: ".encode())
            PASSWORD = CONNECTION_SOCKET.recv(1024).decode('ascii')
            #Open the registeredusers.txt file to check the userID
            try:
                print("Reading from registeredusers.txt")
                RESPONSE = ""
                REASON = ""
                LOGIN_STATUS = ""
                """
                old logic for reading username and password. will cut when everything is 100% working
                for line in open("registeredusers.txt", "r"):
                    if len(line) > 0:
                        print("Line contents: "+line)
                        splitLine = line.split("\t")
                        print("\n"+splitLine[1])
                        print("\n"+splitLine[2])
                        #if USERNAME == line.split("\t")[0].strip() and PASSWORD == line.split("\t")[1].strip():
                        #if USERNAME == split1 and PASSWORD == split2:
                        if USERNAME == splitLine[1] and PASSWORD == splitLine[2]:
                            print("Correct username and password")
                            LOGIN_STATUS = "Success"
                            break
                        else:
                            print("The username and password you entered are incorrect")
                            REASON = "The username and password you entered are incorrect\n"
                            LOGIN_STATUS = "Failure"
                            break
                    else:
                        print("Line is not greater than 0")
                    print("Done reading from registeredusers.txt")
                """
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
                            print("The username and password you entered are incorrect")
                            REASON = "The username and password you entered are incorrect\n"
                            LOGIN_STATUS = "Failure"
                        if LOGIN_STATUS.upper() == "SUCCESS":
                            print("breaking from login status success if statement")
                        print("Done with row")
                print("Done reading from registeredusers.csv")
            except FileNotFoundError:
                print("File Not Found")
        #Start Registration code
        if RESPONSE.upper() == "REGISTER":
            print("Entering register code")
            RESPONSE = ""
            CONNECTION_SOCKET.send("Enter email: ".encode())
            EMAIL = CONNECTION_SOCKET.recv(1024).decode('ascii')
            CONNECTION_SOCKET.send("Enter username: ".encode())
            USERNAME = CONNECTION_SOCKET.recv(1024).decode('ascii')
            CONNECTION_SOCKET.send("Enter password: ".encode())
            PASSWORD = CONNECTION_SOCKET.recv(1024).decode('ascii')
            #Open the registeredusers.txt file to check the userID
            try:
                print("Reading from registeredusers.csv")
                REASON = ""
                NEED_TO_REGISTER = False
                REGISTRATION_ERROR = False
                for line in open("registeredusers.csv", "r"):
                    if USERNAME not in line:
                        if USERNAME not in line and EMAIL not in line:
                            if len(PASSWORD) >= 6:
                                NEED_TO_REGISTER = True
                            else:
                                print("Password length is shorter than 6")
                                REASON += "Password length is shorter than 6\n"
                                REGISTRATION_ERROR = True
                                break
                        else:
                            print("The email you entered is already in use")
                            REASON += "The email you entered is already in use\n"
                            REGISTRATION_ERROR = True
                            break
                    else:
                        print("The username you entered is already in use")
                        REASON += "The username  you entered is already in use\n"
                        REGISTRATION_ERROR = True
                        break
                    print("Done reading from registeredusers.txt")
            except FileNotFoundError:
                print("File Not Found")
            if NEED_TO_REGISTER:
                print("Entering needs to register code")
                ACCESS_TIME = datetime.now()
                STRING_ACCESS_TIME = ACCESS_TIME.strftime('%m/%d/%Y %H:%M:%S')
                print("Access time is ", STRING_ACCESS_TIME)
                REGISTRATION_RECORD = EMAIL+","+USERNAME+","+PASSWORD+"\n"
                #REGISTRATION_RECORD += USER_PASSWORD+"\t"+ADDR[0]+"\t"+STRING_ACCESS_TIME+"\n"
                OUTPUT_FILE = open("registeredusers.csv", "a")
                OUTPUT_FILE.write(REGISTRATION_RECORD)
                OUTPUT_FILE.close()
                SEND = "Registration Status: SUCCESS\n"
                SEND += "Input your choice:\n\tRegister\n\tLogin\n\tQuit\n"
                CONNECTION_SOCKET.send(SEND.encode())
            if REGISTRATION_ERROR:
                print("Entering registration failure code")
                SEND = "Registration Status: FAILED\n"
                SEND += REASON
                SEND += "Input your choice:\n\tRegister\n\tLogin\n\tQuit\n"
                CONNECTION_SOCKET.send(SEND.encode())
        if LOGIN_STATUS.upper() == "SUCCESS":
            print("Entering login status success code")
            print("Sending Welcome message to client")
            CONNECTION_SOCKET.send("Welcome".encode())
        if LOGIN_STATUS.upper() == "FAILURE":
            print("Entering login status failure code")
            SEND = "Login Status: FAILED\n"
            SEND += REASON
            SEND += "Input your choice:\n\tRegister\n\tLogin\n\tQuit\n"
            CONNECTION_SOCKET.send(SEND.encode())
    CONNECTION_SOCKET.close()

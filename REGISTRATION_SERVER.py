#REGISTRATION_SERVER.py
#Server program for registering an account
#Created By: Paul Knisely
#Created on: 2/26/2018

from socket import *
from datetime import datetime

#Create a socket bound at SERVER_PORT
SERVER_PORT = 12015
SERVER_SOCKET = socket(AF_INET, SOCK_STREAM)
SERVER_SOCKET.bind(('', SERVER_PORT))
SERVER_SOCKET.listen(10)
print("Registration server is ready to receive")
ACCESS_TIME = datetime.now()
print("Access time is ", ACCESS_TIME)

while 1:
    CONNECTION_SOCKET, ADDR = SERVER_SOCKET.accept()
    print("from", ADDR)
    REGISTRATION_STATUS = "Failure"
    while 1:
        REQUEST = CONNECTION_SOCKET.recv(1024).decode('ascii')
        print("Request message: ", REQUEST)
        if REQUEST.upper() == "QUIT":
            break
        METHOD_NAME = REQUEST.split("\t")[0].strip()
        print("From ", ADDR, METHOD_NAME)
        if METHOD_NAME.upper() == "REGISTER":
            #Checking if userID has been registered
            print("Checking if user has been registered...")
            USER_ID = REQUEST.split("\t")[1]
            USER_NAME = REQUEST.split("\t")[2]
            USER_EMAIL = REQUEST.split("\t")[3]
            USER_PASSWORD = REQUEST.split("\t")[4]
            print(METHOD_NAME, USER_ID)
            #Open the UserProfile.txt file to check the userID
            try:
                print("Reading from UserProfile.txt")
                for line in open("UserProfile.txt", "r"):
                    REASON = ""
                    if USER_ID not in line:
                        if USER_NAME not in line and USER_EMAIL not in line:
                            if len(USER_PASSWORD) >= 6:
                                REGISTRATION_STATUS = "Success"
                            else:
                                print("Password length is shorter than 6")
                                REASON += "Password length is shorter than 6\t"
                                REGISTRATION_STATUS = "Failure"
                        else:
                            print("There is an existing user id for this user")
                            REASON += "There is an existing user id for this user\t"
                            REGISTRATION_STATUS = "Failure"
                    else:
                        print("The user id already exists")
                        REASON += "The user id already exists\t"
                        REGISTRATION_STATUS = "Failure"
                    print("Done reading from UserProfile.txt")
            except FileNotFoundError:
                print("File Not Found")
            if REGISTRATION_STATUS == "Success":
                ACCESS_TIME = datetime.now()
                STRING_ACCESS_TIME = ACCESS_TIME.strftime('%m/%d/%Y %H:%M:%S')
                print("Access time is ", STRING_ACCESS_TIME)
                REGISTRATION_RECORD = USER_ID+"\t"+USER_NAME+"\t"+USER_EMAIL+"\t"
                REGISTRATION_RECORD += USER_PASSWORD+"\t"+ADDR[0]+"\t"+STRING_ACCESS_TIME+"\n"
                OUTPUT_FILE = open("UserProfile.txt", "a")
                OUTPUT_FILE.write(REGISTRATION_RECORD)
                OUTPUT_FILE.close()
            #Send the registration status response back to the client
            RESPONSE = "Registration status: "+REGISTRATION_STATUS+"\r\n"
            if REGISTRATION_STATUS == "Success":
                CONNECTION_SOCKET.send(RESPONSE.encode())
            else:
                RESPONSE += REASON
                CONNECTION_SOCKET.send(RESPONSE.encode())
            print("Return to client: ", RESPONSE)
        else:
            break
    CONNECTION_SOCKET.close()

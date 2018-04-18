from socket import *
import sys
from _thread import *
import time
import msvcrt

serverName = "172.22.8.147"
serverPort = 12009
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
#print(clientSocket.recv(1024).decode('ascii'))
running = True

#thread function for getting messages from server
def chatRoomFromServer(clientSocket, x):
    global running
    #clientSocket.listen(10)
    while running:
        msg = clientSocket.recv(1024).decode('ascii')
        if len(msg) > 0:
            print(msg)
        if msg.upper() == "\nEXITING CHATROOM":
            running = False
            break

#thread function for sending messages to the server
def chatRoomToServer(clientSocket, x):
    global running
    #clientSocket.listen(10)
    while running:#chatroom while loop
        x = msvcrt.kbhit()#detects keyboard hit
        if x:
            ch = msvcrt.getch().decode()
            #fix if statement-not detecting character
            if ch == 'e':#if e key is hit        
                msg = input("\nEnter your message:\n")
                if len(msg) > 0:
                    clientSocket.send(msg.encode())
                if msg.upper() == "\nQUIT CHATROOM":
                    running = False
                    break

#main while loop for connection
while True:
    print("Input your choice:\n\tregister\n\tlogin\n\tquit\n")
    sentence = input("Input lowercase sentence:")#hello world
    x = "hello"
    clientSocket.send(sentence.encode())
    modifiedSentence = clientSocket.recv(1024).decode('ascii')
    print("From Server:", modifiedSentence)

    if "Connected" in modifiedSentence:
        #thread for receiving messages from server
        start_new_thread(chatRoomFromServer, (clientSocket, x))
        #thread for sending messages to the server
        start_new_thread(chatRoomToServer, (clientSocket, x))

        while running:
            time.sleep(.05)
        
            
    #receiving = clientSocket.recv(1024).decode('ascii')

    if modifiedSentence.upper() == "\nGOODBYE":
        sys.exit(0);
        #break
    
clientSocket.close()





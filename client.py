from socket import *
import sys
from _thread import *

serverName = "172.22.8.147"
serverPort = 12009
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
running = True

def chatRoom(clientSocket, x):
    global running
    #clientSocket.listen(10)
    while running:
        msg = clientSocket.recv(1024).decode('ascii')
        if len(msg) > 0:
            print(msg)
        elif msg.upper() == "QUIT CHATROOM":
            running = False
            break

while True:
    sentence = input("Input lowercase sentence:")#hello world
    #if not sentence:
     #   break
    x = "hello"
    clientSocket.send(sentence.encode())
    modifiedSentence = clientSocket.recv(1024).decode('ascii')
    print("From Server:", modifiedSentence)

    if "Connected" in modifiedSentence:
        start_new_thread(chatRoom, (clientSocket, x))
        #To Do: start a new thread for the client to send messages to server
        while running:#chatroom while loop
            msg = input("Enter your message: ")
            clientSocket.send(msg.encode())
            if msg.upper() == "QUIT CHATROOM":
                break
            
    #receiving = clientSocket.recv(1024).decode('ascii')

    if modifiedSentence.upper() == "GOODBYE":
        sys.exit(0);
        #break
    
clientSocket.close()





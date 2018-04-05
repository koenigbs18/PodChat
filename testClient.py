from socket import *
serverName = "127.0.0.1" #Use IP address of server
serverPort = 12008

#Create a socket and connect to the server
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

#Once it has been connected, Client send a Hello message to the server
message = "Hello"
clientSocket.send(message.encode()) #may need to just change to ("Hello")
#Once you receive a response, check the response, if it asks for name, ask
# user to input the name and send to the server

responseToHello = clientSocket.recv(1024).decode() #packet size is 1024kb max
print("Response to Hello: ", responseToHello)

if('name' in responseToHello):
    name = input('Please input your user:')
    clientSocket.send(name.encode())

##test##

from tkinter import *
import tkinter as tk
from socket import *
import ctypes  # An included library with Python install.
import time
import os
import sys
import subprocess

# client code
# create a socket and connect to the server
serverName = "96.40.228.79"
serverPort = 12009
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

#GUI Code
class PodChatApp(tk.Tk):

        def __init__(self, *args, **kwargs):
            tk.Tk.__init__(self, *args, **kwargs)
            container = tk.Frame(self)

            container.pack(side="top", fill="both", expand=True)

            container.grid_rowconfigure(0, weight=1)
            container.grid_rowconfigure(0, weight=1)

            self.frames = {}

            for F in (Login, Register, Menu, CreateChatRoom, ChatRoomBtns, OfflineMessages):
                frame = F(container, self)

                self.frames[F] = frame

                frame.grid(row=0, column=0, sticky="nsew")

            self.show_frame(Login)

        def show_frame(self, cont):
            frame = self.frames[cont]
            frame.tkraise()

        '''
        def showMessage(self, mess):
    
            frame = self.frames[mess]
            frame.tkraise()
        '''
        def send_message_protocol(self, toEntry, msgEntry):

            clientSocket.send("Chatroom".encode())

            try:
                SERVER_INFO = clientSocket.recv(1024).decode('ascii')
                print("server info: ", SERVER_INFO)
            except ConnectionResetError as e:
                print(e)
                print(e.args)
                print("connection times out")
                self.Mbox('pod Chat', 'could not reach server, please try again',1)
                return

            print("to entry: ", toEntry.get())
            print("message entry: ", msgEntry.get())

            sendMessage = toEntry.get() + "," + msgEntry.get()
            clientSocket.send(sendMessage.encode())
            #self.show_updated_msgframe(msgEntry.get(), CreateChatRoom)
            display = CreateChatRoom(None, None)
            self.display.test()

        ########show updated msg frame method############
        def show_updated_msgframe(self, msgEntry, cont):
            frame = self.frames[cont]
            frame.tkraise()


        def login_protocol(self, userNameEntry, pwdEntry):
            clientSocket.send("Login".encode())
            print("Client sent ""login"" message to server")

            try:
                SERVER_INFO = clientSocket.recv(1024).decode('ascii')
                print("server info:", SERVER_INFO)
            except ConnectionResetError as e:
                print(e)
                print(e.args)
                print("Connection timed out.")
                self.Mbox('Pod Chat', 'Could not reach server, please try again.', 1)
                return

            print("username: ", userNameEntry.get())
            print("password: ", pwdEntry.get())

            login = userNameEntry.get() + "," + pwdEntry.get()
            clientSocket.send(login.encode())
            loginValidation = clientSocket.recv(1024).decode('ascii')

            if "SUCCESS" in loginValidation.upper():
                self.show_frame(Menu)
                return
            else:
                print(loginValidation)
                self.Mbox('Pod Chat', loginValidation, 1)
                return

        def register_protocol(self, emailEntry, userNameEntry, pwdEntry):
            clientSocket.send("Register".encode())
            print("Client sent ""Register"" message to server")

            try:
                SERVER_INFO = clientSocket.recv(1024).decode('ascii')
                print("server info:", SERVER_INFO)
            except ConnectionResetError as e:
                print(e)
                print(e.args)
                print("Connection timed out.")
                self.Mbox('Pod Chat', 'Could not reach server, please try again.', 1)
                return

            print("email: ", emailEntry.get())
            print("username: ", userNameEntry.get())
            print("password: ", pwdEntry.get())

            register = emailEntry.get() + "," + userNameEntry.get() + "," + pwdEntry.get()
            clientSocket.send(register.encode())
            registrationValidation = clientSocket.recv(1024).decode('ascii')

            if "SUCCESS" in registrationValidation.upper():
                self.show_frame(Login)
                return
            else:
                print(registrationValidation)
                self.Mbox('Pod Chat', registrationValidation, 1)
                self.show_frame(Register)#goes back to register frame to retry
                return


        def logout_protocol(self):
            clientSocket.send("Logout".encode())
            print("Client: sent Logout message to server.")
            logoutMsg = clientSocket.recv(1024).decode('ascii')
            logoutMsg1 = clientSocket.recv(1024).decode('ascii')

            print(logoutMsg)
            print(logoutMsg1)

            if "SUCCESS" in logoutMsg1.upper():
                self.show_frame(Login)
                return
            else:
                #print(logoutMsg)
                self.Mbox('Pod Chat', logoutMsg1, 1)
                return

        def Mbox(self, title, text, style):
            return ctypes.windll.user32.MessageBoxW(0, text, title, style)


class Login(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Frame.configure(self, background='black')
        self.grid()

        #welcome message
        self.welcomeMsg = Label(self, text="Welcome to Pod Chat!\n Created and Used by Millennials!", background='black', fg="white")
        self.welcomeMsg.grid(row=0, sticky=N, columnspan=2, padx=50, pady=(25, 0))

        #username label
        self.userNameLabel = Label(self, text="Username: ", background='black', fg='white')
        self.userNameLabel.grid(row=1, sticky=W, padx=(50, 0), pady=(50, 0))

        #username entry
        self.userNameEntry = Entry(self)
        self.userNameEntry.grid(row=1, column=1, sticky=W, padx=(0, 50), pady=(50, 0))

        #password label
        self.pwdLabel = Label(self, text="Password:", background='black', fg='white')
        self.pwdLabel.grid(row=2, sticky=W, padx=(50, 0))

        #password entry
        self.pwdEntry = Entry(self, show="*")
        self.pwdEntry.grid(row=2, column=1, sticky=W, padx=(0, 50))

        #login button
        self.login = Button(self, text="Login", background='blue', fg='white', command=lambda: controller.login_protocol(self.userNameEntry, self.pwdEntry))
        self.login.grid(row=3, column=1, padx=(30, 0))

        # register label
        self.registerMsg = Label(self, text="New here?", background='black', fg='white')
        self.registerMsg.grid(row=4, pady=(50, 0), padx=(60, 0))

        #register button
        self.register = Button(self, text="Register", background='red', fg='white', command=lambda: controller.show_frame(Register))
        self.register.grid(row=4, column=1, pady=(50, 0))

class Register(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Frame.configure(self, background='black')
        self.grid()

        #welcome message
        self.registerMsg = Label(self, text="Register", background='black', fg="white")
        self.registerMsg.grid(row=0, sticky=N, columnspan=2, padx=50, pady=(25, 0))

        # email label
        self.emailLabel = Label(self, text="Email: ", background='black', fg='white')
        self.emailLabel.grid(row=1, sticky=W, padx=(50, 0), pady=(50, 0))

        # email entry
        self.emailEntry = Entry(self)
        self.emailEntry.grid(row=1, column=1, sticky=W, padx=(0, 50), pady=(50, 0))

        #username label
        self.userNameLabel = Label(self, text="Username: ", background='black', fg='white')
        self.userNameLabel.grid(row=2, sticky=W, padx=(50, 0))

        #username entry
        self.userNameEntry = Entry(self)
        self.userNameEntry.grid(row=2, column=1, sticky=W, padx=(0, 50))

        #password label
        self.pwdLabel = Label(self, text="Password:", background='black', fg='white')
        self.pwdLabel.grid(row=3, sticky=W, padx=(50, 0))

        #password entry
        self.pwdEntry = Entry(self, show="*")
        self.pwdEntry.grid(row=3, column=1, sticky=W, padx=(0, 50))

        #register button
        self.register = Button(self, text="Register", background='blue', fg='white', command=lambda: controller.register_protocol(self.emailEntry, self.userNameEntry, self.pwdEntry))
        self.register.grid(row=4, column=1, padx=(30, 0))

class OfflineMessages(tk.Frame):

    #default initial frame code for every frame
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Frame.configure(self, background='black')
        self.grid()

        #Sign out button
        self.signOutButton = Button(self, text="Sign Out", background='red', fg='white', command=lambda: controller.logout_protocol())
        self.signOutButton.grid(row=0, pady=(10,0),padx=(245,0), sticky=E)

        # Back button
        self.backButton = Button(self, text="Back", background='red', fg='white', command=lambda: controller.show_frame(Menu))
        self.backButton.grid(row=0, pady=10, sticky=W)

        #header message
        self.headerMsg = Label(self, text="Offline Messages", background='black', fg="white")
        self.headerMsg.grid(row=1, column=3, columnspan=3, sticky=N, pady=25)

        #Messages Button
        self.messages = Button(self, text="Messages", background='blue', fg='white',command = lambda: controller.show_frame(CreateChatRoom))
        self.messages.grid()

        #Chat Rooms button
        #self.chatRooms = Button(self, text="Chat Rooms", background='blue', fg='white', command=lambda: controller.show_frame(ChatRoomBtns))
        #self.chatRooms.grid(row=2, column=4)

        #Friends List Button
        #self.friendsList = Button(self, text="Friends List", background='blue', fg='white')
        #self.friendsList.grid(row=4, column=4)


class Menu(tk.Frame):

    #default initial frame code for every frame
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Frame.configure(self, background='black')
        self.grid()

        #Sign out button
        self.signOutButton = Button(self, text="Sign Out", background='red', fg='white', command=lambda: controller.logout_protocol())
        self.signOutButton.grid(row=0, padx=10, pady=10)

        #header message
        self.headerMsg = Label(self, text="What do you want to do?", background='black', fg="white")
        self.headerMsg.grid(row=1, column=3, columnspan=3, sticky=N, pady=25)

        #Chat Rooms button
        self.chatRooms = Button(self, text="Chat Room", background='blue', fg='white', command=lambda: controller.show_frame(CreateChatRoom))
        self.chatRooms.grid(row=2, column=4)

        #Messages Button
        self.messages = Button(self, text="Messages", background='blue', fg='white', command=lambda: controller.show_frame(OfflineMessages))
        self.messages.grid(row=3, column=4)

        #Friends List Button
        #self.friendsList = Button(self, text="Friends List", background='blue', fg='white')
        #self.friendsList.grid(row=4, column=4)

class CreateChatRoom(tk.Frame):

    #default initial frame code for every frame
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        tk.Frame.configure(self, background='black')
        self.grid()

        #Back button
        self.backButton = Button(self, text="Back", background='red', fg='white', command=lambda: controller.show_frame(Menu))
        self.backButton.grid(row=0)

        #self.createChatRoomLabel = Label(self, text="Chat Room", background='black', fg='white')
        #self.createChatRoomLabel.grid(row=0, column=1)

        # Room Name: label
       # self.RoomNameLabel = Label(self, text="Room: ", background='black', fg='white')
       # self.RoomNameLabel.grid(row=1, sticky=E, padx=(50, 0), pady=(25, 0))

        # Room Name: entry
       # self.RoomNameEntry = Entry(self)
       # self.RoomNameEntry.grid(row=1, column=1, sticky=W, padx=(0, 50), pady=(25, 0))

        #To: label

        self.toLabel = Label(self, text="To: ", background='black', fg='white')
        self.toLabel.grid(row=2, sticky=E, padx=(50, 0), pady=(5, 0))

        #self.toLabel = Label(self, text="To: ", background='black', fg='white')
        #self.toLabel.grid(row=2, sticky=E, padx=(50, 0), pady=(5, 0))


        # To: entry
        #self.toEntry = Entry(self)
        #self.toEntry.grid(row=2, column=1, sticky=W, padx=(0, 50), pady=(5, 0))

        #message window frame

        self.msgWindow = Frame(self, width=50, height=50)
        self.msgWindow.grid(row=3)

        #self.msgWindow = Frame(self, width=300, height=200)
        #self.msgWindow.grid(row=1)

        self.listbox = Listbox(self, width=50, height=15)
        self.listbox.insert(END, "hello")
        self.listbox.grid(padx=(0,5))

        #Message entry
        self.msgEntry = Entry(self, width=50)
        self.msgEntry.grid(row=2)




        #Send button

        #self.sendButton = Button(self, text="Send", background='blue', fg='white', command=lambda: controller.send_message_protocol(self.toEntry,self.msgEntry))
        self.sendButton = Button(self, text="Send", background='blue', fg='white', command=self.test)

        self.sendButton.grid(row=5, column=1, pady=(5, 0), padx=(75, 0))

        self.sendButton = Button(self, text="Send", background='blue', fg='white',command=lambda: controller.show_frame(Menu))
        self.sendButton.grid(row=3, pady=(5, 0))

    def test(self):
        print("test")


class ChatRoomBtns(tk.Frame):

    #default initial frame code for every frame
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Frame.configure(self, background='black')
        self.grid()

        #Sign out button
        self.signOutButton = Button(self, text="Sign Out", background='red', fg='white')
        self.signOutButton.grid(row=0, padx=10, pady=10)

        #welcome message
        self.welcomeMsg = Label(self, text="What do you want to do?", background='black', fg="white")
        self.welcomeMsg.grid(row=1, column=3, columnspan=3, sticky=N, pady=25)

        #Chat Rooms button
        self.chatRooms = Button(self, text="Chat Rooms", background='blue', fg='white', command=lambda: controller.show_frame(Menu))
        self.chatRooms.grid(row=2, column=4)

        self.subBtnFrame = Frame(self, width=200, height=100)
        self.subBtnFrame.grid(row=3, column=4)

        self.create = Button(self.subBtnFrame, text="Create", background='white', fg='black', command=lambda: controller.show_frame(CreateChatRoom))
        self.create.grid(row=3, column=4)

        #self.join = Button(self.subBtnFrame, text="Join", background='white', fg='black')
        #self.join.grid(row=3, column=5)

        #Messages Button
        self.messages = Button(self, text="Messages", background='blue', fg='white')
        self.messages.grid(row=5, column=4)

        #Friends List Button
        #self.friendsList = Button(self, text="Friends List.", background='blue', fg='white')
        #self.friendsList.grid(row=6, column=4)



app = PodChatApp()


app.title("Pod Chat")

#icon at top left
icon = PhotoImage(file='podCon.png')
app.tk.call('wm', 'iconphoto', app._w, icon)

#window size
width = 300
height = 400

screenWidth = app.winfo_screenwidth()
screenHeight = app.winfo_height()

x = (screenWidth/2) - (width/2)
y = (screenHeight/2) - (height/2)

app.geometry('%dx%d+%d+%d' % (width, height, 200, 200))

app.mainloop()


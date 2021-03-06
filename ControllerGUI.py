from tkinter import *
import tkinter as tk
from socket import *
from _thread import *
import ctypes  # An included library with Python install.
import time
import os
import sys
import subprocess

# client code
# create a socket and connect to the server
serverName = "127.0.0.1"
serverPort = 12009
clientSocket = socket(AF_INET, SOCK_STREAM)
chatRoomActive=False
listbox=None
username=None
headerMsg=None
try:
    clientSocket.connect((serverName, serverPort))
except TimeoutError as e:
    print(e)
    print(e.args)
    print("Connection timed out.")
    ctypes.windll.user32.MessageBoxW(0,'Could not reach server, please try again.','Pod Chat', 1)
    sys.exit(0)

#GUI Code
class PodChatApp(tk.Tk):

        def __init__(self, *args, **kwargs):
            tk.Tk.__init__(self, *args, **kwargs)

            container = tk.Frame(self)

            container.pack(side="top", fill="both", expand=True)

            container.grid_rowconfigure(0, weight=1)
            container.grid_rowconfigure(0, weight=1)

            self.frames = {}

            for F in (Login, Register, Menu, CreateChatRoom,OfflineMessages):
                frame = F(container, self)

                self.frames[F] = frame

                frame.grid(row=0, column=0, sticky="nsew")

            self.show_frame(Login)

        def show_frame(self, cont):
            frame = self.frames[cont]
            frame.tkraise()

        def login_protocol(self, userNameEntry, pwdEntry):
            global username
            global headerMsg
            clientSocket.send("Login".encode())
            SERVER_INFO = clientSocket.recv(1024).decode('ascii')
            print("server info:" + str(SERVER_INFO))

            print("username: " + str(userNameEntry.get()))
            print("password: " + str(pwdEntry.get()))

            login = userNameEntry.get() + "," + pwdEntry.get()
            clientSocket.send(login.encode())
            loginValidation = clientSocket.recv(1024).decode('ascii')
            print(loginValidation)

            if "SUCCESS" in loginValidation.upper():
                username=str(userNameEntry.get())
                headerMsg['text'] = "Welcome " + username
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
            global username
            clientSocket.send("Logout".encode())
            print("Client: sent Logout message to server.")
            username=None
            self.show_frame(Login)

        def chatroom_connection_protocol(self):
            global chatRoomActive
            global listbox
            chatRoomActive=True
            global username

            clientSocket.send("Chatroom".encode())
            offlinemsgs = clientSocket.recv(1024).decode('ascii')
            print("message: " + offlinemsgs)
            if len(offlinemsgs) > 0:
                offlinemsgs = offlinemsgs.split(',')
                for m in offlinemsgs:
                    if m != "ignore9999999":
                        print("inserting " + m)
                        listbox.insert(END, m)

            clientSocket.send((username + " has connected.").encode())
            # thread for receiving messages from server
            start_new_thread(self.chatRoomFromServer, ())
            self.show_frame(CreateChatRoom)

        # thread function for getting messages from server
        def chatRoomFromServer(self):
            global chatRoomActive
            global listbox

            while chatRoomActive == True:
                msg = clientSocket.recv(1024).decode('ascii')
                if len(msg) > 0:
                    listbox.insert(END, msg)
                    listbox.yview(END)
                    print(msg)
            print("chatroom thread ended")

        def quit_chatroom(self):
            global chatRoomActive
            global username
            global listbox
            chatRoomActive=False

            clientSocket.send((username + " has left.").encode())
            clientSocket.send("Qtchatroom".encode())
            listbox.delete(0, END)
            self.show_frame(Menu)

        def getUsername(self):
            return username


        def Mbox(self, title, text, style):
            return ctypes.windll.user32.MessageBoxW(0, text, title, style)


class Login(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Frame.configure(self, background='black')
        self.grid()

        #welcome message
        self.welcomeMsg = Label(self, text="Welcome to Pod Chat!", background='black', fg="white")
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

        #welcome message
        self.welcomeMsg = Label(self, text="Copyright 2018. Created and used by millennials.", background='black', fg="white", font=('', 8))
        self.welcomeMsg.grid(row=5, sticky=N, columnspan=2, pady=(100, 0))

class Register(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Frame.configure(self, background='black')
        self.grid()

        # Back button
        self.backButton = Button(self, text="Back", background='red', fg='white', command=lambda: controller.show_frame(Login))
        self.backButton.grid(row=0, pady=10, padx=10 ,sticky=W)

        #welcome message
        self.registerMsg = Label(self, text="Register", background='black', fg="white")
        self.registerMsg.grid(row=1, sticky=N, columnspan=2, padx=50, pady=(25, 0))

        # email label
        self.emailLabel = Label(self, text="Email: ", background='black', fg='white')
        self.emailLabel.grid(row=2, sticky=W, padx=(50, 0), pady=(50, 0))

        # email entry
        self.emailEntry = Entry(self)
        self.emailEntry.grid(row=2, column=1, sticky=W, padx=(0, 50), pady=(50, 0))

        #username label
        self.userNameLabel = Label(self, text="Username: ", background='black', fg='white')
        self.userNameLabel.grid(row=3, sticky=W, padx=(50, 0))

        #username entry
        self.userNameEntry = Entry(self)
        self.userNameEntry.grid(row=3, column=1, sticky=W, padx=(0, 50))

        #password label
        self.pwdLabel = Label(self, text="Password:", background='black', fg='white')
        self.pwdLabel.grid(row=4, sticky=W, padx=(50, 0))

        #password entry
        self.pwdEntry = Entry(self, show="*")
        self.pwdEntry.grid(row=4, column=1, sticky=W, padx=(0, 50))

        #register button
        self.register = Button(self, text="Register", background='blue', fg='white', command=lambda: controller.register_protocol(self.emailEntry, self.userNameEntry, self.pwdEntry))
        self.register.grid(row=5, column=1, padx=(30, 0))

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
        global username
        global headerMsg
        tk.Frame.__init__(self, parent)
        tk.Frame.configure(self, background='black')
        self.grid()
        #welcomemsg = "Welcome " + parent.username.get()

        #Sign out button
        self.signOutButton = Button(self, text="Sign Out", background='red', fg='white', command=lambda: controller.logout_protocol())
        self.signOutButton.grid(row=0, padx=10, pady=10)

        #header message
        self.headerMsg1 = Label(self, text= "Welcome ", background='black', fg="white")
        self.headerMsg1.grid(row=1, column=3, columnspan=3, sticky=N, pady=25)
        headerMsg = self.headerMsg1

        #Chat Rooms button
        self.chatRooms = Button(self, text="Chat Room", background='blue', fg='white', command=lambda: controller.chatroom_connection_protocol())
        self.chatRooms.grid(row=4, column=5, padx=40, pady = 6)

    # def getUsername(self):
    #     global username
    #     print(self.username.get())
    #     return self.username.get()


class CreateChatRoom(tk.Frame):

    #default initial frame code for every frame
    def __init__(self, parent, controller):
        global listbox
        tk.Frame.__init__(self, parent)
        tk.Frame.configure(self, background='black')
        self.grid()

        #Back button
        self.backButton = Button(self, text="Back", background='red', fg='white', command=lambda: controller.quit_chatroom())
        self.backButton.grid(row=0)

        #listbox
        self.listbox1 = Listbox(self, width=50, height=15)
        self.listbox1.grid(pady=(0,5))
        listbox = self.listbox1

        #Message entry
        self.msgEntry = Entry(self, width=50)
        self.msgEntry.bind('<Return>', lambda event: self.sendMessage(self.msgEntry))
        self.msgEntry.grid(row=2)


        #Send button
        self.sendButton = Button(self, text="Send", background='blue', fg='white', command=lambda: self.sendMessage(self.msgEntry))
        self.sendButton.grid(row=3, pady=(5, 0))

    def sendMessage(self, msg):
        global username
        size = len(str(msg.get()))
        spacestr = ""
        spaceindex = 0

        index = 0
        sendCount = -(-size//32) # amount of messages to send

        while spaceindex < (len(username)*2):
            spacestr = spacestr + " "
            spaceindex = spaceindex + 1

        if size > 0:
            clientSocket.send((username + ": " + msg.get()[0:32]).encode())
            time.sleep(.05)
            if size >= 32:
                time.sleep(.05)
                clientSocket.send((spacestr + msg.get()[32:64]).encode())
                time.sleep(.05)
                if size >= 64:
                    clientSocket.send((spacestr + msg.get()[64:96]).encode())

        self.msgEntry.delete(0, 'end')


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


def on_closing():
    if chatRoomActive == False:
        clientSocket.send("Quit".encode())
        recmsg = clientSocket.recv(1024).decode()
    elif chatRoomActive == True:
        clientSocket.send("Qtchatroom".encode())
        recmsg = clientSocket.recv(1024).decode()
        clientSocket.send("Quit".encode())

    try:
        app.destroy()
    except:
        pass

app.protocol("WM_DELETE_WINDOW", on_closing)

app.mainloop()


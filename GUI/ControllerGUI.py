from tkinter import *
import tkinter as tk

class PodChatApp(tk.Tk):

        def __init__(self, *args, **kwargs):

            tk.Tk.__init__(self, *args, **kwargs)
            container = tk.Frame(self)

            container.pack(side="top", fill="both", expand=True)

            container.grid_rowconfigure(0, weight=1)
            container.grid_rowconfigure(0, weight=1)

            self.frames = {}

            for F in (Login, Register, Menu, NewMessage, ChatRoom):
                frame = F(container, self)

                self.frames[F] = frame

                frame.grid(row=0, column=0, sticky="nsew")

            self.show_frame(Login)

        def show_frame(self, cont):
            frame = self.frames[cont]
            frame.tkraise()

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
        self.userNameLabel.grid(row=1, sticky=W, padx=(50, 0), pady=(50,0))

        #username entry
        self.userNameEntry = Entry(self)
        self.userNameEntry.grid(row=1, column=1, sticky=W, padx=(0, 50), pady=(50,0))

        #password label
        self.pwdLabel = Label(self, text="Password:", background='black', fg='white')
        self.pwdLabel.grid(row=2, sticky=W, padx=(50, 0))

        #password entry
        self.pwdEntry = Entry(self, show="*")
        self.pwdEntry.grid(row=2, column=1, sticky=W, padx=(0, 50))

        #login button
        self.login = Button(self, text="Login", background='blue', fg='white', command=lambda: controller.show_frame(Menu))
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
        self.register = Button(self, text="Register", background='blue', fg='white', command=lambda: controller.show_frame(Login))
        self.register.grid(row=4, column=1, padx=(30, 0))

class Menu(tk.Frame):

    #default initial frame code for every frame
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Frame.configure(self, background='black')
        self.grid()

        #Sign out button
        self.signOutButton = Button(self, text="Sign Out", background='red', fg='white')
        self.signOutButton.grid(row=0, padx=10, pady=10)

        #header message
        self.headerMsg = Label(self, text="What do you want to do?", background='black', fg="white")
        self.headerMsg.grid(row=1, column=3, columnspan=3, sticky=N, pady=25)

        #Chat Rooms button
        self.chatRooms = Button(self, text="Chat Rooms", background='blue', fg='white', command=lambda: controller.show_frame(ChatRoom))
        self.chatRooms.grid(row=2, column=4)

        #Messages Button
        self.messages = Button(self, text="Messages", background='blue', fg='white')
        self.messages.grid(row=3, column=4)

        #Friends List Button
        self.friendsList = Button(self, text="Friends List", background='blue', fg='white')
        self.friendsList.grid(row=4, column=4)

class NewMessage(tk.Frame):

    #default initial frame code for every frame
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Frame.configure(self, background='black')
        self.grid()

        #Back button
        self.backButton = Button(self, text="Back", background='red', fg='white')
        self.backButton.grid(row=0, padx=10, pady=10)

        self.newMsgLabel = Label(self, text="New Message", background='black', fg='white')
        self.newMsgLabel.grid(row=0, column=1, padx=(0,25), pady=(15, 0))

        # To: label
        self.toLabel = Label(self, text="To: ", background='black', fg='white')
        self.toLabel.grid(row=1, sticky=W, padx=(50, 0), pady=(25, 0))

        # To: entry
        self.toEntry = Entry(self)
        self.toEntry.grid(row=1, column=1, sticky=W, padx=(0, 50), pady=(25, 0))

        #message window frame
        self.msgWindow = Frame(self, width=200, height=200)
        self.msgWindow.grid(row=2, column=1, pady=(5,0), columnspan=2)

        #Message entry
        self.msgEntry = Entry(self, width=25)
        self.msgEntry.grid(row=3, column=0, columnspan=2, padx=(30, 0), pady=(5,0))

        #Send button
        self.sendButton = Button(self, text="Send", background='blue', fg='white')
        self.sendButton.grid(row=3, column=1, pady=(5,0), padx=(165,0))

class ChatRoom(Frame):

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

        self.create = Button(self.subBtnFrame, text="Create", background='white', fg='black', command=lambda: controller.show_frame(NewMessage))
        self.create.grid(row=3, column=4)

        self.join = Button(self.subBtnFrame, text="Join", background='white', fg='black')
        self.join.grid(row=3, column=5)

        #Messages Button
        self.messages = Button(self, text="Messages", background='blue', fg='white')
        self.messages.grid(row=5, column=4)

        #Friends List Button
        self.friendsList = Button(self, text="Friends List.", background='blue', fg='white')
        self.friendsList.grid(row=6, column=4)

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


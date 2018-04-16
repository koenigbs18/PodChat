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

            for F in (Login, Register):
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
        self.login = Button(self, text="Login", background='blue', fg='white')
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
        self.register = Button(self, text="Register", background='blue', fg='white', command=controller.show_frame(Login))
        self.register.grid(row=4, column=1, padx=(30, 0))



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

#from tkinter import *
# from RegisterGUI import *
#
# class Application(Frame):
#     def __init__(self, master):
#         #Initializes frame
#         Frame.__init__(self, master)
#         self.grid()
#         self.create_widgets()
#
#     def create_widgets(self):
#
#         #welcome message
#         self.welcomeMsg = Label(self, text="Welcome to Pod Chat!\n Created and Used by Millennials!", background='black', fg="white")
#         self.welcomeMsg.grid(row=0, sticky=N, columnspan=2, padx=50, pady=(25, 0))
#
# class Login(Frame):
#
#     def __init__(self, master):
#         #Initializes frame
#         Frame.__init__(self, master)
#         self.grid()
#         self.create_widgets()
#
#     def create_widgets(self):
#
#         #welcome message
#         self.welcomeMsg = Label(self, text="Welcome to Pod Chat!\n Created and Used by Millennials!", background='black', fg="white")
#         self.welcomeMsg.grid(row=0, sticky=N, columnspan=2, padx=50, pady=(25, 0))
#
#         #username label
#         self.userNameLabel = Label(self, text="Username: ", background='black', fg='white')
#         self.userNameLabel.grid(row=1, sticky=W, padx=(50, 0), pady=(50,0))
#
#         #username entry
#         self.userNameEntry = Entry(self)
#         self.userNameEntry.grid(row=1, column=1, sticky=W, padx=(0, 50), pady=(50,0))
#
#         #password label
#         self.pwdLabel = Label(self, text="Password:", background='black', fg='white')
#         self.pwdLabel.grid(row=2, sticky=W, padx=(50, 0))
#
#         #password entry
#         self.pwdEntry = Entry(self, show="*")
#         self.pwdEntry.grid(row=2, column=1, sticky=W, padx=(0, 50))
#
#         #login button
#         self.login = Button(self, text="Login", background='blue', fg='white', command=self.login)
#         self.login.grid(row=3, column=1, padx=(30, 0))
#
#         # register label
#         self.registerMsg = Label(self, text="New here?", background='black', fg='white')
#         self.registerMsg.grid(row=4, pady=(50, 0), padx=(60, 0))
#
#         #register button
#         #self.register = Button(self, text="Register", background='red', fg='white', command=self.show_frame(Register))
#         self.register = Button(self, text="Register", background='red', fg='white')
#         self.register.grid(row=4, column=1, pady=(50, 0))
#
#     def login(self):
#
#         username = self.userNameEntry.get()
#         password = self.pwdEntry.get()
#
#         #hello(username, password)
#
#     def show_frame(self, cont):
#         frame = self.frames[cont]
#         frame.tkraise()
#
# class Register(Frame):
#
#     def __init__(self, master):
#         #Initializes frame
#         Frame.__init__(self, master)
#         self.grid()
#         self.create_widgets()
#
#     def create_widgets(self):
#
#         #welcome message
#         self.registerMsg = Label(self, text="Register", background='black', fg="white")
#         self.registerMsg.grid(row=0, sticky=N, columnspan=2, padx=50, pady=(25, 0))
#
#         # username label
#         self.emailLabel = Label(self, text="Email: ", background='black', fg='white')
#         self.emailLabel.grid(row=1, sticky=W, padx=(50, 0), pady=(50, 0))
#
#         # username entry
#         self.emailEntry = Entry(self)
#         self.emailEntry.grid(row=1, column=1, sticky=W, padx=(0, 50), pady=(50, 0))
#
#         #username label
#         self.userNameLabel = Label(self, text="Username: ", background='black', fg='white')
#         self.userNameLabel.grid(row=2, sticky=W, padx=(50, 0))
#
#         #username entry
#         self.userNameEntry = Entry(self)
#         self.userNameEntry.grid(row=2, column=1, sticky=W, padx=(0, 50))
#
#         #password label
#         self.pwdLabel = Label(self, text="Password:", background='black', fg='white')
#         self.pwdLabel.grid(row=3, sticky=W, padx=(50, 0))
#
#         #password entry
#         self.pwdEntry = Entry(self, show="*")
#         self.pwdEntry.grid(row=3, column=1, sticky=W, padx=(0, 50))
#
#
#
#         #login button
#         self.register = Button(self, text="Register", background='blue', fg='white', command=self.login)
#         self.register.grid(row=4, column=1, padx=(30, 0))
#
#
# root = Tk()
#
# root.title("Pod Chat")
# root.configure(background='black')
#
# #icon at top left
# icon = PhotoImage(file='podCon.png')
# root.tk.call('wm', 'iconphoto', root._w, icon)
#
# #window size
# width = 300
# height = 400
#
# screenWidth = root.winfo_screenwidth()
# screenHeight = root.winfo_height()
#
# x = (screenWidth/2) - (width/2)
# y = (screenHeight/2) - (height/2)
#
# root.geometry('%dx%d+%d+%d' % (width, height, 200, 200))
#
# loginFrame = Application(root)
# loginFrame.configure(background='black')
#
# root.mainloop()

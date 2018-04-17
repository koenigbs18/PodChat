from tkinter import *
from practicefunctions import *

class Login(Frame):

    def __init__(self, master):
        #Initializes frame
        Frame.__init__(self, master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):

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
        self.login = Button(self, text="Login", background='blue', fg='white', command=self.login)
        self.login.grid(row=3, column=1, padx=(30, 0))

        # register label
        self.registerMsg = Label(self, text="New here?", background='black', fg='white')
        self.registerMsg.grid(row=4, pady=(50, 0), padx=(60, 0))

        #register button
        #self.register = Button(self, text="Register", background='red', fg='white', command=self.login)
        self.register = Button(self, text="Register", background='red', fg='white')
        self.register.grid(row=4, column=1, pady=(50, 0))

    def login(self):

        username = self.userNameEntry.get()
        password = self.pwdEntry.get()

        hello(username, password)

root = Tk()

root.title("Pod Chat")
root.configure(background='black')

#icon at top left
icon = PhotoImage(file='podCon.png')
root.tk.call('wm', 'iconphoto', root._w, icon)

#window size
width = 300
height = 400

screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_height()

x = (screenWidth/2) - (width/2)
y = (screenHeight/2) - (height/2)

root.geometry('%dx%d+%d+%d' % (width, height, 200, 200))

loginFrame = Login(root)
loginFrame.configure(background='black')

root.mainloop()





#
#username = StringVar()
#password = StringVar()

#login labels and entries
#Label(root, text="Username: ", background='black', fg='white').grid(row=0, sticky=W, pady=(100, 0), padx=(50, 0))
#Entry(root).grid(row=0, column=1, sticky=E, pady=(100, 0))

#Label(root, text="Password: ", background='black', fg='white').grid(row=1, sticky=W, padx=(50, 0))
#Entry(root).grid(row=1, column=1, sticky=E, pady=4)

#loginF = practicefunctions.hello("<Button-1>", username, password)
#login button
#loginButton = Button(root, text="Login", background='blue', fg='white', command=lambda: hello("<Button-1>", username, password))
#loginButton.grid(row=3, column=1, padx=(75, 0))


#register label and button
#Label(root, text="New here?", background='black', fg='white').grid(row=4, columnspan=2, pady=(50, 0))
#Button(root, text="Register", background='red', fg='white').grid(row=4, column=1, pady=(50, 0), padx=(50, 0))



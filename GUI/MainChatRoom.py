from tkinter import *


class MainChatRoom(Frame):

    def __init__(self, master):
        #Initializes frame
        Frame.__init__(self, master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        #Back button
        self.backButton = Button(self, text="Back", background='red', fg='white')
        self.backButton.grid(row=0, padx=10, pady=10)

        self.roomNameLabel = Label(self, text="Room Name", background='black', fg='white')
        self.roomNameLabel.grid(row=0, column=1, padx=(0,25), pady=(15, 0))

        # Users List label

        var = StringVar()
        var.set("Users List:")

        self.userListLabel = Label(self, background='black', fg='white', textvariable=var)
        self.userListLabel.grid(row=1, sticky=W, padx=(50, 0), pady=(25, 0))

        # message window frame
        self.msgWindow = Frame(self, width=150, height=200)
        self.msgWindow.grid(row=3, column=1, pady=(5, 0), columnspan=2, sticky=W)

        # Message entry
        self.msgEntry = Entry(self, width=24)
        self.msgEntry.grid(row=4, column=0, columnspan=2, padx=(125, 0), pady=(5, 0), sticky=W)

        # Send button
        self.sendButton = Button(self, text="Send", background='blue', fg='white')
        self.sendButton.grid(row=5, column=1, pady=(5, 0), padx=(75, 0))


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

mainChatRoom = MainChatRoom(root)
mainChatRoom.configure(background='black')

root.mainloop()

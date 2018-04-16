from tkinter import *


class ChatRoom(Frame):

    def __init__(self, master):
        #Initializes frame
        Frame.__init__(self, master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):

        #Sign out button
        self.signOutButton = Button(self, text="Sign Out", background='red', fg='white')
        self.signOutButton.grid(row=0, padx=10, pady=10)

        #welcome message
        self.welcomeMsg = Label(self, text="What do you want to do?", background='black', fg="white")
        self.welcomeMsg.grid(row=1, column=3, columnspan=3, sticky=N, pady=25)

        #Chat Rooms button
        self.chatRooms = Button(self, text="Chat Rooms", background='blue', fg='white')
        self.chatRooms.grid(row=2, column=4)

        self.subBtnFrame = Frame(self, width=200, height=100)
        self.subBtnFrame.grid(row=3, column=4)

        self.create = Button(self.subBtnFrame, text="Create", background='white', fg='black')
        self.create.grid(row=3, column=4)

        self.join = Button(self.subBtnFrame, text="Join", background='white', fg='black')
        self.join.grid(row=3, column=5)

        #Messages Button
        self.messages = Button(self, text="Messages", background='blue', fg='white')
        self.messages.grid(row=5, column=4)

        #Friends List Button
        self.friendsList = Button(self, text="Friends List.", background='blue', fg='white')
        self.friendsList.grid(row=6, column=4)


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

chatroom = ChatRoom(root)
chatroom.configure(background='black')

root.mainloop()

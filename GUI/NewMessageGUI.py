from tkinter import *


class NewMessage(Frame):

    def __init__(self, master):
        #Initializes frame
        Frame.__init__(self, master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
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

NewMessage = NewMessage(root)
NewMessage.configure(background='black')

root.mainloop()

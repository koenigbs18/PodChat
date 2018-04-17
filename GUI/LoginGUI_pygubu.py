try:
    import tkinter as tk  # for python 3
except:
    import Tkinter as tk  # for python 2
import pygubu
from tkinter import*

class Application:
    def __init__(self, master):

        #1: Create a builder
        self.builder = builder = pygubu.Builder()

        #2: Load a ui file
        #builder.add_from_file('podchat2.ui')

        #3: Create the widget using a master as parent
        self.mainwindow = builder.get_object(self, master)

        #4: Connect callbacks
        builder.connect_callbacks(self)

    def printHello(self):
        print("Hello")


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Pod Chat")
    root.configure(background='black')

    # icon at top left
    icon = PhotoImage(file='podCon.png')
    root.tk.call('wm', 'iconphoto', root._w, icon)

    # window size
    width = 300
    height = 400

    screenWidth = root.winfo_screenwidth()
    screenHeight = root.winfo_height()

    x = (screenWidth / 2) - (width / 2)
    y = (screenHeight / 2) - (height / 2)

    root.geometry('%dx%d+%d+%d' % (width, height, 200, 200))

    app = Application(root)

    # login labels and entries
    Label(root, text="Username: ", background='black', fg='white').grid(row=0, sticky=W, pady=(100, 0), padx=(50, 0))
    Entry(root).grid(row=0, column=1, sticky=E, pady=(100, 0))

    Label(root, text="Password: ", background='black', fg='white').grid(row=1, sticky=W, padx=(50, 0))
    Entry(root).grid(row=1, column=1, sticky=E, pady=4)

    # loginF = practicefunctions.hello("<Button-1>", username, password)
    # login button
    loginButton = Button(root, text="Login", background='blue', fg='white',
                         command=lambda: hello("<Button-1>", username, password))
    loginButton.grid(row=3, column=1, padx=(75, 0))

    # register label and button
    Label(root, text="New here?", background='black', fg='white').grid(row=4, columnspan=2, pady=(50, 0))
    Button(root, text="Register", background='red', fg='white').grid(row=4, column=1, pady=(50, 0), padx=(50, 0))

    root.mainloop()
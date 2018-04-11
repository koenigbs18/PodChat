from tkinter import*
from tkinter import ttk
import practicefunctions

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

username = StringVar()
password = StringVar()

#login labels and entries
Label(root, text="Username: ", background='black', fg='white').grid(row=0, sticky=W, pady=(100, 0), padx=(50, 0))
username = Entry(root).grid(row=0, column=1, sticky=E, pady=(100, 0))

Label(root, text="Password: ", background='black', fg='white').grid(row=1, sticky=W, padx=(50, 0))
password = Entry(root).grid(row=1, column=1, sticky=E, pady=4)

loginF = practicefunctions.hello("<Button-1>", username, password)
#login button
loginButton = Button(root, text="Login", background='blue', fg='white', command=loginF)
loginButton.grid(row=3, column=1, padx=(75, 0))


#register label and button
Label(root, text="New here?", background='black', fg='white').grid(row=4, columnspan=2, pady=(50, 0))
Button(root, text="Register", background='red', fg='white').grid(row=4, column=1, pady=(50, 0), padx=(50, 0))


root.mainloop()
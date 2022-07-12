from tkinter import *

root = Tk()

e = Entry(root, width=40, borderwidth=10, fg="red")
e.pack()
e.insert(0, "Your name here")


def myClick():
    myLabel = Label(root, text=e.get())
    myLabel.pack()


myButton = Button(root, text="Enter your name", command=myClick, fg="purple", bg="#ffffff")  # state=DISABLED # padx=40, pady=40
myButton.pack()

root.mainloop()

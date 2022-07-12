from tkinter import *

root = Tk()


def myClick():
    myLabel = Label(root, text="Look! I click a Button!!!")
    myLabel.pack()


myButton = Button(root, text="Click Me!", command=myClick, fg="purple", bg="#ffffff")  # state=DISABLED # padx=40, pady=40
myButton.pack()

root.mainloop()

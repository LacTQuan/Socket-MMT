from tkinter import *

root = Tk()

# Create a Label Widget
myLabel1 = Label(root, text="Hello World!")
myLabel2 = Label(root, text="I am Dang.")
# Show it onto the screen
myLabel1.grid(row=0, column=0)
myLabel2.grid(row=1, column=0)


root.mainloop()

import necessary libraries
from tkinter import *

root = Tk()
root.geometry("480x380")
root.title("main")

def topwin():
    top = Toplevel()
    top.geometry("180x150")
    top.title("toplevel")
    lbl = Label(top, text = "This is toplevel window")
    lbl.pack()
    top.mainloop()
btn = Button(top, text = "Click here to open another window", command = topwin)
btn.pack()
root.mainloop()
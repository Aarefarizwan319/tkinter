import tkinter as tk
from tkinter import messagebox

root = tk.Tk()

root.geometry("200x200")

def on_click():
    messagebox.showwarning("Alert, Virus Found !")

button=tk.Button(root,text="scan for virus",command=on_click)
button.place(x=40,y=80)

root.mainloop()
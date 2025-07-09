from tkinter import *
from PIL import Image, ImageTk

root = Tk()
root.title('Image Viewer')
root.geometry('400x400')

upload=Image.open("hp.jpg")
image=ImageTk.PhotoImage(upload)

label=Label(root,image=image,height=300,width=300)
label.place(x=50,y=0)

label2=Label(root,text="This is how we add image")
label.place(x=50,y=310)

root.mainloop()


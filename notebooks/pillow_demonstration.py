from tkinter import *
from tkinter import font
from PIL import Image, ImageTk

root = Tk()
root.geometry("1280x720")

own_font1 = font.Font(name="McFont", family="Arial", size=24, weight="bold", slant="roman", underline=1, overstrike=0)
default_font = font.nametofont("TkTextFont")
font_list = font.families()
label = Label(root, text="Deez Nuts", font=("Orange Gummy", 24)).pack()


# image_file = ImageTk.PhotoImage(image="C:/users/pc/downloads/man.jpg", size=(32,32))
# image_file2 = ImageTk.PhotoImage(Image.open("C:/users/pc/downloads/man.jpg").resize((32, 32)))
size=(32,32)
image_file2 = ImageTk.PhotoImage(Image.open("C:/users/pc/downloads/man.jpg", size))

Button(root, text="Hello my child", image=image_file2, compound=LEFT).pack()


root.mainloop()


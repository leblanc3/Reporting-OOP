from tkinter import *
from PIL import ImageTk, Image
import random

main = Tk()
main.title("Doctor's Note")
main.geometry("1280x720")

own_image = Image.open("images/jesus.png")
own_image_resized = own_image.resize((500, 500))
own_image_tk = ImageTk.PhotoImage(own_image_resized)

def change_color():
    color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
    first_line.config(fg=color)
    main.after(200, change_color)

font_families = ["Arial", "Courier", "Helvetica", "Times", "Comic Sans", "MS", "Verdana", "Georgia"]

def change_font():
    random_font = random.choice(font_families)
    size = random.randint(12, 24)
    style = random.choice(["normal", "bold", "italic"])
    second_line.config(font=(random_font, size, style))
    main.after(1000, change_font)

def lower_lifespan():
    global months_to_live
    months_to_live -= 1

    if months_to_live <= 0:
        first_line.config(text="Your suffering is no longer.")
        second_line.destroy()
        upper_line.destroy()
        button.destroy()
        Label(main, image=own_image_tk).pack(expand=True, fill="both")
    else:
        second_line.config(text="You have " + str(months_to_live) + " months left to live.")

types_of_cancer = ["Lung", "Pancreatic", "Breast", "Skin", "Prostate"]

type_of_cancer = types_of_cancer[random.randint(0, 4)]
months_to_live = random.randint(1, 12)

upper_line = Label(main, text="You have:", font=("Arial", 35))
upper_line.pack(expand=True)

first_line = Label(main, text=type_of_cancer + " Cancer", font=("Arial", 78))
first_line.pack(expand=True)

second_line = Label(main, text="You have " + str(months_to_live) + " months left to live.")
second_line.pack(expand=True)

button = Button(main, text="Click to slowly end your suffering", command=lower_lifespan)
button.pack(expand=True)

change_color()
change_font()

main.mainloop()
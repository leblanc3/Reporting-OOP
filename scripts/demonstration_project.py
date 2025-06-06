from tkinter import *
from tkinter import ttk

# Comment ni zybert

def display_widget():
    selected_widget = widget_chooser.curselection()

    if selected_widget:
        selected_widget_name = widget_chooser.get(selected_widget[0])
        selected_widget_class = widgets_dictionary[selected_widget_name]
        
        selected_widget_class(main).grid()

main = Tk()
main.geometry("1280x720")
main.title("Demonstration Program")

widgets_dictionary = {"Frame": Frame, 
                      "Label": Label, 
                      "Button": Button, 
                      "Checkbutton": Checkbutton, 
                      "Radiobutton": Radiobutton, 
                      "Entry": Entry, 
                      "Combobox": ttk.Combobox, 
                      "Listbox": Listbox, 
                      "Scrollbar": Scrollbar, 
                      "Text": Text}

widget_chooser = Listbox(main, height=10)
widget_chooser.grid()

for widget_name in widgets_dictionary:
    widget_chooser.insert(END, widget_name)

choose_widget_button = Button(main, text="Display widget", command=display_widget)
choose_widget_button.grid()

main.mainloop()
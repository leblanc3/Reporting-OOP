from tkinter import *
from tkinter import ttk

class WidgetSelectorDisplay:
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
    widget_chooser.pack()

    @staticmethod
    def initialize_widgets():
        for widget_name in WidgetSelectorDisplay.widgets_dictionary:
            WidgetSelectorDisplay.widget_chooser.insert(END, widget_name)
        
        choose_widget_button = Button(WidgetSelectorDisplay.main, text="Display widget", command=WidgetSelectorDisplay.display_widget)
        choose_widget_button.pack()

    @staticmethod
    def display_widget():
        selected_widget = WidgetSelectorDisplay.widget_chooser.curselection()

        if selected_widget:
            selected_widget_name = WidgetSelectorDisplay.widget_chooser.get(selected_widget[0])
            selected_widget_class = WidgetSelectorDisplay.widgets_dictionary[selected_widget_name]
            
            selected_widget_class(WidgetSelectorDisplay.main).pack()

WidgetSelectorDisplay.initialize_widgets()
WidgetSelectorDisplay.main.mainloop()
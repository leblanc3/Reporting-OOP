from tkinter import *
from tkinter import ttk
from tkinter import font, filedialog, colorchooser
from PIL import Image, ImageTk

window = Tk()
window.title("Widget Customizer")
window.geometry("1000x700")  # wider window to fit both sides nicely

# Global variables
current_widget = None
current_image = None
default_text = "Sample Text"
last_widget_type = None  # for proper reset

# ---------- Main layout ----------

main_frame = Frame(window)
main_frame.pack(fill="both", expand=True)

# Left frame for widget display
left_frame = Frame(main_frame, width=500)
left_frame.pack(side="left", fill="both", expand=True)

# Right frame for notebook (tabs)
right_frame = Frame(main_frame, width=500)
right_frame.pack(side="right", fill="both", expand=True)

# ---------- Selected Widget Display Area ----------

selected_widget_frame = LabelFrame(left_frame, text="Selected Widget Display", padx=10, pady=10)
selected_widget_frame.pack(pady=10, fill="x")

# Widget options
widget_var = StringVar()
widget_options = ["Label", "Button", "Entry", "Checkbutton", "Radiobutton", "Listbox", "Text"]

top_row_frame = Frame(selected_widget_frame)
top_row_frame.pack(fill="x")

widget_dropdown = ttk.Combobox(top_row_frame, textvariable=widget_var, values=widget_options)
widget_dropdown.pack(side="left", padx=5)

# Display area
display_area = Frame(selected_widget_frame, height=300, bg="white")
display_area.pack(fill="both", expand=True, pady=20)

# Function to display selected widget
def display_widget():
    global current_widget, last_widget_type
    for child in display_area.winfo_children():
        child.destroy()

    widget_type = widget_var.get()
    last_widget_type = widget_type  # remember for reset

    if widget_type == "Label":
        current_widget = Label(display_area, text=default_text)
    elif widget_type == "Button":
        current_widget = Button(display_area, text=default_text)
    elif widget_type == "Entry":
        current_widget = Entry(display_area)
        current_widget.insert(0, default_text)
    elif widget_type == "Checkbutton":
        current_widget = Checkbutton(display_area, text=default_text)
    elif widget_type == "Radiobutton":
        current_widget = Radiobutton(display_area, text=default_text, value=1)
    elif widget_type == "Listbox":
        current_widget = Listbox(display_area)
        current_widget.insert(END, default_text)
    elif widget_type == "Text":
        current_widget = Text(display_area, height=5)
        current_widget.insert(END, default_text)
    else:
        current_widget = Label(display_area, text="Unknown Widget")
    
    current_widget.pack(pady=20)

# Display and Reset buttons
Button(top_row_frame, text="Display Widget", command=display_widget).pack(side="left", padx=5)

def reset_all():
    # Simply recreate last selected widget for true reset
    if last_widget_type:
        widget_var.set(last_widget_type)
        display_widget()

Button(top_row_frame, text="Reset All", command=reset_all).pack(side="left", padx=5)

# ---------- Notebook Tabs ----------

notebook = ttk.Notebook(right_frame)
notebook.pack(fill="both", expand=True)

# Helper to create scrollable tab
def create_scrollable_tab(notebook, tab_name):
    tab_frame = Frame(notebook)
    notebook.add(tab_frame, text=tab_name)

    canvas = Canvas(tab_frame)
    scrollbar = Scrollbar(tab_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Fix canvas min size so scrollbar always appears when needed
    canvas.update_idletasks()
    canvas.config(width=480, height=600)

    return scrollable_frame

# ---------- Font Customizer Tab ----------

font_frame = create_scrollable_tab(notebook, "Font Customizer")

Label(font_frame, text="Change Displayed Text:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
text_entry = Entry(font_frame)
text_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

Label(font_frame, text="Choose Font Family:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
font_family = ttk.Combobox(font_frame, values=list(font.families()))
font_family.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

Label(font_frame, text="Choose Font Size:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
font_size = ttk.Combobox(font_frame, values=[str(i) for i in range(8, 49)])
font_size.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

bold_var = BooleanVar()
italic_var = BooleanVar()
underline_var = BooleanVar()
strikethrough_var = BooleanVar()

Checkbutton(font_frame, text="Bold", variable=bold_var).grid(row=3, column=0, sticky="w", padx=10)
Checkbutton(font_frame, text="Italic", variable=italic_var).grid(row=4, column=0, sticky="w", padx=10)
Checkbutton(font_frame, text="Underlined", variable=underline_var).grid(row=5, column=0, sticky="w", padx=10)
Checkbutton(font_frame, text="Strikethrough", variable=strikethrough_var).grid(row=6, column=0, sticky="w", padx=10)

def change_font():
    global current_widget
    if current_widget is None:
        return

    apply_font = False

    # Check if any field was provided
    family = font_family.get()
    size = font_size.get()

    weight = "bold" if bold_var.get() else "normal"
    slant = "italic" if italic_var.get() else "roman"
    underline = underline_var.get()
    overstrike = strikethrough_var.get()

    # If font family or size or style checkboxes used → apply font
    if family or size or bold_var.get() or italic_var.get() or underline_var.get() or strikethrough_var.get():
        apply_font = True

    if apply_font:
        # Build font using current widget's font as base
        try:
            current_font = font.Font(font=current_widget.cget("font"))
        except:
            current_font = font.Font(family="Arial", size=12)

        # Override only provided fields
        new_family = family if family else current_font.actual("family")
        new_size = int(size) if size else current_font.actual("size")

        new_font = font.Font(
            family=new_family,
            size=new_size,
            weight=weight,
            slant=slant,
            underline=underline,
            overstrike=overstrike
        )

        try:
            current_widget.configure(font=new_font)
        except:
            pass

    # Change text if Entry is not empty
    new_text = text_entry.get()
    if new_text.strip():
        try:
            current_widget.configure(text=new_text)
        except:
            try:
                current_widget.delete(0, END)
                current_widget.insert(0, new_text)
            except:
                try:
                    current_widget.delete("1.0", END)
                    current_widget.insert("1.0", new_text)
                except:
                    pass


Button(font_frame, text="Change Font", command=change_font).grid(row=0, column=2, rowspan=7, padx=20, sticky="nw")

# ---------- Color Customizer Tab ----------

color_frame = create_scrollable_tab(notebook, "Color Customizer")

Label(color_frame, text="Background Color:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
bg_color_entry = Entry(color_frame)
bg_color_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

def choose_bg_color():
    color = colorchooser.askcolor()[1]
    if color:
        bg_color_entry.delete(0, END)
        bg_color_entry.insert(0, color)

Button(color_frame, text="Choose Background Color", command=choose_bg_color).grid(row=0, column=2, sticky="nw", padx=20)

Label(color_frame, text="Foreground Color:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
fg_color_entry = Entry(color_frame)
fg_color_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

def choose_fg_color():
    color = colorchooser.askcolor()[1]
    if color:
        fg_color_entry.delete(0, END)
        fg_color_entry.insert(0, color)

Button(color_frame, text="Choose Foreground Color", command=choose_fg_color).grid(row=1, column=2, sticky="nw", padx=20)

def change_color():
    global current_widget
    if current_widget is None:
        return

    bg_color = bg_color_entry.get()
    fg_color = fg_color_entry.get()

    try:
        if bg_color:
            current_widget.configure(bg=bg_color)
    except:
        pass

    try:
        if fg_color:
            current_widget.configure(fg=fg_color)
    except:
        pass

Button(color_frame, text="Change Color", command=change_color).grid(row=2, column=2, rowspan=2, padx=20, sticky="nw")

# ---------- Image Customizer Tab ----------

image_frame = create_scrollable_tab(notebook, "Image Customizer")

Label(image_frame, text="Paste Image File Path:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
image_path_entry = Entry(image_frame)
image_path_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

def browse_image_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")]
    )
    if file_path:
        image_path_entry.delete(0, END)
        image_path_entry.insert(0, file_path)

Button(image_frame, text="Browse...", command=browse_image_file).grid(row=0, column=2, sticky="nw", padx=20)

Label(image_frame, text="Resize Width:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
resize_width_entry = Entry(image_frame)
resize_width_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

Label(image_frame, text="Resize Height:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
resize_height_entry = Entry(image_frame)
resize_height_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

Label(image_frame, text="Compound Option:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
compound_var = StringVar(value="none")
compound_options = ["none", "top", "bottom", "left", "right", "center"]
compound_dropdown = ttk.Combobox(image_frame, textvariable=compound_var, values=compound_options)
compound_dropdown.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

def change_image():
    global current_widget, current_image
    path = image_path_entry.get()

    try:
        img = Image.open(path)

        width = resize_width_entry.get()
        height = resize_height_entry.get()
        if width and height:
            img = img.resize((int(width), int(height)))
        else:
            img.thumbnail((300, 300))

        img_tk = ImageTk.PhotoImage(img)

        if isinstance(current_widget, (Label, Button, Checkbutton, Radiobutton)):
            current_widget.configure(image=img_tk, compound=compound_var.get())
            current_widget.image = img_tk
            current_image = img_tk
        else:
            print("Current widget does not support images.")

    except Exception as e:
        print("Error loading image:", e)

Button(image_frame, text="Change Image", command=change_image).grid(row=1, column=2, rowspan=2, padx=20, sticky="nw")

# ---------- Run App ----------
window.mainloop()

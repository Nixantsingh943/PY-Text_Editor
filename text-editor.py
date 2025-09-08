import tkinter as tk
from tkinter import filedialog, messagebox, font, colorchooser

# ----------------- Functions -----------------
def new_file():
    text_area.delete(1.0, tk.END)
    root.title("Untitled - Text Editor")

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "r") as f:
            content = f.read()
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, content)
        root.title(f"{file_path} - Text Editor")

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=[("Text Files", "*.txt")])
    if file_path:
        try:
            with open(file_path, "w") as f:
                f.write(text_area.get(1.0, tk.END))
            messagebox.showinfo("Saved", "File saved successfully!")
            root.title(f"{file_path} - Text Editor")
        except Exception as e:
            messagebox.showerror("Error", str(e))

def toggle_bold():
    try:
        current_tags = text_area.tag_names("sel.first")
        if "bold" in current_tags:
            text_area.tag_remove("bold", "sel.first", "sel.last")
        else:
            text_area.tag_add("bold", "sel.first", "sel.last")
    except tk.TclError:
        messagebox.showwarning("No text selected", "Please select text to make it bold.")

def toggle_italic():
    try:
        current_tags = text_area.tag_names("sel.first")
        if "italic" in current_tags:
            text_area.tag_remove("italic", "sel.first", "sel.last")
        else:
            text_area.tag_add("italic", "sel.first", "sel.last")
    except tk.TclError:
        messagebox.showwarning("No text selected", "Please select text to make it italic.")

def toggle_underline():
    try:
        current_tags = text_area.tag_names("sel.first")
        if "underline" in current_tags:
            text_area.tag_remove("underline", "sel.first", "sel.last")
        else:
            text_area.tag_add("underline", "sel.first", "sel.last")
    except tk.TclError:
        messagebox.showwarning("No text selected", "Please select text to underline.")

def choose_text_color():
    color = colorchooser.askcolor()[1]
    if color:
        text_area.tag_add("colored", "sel.first", "sel.last")
        text_area.tag_configure("colored", foreground=color)

def change_bg_color():
    color = colorchooser.askcolor()[1]
    if color:
        text_area.config(bg=color)

def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode
    if dark_mode:
        text_area.config(bg="black", fg="white", insertbackground="white")
    else:
        text_area.config(bg="#fdf6e3", fg="black", insertbackground="black")

def change_font_size(event=None):
    size = font_size_var.get()
    text_area.config(font=("Arial", size))

def update_status(event=None):
    row, col = text_area.index(tk.INSERT).split(".")
    status_bar.config(text=f"Line: {row} | Column: {col}")

# ----------------- GUI Setup -----------------
root = tk.Tk()
root.title(" Text Editor")
root.geometry("800x600")
root.config(bg="#f0f0f0")

# Main Text Area (colorful background by default)
text_area = tk.Text(root, wrap="word", font=("Arial", 14), undo=True,
                    bg="#fdf6e3", fg="black", insertbackground="black")
text_area.pack(expand=True, fill="both")

# Font Styles
bold_font = font.Font(text_area, text_area.cget("font"))
bold_font.configure(weight="bold")
text_area.tag_configure("bold", font=bold_font)

italic_font = font.Font(text_area, text_area.cget("font"))
italic_font.configure(slant="italic")
text_area.tag_configure("italic", font=italic_font)

underline_font = font.Font(text_area, text_area.cget("font"))
underline_font.configure(underline=True)
text_area.tag_configure("underline", font=underline_font)

# ----------------- Toolbar -----------------
toolbar = tk.Frame(root, bg="#d9e6f2", height=40)
toolbar.pack(side="top", fill="x")

btn_bold = tk.Button(toolbar, text="B", command=toggle_bold, font=("Arial", 12, "bold"), width=3, bg="#ffcccc")
btn_bold.pack(side="left", padx=2, pady=2)

btn_italic = tk.Button(toolbar, text="I", command=toggle_italic, font=("Arial", 12, "italic"), width=3, bg="#ccffcc")
btn_italic.pack(side="left", padx=2, pady=2)

btn_underline = tk.Button(toolbar, text="U", command=toggle_underline, font=("Arial", 12, "underline"), width=3, bg="#ccccff")
btn_underline.pack(side="left", padx=2, pady=2)

btn_text_color = tk.Button(toolbar, text="🎨", command=choose_text_color, width=3, bg="#ffffcc")
btn_text_color.pack(side="left", padx=2, pady=2)

btn_bg_color = tk.Button(toolbar, text="🖌️", command=change_bg_color, width=3, bg="#e6ccff")
btn_bg_color.pack(side="left", padx=2, pady=2)

btn_theme = tk.Button(toolbar, text="🌙", command=toggle_theme, width=3, bg="#ffd9b3")
btn_theme.pack(side="left", padx=2, pady=2)

# Font size dropdown
font_size_var = tk.IntVar(value=14)
font_size_dropdown = tk.OptionMenu(toolbar, font_size_var, *list(range(8, 33)), command=change_font_size)
font_size_dropdown.pack(side="left", padx=5)

# ----------------- Menu Bar -----------------
menu_bar = tk.Menu(root)

# File Menu
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
menu_bar.add_cascade(label="File", menu=file_menu)

root.config(menu=menu_bar)

# ----------------- Status Bar -----------------
status_bar = tk.Label(root, text="Line: 1 | Column: 0", anchor="e", bg="#f0f0f0")
status_bar.pack(side="bottom", fill="x")

text_area.bind("<KeyRelease>", update_status)
text_area.bind("<ButtonRelease>", update_status)

# ----------------- Run App -----------------
dark_mode = False
root.mainloop()

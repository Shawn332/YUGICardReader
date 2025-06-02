import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

def open_file_dialog():
    filetypes = (
        ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif"),
        ("All files", "*.*")
    )
    
    filepath = filedialog.askopenfilename(
        title="Select an Image",
        initialdir="/",
        filetypes=filetypes
    )
    
    if filepath:
        selected_file_label.config(text=f"Selected File: {filepath}")
        load_image(filepath)
    else:
        messagebox.showinfo("No Selection", "No file selected.")

def load_image(filepath):
    global img, tk_img
    img = Image.open(filepath)
    tk_img = ImageTk.PhotoImage(img)
    canvas.config(width=tk_img.width(), height=tk_img.height())
    canvas.create_image(0, 0, anchor="nw", image=tk_img)

def on_mouse_down(event):
    global start_x, start_y
    start_x, start_y = event.x, event.y
    canvas.delete("selection")

def on_mouse_drag(event):
    global start_x, start_y, rect
    if rect:
        canvas.delete(rect)
    rect = canvas.create_rectangle(start_x, start_y, event.x, event.y, outline="red")

def on_mouse_up(event):
    global start_x, start_y, rect
    end_x, end_y = event.x, event.y
    if rect:
        canvas.delete(rect)
    canvas.create_rectangle(start_x, start_y, end_x, end_y, outline="red")
    selected_area_label.config(text=f"Selected Area: ({start_x}, {start_y}) to ({end_x}, {end_y})")

# Create the main window
root = tk.Tk()
root.title("Image File Dialog Example")
root.geometry("800x600")

# Create and place the open button
open_button = tk.Button(root, text="Open Image", command=open_file_dialog)
open_button.pack(pady=20)

# Create and place the label to show the selected file path
selected_file_label = tk.Label(root, text="Selected File: None")
selected_file_label.pack(pady=10)

# Create and place the label to show the selected area coordinates
selected_area_label = tk.Label(root, text="Selected Area: None")
selected_area_label.pack(pady=10)

# Create a canvas to display the image
canvas = tk.Canvas(root)
canvas.pack()

# Bind mouse events to the canvas
canvas.bind("<ButtonPress-1>", on_mouse_down)
canvas.bind("<B1-Motion>", on_mouse_drag)
canvas.bind("<ButtonRelease-1>", on_mouse_up)

# Initialize global variables
img = None
tk_img = None
start_x = start_y = 0
rect = None

# Run the main event loop
root.mainloop()

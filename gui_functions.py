import tkinter as tk
from tkinter import ttk, simpledialog, colorchooser
import win32gui

# Global variables for selected area and font settings
selected_area = None
desc_font = ("Times New Roman", 12)
desc_font_color = "#000000"
capture_frequency = 1.0
hotkeys = {
    "start": "F1",
    "stop": "F2",
    "report": "F3"
}

# Function to update GUI
def update_gui(details, description, card_details_label, card_desc_label):
    card_details_label.config(state=tk.NORMAL)
    card_details_label.delete(1.0, tk.END)
    card_details_label.insert(1.0, details)
    card_details_label.config(state=tk.DISABLED)

    card_desc_label.config(state=tk.NORMAL)
    card_desc_label.delete(1.0, tk.END)
    card_desc_label.insert(1.0, description)
    card_desc_label.config(state=tk.DISABLED)

# Function to change description font
def change_desc_font(root, card_details_label, card_desc_label):
    def update_font():
        global desc_font, desc_font_color
        selected_font = font_family_var.get()
        font_size = font_size_var.get()
        if selected_font and font_size.isdigit():
            desc_font = (selected_font, int(font_size))
            card_details_label.config(font=desc_font, fg=desc_font_color)
            card_desc_label.config(font=desc_font, fg=desc_font_color)

    def change_color():
        global desc_font_color
        color = colorchooser.askcolor()[1]
        if color:
            desc_font_color = color
            card_details_label.config(fg=desc_font_color)
            card_desc_label.config(fg=desc_font_color)

    font_window = tk.Toplevel(root)
    font_window.title("Change Font")

    tk.Label(font_window, text="Font Family:").pack(padx=10, pady=5)
    font_family_var = tk.StringVar(value=desc_font[0])
    font_families = list(tk.font.families())
    font_family_menu = ttk.Combobox(font_window, textvariable=font_family_var, values=font_families)
    font_family_menu.pack(padx=10, pady=5)

    tk.Label(font_window, text="Font Size:").pack(padx=10, pady=5)
    font_size_var = tk.StringVar(value=str(desc_font[1]))
    tk.Entry(font_window, textvariable=font_size_var).pack(padx=10, pady=5)

    tk.Button(font_window, text="+", command=lambda: font_size_var.set(str(int(font_size_var.get()) + 1))).pack(side=tk.LEFT, padx=5)
    tk.Button(font_window, text="-", command=lambda: font_size_var.set(str(int(font_size_var.get()) - 1))).pack(side=tk.LEFT, padx=5)

    tk.Label(font_window, text="Font Color:").pack(padx=10, pady=5)
    tk.Button(font_window, text="Change Color", command=change_color).pack(padx=10, pady=5)

    tk.Button(font_window, text="Apply", command=update_font).pack(padx=10, pady=10)

# Function to change processing frequency
def change_processing_frequency():
    global capture_frequency
    try:
        new_frequency = simpledialog.askfloat("Change Processing Frequency", "Enter the new frequency in seconds:", minvalue=0.1, maxvalue=10.0)
        if new_frequency is not None:
            capture_frequency = new_frequency
            print(f"Processing frequency updated to {capture_frequency} seconds.")  # Optional: for debugging or user feedback
    except ValueError:
        print("Invalid input. Please enter a numeric value.")  # Optional: error handling for non-numeric input

# Function to set the selected area
def set_area(area, status_label):
    """Set the area and update status label without using global."""
    status_label.config(text=f"Status: Not Running | Area: {area}")
    print(f"Selected area: {area}")  # For debugging
    return area  # Return the area so it can be captured where this function is called

# Function to modify hotkeys
def change_hotkeys(root):
    def update_hotkey(action):
        new_hotkey = simpledialog.askstring("Change Hotkey", f"Enter new hotkey for {action}:", initialvalue=hotkeys[action])
        if new_hotkey:
            hotkeys[action] = new_hotkey
            hotkey_labels[action].config(text=f"{action.capitalize()}: {hotkeys[action]}")

    hotkey_window = tk.Toplevel(root)
    hotkey_window.title("Change Hotkeys")

    hotkey_labels = {}
    for action in hotkeys:
        frame = tk.Frame(hotkey_window)
        frame.pack(padx=10, pady=5, fill=tk.X)
        label = tk.Label(frame, text=f"{action.capitalize()}: {hotkeys[action]}")
        label.pack(side=tk.LEFT, padx=10)
        hotkey_labels[action] = label
        button = tk.Button(frame, text="Change", command=lambda a=action: update_hotkey(a))
        button.pack(side=tk.RIGHT, padx=10)

# Function to stick the window to the right of the masterduel window and set initial width
def stick_to_masterduel(root):
    hwnd = win32gui.FindWindow(None, 'masterduel')
    if hwnd:
        masterduel_rect = win32gui.GetWindowRect(hwnd)
        x = masterduel_rect[2]  # Right edge of masterduel window
        y = masterduel_rect[1]  # Top edge of masterduel window
        root.geometry(f"400x800+{x}+{y}")  # Set initial width to 400
    root.after(1000, lambda: stick_to_masterduel(root))  # Check every second

# Function to set initial window size (width and height)
def set_initial_window_size(root, width, height):
    root.geometry(f"{width}x{height}")

# Example usage in the main script
if __name__ == "__main__":
    root = tk.Tk()
    set_initial_window_size(root, 400, 800)
    stick_to_masterduel(root)
    root.mainloop()

import json
import time
import threading
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox, font, colorchooser
from tkinter.scrolledtext import ScrolledText
from card_database import open_card_database
from gui_functions import change_desc_font, update_gui, change_processing_frequency, stick_to_masterduel, change_hotkeys
from image_processing import screenshot, get_hash_from_area, find_closest_hash, hash_values, cids
from card_data import load_card_data, load_hash_data, format_card_details
import numpy as np
import win32gui
import os
from PIL import Image, ImageTk
import Configure

# Prompt user for language selection
root = tk.Tk()
root.title("选择语言")
root.geometry("300x150")

def select_language():
    selected_language = language_var.get()
    if selected_language in Configure.LANGUAGES:
        Configure.set_language(selected_language)
        root.destroy()
    else:
        messagebox.showerror("错误", "无效的语言选择。")

tk.Label(root, text="请选择语言", font=("Arial", 12)).pack(pady=10)

language_var = tk.StringVar(value="English")
language_menu = ttk.Combobox(root, textvariable=language_var, values=list(Configure.LANGUAGES.keys()), state="readonly")
language_menu.pack(pady=10)

select_button = tk.Button(root, text="确认", command=select_language)
select_button.pack(pady=10)

root.mainloop()

# Load JSON data
def load_breakpoint_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)

card_data = load_card_data("D:/Yu-Gi-Oh MD/Card Reader/Database/card_data.json")
hash_data = load_hash_data("D:/Yu-Gi-Oh MD/Card Reader/Database/hash.json")
breakpoint_data = load_breakpoint_data("D:/Yu-Gi-Oh MD/Card Reader/Database/breakpoint.json")

# Ensure hash_data is in the correct format
hash_data = [[entry[0], int(entry[1])] for entry in hash_data]

# Define global variables
breakpoint_window = None
capture_frequency = 1.0
is_running = False
selected_area = None
previous_image_hash = None
current_cid = None
current_hash = None
desc_font = ("Times New Roman", 12)
desc_font_color = "#000000"
stop_event = threading.Event()

# Define BOXES and other constants
BOXES = {
    "box1": (55, 159, 126, 231),  # Deck
    "box2": (40, 178, 117, 255),  # Duel1
    "box3": (104, 663, 249, 710),  # MyLP
    "box4": (1018, 35, 1171, 82),  # OpponentLP
    "box5": (340, 146, 840, 421),  # Main Deck
    "box6": (340, 526, 842, 662),  # Extra Deck
    "box7": (882, 215, 1230, 668),  # Card List
    "box8": (962, 470, 1042, 551),  # Grave
    "box9": (984, 392, 1054, 456),  # Upper Grave
    "box10": (341, 591, 952, 714),  # Hand 
    "box11": (1180, 128, 1264, 634),  # Grave Card List
    "box12": (139, 234, 269, 298),  # Breakpoint
}

def get_master_duel_window_position():
    hwnd = win32gui.FindWindow(None, "masterduel")
    if hwnd:
        rect = win32gui.GetWindowRect(hwnd)
        return rect
    return None

def set_area(area):
    global selected_area, is_running
    selected_area = area
    if is_running:
        status_label.config(text=f"{Configure.get_text('status_running')}{selected_area}")
    else:
        status_label.config(text=Configure.get_text('status_not_running'))
    print(f"Selected area: {selected_area}")  # For debugging

def start_processing():
    global thread, is_running, selected_area, stop_event
    if not is_running:
        if selected_area:
            stop_event.clear()
            is_running = True
            thread = threading.Thread(target=capture_and_process)
            thread.daemon = True  # Set the thread as a daemon
            thread.start()
            status_label.config(text=f"{Configure.get_text('status_running')}{selected_area}")
        else:
            messagebox.showinfo(Configure.get_text('error'), Configure.get_text('no_area_selected'))
    else:
        messagebox.showinfo(Configure.get_text('information'), "Processing is already active.")

def stop_processing():
    global is_running
    if is_running:
        is_running = False
        update_gui("", "", card_details_label, card_desc_label)
        card_name_label.config(text="")
        status_label.config(text=Configure.get_text('status_not_running'))
        hide_tier_popup()
        messagebox.showinfo(Configure.get_text('information'), "Processing has been stopped.")

def capture_and_process():
    global is_running, previous_image_hash, current_cid, current_hash
    is_running = True

    # Start the popup updater thread
    threading.Thread(target=update_popup_position, daemon=True).start()

    while is_running:
        full_img, box = screenshot()
        if full_img is None:
            root.title(Configure.get_text("title") + " - " + Configure.get_text("no_area_selected"))
            update_gui("", "", card_details_label, card_desc_label)
            card_name_label.config(text="")
            status_label.config(text=Configure.get_text('status_not_running'))
            hide_tier_popup()
            time.sleep(1)
            continue

        root.title(Configure.get_text("title"))
        if selected_area == "deck":
            card_hash = get_hash_from_area(full_img.crop(BOXES['box1']))
        elif selected_area == "duel":
            card_hash = get_hash_from_area(full_img.crop(BOXES['box2']))
        else:
            update_gui(Configure.get_text('no_area_selected'), "", card_details_label, card_desc_label)
            card_name_label.config(text="")
            status_label.config(text=f"{Configure.get_text('status_running')}{Configure.get_text('no_area_selected')}")
            hide_tier_popup()
            time.sleep(capture_frequency)
            continue

        if not is_running:
            break  # Exit the loop if is_running is False

        # Check if the hash value is the same as the previous one
        if previous_image_hash is not None and np.array_equal(card_hash, previous_image_hash):
            time.sleep(capture_frequency)
            continue  # Skip matching and continue to the next iteration

        previous_image_hash = card_hash  # Update the previous hash value

        cid, distance = find_closest_hash(card_hash, hash_values, cids)
        current_cid = cid
        current_hash = card_hash  # Ensure current_hash is set here

        if cid:
            details, description = format_card_details(cid, card_data)
            update_gui(details, description, card_details_label, card_desc_label)
            card_name_label.config(text=card_data[str(cid)]['en_name'])

            # Display tier value or '无断点' in a popup window
            if selected_area == "duel":
                if str(cid) in breakpoint_data:
                    tier = get_tier_description(breakpoint_data[str(cid)]['tier'])
                else:
                    tier = "无断点"
                show_tier_popup(tier)
            else:
                hide_tier_popup()
        else:
            update_gui(Configure.get_text('no_area_selected'), "", card_details_label, card_desc_label)
            card_name_label.config(text="")
            hide_tier_popup()

        status_label.config(text=f"{Configure.get_text('status_running')}{selected_area}")
        time.sleep(capture_frequency)

def update_popup_position():
    """Continuously update the popup window's position."""
    if is_running:
        master_duel_rect = get_master_duel_window_position()
        if master_duel_rect and breakpoint_window and breakpoint_window.winfo_exists():
            master_duel_x, master_duel_y, _, _ = master_duel_rect
            box12_x1, box12_y1, box12_x2, box12_y2 = BOXES['box12']
            popup_x = master_duel_x + box12_x1
            popup_y = master_duel_y + box12_y1
            popup_width = box12_x2 - box12_x1
            popup_height = box12_y2 - box12_y1
            breakpoint_window.geometry(f"{popup_width}x{popup_height}+{popup_x}+{popup_y}")
        root.after(100, update_popup_position)  # Schedule the function to run again after 100ms

def show_tier_popup(tier):
    global breakpoint_window

    master_duel_rect = get_master_duel_window_position()
    if master_duel_rect is None:
        print("Yu-Gi-Oh! Master Duel window not found.")
        return

    master_duel_x, master_duel_y, _, _ = master_duel_rect
    box12_x1, box12_y1, box12_x2, box12_y2 = BOXES['box12']
    popup_x = master_duel_x + box12_x1
    popup_y = master_duel_y + box12_y1
    popup_width = box12_x2 - box12_x1
    popup_height = box12_y2 - box12_y1

    if breakpoint_window is None or not breakpoint_window.winfo_exists():
        # Create the window if it doesn't exist
        breakpoint_window = tk.Toplevel()
        breakpoint_window.overrideredirect(1)  # Remove window frame
        breakpoint_window.geometry(f"{popup_width}x{popup_height}+{popup_x}+{popup_y}")

        # Set transparent background
        breakpoint_window.wm_attributes('-transparentcolor', 'white')
        breakpoint_window.configure(bg='white')

        # Keep the window on top
        breakpoint_window.attributes('-topmost', True)

        # Create the label to display the tier information
        breakpoint_window.label = tk.Label(breakpoint_window, text="", font=("Times New Roman", 16, "bold"), bg='white', fg='black')
        breakpoint_window.label.pack(expand=True, fill='both')

    # Update the label text
    breakpoint_window.label.config(text=f"{tier}")
    # Update the window position to handle any movement of the Master Duel window
    breakpoint_window.geometry(f"{popup_width}x{popup_height}+{popup_x}+{popup_y}")

    # Schedule the position update
    root.after(100, update_popup_position)

def get_tier_description(tier_value):
    tier_descriptions = {
        99: "无效断点",
        98: "除外断点",
        97: "破坏断点",
    }
    return tier_descriptions.get(tier_value, "无效断点")

def hide_tier_popup():
    global breakpoint_window
    if breakpoint_window and breakpoint_window.winfo_exists():
        breakpoint_window.destroy()
        breakpoint_window = None

def report_incorrect_card():
    global current_cid, hash_data, current_hash
    if not current_cid:
        messagebox.showinfo(Configure.get_text('information'), Configure.get_text('no_card_detected'))
        return

    try:
        hash_string = generate_hash_string(current_hash)
    except Exception as e:
        messagebox.showinfo(Configure.get_text('error'), Configure.get_text('hash_string_error'))
        return

    # Create a new window for reporting the incorrect card
    report_window = tk.Toplevel()
    report_window.title(Configure.get_text('report'))

    # Search frame
    search_frame = tk.Frame(report_window)
    search_frame.pack(padx=10, pady=10)

    search_label = ttk.Label(search_frame, text=Configure.get_text('card_details'))
    search_label.pack(side=tk.LEFT)

    search_entry = ttk.Entry(search_frame)
    search_entry.pack(side=tk.LEFT, padx=5)

    search_button = ttk.Button(search_frame, text=Configure.get_text('report'), command=lambda: search_card_by_name(search_entry.get(), search_results_listbox))
    search_button.pack(side=tk.LEFT)

    # Listbox to display search results
    search_results_listbox = tk.Listbox(report_window)
    search_results_listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # CID entry frame
    cid_frame = tk.Frame(report_window)
    cid_frame.pack(padx=10, pady=10)

    cid_label = ttk.Label(cid_frame, text=Configure.get_text('card_details'))
    cid_label.pack(side=tk.LEFT)

    cid_entry = ttk.Entry(cid_frame)
    cid_entry.pack(side=tk.LEFT, padx=5)

    # Populate the CID entry when a card is selected from the search results
    search_results_listbox.bind("<<ListboxSelect>>", lambda event: fill_cid_from_selection(search_results_listbox, cid_entry))

    # Hash display frame
    hash_frame = tk.Frame(report_window)
    hash_frame.pack(padx=10, pady=10, fill=tk.X)

    hash_label = ttk.Label(hash_frame, text=Configure.get_text('card_details'))
    hash_label.pack(side=tk.LEFT)

    hash_text = tk.Text(hash_frame, height=1, wrap=tk.NONE)
    hash_text.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
    hash_text.insert(tk.END, hash_string)
    hash_text.config(state=tk.NORMAL)  # Make the text box read-only

    submit_button = ttk.Button(report_window, text=Configure.get_text('report'), command=lambda: submit_incorrect_card(cid_entry.get(), hash_string, report_window))
    submit_button.pack(padx=10, pady=10)

def generate_hash_string(hash_array):
    """Convert a NumPy hash array to a hexadecimal string."""
    return ''.join(format(x, '02x') for x in np.packbits(hash_array))

def search_card_by_name(search_query, search_results_listbox):
    search_results_listbox.delete(0, tk.END)
    for cid, card_info in card_data.items():
        if search_query.lower() in card_info['en_name'].lower():
            search_results_listbox.insert(tk.END, f"{cid} - {card_info['en_name']}")

def fill_cid_from_selection(search_results_listbox, cid_entry):
    selected_card = search_results_listbox.get(search_results_listbox.curselection())
    cid = selected_card.split(" - ")[0]
    cid_entry.delete(0, tk.END)
    cid_entry.insert(0, cid)

def submit_incorrect_card(new_cid, hash_string, report_window):
    global hash_data, current_cid, current_hash
    try:
        new_cid = int(new_cid)
    except ValueError:
        messagebox.showinfo(Configure.get_text('error'), "CID must be an integer.")
        return

    if str(new_cid) not in card_data:
        messagebox.showinfo(Configure.get_text('error'), "The entered CID does not exist in the card database.")
        return

    new_entry = [hash_string, new_cid]
    updated = False
    for index, (hash_value, cid) in enumerate(hash_data):
        if hash_value == hash_string:
            hash_data[index] = new_entry
            updated = True
            break
    if not updated:
        hash_data.append(new_entry)

    try:
        with open("D:/Yu-Gi-Oh MD/Card Reader/Database/hash.json", "w", encoding="utf-8") as f:
            json.dump(hash_data, f, ensure_ascii=False, indent=4)
        messagebox.showinfo(Configure.get_text('information'), f"Updated hash for card {new_cid}.")
        report_window.destroy()

        # Reload hash data
        hash_data = load_hash_data("D:/Yu-Gi-Oh MD/Card Reader/Database/hash.json")

        # Re-process the image to update the displayed card information
        if current_hash is not None:
            cid, distance = find_closest_hash(current_hash, hash_data)
            if cid:
                details, description = format_card_details(cid, card_data)
                update_gui(details, description, card_details_label, card_desc_label)
                card_name_label.config(text=card_data[str(cid)]['en_name'])
            else:
                update_gui(Configure.get_text('no_area_selected'), "", card_details_label, card_desc_label)
                card_name_label.config(text="")
    except Exception as e:
        messagebox.showinfo(Configure.get_text('error'), "Failed to save updated hash data.")

def change_language():
    selected_language = simpledialog.askstring(Configure.get_text('change_language'), "Enter the language (English/Chinese):")
    if selected_language in Configure.LANGUAGES:
        Configure.set_language(selected_language)
        update_language()

def update_language():
    root.title(Configure.get_text('title'))
    area_button.config(text=Configure.get_text('select_area'))
    area_menu.entryconfig(0, label=Configure.get_text('deck_area'))
    area_menu.entryconfig(1, label=Configure.get_text('duel_area'))
    settings_button.config(text=Configure.get_text('settings'))
    settings_menu.entryconfig(0, label=Configure.get_text('change_font'))
    settings_menu.entryconfig(1, label=Configure.get_text('change_frequency'))
    settings_menu.entryconfig(2, label=Configure.get_text('change_hotkeys'))
    settings_menu.entryconfig(3, label=Configure.get_text('change_language'))
    start_button.config(text=Configure.get_text('start'))
    stop_button.config(text=Configure.get_text('stop'))
    report_button.config(text=Configure.get_text('report'))
    status_label.config(text=Configure.get_text('status_not_running'))

# Tkinter GUI setup
root = tk.Tk()
root.title(Configure.get_text('title'))

# Create a notebook for tabbed interface
notebook = ttk.Notebook(root)
notebook.pack(expand=1, fill='both')

# Create frames for the tabs
card_reader_frame = ttk.Frame(notebook)

# Add frames to the notebook
notebook.add(card_reader_frame, text=Configure.get_text('card_details'))

# Card Reader Tab
button_frame = tk.Frame(card_reader_frame)
button_frame.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)

area_button = ttk.Menubutton(button_frame, text=Configure.get_text('select_area'))
area_menu = tk.Menu(area_button, tearoff=0)
area_button["menu"] = area_menu
area_menu.add_command(label=Configure.get_text('deck_area'), command=lambda: set_area("deck"))
area_menu.add_command(label=Configure.get_text('duel_area'), command=lambda: set_area("duel"))
area_button.pack(side=tk.LEFT, padx=2, pady=2)

settings_button = ttk.Menubutton(button_frame, text=Configure.get_text('settings'))
settings_menu = tk.Menu(settings_button, tearoff=0)
settings_button["menu"] = settings_menu
settings_menu.add_command(label=Configure.get_text('change_font'), command=lambda: change_desc_font(root, card_details_label, card_desc_label))
settings_menu.add_command(label=Configure.get_text('change_frequency'), command=change_processing_frequency)
settings_menu.add_command(label=Configure.get_text('change_hotkeys'), command=lambda: change_hotkeys(root))
settings_menu.add_command(label=Configure.get_text('change_language'), command=change_language)
settings_button.pack(side=tk.LEFT, padx=2, pady=2)

start_button = ttk.Button(button_frame, text=Configure.get_text('start'), command=start_processing)
start_button.pack(side=tk.LEFT, padx=2, pady=2)

stop_button = ttk.Button(button_frame, text=Configure.get_text('stop'), command=stop_processing)
stop_button.pack(side=tk.LEFT, padx=2, pady=2)

report_button = ttk.Button(button_frame, text=Configure.get_text('report'), command=report_incorrect_card)
report_button.pack(side=tk.LEFT, padx=2, pady=2)

card_name_label = ttk.Label(card_reader_frame, text="", font=("Times New Roman", 12))
card_name_label.pack(padx=10, pady=5)

card_details_label = ScrolledText(card_reader_frame, wrap=tk.WORD, width=40, height=10, state=tk.DISABLED)
card_details_label.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

card_desc_label = ScrolledText(card_reader_frame, wrap=tk.WORD, width=40, height=10, state=tk.DISABLED, font=desc_font, fg=desc_font_color)
card_desc_label.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

status_label = ttk.Label(root, text=Configure.get_text('status_not_running'))
status_label.pack(side=tk.BOTTOM, pady=5)

stick_to_masterduel(root)

root.mainloop()

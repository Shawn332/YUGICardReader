import tkinter as tk
from tkinter import ttk, messagebox
from card_data import load_card_data

# Ensure card_data is loaded correctly
card_data = load_card_data("D:/Yu-Gi-Oh MD/Card Reader/Database/card_data.json")
deck_cache = {}
def open_card_database(selected_deck, main_card_list_text, extra_card_list_text, display_deck_cards_callback):
    if not selected_deck:
        messagebox.showinfo("Information", "Please select a deck before adding a card.")
        return

    card_database_window = tk.Toplevel()
    card_database_window.title("Card Database")
    card_database_window.attributes('-topmost', True)  # Make the window prioritized

    search_frame = tk.Frame(card_database_window)
    search_frame.pack(padx=10, pady=10)

    search_label = ttk.Label(search_frame, text="Search:")
    search_label.pack(side=tk.LEFT)

    search_entry = ttk.Entry(search_frame)
    search_entry.pack(side=tk.LEFT, padx=5)

    search_button = ttk.Button(search_frame, text="Search", command=lambda: search_cards(search_entry.get(), card_listbox))
    search_button.pack(side=tk.LEFT)

    card_listbox = tk.Listbox(card_database_window)
    card_listbox.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

    deck_var = tk.StringVar(value="main")
    main_deck_radio = ttk.Radiobutton(card_database_window, text="Main Deck", variable=deck_var, value="main")
    main_deck_radio.pack(padx=10, pady=5)

    extra_deck_radio = ttk.Radiobutton(card_database_window, text="Extra Deck", variable=deck_var, value="extra")
    extra_deck_radio.pack(padx=10, pady=5)

    add_button = ttk.Button(card_database_window, text="Add Card", command=lambda: add_selected_card(card_listbox, deck_var.get(), selected_deck, main_card_list_text, extra_card_list_text, display_deck_cards_callback))
    add_button.pack(padx=10, pady=10)

def search_cards(query, card_listbox):
    # Clear the listbox
    card_listbox.delete(0, tk.END)

    # Search for cards matching the query
    for cid, card_info in card_data.items():
        if query.lower() in card_info['en_name'].lower() or str(cid) == query:
            card_listbox.insert(tk.END, f"{cid} - {card_info['en_name']}")

def populate_card_database(card_listbox, card_data):
    # Clear the listbox
    card_listbox.delete(0, tk.END)

    # Populate the listbox with all cards
    for cid, card_info in card_data.items():
        card_listbox.insert(tk.END, f"{cid} - {card_info['en_name']}")

def add_selected_card(card_listbox, deck_type, selected_deck, main_card_list_text, extra_card_list_text, display_deck_cards_callback):
    if not card_listbox.curselection():
        messagebox.showinfo("Information", "Please select a card to add.")
        return

    selected_card = card_listbox.get(card_listbox.curselection())
    cid, card_name = selected_card.split(' - ', 1)
    cid = int(cid)

    if selected_deck in deck_cache:
        deck_data = deck_cache[selected_deck]
        card_info = {
            "name": card_name,
            "cid": cid,
            "type": card_data[str(cid)]['type']
        }
        deck_data[deck_type].append(card_info)

    if deck_type == "main":
        main_card_list_text.insert(tk.END, card_name + "\n")
    else:
        extra_card_list_text.insert(tk.END, card_name + "\n")

    messagebox.showinfo("Information", "Card added successfully.")
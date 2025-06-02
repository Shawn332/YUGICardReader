import os
from PIL import Image
import imagehash  # Import ImageHash library for aHash
import json
from tkinter import Tk, Label, Button, Text, Scrollbar, LEFT, BOTH, END, Y, RIGHT

def calculate_hash(image_path, crop_box):
    try:
        with Image.open(image_path) as img:
            img = img.crop(crop_box)  # Crop the image to the specified box
            return imagehash.average_hash(img)  # Compute aHash
    except Exception as e:
        print(f"Error processing image: {image_path}")
        print(f"Error message: {str(e)}")
        return None

class ProgressWindow(Tk):
    def __init__(self):
        super().__init__()
        self.title("Hash Progress")
        self.geometry("400x300")
        
        self.progress_label = Label(self, text="Processing images...")
        self.progress_label.pack()
        
        self.progress_text = Text(self, wrap="word")
        self.progress_text.pack(side=LEFT, fill=BOTH, expand=True)
        
        self.scrollbar = Scrollbar(self, command=self.progress_text.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        
        self.progress_text.config(yscrollcommand=self.scrollbar.set)
        
        self.close_button = Button(self, text="Close", command=self.destroy)
        self.close_button.pack()
    
    def update_progress(self, message):
        self.progress_text.insert(END, message + "\n")
        self.progress_text.see(END)
        self.update()

def process_folders(progress_window, base_dir, folders, crop_box):
    hashes = []
    for folder in folders:
        folder_path = os.path.join(base_dir, folder)
        if os.path.isdir(folder_path):
            for filename in os.listdir(folder_path):
                if filename.endswith(".jpg") or filename.endswith(".png"):
                    image_path = os.path.join(folder_path, filename)
                    hash_value = calculate_hash(image_path, crop_box)
                    if hash_value is not None:
                        cid = int(os.path.splitext(filename)[0])  # Extract the numeric part of the filename as CID
                        hashes.append([str(hash_value), cid])  # Convert hash to string
                        progress_window.update_progress(f"Processed image: {filename}")
    return hashes

def save_hashes_to_file(hashes, output_file, progress_window):
    with open(output_file, 'w') as f:
        json.dump(hashes, f)
    progress_window.update_progress(f"Hashes saved to {output_file}")

if __name__ == '__main__':
    crop_box = (96, 215, 717, 838)  # Updated coordinates based on your specific images
    base_dir = "D:\\Yu-Gi-Oh MD\\Card Reader\\Database\\Image"
    folders = ["folder_1", "folder_2", "folder_3", "folder_4", "folder_5"]
    output_file = "hash.json"

    progress_window = ProgressWindow()
    hashes = process_folders(progress_window, base_dir, folders, crop_box)
    save_hashes_to_file(hashes, output_file, progress_window)
    progress_window.mainloop()

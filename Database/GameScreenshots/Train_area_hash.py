import os
from PIL import Image
import imagehash  # Import ImageHash library for aHash
import json
from tkinter import Tk, Label, Button, Text, Scrollbar, LEFT, BOTH, END, Y, RIGHT

def calculate_hash(image_path):
    try:
        with Image.open(image_path) as img:
            return imagehash.average_hash(img)  # Compute aHash for the entire image
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

def process_images_in_directory(progress_window, directory):
    hashes = []
    for filename in os.listdir(directory):
        if filename.endswith(".png"):
            image_path = os.path.join(directory, filename)
            hash_value = calculate_hash(image_path)
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
    directory = "D:\\Yu-Gi-Oh MD\\Card Reader\\Database\\Gamescreenshot\\Area"
    output_file = "area_hash.json"

    progress_window = ProgressWindow()
    hashes = process_images_in_directory(progress_window, directory)
    save_hashes_to_file(hashes, output_file, progress_window)
    progress_window.mainloop()

import os
import cv2
import numpy as np
from PIL import Image
import pytesseract

# Define constants
IMG_SIZE = (813, 1185)  # Updated image size
UPPER_SIZE = (813, 593)  # Size of the upper area (half of the original height)

# Step 2: Data Preparation
def load_images_from_folder(folder, img_size=UPPER_SIZE):
    images = []
    filenames = sorted([f for f in os.listdir(folder) if f.split('.')[0].isdigit()], key=lambda x: int(os.path.splitext(x)[0]))

    for filename in filenames:
        img_path = os.path.join(folder, filename)
        if os.path.isfile(img_path):
            img = cv2.imread(img_path)
            if img is not None:
                img = cv2.resize(img, IMG_SIZE)
                img = img[:UPPER_SIZE[1], :]  # Extract the upper area of the image
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                images.append(img)
            else:
                print(f"Warning: Unable to load image {img_path}")
    return images

# Step 3: Word Extraction
def extract_words_from_images(images):
    words = []
    for img in images:
        pil_img = Image.fromarray(img)
        word = pytesseract.image_to_string(pil_img, lang='eng', config='--psm 6')
        words.append(word.strip())
    return words

# Define the folder path for the first folder
folder_path = r'D:\Yu-Gi-Oh MD\AI\Image Re\md_hover-main\Database\Image\folder_1'

# Load images from the folder
images = load_images_from_folder(folder_path)

# Extract words from the images
words = extract_words_from_images(images)

# Print the extracted words
for i, word in enumerate(words):
    print(f"Image {i+1}: {word}")
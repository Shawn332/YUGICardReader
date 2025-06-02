from PIL import Image, ImageGrab
import win32gui
import win32con
import win32ui
from ctypes import windll
import imagehash
import numpy as np
from numba import njit
import json

# Function to load hash data
def load_hash_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

# Load hash data and convert to NumPy arrays
def initialize_hash_data(filepath):
    hash_data = load_hash_data(filepath)
    hash_values = np.array([imagehash.hex_to_hash(hash_pair[0]).hash.flatten() for hash_pair in hash_data])
    cids = np.array([hash_pair[1] for hash_pair in hash_data])
    return hash_values, cids

# Initialize hash data
hash_values, cids = initialize_hash_data("D:/Yu-Gi-Oh MD/Card Reader/Database/hash.json")

# Function to take screenshot
def screenshot():
    hwnd = win32gui.FindWindow(None, 'masterduel')
    if hwnd:
        box = win32gui.GetWindowRect(hwnd)
        box_w = box[2] - box[0]
        box_h = box[3] - box[1]
        hwnd_dc = win32gui.GetWindowDC(hwnd)
        mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
        save_dc = mfc_dc.CreateCompatibleDC()
        save_bitmap = win32ui.CreateBitmap()
        save_bitmap.CreateCompatibleBitmap(mfc_dc, box_w, box_h)
        save_dc.SelectObject(save_bitmap)
        result = windll.user32.PrintWindow(hwnd, save_dc.GetSafeHdc(), 3)
        bmpinfo = save_bitmap.GetInfo()
        bmpstr = save_bitmap.GetBitmapBits(True)
        im = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)
        win32gui.DeleteObject(save_bitmap.GetHandle())
        save_dc.DeleteDC()
        mfc_dc.DeleteDC()
        win32gui.ReleaseDC(hwnd, hwnd_dc)
        if result != 0:
            return im, box
    return None, None

# Function to generate hash from image
def generate_hash(image):
    return str(imagehash.average_hash(image))

# Function to get hash from area
def get_hash_from_area(image):
    image = image.convert('L')
    return np.array(imagehash.average_hash(image).hash.flatten())

@njit
def hamming_distance(hash1, hash2):
    return np.sum(hash1 != hash2)

@njit
def find_closest_hash(target_hash, hash_values, cids):
    min_distance = np.inf
    closest_cid = None
    for i in range(len(hash_values)):
        distance = hamming_distance(target_hash, hash_values[i])
        if distance < min_distance:
            min_distance = distance
            closest_cid = cids[i]
            if distance == 0:
                break
    return closest_cid, min_distance

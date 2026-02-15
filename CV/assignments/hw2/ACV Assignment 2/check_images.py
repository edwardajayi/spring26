import cv2
import os
import numpy as np

def check_image(filename):
    img = cv2.imread(filename)
    if img is None:
        print(f"Error reading {filename}")
        return

    is_white = np.all(img == 255)
    is_black = np.all(img == 0)
    
    unique_colors = np.unique(img.reshape(-1, img.shape[2]), axis=0)
    num_unique_colors = len(unique_colors)

    print(f"File: {filename}")
    print(f"  Shape: {img.shape}")
    print(f"  Is all white: {is_white}")
    print(f"  Is all black: {is_black}")
    print(f"  Unique colors count: {num_unique_colors}")
    if num_unique_colors < 10:
        print(f"  Unique colors: {unique_colors}")
    print("-" * 20)

files = [f for f in os.listdir('.') if f.endswith('.jpg') or f.endswith('.png')]
files.sort()

for f in files:
    check_image(f)

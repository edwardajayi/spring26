import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

def compress_image(image_path, keep_fraction=0.1):
    # 1. Load and Grayscale
    img = cv2.imread(image_path, 0) # Load directly as grayscale
    if img is None: 
        print(f"Error: Could not load image at {image_path}")
        return None
    
    # 2. Compute FFT
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    
    # 3. Thresholding
    # Calculate magnitude spectrum
    magnitude = np.abs(fshift)
    
    # Sort magnitude values to find threshold
    sorted_indices = np.sort(magnitude.flatten())
    # The index to threshold at. keep_fraction=0.1 means we keep top 10%
    thresh_index = int((1 - keep_fraction) * len(sorted_indices))
    threshold = sorted_indices[thresh_index]
    
    # Create a mask: 1 if magnitude > threshold, 0 otherwise
    # numpy boolean indexing
    mask = magnitude > threshold
    
    # Apply mask to the complex FFT coefficients
    fshift_filtered = fshift * mask
    
    # Count non-zero coefficients
    original_count = img.size
    compressed_count = np.sum(mask)
    compression_ratio = original_count / compressed_count
    print(f"Kept {compressed_count} of {original_count} coefficients. Ratio: {compression_ratio:.2f}:1")

    # 4. Inverse FFT
    f_ishift = np.fft.ifftshift(fshift_filtered)
    img_back = np.fft.ifft2(f_ishift)
    img_back = np.abs(img_back)
    
    # Save for Report
    os.makedirs('Assets', exist_ok=True)
    
    plt.figure(figsize=(15, 5))
    plt.subplot(1, 3, 1)
    plt.imshow(img, cmap='gray')
    plt.title("Original")
    plt.axis('off')
    
    plt.subplot(1, 3, 2)
    # Log transform for visualization of spectrum
    plt.imshow(20*np.log(magnitude + 1), cmap='gray')
    plt.title("Magnitude Spectrum")
    plt.axis('off')
    
    plt.subplot(1, 3, 3)
    plt.imshow(img_back, cmap='gray')
    plt.title(f"Compressed (Keep {keep_fraction*100:.1f}%)")
    plt.axis('off')
    
    plt.savefig('Assets/q3_compression.png')
    plt.show()
    
    return img_back

if __name__ == "__main__":
    pass

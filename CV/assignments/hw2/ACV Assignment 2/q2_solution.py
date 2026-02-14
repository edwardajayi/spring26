import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

def straighten_image(image_path):
    img = cv2.imread(image_path)
    if img is None: 
        print(f"Error: Could not load image at {image_path}")
        return None
    
    # 1. Grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 2. Blur & CLAHE
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(blurred)
    
    # 3. Edge Detection
    # Adjustable thresholds
    edges = cv2.Canny(enhanced, 50, 150)
    
    # 4. Hough Transform
    # rho=1 pixel resolution, theta=1 degree resolution, threshold=100 votes
    lines = cv2.HoughLines(edges, 1, np.pi/180, 150)
    
    if lines is None:
        print("No lines detected!")
        return None
        
    # 5. Analyze Angles
    angles = []
    for line in lines:
        rho, theta = line[0]
        # Convert theta (radians) to degrees
        angle = np.degrees(theta)
        # We care about deviation from horizontal/vertical
        # Normalize to -45 to 45 range
        if angle > 45 and angle <= 135:
            angle = angle - 90
        elif angle > 135:
            angle = angle - 180
            
        angles.append(angle)
    
    # Find median angle to be robust to outliers
    median_angle = np.median(angles)
    print(f"Detected Rotation Angle: {median_angle:.2f} degrees")
    
    # 6. Rotate
    (h, w) = img.shape[:2]
    center = (w // 2, h // 2)
    # Rotate by the negative of the detected angle to straighten
    M = cv2.getRotationMatrix2D(center, median_angle, 1.0)
    rotated = cv2.warpAffine(img, M, (w, h))
    
    # Save for Report
    os.makedirs('Assets', exist_ok=True)
    
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title("Original")
    plt.axis('off')
    
    plt.subplot(1, 2, 2)
    plt.imshow(cv2.cvtColor(rotated, cv2.COLOR_BGR2RGB))
    plt.title(f"Straightened ({median_angle:.2f} deg)")
    plt.axis('off')
    plt.savefig('Assets/q2_straightened.png')
    plt.show()
    
    return rotated

if __name__ == "__main__":
    # Test with a dummy path or user can run this
    pass

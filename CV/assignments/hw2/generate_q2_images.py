import cv2
import numpy as np
import os

def process_q2_all():
    image_names = ['2a.jpg', '2b.jpg', '2c.jpg', 'sat_img1.jpg']
    input_dir = 'ACV Assignment 2/q2_data'
    output_dir = 'ACV Assignment 2/Assets'
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for img_name in image_names:
        image_path = os.path.join(input_dir, img_name)
        base_name = os.path.splitext(img_name)[0]
        output_lines_path = os.path.join(output_dir, f'linesDetected_{base_name}.jpg')
        output_straight_path = os.path.join(output_dir, f'straightened_{base_name}.jpg')

        print(f"\n--- Processing {img_name} ---")
        img = cv2.imread(image_path)
        if img is None:
            print(f"Error: Could not read {image_path}")
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(blurred)
        edges = cv2.Canny(enhanced, 100, 200)
        lines = cv2.HoughLines(edges, 1, np.pi / 180, 300)

        img_lines = img.copy()
        angles_count = {}

        if lines is not None:
            print(f"Lines detected: {len(lines)}")
            for r_theta in lines:
                rho, theta = r_theta[0]
                angle_deg = int(np.degrees(theta))
                angles_count[angle_deg] = angles_count.get(angle_deg, 0) + 1
                
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a * rho
                y0 = b * rho
                x1 = int(x0 + 1000 * (-b))
                y1 = int(y0 + 1000 * (a))
                x2 = int(x0 - 1000 * (-b))
                y2 = int(y0 - 1000 * (a))
                cv2.line(img_lines, (x1, y1), (x2, y2), (0, 0, 255), 2)
        else:
            print(f"No lines detected with threshold 300")

        cv2.imwrite(output_lines_path, img_lines)

        if not angles_count:
            print("Skipping rotation.")
            continue

        # Print top 5 angles to debug
        sorted_angles = sorted(angles_count, key=angles_count.get, reverse=True)
        print(f"Top 5 angles (degrees): {sorted_angles[:5]}")
        
        best_angle = sorted_angles[0]
        print(f"Dominant Angle: {best_angle}")

        rotation_angle = 0
        if best_angle < 45:
            rotation_angle = -best_angle
        elif best_angle < 135:
            rotation_angle = 90 - best_angle
        else:
            rotation_angle = 180 - best_angle
        
        print(f"Applying Rotation: {rotation_angle} degrees")

        (h, w) = img.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, rotation_angle, 1.0)
        
        # Use CONSTANT border with GREEN color to make rotation obvious
        rotated = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_LINEAR, 
                                borderMode=cv2.BORDER_CONSTANT, 
                                borderValue=(0, 255, 0)) # Green border

        cv2.imwrite(output_straight_path, rotated)
        print(f"Saved {output_straight_path}")

if __name__ == "__main__":
    process_q2_all()

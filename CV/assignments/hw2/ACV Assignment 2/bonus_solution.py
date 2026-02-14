import cv2
import numpy as np
import os

def process_video(input_video_path, output_video_path):
    """
    Process video frame-by-frame using the naive object counting pipeline.
    Uses: Grayscale -> Blur -> Canny -> Contours (same as Q1).
    """
    cap = cv2.VideoCapture(input_video_path)
    
    if not cap.isOpened():
        print(f"Error: Could not open video file {input_video_path}")
        return

    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps    = cap.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    frame_count = 0
    
    print(f"Processing video: {input_video_path}")
    print(f"Resolution: {width}x{height}, FPS: {fps}")
    
    # Scale min_area relative to frame size
    # For 1920x1080, total pixels = ~2M. A real object should be at least 0.1% of the frame.
    total_pixels = width * height
    min_area = int(total_pixels * 0.005)  # 0.5% of frame = ~10000 pixels for 1080p
    print(f"Min contour area filter: {min_area} pixels")
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        frame_count += 1
        
        # --- Object Counting Pipeline (Same as Q1) ---
        
        # 1. Grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # 2. Gaussian Blur
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # 3. Canny Edge Detection
        edges = cv2.Canny(blurred, 30, 150)
        
        # 4. Dilate edges to close small gaps in object boundaries
        kernel = np.ones((3, 3), np.uint8)
        edges_dilated = cv2.dilate(edges, kernel, iterations=2)
        
        # 5. Find Contours
        contours, _ = cv2.findContours(edges_dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # 6. Filter by area — scaled to frame resolution
        valid_contours = [c for c in contours if cv2.contourArea(c) > min_area]
        
        count = len(valid_contours)
        
        # --- Visualization ---
        cv2.drawContours(frame, valid_contours, -1, (0, 255, 0), 2)
        
        text = f"Count: {count}"
        cv2.putText(frame, text, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 
                    3, (0, 0, 255), 5, cv2.LINE_AA)
        
        out.write(frame)
        
        if frame_count % 30 == 0:
            print(f"Frame {frame_count}: Count = {count}")

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"\nDone. {frame_count} frames processed. Saved to {output_video_path}")

if __name__ == "__main__":
    input_path = "three_objects_video.mp4"
    output_path = "Assets/bonus_output.mp4"
    
    os.makedirs('Assets', exist_ok=True)
    process_video(input_path, output_path)

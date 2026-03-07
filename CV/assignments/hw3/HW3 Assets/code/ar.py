import numpy as np
import cv2
#Import necessary functions only
from matchPics import matchPics
from planarH import computeH_ransac, compositeH

#Write script for Q4.1

# Load the reference book cover
cv_cover = cv2.imread('../data/cv_cover.jpg')
cover_h, cover_w = cv_cover.shape[:2]
print(f"Cover size: {cover_w} x {cover_h}")

# Open video streams
book_cap = cv2.VideoCapture('../data/book.mov')
ar_cap = cv2.VideoCapture('../data/ar_source.mov')

# Get video properties
book_fps = book_cap.get(cv2.CAP_PROP_FPS)
book_w = int(book_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
book_h = int(book_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
book_frames = int(book_cap.get(cv2.CAP_PROP_FRAME_COUNT))

ar_w = int(ar_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
ar_h = int(ar_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
ar_frames = int(ar_cap.get(cv2.CAP_PROP_FRAME_COUNT))

print(f"Book video: {book_w}x{book_h}, {book_fps} fps, {book_frames} frames")
print(f"AR source:  {ar_w}x{ar_h}, {ar_frames} frames")

# Setup output video writer
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('../results/ar.avi', fourcc, book_fps, (book_w, book_h))

# Compute aspect ratio of the book cover for cropping the AR source
cover_aspect = cover_w / cover_h  # width / height of cover

frame_count = 0
n_frames = min(book_frames, ar_frames)

while True:
    ret_book, book_frame = book_cap.read()
    ret_ar, ar_frame = ar_cap.read()
    
    if not ret_book or not ret_ar:
        break
    
    frame_count += 1
    
    # Crop the AR source frame to match the book cover's aspect ratio
    ar_frame_h, ar_frame_w = ar_frame.shape[:2]
    ar_aspect = ar_frame_w / ar_frame_h
    
    if ar_aspect > cover_aspect:
        # AR frame is wider: crop width
        new_w = int(ar_frame_h * cover_aspect)
        start_x = (ar_frame_w - new_w) // 2
        ar_cropped = ar_frame[:, start_x:start_x + new_w]
    else:
        # AR frame is taller: crop height
        new_h = int(ar_frame_w / cover_aspect)
        start_y = (ar_frame_h - new_h) // 2
        ar_cropped = ar_frame[start_y:start_y + new_h, :]
    
    # Resize cropped AR frame to match cover dimensions
    ar_resized = cv2.resize(ar_cropped, (cover_w, cover_h))
    
    # Match the book cover with the current book frame
    try:
        matches, locs1, locs2 = matchPics(cv_cover, book_frame)
        
        if len(matches) < 4:
            print(f"Frame {frame_count}: Not enough matches ({len(matches)}), skipping")
            out.write(book_frame)
            continue
        
        # Convert locs from [row, col] to [x, y]
        x1 = locs1[matches[:, 0]][:, [1, 0]]  # cover points
        x2 = locs2[matches[:, 1]][:, [1, 0]]  # book frame points
        
        # Compute homography: maps cover coords to book frame coords
        bestH2to1, inliers = computeH_ransac(x2, x1)
        
        if bestH2to1 is None:
            print(f"Frame {frame_count}: RANSAC failed, skipping")
            out.write(book_frame)
            continue
        
        # Composite: overlay the AR frame onto the book frame
        composite = compositeH(bestH2to1, ar_resized, book_frame)
        out.write(composite)
        
        if frame_count % 10 == 0:
            print(f"Frame {frame_count}/{n_frames}: {len(matches)} matches, {np.sum(inliers)} inliers")
    
    except Exception as e:
        print(f"Frame {frame_count}: Error - {e}, skipping")
        out.write(book_frame)
        continue

# Release everything
book_cap.release()
ar_cap.release()
out.release()
print(f"\nDone! Processed {frame_count} frames.")
print("Output saved to ../results/ar.avi")

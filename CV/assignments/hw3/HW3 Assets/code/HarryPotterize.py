import numpy as np
import cv2
import skimage.io 
import skimage.color
#Import necessary functions only
from matchPics import matchPics
from planarH import computeH_ransac, compositeH


#Write script for Q3.9

# Step 1: Read images
cv_cover = cv2.imread('../data/cv_cover.jpg')
cv_desk = cv2.imread('../data/cv_desk.png')
hp_cover = cv2.imread('../data/hp_cover.jpg')

print(f"cv_cover shape: {cv_cover.shape}")
print(f"cv_desk shape:  {cv_desk.shape}")
print(f"hp_cover shape: {hp_cover.shape}")

# Step 2: Compute homography automatically using matchPics and computeH_ransac
matches, locs1, locs2 = matchPics(cv_cover, cv_desk)
print(f"Number of matches: {len(matches)}")

# locs are in [row, col] = [y, x] format (skimage convention)
# For homography we need [x, y] format
x1 = locs1[matches[:, 0]][:, [1, 0]]  # cover points [x, y]
x2 = locs2[matches[:, 1]][:, [1, 0]]  # desk points [x, y]

# Compute homography from cover to desk
# H maps desk points to cover points: x_cover = H * x_desk
# But we need: x_desk = H_inv * x_cover, i.e. warp cover -> desk
bestH2to1, inliers = computeH_ransac(x2, x1)
print(f"Inliers: {np.sum(inliers)}/{len(matches)}")

# Step 3: Resize hp_cover to match the dimensions of cv_cover
# This fixes the aspect ratio mismatch
hp_cover_resized = cv2.resize(hp_cover, (cv_cover.shape[1], cv_cover.shape[0]))
print(f"hp_cover_resized shape: {hp_cover_resized.shape}")

# Step 5: Compose using compositeH
composite_img = compositeH(bestH2to1, hp_cover_resized, cv_desk)

# Save and display result
cv2.imwrite('../results/harrypotterize_result.png', composite_img)
print("Composite image saved to ../results/harrypotterize_result.png")

# Display
cv2.imshow('HarryPotterized', composite_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

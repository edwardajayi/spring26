import numpy as np
import cv2
#Import necessary functions only

def computeH(x1, x2):
	#Q3.6
	#Compute the homography between two sets of points
	# x1, x2 are N x 2 matrices of corresponding points
	# Returns H2to1: 3x3 homography matrix such that x1 ~ H * x2

	N = x1.shape[0]
	
	# Build the A matrix (2N x 9)
	A = np.zeros((2 * N, 9))
	for i in range(N):
		x2_i, y2_i = x2[i, 0], x2[i, 1]
		x1_i, y1_i = x1[i, 0], x1[i, 1]
		
		A[2*i]   = [-x2_i, -y2_i, -1,     0,     0,  0, x1_i*x2_i, x1_i*y2_i, x1_i]
		A[2*i+1] = [    0,     0,  0, -x2_i, -y2_i, -1, y1_i*x2_i, y1_i*y2_i, y1_i]
	
	# Solve using SVD
	U, S, Vt = np.linalg.svd(A)
	
	# The solution is the last row of Vt (last column of V)
	h = Vt[-1, :]
	H2to1 = h.reshape(3, 3)

	return H2to1


def computeH_norm(x1, x2):
	#Q3.7
	#Compute the centroid of the points
	mean1 = np.mean(x1, axis=0)
	mean2 = np.mean(x2, axis=0)

	#Shift the origin of the points to the centroid
	x1_shifted = x1 - mean1
	x2_shifted = x2 - mean2

	#Normalize the points so that the largest distance from the origin is equal to sqrt(2)
	max_dist1 = np.max(np.sqrt(np.sum(x1_shifted**2, axis=1)))
	max_dist2 = np.max(np.sqrt(np.sum(x2_shifted**2, axis=1)))
	
	# Avoid division by zero
	if max_dist1 == 0:
		max_dist1 = 1
	if max_dist2 == 0:
		max_dist2 = 1
	
	scale1 = np.sqrt(2) / max_dist1
	scale2 = np.sqrt(2) / max_dist2

	#Similarity transform 1
	T1 = np.array([
		[scale1,      0, -scale1 * mean1[0]],
		[     0, scale1, -scale1 * mean1[1]],
		[     0,      0,                  1]
	])

	#Similarity transform 2
	T2 = np.array([
		[scale2,      0, -scale2 * mean2[0]],
		[     0, scale2, -scale2 * mean2[1]],
		[     0,      0,                  1]
	])

	#Compute homography on normalized points
	x1_norm = (T1 @ np.hstack([x1, np.ones((x1.shape[0], 1))]).T).T[:, :2]
	x2_norm = (T2 @ np.hstack([x2, np.ones((x2.shape[0], 1))]).T).T[:, :2]
	
	H_norm = computeH(x1_norm, x2_norm)

	#Denormalization
	H2to1 = np.linalg.inv(T1) @ H_norm @ T2

	return H2to1




def computeH_ransac(x1, x2):
	#Q3.8
	#Compute the best fitting homography given a list of matching points
	
	N = x1.shape[0]
	max_iters = 1000
	tol = 5  # pixel threshold for inliers
	
	bestH2to1 = None
	best_inlier_count = 0
	inliers = np.zeros(N, dtype=int)
	
	# Convert to homogeneous coordinates for testing
	x1_h = np.hstack([x1, np.ones((N, 1))])  # N x 3
	x2_h = np.hstack([x2, np.ones((N, 1))])  # N x 3
	
	for _ in range(max_iters):
		# Randomly sample 4 point pairs
		idx = np.random.choice(N, 4, replace=False)
		
		# Compute homography from sample
		try:
			H = computeH_norm(x1[idx], x2[idx])
		except:
			continue
		
		# Transform all x2 points using H
		x2_transformed = (H @ x2_h.T).T  # N x 3
		
		# Convert from homogeneous to inhomogeneous
		# Avoid division by zero
		w = x2_transformed[:, 2:3]
		w[w == 0] = 1e-10
		x2_proj = x2_transformed[:, :2] / w
		
		# Compute distances
		dists = np.sqrt(np.sum((x1 - x2_proj)**2, axis=1))
		
		# Count inliers
		current_inliers = (dists < tol).astype(int)
		inlier_count = np.sum(current_inliers)
		
		if inlier_count > best_inlier_count:
			best_inlier_count = inlier_count
			bestH2to1 = H
			inliers = current_inliers
	
	# Recompute H using all inliers for better accuracy
	if best_inlier_count >= 4:
		inlier_mask = inliers.astype(bool)
		bestH2to1 = computeH_norm(x1[inlier_mask], x2[inlier_mask])
	
	print(f"RANSAC: {best_inlier_count}/{N} inliers")

	return bestH2to1, inliers



def compositeH(H2to1, template, img):
	
	#Create a composite image after warping the template image on top
	#of the image using the homography

	#Note that the homography we compute is from the image to the template;
	#x_template = H2to1*x_photo
	#For warping the template to the image, we need to invert it.
	H_inv = np.linalg.inv(H2to1)

	#Create mask of same size as template
	mask = np.ones(template.shape[:2], dtype=np.uint8) * 255

	#Warp mask by appropriate homography
	warped_mask = cv2.warpPerspective(mask, H_inv, (img.shape[1], img.shape[0]))

	#Warp template by appropriate homography
	warped_template = cv2.warpPerspective(template, H_inv, (img.shape[1], img.shape[0]))

	#Use mask to combine the warped template and the image
	# Where the mask is non-zero, use the warped template; otherwise, use the original image
	composite_img = img.copy()
	mask_bool = warped_mask > 0
	if len(composite_img.shape) == 3:
		for c in range(3):
			composite_img[:, :, c][mask_bool] = warped_template[:, :, c][mask_bool]
	else:
		composite_img[mask_bool] = warped_template[mask_bool]
	
	return composite_img



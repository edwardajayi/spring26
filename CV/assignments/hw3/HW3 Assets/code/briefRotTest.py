import numpy as np
import cv2
from matchPics import matchPics
from scipy.ndimage import rotate
import matplotlib.pyplot as plt
from helper import plotMatches


#Q3.5
#Read the image and convert to grayscale, if necessary, you can use OpenCV
cv_cover = cv2.imread('../data/cv_cover.jpg')

match_counts = []
angles = range(0, 360, 10)

for i, angle in enumerate(angles):
	#Rotate Image
	rotated = rotate(cv_cover, angle, reshape=False)
	rotated = rotated.astype(np.uint8)

	#Compute features, descriptors and Match features
	matches, locs1, locs2 = matchPics(cv_cover, rotated)

	#Update histogram
	match_counts.append(len(matches))
	print(f"Angle: {angle:3d}°  Matches: {len(matches)}")

	# Save visualizations for 3 orientations: 30, 90, 180 degrees
	if angle in [30, 90, 180]:
		fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(12, 5))
		im1_gray = cv2.cvtColor(cv_cover, cv2.COLOR_BGR2GRAY)
		im2_gray = cv2.cvtColor(rotated, cv2.COLOR_BGR2GRAY)
		import skimage.feature
		skimage.feature.plot_matches(ax, im1_gray, im2_gray,
			locs1, locs2, matches, matches_color='r', only_matches=True)
		ax.set_title(f'Feature Matches at {angle}° rotation ({len(matches)} matches)')
		plt.tight_layout()
		plt.savefig(f'../results/brief_rot_{angle}.png', dpi=120)
		plt.close()
		print(f"  → Saved visualization for {angle}°")

#Display histogram
plt.figure(figsize=(10, 5))
plt.bar(list(angles), match_counts, width=8, color='steelblue', edgecolor='black')
plt.xlabel('Rotation Angle (degrees)')
plt.ylabel('Number of Matches')
plt.title('BRIEF Feature Matches vs. Rotation Angle')
plt.xticks(list(angles), rotation=45)
plt.tight_layout()
plt.savefig('../results/brief_rotation_histogram.png', dpi=120)
plt.show()
print("Histogram saved to ../results/brief_rotation_histogram.png")

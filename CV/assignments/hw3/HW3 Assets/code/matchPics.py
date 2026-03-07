import numpy as np
import cv2
import skimage.color
from helper import briefMatch
from helper import computeBrief
from helper import corner_detection
#Complete functions above this line before this step
def matchPics(I1, I2):
	#I1, I2 : Images to match
	

	#Convert Images to GrayScale
	if len(I1.shape) == 3:
		I1_gray = cv2.cvtColor(I1, cv2.COLOR_BGR2GRAY)
	else:
		I1_gray = I1
	if len(I2.shape) == 3:
		I2_gray = cv2.cvtColor(I2, cv2.COLOR_BGR2GRAY)
	else:
		I2_gray = I2
	
	#Detect Features in Both Images
	locs1 = corner_detection(I1_gray, sigma=0.15)
	locs2 = corner_detection(I2_gray, sigma=0.15)
	
	#Obtain descriptors for the computed feature locations
	desc1, locs1 = computeBrief(I1_gray, locs1)
	desc2, locs2 = computeBrief(I2_gray, locs2)

	#Match features using the descriptors
	matches = briefMatch(desc1, desc2, ratio=0.65)

	return matches, locs1, locs2

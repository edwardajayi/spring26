# Question 2: Image Straightening - Robot-Assisted Chess Training

## Objective
The goal of this task is to automatically straighten images of a chessboard that are tilted due to varying camera angles. Correcting this orientation is crucial for downstream tasks like piece identification and move validation in an AI chess coach.

## Methodology

We will implement a pipeline to detect the dominant orientation of the chessboard lines and rotate the image to align them with the vertical and horizontal axes. The steps are as follows:

### 1. Preprocessing
*   **Grayscale Conversion**: Color information is not needed for detecting geometric lines. Converting to grayscale simplifies the image and reduces computational load.
*   **Noise Reduction (Gaussian Blur)**: Images often contain noise that can cause false edge detections. Applying a Gaussian Blur smooths the image, suppressing high-frequency noise while preserving the strong edges formed by the grid lines.
*   **Contrast Enhancement (CLAHE)**: The chessboard might have uneven lighting. Contrast Limited Adaptive Histogram Equalization (CLAHE) locally enhances contrast, making the grid lines distinct across the entire image, which improves edge detection performance.

### 2. Edge Detection
*   **Canny Edge Detector**: We use the Canny algorithm to find edges in the preprocessed image. It is effective because it uses a multi-stage algorithm to detect a wide range of edges and suppresses weak edges that are not connected to strong ones (hysteresis thresholding).

### 3. Line Detection
*   **Hough Transform**: The Hough Transform is a feature extraction technique used to detect imperfect instances of objects within a certain class of shapes by a voting procedure. We use it to find straight lines in the edge map. The algorithm transforms points in the image space to a parameter space (Hough space), usually represented by $\rho$ (distance from origin) and $\theta$ (angle). Grid lines on the chessboard will result in peaks in the Hough space corresponding to their $\rho$ and $\theta$.

### 4. Angle Analysis and Straightening
*   **Dominant Orientation**: The detected lines will predominantly lie along the grid axes of the chessboard. We analyze the distribution of the angles ($\theta$) of these lines. The most frequent angle (mode) or the average of the dominant cluster of angles represents the rotation of the board relative to the image frame.
*   **Rotation**: Once the rotation angle is determined, we straighten the image by rotating it in the opposite direction (negative of the detected angle). We compute an affine rotation matrix and warp the image to its new, straightened orientation.

## Algorithm Steps (as implemented in the notebook)
1.  Load the image.
2.  Convert to grayscale.
3.  Apply Gaussian Blur.
4.  Apply CLAHE for contrast enhancement.
5.  Detect edges using Canny.
6.  (Optional) Use morphological operations to refine edges.
7.  Detect lines using `cv2.HoughLines`.
8.  Extract $\theta$ values and find the dominant angle.
9.  Rotate the image by this angle to straighten it.

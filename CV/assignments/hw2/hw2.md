# Homework 2: Deep Dive and Explanations

## Question 1: Counting Objects - Inventory Management Systems

### Goal
The objective is to count the number of distinct objects in an image. This is a fundamental computer vision task used in automated inventory systems, cell counting in biology, and manufacturing quality control.

### The Pipeline: "Naive" Method
We call this "naive" because it relies on simple image processing steps (thresholding/edge detection) rather than learning-based approaches (like deep learning object detectors). It assumes objects have distinct boundaries and contrast against the background.

#### 1. Load Image
We use OpenCV to load the image. Images are typically loaded as BGR (Blue, Green, Red) matrices.
```python
img = cv2.imread(image_path)
```

#### 2. Grayscale Conversion
**Why?** Color information often adds complexity without helping with edge detection. Edges are primarily defined by changes in intensity (luminance), not color. Processing a single channel (grayscale) is computationally faster (1/3rd the data) and conceptually simpler.

**Math:**
A common formula to convert RGB to Grayscale ($Y$) perceives luminance by weighting color channels based on human perception (we are more sensitive to green):
$$Y = 0.299R + 0.587G + 0.114B$$

```python
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
```

#### 3. Gaussian Blur (Smoothing)
**Why?** Real-world images contain noise (random pixel variations). Edge detectors look for sharp changes in intensity. Noise looks like sharp changes! If we don't smooth the image, the edge detector will pick up noise as valid edges.

**Math & Sigma ($\sigma$):**
We convolve the image with a Gaussian Kernel. The Gaussian function in 2D is:
$$G(x, y) = \frac{1}{2\pi\sigma^2} e^{-\frac{x^2+y^2}{2\sigma^2}}$$
where $\sigma$ (sigma) determines the "spread" or amount of blurring.

**Controlling Sigma vs. Kernel Size:**
In `cv2.GaussianBlur(src, ksize, sigmaX)`, you have two knobs:
1.  **`ksize` (Kernel Size)**: The strictly definable width/height of the window (e.g., (5, 5)). Must be positive and odd.
2.  **`sigmaX` (Standard Deviation)**: Controls the width of the bell curve.

**Automatic vs. Manual Sigma:**
*   **Automatic (`sigmaX=0`)**: If you set sigma to 0, OpenCV calculates it automatically from the kernel size using the formula: $\sigma = 0.3 \times ((ksize - 1) \times 0.5 - 1) + 0.8$. For a 5x5 kernel, $\sigma \approx 1.1$.
    *   *Standard Practice:* This is very common for general image processing tasks where "good enough" smoothing is needed without fine-tuning.
*   **Manual Assignment**: You can specify a float value (e.g., `1.5`).
    *   *When is it a GOOD idea?*
        *   **Precision**: When you need exact control over the frequency response (e.g., in Scale-Space theory, SIFT feature detection) where specific $\sigma$ values represent specific physical scales.
        *   **Fine Tuning**: Discrete kernel sizes (3, 5, 7) might be too coarse. A sigma of 1.2 vs 1.3 makes a subtle difference that integer kernels can't capture.
    *   *When is it a BAD idea?*
        *   **Mismatch**: If you set a high sigma (e.g., 5.0) but a small kernel (e.g., 3x3), the Gaussian function gets "cropped" or truncated prematurely, leading to artifacts and poor smoothing.
        *   **Rule of Thumb**: If estimating manually, your kernel size should be at least $6\sigma$ (e.g., radius of $3\sigma$ on each side) to capture 99.7% of the Gaussian curve. If $\sigma=1.0$, `ksize` should be at least $6 \times 1 \approx 7$ (closest odd number).

```python
# Automatic sigma (calculated from 5x5 kernel)
blurred_auto = cv2.GaussianBlur(gray, (5, 5), 0)

# Manual sigma (Explicit control)
# Here we want more blur (sigma=2.0).
# To avoid cutting off the curve, we calculate ksize or let OpenCV compute ksize if we use other functions like getGaussianKernel.
# For GaussianBlur force ksize to be 0 is NOT allowed for kernel calculation, 
# you typically ensure ksize is large enough, e.g., 6*sigma + 1 => 13
blurred_manual = cv2.GaussianBlur(gray, (13, 13), 2.0)
```

#### 4. Edge Detection (Canny)
**Why?** To find the boundaries of objects. The Canny Edge Detector is a multi-stage algorithm considered the "gold standard" for traditional edge detection.

**Steps inside Canny:**
1.  **Noise Reduction:** Application of Gaussian blur (we effectively did this, but Canny can do it internally).
2.  **Gradient Calculation:** Finds intensity gradients ($G_x$ and $G_y$) usually using Sobel operators.
    *   Gradient Magnitude: $G = \sqrt{G_x^2 + G_y^2}$
    *   Gradient Direction: $\theta = \arctan(G_y / G_x)$
3.  **Non-Maximum Suppression:** Thins the edges. It checks if the gradient magnitude at a pixel is the local maximum along the gradient direction. If not, it sets it to zero (suppresses it). This results in thin, single-pixel wide lines.
4.  **Hysteresis Thresholding:** Uses two thresholds, `minVal` and `maxVal`.
    *   Edges with intensity > `maxVal` are "Sure Edges".
    *   Edges with intensity < `minVal` are discarded.
    *   Edges between `minVal` and `maxVal` are accepted *only if* they are connected to a "Sure Edge".

```python
edges = cv2.Canny(blurred, 50, 150) # 50 is minVal, 150 is maxVal
```

#### 5. Find Contours
**Why?** Edges are just disconnected pixels. Contours connect these pixels into continuous curves or shapes. OpenCV's `findContours` algorithm (based on Suzuki algorithm) analyzes the topological structure of binary images (like our edge map) to find boundaries.

**Hierarchy:**
*   `cv2.RETR_EXTERNAL`: Retrieves only the extreme outer contours (good for counting distinct objects).
*   `cv2.RETR_TREE`: Retrieves all nested contours.

```python
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
```

#### 6. Count
The number of contours found corresponds to the number of separated objects.

### Full Code Solution for Question 1

```python
import cv2
import numpy as np
import matplotlib.pyplot as plt

def count_objects(image_path):
    # 1. Load the image
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Could not load image at {image_path}")
        return 0

    # 2. Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 3. Apply GaussianBlur
    # (5, 5) is the kernel size (must be odd). 0 lets OpenCV calculate sigma from kernel size.
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # 4. Canny Edge Detection
    # Thresholds 30 and 150 are commonly used starting points.
    # Lower threshold captures weak edges, Upper captures strong edges.
    edges = cv2.Canny(blurred, 30, 150)

    # 5. Find Contours
    # RETR_EXTERNAL retrieves only the outer contours.
    # CHAIN_APPROX_SIMPLE compresses horizontal, vertical, and diagonal segments
    # and leaves only their end points (saves memory).
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 6. Count
    count = len(contours)

    # Visualizing the result (Optional but recommended for debugging)
    # Draw contours on a copy of the original image
    output_img = img.copy()
    cv2.drawContours(output_img, contours, -1, (0, 255, 0), 2) # -1 draws all contours, Green color, Thickness 2

    # Display using matplotlib (handles BGR to RGB conversion for display)
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.title("Edge Map")
    plt.imshow(edges, cmap='gray')
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.title(f"Detected Contours: {count}")
    plt.imshow(cv2.cvtColor(output_img, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()

    return count
```


### Task 2: Experimentation & Improvements using Morphological Operations

For touching objects (image `1b.png`) or noisy backgrounds, naive edge detection fails because boundaries merge. To separate touching objects, we use **Morphological Operations**, a **Distance Transform**, and the **Watershed Algorithm**.

#### Morphological Operations Explained
These operations start with a binary image and a "structuring element" (kernel $B$) that slides over the image ($A$).

1.  **Dilation ($A \oplus B$)**: Adds pixels to boundaries.
    *   **Logic:** A pixel is 1 if *at least one* pixel under the kernel is 1.
    *   **Effect:** Fills holes, joins broken lines, makes objects thicker.
2.  **Erosion ($A \ominus B$)**: Removes pixels from boundaries.
    *   **Logic:** A pixel is 1 *only if all* pixels under the kernel are 1.
    *   **Effect:** Removes small noise, separates connected objects (if the connection is thin), makes objects thinner.
3.  **Opening ($A \circ B = (A \ominus B) \oplus B$)**: Erosion followed by Dilation.
    *   **Effect:** Removes small noise while preserving the shape and size of larger objects.
4.  **Closing ($A \bullet B = (A \oplus B) \ominus B$)**: Dilation followed by Erosion.
    *   **Effect:** Closes small holes inside foreground objects.

#### Distance Transform
For each foreground pixel $p$, the distance transform computes its distance to the nearest background pixel:
$$D(p) = \min_{q \in \text{background}} \| p - q \|_2$$

This creates "peaks" at the centers of objects. The **height** of a peak is proportional to the object's **thickness** — a thick circular object produces a tall peak, while a thin elongated object produces a low peak.

#### Watershed Algorithm
The watershed treats the distance transform as a topographic surface:
1.  We threshold the distance transform to find "sure foreground" (the peaks).
2.  These peaks become **markers** (seeds).
3.  The algorithm "floods" from each marker. Where water from two different markers meets, a **boundary** is drawn, separating touching objects.

#### The Threshold Problem: Why Parameter Tuning Matters

The critical parameter is the distance transform threshold:
$$\text{sure\_fg} = \{ p \mid D(p) > \alpha \cdot D_{\max} \}$$

where $\alpha$ is the threshold factor and $D_{\max} = \max_p D(p)$.

**The issue:** When objects have **varying thicknesses**, a single $\alpha$ relative to $D_{\max}$ creates a conflict:
*   $D_{\max}$ is determined by the **thickest** object (e.g., a large circular disk might have $D_{\max} = 50$ pixels).
*   A thin wrench-arm might only have a peak of $D = 8$ pixels.
*   If $\alpha = 0.5$, the threshold becomes $0.5 \times 50 = 25$. The wrench ($D = 8 < 25$) gets **no marker** and is invisible to Watershed.
*   If $\alpha = 0.1$, the threshold is $0.1 \times 50 = 5$. The wrench ($D = 8 > 5$) gets a marker, but nearby objects with overlapping distance regions may **merge** into one marker.

**Our debugging process on `1b.png` (13 objects):**

| $\alpha$ | Opening Iterations | Count | Issue |
|---|---|---|---|
| 0.5 | 2 | **2** | Threshold too high: only the 2 thickest objects survived |
| 0.1 | 2 | **10** | Threshold too low: some thin objects merged; opening eroded small objects |
| 0.15 | 1 | **13** ✓ | Sweet spot: all objects get individual markers |

**Why `iterations=1` helps:** Each iteration of opening erodes the binary mask by one kernel-width. With a 3×3 kernel and 2 iterations, thin objects (width ≤ 4px after thresholding) can be completely eroded away. Reducing to 1 iteration preserves these thin objects while still removing single-pixel noise.

### Corrected Code for Touching Objects

```python
def count_touching_objects(image_path):
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Could not load image at {image_path}")
        return 0
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 1. Otsu's Thresholding
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # 2. Noise Removal (Opening) - iterations=1 to preserve thin objects
    kernel = np.ones((3,3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    
    # 3. Sure Background Area (Dilation)
    sure_bg = cv2.dilate(opening, kernel, iterations=3)
    
    # 4. Sure Foreground Area (Distance Transform)
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    # alpha=0.15: tuned to handle both thick and thin objects
    _, sure_fg = cv2.threshold(dist_transform, 0.15 * dist_transform.max(), 255, 0)
    
    # 5. Unknown Region (Border between FG and BG)
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)
    
    # 6. Marker Labelling
    _, markers = cv2.connectedComponents(sure_fg)
    markers = markers + 1  # Add 1 so bg is 1, not 0
    markers[unknown == 255] = 0  # Mark unknown regions as 0
    
    # 7. Watershed
    markers = cv2.watershed(img, markers)
    img[markers == -1] = [0, 0, 255]  # Draw boundaries in Red
    
    count = markers.max() - 1  # Subtract 1 for background
    
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(thresh, cmap='gray')
    plt.title("Otsu Threshold")
    plt.axis('off')
    
    plt.subplot(1, 2, 2)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title(f"Watershed Count: {count}")
    plt.axis('off')
    plt.show()
    return count
```

### Task 3: Real World Experimentation
**Guidance:**
1.  **Setup:** Place distinct objects (coins, pens, fruits) on a white sheet of paper or distinct table.
2.  **Capture:** Take a photo from directly above (top-down view) to minimize perspective distortion and occlusion.
3.  **Process:** Run your `count_objects` function on this image.

### Task 4: Difficulties & Improvements
**Common Difficulties:**
*   **Shadows:** Strong lighting creates shadows that look like new objects or extensions of objects. *Improvement: Better lighting, Shadow removal algorithms.*
*   **reflections:** Shiny objects reflect light, creating "holes" or false edges inside the object. *Improvement: Polarizing filters, Diffuse lighting.*
*   **Occlusion:** Objects partially hiding others. Naive counting counts the visible mass as one or two depending on separation. *Improvement: Deep Learning (YOLO, Faster R-CNN) which learns object features, not just boundaries.*
*   **Complex Backgrounds:** If the background isn't plain, texture is picked up as edges. *Improvement: Background subtraction (if static camera), Deep Learning.*

### Task 5: Real World Scenarios
*   **Traffic Monitoring:** Counting cars on a highway.
*   **Microbiology:** Counting bacteria or cells on a petri dish.
*   **Crowd Control:** Estimating number of people in a zone.
*   **Agriculture:** Counting fruits on a tree or conveyor belt for yield estimation.



## Bonus: Evaluating Image-Based Object Counting on Video

### Goal
To evaluate the robustness of the static image-based counting algorithm (from Question 1) when applied to a dynamic video stream. Real-world environments introduce temporal variations that static algorithms normally don't account for.

### The Pipeline: Frame-by-Frame Processing
We treat the video as a sequence of independent images $I(x,y,t)$ where $t$ is the frame index. For each frame, we apply the identical pipeline:
1.  Color Conversion: $RGB \to Gray$
2.  Gaussian Blur: $G(x,y) * I(x,y,t)$
3.  Canny Edge Detection: $\nabla I > T_{high}$
4.  Contour Extraction & Counting.

### Limitations & Failure Modes (Analysis with Math)

Applying a static method to video reveals several fundamental limitations:

#### 1. Temporal Instability (Flickering Counts)
**Observation:** The count fluctuates (e.g., $7 \to 6 \to 7$) even when objects are stationary.
**Mathematical Reason:**
Video contains sensor noise $n(x,y,t)$. A pixel's intensity $I(x,y,t)$ is a random variable:
$$ I(x,y,t) = I_{true}(x,y) + n(x,y,t) $$
In Canny edge detection, a pixel is an edge if its gradient magnitude $\|\nabla I\|$ exceeds a threshold $T$.
If a pixel is near the threshold ($\|\nabla I\| \approx T$), the noise term $n(x,y,t)$ can push it above or below $T$ in consecutive frames.
*   Frame $t$: $\|\nabla I\| + n > T \implies$ Edge detected.
*   Frame $t+1$: $\|\nabla I\| - n < T \implies$ Edge lost.
This breaks the contour connectivity, causing one object to split into two or disappear, leading to count jitter.

#### 2. Motion Blur
**Observation:** Fast-moving objects are not detected.
**Mathematical Reason:**
Motion blur is a convolution of the image with a motion kernel $K_{motion}$ (e.g., a box filter in the direction of motion).
$$ I_{blurred} = I * K_{motion} $$
Convolution acts as a low-pass filter, smoothing out high-frequency details (edges).
The gradient magnitude $\|\nabla I\|$ decreases as the edge spreads over more pixels.
If $\|\nabla I_{blurred}\| < T_{low}$ (Canny's lower threshold), the edge detectors fail to fire, and the object "vanishes" during motion.

#### 3. Lighting Variations (Auto-Exposure/White Balance)
**Observation:** The count changes when a hand enters the scene or lighting shifts.
**Mathematical Reason:**
Cameras automatically adjust exposure time ($E$) and gain ($g$) based on the total scene brightness.
$$ I(x,y,t) = g(t) \cdot E(t) \cdot L(x,y) \cdot R(x,y) $$
where $L$ is illumination and $R$ is reflectance.
If a dark object (hand) enters, the camera might increase gain $g(t)$ to compensate. This brightens the background, potentially reducing the contrast ratio $\frac{I_{obj}}{I_{bg}}$ or amplifying noise $n(x,y,t)$, triggering false edges (background texture) or washing out weak edges.

### Solution Code (`bonus_solution.py`)
This script reads the video, processes it, and writes the output with overlay.



## Question 2: Finding lines on a chessboard and straightening the image - Robot-Assisted Chess Training

### Goal
The objective is to automatically straighten a tilted image of a chessboard. This is a common preprocessing step in computer vision pipelines (like optical character recognition or document scanning) to standardize the input before further analysis (like recognizing chess pieces or board state).

### The Pipeline
We use a classic geometric computer vision pipeline: Enhance contrast $\rightarrow$ Detect Edges $\rightarrow$ Detect Lines $\rightarrow$ Calculate Rotation $\rightarrow$ Warp (Rotate).

#### 1. Preprocessing (Grayscale & Blur)
Similar to Question 1, we convert to grayscale and apply Gaussian Blur.
**Why?** Color is irrelevant for line detection, and blurring suppresses noise that would cause false edge detections.

The **kernel size** matters: a small `(5,5)` kernel is often sufficient. While larger kernels like `(9,9)` suppress more texture (like wood grain), they can also blur the grid lines themselves, causing them to be missed.

```python
blurred = cv2.GaussianBlur(gray, (5, 5), 0)  # (5,5) found to be optimal for this image
# (9,9) was too aggressive and missed lines.
```

#### 2. Contrast Limited Adaptive Histogram Equalization (CLAHE)
**Why?** Standard histogram equalization spreads contrast across the entire image, which can over-amplify noise in uniform regions. CLAHE does this on small tiles (grid size) and limits the contrast amplification (clip limit).
 This is crucial for chessboards because lighting is often uneven (e.g., reflections on the board). CLAHE ensures grid lines are visible everywhere.

```python
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
enhanced = clahe.apply(blurred)
```

#### 3. Edge Detection (Canny)
**Why?** To extract the boundaries of the grid squares.
We use the same Canny edge detector as in Question 1. The output is a binary map where 1 represents an edge pixel.

#### 3.5. (Optional) Morphological Operations to Enhance Edges
After Canny, the edge map can contain **gaps** (broken lines) due to noise, low contrast, or uneven lighting. The Hough Transform is a voting-based method — it accumulates votes from edge pixels along a line. If a chessboard grid line has gaps, fewer pixels vote for that line, so it may fall below the Hough threshold and be missed entirely.

**Morphological operations** are pixel-level binary image transformations that can close these gaps and strengthen the edge map before line detection.

**Structuring Element (Kernel):**
All morphological operations use a small binary matrix called a *structuring element* or *kernel* $B$. A common choice is a $3 \times 3$ or $5 \times 5$ matrix of all ones:
$$B = \begin{bmatrix} 1 & 1 & 1 \\ 1 & 1 & 1 \\ 1 & 1 & 1 \end{bmatrix}$$

```python
kernel = np.ones((3, 3), np.uint8)
```

**Dilation ($A \oplus B$):**
*   **Rule:** A pixel in the output is set to **1** if **at least one** pixel under the kernel is 1 in the input.
*   **Effect on edges:** Edge pixels "grow" outward by the kernel radius. Small gaps between edge segments get filled because a nearby edge pixel "reaches across" the gap.
*   **Intuition:** Think of it as painting with a thick brush over existing lines — the lines get thicker, and small breaks disappear.

```python
dilated = cv2.dilate(edges, kernel, iterations=1)
```

**Erosion ($A \ominus B$):**
*   **Rule:** A pixel in the output is **1** only if **all** pixels under the kernel are 1 in the input.
*   **Effect after dilation:** Shrinks the thickened edges back toward their original width, while the newly-connected bridge pixels remain (because they are now surrounded by other edge pixels).
*   **Intuition:** It peels one layer off the edge boundary. Since dilation added a layer, erosion restores the original thickness but keeps the connections.

```python
eroded = cv2.erode(dilated, kernel, iterations=1)
```

This Dilation→Erosion sequence is called **Closing** ($A \bullet B = (A \oplus B) \ominus B$). It "closes" small gaps without changing the overall geometry.

**Why "should be applied with care"?**
*   If the kernel is **too large** or you use **too many iterations**, nearby parallel grid lines can merge into one thick blob. The Hough Transform then sees one wide band instead of two distinct lines, miscounting the lines and corrupting the angle histogram.
*   **Rule of thumb:** The kernel size should be smaller than the gap between adjacent grid lines. For a chessboard image where grid lines are ~2px apart, a $3 \times 3$ kernel with 1 iteration is safe. A $7 \times 7$ kernel would likely merge them.

| Parameter       | Too Small               | Sweet Spot              | Too Large                    |
|----------------|--------------------------|--------------------------|------------------------------|
| **Kernel Size** | No effect on gaps        | Fills gaps, preserves lines | Merges adjacent lines       |
| **Iterations**  | No effect on gaps        | 1–2 usually sufficient   | Blobs grow; geometry breaks |

#### 4. Line Detection (Hough Transform)
**Why?** To group edge pixels into straight lines.
**Math:**
A line in the image space $y = mx + c$ can be represented in Hessian Normal form:
$$ \rho = x \cos \theta + y \sin \theta $$
where $\rho$ is the perpendicular distance from the origin to the line, and $\theta$ is the angle of that normal.
1.  **Voting:** The algorithm creates a 2D accumulator array (Hough Space) with axes $\rho$ and $\theta$.
2.  For every edge pixel $(x, y)$, we iterate through all possible $\theta$ and calculate $\rho$. We vote (increment) the corresponding $(\rho, \theta)$ bin.
3.  **Peaks:** Peaks in the accumulator represent lines formed by many edge pixels.

The **threshold** parameter is the minimum number of edge pixel votes required to accept a line.

```python
# rho=1 pixel, theta=1 degree (pi/180), threshold=300 votes
lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=300)
```

> [!WARNING]
> *   **200 (Too Low):** Produces excessive number of spurious lines from background texture/reflections.
> *   **500 (Too High):** Misses legitimate grid lines.
> *   **400 (Okay):** Misses a few legitimate grid lines but detects most.
> *   **300 (Sweet Spot):** Detected the main grid lines without being overwhelmed by noise. See experimentation below.

#### 5. Angle Analysis
**Goal:** Find the dominant orientation of the board.
We iterate through all detected lines and look at their angles ($\theta$).
*   Grid lines are either horizontal ($\theta \approx 0^\circ$ or $180^\circ$) or vertical ($\theta \approx 90^\circ$).
*   If the board is tilted by $10^\circ$, we expect peaks at $10^\circ$ and $100^\circ$.
*   We collect all $\theta$ values and find the **mode** (most frequent angle) or average of the major cluster.

We determine which rectilinear axis (0°, 90°, or 180°) the dominant angle is closest to, and compute the difference — that's our corrective rotation:

```python
angle = np.degrees(top_3_angles[0])  # Convert dominant theta from radians to degrees
if angle < 45:
    rotation_angle = -angle           # Snap to 0°
elif angle < 135:
    rotation_angle = 90 - angle       # Snap to 90°
else:
    rotation_angle = 180 - angle      # Snap to 180°
```

#### 6. Image Rotation (Affine Transform)
**Math:**
To rotate an image by $\phi$ around a center $(c_x, c_y)$, we use the rotation matrix:
$$
M = \begin{bmatrix}
\alpha & \beta & (1-\alpha)c_x - \beta c_y \\
-\beta & \alpha & \beta c_x + (1-\alpha)c_y
\end{bmatrix}
$$
where $\alpha = \text{scale} \cdot \cos \phi$ and $\beta = \text{scale} \cdot \sin \phi$.

We use `cv2.getRotationMatrix2D` to construct $M$ and `cv2.warpAffine` to apply it:

```python
def rotate_image(image, angle):
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, rotation_matrix, (w, h),
                             flags=cv2.INTER_LINEAR,
                             borderMode=cv2.BORDER_REPLICATE)
    return rotated
```

**Key parameters:**
*   `cv2.INTER_LINEAR` — **Bilinear interpolation**. Since rotation maps destination pixels to non-integer source coordinates, we need to interpolate. Bilinear averages the 4 nearest pixels, producing smooth results (vs. `INTER_NEAREST` which would be blocky).
*   `cv2.BORDER_REPLICATE` — When rotation exposes pixels outside the original image boundary (the "empty corners"), this fills them by **repeating the nearest edge pixel** instead of leaving black voids. This looks more natural than the default black fill.

> [!NOTE]
> **BGR vs RGB:** OpenCV loads images as BGR (Blue-Green-Red), but Matplotlib's `plt.imshow()` expects RGB. If you display directly without converting, the image will look blue-tinted. Always convert before displaying:
> ```python
> plt.imshow(cv2.cvtColor(rotated, cv2.COLOR_BGR2RGB))
> ```

### Parameter Tuning & Experimentation

The image straightening pipeline has many tunable parameters. Finding the right combination requires experimentation. Here are the key findings from testing on `q2_data/2b.jpg`:

#### Hough Transform Threshold (Most Impactful)

| Threshold | Result | Assessment |
|-----------|--------|------------|
| **200** | Hundreds of lines detected. Image flooded with red lines. | ❌ Far too low (Over-detection) |
| **300** | Good balance. Detects main grid boundaries while ignoring most table grain. | ✅ Optimal |
| **400-500** | Missed several legitimate grid lines. | ❌ Too high (Under-detection) |

**Takeaway:** The threshold needs to be tuned. `300` was the best performer for `q2_data/2b.jpg`.

#### Gaussian Blur Kernel Size

| Kernel | Effect |
|--------|--------|
| **(5, 5)** | **Optimal.** Preserves grid lines while smoothing enough noise. Detected lines in the main direction well. |
| **(7, 7)** | Mixed results. Missed the middle line in the main direction but found more side lines. |
| **(9, 9)** | **Too aggressive.** Blurred out lines to the point where they weren't detected. |

#### Why Only One Axis of Lines Is Detected

With threshold=400, typically only the **horizontal** grid lines are detected, not the vertical ones. This happens because:
*   **Chess pieces sit on the board**, physically breaking the vertical edge continuity. Each piece fragments the vertical line into short segments that individually don't accumulate enough Hough votes.
*   **Horizontal edges are more continuous** because pieces sit *on top of* horizontal boundaries rather than blocking them.

> [!TIP]
> This is perfectly fine for straightening! We only need **one set of parallel lines** to determine the board's tilt angle. The vertical lines would be exactly 90° offset from the horizontal ones — they carry the same rotation information.

### Full Code Solution for Question 2

The following code matches what was used in the notebook, with the tuned parameters discovered through experimentation.

**Cell 1 — Line Detection:**
```python
import cv2
import numpy as np
import matplotlib.pyplot as plt

def find_lines(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(blurred)
    edges = cv2.Canny(enhanced, 100, 200)
    lines = cv2.HoughLines(edges, 1, np.pi/180, threshold=300)
    angles_count = {}
    for r_theta in lines:
        arr = np.array(r_theta[0], dtype=np.float64)
        r, theta = arr
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*r
        y0 = b*r
        if theta in angles_count.keys():
            angles_count[theta] += 1
        else:
            angles_count[theta] = 1
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
    cv2.imwrite('linesDetected.jpg', img)
    return angles_count

angles_count = find_lines('q2_data/2b.jpg')
top_3_angles = sorted(angles_count, key=angles_count.get, reverse=True)[:3]
img = cv2.imread('linesDetected.jpg')
```

**Cell 2 — Angle Calculation:**
```python
angle = np.degrees(top_3_angles[0])
print(f"Dominant angle: {angle:.2f} degrees")

if angle < 45:
    rotation_angle = -angle
elif angle < 135:
    rotation_angle = 90 - angle
else:
    rotation_angle = 180 - angle

print(f"Rotation needed: {rotation_angle:.2f} degrees")
```

**Cell 3 — Rotation & Display:**
```python
def rotate_image(image, angle):
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, rotation_matrix, (w, h),
                             flags=cv2.INTER_LINEAR,
                             borderMode=cv2.BORDER_REPLICATE)
    return rotated

rot_img = rotate_image(img, rotation_angle)
plt.imshow(cv2.cvtColor(rot_img, cv2.COLOR_BGR2RGB))
plt.title(f'Straightened (Rotation: {rotation_angle:.2f}°)')
plt.axis('off')
```

### Results

| Image | Dominant Angle | Rotation Applied |
|-------|---------------|-----------------|
| **2a.jpg** | 90.00° | -0.00° (already straight) |
| **2b.jpg** | 34.00° | -34.00° |
| **2c.jpg** | 20.00° | -20.00° |


## Question 3: Image Compression with Fourier Transform

### Explanation
The Fourier Transform decomposes an image into its constituent sine and cosine components. In the frequency domain, an image is represented as a sum of these periodic functions with varying amplitudes and phases.
*   **Low Frequencies:** Represent smooth variations, large structures, and general shapes (e.g., sky, walls). These contain the majority of the image's energy.
*   **High Frequencies:** Represent abrupt changes, edges, fine details, and noise.

**Compression Principle:**
Most natural images are dominated by low-frequency information. We can compress an image by transforming it to the frequency domain (FFT), keeping only the coefficients with the highest magnitudes (typically low frequencies), and discarding the rest (setting them to zero). The Inverse FFT then reconstructs the image. This is a form of *lossy compression*.

### Mathematical Reasoning
The Discrete Fourier Transform (DFT) of an image $f(x,y)$ of size $M \times N$ is given by:

$$
F(u,v) = \sum_{x=0}^{M-1} \sum_{y=0}^{N-1} f(x,y) e^{-j 2\pi (ux/M + vy/N)}
$$

where $F(u,v)$ is the complex frequency coefficient at coordinates $(u,v)$. The magnitude $|F(u,v)|$ represents the strength of that frequency component.

We shift the zero-frequency component ($F(0,0)$, or DC component) to the center of the spectrum for easier analysis. We then apply a **threshold mask** $M(u,v)$:

$$
F_{filtered}(u,v) = \begin{cases} 
F(u,v) & \text{if } |F(u,v)| \geq T_{percentile} \\
0 & \text{otherwise}
\end{cases}
$$

The compressed image is reconstructed using the Inverse DFT:

$$
f_{compressed}(x,y) = \frac{1}{MN} \sum_{u=0}^{M-1} \sum_{v=0}^{N-1} F_{filtered}(u,v) e^{j 2\pi (ux/M + vy/N)}
$$

### Full Code Solution for Question 3
The following code implements the compression pipeline:
1.  **FFT:** Converts grayscale image to frequency domain.
2.  **Thresholding:** Sorts all coefficients by magnitude and keeps the top $k\%$ (e.g., 10%).
3.  **IFFT:** Reconstructs the compressed spatial image.

```python
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

def compress_image_fft_new(image_path, keep_fraction=0.1):
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Could not read {image_path}")
        return None, None, None
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 1. Compute FFT
    f = np.fft.fft2(gray)
    fshift = np.fft.fftshift(f)
    
    # 2. Magnitude Spectrum
    magnitude = np.abs(fshift)
    
    # 3. Thresholding: keep top 'keep_fraction' of coefficients
    # Flatten and sort to find threshold value
    sorted_indices = np.argsort(magnitude.flatten())
    n_pixels = magnitude.size
    cutoff_index = int((1 - keep_fraction) * n_pixels)
    threshold_val = magnitude.flatten()[sorted_indices[cutoff_index]]
    
    # Create mask (1 where mag >= threshold, 0 otherwise)
    mask = np.zeros_like(magnitude)
    mask[magnitude >= threshold_val] = 1
    
    # Apply mask
    fshift_filtered = fshift * mask
    
    # 4. Inverse FFT to reconstruct image
    f_ishift = np.fft.ifftshift(fshift_filtered)
    img_back = np.abs(np.fft.ifft2(f_ishift))
    
    return gray, img_back, mask

# Process all images in q3_data
data_dir = "ACV Assignment 2/q3_data"  
output_dir = "ACV Assignment 2/Assets"
os.makedirs(output_dir, exist_ok=True)

# List images
images = [f for f in os.listdir(data_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

for filename in images:
    path = os.path.join(data_dir, filename)
    name = os.path.splitext(filename)[0]
    print(f"Processing {name}...")
    
    # Compress keeping top 10% of coefficients
    original, compressed, mask = compress_image_fft_new(path, keep_fraction=0.1)
    
    if original is not None:
        cv2.imwrite(os.path.join(output_dir, f"compressed_{name}.jpg"), compressed)
        
        # Plot Comparison
        plt.figure(figsize=(15, 5))
        plt.subplot(131), plt.imshow(original, cmap='gray'), plt.title('Original'), plt.axis('off')
        plt.subplot(132), plt.imshow(np.log(1 + np.abs(np.fft.fftshift(np.fft.fft2(original)))), cmap='gray'), plt.title('Log Magnitude Spectrum'), plt.axis('off')
        plt.subplot(133), plt.imshow(compressed, cmap='gray'), plt.title(f'Compressed (Top 10% FFT Coeffs)'), plt.axis('off')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f"comparison_{name}.png"))
        plt.show()
        plt.close()
```

### Results & Observations
*   **Low Frequency Images:** Compress very well. Since they lack fine details, discarding high frequencies (the "tails" of the spectrum) results in minimal visual loss.
*   **High Frequency Images:** Show more artifacts (ringing or "Gibbs phenomenon") around sharp edges when compressed, as the high-frequency components defining those edges are discarded.
*   **Satellite Images:** Preserving coastlines and major roads (edges) requires retaining a sufficient percentage of high-frequency components. Typically, 5-10% is enough for recognizability, but 15-20% is needed for high fidelity.

---

## Question 4: Data Augmentation

### Goal
Data augmentation is a technique used to artificially increase the diversity of a training dataset by applying random (but realistic) transformations to existing images. This helps prevent overfitting in machine learning models (like CNNs).

### The Pipeline: Augmentations

#### 1. Resizing (`resize1` & `resize2`)
Changing image dimensions to a fixed size (e.g., $224 \times 224$) is standard for feeding neural networks (like ResNet).
*   **Nearest Neighbor (`cv2.INTER_NEAREST`):** Fast but blocky. Useful for segmentation masks where you want to preserve class labels (integers).
*   **Cubic Spline (`cv2.INTER_CUBIC`):** Smoother transitions. Preferred for RGB images to avoid aliasing artifacts.

#### 2. Flipping (`vertical_flip` & `horizontal_flip`)
*   **Horizontal:** Mirrors the image left-to-right. Essential for object detection/classification as most objects are symmetric or orientation-invariant.
*   **Vertical:** Mirrors upside-down. Less common for natural scenes but useful for top-down imagery (satellite, microscopy).

#### 3. Blur / Noise (`blur_noise`)
Simulates lens defocus or sensor noise. We use Gaussian Blur, which convolving the image with a Gaussian kernel. This helps the model become robust to low-quality or out-of-focus inputs.

#### 4. Rotation (`rotation`)
Rotates the image by an angle $\theta$. We use an affine transform matrix:
$$
\begin{bmatrix}
\alpha & \beta & (1-\alpha) \cdot c_x - \beta \cdot c_y \\
-\beta & \alpha & \beta \cdot c_x + (1-\alpha) \cdot c_y
\end{bmatrix}
$$
where $\alpha = \cos \theta, \beta = \sin \theta$.

#### 5. Shear (`shear_x` & `shear_y`)
Slants the image along an axis, simulating a change in camera perspective.
*   **X-Shear Matrix:** $\begin{bmatrix} 1 & sh_x & 0 \\ 0 & 1 & 0 \end{bmatrix}$
*   **Y-Shear Matrix:** $\begin{bmatrix} 1 & 0 & 0 \\ sh_y & 1 & 0 \end{bmatrix}$

### Code Implementation
```python
import cv2
import numpy as np

def data_augmentation(img, type):
    image = img # Fix variable name mismatch if user uses 'image' internally
    rows, cols = image.shape[:2] # Needed for rotation/shear
    
    if type=="resize1":
        # resize the  image to 224 x 224 use nearest neighbor 
        return cv2.resize(image, (224, 224), interpolation=cv2.INTER_NEAREST)
    elif type=="resize2":
        # resize the  image to 224 x 224 use cubic spline interpolation
        return cv2.resize(image, (224, 224), interpolation=cv2.INTER_CUBIC)
    elif type=="vertical_flip":
        # flip the image vertically
        return cv2.flip(image, 0)
    elif type=="horizontal_flip":
        # flip the image horizontally
        return cv2.flip(image, 1)
    elif type=="blur_noise":
        # add Gaussian noise
        return cv2.GaussianBlur(image, (15, 15), 0)
    elif type=="rotation":
        # # 90 degree rotation
        # return cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        # 30 degree rotation
        # FIXED: cv2.ROTATE_30_CLOCKWISE does not exist. Using warpAffine.
        M = cv2.getRotationMatrix2D((cols/2, rows/2), 30, 1)
        return cv2.warpAffine(image, M, (cols, rows))
    elif type=="shear on y-axis":
        # use your own parameters
        M = np.float32([[1, 0, 0], [0.5, 1, 0]])
        return cv2.warpAffine(image, M, (cols, int(rows*1.5)))
    elif type=="shear on x-axis":
        # use your own parameters
        M = np.float32([[1, 0.5, 0], [0, 1, 0]])
        return cv2.warpAffine(image, M, (int(cols*1.5), rows))
    return image
```

### Bonus: Validity for Face Recognition
For a dataset labeled "Face", do these augmentations preserve the label's validity?

| Augmentation | Valid? | Reasoning |
| :--- | :--- | :--- |
| **Horizontal Flip** | **YES** | A mirrored face is structurally identical to a real face. Highly beneficial. |
| **Vertical Flip** | **NO** | Upside-down faces are rare in natural datasets. Learning this invariance might confuse the network about facial geometry (eyes above mouth). |
| **Rotation ($30^\circ$)** | **YES** | Head tilt is common. Helping the network learn rotational invariance is useful. |
| **Shear** | **MAYBE** | Slight shear simulates perspective changes. Extreme shear distorts facial proportions, potentially making it unrecognizable or "unnatural". |
| **Blur** | **YES** | Real-world photos are often blurry. Robustness to blur is essential. |
| **Resize** | Scale to 224x224 | **YES** | Essential for standardizing input. Aspect ratio distortion should be minimized (e.g., by padding). |
| **Gaussian Blur** | Smooths details | **YES** | Simulates low-quality cameras or motion blur. Makes the model robust to camera focus issues. |
| **Rotation ($90^\circ$)** | Rotate sideways | **NO** | Similar to vertical flip, people don't usually walk sideways. Small rotations ($\pm 15^\circ$) are valid (head tilt), but large ones ($90^\circ$) are rare. |
| **Shear** | Slant | **MAYBE** | Small shear simulates perspective magnitude. Large shear distorts facial geometry unnaturally. |




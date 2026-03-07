# HW3 Solutions — In-Depth Explanations with Code

**Applied Computer Vision (CMU-Africa) — Spring 2026**  
**Assignment 3: Augmented Reality with Planar Homographies**

---

## Table of Contents
- [Q1.1 — Correspondences](#q11--correspondences-10-points)
- [Q2.1 — FAST Detector](#q21--fast-detector-3-points)
- [Q2.2 — BRIEF Descriptor](#q22--brief-descriptor-3-points)
- [Q2.3 — Matching Methods](#q23--matching-methods-3-points)
- [Q2.4 — Feature Matching](#q24--feature-matching-6-points)
- [Q2.5 — BRIEF and Rotations](#q25--brief-and-rotations-8-points)
- [Q2.6 — Computing the Homography](#q26--computing-the-homography-13-points)
- [Q2.7 — Homography with Normalization](#q27--homography-with-normalization-6-points)
- [Q2.8 — RANSAC](#q28--ransac-for-computing-a-homography-20-points)
- [Q2.9 — HarryPotterize](#q29--putting-it-together-8-points)
- [Q3.1 — AR Video](#q31--incorporating-video-18-points)
- [Q4.1 — Image Classification](#q41--binary-image-classification-23-points)

---

# Q1.1 — Correspondences (10 points)

## Concept: Planar Homography & DLT

A **planar homography** $H$ is a $3 \times 3$ matrix that maps points on a plane in one image to corresponding points in another image:

$$x_1 \equiv H x_2$$

where $x_1, x_2$ are in **homogeneous coordinates** (adding a third coordinate = 1).

### 1. Degrees of Freedom of $h$

$H$ has 9 entries, but since it's defined **up to scale** (multiplying $H$ by any non-zero scalar gives the same transformation), one parameter is redundant:

$$\text{DOF} = 9 - 1 = \boxed{8}$$

### 2. Number of Point Pairs

Each point correspondence gives **2 independent equations** (from the x and y components). To solve for 8 unknowns:

$$\text{Min pairs} = \frac{8}{2} = \boxed{4}$$

### 3. Derivation of $A_i$

Starting from $x_1^i = H x_2^i$, we expand using the cross-product formulation. For point pair $(x_1, y_1) \leftrightarrow (x_2, y_2)$:

$$
A_i = \begin{bmatrix}
-x_2 & -y_2 & -1 & 0 & 0 & 0 & x_1 x_2 & x_1 y_2 & x_1 \\
0 & 0 & 0 & -x_2 & -y_2 & -1 & y_1 x_2 & y_1 y_2 & y_1
\end{bmatrix}
$$

**How this is derived:** Writing out $x_1 = H x_2$ in component form:
- $x_1 \cdot (h_7 x_2 + h_8 y_2 + h_9) = h_1 x_2 + h_2 y_2 + h_3$
- $y_1 \cdot (h_7 x_2 + h_8 y_2 + h_9) = h_4 x_2 + h_5 y_2 + h_6$

Rearranging each to $\text{something} \cdot h = 0$ gives the two rows of $A_i$.

### 4. Null Space Analysis

- **Trivial solution:** $h = 0$ (the zero vector) — useless since it means no transformation.
- **Rank of $A$:** With 4+ correspondences, $A$ is $(2N \times 9)$ with rank 8. It's **not full rank** (rank 8 < 9 columns) because the homography is defined up to scale.
- **Impact on singular values:** Exactly one singular value is zero (or near-zero with noise), corresponding to the 1-dimensional null space.
- **Impact on singular vectors:** The right singular vector $v_9$ corresponding to the smallest singular value IS the solution $h$.

---

# Q2.1 — FAST Detector (3 points)

## FAST vs Harris: Key Differences

| Aspect | Harris | FAST |
|--------|--------|------|
| **Method** | Gradient-based: computes structure tensor $M$ from $I_x, I_y$ | Intensity comparison: checks 16 pixels on a circle of radius 3 |
| **Corner criterion** | Eigenvalues of $M$ indicate corner when both are large | Corner when $n$ contiguous pixels are all brighter/darker than center by threshold $t$ |
| **Computation** | Requires gradient computation, Gaussian smoothing, matrix operations | Simple integer comparisons with early rejection |
| **Speed** | Slower — involves convolutions and matrix eigenvalue analysis | Much faster — suitable for real-time (SLAM, mobile vision) |

**Why FAST is faster:** It uses a *segment test* — checking if 12+ out of 16 surrounding pixels differ by a threshold. It can reject most non-corner pixels by checking just 4 pixels first (at positions 1, 5, 9, 13 on the circle). This early-rejection heuristic makes it orders of magnitude faster.

---

# Q2.2 — BRIEF Descriptor (3 points)

## BRIEF vs Filter Banks

**Filter banks** (like Gaussians, Gabor, oriented derivatives) produce **continuous floating-point** responses by convolving filters across the image patch. This yields high-dimensional, real-valued feature vectors.

**BRIEF** uses a fundamentally different approach:
1. Select pairs of pixel locations $(p_i, p_j)$ within a patch
2. For each pair, emit a single bit:
$$\tau(p_i, p_j) = \begin{cases} 1 & \text{if } I(p_i) < I(p_j) \\ 0 & \text{otherwise} \end{cases}$$
3. Concatenate bits → **binary string** (256 bits in our case)

**Can filter banks be used as descriptors?** Yes — you could use the vector of filter responses as a descriptor. SIFT essentially does this with gradient histograms. However, filter bank descriptors are larger (more memory) and slower to match (Euclidean distances on floats vs. Hamming on bits).

---

# Q2.3 — Matching Methods (3 points)

## Hamming Distance & Nearest Neighbor

**Hamming distance** = the number of bit positions where two binary strings differ.

For two 256-bit BRIEF descriptors $d_1$ and $d_2$:
$$d_H(d_1, d_2) = \text{popcount}(d_1 \oplus d_2)$$
where $\oplus$ is bitwise XOR and popcount counts the 1-bits.

**Nearest Neighbor matching:**
1. For each descriptor in image 1, compute Hamming distance to all descriptors in image 2
2. The descriptor with the **smallest** Hamming distance is the match
3. We also use a **ratio test** (matching the best vs second-best distance) to filter unreliable matches

**Why Hamming over Euclidean?**
- **Speed:** XOR + popcount can be done in a single CPU instruction; Euclidean needs floating-point multiply/add
- **Memory:** 256 bits = 32 bytes vs 256 floats = 1024 bytes
- **Hardware support:** Modern CPUs have native popcount instructions

---

# Q2.4 — Feature Matching (6 points)

## Concept

We need to find corresponding points between two images automatically. The pipeline is:

1. **Detect** interest points using FAST corner detector
2. **Describe** each interest point region using BRIEF binary descriptor
3. **Match** descriptors between the two images using Hamming distance

## Full Code: `matchPics.py`

```python
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
```

### Line-by-line explanation:

1. **Grayscale conversion:** FAST and BRIEF operate on single-channel images. We check `len(shape) == 3` to handle both color (BGR) and already-grayscale inputs.

2. **`corner_detection(img, sigma=0.15)`:** Calls `skimage.feature.corner_fast` internally. Returns `locs` as an $(K, 2)$ array of `[row, col]` positions (skimage convention). The `sigma` parameter controls sensitivity — lower values detect more corners.

3. **`computeBrief(img, locs)`:** Takes the grayscale image and corner locations, computes 256-bit binary descriptors for each point. It also **filters** points too close to the image border (within 4 pixels) since BRIEF needs a $9 \times 9$ patch. Returns updated `desc` $(K', 256)$ and filtered `locs` $(K', 2)$.

4. **`briefMatch(desc1, desc2, ratio=0.65)`:** Uses `skimage.feature.match_descriptors` with Hamming distance and **cross-check** + **ratio test**. The ratio test (Lowe's ratio) keeps a match only if the best distance is less than `ratio × second_best_distance`. Lower ratio = stricter matching.

---

# Q2.5 — BRIEF and Rotations (8 points)

## Concept

This experiment reveals that BRIEF is **not rotation-invariant**. By rotating `cv_cover.jpg` and matching against the original, we observe that match count drops sharply with increasing rotation.

## Full Code: `briefRotTest.py`

```python
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
```

### Explanation:

- **`scipy.ndimage.rotate(img, angle, reshape=False)`:** Rotates the image by `angle` degrees. `reshape=False` keeps the output the same size as the input (corners get clipped).
- **`.astype(np.uint8)`:** After rotation, scipy may return float64 values. We cast back to uint8 because FAST/BRIEF require integer images.
- **3 orientations visualized:** At 30°, 90°, and 180° we save side-by-side match visualizations to show the degradation.

### Why BRIEF is NOT rotation-invariant:

BRIEF compares **fixed pixel pairs** at pre-determined locations within the patch. When the image rotates, these locations no longer correspond to the same visual content. For example, if BRIEF compares "pixel at offset (3, 0) vs pixel at offset (-2, 4)", after a 90° rotation those absolute offsets point to completely different image content.

Unlike ORB (which estimates a dominant orientation and rotates the patch before computing the descriptor), BRIEF makes no such correction. This is a deliberate design trade-off — BRIEF sacrifices rotation invariance for **extreme computational speed**.

---

# Q2.6 — Computing the Homography (13 points)

## Concept: Direct Linear Transform (DLT)

Given $N$ point correspondences $(x_1^i, x_2^i)$, we want to find the $3 \times 3$ matrix $H$ such that $x_1 \equiv H x_2$. We reshape $H$ into a 9-vector $h$ and solve $Ah = 0$ using SVD.

## Code: `computeH` in `planarH.py`

```python
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
```

### Line-by-line explanation:

1. **Building $A$ matrix:** Each point pair contributes 2 rows to $A$, following the derivation from Q1.1. Row 1 handles the $x$-component equation and row 2 handles the $y$-component.

2. **`np.linalg.svd(A)`:** Computes $A = U \Sigma V^T$. The SVD decomposes A into orthogonal matrices and a diagonal of singular values.

3. **`Vt[-1, :]`:** The last row of $V^T$ (equivalently, the last column of $V$) is the right singular vector corresponding to the **smallest singular value**. This is the $h$ that minimizes $\|Ah\|^2$ subject to $\|h\| = 1$ — exactly the least-squares solution to $Ah = 0$.

4. **`h.reshape(3, 3)`:** Rearranges the 9-element vector back into the $3 \times 3$ homography matrix.

---

# Q2.7 — Homography with Normalization (6 points)

## Concept

Raw pixel coordinates (e.g., hundreds of pixels) create numerical instability when forming the $A$ matrix — products like $x_1 \cdot x_2$ can be very large, degrading SVD precision. Normalization fixes this by:

1. **Translating** the centroid to the origin
2. **Scaling** so the max distance from origin is $\sqrt{2}$

After computing $\tilde{H}$ on normalized points, we denormalize: $H = T_1^{-1} \tilde{H} T_2$

## Code: `computeH_norm` in `planarH.py`

```python
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
```

### Explanation:

1. **Centroid computation:** `np.mean(x, axis=0)` gives the mean $(x, y)$ coordinate. Subtracting centers the points at the origin.

2. **Scale factor:** We compute the maximum distance from any point to the origin after centering, then scale so this maximum becomes $\sqrt{2}$. This ensures both point sets are in a comparable range.

3. **Similarity transforms $T_1, T_2$:** These $3 \times 3$ matrices combine translation (moving centroid to origin) and scaling into a single homogeneous transformation.

4. **Transform and compute:** We apply $T_1, T_2$ to the points (converting to homogeneous first), then call `computeH` on the normalized points.

5. **Denormalization:** The key equation: if $\tilde{x}_1 = \tilde{H} \tilde{x}_2$, then substituting back: $T_1 x_1 = \tilde{H} T_2 x_2 \Rightarrow x_1 = T_1^{-1} \tilde{H} T_2 x_2$. So $H = T_1^{-1} \tilde{H} T_2$.

---

# Q2.8 — RANSAC for Computing a Homography (20 points)

## Concept

**RANSAC (Random Sample Consensus)** handles **outliers** — incorrect feature matches that would corrupt the DLT solution. Normally, a single bad match can ruin the homography. RANSAC iteratively samples small subsets, fits a model, and picks the one that fits the most points.

### Algorithm:
1. Randomly sample 4 point pairs (minimum for homography)
2. Compute $H$ using `computeH_norm`
3. Transform ALL $x_2$ points with $H$ and check how close they land to $x_1$
4. Points within threshold = **inliers**
5. Repeat many times, keep the $H$ with most inliers
6. **Refit** using all inliers for a cleaner final model

## Code: `computeH_ransac` in `planarH.py`

```python
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
```

### Explanation:

1. **`max_iters = 1000`:** Probability of finding the right model depends on the outlier ratio. With 1000 iterations and ~50% outliers, probability of success is essentially 100%.

2. **`tol = 5` pixels:** A projected point is an inlier if it lands within 5 pixels of the expected position. This threshold balances strictness (too low = few inliers) and permissiveness (too high = includes bad matches).

3. **Homogeneous conversion:** We append 1s to make $[x, y, 1]$ vectors so we can multiply by the $3 \times 3$ homography matrix.

4. **Projection:** $H \cdot x_2^h$ gives a homogeneous result $[x', y', w']$. Dividing by $w'$ gives the 2D projected point. The `w == 0` guard prevents division by zero.

5. **Distance check:** Euclidean distance between the projected point and the expected point. Below `tol` = inlier.

6. **Refitting:** After finding the best consensus set, we recompute the homography using ALL inliers (not just the random 4). This uses more data → better accuracy.

---

# Q2.9 — Putting it Together (8 points)

## Concept

The "HarryPotterize" script chains everything together: detect features, match them, compute a robust homography, and warp one image onto another. The key insight is that we match `cv_cover` (clean book) against `cv_desk` (book on desk), then use the resulting homography to warp `hp_cover` into the book's location.

## Full Code: `HarryPotterize.py`

```python
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
```

### Key Explanations:

**Coordinate convention trap:**
`locs` from `corner_detection` are in `[row, col]` format (skimage's convention), but homography math uses `[x, y]` = `[col, row]`. The line `[:, [1, 0]]` swaps the columns.

**Homography direction:**
We compute `computeH_ransac(x2, x1)` where `x2` = desk points and `x1` = cover points. This gives us $H$ such that cover → desk (mapping cover coordinates to where they appear on the desk).

**Aspect ratio fix (Step 4 discussion):**
`hp_cover.jpg` is $200 \times 295$ but `cv_cover.jpg` is $350 \times 440$. Without resizing, the warped HP cover would be the wrong size for the book-shaped region the homography maps to. We resize HP cover to match CV cover's dimensions first.

## Code: `compositeH` in `planarH.py`

```python
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
    # Where the mask is non-zero, use the warped template; otherwise keep original
    composite_img = img.copy()
    mask_bool = warped_mask > 0
    if len(composite_img.shape) == 3:
        for c in range(3):
            composite_img[:, :, c][mask_bool] = warped_template[:, :, c][mask_bool]
    else:
        composite_img[mask_bool] = warped_template[mask_bool]

    return composite_img
```

### Explanation:

1. **Homography inversion:** The computed $H$ maps FROM the desk TO the cover. To warp the template (cover replacement) INTO the desk image, we need the inverse direction.

2. **Mask technique:** We create a white mask the same size as the template. When warped, this mask shows exactly where the template pixels land in the output. This is crucial for blending — we only overwrite desk pixels where the warped template should appear.

3. **`cv2.warpPerspective`:** Applies a perspective transformation (homography) to an image. Parameters: source image, $3 \times 3$ transformation matrix, output size as `(width, height)`.

4. **Channel-by-channel compositing:** For color images we need to apply the mask to each BGR channel separately.

---

# Q3.1 — Incorporating Video (18 points)

## Concept

This extends the HarryPotterize concept to video: for each frame, we track the book, compute a homography, and overlay AR content. The main challenge is **aspect ratio matching** — the AR video has different proportions than the book cover.

## Full Code: `ar.py`

```python
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
            print(f"Frame {frame_count}/{n_frames}: {len(matches)} matches, "
                  f"{np.sum(inliers)} inliers")

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
```

### Key Explanations:

**Central cropping for aspect ratio:**
The AR source video is wider than the book cover. We compute the target width for the cover's aspect ratio, then crop equally from left and right. This preserves the center of the video content — the most visually important part.

```
Original AR frame:      [####|CONTENT|####]
After central crop:          [CONTENT]
```

**Frame-by-frame processing:** Instead of using `loadVid` (which loads all frames into a massive array), we use OpenCV's `VideoCapture` to read one frame at a time. This is memory-efficient for long videos.

**Error handling:** Some frames may have too few matches or degenerate homographies. The `try/except` block catches these and falls back to writing the original book frame (no overlay).

---

# Q4.1 — Binary Image Classification (23 points)

## The Full Pipeline

```
Raw Images → Resize to 256×256 → Augment (×3) → FAST Keypoints → BRIEF Descriptors → Mean Pool → k-NN Classify
```

## Part A — Dataset Setup

- **Dataset:** 15 face images + 15 no-face images, all 256×256
- `TARGET_SIZE = (256, 256)` — matches the provided image dimensions

## Part B — Data Augmentation Code

```python
AUGMENTATION_FACTOR_1 = 'Brightness'  # Photometric: add/subtract pixel intensity
AUGMENTATION_FACTOR_2 = 'Rotation'    # Geometric: rotate image by small angle

def augment_images(images, labels, seed=42):
    np.random.seed(seed)
    aug_images = list(images)
    aug_labels = list(labels)
    h, w   = images[0].shape
    centre = (w // 2, h // 2)   # cv2 expects (col, row) for centre point

    for img, lbl in zip(images, labels):

        # Augmentation for AUGMENTATION_FACTOR_1: Brightness
        # Random brightness shift in range [-40, +40]
        shift = np.random.randint(-40, 41)
        aug1 = np.clip(img.astype(np.int16) + shift, 0, 255).astype(np.uint8)
        aug_images.append(aug1)
        aug_labels.append(lbl)

        # Augmentation for AUGMENTATION_FACTOR_2: Rotation
        # Random rotation in range [-15°, +15°]
        angle = np.random.uniform(-15, 15)
        M = cv2.getRotationMatrix2D(centre, angle, 1.0)
        aug2 = cv2.warpAffine(img, M, (w, h), borderMode=cv2.BORDER_REFLECT)
        aug_images.append(aug2)
        aug_labels.append(lbl)

    return aug_images, aug_labels
```

### Explanation:

**Brightness augmentation:** We add a random integer shift (±40) to every pixel value. `np.clip` ensures values stay in [0, 255]. The `int16` cast prevents overflow — uint8 would wrap around (255 + 10 = 9 instead of 265 → 255).

**Rotation augmentation:** `cv2.getRotationMatrix2D(center, angle, scale)` creates a 2×3 affine transformation matrix for rotation around the center point. `cv2.BORDER_REFLECT` fills the exposed corners by reflecting image content (looks natural, avoids black borders that would confuse the classifier).

**Why these factors?**
- **Brightness:** Faces appear under dramatically different lighting (indoor fluorescent, outdoor sun, shadows, flash). A classifier trained only on one lighting condition would fail in others.
- **Rotation:** People naturally tilt their heads; cameras can be held at angles. Small rotations (±15°) simulate this without extreme distortion.

## Part C — Conceptual Questions (answered in code)

1. **Why resize to TARGET_SIZE?** FAST detects corners at a fixed scale. Different image sizes would produce different keypoint counts/distributions for the same content, making features incomparable.

2. **Why can't variable-size matrices go to classifiers?** Classifiers need fixed-length input. Each image produces a different number $K'$ of keypoints → $(K', 256)$ has varying rows. Mean pooling collapses to a fixed $(256,)$ vector.

3. **What's lost in mean pooling?** Spatial layout (WHERE features are), inter-keypoint relationships, and distinctive local patterns. Two very different images could have similar mean descriptors.

4. **How does k-NN work?** Given a (256,) query vector, k-NN computes Euclidean distance to all training vectors, picks the 5 closest, and predicts the majority class. Good for small datasets — no training to overfit, no distributional assumptions.

## Part D — Feature Extraction Code

```python
def extract_features(images, sigma=0.15):
    feature_matrix = []
    kp_counts      = []

    for img in images:

        # Step 1 — detect keypoints
        locs = corner_detection(img, sigma)
        if len(locs) == 0:
            feature_matrix.append(np.zeros(BRIEF_D))
            kp_counts.append(0)
            continue

        # Step 2 — compute BRIEF descriptors
        desc, locs = computeBrief(img, locs)
        if len(desc) == 0:
            feature_matrix.append(np.zeros(BRIEF_D))
            kp_counts.append(0)
            continue

        # Step 3 — mean pool (K', 256) → (256,)
        feature_vector = np.mean(desc, axis=0)
        feature_matrix.append(feature_vector)
        kp_counts.append(len(locs))

    feature_matrix = np.vstack(feature_matrix)  # (N, 256)
    return feature_matrix, kp_counts
```

### Explanation:

**Edge case handling is critical:**
- `corner_detection` might return 0 keypoints for very smooth images
- `computeBrief` filters out keypoints near the border — can reduce K to 0
- `np.mean` on an empty array produces `NaN`, which propagates silently through the classifier and corrupts all predictions
- The zero-vector fallback is safe — it represents "no interesting features found"

**Mean pooling equation:**
$$f_{image} = \frac{1}{K} \sum_{k=1}^{K} d_k \in \mathbb{R}^{256}$$

Each $d_k$ is a binary vector of 0s and 1s. After averaging, the result is a float vector where each dimension represents "what fraction of keypoints had a 1 at this bit position."

## Part D3 — Classifier Code

```python
def train_classifier(X_train, y_train):
    from sklearn.neighbors import KNeighborsClassifier

    # k=5: odd number avoids ties; small enough for our dataset
    classifier = KNeighborsClassifier(n_neighbors=5, metric='euclidean')

    classifier.fit(X_train, y_train)
    return classifier
```

### Why k-NN with k=5?

- **Non-parametric:** No assumptions about data distribution (unlike SVM which assumes linear separability or specific kernel shapes)
- **No overfitting risk in training:** k-NN is a "lazy learner" — it just stores the training data. Overfitting only manifests through too-small $k$
- **k=5:** Odd number prevents ties in binary classification. Small enough to be sensitive to local structure, large enough to be robust to noise. With 90 training images, 5 neighbors is ~5.5% of the dataset

## Part D5 — Prediction Code

```python
def predict_single_image(image_path, classifier):
    # 1. Load image
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Could not load image: {image_path}")

    # 2. Resize to TARGET_SIZE
    img = cv2.resize(img, (TARGET_SIZE[1], TARGET_SIZE[0]))

    # 3. Convert to grayscale (2D uint8)
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 4. Extract features
    feature_matrix, kp_counts = extract_features([img])

    # 5. Predict
    prediction = classifier.predict(feature_matrix)[0]
    class_names = ['face', 'no_face']
    class_name = class_names[prediction]

    # 6. Get confidence
    confidence = 0.0
    if hasattr(classifier, 'predict_proba'):
        proba = classifier.predict_proba(feature_matrix)[0]
        confidence = proba[prediction]

    return prediction, class_name, confidence
```

### Explanation:

This follows the exact same feature extraction pipeline used during training:
1. Load → 2. Resize → 3. Grayscale → 4. FAST + BRIEF + mean pool → 5. k-NN predict

**Confidence:** `predict_proba` for k-NN returns the fraction of neighbors voting for each class. So confidence of 0.8 means 4 out of 5 neighbors voted for the predicted class.

---

## Summary of All Files

| File | Question | What Was Implemented |
|------|----------|---------------------|
| `matchPics.py` | Q2.4 | Feature matching: grayscale → FAST → BRIEF → Hamming match |
| `briefRotTest.py` | Q2.5 | Rotation invariance test with histogram and 3 visualizations |
| `planarH.py` | Q2.6–Q2.8 | `computeH` (DLT), `computeH_norm` (normalized DLT), `computeH_ransac` (robust fitting), `compositeH` (warping + compositing) |
| `HarryPotterize.py` | Q2.9 | End-to-end book cover replacement |
| `ar.py` | Q3.1 | AR video overlay with aspect ratio cropping |
| `classify.py` | Q4.1 | Full ML pipeline: augmentation, feature extraction, k-NN classifier |
| `hw3.tex` | Q1.1, Q2.1–Q2.3 | Theory answers (DLT, FAST, BRIEF, Hamming) + all write-up sections |

# Feature Detection

## What is an Edge

An edge is a location in an image where:
- The image intensity changes rapidly.
- The gradient magnitude is large.

If $I(x, y)$ is the image, edges occur where the gradient $\nabla I = \left[\frac{\partial I}{\partial x}, \frac{\partial I}{\partial y}\right]$ is large.

**Edges are detected by measuring local intensity variation.**

---

## Edge Detection Using First Derivative

Edge detection can be performed by analyzing the first derivative of the image intensity function $f(x)$. The first derivative, $\frac{\partial f}{\partial x}$, measures how quickly the intensity changes at each point.

- When the intensity changes rapidly (such as at an edge), the first derivative exhibits a sharp peak or valley.
- The absolute value $\left|\frac{\partial f}{\partial x}\right|$ highlights these changes, making it easier to locate edges.

In the illustration:
- The top plot shows the original intensity function $f(x)$, which has a step-like change.
- The middle plot shows the first derivative $\frac{\partial f}{\partial x}$, which spikes at the locations of rapid intensity change (edges).
- The bottom plot shows the absolute value of the first derivative, which clearly marks the edge locations.

This method is fundamental in edge detection, as it directly identifies points of significant intensity variation.

---

## Edge Detection Using Image Gradients

To detect edges in a 2D image, we compute the gradients:
- The horizontal gradient $\frac{\partial I}{\partial x}$ measures intensity change in the x-direction.
- The vertical gradient $\frac{\partial I}{\partial y}$ measures intensity change in the y-direction.

From these gradients, we derive:
- **Edge strength**: The magnitude of the gradient vector, which quantifies how strong the edge is at each point:

$$
S = \|\nabla I\| = \sqrt{\left(\frac{\partial I}{\partial x}\right)^2 + \left(\frac{\partial I}{\partial y}\right)^2}
$$

- **Edge direction**: The orientation of the edge, given by:

$$
	heta = \tan^{-1}\left(\frac{\partial I}{\partial y} / \frac{\partial I}{\partial x}\right)
$$

These computations allow us to not only detect where edges are, but also how strong they are and in which direction they are oriented. This is crucial for many computer vision tasks, such as object detection and image segmentation.

---

## Edge Detection with Gradients in Digital Images

- In theory, an image is a continuous function $I(x, y)$, where $x$ and $y$ are spatial coordinates.
- In practice, a digital image is a grid of discrete pixel values, represented as $I[r, c]$, where $r$ is the row and $c$ is the column.

### Implications
- Derivatives do not exist analytically for digital images.
- Instead, derivatives must be approximated numerically.

### Estimating Intensity Change
- The goal is to estimate how intensity changes between neighboring pixels.
- In the discrete domain, derivatives are approximated using **finite differences**:

#### Horizontal Derivative
- Measures change along columns (horizontal gradient):
  $$
  I_x(r, c) \approx I(r, c+1) - I(r, c)
  $$
  or
  $$
  I_x(r, c) \approx \frac{I(r, c+1) - I(r, c-1)}{2}
  $$

#### Vertical Derivative
- Measures change along rows (vertical gradient):
  $$
  I_y(r, c) \approx I(r+1, c) - I(r, c)
  $$
  or
  $$
  I_y(r, c) \approx \frac{I(r+1, c) - I(r-1, c)}{2}
  $$

### What Do These Measure?
- Change along columns → horizontal gradient
- Change along rows → vertical gradient

**In a nutshell: gradients compare a pixel to its neighbors.** This allows us to estimate how the intensity changes locally, which is essential for detecting edges in digital images.

---

## The Nabla (∇) vs Delta (Δ) Symbols

The nabla symbol ($\nabla$) and the delta symbol ($\Delta$) are both used in mathematics, but they represent different concepts:

### Nabla ($\nabla$)
- The nabla symbol is used to denote the **gradient** (or other differential operators like divergence and curl) in vector calculus.
- In the context of images, $\nabla I$ represents the gradient of the image $I$, which is a vector of partial derivatives:
  $$
  \nabla I = \left[\frac{\partial I}{\partial x}, \frac{\partial I}{\partial y}\right]
  $$
- The gradient points in the direction of the greatest rate of increase of the function, and its magnitude indicates how steep the increase is.

### Delta ($\Delta$)
- The delta symbol is used to represent **change** or **difference**.
- In calculus, $\Delta x$ means a finite change in $x$ (not a derivative).
- In mathematics, $\Delta$ can also denote the Laplacian operator ($\Delta f$), which is the sum of second derivatives:
  $$
  \Delta f = \frac{\partial^2 f}{\partial x^2} + \frac{\partial^2 f}{\partial y^2}
  $$

### Summary
- $\nabla$ is used for gradients (first derivatives, vector-valued).
- $\Delta$ is used for finite differences or the Laplacian (second derivatives, scalar-valued).

In edge detection, $\nabla$ is most commonly used to find where intensity changes rapidly (edges).

### Example Quiz Question

**Question:**
Suppose you have a digital image represented as a grid of pixel values $I[r, c]$. If $I[3, 4] = 100$, $I[3, 5] = 120$, and $I[3, 3] = 90$, what is the horizontal gradient at pixel $(3, 4)$ using the central difference formula?

**Answer:**
The central difference formula for the horizontal gradient is:
$$
I_x(r, c) = \frac{I(r, c+1) - I(r, c-1)}{2}
$$
Plugging in the values:
$$
I_x(3, 4) = \frac{I(3, 5) - I(3, 3)}{2} = \frac{120 - 90}{2} = \frac{30}{2} = 15
$$

**Explanation:**
The horizontal gradient measures how much the intensity changes between the left and right neighbors of the pixel. A positive value (15) means the intensity increases as you move from left to right across pixel $(3, 4)$.

### Example Quiz Question (Vertical Gradient)

**Question:**
Suppose you have a digital image represented as a grid of pixel values $I[r, c]$. If $I[2, 4] = 80$, $I[3, 4] = 100$, and $I[4, 4] = 130$, what is the vertical gradient at pixel $(3, 4)$ using the central difference formula?

**Answer:**
The central difference formula for the vertical gradient is:
$$
I_y(r, c) = \frac{I(r+1, c) - I(r-1, c)}{2}
$$
Plugging in the values:
$$
I_y(3, 4) = \frac{I(4, 4) - I(2, 4)}{2} = \frac{130 - 80}{2} = \frac{50}{2} = 25
$$

**Explanation:**
The vertical gradient measures how much the intensity changes between the top and bottom neighbors of the pixel. A positive value (25) means the intensity increases as you move from top to bottom across pixel $(3, 4)$.

---

## How Gradient Location Is Determined

When calculating the gradient at a pixel, the method depends on how many neighboring pixels you consider:

- **Central difference (using 3 pixels):**
  If you have values at positions 2, 3, and 4, the gradient at position 3 is:
  $$
  \text{Gradient at 3} = \frac{\text{Value at 4} - \text{Value at 2}}{2}
  $$
  This estimates the change centered at pixel 3, using its immediate neighbors.

- **Forward difference (using adjacent pixels):**
  If you only consider adjacent pixels, the gradient at position 3 is:
  $$
  \text{Gradient at 3} = \text{Value at 4} - \text{Value at 3}
  $$
  This estimates the change from pixel 3 to pixel 4.

- **Backward difference:**
  Similarly, you could use:
  $$
  \text{Gradient at 3} = \text{Value at 3} - \text{Value at 2}
  $$

**Summary:**
- Central difference uses both neighbors and gives the gradient at the center pixel.
- Forward/backward difference uses only adjacent pixels and gives the gradient at the starting pixel.

If you want to check the change at pixel 4, you use its neighbors (for central difference: pixels 3 and 5; for forward difference: pixels 4 and 5).

---

## Gradients as Convolution Filters: The Prewitt Operator

Finite differences, which are used to approximate derivatives in digital images, can be implemented as **convolutions**. This means we can use small matrices (called kernels or filters) to scan across the image and compute gradients efficiently.

### The Prewitt Operator
- The **Prewitt operator** is a classic method for edge detection in image processing.
- It combines:
  - **Differentiation in one direction:** Measures how intensity changes (gradient) in either the horizontal or vertical direction.
  - **Averaging in the perpendicular direction:** Smooths the image to reduce noise, making the gradient calculation more robust.

### Prewitt Kernels
- The Prewitt operator uses two 3x3 kernels:

  - **Horizontal kernel ($G_x$):**
    $$
    G_x = \begin{bmatrix}
    -1 & 0 & 1 \\
    -1 & 0 & 1 \\
    -1 & 0 & 1
    \end{bmatrix}
    $$
    This kernel detects edges by measuring intensity change along columns (horizontal gradient).

  - **Vertical kernel ($G_y$):**
    $$
    G_y = \begin{bmatrix}
    -1 & -1 & -1 \\
     0 &  0 &  0 \\
     1 &  1 &  1
    \end{bmatrix}
    $$
    This kernel detects edges by measuring intensity change along rows (vertical gradient).

### Interpretation
- **Center difference → gradient:**
  - The middle column/row in the kernel is zero, so the filter computes the difference between the left/right or top/bottom neighbors, which is a central difference.
- **Vertical/horizontal averaging → smoothing:**
  - The kernel averages across the perpendicular direction, which helps reduce noise and makes the gradient calculation more stable.

### Why Use Prewitt?
- The Prewitt operator is simple, fast, and effective for detecting edges in images.
- It is less sensitive to noise than simple difference filters because of the built-in smoothing.
- It is often used as a first step in feature detection and image analysis tasks.

## Further Insights: Prewitt Operator and Kernel Relationship

### Are the Horizontal and Vertical Kernels Transposes?
The horizontal ($G_x$) and vertical ($G_y$) Prewitt kernels are not exact transposes of each other, but they are closely related:
- $G_x$ emphasizes changes along columns (horizontal edges), while $G_y$ emphasizes changes along rows (vertical edges).
- $G_x$ has zeros in the middle column, $G_y$ has zeros in the middle row.
- If you transpose $G_x$, you get a kernel similar to $G_y$, but not identical. The structure is designed to combine differentiation in one direction and averaging in the perpendicular direction.

### Beyond the Slides: Prewitt Operator in Practice
- **Noise Robustness:** The Prewitt operator is more robust to noise than simple difference filters because it averages across three pixels in the perpendicular direction. This smoothing helps reduce the effect of random noise.
- **Edge Orientation:** By applying $G_x$ and $G_y$ separately, you can detect edges in both horizontal and vertical directions. Combining their outputs gives the overall edge magnitude and direction.
- **Comparison to Sobel:** The Sobel operator is similar to Prewitt but gives more weight to the center pixels. Prewitt is simpler and sometimes preferred for speed and simplicity.
- **Applications:** Prewitt is used in:
  - Early stages of feature detection
  - Image segmentation
  - Object boundary detection
  - Texture analysis
- **Limitations:**
  - Prewitt is not rotation invariant; it only detects edges aligned with the axes.
  - It may miss diagonal edges unless combined with other kernels.

### Mathematical Formulation
For an image $I$, the Prewitt response at pixel $(r, c)$ is:
$$
G_x * I(r, c) = \sum_{i=-1}^{1} \sum_{j=-1}^{1} G_x[i, j] \cdot I(r+i, c+j)
$$
$$
G_y * I(r, c) = \sum_{i=-1}^{1} \sum_{j=-1}^{1} G_y[i, j] \cdot I(r+i, c+j)
$$
where $*$ denotes convolution.

### Summary
- Prewitt kernels are not exact transposes, but are designed for orthogonal edge detection.
- The operator is robust, simple, and widely used for basic edge detection tasks.

---

## The Sobel Operator

The **Sobel operator** is very similar to the Prewitt operator but uses a slightly different kernel to provide more emphasis on the central pixels closer to the point of interest.

### Why the difference?
The Sobel operator can be thought of as a combination of:
1.  **Differentiation:** A central difference approximation (like Prewitt).
2.  **Smoothing:** A Gaussian smoothing filter (approximated by `[1, 2, 1]`) instead of a simple box average (like Prewitt's `[1, 1, 1]`).

This weighted averaging (giving the center pixel a weight of 2) makes the Sobel operator slightly less sensitive to noise than the Prewitt operator.

### Sobel Kernels
The standard 3x3 Sobel kernels are:

- **Horizontal Kernel ($G_x$):**
  $$
  G_x = \begin{bmatrix}
  -1 & 0 & 1 \\
  -2 & 0 & 2 \\
  -1 & 0 & 1
  \end{bmatrix}
  $$
  This measures the gradient in the horizontal direction ($x$). Notice the middle row is weighted by 2.

- **Vertical Kernel ($G_y$):**
  $$
  G_y = \begin{bmatrix}
  -1 & -2 & -1 \\
   0 &  0 &  0 \\
   1 &  2 &  1
  \end{bmatrix}
  $$
  This measures the gradient in the vertical direction ($y$). Notice the middle column is weighted by 2.

---

## Practice Questions: Sobel and Prewitt Operators

Below are examples of how to apply these operators manually. These types of questions test your understanding of convolution and gradient calculation.

### Question 1: Calculating Gradient with Sobel
**Problem:**
Consider the following 3x3 image patch representing pixel intensities:
$$
\begin{bmatrix}
10 & 50 & 10 \\
20 & 50 & 20 \\
10 & 50 & 10
\end{bmatrix}
$$
Calculate the horizontal gradient response ($G_x$) and the vertical gradient response ($G_y$) for the **center pixel** using the Sobel operator. Then, determine the gradient magnitude.

**Solution:**

**Step 1: Apply Sobel Horizontal Kernel ($G_x$)**
$$
G_x = \begin{bmatrix} -1 & 0 & 1 \\ -2 & 0 & 2 \\ -1 & 0 & 1 \end{bmatrix}
$$
Overlay $G_x$ on the image patch and perform element-wise multiplication and sum (convolution):
$$
\begin{aligned}
Value &= (-1 \times 10) + (0 \times 50) + (1 \times 10) \\
      &+ (-2 \times 20) + (0 \times 50) + (2 \times 20) \\
      &+ (-1 \times 10) + (0 \times 50) + (1 \times 10)
\end{aligned}
$$
Calculation:
- Top row: $-10 + 0 + 10 = 0$
- Middle row: $-40 + 0 + 40 = 0$
- Bottom row: $-10 + 0 + 10 = 0$
- **Total $G_x = 0$**

**Step 2: Apply Sobel Vertical Kernel ($G_y$)**
$$
G_y = \begin{bmatrix} -1 & -2 & -1 \\ 0 & 0 & 0 \\ 1 & 2 & 1 \end{bmatrix}
$$
Overlay $G_y$ on the image patch:
$$
\begin{aligned}
Value &= (-1 \times 10) + (-2 \times 50) + (-1 \times 10) \\
      &+ (0 \times 20) + (0 \times 50) + (0 \times 20) \\
      &+ (1 \times 10) + (2 \times 50) + (1 \times 10)
\end{aligned}
$$
Calculation:
- Top row (negative weights): $-10 - 100 - 10 = -120$
- Middle row (zeros): $0$
- Bottom row (positive weights): $10 + 100 + 10 = 120$
- **Total $G_y = -120 + 120 = 0$**

**Result:**
Both gradients are 0. This makes sense because the image patch is symmetric around the center in both directions (a bright vertical line in the middle).

---

### Question 2: Comparing Prewitt and Sobel
**Problem:**
Consider this 3x3 patch containing a diagonal edge:
$$
\begin{bmatrix}
0 & 0 & 100 \\
0 & 100 & 100 \\
100 & 100 & 100
\end{bmatrix}
$$
Calculate the horizontal gradient ($G_x$) for the center pixel using both **Prewitt** and **Sobel** operators.

**Solution:**

**1. Using Prewitt Operator ($G_x$)**
Kernel: $\begin{bmatrix} -1 & 0 & 1 \\ -1 & 0 & 1 \\ -1 & 0 & 1 \end{bmatrix}$

Calculation:
$$
\begin{aligned}
G_x &= (-1 \times 0) + (0 \times 0) + (1 \times 100) \\
    &+ (-1 \times 0) + (0 \times 100) + (1 \times 100) \\
    &+ (-1 \times 100) + (0 \times 100) + (1 \times 100)
\end{aligned}
$$
- Row 1: $0 + 0 + 100 = 100$
- Row 2: $0 + 0 + 100 = 100$
- Row 3: $-100 + 0 + 100 = 0$
- **Total Prewitt $G_x = 200$**

**2. Using Sobel Operator ($G_x$)**
Kernel: $\begin{bmatrix} -1 & 0 & 1 \\ -2 & 0 & 2 \\ -1 & 0 & 1 \end{bmatrix}$

Calculation:
$$
\begin{aligned}
G_x &= (-1 \times 0) + (0 \times 0) + (1 \times 100) \\
    &+ (-2 \times 0) + (0 \times 100) + (2 \times 100) \\
    &+ (-1 \times 100) + (0 \times 100) + (1 \times 100)
\end{aligned}
$$
- Row 1: $100$ (Weight 1)
- Row 2: $200$ (Weight 2)
- Row 3: $0$ (Weight 1)
- **Total Sobel $G_x = 300$**

**Analysis:**
The Sobel operator produces a higher magnitude (300 vs 200) because it weights the central row's strong contrast ($0 \to 100$) more heavily (weight of 2) than Prewitt (weight of 1).

---

### Question 3: Gradient Magnitude and Direction
**Problem:**
After applying the Sobel operator to a pixel, you obtain:
- $G_x = 40$
- $G_y = 30$

Calculate the Gradient Magnitude and Gradient Orientation (Direction).

**Solution:**

**1. Gradient Magnitude ($S$)**
Formula: $S = \sqrt{G_x^2 + G_y^2}$
$$
S = \sqrt{40^2 + 30^2} = \sqrt{1600 + 900} = \sqrt{2500} = 50
$$

**2. Gradient Direction ($\theta$)**
Formula: $\theta = \tan^{-1}\left(\frac{G_y}{G_x}\right)$
$$
\theta = \tan^{-1}\left(\frac{30}{40}\right) = \tan^{-1}(0.75) \approx 36.87^\circ
$$
This means the edge is oriented at approximately $37^\circ$ relative to the horizontal axis (or the gradient points in that direction perpendicular to the edge).

---

## Edge Thresholding

Once you have calculated the gradient magnitude $\|\nabla I\|$ for every pixel, you have a "gradient image" where bright pixels act like potential edges. However, you still need to make a binary decision: **Is this pixel an edge or not?**

This is done via thresholding.

### 1. Standard (Single) Thresholding
The simplest approach using a single threshold value $T$.

- **Rule:**
  - If $\|\nabla I(x, y)\| < T \implies$ **Not an Edge** (discard).
  - If $\|\nabla I(x, y)\| \ge T \implies$ **Definitely an Edge** (keep).

- **The Problem:**
  - If $T$ is too set **high**, you miss faint edges (broken lines).
  - If $T$ is set too **low**, you get too much noise (spurious edges).
  - It's very hard to find one "magic number" that works for the whole image.

### 2. Hysteresis Thresholding (Double Thresholding)
This is a more robust technique used in algorithms like the **Canny Edge Detector**. It uses **two** thresholds: a low threshold $T_{low}$ and a high threshold $T_{high}$.

- **Logic:**
  1.  **Strong Edges:** Pixels with $\|\nabla I\| \ge T_{high}$ are definitely edges.
  2.  **No Edges:** Pixels with $\|\nabla I\| < T_{low}$ are definitely noise (discarded).
  3.  **Weak Edges:** Pixels where $T_{low} \le \|\nabla I\| < T_{high}$ are "maybe" edges.

- **The "Hysteresis" Rule:**
  - A **weak edge** is kept ONLY if it is connected (neighboring) to a **strong edge**.
  - If a weak edge is isolated (surrounded by non-edges), it is removed.

- **Why is this better?**
  - It allows us to track faint lines that belong to a main contour (like the fading tail of an object's outline) without picking up random unconnected noise elsewhere in the image.

---

## Edge Detection: Second Derivative

So far, we have looked at the **first derivative** (gradient), where edges appear as **peaks** (maxima).
We can also find edges using the **second derivative**, where edges appear as **zero-crossings**.

### The Intuition

Imagine scanning a single line of an image where there is a step edge (dark to bright).

1.  **Intensity function ($f(x)$):** Looks like a ramp or step up.
2.  **First Derivative ($f'(x)$):** Measures the rate of change.
    - At the start of the edge, the slope goes up.
    - At the steepest point mid-edge, the slope is maximum (**Peak**).
    - At the end of the edge, the slope goes back down.
3.  **Second Derivative ($f''(x)$):** Measures the *change in the slope*.
    - As the slope increases (start of edge), $f''(x)$ is positive.
    - At the peak of $f'(x)$ (steepest point), the slope stops changing momentarily, so **$f''(x) = 0$**.
    - As the slope decreases (end of edge), $f''(x)$ is negative.

### Conclusion
- **Edges correspond to Extrema (Peaks) of the First Derivative.**
- **Edges correspond to Zero-Crossings of the Second Derivative.**

Finding where the second derivative value crosses from positive to negative (the "zero-crossing") allows for very precise localization of the edge center.

### The Laplacian Operator ($\nabla^2 f$)
To calculate the second derivative in 2D, we use the **Laplacian** operator:
$$
\nabla^2 f = \frac{\partial^2 f}{\partial x^2} + \frac{\partial^2 f}{\partial y^2}
$$
Just like Sobel approximates the first derivative, we have kernels to approximate the Laplacian. A common 3x3 Laplacian kernel is:
$$
\begin{bmatrix}
0 & 1 & 0 \\
1 & -4 & 1 \\
0 & 1 & 0
\end{bmatrix}
$$
(Note that the sum of elements is 0, ensuring that regions of constant intensity have a 0 response).

### Discrete Laplacian Kernels
In digital images, we cannot calculate true derivatives, so we approximate them using convolution kernels. Common 3x3 kernels for the Laplacian include:

**1. 4-Connectivity Kernel:**
Only considers vertical and horizontal neighbors.
$$
\begin{bmatrix}
0 & 1 & 0 \\
1 & -4 & 1 \\
0 & 1 & 0
\end{bmatrix}
$$

**2. 8-Connectivity Kernel:**
Considers all 8 neighbors (including diagonals), giving a more isotropic response.
$$
\begin{bmatrix}
1 & 1 & 1 \\
1 & -8 & 1 \\
1 & 1 & 1
\end{bmatrix}
$$
*Key observation:* In both cases, the central pixel is negative (or positive), and the surrounding pixels have the opposite sign. The sum of all elements is always **zero**, meaning that in a purely flat (constant color) region, the response is zero.

---

## The Problem: Noise Sensitivity

While the second derivative is powerful for finding the exact center of an edge (zero-crossing), it has a major weakness: **It is extremely sensitive to noise.**

### Why?
1.  **Gradient (1st derivative):** Amplifies noise somewhat. If a signal jitters slightly, the slope changes.
2.  **Laplacian (2nd derivative):** Measures the *change* in the slope. High-frequency noise (rapid jitter) causes the slope to change direction wildly.
    - As a result, the second derivative of a noisy signal is often just a mess of huge spikes, identifying "edges" everywhere.

*Visually:* If $f(x)$ is a noisy step function, $f'(x)$ is a bumpy peak, but $f''(x)$ is a chaotic oscillation that obscures the true zero-crossing.

---

## The Solution: Laplacian of Gaussian (LoG)

To fix the noise problem, we must **smooth** the image before calculating the second derivative.

**The Strategy:**
1.  **Smooth:** Apply a Gaussian filter ($G_\sigma$) to remove noise.
2.  **Derive:** Apply the Laplacian ($\nabla^2$) to detect edges.

Mathematically, we want to calculate:
$$
\nabla^2 (G_\sigma * I)
$$
Where $I$ is the image and $G_\sigma$ is the Gaussian kernel.

### The "LoG" Operator
Because convolution is associative, we can combine these steps into a single operator! instead of smoothing the image and *then* differentiating, we can differentiate the Gaussian kernel itself and *then* convolve it with the image.
$$
\nabla^2 (G_\sigma * I) = (\nabla^2 G_\sigma) * I
$$

The term $(\nabla^2 G_\sigma)$ is called the **Laplacian of Gaussian (LoG)** operator.

- **Shape:** It looks like a "Mexican Hat" (or an inverted sombrero).
  - It has a positive central peak (checking for a "blob").
  - It is surrounded by a negative ring (checking for the surrounding average).
  - It fades to zero at the edges.

**Benefits of LoG:**
- **Robustness:** The Gaussian part suppresses high-frequency noise.
- **Localization:** The Laplacian part finds the precise edge location via zero-crossings.
- **Tunable:** You can adjust the Gaussian width ($\sigma$) to detect edges at different scales (fine details vs. coarse outlines).

---

## Example Scenario: Hysteresis in Action

**Scenario:**
You are detecting edges on a cat. The cat's outline is strong, but the tail fades into the background shadow.
- $T_{high} = 100$
- $T_{low} = 50$

**Pixels:**
1.  **Pixel A (Back of cat):** Gradient = 120.
    - Result: **Strong Edge** (Keep).
2.  **Pixel B (Background noise):** Gradient = 60.
    - Result: Weak Edge. Is it connected to a strong edge? No. **Discard.**
3.  **Pixel C (Tail tip):** Gradient = 60.
    - Result: Weak Edge.
    - However, Pixel C is neighbor to Pixel D (Gradient 70), which neighbors Pixel E (Gradient 110).
    - Because Pixel C is part of a chain connecting to a Strong Edge (Pixel E), we **Keep** it.

This preserves the tail (C) while removing the noise (B), even though they had the same gradient strength!

---

# Feature Detection Quiz

Test your understanding with these 20 practice questions. Try to answer them before checking the solutions below.

## Concept & Gradient Questions

1.  **What characteristic primarily defines an "edge" in an image?**
    a) A region of constant high intensity.
    b) A rapid change in image intensity.
    c) A region with zero gradient.
    d) A pixel with a value of 255.

2.  **The gradient of an image $\nabla I$ is a vector. What does its direction point to?**
    a) Along the edge.
    b) In the direction of greatest intensity increase.
    c) In the direction of greatest intensity decrease.
    d) Always towards the top-left corner.

3.  **If an edge is a vertical line (dark on left, bright on right), what is the direction of the gradient vector?**
    a) Horizontal ($0^\circ$).
    b) Vertical ($90^\circ$).
    c) Diagonal ($45^\circ$).
    d) Undefined.

4.  **Which finite difference formula uses the values $I(x+1)$ and $I(x-1)$ to estimate the derivative at $x$?**
    a) Forward difference.
    b) Backward difference.
    c) Central difference.
    d) Gaussian difference.

5.  **Calculate the Gradient Magnitude:** If $\frac{\partial I}{\partial x} = 3$ and $\frac{\partial I}{\partial y} = 4$, what is the gradient magnitude?
    a) 5
    b) 7
    c) 12
    d) 25

## Kernels & Operators

6.  **Identify this kernel:** $\begin{bmatrix} -1 & 0 & 1 \\ -1 & 0 & 1 \\ -1 & 0 & 1 \end{bmatrix}$
    a) Sobel Horizontal
    b) Prewitt Horizontal
    c) Laplacian
    d) Gaussian

7.  **Identify this kernel:** $\begin{bmatrix} -1 & -2 & -1 \\ 0 & 0 & 0 \\ 1 & 2 & 1 \end{bmatrix}$
    a) Sobel Horizontal ($G_x$)
    b) Sobel Vertical ($G_y$)
    c) Prewitt Vertical ($G_y$)
    d) Laplacian

8.  **What is the main advantage of the Sobel operator over the Prewitt operator?**
    a) It is faster to compute.
    b) It provides better noise smoothing by weighting the central pixels.
    c) It detects diagonal edges perfectly.
    d) It calculates the second derivative.

9.  **Why must the sum of elements in a derivative kernel (like Prewitt or Sobel) typically be zero?**
    a) To ensure the output is zero in constant/flat regions.
    b) To make the kernel invertible.
    c) To prevent integer overflow.
    d) It is just a convention with no mathematical reason.

10. **A "box filter" (averaging filter) is used for:**
    a) Sharpening.
    b) Edge detection.
    c) Smoothing/Blurring.
    d) Increasing contrast.

## Thresholding & Hysteresis

11. **In Single Thresholding, if you set the threshold $T$ too low, what happens?**
    a) You miss important edges.
    b) You get broken, disconnected edges.
    c) You detect too many spurious edges (noise).
    d) The image becomes black.

12. **In Hysteresis Thresholding (used in Canny), a "weak" edge pixel is kept ONLY if:**
    a) Its gradient is above $T_{high}$.
    b) It is connected to a "strong" edge pixel.
    c) It is connected to another "weak" edge pixel.
    d) It is in the center of the image.

13. **What is the purpose of using two thresholds ($T_{low}, T_{high}$) instead of one?**
    a) To separate horizontal and vertical edges.
    b) To improve speed.
    c) To link faint edges to strong edges while rejecting isolated noise.
    d) To color code the edges.

## Second Derivative & Laplacian

14. **In the First Derivative, an edge appears as a peak (extremum). How does it appear in the Second Derivative?**
    a) A peak.
    b) A flat line.
    c) A zero-crossing.
    d) A step function.

15. **Which operator approximates the Second Derivative in 2D?**
    a) Sobel
    b) Prewitt
    c) Laplacian
    d) Gaussian

16. **Why is the raw Laplacian operator rarely used directly on natural images?**
    a) It is too computationally expensive.
    b) It is extremely sensitive to noise.
    c) It cannot detect horizontal edges.
    d) It always returns zero.

17. **What does "LoG" stand for?**
    a) Logarithm of Gradients.
    b) Laplacian of Gaussian.
    c) Linear on Grid.
    d) Level of Grey.

18. **The shape of the LoG operator is often described as:**
    a) A pyramid.
    b) A Mexican hat (inverted sombrero).
    c) A box.
    d) A saddle.

19. **What is the first step in the LoG process?**
    a) Calculate the Laplacian.
    b) Threshold the image.
    c) Smooth the image with a Gaussian.
    d) Invert the image colors.

20. **Which parameter in the LoG operator controls the scale of edges detected?**
    a) The threshold $T$.
    b) The Gaussian sigma ($\sigma$).
    c) The kernel size ($3 \times 3$ vs $5 \times 5$).
    d) The image resolution.

---

## Quiz Answers & Explanations

1.  **b)** A rapid change in image intensity.
2.  **b)** In the direction of greatest intensity increase (from dark to bright).
3.  **a)** Horizontal ($0^\circ$). Standard convention measures angle from the x-axis. A vertical edge has a horizontal gradient.
4.  **c)** Central difference. (Uses both left and right neighbors).
5.  **a)** 5. Formula: $\sqrt{3^2 + 4^2} = \sqrt{9+16} = \sqrt{25} = 5$.
6.  **b)** Prewitt Horizontal (measures change in horizontal direction, weights are all 1).
7.  **b)** Sobel Vertical. (Measures vertical change, notice the 2 in the middle column derivative). Wait—correction: The matrix shown is $\begin{bmatrix} -1 & -2 & -1 \\ 0 & 0 & 0 \\ 1 & 2 & 1 \end{bmatrix}$. This differentiates in the **vertical** direction (rows change from - to +). So it is $G_y$.
8.  **b)** It provides better noise smoothing by weighting the central pixels (1-2-1 vs 1-1-1).
9.  **a)** To ensure the output is zero in constant/flat regions. (Derivative of a constant is 0).
10. **c)** Smoothing/Blurring.
11. **c)** You detect too many spurious edges (noise).
12. **b)** It is connected to a "strong" edge pixel.
13. **c)** To link faint edges to strong edges while rejecting isolated noise.
14. **c)** A zero-crossing. (Slope goes from positive increasing to positive decreasing, crossing zero rate of change of slope).
15. **c)** Laplacian.
16. **b)** It is extremely sensitive to noise. (2nd derivative amplifies high freq noise).
17. **b)** Laplacian of Gaussian.
18. **b)** A Mexican hat.
19. **c)** Smooth the image with a Gaussian (to reduce noise before differentiating).
20. **b)** The Gaussian sigma ($\sigma$). Larger sigma = coarser scale (blurry edges), Smaller sigma = fine scale.
# CV Course Notes - Image Pyramids and Merging
**Ref:** `3 Image Pyramid and Merging.pdf`

---

## Topic: Aliasing (The Problem with Under-Sampling)

### What is a Signal?
![Original Signal](uploaded_media_3_1770017673290.png)

- **$f(x)$**: A continuous signal (like a sine wave). 
- In images, this represents the **intensity variations** across pixels.
- High-frequency signals = rapid changes (fine details, sharp edges).

### The Sampling Process
![Sampling f(x)](uploaded_media_0_1770017673290.png)

- **Sampling**: Taking discrete measurements (red dots) from the continuous signal at regular intervals.
- **The Problem Here**: The sampling rate is **too low** for this high-frequency wave.
- Notice: All the red dots happen to land near the same value (the zero-crossing). This gives a misleading picture of the signal.

### What Goes Wrong: Under-Sampling
![Bad Samples](uploaded_media_2_1770017673290.png)

- With a different phase or slightly different sampling positions, the red dots now land at various heights.
- **But still**: If you tried to reconstruct the signal from just these dots, you wouldn't get the original high-frequency wave back.

### The "Alias" Appears
![Alias Appears](uploaded_media_1_1770017673290.png)

- **$g(x)$** (red curve): A **low-frequency** wave that **also passes through the exact same sample points**.
- This is the "alias" – a completely different signal that looks identical when sampled at this rate.

### Aliasing Explained
![Aliasing](uploaded_media_4_1770017673290.png)

- **Definition**: $g(x)$ is an **alias** of $f(x)$.
- When you under-sample a high-frequency signal, you **cannot distinguish it from a lower-frequency signal**.
- **Result in Images**: 
  - Jagged edges (instead of smooth lines).
  - Moiré patterns (weird stripes/interference).
  - Loss of fine detail.

### The Nyquist Theorem (The Solution)
![Nyquist Rate](uploaded_media_2_1770018177521.png)

**Side-by-Side Comparison:**
| Left (BAD) | Right (GOOD) |
|------------|--------------|
| < 1 sample per cycle | > 10 samples per cycle |
| Red alias appears | Samples follow the wave |

**The Rule:**
> **Sample at least 2x the highest frequency in the signal.**

$$f_s \geq 2 \cdot f_{max}$$

- $f_s$ = Sampling frequency.
- $f_{max}$ = Highest frequency in the signal.
- This minimum rate is called the **Nyquist Rate**.

### No Aliasing Example
![No Aliasing](uploaded_media_1_1770018177521.png)

- Here, we have a **low-frequency** signal $f(x)$.
- We sample it with **many points** (high sampling rate).
- Result: $g(x) \approx f(x)$ — the reconstructed signal matches the original!
- **No aliasing** because we have ≥ 2 samples per cycle.

### But What About Non-Sine Waves?
![Fourier Transform](uploaded_media_3_1770018177521.png)

**The Question:** "This only works for sine waves, right?"

**The Answer:** No! Thanks to the **Fourier Transform**:
- **Any signal** (even weird square waves, spikes, etc.) can be decomposed into a **weighted sum of sines and cosines**.
- So, find the **highest frequency component** in that sum.
- Sample at ≥ 2x that frequency.

**Key Insight:**
- Complex signals = many frequencies added together.
- Nyquist applies to the **maximum frequency present**.
- In images: sharp edges = high frequencies → need high sampling rate.

### Fourier Series: Building Complex Signals from Sines
![Fourier Series](uploaded_media_1770020311070.png)

**The Idea:**
- **Left (Target):** A square wave. Sharp edges, definite not a sine wave.
- **Right (Decomposition):**
  - Low-frequency sine (the big wave).
  - High-frequency sine (the small, fast wave).
  - **Sum them → you get something that looks like the square wave!**

**Why This Matters:**
1.  Any signal (image row, audio, etc.) = **sum of sines at different frequencies**.
2.  Sharp edges (like the square wave's vertical edges) require **high-frequency sines**.
3.  To capture those edges when sampling → you need to sample at **≥ 2x the highest frequency**.

**In Practice:**
- More sines added → better approximation of the square wave.
- The "infinite Fourier Series" perfectly reconstructs the square wave.
- For images: sharp edges = many high-frequency components.

### Practical Implication for Images
Before **downsampling** an image (reducing resolution):
1.  **Blur first** (Low-pass filter / Gaussian).
2.  This removes the high-frequency content that would cause aliasing.
3.  **Then** sample (reduce pixels).

---

## Topic: Image Resizing (Downsampling & Upsampling)

### The Problem with Naive Resizing
![Image Resizing Van Gogh](uploaded_media_0_1770020813148.png)

| 1/2 Size | 1/4 Size (2x zoom) | 1/8 Size (4x zoom) |
|----------|--------------------|--------------------|
| Looks okay | Getting noisy | Very blocky/aliased |

**Observation:** As we downsample more aggressively, we lose detail and get **aliasing artifacts** (blocky, noisy appearance).

### Downsampling (Reducing Resolution)
![Downsampling](uploaded_media_1_1770020813148.png)

**What it means:** Taking fewer pixels from the original.
- Example: Keep every 2nd pixel, throw away the rest.
- **Problem:** If the original has high frequencies (fine details), they get aliased.

**Naive approach:**
```
Original: [p1, p2, p3, p4, p5, p6, p7, p8]
Downsample 2x: [p1, p3, p5, p7]  (skip every other pixel)
```

### Upsampling (Increasing Resolution)
![Upsampling](uploaded_media_2_1770020813148.png)

**What it means:** Adding more pixels than you originally had.
- Example: Double the resolution.
- **Problem:** Where do the new pixels come from? You have to **interpolate** (guess).

**Naive approach:**
```
Original: [p1, p2, p3, p4]
Upsample 2x: [p1, ?, p2, ?, p3, ?, p4, ?]  (fill in gaps)
```

### Interpolation for Upsampling
![Interpolation](uploaded_media_3_1770020813148.png)

- **$v[n]$** (top): The sparse original samples.
- **$y[n]$** (bottom): The upsampled signal with interpolated values.

**Methods to fill the gaps:**
1. **Nearest Neighbor:** Copy the closest pixel. (Blocky result.)
2. **Bilinear:** Average of nearby pixels. (Smoother.)
3. **Bicubic:** Weighted average using more neighbors. (Even smoother.)

### Linear Interpolation Formula
![Linear Interpolation](uploaded_media_1770020972823.png)

**Left Grid (Original 3x3):**
```
5  7  8
4  7  8
3  2  1
```

**Right Grid (Upsampled, gaps to fill):**
```
5  ?  ?  8
4  ?  ?  8
?  ?  ?  ?
3  ?  ?  1
```

**The Formula:**
$$y = y_0 + \frac{y_1 - y_0}{x_1 - x_0} (x - x_0)$$

**In Plain English:**
- You have two known values: $y_0$ (left neighbor) and $y_1$ (right neighbor).
- You want to find $y$ at position $x$ (somewhere in between).
- **Slope:** $(y_1 - y_0) / (x_1 - x_0)$ = how fast the value changes.
- **Result:** Start at $y_0$, then add the slope times how far you've moved from $x_0$.

**Example:**
- $y_0 = 5$ (at position $x_0 = 0$)
- $y_1 = 8$ (at position $x_1 = 3$)
- What's the value at $x = 1$?
- $y = 5 + \frac{8-5}{3-0}(1-0) = 5 + 1 = 6$

### Full Calculation: Bilinear Interpolation (Correct Method)

**The "?" we want to find is surrounded by 4 known values:**
```
5 --- 7       (from original row 1)
|  ?  |
4 --- 7       (from original row 2)
```

**Step 1: Horizontal Interpolation (Top Row)**
- Left: $5$, Right: $7$, midpoint position.
$$\text{Top} = \frac{5 + 7}{2} = 6$$

**Step 2: Horizontal Interpolation (Bottom Row)**
- Left: $4$, Right: $7$, midpoint position.
$$\text{Bottom} = \frac{4 + 7}{2} = 5.5$$

**Step 3: Vertical Interpolation (Between the two results)**
- Top result: $6$, Bottom result: $5.5$, midpoint position.
$$? = \frac{6 + 5.5}{2} = \boxed{5.75}$$

**Summary:**
1. Find the **4 corners** surrounding the missing pixel.
2. **Horizontal interpolation** on top row → one value.
3. **Horizontal interpolation** on bottom row → one value.
4. **Vertical interpolation** between those two → final answer.

*This is called **Bilinear Interpolation** because we interpolate in two directions (horizontal + vertical).*

---

## Topic: Multi-Resolution Image Pyramids

### What is an Image Pyramid?
![Multi-Resolution Pyramid](uploaded_media_0_1770021636337.png)

An **Image Pyramid** is a collection of the same image at **different resolutions**, stacked like a pyramid.

| Level | Name | Resolution | # Pixels |
|-------|------|------------|----------|
| $l = 0$ | Fine (Original) | $W \times H$ | $W \cdot H$ |
| $l = 1$ | Medium | $\frac{W}{2} \times \frac{H}{2}$ | $\frac{1}{4}$ of original |
| $l = 2$ | Coarse | $\frac{W}{4} \times \frac{H}{4}$ | $\frac{1}{16}$ of original |

**Key Insight:** Each level has **half the width and height** of the previous level, so **1/4 the total pixels**.

### Why Use Pyramids?
1. **Coarse-to-Fine Matching:** Start matching at low resolution (fast, rough), then refine at high resolution.
2. **Optical Flow:** Track motion at multiple scales.
3. **Stereo Vision:** Match left/right images efficiently.
4. **Image Blending:** Seamlessly merge images (we'll see this later!).
5. **Deep Neural Networks:** CNNs naturally create "feature pyramids" at different scales.

---

## Topic: The Gaussian Pyramid

### What is a Gaussian Pyramid?
![Gaussian Pyramid](uploaded_media_1_1770021636337.png)

A **Gaussian Pyramid** is built by repeatedly:
1. **Blurring** the image (with a Gaussian filter).
2. **Downsampling** (keeping every other pixel).

**Why "Gaussian"?** Because we use a **Gaussian blur** before downsampling to avoid aliasing!

**The Frequency Diagram (Right Side):**
- The circle represents the **frequency content** of the image.
- As we go up the pyramid (smaller images), the circle **shrinks**.
- This means: higher levels have **less high-frequency detail** (smoother).

### Building a Gaussian Pyramid: Step-by-Step
![Gaussian Pyramid Steps](uploaded_media_2_1770021636337.png)

#### Step 1: Level 0 (Original)
- Start with the original image: $G_0$.
- This is the **finest resolution** (all details present).

#### Step 2: Gaussian Smoothing (Anti-Aliasing)
- Convolve with a Gaussian kernel $g_\sigma$:
$$\tilde{G}_k = g_\sigma * G_k$$
- **Purpose:** Remove high frequencies that would cause aliasing when we downsample.
- This is the **blur-before-resize** rule we learned earlier!

##### The Gaussian Kernel (How to Blur)

**$3 \times 3$ Gaussian Kernel:**
$$g_\sigma = \frac{1}{16} \begin{bmatrix} 1 & 2 & 1 \\ 2 & 4 & 2 \\ 1 & 2 & 1 \end{bmatrix}$$

**$5 \times 5$ Gaussian Kernel:**
$$g_\sigma = \frac{1}{256} \begin{bmatrix} 1 & 4 & 6 & 4 & 1 \\ 4 & 16 & 24 & 16 & 4 \\ 6 & 24 & 36 & 24 & 6 \\ 4 & 16 & 24 & 16 & 4 \\ 1 & 4 & 6 & 4 & 1 \end{bmatrix}$$

**Properties:**
- Center has **highest weight** (the pixel itself matters most).
- Weights decrease outward (neighbors matter less).
- All weights sum to **1** (preserves brightness).

##### Applying the Blur: Convolution!
Same sliding window operation from Lecture 2:
$$\tilde{G}(i,j) = \sum_{k,l} G(i+k, j+l) \cdot g(k,l)$$

```python
# Python Example
from scipy.ndimage import convolve

gaussian_kernel = (1/16) * np.array([
    [1, 2, 1],
    [2, 4, 2],
    [1, 2, 1]
])

blurred = convolve(image, gaussian_kernel)
downsampled = blurred[::2, ::2]  # Keep every other pixel
```

#### Step 3: Downsampling
- Keep every other pixel (subsample by factor of 2):
$$G_{k+1}(x, y) = \tilde{G}_k(2x, 2y)$$
- **Result:** Image size becomes $\frac{1}{2}$ width × $\frac{1}{2}$ height = $\frac{1}{4}$ pixels.

#### Step 4: Repeat
- Apply Steps 2-3 again to build $G_1, G_2, G_3, ...$
- Each level is **smaller** and **smoother** than the previous.

### Summary: The Gaussian Pyramid Recipe
```
G_0 = Original Image

For k = 0, 1, 2, ...:
    1. Blur:      G̃_k = Gaussian * G_k
    2. Downsample: G_{k+1} = G̃_k[::2, ::2]  (every other pixel)
```

**Properties:**
- Level 0: Full detail, full size.
- Level k: Less detail, $\frac{1}{2^k}$ width/height, $\frac{1}{4^k}$ pixels.
- **No aliasing** because we blur first!

---

## Topic: The Laplacian Pyramid (Capturing Lost Details)

### The Big Idea
![Laplacian Concept](uploaded_media_0_1770022601067.png)

**Problem with Gaussian Pyramid:**
- When we blur and downsample, we **lose high-frequency details** (edges, textures).
- We can't get them back from the smaller image alone.

**Solution: Laplacian Pyramid**
- Store the **difference** between each level and its "reconstructed" version.
- This difference = the **details that were lost** during downsampling.

**The Frequency Diagram (Right):**
- Gaussian Pyramid: Full circle (all frequencies up to a limit).
- Laplacian Pyramid: **Ring** (only the frequencies between levels).
- Each Laplacian level captures a specific **frequency band**.

### What Does a Laplacian Pyramid Look Like?
![Laplacian Pyramid Levels](uploaded_media_1_1770022601067.png)

- The images look **gray with edges highlighted**.
- These are the **details** (edges, textures) at each scale.
- Most pixels are near zero (gray = no difference).
- Strong edges appear as bright/dark lines.
- The **smallest image** in the corner is just the coarsest Gaussian level (low-frequency base).

### Building a Laplacian Pyramid: Step-by-Step
![Laplacian Steps](uploaded_media_2_1770022601067.png)

#### Step 1: Start with a Gaussian Pyramid
You already have: $G_0, G_1, G_2, ..., G_N$

#### Step 2: Upsample the Next Level
Take the smaller image $G_{k+1}$ and **expand** it back to the size of $G_k$:
$$\hat{G}_k = \text{Expand}(G_{k+1})$$

**Expand = Upsample + Blur:**
- Insert zeros between pixels (upsample).
- Convolve with Gaussian to fill in the gaps (interpolate).

#### Step 3: Take the Difference
Subtract the expanded version from the original:
$$L_k = G_k - \hat{G}_k$$

**What is $L_k$?**
- It's the **detail lost** when going from $G_k$ to $G_{k+1}$.
- It contains the **high-frequency information** at that scale.

#### Step 4: Repeat for All Levels
- Compute $L_0, L_1, L_2, ..., L_{N-1}$.
- The **final level** is just the coarsest Gaussian:
$$L_N = G_N$$
- This is the low-frequency "base" of the image.

### Visual Walkthrough

**Level 0 (Finest):**
```
Original G_0:    [Full detail baboon]
Expanded G_1:    [Blurry baboon, same size]
L_0 = G_0 - Ĝ_0: [Fine edges and textures]
```

**Level 1:**
```
G_1:             [Half-size baboon]
Expanded G_2:    [Blurry, same size as G_1]
L_1 = G_1 - Ĝ_1: [Medium-scale edges]
```

**Level N (Coarsest):**
```
L_N = G_N:       [Tiny, blurry base image]
```

### Why is it Called "Laplacian"?
- The difference $G_k - \hat{G}_k$ approximates a **Laplacian of Gaussian (LoG)** filter.
- LoG = Edge detector that finds regions of rapid intensity change.
- So each Laplacian level is essentially an **edge image at that scale**.

### The Magic: Perfect Reconstruction
Because we stored what was lost, we can **perfectly rebuild the original**:

$$G_k = L_k + \hat{G}_k = L_k + \text{Expand}(G_{k+1})$$

**Reconstruction Algorithm:**
```
Start with L_N = G_N (the coarsest level)

For k = N-1, N-2, ..., 0:
    G_k = L_k + Expand(G_{k+1})

Result: G_0 = Original Image!
```

### Summary Table

| Pyramid | What it Stores | Frequency Content | Reconstructible? |
|---------|---------------|-------------------|------------------|
| Gaussian | Blurred versions | Low-pass (all lower freqs) | No (lossy) |
| Laplacian | Detail differences | Band-pass (specific freq range) | **Yes (lossless)** |

---

## Topic: Image Blending (The "Oraple" Magic)

### Slide 1: The Problem with Hard Compositing
![Hard Compositing](uploaded_media_0_1770023249408.png)

**Hard Compositing Formula:**
$$I(x,y) = M(x,y) \cdot S(x,y) + (1 - M(x,y)) \cdot T(x,y)$$

Where:
- $S(x,y)$ = **Source** image (e.g., apple)
- $T(x,y)$ = **Target** image (e.g., orange)
- $M(x,y)$ = **Mask** (1 = use source, 0 = use target)

**The Problem:**
- When $M = 1$: Take pixel from Source (apple).
- When $M = 0$: Take pixel from Target (orange).
- **Result:** A sharp, ugly seam where the mask changes from 0 to 1!

### Slide 2: Laplacian Pyramid Blending (The Solution)
![Laplacian Blending](uploaded_media_1_1770023249408.png)

**The Algorithm:**

1. **Compute Laplacian pyramids** for both Source and Target:
   - $L^S$ = Laplacian pyramid of Source (apple)
   - $L^T$ = Laplacian pyramid of Target (orange)

2. **Compute Gaussian pyramid** for the Mask:
   - $G$ = Gaussian pyramid of Mask
   - This makes the mask **gradually blur** at higher levels!

3. **Blend at each level:**
$$L^{blend}_i = G_i \cdot L^S_i + (1 - G_i) \cdot L^T_i$$

4. **Reconstruct** from the blended Laplacian pyramid.

**Result Comparison:**
| (a) Apple | (b) Orange | (c) Regular Splice | (d) Pyramid Blend |
|-----------|------------|-------------------|-------------------|
| Original | Original | Hard edge visible | **Seamless!** |

### Slide 3: The Famous "Oraple" Result
![Pyramid Blending](uploaded_media_2_1770023249408.png)

This is the famous result from **Burt & Adelson (1983)**:
- Top row: Apple and Orange originals.
- Bottom row: Different blending results.
- **Rightmost:** The seamless "Oraple" using Laplacian pyramid blending!

### Slide 4: Blending at Different Levels
![Blending Levels](uploaded_media_3_1770023249408.png)

**Left Column:** Apple's Laplacian levels (L^S)
**Middle Column:** Orange's Laplacian levels (L^T)
**Right Column:** Blended Laplacian levels

**Key Insight:**
- **Level 4 (coarse):** Blur is wide → colors blend smoothly.
- **Level 2 (medium):** Medium-scale features blend.
- **Level 0 (fine):** Fine details blend with sharp mask.

**Why it works:**
- At **coarse levels**, the mask is blurry → smooth color transition.
- At **fine levels**, the mask is sharp → preserves edge details.
- **Result:** Smooth blend without losing sharpness!

### Slide 5: Full Pyramid Blending Process
![Full Process](uploaded_media_4_1770023249408.png)

**Left Side (Apple/Orange):** Shows all Laplacian levels from fine (a) to coarse (i), then reconstruction (j, k, l).

**Right Side (Face/Hand):** Another example showing:
- (a) Face image
- (b) Hand image
- (c) Mask (white = face region)
- (d) **Blended result** — seamless!

### Summary: The Pyramid Blending Recipe

```
1. Build Laplacian pyramids: L^S, L^T
2. Build Gaussian pyramid: G (from mask M)

3. For each level i = 0 to N:
       L^blend_i = G_i * L^S_i + (1 - G_i) * L^T_i

4. Reconstruct from L^blend → Seamless composite!
```

**Why Gaussian for the mask?**
- Blurring the mask at higher levels creates a **gradient transition**.
- This matches the frequency bands of the Laplacian levels.
- Fine details (level 0) get hard transitions.
- Coarse features (level N) get smooth transitions.

---

### Topic:

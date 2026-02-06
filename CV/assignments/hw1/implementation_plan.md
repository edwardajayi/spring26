# HW1 Part I: Pinhole Camera Model - Implementation Plan

## Goal
Implement a complete pinhole camera model to project 3D points onto 2D image planes, experimenting with different camera parameters.

---

## What's Already Done (in hw1.tex)
- ✅ Image plane equations (constant-depth and general)
- ✅ Parametric ray equation derivation
- ✅ Ray-plane intersection formula
- ✅ 2D mapping equations
- ✅ Parameter analysis text

---

## What Needs to Be Implemented (Python Code)

### Step 1: Load Data and Define Camera Parameters

```python
import pickle
import numpy as np
import matplotlib.pyplot as plt

# Load points
with open('points.pkl', 'rb') as f:
    data = pickle.load(f)
blue_points = data['blue_points']   # Nx3 array
black_points = data['black_points'] # Nx3 array

# Camera parameters
camera_center = np.array([0, 0, 0])  # C = (0, 0, 0)
focal_lengths = [10, 50, 100]        # Different f values to test
```

---

### Step 2: Ray-Plane Intersection Functions

**Standard Plane (Z = Z₀):**
```python
def project_standard_plane(points, camera_center, z0):
    """Project points onto Z = z0 plane"""
    C = camera_center
    # t = (z0 - Cz) / (Z - Cz)
    t = (z0 - C[2]) / (points[:, 2] - C[2])
    
    Ix = C[0] + t * (points[:, 0] - C[0])
    Iy = C[1] + t * (points[:, 1] - C[1])
    
    return np.column_stack([Ix, Iy])
```

**Tilted Plane (ax + by + cz + d = 0):**
```python
def project_tilted_plane(points, camera_center, a, b, c, d):
    """Project points onto tilted plane ax + by + cz + d = 0"""
    C = camera_center
    dx = points[:, 0] - C[0]
    dy = points[:, 1] - C[1]
    dz = points[:, 2] - C[2]
    
    numerator = -(a*C[0] + b*C[1] + c*C[2] + d)
    denominator = a*dx + b*dy + c*dz
    
    t = numerator / denominator
    
    Ix = C[0] + t * dx
    Iy = C[1] + t * dy
    Iz = C[2] + t * dz
    
    return np.column_stack([Ix, Iy, Iz])
```

---

### Step 3 & 4: Map to 2D Image Coordinates

```python
def map_to_image_coords(projected_points, cx=0, cy=0):
    """Map to 2D pixel coordinates (u, v)"""
    # u = Ix + cx, v = Iy + cy (with sx=sy=1, Ox=Oy=0)
    u = projected_points[:, 0] + cx
    v = projected_points[:, 1] + cy
    return np.column_stack([u, v])
```

---

### Experiment: Focal Length Comparison

```python
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

for i, f in enumerate(focal_lengths):
    blue_proj = project_standard_plane(blue_points, camera_center, f)
    black_proj = project_standard_plane(black_points, camera_center, f)
    
    axes[i].scatter(blue_proj[:, 0], blue_proj[:, 1], c='blue', s=2, label='Blue')
    axes[i].scatter(black_proj[:, 0], black_proj[:, 1], c='black', s=2, label='Black')
    axes[i].set_title(f'f = {f}')
    axes[i].axis('equal')
    axes[i].legend()

plt.tight_layout()
plt.savefig('focal_length_comparison.png', dpi=150)
plt.show()
```

---

### Experiment: Distance Calculations

```python
def euclidean_distance(p1, p2):
    return np.sqrt(np.sum((p1 - p2)**2))

# 3D distances (before projection)
dist_first_3d = euclidean_distance(black_points[0], blue_points[0])
dist_last_3d = euclidean_distance(black_points[-1], blue_points[-1])

# 2D distances (after projection)
blue_proj = project_standard_plane(blue_points, camera_center, 50)
black_proj = project_standard_plane(black_points, camera_center, 50)

dist_first_2d = euclidean_distance(black_proj[0], blue_proj[0])
dist_last_2d = euclidean_distance(black_proj[-1], blue_proj[-1])

print(f"First points - 3D: {dist_first_3d:.4f}, 2D: {dist_first_2d:.4f}")
print(f"Last points - 3D: {dist_last_3d:.4f}, 2D: {dist_last_2d:.4f}")
```

---

## Deliverables Checklist

- [ ] 3D point visualization
- [ ] Projection plots for f=10, 50, 100
- [ ] Tilted plane projection plot
- [ ] Distance calculation results
- [ ] Add figures to LaTeX report
- [ ] Answer analysis questions

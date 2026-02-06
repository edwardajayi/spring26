import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from IPython.display import HTML

# 1. Verify Data & Setup Center
bonus_points = custom_points_3d
if len(bonus_points) == 0:
    raise ValueError("Error: custom_points_3d is empty!")

pc_center = np.mean(bonus_points, axis=0)
pc_extent = np.max(np.abs(bonus_points - pc_center))
bound = pc_extent * 2.0 

# ---------------------------------------------------------
# BONUS 1: Compare Perspective vs Orthographic Projection
# ---------------------------------------------------------

def project_orthographic(points, camera_pos, rotation_matrix, scale=1.0):
    points_centered = points - camera_pos
    points_cam = (rotation_matrix @ points_centered.T).T
    Xc, Yc, Zc = points_cam[:, 0], points_cam[:, 1], points_cam[:, 2]
    valid_mask = Zc > 0
    u = np.full(len(points), np.nan)
    v = np.full(len(points), np.nan)
    if np.any(valid_mask):
        u[valid_mask] = scale * Xc[valid_mask]
        v[valid_mask] = scale * Yc[valid_mask]
    return np.column_stack([u, v]), Zc, valid_mask

# --- Setup Comparison ---
R_front = np.array([[1, 0, 0], [0, 1, 0], [0, 0, -1]]) 
cam_pos_front = pc_center + np.array([0, 0, pc_extent * 3])

proj_p, depths_p, mask_p = project_with_camera_pose(
    bonus_points, cam_pos_front, R_front, focal_length=800
)

proj_o, depths_o, mask_o = project_orthographic(
    bonus_points, cam_pos_front, R_front, scale=5.0
)

# --- Plot Side-by-Side ---
fig, axes = plt.subplots(1, 2, figsize=(14, 7))

# Perspective
if np.any(mask_p):
    valid_p = proj_p[mask_p]
    max_range = np.max(np.abs(valid_p)) * 1.2
    plot_step = 10 if len(valid_p) > 200000 else 1
    axes[0].scatter(valid_p[::plot_step, 0], -valid_p[::plot_step, 1], s=2, alpha=0.7, 
                   c=depths_p[mask_p][::plot_step], cmap='plasma')
    axes[0].set_xlim(-max_range, max_range)
    axes[0].set_ylim(-max_range, max_range)

axes[0].set_title("Perspective (Color by Depth)")
axes[0].set_aspect('equal')

# Orthographic
if np.any(mask_o):
    valid_o = proj_o[mask_o]
    max_range_o = np.max(np.abs(valid_o)) * 1.2
    plot_step = 10 if len(valid_o) > 200000 else 1
    axes[1].scatter(valid_o[::plot_step, 0], -valid_o[::plot_step, 1], s=2, alpha=0.7, 
                   c=depths_o[mask_o][::plot_step], cmap='plasma')
    axes[1].set_xlim(-max_range_o, max_range_o)
    axes[1].set_ylim(-max_range_o, max_range_o)

axes[1].set_title("Orthographic (Color by Depth)")
axes[1].set_aspect('equal')

plt.tight_layout()
plt.show()


# ---------------------------------------------------------
# BONUS 2: Animation (Self-Contained & Optimized)
# ---------------------------------------------------------

# Ensure we have the optimized points variable defined LOCALLY here
# This prevents NameError if you run cells out of order
if 'bonus_points' not in locals():
    bonus_points = custom_points_3d

# Aggressive Downsampling for Animation Speed
# Cap at 5000 points max
if len(bonus_points) > 5000:
    step = len(bonus_points) // 5000
    points_to_animate = bonus_points[::step]
    print(f"Animation: Optimizing from {len(bonus_points)} to {len(points_to_animate)} points.")
else:
    points_to_animate = bonus_points

def look_at(eye, target, up):
    z_axis = target - eye  
    z_axis = z_axis / np.linalg.norm(z_axis)
    x_axis = np.cross(up, z_axis) 
    x_axis = x_axis / np.linalg.norm(x_axis)
    y_axis = np.cross(z_axis, x_axis)
    x_axis = -x_axis 
    return np.array([x_axis, y_axis, z_axis])

fig_anim, ax_anim = plt.subplots(figsize=(6, 6))
radius = pc_extent * 3.0
num_frames = 20 

def update(frame):
    ax_anim.clear()
    
    theta = 2 * np.pi * frame / num_frames
    x = radius * np.sin(theta)
    z = radius * np.cos(theta)
    
    current_pos = pc_center + np.array([x, 0, z])
    R_orbit = look_at(current_pos, pc_center, np.array([0, 1, 0]))
    
    # Use the LOCALLY defined points_to_animate
    proj, depths, mask = project_with_camera_pose(
        points_to_animate, current_pos, R_orbit, focal_length=800
    )
    
    if np.any(mask):
        valid = proj[mask]
        valid_depths = depths[mask]
        ax_anim.scatter(valid[:, 0], -valid[:, 1], s=5, alpha=0.8, 
                       c=valid_depths, cmap='turbo')
        
        limit = np.max(np.abs(valid)) * 1.5
        ax_anim.set_xlim(-limit, limit)
        ax_anim.set_ylim(-limit, limit)
    else:
        ax_anim.set_xlim(-1000, 1000)
        ax_anim.set_ylim(-1000, 1000)
        
    ax_anim.set_aspect('equal')
    ax_anim.axis('off')
    ax_anim.set_title(f"Orbit Frame {frame}")

print(f"Generating animation ({num_frames} frames)...")
ani = animation.FuncAnimation(fig_anim, update, frames=num_frames, interval=100)
HTML(ani.to_jshtml())

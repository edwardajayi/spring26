import numpy as np
import matplotlib.pyplot as plt
from plyfile import PlyData
import os
import matplotlib.animation as animation
from matplotlib import rc

# Load Data
ply_file = 'scene.ply'
if not os.path.exists(ply_file):
    print("Error: scene.ply not found.")
    exit(1)

plydata = PlyData.read(ply_file)
vertices = plydata['vertex']
points_3d = np.column_stack([vertices['x'], vertices['y'], vertices['z']])
# Downsample for speed during testing
points_3d = points_3d[::10] 

vertex_properties = [p.name for p in vertices.properties]
if 'red' in vertex_properties:
    colors = np.column_stack([vertices['red'], vertices['green'], vertices['blue']]) / 255.0
    colors = colors[::10]
else:
    colors = None

pc_center = np.mean(points_3d, axis=0)
pc_extent = np.max(np.abs(points_3d - pc_center))
camera_distance = pc_extent * 3

# Helper Functions
def create_rotation_matrix_y(angle):
    c, s = np.cos(angle), np.sin(angle)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])

def project_perspective(points, camera_pos, rotation_matrix, focal_length=500):
    points_centered = points - camera_pos
    points_cam = (rotation_matrix @ points_centered.T).T
    Xc, Yc, Zc = points_cam[:, 0], points_cam[:, 1], points_cam[:, 2]
    
    valid_mask = Zc > 0
    u = np.full(len(points), np.nan)
    v = np.full(len(points), np.nan)
    
    # Perspective division
    if np.any(valid_mask):
        u[valid_mask] = focal_length * (Xc[valid_mask] / Zc[valid_mask])
        v[valid_mask] = focal_length * (Yc[valid_mask] / Zc[valid_mask])
    
    return np.column_stack([u, v]), valid_mask

def project_orthographic(points, camera_pos, rotation_matrix, scale=10):
    points_centered = points - camera_pos
    points_cam = (rotation_matrix @ points_centered.T).T
    Xc, Yc = points_cam[:, 0], points_cam[:, 1]
    
    # No division by Z
    u = scale * Xc
    v = scale * Yc
    
    # For orthographic, basically all points 'in front' or we just project everything.
    # Usually we still clip Z < 0 if simulating a camera, but for pure ortho we often keep all.
    # Let's clip Z > 0 to match camera logic
    Zc = points_cam[:, 2]
    valid_mask = Zc > 0
    
    return np.column_stack([u, v]), valid_mask

# --- Comparisons ---
print("Generating comparison...")
# Define a camera pose (Front view)
cam_pos = pc_center + np.array([0, 0, camera_distance])
# Looking -Z: R should map World +X to Cam +X, World +Y to Cam +Y, World -Z to Cam +Z
# World: X, Y, Z. Cam: Right, Down, Forward.
# Standard: Xc=X, Yc=Y, Zc=-Z (if looking down -Z)
# Our previous notebook used a specific rotation for 'front'
# front: rotation: np.array([[1, 0, 0], [0, 1, 0], [0, 0, -1]])
R_front = np.array([[1, 0, 0], [0, 1, 0], [0, 0, -1]])

proj_persp, mask_p = project_perspective(points_3d, cam_pos, R_front, focal_length=800)
proj_ortho, mask_o = project_orthographic(points_3d, cam_pos, R_front, scale=5) # scale needs adjustment to match size

fig, axes = plt.subplots(1, 2, figsize=(12, 6))

# Center the plots
valid_p = proj_persp[mask_p]
if len(valid_p) > 0:
    axes[0].scatter(valid_p[:, 0], -valid_p[:, 1], s=0.5, c=colors[mask_p] if colors is not None else 'b')
    axes[0].set_title("Perspective Projection")
    axes[0].set_aspect('equal')
    axes[0].set_xlim(-500, 500)
    axes[0].set_ylim(-500, 500)

valid_o = proj_ortho[mask_o]
if len(valid_o) > 0:
    axes[1].scatter(valid_o[:, 0], -valid_o[:, 1], s=0.5, c=colors[mask_o] if colors is not None else 'b')
    axes[1].set_title("Orthographic Projection")
    axes[1].set_aspect('equal')
    axes[1].set_xlim(-300, 300)
    axes[1].set_ylim(-300, 300)

plt.tight_layout()
plt.savefig('projection_comparison.png')
print("Comparison saved.")

# --- Animation ---
print("Generating animation frames...")
# Orbit around Y axis
num_frames = 10 # small number for testing
angles = np.linspace(0, 2*np.pi, num_frames)
radius = camera_distance

for i, angle in enumerate(angles):
    # Calculate position on circle in XZ plane
    x = radius * np.sin(angle)
    z = radius * np.cos(angle)
    pos = pc_center + np.array([x, 0, z])
    
    # Calculate rotation to look at center
    # Forward vector (cam Z) = Center - Pos (normalized) -> inverted for cam coordinates usually
    # Actually we want the camera Z axis to point *opposite* to the view direction? 
    # Usually: ViewDir = Target - Eye. CamZ = -ViewDir.
    # But let's stick to the rotation logic: R transforms (P-C).
    # Simple Y-rotation of the 'front' matrix should work if we rotate the camera frame itself
    
    # Or cleaner: LookAt function
    def look_at(eye, target, up):
        z_axis = eye - target
        z_axis = z_axis / np.linalg.norm(z_axis)
        x_axis = np.cross(up, z_axis)
        x_axis = x_axis / np.linalg.norm(x_axis)
        y_axis = np.cross(z_axis, x_axis)
        # R has rows as axes
        return np.array([x_axis, y_axis, z_axis])

    R = look_at(pos, pc_center, np.array([0, 1, 0]))
    
    proj, mask = project_perspective(points_3d, pos, R, focal_length=800)
    
    plt.figure(figsize=(6, 6))
    if np.any(mask):
        valid = proj[mask]
        plt.scatter(valid[:, 0], -valid[:, 1], s=0.5, c=colors[mask] if colors is not None else 'b')
    plt.xlim(-500, 500)
    plt.ylim(-500, 500)
    plt.axis('off')
    plt.savefig(f'orbit_frame_{i:03d}.png')
    plt.close()

print("Frames generated.")

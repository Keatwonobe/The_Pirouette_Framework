import numpy as np
from sklearn.neighbors import KernelDensity
from skimage.measure import marching_cubes
import os

# -------------------------------
# Load PCA coordinates
# -------------------------------
X = np.load("latent_pca_coords.npy")   # shape (N, 3)

# Optionally subsample if N is truly huge
# X = X[::2]

# -------------------------------
# Normalize into [0, 1]^3 box
# -------------------------------
mins = X.min(axis=0)
maxs = X.max(axis=0)
span = maxs - mins
Xn = (X - mins) / span

# -------------------------------
# Fit 3D Gaussian KDE
# -------------------------------
# bandwidth controls smoothness; decrease for sharper features (costs more data)
bandwidth = 0.06   # try 0.04–0.08 if you want to tune later
kde = KernelDensity(kernel="gaussian", bandwidth=bandwidth)
kde.fit(Xn)

# -------------------------------
# Evaluate KDE on a fine grid
# -------------------------------
# Careful: res^3 points; 120^3 ≈ 1.7M, 150^3 ≈ 3.4M
res = 140
grid_lin = np.linspace(0.0, 1.0, res)
gx, gy, gz = np.meshgrid(grid_lin, grid_lin, grid_lin, indexing="ij")
grid_points = np.stack([gx.ravel(), gy.ravel(), gz.ravel()], axis=1)

print(f"[INFO] Evaluating KDE on {grid_points.shape[0]} grid points...")
log_density = kde.score_samples(grid_points)
density = np.exp(log_density).reshape(res, res, res)

# -------------------------------
# Choose an isosurface level
# -------------------------------
# A percentile of density works well; 80–90% highlights “bones”
iso_percentile = 85.0
level = np.percentile(density, iso_percentile)
print(f"[INFO] Using isosurface level = {level:.3e} "
      f"(percentile {iso_percentile})")

# -------------------------------
# Marching cubes to get surface
# -------------------------------
# skimage expects z,y,x ordering, so transpose
verts_n, faces, normals, values = marching_cubes(
    volume=density.transpose(2, 1, 0),  # (z,y,x)
    level=level,
    spacing=(1.0 / (res - 1),) * 3
)

# verts_n are in normalized [0,1]^3 coordinates; convert back to PCA units
verts_pca = verts_n * span + mins

print(f"[INFO] Extracted mesh with {len(verts_pca)} vertices and {len(faces)} faces.")

# -------------------------------
# Simple ASCII STL writer
# -------------------------------
def write_ascii_stl(path, vertices, faces, solid_name="latent_object"):
    with open(path, "w") as f:
        f.write(f"solid {solid_name}\n")
        for tri in faces:
            i, j, k = tri
            v1 = vertices[i]
            v2 = vertices[j]
            v3 = vertices[k]
            # crude normal (we can just write 0s; most tools recompute)
            f.write("  facet normal 0 0 0\n")
            f.write("    outer loop\n")
            f.write(f"      vertex {v1[0]} {v1[1]} {v1[2]}\n")
            f.write(f"      vertex {v2[0]} {v2[1]} {v2[2]}\n")
            f.write(f"      vertex {v3[0]} {v3[1]} {v3[2]}\n")
            f.write("    endloop\n")
            f.write("  endfacet\n")
        f.write(f"endsolid {solid_name}\n")

out_stl = "latent_volume_refined.stl"
write_ascii_stl(out_stl, verts_pca, faces)
print(f"[OK] Wrote refined STL mesh to: {os.path.abspath(out_stl)}")

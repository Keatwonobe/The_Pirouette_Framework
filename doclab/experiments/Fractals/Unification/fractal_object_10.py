import numpy as np
from sklearn.neighbors import NearestNeighbors
import os

# Optional dependencies
try:
    from skimage.measure import marching_cubes
    HAVE_SKIMAGE = True
except ImportError:
    HAVE_SKIMAGE = False
    print("[WARN] scikit-image not found; marching cubes surface will be skipped.")

###############################################################################
# 1. Utility: PLY writers
###############################################################################

def save_ply_points(filename, points, colors=None, scalars=None, scalar_name="scalar"):
    """
    Save point cloud as ASCII PLY.
    points: (N,3)
    colors: optional (N,3) uint8
    scalars: optional (N,) float
    """
    N = points.shape[0]
    has_color = colors is not None
    has_scalar = scalars is not None

    with open(filename, "w") as f:
        # Header
        f.write("ply\n")
        f.write("format ascii 1.0\n")
        f.write(f"element vertex {N}\n")
        f.write("property float x\n")
        f.write("property float y\n")
        f.write("property float z\n")
        if has_color:
            f.write("property uchar red\n")
            f.write("property uchar green\n")
            f.write("property uchar blue\n")
        if has_scalar:
            f.write(f"property float {scalar_name}\n")
        f.write("end_header\n")

        # Body
        if has_color and has_scalar:
            for p, c, s in zip(points, colors, scalars):
                f.write(f"{p[0]} {p[1]} {p[2]} {int(c[0])} {int(c[1])} {int(c[2])} {float(s)}\n")
        elif has_color:
            for p, c in zip(points, colors):
                f.write(f"{p[0]} {p[1]} {p[2]} {int(c[0])} {int(c[1])} {int(c[2])}\n")
        elif has_scalar:
            for p, s in zip(points, scalars):
                f.write(f"{p[0]} {p[1]} {p[2]} {float(s)}\n")
        else:
            for p in points:
                f.write(f"{p[0]} {p[1]} {p[2]}\n")

    print(f"[PLY] Saved points -> {filename}")


def save_ply_mesh(filename, vertices, faces):
    """
    Save triangulated mesh as ASCII PLY.
    vertices: (Nv,3)
    faces: (Nf,3) int indices
    """
    Nv = vertices.shape[0]
    Nf = faces.shape[0]
    with open(filename, "w") as f:
        f.write("ply\n")
        f.write("format ascii 1.0\n")
        f.write(f"element vertex {Nv}\n")
        f.write("property float x\n")
        f.write("property float y\n")
        f.write("property float z\n")
        f.write(f"element face {Nf}\n")
        f.write("property list uchar int vertex_indices\n")
        f.write("end_header\n")
        for v in vertices:
            f.write(f"{v[0]} {v[1]} {v[2]}\n")
        for tri in faces:
            f.write(f"3 {tri[0]} {tri[1]} {tri[2]}\n")
    print(f"[PLY] Saved mesh -> {filename}")

###############################################################################
# 2. Load latent data
###############################################################################

def load_latent_data():
    """
    Loads 3D PCA coordinates and the 5 feature fields from the files 
    produced by fractal_object_5.py ('latent_pca_coords.npy') and 
    fractal_object_3.py ('latent_curve_data.npz').
    """
    # 1. 3D PCA coordinates (The point map) from fractal_object_5.py
    try:
        pca_coords = np.load("latent_pca_coords.npy")
    except FileNotFoundError:
        print("[LOAD ERROR] 'latent_pca_coords.npy' not found. Run fractal_object_5.py first.")
        raise
        
    # 2. Sorted 5D feature fields from fractal_object_3.py
    try:
        data_fields = np.load("latent_curve_data.npz", allow_pickle=True)
        X_sorted = data_fields["X_sorted"]
        names = list(data_fields["names"])
        
        # Create dictionary mapping field name to the (N,) vector
        # Names: ["anchor", "ftle", "tension", "spin", "stiff"]
        fields = {
            names[k]: X_sorted[:, k] for k in range(len(names))
        }

    except FileNotFoundError:
        print("[LOAD ERROR] 'latent_curve_data.npz' not found. Run fractal_object_3.py first.")
        raise

    print(f"[LOAD] {pca_coords.shape[0]} points in PCA space.")
    return pca_coords, fields

###############################################################################
# 3. Tangent-PCA-based sheet extraction (D-PLUS core)
###############################################################################

def extract_sheet_points(pca_coords,
                         k_neighbors=40,
                         max_points=8000,
                         anisotropy_threshold=0.12):
    """
    For each point (or subsample), do local PCA on k-NN neighborhood.
    Keep points whose local covariance has λ3/λ2 < anisotropy_threshold
    (i.e., they lie on a locally 2D sheet in 3D).
    """

    N = pca_coords.shape[0]
    print(f"[SHEET] Building k-NN structure on {N} points...")
    nbrs = NearestNeighbors(n_neighbors=k_neighbors, algorithm="auto").fit(pca_coords)
    # Subsample indices to keep compute time reasonable
    if N > max_points:
        idx = np.random.choice(N, size=max_points, replace=False)
        print(f"[SHEET] Subsampling to {max_points} points for tangent PCA.")
    else:
        idx = np.arange(N)

    sheet_mask = np.zeros(N, dtype=bool)
    local_thickness = np.zeros(N, dtype=float)

    for count, i in enumerate(idx):
        if (count + 1) % 1000 == 0:
            print(f"[SHEET] Tangent PCA {count+1}/{idx.shape[0]}...")
        point = pca_coords[i].reshape(1, -1)
        distances, indices = nbrs.kneighbors(point, return_distance=True)
        neigh = pca_coords[indices[0]]  # (k,3)
        # Center
        centered = neigh - neigh.mean(axis=0, keepdims=True)
        # Local covariance
        C = centered.T @ centered / (centered.shape[0] - 1)
        # Eigenvalues
        eigvals, eigvecs = np.linalg.eigh(C)
        # Sort (ascending)
        eigvals = np.sort(eigvals)
        lam1, lam2, lam3 = eigvals  # lam3 largest
        # We care about thickness vs surface: lam1 is smallest
        # But our 2D sheet criterion is: lam1 << lam2 ≈ lam3 or lam3/lam2 small.
        # In practice, lam1 << lam2 and lam2 ~ lam3 -> lam1/lam2 small.
        ratio = lam1 / max(lam2, 1e-12)
        local_thickness[i] = lam1

        if ratio < anisotropy_threshold:
            sheet_mask[i] = True

    print(f"[SHEET] Identified {sheet_mask.sum()} points as sheet-like (ratio < {anisotropy_threshold}).")
    return sheet_mask, local_thickness


###############################################################################
# 4. Ultra-res voxelization & marching cubes
###############################################################################

def voxelize_and_march(pca_coords, sheet_mask,
                       grid_res=(320, 320, 320),
                       percentile=80):
    """
    Voxelize the sheet points in a high-res grid and run marching cubes
    on the density field at a chosen percentile.
    """
    if not HAVE_SKIMAGE:
        print("[VOXEL] Skipping voxelization+marching cubes (no scikit-image).")
        return None, None

    pts = pca_coords[sheet_mask]
    print(f"[VOXEL] Voxelizing {pts.shape[0]} sheet points into grid {grid_res}...")

    # Compute bounding box with small padding
    mins = pts.min(axis=0)
    maxs = pts.max(axis=0)
    padding = 0.05 * (maxs - mins)
    mins -= padding
    maxs += padding

    nx, ny, nz = grid_res
    # Map points to voxel coords [0, nx-1], etc.
    scale = (np.array([nx, ny, nz]) - 1) / (maxs - mins)
    shifted = (pts - mins) * scale

    # Initialize density grid
    density = np.zeros((nx, ny, nz), dtype=np.float32)

    idx = np.floor(shifted).astype(int)
    idx = np.clip(idx, 0, np.array([nx - 1, ny - 1, nz - 1]))
    for i, j, k in idx:
        density[i, j, k] += 1.0

    nonzero = density[density > 0]
    if nonzero.size == 0:
        print("[VOXEL] No nonzero densities; cannot build isosurface.")
        return None, None

    thresh = np.percentile(nonzero, percentile)
    print(f"[VOXEL] Marching cubes at density threshold = {thresh:.3f} (p={percentile}%).")

    verts, faces, normals, values = marching_cubes(
        volume=density,
        level=thresh,
        spacing=(1.0 / scale[0], 1.0 / scale[1], 1.0 / scale[2])
    )
    # Shift back to PCA coords
    verts = verts + mins

    print(f"[VOXEL] Marching cubes produced {verts.shape[0]} vertices, {faces.shape[0]} faces.")
    return verts, faces


###############################################################################
# 5. Main orchestration
###############################################################################

def main():
    # REMOVE this line: npz_path = "latent_pca_coords.npz" 

    out_dir = "D_PLUS_outputs"
    os.makedirs(out_dir, exist_ok=True)

    # Correct the function call to remove the argument:
    pca_coords, fields = load_latent_data() 

    # --- Sheet extraction via tangent PCA ---
    sheet_mask, local_thickness = extract_sheet_points(
        pca_coords,
        k_neighbors=40,
        max_points=8000,
        anisotropy_threshold=0.12,
    )

    sheet_points = pca_coords[sheet_mask]
    sheet_thickness = local_thickness[sheet_mask]

    # Normalize thickness for coloring if you want
    t_min, t_max = sheet_thickness.min(), sheet_thickness.max()
    t_norm = (sheet_thickness - t_min) / max(t_max - t_min, 1e-12)
    colors = np.stack([
        255 * t_norm,
        255 * (1.0 - t_norm),
        128 * np.ones_like(t_norm)
    ], axis=1).astype(np.uint8)

    save_ply_points(
        os.path.join(out_dir, "latent_sheet_points.ply"),
        sheet_points,
        colors=colors,
        scalars=sheet_thickness,
        scalar_name="thickness"
    )

    # --- High-res voxelization + isosurface (if skimage available) ---
    verts, faces = voxelize_and_march(
        pca_coords,
        sheet_mask,
        grid_res=(320, 320, 320),
        percentile=80
    )

    if verts is not None and faces is not None:
        save_ply_mesh(
            os.path.join(out_dir, "latent_sheet_mesh.ply"),
            verts,
            faces
        )

    print("[DONE] D-PLUS extraction complete.")
    print("       - latent_sheet_points.ply (point cloud + thickness)")
    if verts is not None:
        print("       - latent_sheet_mesh.ply (isosurface mesh)")
    else:
        print("       - no mesh (install scikit-image if you want isosurface extraction).")


if __name__ == "__main__":
    main()

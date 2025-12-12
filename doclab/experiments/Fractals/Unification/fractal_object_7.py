import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

DATA_FILE = "latent_curve_data.npz"


def compute_pca_embedding(X, n_components=3):
    """
    Simple PCA -> returns projected coords Y [N, n_components]
    and the explained variance ratios.
    """
    Xc = X - X.mean(axis=0, keepdims=True)
    U, S, Vt = np.linalg.svd(Xc, full_matrices=False)
    W = Vt[:n_components].T   # [D, n_components]
    Y = Xc @ W                # [N, n_components]
    var = S**2
    var_ratio = var[:n_components] / var.sum()
    return Y, var_ratio


def voxelize_points(Y, grid_res=48, margin=0.1):
    """
    Voxelize 3D points into a regular grid using histogramdd.

    Returns:
      H       : [Nx,Ny,Nz] density field
      edges   : (edges_x, edges_y, edges_z)
    """
    # bounding box with a little padding
    mins = Y.min(axis=0)
    maxs = Y.max(axis=0)
    span = maxs - mins
    mins = mins - margin * span
    maxs = maxs + margin * span

    edges = [
        np.linspace(mins[d], maxs[d], grid_res + 1) for d in range(3)
    ]

    H, edges = np.histogramdd(Y, bins=edges)
    # Normalize to [0,1]
    if H.max() > 0:
        H = H / H.max()

    return H.astype(np.float32), edges


def smooth_volume_3d(H, sigma=1.0):
    """
    Tiny 3D Gaussian-ish smoothing using separable 1D convolutions
    so we don't rely on scipy. Very lightweight.
    """
    if sigma <= 0:
        return H

    radius = int(3 * sigma)
    xs = np.arange(-radius, radius + 1)
    kernel = np.exp(-0.5 * (xs / sigma) ** 2)
    kernel = kernel / kernel.sum()

    def conv1d_along_axis(arr, axis):
        arr_pad = np.pad(arr, [(radius, radius)] * 3, mode="edge")
        out = np.zeros_like(arr_pad)
        # roll kernel along axis by convolution
        it = np.nditer(np.zeros(arr_pad.shape), flags=["multi_index"])
        while not it.finished:
            idx = list(it.multi_index)
            s = 0.0
            for k, w in enumerate(kernel):
                idx_k = idx.copy()
                idx_k[axis] = idx[axis] + k - radius
                s += w * arr_pad[tuple(idx_k)]
            out[tuple(idx)] = s
            it.iternext()
        # crop padding
        slices = [slice(radius, -radius)] * 3
        return out[tuple(slices)]

    # WARNING: naive 3D loop above is expensive for large grids.
    # To keep this practical, use a fast separable conv via FFT-ish method
    # if grids get big. But with ~48^3 it's fine.
    Hx = conv1d_along_axis(H, axis=0)
    Hy = conv1d_along_axis(Hx, axis=1)
    Hz = conv1d_along_axis(Hy, axis=2)
    return Hz


def marching_cubes_surface(H, edges, level=0.25):
    """
    Try to compute an isosurface using scikit-image's marching_cubes.
    If skimage is not available, returns (None, None).
    """
    try:
        from skimage import measure
    except ImportError:
        print("[Step6] scikit-image not available; "
              "skipping mesh extraction. You can still use latent_volume.npy.")
        return None, None

    # H is indexed [ix, iy, iz]; marching_cubes expects volume[z,y,x]
    V = np.transpose(H, (2, 1, 0))
    verts, faces, _, _ = measure.marching_cubes(V, level=level)

    # map voxel coords back to PCA coordinates
    ex, ey, ez = edges
    # voxel centers
    cx = 0.5 * (ex[:-1] + ex[1:])
    cy = 0.5 * (ey[:-1] + ey[1:])
    cz = 0.5 * (ez[:-1] + ez[1:])

    # verts are in index space (z,y,x) -> map to (x,y,z) coordinates
    verts_xyz = np.column_stack([
        cx[verts[:, 2].astype(int)],
        cy[verts[:, 1].astype(int)],
        cz[verts[:, 0].astype(int)],
    ])

    return verts_xyz, faces


def save_ply(filename, verts, faces):
    """
    Minimal ASCII PLY writer for a triangular mesh.
    """
    n_verts = verts.shape[0]
    n_faces = faces.shape[0]

    with open(filename, "w") as f:
        f.write("ply\n")
        f.write("format ascii 1.0\n")
        f.write(f"element vertex {n_verts}\n")
        f.write("property float x\n")
        f.write("property float y\n")
        f.write("property float z\n")
        f.write(f"element face {n_faces}\n")
        f.write("property list uchar int vertex_indices\n")
        f.write("end_header\n")
        for v in verts:
            f.write(f"{v[0]} {v[1]} {v[2]}\n")
        for tri in faces:
            f.write(f"3 {tri[0]} {tri[1]} {tri[2]}\n")


def preview_surface(verts, faces, out_file="latent_volume_preview.png"):
    fig = plt.figure(figsize=(7, 6))
    ax = fig.add_subplot(111, projection="3d")

    mesh = Poly3DCollection(verts[faces], alpha=0.55)
    mesh.set_edgecolor("k")
    mesh.set_linewidth(0.2)
    ax.add_collection3d(mesh)

    ax.set_xlabel("PC1")
    ax.set_ylabel("PC2")
    ax.set_zlabel("PC3")

    # Auto-scale to vertices
    mins = verts.min(axis=0)
    maxs = verts.max(axis=0)
    span = maxs - mins
    center = 0.5 * (mins + maxs)
    r = 0.6 * span.max()
    ax.set_xlim(center[0] - r, center[0] + r)
    ax.set_ylim(center[1] - r, center[1] + r)
    ax.set_zlim(center[2] - r, center[2] + r)

    plt.title("Latent volume isosurface")
    plt.tight_layout()
    plt.savefig(out_file, dpi=150)
    print(f"[Step6] Saved preview image '{out_file}'")


def main():
    # --------------------------------------------------
    # 1. Load latent fields
    # --------------------------------------------------
    data = np.load(DATA_FILE, allow_pickle=True)
    X_sorted = data["X_sorted"]   # [N,5]
    names = list(data["names"])
    xi = data["xi"]

    print(f"[Step6] Loaded {X_sorted.shape[0]} samples "
          f"with fields {names}")

    # --------------------------------------------------
    # 2. PCA -> 3D embedding
    # --------------------------------------------------
    Y, var_ratio = compute_pca_embedding(X_sorted, n_components=3)
    print("[Step6] PCA variance ratios (first 3 PCs):",
          np.round(var_ratio, 4))

    # --------------------------------------------------
    # 3. Voxelize into 3D density field
    # --------------------------------------------------
    H, edges = voxelize_points(Y, grid_res=48, margin=0.1)
    print("[Step6] Volume shape:", H.shape,
          "| min/max:", H.min(), H.max())

    # optional gentle smoothing; commented out because 48^3 is already nice
    # H_sm = smooth_volume_3d(H, sigma=1.0)
    H_sm = H

    # save volume + axes for later
    np.save("latent_volume.npy", H_sm)
    np.savez("latent_volume_axes.npz",
             edges_x=edges[0],
             edges_y=edges[1],
             edges_z=edges[2])
    print("[Step6] Saved 'latent_volume.npy' and 'latent_volume_axes.npz'")

    # --------------------------------------------------
    # 4. Marching cubes isosurface (if possible)
    # --------------------------------------------------
    level = 0.25  # adjust to see more or less of the “organ”
    verts, faces = marching_cubes_surface(H_sm, edges, level=level)

    if verts is None or faces is None:
        print("[Step6] No mesh created (probably missing scikit-image).")
        return

    print("[Step6] Mesh vertices:", verts.shape[0],
          "| faces:", faces.shape[0])

    # --------------------------------------------------
    # 5. Save PLY mesh and PNG preview
    # --------------------------------------------------
    ply_name = "latent_volume_surface_level{:.2f}.ply".format(level)
    save_ply(ply_name, verts, faces)
    print(f"[Step6] Saved mesh '{ply_name}' "
          "(import this into Blender / MeshLab).")

    preview_surface(verts, faces, out_file="latent_volume_surface_preview.png")


if __name__ == "__main__":
    main()

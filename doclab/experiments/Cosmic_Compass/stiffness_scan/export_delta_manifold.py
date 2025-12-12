import os
import numpy as np

# ======================================================
# 1. Core Δ-field dynamics (same structure as atlas)
# ======================================================

def compute_delta_manifold(
    resolution=220,
    m_range=(-1.5, 1.5),
    l_range=(-1.0, 2.0),
    max_steps=800,
    dt=0.05,
    sigma=1.0,
    escape_radius_sq=20.0,
):
    """
    Evolve the Δ-field Hamiltonian system and return:

      m_vals, l_vals: 1D axes
      esc_steps:      2D array of escape time (or max_steps if trapped)
      status:         2D basin ID (0 = trapped, 1/2/3 = basins)

    This is the same engine you used in the 3D atlas.
    """

    m_vals = np.linspace(m_range[0], m_range[1], resolution)
    l_vals = np.linspace(l_range[0], l_range[1], resolution)
    M, L = np.meshgrid(m_vals, l_vals)

    p_m = np.zeros_like(M)
    p_l = np.zeros_like(L)

    status = np.zeros_like(M, dtype=int)
    active = np.ones_like(M, dtype=bool)
    esc_steps = np.zeros_like(M, dtype=float)

    print(f"[Δ] Computing manifold on {resolution}x{resolution} grid...")
    print(f"    m ∈ {m_range}, λ ∈ {l_range}, max_steps={max_steps}, dt={dt}")

    for step in range(1, max_steps + 1):
        # Gradient of V at current position
        grad_m = M + 2.0 * sigma * M * L
        grad_l = L + sigma * (M**2 - L**2)

        # Half-step momentum
        p_m_half = p_m - 0.5 * dt * grad_m
        p_l_half = p_l - 0.5 * dt * grad_l

        # Full-step position
        M = M + dt * p_m_half
        L = L + dt * p_l_half

        # Gradient at new position
        grad_m2 = M + 2.0 * sigma * M * L
        grad_l2 = L + sigma * (M**2 - L**2)

        # Full-step momentum
        p_m = p_m_half - 0.5 * dt * grad_m2
        p_l = p_l_half - 0.5 * dt * grad_l2

        # Escape / blowup check
        r2 = M**2 + L**2
        bad = (~np.isfinite(M)) | (~np.isfinite(L)) | (~np.isfinite(r2))
        escaped_now = ((r2 > escape_radius_sq) | bad) & active

        if np.any(escaped_now):
            theta = np.arctan2(L[escaped_now], M[escaped_now])

            mask_e1 = (theta > 0.5) & (theta < 2.5)
            mask_e3 = np.abs(theta) > 2.5
            mask_e2 = ~(mask_e1 | mask_e3)

            s = status[escaped_now]
            s[mask_e1] = 1
            s[mask_e2] = 2
            s[mask_e3] = 3
            status[escaped_now] = s

            esc_steps[escaped_now] = step
            active[escaped_now] = False

        if not np.any(active):
            print(f"[Δ] All trajectories escaped by step {step}.")
            break

    esc_steps[active] = max_steps

    esc_steps = np.where(np.isfinite(esc_steps), esc_steps, max_steps).astype(float)
    status = np.where(np.isfinite(status), status, 0).astype(int)

    print("[Δ] Manifold computation done.")
    return m_vals, l_vals, esc_steps, status


# Optional cache so you don't recompute the 20s every time
CACHE_PATH = "pirouette_manifold_cache.npz"


def load_or_compute_manifold(
    use_cache=True,
    **kwargs,
):
    if use_cache and os.path.exists(CACHE_PATH):
        print(f"[Δ] Loading manifold from cache: {CACHE_PATH}")
        data = np.load(CACHE_PATH)
        return (
            data["m_vals"],
            data["l_vals"],
            data["esc_steps"],
            data["status"],
        )

    m_vals, l_vals, esc_steps, status = compute_delta_manifold(**kwargs)

    if use_cache:
        print(f"[Δ] Saving manifold cache to {CACHE_PATH}")
        np.savez_compressed(
            CACHE_PATH,
            m_vals=m_vals,
            l_vals=l_vals,
            esc_steps=esc_steps,
            status=status,
        )
    return m_vals, l_vals, esc_steps, status


# ======================================================
# 2. Fractal smoothing on the height field
# ======================================================

def smooth_height(h, passes=2):
    """
    Simple 3x3 box blur applied 'passes' times.
    Acts as a fractal smoothing / anti-aliasing filter.
    """
    h_sm = h.copy()
    for _ in range(passes):
        pad = np.pad(h_sm, 1, mode="edge")
        h_sm = (
            pad[:-2, :-2] + pad[:-2, 1:-1] + pad[:-2, 2:] +
            pad[1:-1, :-2] + pad[1:-1, 1:-1] + pad[1:-1, 2:] +
            pad[2:, :-2] + pad[2:, 1:-1] + pad[2:, 2:]
        ) / 9.0
    return h_sm


# ======================================================
# 3. PLY writer
# ======================================================

def write_ply(
    filename,
    vertices,
    faces,
    colors=None,
):
    """
    Write an ASCII PLY file.

    vertices: (N, 3) float array
    faces:    (F, 3) int array (0-based indices)
    colors:   (N, 3) uint8 RGB or None
    """

    n_vertices = vertices.shape[0]
    n_faces = faces.shape[0]

    has_color = colors is not None
    if has_color and colors.shape[0] != n_vertices:
        raise ValueError("colors must have same length as vertices")

    with open(filename, "w") as f:
        # Header
        f.write("ply\n")
        f.write("format ascii 1.0\n")
        f.write(f"element vertex {n_vertices}\n")
        f.write("property float x\n")
        f.write("property float y\n")
        f.write("property float z\n")
        if has_color:
            f.write("property uchar red\n")
            f.write("property uchar green\n")
            f.write("property uchar blue\n")
        f.write(f"element face {n_faces}\n")
        f.write("property list uchar int vertex_indices\n")
        f.write("end_header\n")

        # Vertices
        if has_color:
            for (x, y, z), (r, g, b) in zip(vertices, colors):
                f.write(f"{x} {y} {z} {int(r)} {int(g)} {int(b)}\n")
        else:
            for (x, y, z) in vertices:
                f.write(f"{x} {y} {z}\n")

        # Faces (triangles)
        for i, j, k in faces:
            f.write(f"3 {int(i)} {int(j)} {int(k)}\n")

    print(f"[Δ] Wrote PLY mesh to {filename}")


# ======================================================
# 4. Build mesh from grid
# ======================================================

def build_mesh_from_grid(M, L, H, status, height_scale=1.0):
    """
    Convert 2D grids M, L, H into a triangle mesh plus vertex colors.

    Returns vertices (N, 3), faces (F, 3), colors (N, 3 uint8).
    """

    # Flatten vertices
    Z = H * height_scale
    vertices = np.stack([M.ravel(), L.ravel(), Z.ravel()], axis=1)

    # Basin-based colors (same palette as your atlas)
    status_flat = status.ravel()
    colors = np.zeros((status_flat.size, 3), dtype=np.uint8)

    # 0: trapped/core (black)
    colors[status_flat == 0] = np.array([0, 0, 0], dtype=np.uint8)
    # 1: teal
    colors[status_flat == 1] = np.array([0, 204, 204], dtype=np.uint8)
    # 2: gold
    colors[status_flat == 2] = np.array([230, 179, 26], dtype=np.uint8)
    # 3: red
    colors[status_flat == 3] = np.array([230, 77, 26], dtype=np.uint8)

    # Faces: two triangles per grid cell
    ny, nx = M.shape
    faces = []
    def idx(i, j):
        return i * nx + j

    for i in range(ny - 1):
        for j in range(nx - 1):
            v0 = idx(i, j)
            v1 = idx(i + 1, j)
            v2 = idx(i + 1, j + 1)
            v3 = idx(i, j + 1)
            # Triangle 1: (v0, v1, v2)
            faces.append((v0, v1, v2))
            # Triangle 2: (v0, v2, v3)
            faces.append((v0, v2, v3))

    faces = np.array(faces, dtype=np.int32)
    return vertices, faces, colors


# ======================================================
# 5. Main: generate 3D model
# ======================================================

if __name__ == "__main__":
    # --- Step 1: Get the manifold ---
    m_vals, l_vals, esc_steps, status = load_or_compute_manifold(
        use_cache=True,
        resolution=220,
        m_range=(-1.5, 1.5),
        l_range=(-1.0, 2.0),
        max_steps=800,
        dt=0.05,
        sigma=1.0,
        escape_radius_sq=20.0,
    )

    # --- Step 2: Build height field (normalized escape time) ---
    max_steps = 800.0
    esc_norm = esc_steps / max_steps
    esc_norm = np.clip(esc_norm, 0.0, 1.0)

    # Smoothing to keep the spike numerically tame but still tall
    esc_smooth = smooth_height(esc_norm, passes=2)

    # --- Step 3: Build mesh ---
    M, L = np.meshgrid(m_vals, l_vals)
    height_scale = 3.0  # tweak this for taller/shorter column
    vertices, faces, colors = build_mesh_from_grid(
        M, L, esc_smooth, status, height_scale=height_scale
    )

    # --- Step 4: Export as PLY ---
    out_file = "pirouette_manifold_smoothed.ply"
    write_ply(out_file, vertices, faces, colors=colors)

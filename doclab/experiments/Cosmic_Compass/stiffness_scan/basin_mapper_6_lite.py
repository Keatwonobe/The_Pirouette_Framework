import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.tri import Triangulation

CACHE_PATH = "pirouette_manifold_cache.npz"

# [FIX 1] Added a stride parameter to reduce point density
def load_clean_manifold(cache_path=CACHE_PATH, max_steps=1000, stride=10):
    """
    Load M, L, Z, status. 
    stride: integer, take every Nth point to reduce memory usage.
    """
    print(f"[Δ] Loading manifold from cache: {cache_path}")
    try:
        data = np.load(cache_path)
    except FileNotFoundError:
        print(f"Error: Could not find {cache_path}")
        return np.array([]), np.array([]), np.array([]), np.array([])

    M = data["M"].astype(float)
    L = data["L"].astype(float)
    Z = data["Z"].astype(float)
    status = data["status"].astype(int)

    steps = np.expm1(Z)
    h = steps / float(max_steps)
    h = np.clip(h, 0.0, 1.0)

    # Flatten
    M_flat = M.ravel()
    L_flat = L.ravel()
    h_flat = h.ravel()
    status_flat = status.ravel()

    # Filter finite
    finite = np.isfinite(M_flat) & np.isfinite(L_flat) & np.isfinite(h_flat)
    x = M_flat[finite]
    y = L_flat[finite]
    z = h_flat[finite]
    b = status_flat[finite]

    # [FIX 1 Implementation] Apply Stride
    # If we have 1,000,000 points, stride=10 reduces it to 100,000
    if stride > 1:
        print(f"[Δ] Decimating data by factor of {stride}...")
        x = x[::stride]
        y = y[::stride]
        z = z[::stride]
        b = b[::stride]

    print(f"[Δ] Clean manifold points to plot: {x.size}")
    return x, y, z, b


def make_spin_from_cache(
    cache_path=CACHE_PATH,
    outfile="pirouette_manifold_spin.gif",
    elev=45,        # Lowered elevation slightly for better 3D look
    n_frames=120,   # [FIX 2] Reduced frames (360 is overkill for a test)
    fps=20,         # [FIX 2] Standard GIF fps
    stride=20       # [FIX 3] Default aggressive stride
):
    # 1. Load & clean with stride
    x, y, z, b = load_clean_manifold(cache_path=cache_path, stride=stride)

    if x.size == 0:
        print("No data loaded. Check cache path.")
        return

    # 2. Triangulation
    print("[Δ] Building triangulation...")
    # This is the memory heavy step. If x.size > 50,000 this will be slow.
    tri = Triangulation(x, y)

    colors = np.zeros_like(z, dtype=float)
    colors[b == 1] = 0.2
    colors[b == 2] = 0.5
    colors[b == 3] = 0.8

    fig = plt.figure(figsize=(8, 6)) # Slightly smaller figure
    ax = fig.add_subplot(111, projection="3d")

    # 3. Plot Trisurf
    print(f"[Δ] Plotting trisurf with {x.size} vertices...")
    surf = ax.plot_trisurf(
        tri,
        z,
        cmap="viridis",
        linewidth=0.0,
        antialiased=False,
    )
    surf.set_array(colors)
    surf.autoscale()

    ax.set_xlabel("m (Mass)")
    ax.set_ylabel("λ (Coupling)")
    ax.set_zlabel("Stability")
    ax.set_title(f"Manifold Spin ({x.size} pts)")

    # 4. Animation
    def init():
        ax.view_init(elev=elev, azim=0)
        return (surf,)

    def update(frame):
        # Rotate 360 degrees over n_frames
        azim = (frame / n_frames) * 360
        ax.view_init(elev=elev, azim=azim)
        return (surf,)

    print("[Δ] Creating animation...")
    anim = animation.FuncAnimation(
        fig,
        update,
        init_func=init,
        frames=n_frames,
        interval=1000 / fps,
        blit=False,
    )

    try:
        # [FIX 4] Lower DPI to 80-100 to save RAM during rendering
        print(f"[Δ] Saving animation to {outfile} (Low DPI mode)...")
        anim.save(outfile, fps=fps, dpi=80, writer='pillow') 
        print("[Δ] Done.")
    except Exception as e:
        print("[Δ] Writer failed:", repr(e))
    finally:
        plt.close(fig)

if __name__ == "__main__":
    # Adjust stride based on your resolution.
    # If your original grid is 1000x1000, use stride=50 or 100.
    make_spin_from_cache(stride=25)
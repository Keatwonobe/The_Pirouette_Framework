import numpy as np
import matplotlib.pyplot as plt
from matplotlib.tri import Triangulation
from PIL import Image
import os
import gc
import sys

CACHE_PATH = "pirouette_manifold_cache.npz"
TEMP_DIR = "temp_frames_spin"

def load_clean_manifold(cache_path=CACHE_PATH, max_steps=1000, stride=1):
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
    finite = np.isfinite(M.ravel()) & np.isfinite(L.ravel()) & np.isfinite(h.ravel())
    x = M.ravel()[finite]
    y = L.ravel()[finite]
    z = h.ravel()[finite]
    b = status.ravel()[finite]

    # Decimate
    if stride > 1:
        x = x[::stride]
        y = y[::stride]
        z = z[::stride]
        b = b[::stride]

    print(f"[Δ] Clean manifold points to plot: {x.size}")
    return x, y, z, b

def make_spin_checkpointed(
    cache_path=CACHE_PATH,
    outfile="pirouette_manifold_spin.gif",
    elev=45,
    n_frames=60,
    stride=1
):
    # 1. Setup Directories (Do NOT delete existing temp dir)
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)
        print(f"[Δ] Created temp directory: {TEMP_DIR}")
    else:
        print(f"[Δ] Found existing temp directory: {TEMP_DIR} (Resuming...)")

    # 2. Load Data
    x, y, z, b = load_clean_manifold(cache_path, stride=stride)
    if x.size == 0: return

    # 3. Triangulate
    print("[Δ] Building triangulation...")
    tri = Triangulation(x, y)

    colors = np.zeros_like(z, dtype=float)
    colors[b == 1] = 0.2
    colors[b == 2] = 0.5
    colors[b == 3] = 0.8

    # 4. Setup Figure
    # We use 'agg' backend to force off-screen rendering (more stable for scripts)
    plt.switch_backend('agg') 
    
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")
    
    print(f"[Δ] Plotting trisurf ({x.size} vertices)...")
    surf = ax.plot_trisurf(tri, z, cmap="viridis", linewidth=0.0, antialiased=False)
    surf.set_array(colors)
    surf.autoscale()
    
    ax.set_xlabel("m (Mass)")
    ax.set_ylabel("λ (Coupling)")
    ax.set_zlabel("Stability")
    ax.set_title(f"Manifold Spin ({x.size} pts)")

    filenames = []
    
    # 5. Render Loop with Checkpointing
    print(f"[Δ] Processing {n_frames} frames...")
    
    for i in range(n_frames):
        fname = os.path.join(TEMP_DIR, f"frame_{i:03d}.png")
        filenames.append(fname)
        
        # CHECKPOINT: If file exists, skip rendering
        if os.path.exists(fname):
            # We still print periodically so you know it's checking
            if i % 10 == 0:
                print(f"    [Skip] Frame {i}/{n_frames} exists.")
            continue

        # If not exists, Render
        print(f"    [Render] Frame {i}/{n_frames}...")
        
        try:
            azim = (i / n_frames) * 360
            ax.view_init(elev=elev, azim=azim)
            plt.savefig(fname, dpi=80)
            
            # FORCE MEMORY CLEANUP
            gc.collect() 
            
        except Exception as e:
            print(f"[!] Crash at frame {i}: {e}")
            print("[!] Exiting. Run script again to resume.")
            sys.exit(1)

    plt.close(fig)

    # 6. Stitching
    # Check if we actually have all frames
    existing_frames = [f for f in filenames if os.path.exists(f)]
    
    if len(existing_frames) < n_frames:
        print(f"[!] Warning: Only found {len(existing_frames)}/{n_frames} frames.")
        print("    Run the script again to finish rendering missing frames.")
    else:
        print(f"[Δ] All frames found. Stitching into {outfile}...")
        images = [Image.open(f) for f in filenames]
        images[0].save(
            outfile,
            save_all=True,
            append_images=images[1:],
            duration=50, 
            loop=0
        )
        print("[Δ] Success! GIF saved.")
        
        # Optional: Uncomment to clear temp files only on FULL success
        # import shutil
        # shutil.rmtree(TEMP_DIR)
        # print("[Δ] Temp files cleaned.")

if __name__ == "__main__":
    # Stride 1 for full detail, relying on checkpointing to get us through
    make_spin_checkpointed(stride=1)
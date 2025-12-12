import numpy as np
import os
from export_delta_manifold import compute_delta_manifold, smooth_height, build_mesh_from_grid, write_ply

# ============================================================
# LAYER DEFINITIONS
# ============================================================

LAYERS = [
    # Layer 0 — whole field
    {
        "name": "layer0",
        "m_range": (-1.5, 1.5),
        "l_range": (-1.0, 2.0),
        "resolution": 220,
        "max_steps": 800,
    },
    # Layer 1 — zoom ×2
    {
        "name": "layer1",
        "m_range": (-0.75, 0.75),
        "l_range": (-0.25, 1.5),
        "resolution": 350,
        "max_steps": 1000,
    },
    # Layer 2 — zoom ×4
    {
        "name": "layer2",
        "m_range": (-0.35, 0.35),
        "l_range": (0.1, 0.9),
        "resolution": 500,
        "max_steps": 1400,
    },
    # Layer 3 — tip region
    {
        "name": "layer3",
        "m_range": (-0.15, 0.15),
        "l_range": (0.35, 0.65),
        "resolution": 800,
        "max_steps": 2000,
    }
]

# ============================================================
# MAIN GENERATION LOOP
# ============================================================

if __name__ == "__main__":

    for layer in LAYERS:

        name = layer["name"]
        print(f"\n[Δ] GENERATING {name.upper()}")

        m_vals, l_vals, esc_steps, status = compute_delta_manifold(
            resolution=layer["resolution"],
            m_range=layer["m_range"],
            l_range=layer["l_range"],
            max_steps=layer["max_steps"],
            dt=0.05,
            sigma=1.0,
            escape_radius_sq=20.0,
        )

        # Normalize height
        esc_norm = esc_steps / layer["max_steps"]
        esc_norm = np.clip(esc_norm, 0.0, 1.0)

        # Smoothing
        esc_smooth = smooth_height(esc_norm, passes=2)

        # Create mesh
        M, L = np.meshgrid(m_vals, l_vals)
        vertices, faces, colors = build_mesh_from_grid(
            M, L, esc_smooth, status, height_scale=3.0
        )

        out_file = f"{name}.ply"
        write_ply(out_file, vertices, faces, colors)

        print(f"[Δ] Saved {out_file}")

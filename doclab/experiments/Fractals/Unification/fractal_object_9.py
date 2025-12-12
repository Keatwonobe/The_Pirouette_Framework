import numpy as np
from skimage.measure import marching_cubes
import os

# ============================================================
# 1. Load latent cloud + fields (KEYS HAVE BEEN CORRECTED)
# ============================================================

data = np.load("latent_cloud.npz")
XYZ    = data["XYZ"].astype(np.float64)            # (N, 3)
# --- FIX: Use the '_flat' suffix for the field names ---
anchor = data["anchor_flat"].astype(np.float64)
ftle   = data["ftle_flat"].astype(np.float64)
tension= data["tension_flat"].astype(np.float64)
spin   = data["spin_flat"].astype(np.float64)
stiff  = data["stiff_flat"].astype(np.float64)
# --------------------------------------------------------

N = XYZ.shape[0]
print(f"[INFO] Loaded {N} latent points")

# Optional: drop any NaNs just in case
mask = np.isfinite(XYZ).all(axis=1)
for arr in (anchor, ftle, tension, spin, stiff):
    mask &= np.isfinite(arr)
XYZ    = XYZ[mask]
anchor = anchor[mask]
ftle   = ftle[mask]
tension= tension[mask]
spin   = spin[mask]
stiff  = stiff[mask]
print(f"[INFO] After NaN filtering: {XYZ.shape[0]} points")

# ============================================================
# 2. Normalise latent coordinates into a box
#    (We'll also keep the real-world bbox for putting verts back)
# ============================================================

bbox_min = XYZ.min(axis=0)
bbox_max = XYZ.max(axis=0)
extent   = bbox_max - bbox_min
print("[INFO] Latent bbox min:", bbox_min)
print("[INFO] Latent bbox max:", bbox_max)

# Avoid zero extent
extent[extent == 0.0] = 1.0

XYZ_norm = (XYZ - bbox_min) / extent   # all coords in [0, 1]

# ============================================================
# 3. Build a high-resolution 3-D grid and voxelise
# ============================================================

# You can crank this up; 160^3 is already pretty detailed
NX = NY = NZ = 80

print(f"[INFO] Building volume grid: {NX} x {NY} x {NZ}")

# Voxel indices
ix = np.clip((XYZ_norm[:, 0] * (NX - 1)).astype(int), 0, NX - 1)
iy = np.clip((XYZ_norm[:, 1] * (NY - 1)).astype(int), 0, NY - 1)
iz = np.clip((XYZ_norm[:, 2] * (NZ - 1)).astype(int), 0, NZ - 1)

# Count hits and accumulate field sums in each voxel
hits      = np.zeros((NX, NY, NZ), dtype=np.int32)
sum_anchor= np.zeros_like(hits, dtype=np.float64)
sum_ftle  = np.zeros_like(hits, dtype=np.float64)
sum_tens  = np.zeros_like(hits, dtype=np.float64)
sum_spin  = np.zeros_like(hits, dtype=np.float64)
sum_stiff = np.zeros_like(hits, dtype=np.float64)

for k in range(XYZ_norm.shape[0]):
    i, j, k3 = ix[k], iy[k], iz[k]
    hits[i, j, k3]      += 1
    sum_anchor[i, j, k3]+= anchor[k]
    sum_ftle[i, j, k3]  += ftle[k]
    sum_tens[i, j, k3]  += tension[k]
    sum_spin[i, j, k3]  += spin[k]
    sum_stiff[i, j, k3] += stiff[k]

occupied = hits > 0
print(f"[INFO] Occupied voxels: {occupied.sum()}")

# Convert sums → voxel-averaged fields where we have points
anchor_v = np.zeros_like(sum_anchor)
ftle_v   = np.zeros_like(sum_ftle)
tens_v   = np.zeros_like(sum_tens)
spin_v   = np.zeros_like(sum_spin)
stiff_v  = np.zeros_like(sum_stiff)

anchor_v[occupied] = sum_anchor[occupied] / hits[occupied]
ftle_v[occupied]   = sum_ftle[occupied]   / hits[occupied]
tens_v[occupied]   = sum_tens[occupied]   / hits[occupied]
spin_v[occupied]   = sum_spin[occupied]   / hits[occupied]
stiff_v[occupied]  = sum_stiff[occupied]  / hits[occupied]

# ============================================================
# 4. Build a composite "world-gut density" field
#    (normalise & combine the five Pirouette fields)
# ============================================================

def norm_field(field, where, invert=False, clip_percentile=(0, 100)):
    """
    Normalise a 3-D field into [0,1] using percentiles on occupied voxels.
    If invert=True, high original values → low score.
    """
    vals = field[where]
    if vals.size == 0:
        return np.zeros_like(field, dtype=np.float64)

    lo, hi = np.percentile(vals, clip_percentile)
    if hi == lo:
        hi = lo + 1.0

    scaled = (field - lo) / (hi - lo)
    scaled = np.clip(scaled, 0.0, 1.0)
    if invert:
        scaled = 1.0 - scaled
    scaled[~where] = 0.0
    return scaled

# log tame for positive-ish fields
anchor_log = np.log1p(np.maximum(anchor_v, 0.0))
stiff_log  = np.log1p(np.maximum(stiff_v,  0.0))

A = norm_field(anchor_log, occupied)           # anchor intensity
F = norm_field(ftle_v,    occupied)           # chaos strength
T = norm_field(tens_v,    occupied, invert=True)  # less negative tension ⇒ larger
S = norm_field(spin_v,    occupied)           # spin
Q = norm_field(stiff_log, occupied)           # vacuum stiffness

# Tunable weights – this is where you impose your physics intuition.
wA, wF, wT, wS, wQ = 0.20, 0.20, 0.20, 0.20, 0.20 # Equalized Test

W = wA * A + wF * F + wT * T + wS * S + wQ * Q
W[~occupied] = 0.0

print("[INFO] Composite field stats on occupied voxels:")
print("  min, max:", W[occupied].min(), W[occupied].max())

# ============================================================
# 5. Marching cubes shells at several percentiles
# ============================================================

def export_ply(vertices, faces, filename):
    """
    Simple ASCII PLY exporter; vertices in 3-D, faces as indices.
    """
    with open(filename, "w") as f:
        f.write("ply\n")
        f.write("format ascii 1.0\n")
        f.write(f"element vertex {len(vertices)}\n")
        f.write("property float x\nproperty float y\nproperty float z\n")
        f.write(f"element face {len(faces)}\n")
        f.write("property list uchar int vertex_indices\n")
        f.write("end_header\n")
        for v in vertices:
            f.write(f"{v[0]} {v[1]} {v[2]}\n")
        for tri in faces:
            f.write(f"3 {tri[0]} {tri[1]} {tri[2]}\n")

# spacing in latent coordinates
sx = extent[0] / (NX - 1)
sy = extent[1] / (NY - 1)
sz = extent[2] / (NZ - 1)
spacing = (sx, sy, sz)

levels_percent = [30, 50, 70]   # outer / mid / inner shells
os.makedirs("latent_shells_D", exist_ok=True)

vals_occ = W[occupied]
for p in levels_percent:
    level = np.percentile(vals_occ, p)
    print(f"[INFO] Extracting shell at {p}th percentile (level={level:.4f})")

    verts, faces, normals, vals = marching_cubes(
        W.transpose(2, 1, 0),    # Volume in (Z, Y, X)
        level=level, 
        spacing=(sz, sy, sx)     # Spacing in (Z, Y, X)
    )
    # skimage marching cubes expects indices, not world coords
    # but the spacing tuple handles the aspect ratio
    verts, faces, normals, vals = marching_cubes(W.transpose(2, 1, 0), level=level, spacing=spacing)
    verts_xyz = verts[:, [2, 1, 0]]
    # Shift back into latent PCA coordinates
    # The output verts are in the coordinate system of the grid (0 to extent) 
    # so we need to add the minimum offset
    verts_world = verts + bbox_min

    out_name = os.path.join("latent_shells_D",
                            f"latent_shell_{p}p.ply")
    export_ply(verts_world, faces, out_name)
    print(f"  -> wrote {out_name} (verts={len(verts)}, faces={len(faces)})")

print("[DONE] D-mode shells exported. Load the PLYs in FreeCAD/Blender & go wild.")
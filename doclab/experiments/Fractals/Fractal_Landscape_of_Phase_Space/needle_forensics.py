import numpy as np
import matplotlib.pyplot as plt
from mass_hierarchy_apex import local_mass, find_apex
import matplotlib as mpl

# ================================================================
# PARAMETERS
# ================================================================
SPAN = 0.35       # size of region around apex (in m, λ units)
N = 400           # grid resolution
APERTURE_LEVEL = 40.0  # isocontour value for wound "mouth"


# ================================================================
# BUILD HIGH-RES PATCH
# ================================================================
def sample_patch(m0, l0, span=SPAN, n=N):
    mvals = np.linspace(m0-span, m0+span, n)
    lvals = np.linspace(l0-span, l0+span, n)
    M,L = np.meshgrid(mvals, lvals)

    Patch = np.zeros_like(M)
    for i in range(n):
        for j in range(n):
            Patch[i,j] = local_mass(M[i,j], L[i,j])

    return M,L,Patch


# ================================================================
# MASK THE NEEDLE (remove diverging spike)
# ================================================================
def mask_spike(Patch, threshold_factor=0.25):
    finite_vals = Patch[np.isfinite(Patch)]
    median = np.median(finite_vals)
    threshold = median + threshold_factor * (np.max(finite_vals)-median)
    Mask = Patch.copy()
    Mask[Patch > threshold] = np.nan
    return Mask


# ================================================================
# EXTRACT APERTURE CONTOUR
# ================================================================
def extract_isocontour(M,L,Patch,level=APERTURE_LEVEL):
    fig,ax = plt.subplots(figsize=(6,6))
    CS = ax.contour(M, L, Patch, levels=[level])
    plt.close(fig)

    # Use the longest isocontour segment (the aperture boundary)
    seg = max(CS.allsegs[0], key=lambda arr: arr.shape[0])
    return seg


# ================================================================
# POLAR ANALYSIS AROUND APEX
# ================================================================
def polar_profile(seg, m0, l0):
    xs = seg[:,0] - m0
    ys = seg[:,1] - l0
    angles = np.arctan2(ys, xs)
    radii  = np.sqrt(xs**2 + ys**2)

    # Sort by angle so the plot is continuous
    idx = np.argsort(angles)
    return angles[idx], radii[idx]


# ================================================================
# MAIN ANALYZER
# ================================================================
def main_forensics():
    # 1. Apex
    m0, l0, _, Mgrid, Lgrid, Mass = find_apex()

    print("Apex:", m0, l0)

    # 2. Patch
    M,L,P = sample_patch(m0,l0)

    # 3. Spike-removed patch
    Masked = mask_spike(P, threshold_factor=0.15)

    # 4. Extract wound aperture
    aperture = extract_isocontour(M, L, Masked, APERTURE_LEVEL)

    # 5. Polar representation
    ang,rad = polar_profile(aperture, m0, l0)

    # ============================================================
    # FIGURE A – masked wound channel (top-down)
    # ============================================================
    plt.figure(figsize=(8,8))
    plt.imshow(Masked, extent=[M.min(),M.max(),L.min(),L.max()],
               origin='lower', cmap="magma")
    plt.colorbar(label="√λ1 (masked)")
    plt.plot(aperture[:,0], aperture[:,1], 'cyan', lw=2, label="aperture")
    plt.scatter([m0],[l0], color="white", s=80, marker="*", label="apex")
    plt.legend()
    plt.title("Wound Geometry (Needle Removed)")
    plt.xlabel("m"); plt.ylabel("λ")
    plt.savefig("wound_channel_topdown.png", dpi=150)

    # ============================================================
    # FIGURE B – polar angular curvature plot
    # ============================================================
    plt.figure(figsize=(7,7))
    plt.polar(ang, rad, lw=2)
    plt.title("Polar Aperture Profile (Forensic Cross-Section)")
    plt.savefig("wound_channel_polar.png", dpi=150)

    # ============================================================
    # FIGURE C – reconstructed traveler silhouette (scaled)
    # ============================================================
    # invert radii to estimate “projectile cross section”
    inv = 1/(rad + 1e-9)
    inv = inv / np.max(inv)  # normalize to 1

    plt.figure(figsize=(7,7))
    plt.polar(ang, inv, lw=2, color="lime")
    plt.title("Reconstructed Traveler Silhouette (Normalized)")
    plt.savefig("traveler_silhouette.png", dpi=150)

    print("\nDone! Outputs written:\n"
          " - wound_channel_topdown.png\n"
          " - wound_channel_polar.png\n"
          " - traveler_silhouette.png\n")


if __name__ == "__main__":
    main_forensics()

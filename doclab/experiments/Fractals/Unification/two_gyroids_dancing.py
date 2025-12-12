import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------------
# 1. Sphere grid
# --------------------------------------------------
N_TH, N_PH = 300, 600
theta = np.linspace(0, np.pi, N_TH)
phi   = np.linspace(-np.pi, np.pi, N_PH, endpoint=False)
TH, PH = np.meshgrid(theta, phi, indexing="ij")

# Unit vectors on sphere
X = np.sin(TH) * np.cos(PH)
Y = np.sin(TH) * np.sin(PH)
Z = np.cos(TH)

# --------------------------------------------------
# 2. Two gyroids with different orientations
# --------------------------------------------------
# base wavenumber ~ sets something like "L"
k = 3.0

# Gyroid 1 (no rotation)
def gyroid1(x, y, z):
    return (np.sin(k*x)*np.cos(k*y) +
            np.sin(k*y)*np.cos(k*z) +
            np.sin(k*z)*np.cos(k*x))

# Gyroid 2: rotate coordinates around z-axis by angle alpha
alpha = np.deg2rad(35.0)
Xa =  X*np.cos(alpha) - Y*np.sin(alpha)
Ya =  X*np.sin(alpha) + Y*np.cos(alpha)
Za =  Z

def gyroid2(x, y, z):
    return (np.sin(k*x)*np.cos(k*y + 1.2) +
            np.sin(k*y)*np.cos(k*z + 0.7) +
            np.sin(k*z)*np.cos(k*x + 2.4))

G1 = gyroid1(X, Y, Z)
G2 = gyroid2(Xa, Ya, Za)

A1 = 1.0   # strong shear lattice
A2 = 0.6   # weaker lattice
T0 = A1*G1 + A2*G2   # "CMB skeleton" toy

# --------------------------------------------------
# 3. Apply your twist operator in phi
# --------------------------------------------------
def twist_map(T_base, k_twist):
    # remap phi -> k_twist*phi by interpolation
    # phi in [-pi,pi)
    Nth, Nph = T_base.shape
    phi_grid = np.linspace(-np.pi, np.pi, Nph, endpoint=False)
    # new_phi = k_twist * phi, wrap back into [-pi,pi)
    new_phi = (k_twist * phi_grid + np.pi) % (2*np.pi) - np.pi

    # build interpolation indices
    # (simple roll-based nearest neighbor is fine for visualization)
    idx = np.searchsorted(phi_grid, new_phi)
    idx = np.clip(idx, 0, Nph-1)

    return T_base[:, idx]

k_twist = -1.5
T_twisted = twist_map(T0, k_twist)

# --------------------------------------------------
# 4. Plot one frame to compare structure
# --------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(12,5), sharex=True, sharey=True)

for ax, data, title in zip(
    axes,
    [T0, T_twisted],
    [f"Base two-gyroid model",
     f"Twisted model (k={k_twist:.2f})"]
):
    im = ax.imshow(
        data,
        extent=(-180, 180, -90, 90),
        origin="lower",
        cmap="coolwarm",
        aspect="auto"
    )
    ax.set_title(title)
    ax.set_xlabel("Longitude (deg)")
    ax.set_ylabel("Latitude (deg)")

fig.colorbar(im, ax=axes.ravel().tolist(), fraction=0.03)
plt.tight_layout()
plt.show()

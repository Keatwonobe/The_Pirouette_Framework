import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

# Expanded parameter space
Gamma_vals = np.linspace(0.01, 10, 500)
omega_vals = np.linspace(0.1, 20, 500)
stability_map = np.zeros((len(Gamma_vals), len(omega_vals)))

# Improved stability function (continuous stability measure)
def stability_measure(Gamma, omega):
    # Example detailed stability function (use your realistic resonance equations)
    potential_depth = np.abs(-Gamma * np.cos(omega))
    return potential_depth

# Populate stability map with continuous measures
for i, Gamma in enumerate(Gamma_vals):
    for j, omega in enumerate(omega_vals):
        stability_map[i, j] = stability_measure(Gamma, omega)

# Enhanced plotting with LogNorm for vibrant visualization
plt.figure(figsize=(10, 7))
X, Y = np.meshgrid(omega_vals, Gamma_vals)
plt.pcolormesh(X, Y, stability_map, shading='auto', cmap='inferno', norm=LogNorm())
plt.colorbar(label='Potential Depth (Log Scale)')
plt.xlabel("Drive Frequency ω")
plt.ylabel("Gladiator Constant Γ")
plt.title("Enhanced Fractal Resonance Stability Map")
plt.tight_layout()
plt.show()

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(X, Y, np.log10(stability_map), cmap='viridis', edgecolor='none')
ax.set_xlabel('Frequency ω')
ax.set_ylabel('Gamma Γ')
ax.set_zlabel('Log Stability')
ax.set_title('3D Fractal Stability Surface')
fig.colorbar(surf, shrink=0.5, aspect=5)
plt.show()
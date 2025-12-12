import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import logging

# -------------------------------------------------
#  Shared Hamiltonian (same as your other scripts)
# -------------------------------------------------
class PirouetteHamiltonian:
    def __init__(self):
        self.coupling = 1.0

    def gradient(self, m, l):
        # Hénon–Heiles gradient
        dV_dm = m + 2 * m * l
        dV_dl = l + (m**2 - l**2)
        return dV_dm, dV_dl

# -------------------------------------------------
#  Forward "future" lifetime: how long until escape?
# -------------------------------------------------
def forward_dwell_time(m0, l0, H, dt=0.02, max_steps=4000, r_escape=3.5):
    """
    Returns the number of steps an orbit starting at (m0, l0) survives
    before leaving the central region. Interpreted as 'future lifetime'.
    """
    m, l = m0, l0
    pm, pl = 0.0, 0.0
    for t in range(max_steps):
        dV_dm, dV_dl = H.gradient(m, l)
        pm -= 0.5 * dt * dV_dm
        pl -= 0.5 * dt * dV_dl
        m  += dt * pm
        l  += dt * pl
        dV_dm, dV_dl = H.gradient(m, l)
        pm -= 0.5 * dt * dV_dm
        pl -= 0.5 * dt * dV_dl

        if m*m + l*l > r_escape**2:
            return t
    return max_steps

# -------------------------------------------------
#  Retrograde "past" lifetime: integrate backwards
# -------------------------------------------------
def backward_dwell_time(m0, l0, H, dt=-0.02, max_steps=4000, r_escape=3.5):
    """
    Same integrator, but with negative dt.
    Interpreted as 'past lifetime' (how long the history is stable).
    """
    m, l = m0, l0
    pm, pl = 0.0, 0.0
    for t in range(max_steps):
        dV_dm, dV_dl = H.gradient(m, l)
        pm -= 0.5 * dt * dV_dm
        pl -= 0.5 * dt * dV_dl
        m  += dt * pm
        l  += dt * pl
        dV_dm, dV_dl = H.gradient(m, l)
        pm -= 0.5 * dt * dV_dm
        pl -= 0.5 * dt * dV_dl

        if m*m + l*l > r_escape**2:
            return t
    return max_steps

# -------------------------------------------------
#  Present: pure rotational memory (winding count)
#  (simplified from your HelicalAnchor)
# -------------------------------------------------
def total_winding(m0, l0, H, dt=0.02, gamma=0.015,
                  max_steps=3000, r_escape=4.0,
                  v_stop=0.01):
    """
    Damped evolution measuring the accumulated absolute angle,
    i.e. helical memory.
    """
    m, l = m0, l0
    vm, vl = 0.0, 0.0
    prev_ang = np.arctan2(l, m)
    winding = 0.0

    for t in range(max_steps):
        dV_dm, dV_dl = H.gradient(m, l)
        vm += (-dV_dm - gamma * vm) * dt
        vl += (-dV_dl - gamma * vl) * dt
        m  += vm * dt
        l  += vl * dt

        ang = np.arctan2(l, m)
        delta = ang - prev_ang
        # unwrap
        if   delta >  np.pi: delta -= 2*np.pi
        elif delta < -np.pi: delta += 2*np.pi
        winding += abs(delta)
        prev_ang = ang

        speed = np.hypot(vm, vl)
        if speed < v_stop or (m*m + l*l > r_escape**2):
            break

    # convert to "turns" rather than raw radians
    return winding / (2*np.pi)

# -------------------------------------------------
#  Grid scan & normalization helpers
# -------------------------------------------------
def scan_fields(res=300, bounds=1.5):
    H = PirouetteHamiltonian()
    m_vals = np.linspace(-bounds, bounds, res)
    l_vals = np.linspace(-bounds, bounds, res)

    F = np.zeros((res, res), dtype=np.float32)  # forward lifetime
    B = np.zeros((res, res), dtype=np.float32)  # backward lifetime
    W = np.zeros((res, res), dtype=np.float32)  # winding count

    for i, l0 in enumerate(l_vals):
        print(f"row {i+1}/{res}")
        for j, m0 in enumerate(m_vals):
            F[i, j] = forward_dwell_time(m0, l0, H)
            B[i, j] = backward_dwell_time(m0, l0, H)
            W[i, j] = total_winding(m0, l0, H)

    # log-rescale each for visualization and composite
    def norm_log(arr):
        arr = np.log1p(arr)
        arr -= arr.min()
        arr /= arr.max() + 1e-9
        return arr

    Fn = norm_log(F)
    Bn = norm_log(B)
    Wn = norm_log(W)

    return m_vals, l_vals, Fn, Bn, Wn

def make_static_composite(m_vals, l_vals, Fn, Bn, Wn, fname="time_composite.png"):
    """
    RGB composite:
    R = past (retrograde)
    G = present memory (winding)
    B = future (forward)
    """
    rgb = np.stack([Bn, Wn, Fn], axis=-1)
    rgb = np.clip(rgb, 0.0, 1.0)

    fig, ax = plt.subplots(figsize=(8, 8), facecolor="#050510")
    ax.imshow(rgb, origin="lower",
              extent=[m_vals[0], m_vals[-1], l_vals[0], l_vals[-1]])
    ax.set_xlabel("Mass field m", color="white")
    ax.set_ylabel("Coupling field λ", color="white")
    ax.tick_params(colors="white")
    ax.set_title("Time-Symmetric Composite (Past / Present / Future)", color="cyan")
    plt.tight_layout()
    plt.savefig(fname, dpi=200, facecolor="#050510")
    print(f"saved {fname}")

# -------------------------------------------------
#  Optional GIF: morph from past→present→future
# -------------------------------------------------
def make_time_gif(m_vals, l_vals, Fn, Bn, Wn, fname="time_morph.gif"):
    rgb_frames = []
    alphas = np.linspace(0.0, 1.0, 40)  # 0 = pure past, 1 = pure future

    for a in alphas:
        # blend past/future, always include winding
        R = (1-a)*Bn
        G = Wn
        B = a*Fn
        rgb = np.stack([R, G, B], axis=-1)
        rgb_frames.append(np.clip(rgb, 0, 1))

    fig, ax = plt.subplots(figsize=(6, 6), facecolor="#050510")
    im = ax.imshow(rgb_frames[0], origin="lower",
                   extent=[m_vals[0], m_vals[-1], l_vals[0], l_vals[-1]])
    ax.set_axis_off()

    def update(frame_idx):
        im.set_data(rgb_frames[frame_idx])
        return (im,)

    anim = animation.FuncAnimation(fig, update,
                                   frames=len(rgb_frames),
                                   interval=100,
                                   blit=True)
    anim.save(fname, writer="pillow", fps=15)
    print(f"saved {fname}")

if __name__ == "__main__":
    m_vals, l_vals, Fn, Bn, Wn = scan_fields(res=250, bounds=1.5)
    make_static_composite(m_vals, l_vals, Fn, Bn, Wn)
    make_time_gif(m_vals, l_vals, Fn, Bn, Wn)

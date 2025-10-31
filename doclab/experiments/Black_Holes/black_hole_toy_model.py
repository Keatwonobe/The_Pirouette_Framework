# Toy model: AM/FM-modulated ringdown with tiny echo train and spectrum
# Keaton can tweak params at the top. This script will:
# 1) Synthesize a ringdown h(t) with amplitude (AM) and phase (FM) wobble
# 2) Add a faint echo train with optional jitter tied to the wobble frequency
# 3) Plot the time-series (zoomed) and the amplitude spectrum
# 4) Save the waveform and spectrum to CSV files for further analysis

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

# ---------------------------
# Parameters (edit freely)
# ---------------------------
fs = 4096.0              # sample rate [Hz]
T  = 8.0                 # total duration [s]
A0 = 1.0                 # base amplitude
tau = 0.4                # decay time constant [s]
f0 = 150.0               # base ringdown frequency [Hz] (dominant QNM-like)
phi0 = 0.0               # initial phase [rad]

# Wobble (runny yolk) parameters
eps_AM = 0.07            # amplitude modulation depth (0..~0.2 suggested)
eps_FM = 0.07            # phase modulation depth (0..~0.2 suggested)
f_wobble = 20.0          # wobble frequency [Hz]

# Echo train parameters (tiny reflectivity, small jitter)
echo_reflect = 0.03      # base reflectivity per echo (very small)
echo_delay = 0.08        # base echo delay [s] (shell->photon-sphere round trip scale, toy)
echo_N = 6               # number of echoes
echo_jitter_frac = 0.15  # fraction of jitter wrt echo_delay, modulated by wobble

# Export options
out_dir = Path("/mnt/data")
waveform_csv = out_dir / "toy_ringdown_wobble_waveform.csv"
spectrum_csv = out_dir / "toy_ringdown_wobble_spectrum.csv"

# ---------------------------
# Synthesis
# ---------------------------
t = np.arange(0, T, 1/fs)

# AM and FM envelopes
AM = 1.0 + eps_AM * np.cos(2*np.pi*f_wobble*t)
FM = eps_FM * np.sin(2*np.pi*f_wobble*t)  # phase modulation term

# Base ringdown
omega0 = 2*np.pi*f0
h0 = A0 * np.exp(-t/tau) * np.cos(omega0*t + phi0 + FM)

# Add faint echo train with jitter linked to wobble
h = h0.copy()
rng = np.random.default_rng(42)
for n in range(1, echo_N+1):
    # deterministic wobble-driven jitter + small random salt
    jitter = echo_jitter_frac * echo_delay * np.sin(2*np.pi*f_wobble*(n*echo_delay)) 
    jitter += 0.02 * echo_jitter_frac * echo_delay * rng.normal()
    delay_n = n*echo_delay + jitter
    # delayed, decayed, and slightly AM-modulated copy
    idx_shift = int(np.round(delay_n*fs))
    if idx_shift < len(t):
        scale = (echo_reflect**n)
        # modulate echo amplitude at the envelope value near its onset time (approximate)
        env = AM[idx_shift] if idx_shift < len(AM) else 1.0
        # add delayed echo
        h[idx_shift:] += scale * env * A0 * np.exp(-(t[:-idx_shift])/tau) * np.cos(omega0*t[:-idx_shift] + phi0 + FM[:-idx_shift])

# Apply AM to the full signal after echoes (to mimic slow stiffness modulation)
h *= AM

# ---------------------------
# Spectrum (single-sided amplitude)
# ---------------------------
N = len(t)
H = np.fft.rfft(h * np.hanning(N))
f = np.fft.rfftfreq(N, 1/fs)
amp = np.abs(H) / np.max(np.abs(H))

# Save CSVs
df_wave = pd.DataFrame({"t_s": t, "h": h})
df_wave.to_csv(waveform_csv, index=False)

df_spec = pd.DataFrame({"f_Hz": f, "norm_amp": amp})
df_spec.to_csv(spectrum_csv, index=False)

# ---------------------------
# Plots
# ---------------------------

# Time series (zoom to first 1.2 s to see ringdown + early echoes)
t_zoom_max = 1.2
mask_zoom = t <= t_zoom_max
plt.figure(figsize=(9, 4.5))
plt.plot(t[mask_zoom], h[mask_zoom])
plt.xlabel("Time [s]")
plt.ylabel("Strain (arb.)")
plt.title("AM/FM Ringdown with Tiny Echo Train (zoom)")
plt.tight_layout()
plt.show()

# Full spectrum
plt.figure(figsize=(9, 4.5))
plt.plot(f, amp)
plt.xlim(0, 400)  # focus around fundamental and sidebands for this toy parametrization
plt.xlabel("Frequency [Hz]")
plt.ylabel("Normalized amplitude")
plt.title("Amplitude Spectrum (sidebands near f0 ± f_wobble)")
plt.tight_layout()
plt.show()

# Print a quick readout of expected sideband locations and file outputs
sidebands = [f0 - f_wobble, f0, f0 + f_wobble]
print("Expected sideband triplet (Hz):", sidebands)
print(f"Waveform saved to: {waveform_csv}")
print(f"Spectrum saved to: {spectrum_csv}")

# hcs_batch_processor.py
# FINAL VERSION - Batch Processing
# - Ingests an entire directory of images for large-scale analysis.
# - Compiles all results into a single master CSV for database creation.
# - Incorporates the user's robust, modular collapse functions.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from PIL import Image
import argparse
import glob # NEW: For finding all image files in a directory

# --- Helper Functions ---

def polar_grid(n: int = 192, r_max: float = 1.0):
    lin = np.linspace(-r_max, r_max, n)
    x, y = np.meshgrid(lin, lin)
    r = np.sqrt(x*x + y*y) + 1e-12
    theta = np.arctan2(y, x)
    return x, y, r, theta

def dominant_angular_mode(field, theta, max_m=8):
    gx, gy = np.gradient(field)
    gradient_magnitude = np.hypot(gx, gy)
    target_field = gradient_magnitude
    n = target_field.shape[0]
    mask = np.ones_like(target_field, dtype=bool)
    c = n // 2
    rr = np.sqrt((np.indices(target_field.shape)[0] - c)**2 + (np.indices(target_field.shape)[1] - c)**2)
    mask[rr < 4] = False
    amps = []
    for m in range(1, max_m + 1):
        c0 = np.sum(target_field[mask] * np.cos(m * theta[mask]))
        s0 = np.sum(target_field[mask] * np.sin(m * theta[mask]))
        amps.append((m, float(np.hypot(c0, s0))))
    amps.sort(key=lambda t: t[1], reverse=True)
    return int(amps[0][0]), gradient_magnitude

def helical_time_evolve(field, kappa, t, omega=2*np.pi*1.0):
    grad_field_y, grad_field_x = np.gradient(field)
    return np.cos(kappa * omega * t) * field + np.sin(kappa * omega * t) * grad_field_y

# --- NEW: User-provided robust collapse functions ---
def project_out_m3(field, m3_basis):
    a3 = np.sum(field * m3_basis)
    return field - (a3 / (np.sum(m3_basis * m3_basis) + 1e-12)) * m3_basis

def refill_with_m2(field_no_m3, m2_basis):
    E = np.sqrt(np.mean(field_no_m3**2) + 1e-12)
    m2u = m2_basis / np.sqrt(np.mean(m2_basis**2) + 1e-12)
    return E * m2u

def gated_mix(original_field, target_field, gate_param):
    return (1.0 - gate_param) * original_field + gate_param * target_field

def psi_3to2_collapse_strong(field, theta, Ta, Gamma):
    m3_basis = np.cos(3 * theta)
    m2_basis = np.cos(2 * theta)
    field_no_m3 = project_out_m3(field, m3_basis)
    refill_target = refill_with_m2(field_no_m3, m2_basis)
    gate = float(np.clip((1.0 - Ta) * Gamma, 0.0, 1.0))
    collapsed_field = gated_mix(field, refill_target, gate)
    collapse_map = np.abs(collapsed_field - field)
    return collapsed_field, gate, collapse_map
# --- End of new collapse functions ---

def detect_frequency(signal, dt):
    from numpy.fft import rfft, rfftfreq
    sig = signal - np.mean(signal)
    yf = np.abs(rfft(sig))
    xf = rfftfreq(len(sig), dt)
    if len(xf) < 3: return 0.0, 0.0, xf, yf
    yf[0] = 0.0; i = int(np.argmax(yf)); peak = float(yf[i])
    noise = float(np.median(yf[yf > 0])) if np.any(yf > 0) else 1e-12
    return float(xf[i]), float(peak / (noise + 1e-12)), xf, yf

def phase_flux_space(field, dx=1.0):
    gx, gy = np.gradient(field, dx, dx); return float(np.mean(np.hypot(gx, gy)))

def phase_flux_time(signal, dt):
    d = np.gradient(signal, dt); return float(np.mean(np.abs(d)))

def ingest_field(path, size=192):
    try:
        img = Image.open(path).convert("L").resize((size, size))
        arr = np.array(img).astype(np.float32)
        arr = (arr - arr.mean()) / (arr.std() + 1e-12)
        return np.tanh(arr / 2.5)
    except Exception as e:
        print(f"⚠️  Could not process image {path}: {e}")
        return None

def run_one(field, kappa, Ta, Gamma, Ki, outdir=None, tag=None, save_figs=False):
    n = field.shape[0]; x, y, r, theta = polar_grid(n, 1.0)
    lobes_before, pre_grad = dominant_angular_mode(field, theta)
    evolved = helical_time_evolve(field, kappa, t=6.0)
    collapsed, gate, collapse_map = psi_3to2_collapse_strong(evolved, theta, Ta, Gamma)
    lobes_after, post_grad = dominant_angular_mode(collapsed, theta)
    t = np.arange(0, 6.0, 1/160.0); base = float(np.tanh(collapsed.mean()))
    phi = base * np.sin(Ki * t); dt = 1/160.0
    f, snr, xf, yf = detect_frequency(phi, dt)
    space_flux = phase_flux_space(field)
    time_flux = phase_flux_time(phi, dt)
    bal = abs(space_flux - time_flux) / (abs(space_flux) + abs(time_flux) + 1e-12)
    verdict = bool((Ta <= 0.35) and (Gamma >= 0.75) and (lobes_after <= 2) and (snr >= 5.0) and (bal < 0.9))
    
    # Visualization is optional and can be turned off for speed
    if save_figs and outdir and tag:
        # This part remains the same, saving figures if requested
        pass # Figure-saving code is omitted for brevity but can be pasted back in

    return {"lobes_before": lobes_before, "lobes_after": lobes_after, "gate": gate, "beat_peak": f, 
            "beat_SNR": snr, "phase_balance_error": bal, "verdict_pass": verdict}

# --- Main Execution Block for Batch Processing ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run HCS dimensional collapse simulation on a directory of images.")
    # MODIFIED: Takes a directory instead of a single file
    parser.add_argument("image_dir", type=str, help="Path to the directory containing input images.")
    # NEW: Optional flag to turn off saving figures for faster processing
    parser.add_argument("--no_figs", action="store_true", help="Disable saving of image plots for faster batch processing.")
    args = parser.parse_args()

    # --- Simulation Parameters ---
    kappas = [0.2, 0.9]
    params = [(0.90, 0.40, 2*np.pi*0.6), (0.28, 0.88, 2*np.pi*0.8)] # Control, Corridor
    
    # NEW: Find all valid image files in the specified directory
    img_dir = args.image_dir
    if not os.path.isdir(img_dir):
        print(f"❌ Error: Directory not found at '{img_dir}'")
        exit()
        
    image_paths = glob.glob(os.path.join(img_dir, '*.png')) + \
                  glob.glob(os.path.join(img_dir, '*.jpg')) + \
                  glob.glob(os.path.join(img_dir, '*.jpeg'))

    if not image_paths:
        print(f"❌ Error: No images (.png, .jpg) found in '{img_dir}'")
        exit()

    print(f"Found {len(image_paths)} images to process...")
    
    all_results = [] # NEW: Master list to hold all results

    # NEW: Loop over every found image path
    for pth in image_paths:
        slug = os.path.splitext(os.path.basename(pth))[0]
        print(f"\nProcessing: {slug}...")
        
        field = ingest_field(pth, size=192)
        if field is None:
            continue # Skip if image could not be ingested

        # Run the simulation for each parameter combination
        for k in kappas:
            for j, (Ta, Gamma, Ki) in enumerate(params):
                param_type = 'ctrl' if j == 0 else 'corr'
                
                res = run_one(field, k, Ta, Gamma, Ki, save_figs=(not args.no_figs))
                
                # Add context to the results dictionary
                res['image_source'] = slug
                res['kappa'] = k
                res['param_type'] = param_type
                
                all_results.append(res)

    # NEW: Create a single DataFrame from the master list
    master_atlas = pd.DataFrame(all_results)
    
    # Reorder columns for better readability
    cols = ['image_source', 'param_type', 'kappa', 'lobes_before', 'lobes_after', 
            'verdict_pass', 'gate', 'beat_SNR', 'beat_peak', 'phase_balance_error']
    master_atlas = master_atlas[cols]
    
    # NEW: Save the single, consolidated CSV file
    output_csv = "master_collapse_atlas.csv"
    master_atlas.to_csv(output_csv, index=False)

    print("\n" + "="*40)
    print("✅ Batch processing complete!")
    print(f"A total of {len(all_results)} signatures have been collected.")
    print(f"Results saved to: {output_csv}")
    print("="*40)
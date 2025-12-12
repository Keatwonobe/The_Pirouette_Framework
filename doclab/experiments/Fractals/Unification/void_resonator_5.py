import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt
import imageio.v2 as imageio
import os

# Check for acceleration
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"[-] Initializing Differentiable Physics Engine on {DEVICE}...")

# ============================================================
# 1. THE STABILIZED PHYSICS CELL
# ============================================================

class WadaPhysicsCell(nn.Module):
    def __init__(self):
        super().__init__()
        
    def forward(self, m, l, pm, pl, sigma, dt=0.1):
        # 1st Kick
        fm = -(m + 2 * sigma * m * l)
        fl = -(l + sigma * (m**2 - l**2))
        pm = pm + 0.5 * dt * fm
        pl = pl + 0.5 * dt * fl
        
        # Drift
        m = m + dt * pm
        l = l + dt * pl
        
        # 2nd Kick
        fm = -(m + 2 * sigma * m * l)
        fl = -(l + sigma * (m**2 - l**2))
        pm = pm + 0.5 * dt * fm
        pl = pl + 0.5 * dt * fl
        
        # SAFETY CLAMP: Prevent particles from flying to infinity
        # If a particle hits infinity, it generates NaN gradients.
        m = torch.clamp(m, -20.0, 20.0)
        l = torch.clamp(l, -20.0, 20.0)
        
        return m, l, pm, pl

class HolographicObserver(nn.Module):
    def __init__(self, initial_sigma_guess=1.0):
        super().__init__()
        self.sigma_belief = nn.Parameter(torch.tensor([initial_sigma_guess], dtype=torch.float32))
        self.physics = WadaPhysicsCell()
        
    def predict_next_step(self, m_obs, l_obs, pm_est, pl_est):
        return self.physics(m_obs, l_obs, pm_est, pl_est, self.sigma_belief)

# ============================================================
# 2. THE REALITY GENERATOR (Ground Truth)
# ============================================================

def generate_reality_step(m, l, pm, pl, true_sigma, dt=0.1):
    # Standard Numpy implementation
    fm = -(m + 2 * true_sigma * m * l)
    fl = -(l + true_sigma * (m**2 - l**2))
    pm += 0.5 * dt * fm
    pl += 0.5 * dt * fl
    m += dt * pm
    l += dt * pl
    fm = -(m + 2 * true_sigma * m * l)
    fl = -(l + true_sigma * (m**2 - l**2))
    pm += 0.5 * dt * fm
    pl += 0.5 * dt * fl
    
    # Boundary (Soft bounce)
    mask = (m**2 + l**2) > 9.0
    m[mask] *= 0.5; l[mask] *= 0.5
    pm[mask] *= -0.5; pl[mask] *= -0.5
        
    return m, l, pm, pl

# ============================================================
# 3. THE EXPERIMENT
# ============================================================

def run_stabilized_brain():
    RES = 1000 # Slightly lower for faster GIF rendering
    N_SENSORS = 500 
    LEARNING_RATE = 0.02
    ITERATIONS = 5
    FRAMES = 120
    
    print(f"[-] Allocating Universe ({RES}x{RES})...")
    
    # 1. Initialize Reality
    y, x = np.mgrid[-2:2:complex(0, RES), -2:2:complex(0, RES)]
    real_m = x.astype(np.float32)
    real_l = y.astype(np.float32)
    real_pm = np.zeros_like(real_m)
    real_pl = np.zeros_like(real_l)
    
    # 2. Sensors
    sensor_idx_flat = np.random.choice(RES*RES, N_SENSORS, replace=False)
    
    # 3. The Brain
    observer = HolographicObserver(initial_sigma_guess=0.5).to(DEVICE)
    optimizer = torch.optim.Adam(observer.parameters(), lr=LEARNING_RATE)
    
    true_sigma = 1.15
    
    # Setup Plotting
    fig, axes = plt.subplots(1, 3, figsize=(15, 5), facecolor='#111111')
    for ax in axes: ax.axis('off')
    
    # Pre-compute phase masks for faster rendering
    # (We render a downscaled version for the GIF to keep it fast)
    vis_res = 400
    dummy = np.zeros((vis_res, vis_res))
    im_truth = axes[0].imshow(dummy, cmap='inferno', vmin=-1, vmax=1)
    im_halluc = axes[1].imshow(dummy, cmap='inferno', vmin=-1, vmax=1)
    im_error = axes[2].imshow(dummy, cmap='gray', vmin=0, vmax=0.1)
    
    axes[0].set_title("The Void (Reality)", color='cyan')
    axes[1].set_title("The Hallucination (Brain)", color='magenta')
    axes[2].set_title("Structural Defect", color='orange')
    
    txt_info = axes[1].text(5, 20, "Initializing...", color='white', fontsize=10, 
                            bbox=dict(facecolor='black', alpha=0.5))
    
    # Momentum estimates for the brain
    est_pm = torch.zeros(N_SENSORS, device=DEVICE)
    est_pl = torch.zeros(N_SENSORS, device=DEVICE)
    
    frames_buffer = []
    
    print("[-] Streaming Reality & Recording GIF...")
    
    try:
        for t in range(FRAMES):
            
            # --- REALITY ---
            real_m, real_l, real_pm, real_pl = generate_reality_step(
                real_m, real_l, real_pm, real_pl, true_sigma
            )
            
            # --- SENSING ---
            flat_m = real_m.ravel(); flat_l = real_l.ravel()
            sensor_m_truth = torch.tensor(flat_m[sensor_idx_flat], device=DEVICE)
            sensor_l_truth = torch.tensor(flat_l[sensor_idx_flat], device=DEVICE)
            
            if t == 0:
                prev_sensor_m = sensor_m_truth.clone()
                prev_sensor_l = sensor_l_truth.clone()
                continue
            
            # --- LEARNING (Backprop) ---
            loss_val = 0
            for _ in range(ITERATIONS):
                optimizer.zero_grad()
                pred_m, pred_l, new_pm, new_pl = observer.predict_next_step(
                    prev_sensor_m, prev_sensor_l, est_pm, est_pl
                )
                
                loss = torch.mean((pred_m - sensor_m_truth)**2 + (pred_l - sensor_l_truth)**2)
                loss.backward()
                
                # CLIP GRADIENTS
                torch.nn.utils.clip_grad_norm_(observer.parameters(), max_norm=1.0)
                
                optimizer.step()
                
                # CLAMP PARAMETERS
                observer.sigma_belief.data.clamp_(0.1, 3.0)
                
                est_pm = new_pm.detach()
                est_pl = new_pl.detach()
                loss_val = loss.item()

            prev_sensor_m = sensor_m_truth.clone()
            prev_sensor_l = sensor_l_truth.clone()
            
            # --- HALLUCINATION (Rendering) ---
            current_belief = observer.sigma_belief.item()
            
            # Downsample for visualization speed
            step = RES // vis_res
            vis_m = real_m[::step, ::step]
            vis_l = real_l[::step, ::step]
            
            # Simulate Hallucination on CPU for Vis
            halluc_m, halluc_l, _, _ = generate_reality_step(
                vis_m.copy(), vis_l.copy(), 
                np.zeros_like(vis_m), np.zeros_like(vis_l),
                current_belief
            )
            
            img_truth = np.sin(vis_m*5) * np.cos(vis_l*5)
            img_halluc = np.sin(halluc_m*5) * np.cos(halluc_l*5)
            img_err = np.abs(img_truth - img_halluc)
            
            im_truth.set_data(img_truth)
            im_halluc.set_data(img_halluc)
            im_error.set_data(img_err)
            
            acc = 100 * (1.0 - np.mean(img_err))
            txt_info.set_text(
                f"T={t} | True Sigma: {true_sigma:.3f}\n"
                f"Brain Belief: {current_belief:.3f}\n"
                f"Loss: {loss_val:.5f}\n"
                f"Acc: {acc:.1f}%"
            )
            
            # --- FIXED FRAME CAPTURE ---
            fig.canvas.draw()
            # Modern Matplotlib method for RGBA buffer
            image = np.frombuffer(fig.canvas.buffer_rgba(), dtype='uint8')
            image = image.reshape(fig.canvas.get_width_height()[::-1] + (4,))
            image = image[:, :, :3] # Slice off Alpha channel to keep it RGB
            
            frames_buffer.append(image)
            
            print(f"Frame {t}/{FRAMES} | Belief: {current_belief:.4f} (Err: {abs(true_sigma-current_belief):.4f})")
            
            # Drift Truth
            true_sigma += 0.003 * np.cos(t * 0.1)

    except KeyboardInterrupt:
        print("Interrupted. Saving what we have...")
        
    print("[-] Compiling GIF...")
    imageio.mimsave('wada_brain_stabilized.gif', frames_buffer, fps=15)
    print("[+] GIF Saved: 'wada_brain_stabilized.gif'")

if __name__ == "__main__":
    run_stabilized_brain()
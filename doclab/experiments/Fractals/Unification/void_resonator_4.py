import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt
import time

# Check for acceleration
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"[-] Initializing Differentiable Physics Engine on {DEVICE}...")

# ============================================================
# 1. THE DIFFERENTIABLE BRAIN (Instilled Physics)
# ============================================================

class WadaPhysicsCell(nn.Module):
    """
    This is not a standard RNN. This is a Neural Network layer
    that explicitly encodes the differential equations of the Wada Basin.
    
    Because it is built in PyTorch, it is fully differentiable.
    We can backpropagate through the chaos.
    """
    def __init__(self):
        super().__init__()
        
    def forward(self, m, l, pm, pl, sigma, dt=0.1):
        # We perform the integration steps using Torch tensors
        # This allows gradients to flow from the output back to 'sigma'
        
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
        
        return m, l, pm, pl

class HolographicObserver(nn.Module):
    def __init__(self, initial_sigma_guess=1.0):
        super().__init__()
        # The parameter we want to discover.
        # We make it a Learnable Parameter of the network.
        self.sigma_belief = nn.Parameter(torch.tensor([initial_sigma_guess], dtype=torch.float32))
        self.physics = WadaPhysicsCell()
        
    def predict_next_step(self, m_obs, l_obs, pm_est, pl_est):
        # Run the internal physics using the CURRENT belief of sigma
        return self.physics(m_obs, l_obs, pm_est, pl_est, self.sigma_belief)

# ============================================================
# 2. THE HIGH-RES REALITY (Ground Truth Generator)
# ============================================================

def generate_reality_step(m, l, pm, pl, true_sigma, dt=0.1):
    # Standard Numpy implementation for the "World"
    # (The model never sees this code, it only sees the output data)
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

def run_differentiable_holography():
    # SETTINGS
    RES = 2000
    N_SENSORS = 500 # 0.0125% of the data
    LEARNING_RATE = 0.05
    ITERATIONS = 5
    
    print(f"[-] Allocating 4-Megapixel Grid ({RES}x{RES})...")
    
    # 1. Initialize Reality
    y, x = np.mgrid[-2:2:complex(0, RES), -2:2:complex(0, RES)]
    real_m = x.astype(np.float32)
    real_l = y.astype(np.float32)
    real_pm = np.zeros_like(real_m)
    real_pl = np.zeros_like(real_l)
    
    # 2. Initialize Sensors (The Sparse Interface)
    # We pick random indices to monitor
    sensor_idx_flat = np.random.choice(RES*RES, N_SENSORS, replace=False)
    
    # 3. Initialize The Brain
    # The brain starts with a WRONG belief (Sigma = 0.5)
    # The Truth is somewhere else (Sigma = 1.0 -> 1.4)
    observer = HolographicObserver(initial_sigma_guess=0.5).to(DEVICE)
    optimizer = torch.optim.Adam(observer.parameters(), lr=LEARNING_RATE)
    
    true_sigma = 1.15
    
    # Setup Plotting
    plt.ion()
    fig, axes = plt.subplots(1, 3, figsize=(16, 6), facecolor='#111111')
    for ax in axes: ax.axis('off')
    im_truth = axes[0].imshow(np.zeros((500,500)), cmap='inferno', vmin=-1, vmax=1) # Low res preview
    im_hallucination = axes[1].imshow(np.zeros((500,500)), cmap='inferno', vmin=-1, vmax=1)
    im_error = axes[2].imshow(np.zeros((500,500)), cmap='gray', vmin=0, vmax=0.1)
    
    axes[0].set_title("The Void (Reality)", color='cyan')
    axes[1].set_title("The Brain (Differentiable Reconstruction)", color='magenta')
    axes[2].set_title(f"Structural Defect (Error)", color='orange')
    
    txt_info = axes[1].text(10, 50, "Initializing...", color='white', fontsize=12)
    
    print("[-] Streaming Reality...")
    
    # Internal estimation of momentum for the sensors (since we can't see it)
    est_pm = torch.zeros(N_SENSORS, device=DEVICE)
    est_pl = torch.zeros(N_SENSORS, device=DEVICE)
    
    loss_history = []
    
    try:
        for t in range(200):
            
            # --- A. REALITY STEP (Hidden) ---
            # Moves the full 4M pixels
            real_m, real_l, real_pm, real_pl = generate_reality_step(
                real_m, real_l, real_pm, real_pl, true_sigma
            )
            
            # Extract Sensor Data (Ground Truth for the Brain)
            flat_m = real_m.ravel(); flat_l = real_l.ravel()
            sensor_m_truth = torch.tensor(flat_m[sensor_idx_flat], device=DEVICE)
            sensor_l_truth = torch.tensor(flat_l[sensor_idx_flat], device=DEVICE)
            
            # --- B. THE BRAIN LEARNS (The "Ah-ha!" Moment) ---
            # The brain takes the *previous* known sensor positions and tries to predict *current* positions.
            # It updates 'sigma' to minimize the difference.
            
            # For this loop, we just use current state to predict next state to align parameters
            # In a real scenario, we'd use t-1 to predict t.
            # Here we "overfit" the physics to the current observation frame by frame.
            
            if t > 0: # Need history
                for _ in range(ITERATIONS):
                    optimizer.zero_grad()
                    
                    # Brain predicts where sensors *should* be based on its belief
                    pred_m, pred_l, new_pm, new_pl = observer.predict_next_step(
                        prev_sensor_m, prev_sensor_l, est_pm, est_pl
                    )
                    
                    # Calculate Physics Loss (how wrong was the prediction?)
                    loss = torch.mean((pred_m - sensor_m_truth)**2 + (pred_l - sensor_l_truth)**2)
                    
                    # BACKPROPAGATION: The magic step.
                    # We compute gradient of Error w.r.t Sigma and update belief.
                    loss.backward()
                    optimizer.step()
                    
                    # Update internal momentum estimates
                    # In Differentiable Physics, we track the momentum of the *model*
                    est_pm = new_pm.detach() 
                    est_pl = new_pl.detach()
            
            # Store current sensors as "previous" for next frame
            prev_sensor_m = sensor_m_truth.clone()
            prev_sensor_l = sensor_l_truth.clone()
            
            # --- C. HALLUCINATION (Reconstructing the Universe) ---
            # Now that the brain has tuned its Sigma using only 500 points,
            # we ask it: "What does the WHOLE universe look like?"
            
            current_belief = observer.sigma_belief.item()
            
            # To visualize, we generate a low-res preview of the full belief
            # (Generating full 2000x2000 every frame for plot is slow in Matplotlib, 
            # so we downsample the 'Truth' and simulate a 'Model' run on CPU for vis)
            
            vis_step = 4 # Downsample 2000 -> 500
            
            # 1. Visualization Truth
            vis_m = real_m[::vis_step, ::vis_step]
            vis_l = real_l[::vis_step, ::vis_step]
            
            # 2. Visualization Hallucination
            # We take the *Previous* full frame and apply the *Learned* sigma
            # Note: In a pure blind run, the Oracle would maintain its own full state.
            # Here we show the *predictive power*: If we applied the learned sigma to the field.
            
            # Run one CPU step with the learned sigma on the downsampled grid
            halluc_m, halluc_l, _, _ = generate_reality_step(
                vis_m.copy(), vis_l.copy(), 
                np.zeros_like(vis_m), np.zeros_like(vis_l), # ignoring momentum for vis drift
                current_belief
            )
            
            # Render Phase patterns
            img_truth = np.sin(vis_m*5) * np.cos(vis_l*5)
            img_halluc = np.sin(halluc_m*5) * np.cos(halluc_l*5)
            img_err = np.abs(img_truth - img_halluc)
            
            # Update Plots
            im_truth.set_data(img_truth)
            im_hallucination.set_data(img_halluc)
            im_error.set_data(img_err)
            
            acc = 100 * (1.0 - np.mean(img_err))
            txt_info.set_text(
                f"Frame: {t}\n"
                f"True Sigma: {true_sigma:.4f}\n"
                f"Brain Belief: {current_belief:.4f}\n"
                f"Sensors: {N_SENSORS}\n"
                f"Reconstruction Acc: {acc:.1f}%"
            )
            
            if t % 5 == 0:
                print(f"T={t} | Belief: {current_belief:.4f} (Err: {abs(true_sigma-current_belief):.4f})")
                fig.canvas.draw()
                fig.canvas.flush_events()
                
            # Drift the truth slowly to see if Brain keeps up
            true_sigma += 0.002 * np.sin(t * 0.1)

    except KeyboardInterrupt:
        pass
        
    plt.savefig("wada_holographic_brain.png")
    print("[+] Experiment Complete.")

if __name__ == "__main__":
    run_differentiable_holography()
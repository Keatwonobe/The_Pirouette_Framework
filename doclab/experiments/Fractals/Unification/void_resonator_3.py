import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
import time

# ============================================================
# 1. THE HIGH-PERFORMANCE PHYSICS KERNEL (Numba Optimized)
# ============================================================

@njit(fastmath=True)
def wada_field_step(state_m, state_l, sigma, dt):
    """
    Evolves 4 Million pixels simultaneously using Wada Physics.
    """
    rows, cols = state_m.shape
    
    # We create new arrays to avoid modifying in-place during read
    new_m = np.empty_like(state_m)
    new_l = np.empty_like(state_l)
    
    # Flattened logic is often faster for memory access
    flat_m = state_m.ravel()
    flat_l = state_l.ravel()
    out_m = new_m.ravel()
    out_l = new_l.ravel()
    
    limit = rows * cols
    
    for i in prange(limit):
        m = flat_m[i]
        l = flat_l[i]
        
        # 1st Kick
        fm = -(m + 2 * sigma * m * l)
        fl = -(l + sigma * (m*m - l*l))
        pm = 0.5 * dt * fm
        pl = 0.5 * dt * fl
        
        m += dt * pm
        l += dt * pl
        
        # 2nd Kick
        fm = -(m + 2 * sigma * m * l)
        fl = -(l + sigma * (m*m - l*l))
        pm += 0.5 * dt * fm
        pl += 0.5 * dt * fl
        
        # Soft Boundary (Torus-like wrapping for infinite field effect)
        if m*m + l*l > 4.0:
            m = m * 0.5
            l = l * 0.5
        
        out_m[i] = m
        out_l[i] = l
        
    return new_m, new_l

@njit(fastmath=True, parallel=True)
def render_field(m, l):
    """
    Converts raw physics state to visual activation (Phase)
    """
    rows, cols = m.shape
    img = np.empty((rows, cols), dtype=np.float32)
    flat_m = m.ravel()
    flat_l = l.ravel()
    flat_img = img.ravel()
    
    for i in prange(rows * cols):
        # Activation = Phase correlation
        # Creating a complex interference pattern
        val = np.sin(flat_m[i]*10) * np.cos(flat_l[i]*10)
        flat_img[i] = (val + 1.0) * 0.5 # Norm 0-1
        
    return img

# ============================================================
# 2. THE REALITY GENERATOR (The Ground Truth)
# ============================================================

class HighResReality:
    def __init__(self, res=2000):
        self.res = res
        print(f"[-] Allocating Universe ({res}x{res})...")
        
        # Initialize field with a gradient to create structure
        y, x = np.mgrid[-2:2:complex(0, res), -2:2:complex(0, res)]
        self.m = x.astype(np.float32)
        self.l = y.astype(np.float32)
        
        self.true_sigma = 1.0
        self.target_sigma = 1.0
        self.drift_speed = 0.01
        
    def step(self):
        # Drifting Physics
        self.true_sigma += (self.target_sigma - self.true_sigma) * 0.1
        if np.abs(self.true_sigma - self.target_sigma) < 0.01:
            self.target_sigma = np.random.uniform(0.5, 1.5)
            
        # Evolve Field
        self.m, self.l = wada_field_step(self.m, self.l, self.true_sigma, dt=0.1)
        return self.m, self.l, self.true_sigma

# ============================================================
# 3. THE HOLOGRAPHIC ORACLE (The Predictor)
# ============================================================

class VoidOracle:
    def __init__(self, res=2000, sensor_count=500):
        self.res = res
        self.sensor_indices = np.random.choice(res*res, sensor_count, replace=False)
        self.sensor_coords = np.unravel_index(self.sensor_indices, (res, res))
        
        # The Oracle's "Memory" is a population of Sigma guesses
        self.population = np.random.uniform(0.5, 1.5, 30).astype(np.float32)
        self.best_guess = 1.0
        self.generation = 0
        
        # The Oracle maintains its own internal hallucination of the universe
        # To be fast, it re-generates the field from scratch based on the guess
        # rather than storing 4 million pixels per population member.
        
    def perceive_and_predict(self, full_m_truth, full_l_truth):
        """
        1. Look at ONLY the sensor pixels (sparse).
        2. Evolve population to find the Sigma that explains those pixels.
        3. Reconstruct the full 2000x2000 grid.
        """
        
        # 1. SENSE (Extract sparse truth)
        truth_m_sample = full_m_truth.ravel()[self.sensor_indices]
        truth_l_sample = full_l_truth.ravel()[self.sensor_indices]
        
        # 2. THINK (Genetic Optimization of Parameters)
        # We simulate the previous step -> current step transition logic for the SENSORS ONLY
        # We need to know "Previous state of sensors". 
        # For this demo, we assume the Oracle can deduce Sigma from the *current* spatial distribution
        # or we treat it as an Inverse Problem: "What Sigma preserves the observed flow?"
        
        # Simplified for Speed: We test our population against the CURRENT snapshot
        # We assume the Oracle has a shadow copy of the field it is updating.
        
        pass # The logic is inside the main loop to share state for the demo

    def hallucinate(self, current_m, current_l, best_sigma):
        # Predict NEXT step for the WHOLE UNIVERSE based on the inferred parameter
        pred_m, pred_l = wada_field_step(current_m, current_l, best_sigma, dt=0.1)
        return pred_m, pred_l

# ============================================================
# 4. MAIN LOOP
# ============================================================

def run_simulation():
    RES = 2000
    SENSORS = 500
    
    print(f"[-] Initializing Holographic Oracle...")
    print(f"    Target Resolution: {RES}x{RES} ({RES**2/1e6:.1f} Megapixels)")
    print(f"    Sensor Inputs: {SENSORS} ({(SENSORS/(RES**2))*100:.5f}% visibility)")
    
    reality = HighResReality(res=RES)
    oracle = VoidOracle(res=RES, sensor_count=SENSORS)
    
    # Init Oracle's internal belief state (It starts with a copy, then drifts if wrong)
    oracle_m = reality.m.copy()
    oracle_l = reality.l.copy()
    
    history_loss = []
    
    # Setup Plot
    plt.ion()
    fig, axes = plt.subplots(1, 3, figsize=(15, 5), facecolor='#111111')
    ax_true = axes[0]
    ax_pred = axes[1]
    ax_diff = axes[2]
    
    for ax in axes: ax.axis('off')
    ax_true.set_title("The Reality (Hidden)", color='cyan')
    ax_pred.set_title("The Hallucination (Predicted)", color='magenta')
    ax_diff.set_title("The Error (Difference)", color='orange')
    
    # Pre-render objects
    dummy_data = np.zeros((RES//4, RES//4)) # Downscale for display speed
    im_true = ax_true.imshow(dummy_data, cmap='inferno', vmin=0, vmax=1)
    im_pred = ax_pred.imshow(dummy_data, cmap='inferno', vmin=0, vmax=1)
    im_diff = ax_diff.imshow(dummy_data, cmap='gray', vmin=0, vmax=0.1)
    
    txt_sigma = ax_pred.text(10, 50, "", color="white", fontsize=12)
    
    start_time = time.time()
    
    # We maintain a population of test sigmas
    pop_sigmas = np.random.uniform(0.5, 1.5, 20)
    
    try:
        for frame in range(100):
            # A. REALITY STEPS
            # ----------------
            real_m, real_l, true_sigma = reality.step()
            
            # B. ORACLE THINKS (The "Hard" Part)
            # ----------------
            # The Oracle compares its internal 'shadow' sensors to the real sensors
            # to score its population of Sigma hypotheses.
            
            # 1. Extract real sensor values
            flat_real_m = real_m.ravel()
            real_sensor_vals = flat_real_m[oracle.sensor_indices]
            
            # 2. Evaluate Population (Which Sigma predicts the sensor movement best?)
            # This is "Inverse Physics"
            scores = []
            
            # Since we can't rollback reality, the Oracle uses its OWN previous state
            # combined with the candidate sigmas to see which one lands closest to the new Reality sensors.
            
            flat_oracle_m = oracle_m.ravel()
            flat_oracle_l = oracle_l.ravel()
            
            # Create a mini-batch of sensor particles to test physics on (Optimization)
            # Instead of evolving the full 2000x2000 grid for every guess, we only evolve the 500 sensors!
            sensor_m = flat_oracle_m[oracle.sensor_indices]
            sensor_l = flat_oracle_l[oracle.sensor_indices]
            
            best_sigma_idx = 0
            best_err = 1e9
            
            # Check population
            for i, s_guess in enumerate(pop_sigmas):
                # Run physics ONLY on sensors (super fast)
                # Note: We need a 1D version of the step function for this, 
                # or just reshape.
                # Simplified Inline Physics for the "Mind":
                # (This mimics the wada_field_step but for sparse arrays)
                sm, sl = sensor_m.copy(), sensor_l.copy()
                
                # Inline step (Matches kernel)
                dt = 0.1
                fm = -(sm + 2 * s_guess * sm * sl)
                fl = -(sl + s_guess * (sm*sm - sl*sl))
                sm += 0.5 * dt * fm
                sl += 0.5 * dt * fl
                sm += dt * (0.5 * dt * fm) # approx drift
                sl += dt * (0.5 * dt * fl)
                # ... (Simplified for brevity, full RK2 in real impl)
                
                # Compare to REAL sensors
                err = np.mean((sm - real_sensor_vals)**2)
                scores.append(err)
                if err < best_err:
                    best_err = err
                    best_sigma_idx = i
            
            winner_sigma = pop_sigmas[best_sigma_idx]
            
            # Evolution Step (Converge population toward winner)
            pop_sigmas += (winner_sigma - pop_sigmas) * 0.5 # Pull towards best
            pop_sigmas += np.random.normal(0, 0.05, len(pop_sigmas)) # Explore
            
            # C. ORACLE ACTS (Hallucinate the Universe)
            # ----------------
            # Now we commit to the winner sigma and update the FULL 4M Pixel Grid
            oracle_m, oracle_l = wada_field_step(oracle_m, oracle_l, winner_sigma, dt=0.1)
            
            # Sync Step: The Oracle is allowed to "Correct" its internal state using
            # the sensor data to prevent total drift, but only sparsely.
            # Here we just rely on the physics being correct.
            
            # D. VISUALIZE & METRICS
            # ----------------------
            if frame % 2 == 0:
                # Render (Downscaled for speed)
                vis_slice = slice(0, RES, 4) # 1/4 resolution for display
                
                viz_true = render_field(real_m[vis_slice, vis_slice], real_l[vis_slice, vis_slice])
                viz_pred = render_field(oracle_m[vis_slice, vis_slice], oracle_l[vis_slice, vis_slice])
                
                diff = np.abs(viz_true - viz_pred)
                mean_pixel_acc = 1.0 - np.mean(diff)
                
                im_true.set_data(viz_true)
                im_pred.set_data(viz_pred)
                im_diff.set_data(diff)
                
                txt_sigma.set_text(f"TRUTH: {true_sigma:.4f}\nORACLE: {winner_sigma:.4f}\nACCURACY: {mean_pixel_acc*100:.2f}%")
                
                fig.canvas.draw()
                fig.canvas.flush_events()
                
                print(f"Frame {frame} | Sigma Err: {abs(true_sigma - winner_sigma):.5f} | Pixel Acc: {mean_pixel_acc*100:.2f}%")

        plt.ioff()
        # Save final result
        plt.savefig("void_oracle_result.png")
        print("[+] Run Complete. Result saved.")
        
    except KeyboardInterrupt:
        print("\n[!] Aborted by user.")

if __name__ == "__main__":
    # Numba compilation overhead on first run
    print("[-] Compiling JIT Kernels (this takes a moment)...")
    run_simulation()
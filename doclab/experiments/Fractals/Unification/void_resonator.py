import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from scipy.spatial.distance import euclidean

# ============================================================
# 1. THE VOID (The Hidden Source of Chaos)
# ============================================================

class HiddenWadaSource:
    """
    The 'Real World' generator. 
    It runs a Wada simulation with specific parameters that the agent
    must discover purely by observing the output trajectory.
    """
    def __init__(self, seed=42):
        self.rng = np.random.default_rng(seed)
        # Hidden Parameters (The "Truth" we want to find)
        self.true_sigma = 1.15  # Non-standard coupling
        self.true_mass = 0.8    # Hidden mass var
        self.true_dt = 0.1
        
        # Initial State
        self.m = 0.1
        self.l = 0.1
        self.pm = 0.0
        self.pl = 0.0

    def step(self):
        # Wada Physics (Hidden from the learner)
        # 1st half kick
        fm = -(self.m + 2 * self.true_sigma * self.m * self.l)
        fl = -(self.l + self.true_sigma * (self.m**2 - self.l**2))
        
        self.pm += 0.5 * self.true_dt * fm
        self.pl += 0.5 * self.true_dt * fl
        
        # Drift
        self.m += self.true_dt * self.pm
        self.l += self.true_dt * self.pl
        
        # 2nd half kick
        fm2 = -(self.m + 2 * self.true_sigma * self.m * self.l)
        fl2 = -(self.l + self.true_sigma * (self.m**2 - self.l**2))
        
        self.pm += 0.5 * self.true_dt * fm2
        self.pl += 0.5 * self.true_dt * fl2
        
        # Containment (The Void keeps it bouncing)
        if self.m**2 + self.l**2 > 16.0:
            # Soft reset to keep the stream going, mimicking a "pulsar"
            self.m *= 0.1
            self.l *= 0.1
            self.pm *= -0.5
            self.pl *= -0.5
            return np.array([self.m, self.l]), True # Escaped/Reset
            
        return np.array([self.m, self.l]), False

# ============================================================
# 2. THE RESONATOR (The Structure Seeker)
# ============================================================

@dataclass
class ResonanceGene:
    sigma: float
    mass_proxy: float
    coupling: float # How strongly we force our internal state to match observation
    
class VoidResonator:
    """
    A population of 'hypothesis' orbits.
    They watch the 'True' stream and try to sync with it.
    """
    def __init__(self, pop_size=50):
        self.pop_size = pop_size
        self.genes = [self._random_gene() for _ in range(pop_size)]
        
        # Internal states for each gene
        self.states = np.zeros((pop_size, 4)) # m, l, pm, pl
        self.errors = np.zeros(pop_size)
        
    def _random_gene(self):
        return ResonanceGene(
            sigma=np.random.uniform(0.5, 2.0),
            mass_proxy=np.random.uniform(0.5, 1.5),
            coupling=np.random.uniform(0.01, 0.5)
        )

    def initialize_states(self, start_obs):
        # We start our internal models at the observed location
        # but with random momentum (since we can't see momentum)
        for i in range(self.pop_size):
            self.states[i, 0] = start_obs[0]
            self.states[i, 1] = start_obs[1]
            self.states[i, 2] = np.random.normal(0, 0.5)
            self.states[i, 3] = np.random.normal(0, 0.5)

    def predict_and_sync(self, current_obs, dt=0.1):
        """
        1. Predict next step based on internal model.
        2. Calculate Surprisal (Error).
        3. Nudge internal state toward reality (Synchronization).
        """
        predictions = np.zeros((self.pop_size, 2))
        batch_errors = []

        for i in range(self.pop_size):
            g = self.genes[i]
            m, l, pm, pl = self.states[i]
            
            # --- INTERNAL PHYSICS MODEL (Hypothesis) ---
            # We try to replicate the physics we *think* creates the void
            sigma = g.sigma
            
            # Step physics
            fm = -(m + 2 * sigma * m * l)
            fl = -(l + sigma * (m**2 - l**2))
            pm += 0.5 * dt * fm
            pl += 0.5 * dt * fl
            m += dt * pm
            l += dt * pl
            fm2 = -(m + 2 * sigma * m * l)
            fl2 = -(l + sigma * (m**2 - l**2))
            pm += 0.5 * dt * fm2
            pl += 0.5 * dt * fl2
            
            # PREDICTION
            pred_pos = np.array([m, l])
            predictions[i] = pred_pos
            
            # OBSERVE REALITY & CALCULATE SURPRISAL
            # Surprisal = Euclidean distance between Prediction and Reality
            error = np.linalg.norm(pred_pos - current_obs)
            batch_errors.append(error)
            
            # CHAOS CONTROL / SYNCHRONIZATION
            # We "nudge" our internal state towards the observed state
            # The strength of this nudge is the 'coupling' gene.
            # If coupling is correct, we lock on. If too high, we overfit noise.
            m += g.coupling * (current_obs[0] - m)
            l += g.coupling * (current_obs[1] - l)
            
            self.states[i] = [m, l, pm, pl]
            
        return np.array(batch_errors), predictions

    def evolve(self):
        # Genetic Algorithm to favor genes that minimize Surprisal
        # The "Reward" is purely negative entropy.
        
        # Sort by accumulated error (lower is better)
        sorted_indices = np.argsort(self.errors)
        best_indices = sorted_indices[:10] # Top 10 elites
        
        new_genes = []
        for idx in best_indices:
            new_genes.append(self.genes[idx]) # Keep elites
            
        # Breed/Mutate
        while len(new_genes) < self.pop_size:
            parent = self.genes[np.random.choice(best_indices)]
            child = ResonanceGene(
                sigma = parent.sigma + np.random.normal(0, 0.05),
                mass_proxy = parent.mass_proxy + np.random.normal(0, 0.05),
                coupling = np.clip(parent.coupling + np.random.normal(0, 0.01), 0.0, 1.0)
            )
            new_genes.append(child)
            
        self.genes = new_genes
        self.errors = np.zeros(self.pop_size) # Reset error accumulators for next batch

# ============================================================
# 3. THE EXPERIMENT: STRUCTURE IN THE VOID
# ============================================================

def run_experiment():
    print("[-] Opening The Void (Hidden Source)...")
    source = HiddenWadaSource()
    resonator = VoidResonator(pop_size=100)
    
    # Warmup
    start_obs, _ = source.step()
    resonator.initialize_states(start_obs)
    
    history_true = []
    history_pred = []
    surprisal_log = []
    best_gene_log = []
    
    T_STEPS = 1000
    EVOLVE_INTERVAL = 50
    
    print(f"[-] Streaming {T_STEPS} ticks of chaos...")
    
    for t in range(T_STEPS):
        # 1. The Void Moves
        obs, reset = source.step()
        if reset:
            # If void resets, we re-align slightly but keep memory
            pass

        # 2. The Resonator Guesses
        step_errors, predictions = resonator.predict_and_sync(obs)
        
        # 3. Accumulate "Pain" (Surprisal)
        resonator.errors += step_errors
        
        # Log best predictor of this frame
        best_idx = np.argmin(step_errors)
        history_true.append(obs)
        history_pred.append(predictions[best_idx])
        surprisal_log.append(step_errors[best_idx])
        
        # 4. Evolution (The Brain Rewires)
        if t % EVOLVE_INTERVAL == 0 and t > 0:
            resonator.evolve()
            best_gene = resonator.genes[0]
            best_gene_log.append(best_gene.sigma)
            # print(f"    T={t} | Min Surprisal: {step_errors[best_idx]:.5f} | Best Sigma Est: {best_gene.sigma:.3f}")

    # ==========================================
    # VISUALIZATION
    # ==========================================
    history_true = np.array(history_true)
    history_pred = np.array(history_pred)
    surprisal_log = np.array(surprisal_log)
    
    fig = plt.figure(figsize=(12, 10), facecolor='#0f0f0f')
    gs = fig.add_gridspec(3, 2)
    
    # Plot A: Phase Space Synchronization
    ax_phase = fig.add_subplot(gs[0:2, 0])
    ax_phase.set_facecolor('#000000')
    ax_phase.plot(history_true[:, 0], history_true[:, 1], 'c-', lw=1.5, alpha=0.6, label='The Void (Truth)')
    ax_phase.plot(history_pred[:, 0], history_pred[:, 1], 'm--', lw=1, alpha=0.5, label='The Resonator (Model)')
    ax_phase.set_title("Phase Space Shadowing", color='white')
    ax_phase.legend(facecolor='#222', labelcolor='white')
    ax_phase.axis('off')
    
    # Plot B: The Collapse of Surprisal (Entropy)
    ax_err = fig.add_subplot(gs[0, 1])
    ax_err.set_facecolor('#111111')
    ax_err.plot(surprisal_log, color='orange', lw=0.8)
    ax_err.set_yscale('log')
    ax_err.set_title("Surprisal (Prediction Error)", color='white')
    ax_err.grid(color='#333', linestyle=':')
    ax_err.tick_params(colors='white')
    
    # Plot C: Parameter Discovery (Finding the Structure)
    ax_param = fig.add_subplot(gs[1, 1])
    ax_param.set_facecolor('#111111')
    ax_param.plot(np.arange(len(best_gene_log)) * EVOLVE_INTERVAL, best_gene_log, 'g-o', markersize=4)
    ax_param.axhline(source.true_sigma, color='cyan', linestyle='--', label='Hidden Truth')
    ax_param.set_title("Decoding Hidden Variables (Sigma)", color='white')
    ax_param.legend(facecolor='#222', labelcolor='white')
    ax_param.grid(color='#333', linestyle=':')
    ax_param.tick_params(colors='white')
    
    # Plot D: The Moment of Clarity (Zoom on sync)
    ax_zoom = fig.add_subplot(gs[2, :])
    ax_zoom.set_facecolor('#111111')
    limit = 200
    ax_zoom.plot(history_true[-limit:, 0], color='cyan', lw=2, label='True Signal')
    ax_zoom.plot(history_pred[-limit:, 0], color='magenta', linestyle='--', lw=2, label='Predicted Signal')
    ax_zoom.set_title(f"The Moment of Clarity (Last {limit} ticks)", color='white')
    ax_zoom.legend(facecolor='#222', labelcolor='white')
    ax_zoom.grid(color='#333', linestyle=':')
    ax_zoom.tick_params(colors='white')
    
    plt.tight_layout()
    plt.savefig('void_structure_prediction.png')
    print("[+] Structure Decoded. Image saved to 'void_structure_prediction.png'")

if __name__ == "__main__":
    run_experiment()
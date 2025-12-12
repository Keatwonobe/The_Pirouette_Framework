import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass

# ============================================================
# 1. THE DRIFTING VOID (The Moving Target)
# ============================================================

class DriftingVoidSource:
    def __init__(self, seed=42):
        self.rng = np.random.default_rng(seed)
        
        # The Truth is no longer static. It moves.
        self.true_sigma = 1.0 # Starting at standard Wada
        self.drift_velocity = 0.0005 # How fast the laws of physics change
        self.drift_direction = 1.0
        
        # State
        self.m = 0.5 # Start in a more chaotic region
        self.l = 0.5
        self.pm = 0.0
        self.pl = 0.0
        self.dt = 0.1

    def step(self):
        # 1. Mutate the Laws of Physics (Drift)
        self.true_sigma += self.drift_velocity * self.drift_direction
        if self.true_sigma > 1.4 or self.true_sigma < 0.6:
            self.drift_direction *= -1 # Bounce the parameter bounds
            
        # 2. Run Physics
        s = self.true_sigma
        try:
            # Half kick
            fm = -(self.m + 2*s*self.m*self.l)
            fl = -(self.l + s*(self.m**2 - self.l**2))
            self.pm += 0.5 * self.dt * fm
            self.pl += 0.5 * self.dt * fl
            
            # Drift
            self.m += self.dt * self.pm
            self.l += self.dt * self.pl
            
            # Half kick
            fm = -(self.m + 2*s*self.m*self.l)
            fl = -(self.l + s*(self.m**2 - self.l**2))
            self.pm += 0.5 * self.dt * fm
            self.pl += 0.5 * self.dt * fl
            
            # Soft Boundary (Pulsar reset)
            if self.m**2 + self.l**2 > 9.0:
                self.m *= 0.5; self.l *= 0.5
                self.pm *= -0.5; self.pl *= -0.5
                return np.array([self.m, self.l]), True
                
        except (RuntimeError, OverflowError):
            # If the Void itself crashes (rare), hard reset
            self.m, self.l = 0.1, 0.1
            return np.array([0.1, 0.1]), True
            
        return np.array([self.m, self.l]), False

# ============================================================
# 2. THE ADAPTIVE RESONATOR (The Hunter)
# ============================================================

@dataclass
class ResonanceGene:
    sigma: float
    coupling: float

class AdaptiveResonator:
    def __init__(self, pop_size=60):
        self.pop_size = pop_size
        self.genes = [self._random_gene() for _ in range(pop_size)]
        self.states = np.zeros((pop_size, 4)) # m, l, pm, pl
        self.errors = np.zeros(pop_size)
        
    def _random_gene(self):
        # Start with a wide spread of guesses
        return ResonanceGene(
            sigma=np.random.uniform(0.5, 1.5),
            coupling=np.random.uniform(0.1, 0.4)
        )

    def initialize_states(self, obs):
        for i in range(self.pop_size):
            self.states[i] = [obs[0], obs[1], 0, 0]

    def predict_and_sync(self, obs, dt=0.1):
        predictions = np.zeros((self.pop_size, 2))
        step_errors = np.zeros(self.pop_size)

        for i in range(self.pop_size):
            g = self.genes[i]
            m, l, pm, pl = self.states[i]
            
            # Safety wrapper to prevent the "Explosions" from crashing the script
            # We treat Infinity as "High Error"
            try:
                # Physics Step
                fm = -(m + 2*g.sigma*m*l)
                fl = -(l + g.sigma*(m**2 - l**2))
                pm += 0.5 * dt * fm
                pl += 0.5 * dt * fl
                m += dt * pm
                l += dt * pl
                fm2 = -(m + 2*g.sigma*m*l)
                fl2 = -(l + g.sigma*(m**2 - l**2))
                pm += 0.5 * dt * fm2
                pl += 0.5 * dt * fl2
                
                # Check for stability
                if np.isnan(m) or np.isinf(m) or (m*m+l*l > 100):
                    raise OverflowError
                
                # Prediction
                predictions[i] = [m, l]
                
                # Error Calculation
                dist = np.sqrt((m - obs[0])**2 + (l - obs[1])**2)
                step_errors[i] = dist
                
                # Synchronization (Nudge)
                m += g.coupling * (obs[0] - m)
                l += g.coupling * (obs[1] - l)
                self.states[i] = [m, l, pm, pl]

            except (OverflowError, RuntimeWarning):
                # If this gene's physics are impossible, it dies (High Error)
                step_errors[i] = 100.0
                predictions[i] = [0, 0]
                self.states[i] = [obs[0], obs[1], 0, 0] # Reset state
                
        return step_errors, predictions

    def evolve(self):
        # Survival of the fittest
        sorted_indices = np.argsort(self.errors)
        best_indices = sorted_indices[:15] # Keep top 15
        
        new_genes = []
        # Elitism
        for idx in best_indices:
            new_genes.append(self.genes[idx])
            
        # Reproduction with Mutation
        while len(new_genes) < self.pop_size:
            parent = self.genes[np.random.choice(best_indices)]
            # We add a "High Mutation Rate" because the target is moving!
            child = ResonanceGene(
                sigma = parent.sigma + np.random.normal(0, 0.08), 
                coupling = np.clip(parent.coupling + np.random.normal(0, 0.02), 0.05, 0.9)
            )
            new_genes.append(child)
            
        self.genes = new_genes
        self.errors = np.zeros(self.pop_size) # Flush errors

# ============================================================
# 3. EXECUTION: CHASING THE SIGNAL
# ============================================================

def run_drift_experiment():
    print("[-] Opening Drifting Void...")
    source = DriftingVoidSource()
    resonator = AdaptiveResonator(pop_size=80)
    
    # Init
    obs, _ = source.step()
    resonator.initialize_states(obs)
    
    history_sigma_true = []
    history_sigma_est = []
    
    T_STEPS = 1200
    EVOLVE_FREQ = 20 # Evolve faster to catch the drift
    
    print(f"[-] Tracking variable physics for {T_STEPS} ticks...")
    
    for t in range(T_STEPS):
        obs, _ = source.step()
        
        step_errs, _ = resonator.predict_and_sync(obs)
        resonator.errors += step_errs
        
        if t % EVOLVE_FREQ == 0:
            best_gene_idx = np.argmin(resonator.errors)
            est_sigma = resonator.genes[best_gene_idx].sigma
            
            history_sigma_true.append(source.true_sigma)
            history_sigma_est.append(est_sigma)
            
            resonator.evolve()
            
            if t % 200 == 0:
                print(f"    T={t:<4} | True Sigma: {source.true_sigma:.3f} | Est Sigma: {est_sigma:.3f}")

    # Plotting
    plt.figure(figsize=(10, 6), facecolor='#111111')
    ax = plt.gca()
    ax.set_facecolor('#000000')
    
    steps = np.arange(len(history_sigma_true)) * EVOLVE_FREQ
    
    plt.plot(steps, history_sigma_true, 'c--', linewidth=2, label="The Void (Drifting Truth)")
    plt.plot(steps, history_sigma_est, 'g-o', linewidth=1.5, markersize=4, alpha=0.8, label="The Resonator (Tracker)")
    
    plt.title("Resonator Adapting to Changing Laws of Physics", color='white', fontsize=14)
    plt.xlabel("Time Steps", color='gray')
    plt.ylabel("Sigma (Coupling Constant)", color='gray')
    plt.grid(color='#333', linestyle=':')
    plt.legend(facecolor='#222', labelcolor='white')
    plt.tick_params(colors='gray')
    
    plt.tight_layout()
    plt.savefig('void_drifter.png')
    print("[+] Drift Analysis Complete. Saved to 'void_drifter.png'")

if __name__ == "__main__":
    run_drift_experiment()
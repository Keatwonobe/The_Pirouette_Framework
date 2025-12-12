import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import Tuple, Dict, Any, List, Optional

# ============================================================
# 1. Core Physics & Metrics (Shared)
# ============================================================

def step_prism(m: float, l: float, pm: float, pl: float, dt: float, sigma: float = 1.0):
    # First force evaluation
    fm = -(m + 2 * sigma * m * l)
    fl = -(l + sigma * (m * m - l * l))
    force_mag = np.sqrt(fm * fm + fl * fl)
    step_stress = force_mag * dt

    # Half kick momenta
    pm += 0.5 * dt * fm
    pl += 0.5 * dt * fl

    # Drift positions
    m += dt * pm
    l += dt * pl

    # Second force evaluation
    fm2 = -(m + 2 * sigma * m * l)
    fl2 = -(l + sigma * (m * m - l * l))

    # Half kick again
    pm += 0.5 * dt * fm2
    pl += 0.5 * dt * fl2

    return m, l, pm, pl, step_stress

@dataclass
class OrbitMetrics:
    m_traj: np.ndarray
    l_traj: np.ndarray
    lifetime: float
    escaped: bool
    path_length: float
    stress: float
    efficiency: float
    frustration: float
    score: float

def compute_positive_frustration(m_traj: np.ndarray, l_traj: np.ndarray, dt: float) -> float:
    if len(m_traj) < 5: return 0.0
    r = np.sqrt(m_traj**2 + l_traj**2)
    theta = np.arctan2(l_traj, m_traj)
    
    # 1. Radial Breathing
    r_std = np.std(r)
    r_mean = np.mean(r) + 1e-8
    radial_breath = r_std / r_mean
    
    # 2. Curvature
    d2r = np.diff(np.diff(r))
    curv = np.mean(np.abs(d2r)) / (dt * dt + 1e-8)
    curv_norm = curv / (10.0 + curv)
    
    # 3. Angular Span
    theta_un = np.unwrap(theta)
    theta_span = np.max(theta_un) - np.min(theta_un)
    theta_norm = min(np.fmod(theta_span, 2*np.pi), np.pi) / np.pi
    
    rb_norm = radial_breath / (1.0 + radial_breath)
    return float(rb_norm * curv_norm * theta_norm)

def integrate_orbit(m0, l0, pm0, pl0, t_max, dt, escape_r2, 
                    w_life, w_eff, w_frus) -> OrbitMetrics:
    steps = int(t_max / dt)
    m, l, pm, pl = m0, l0, pm0, pl0
    
    m_hist = np.zeros(steps + 1, dtype=np.float32)
    l_hist = np.zeros(steps + 1, dtype=np.float32)
    m_hist[0], l_hist[0] = m, l
    
    stress = 0.0
    path_length = 0.0
    escaped = False
    t_alive = 0.0
    
    for k in range(1, steps + 1):
        m_prev, l_prev = m, l
        m, l, pm, pl, s_stress = step_prism(m, l, pm, pl, dt)
        
        m_hist[k], l_hist[k] = m, l
        stress += s_stress
        path_length += np.sqrt((m - m_prev)**2 + (l - l_prev)**2)
        t_alive += dt
        
        if m*m + l*l > escape_r2:
            escaped = True
            # Trim
            m_hist = m_hist[:k+1]
            l_hist = l_hist[:k+1]
            break
            
    # Metrics
    eff = path_length / (stress + 1e-8)
    life_fac = t_alive / t_max
    frust = compute_positive_frustration(m_hist, l_hist, dt)
    
    score = (w_life * life_fac) + (w_eff * eff) + (w_frus * frust)
    
    return OrbitMetrics(m_hist, l_hist, t_alive, escaped, path_length, stress, eff, frust, score)

# ============================================================
# 2. Chaos Frequency Discovery
# ============================================================

def discover_frequency_bands(n_samples=500, t_limit=50.0) -> np.ndarray:
    """
    Monte Carlo sampling of the basin to find the natural 'chaos frequencies' (1/T_escape).
    This replaces running the full high-res mapper.
    """
    print(f"Scanning basin for chaos frequencies ({n_samples} samples)...")
    rng = np.random.default_rng(42)
    freqs = []
    
    for _ in range(n_samples):
        # Sample broad disk
        r = rng.uniform(0, 2.0)
        th = rng.uniform(0, 2*np.pi)
        m, l = r*np.cos(th), r*np.sin(th)
        pm, pl = rng.normal(0, 0.5, 2)
        
        # Fast integration to check escape time
        # Simplified loop for speed
        t_esc = t_limit
        for step in range(int(t_limit/0.1)):
            m, l, pm, pl, _ = step_prism(m, l, pm, pl, 0.1)
            if m*m + l*l > 16.0:
                t_esc = step * 0.1
                break
        
        # F = 1 / T
        if t_esc > 0:
            freqs.append(1.0 / t_esc)
            
    freqs = np.array(freqs)
    # Filter out "instant" escapes (very high freq) and "stable" (low freq) to find the interesting bands
    valid_freqs = freqs[(freqs > 1.0/t_limit) & (freqs < 2.0)] 
    
    if len(valid_freqs) < 10:
        return np.array([0.05, 0.1, 0.2, 0.4]) # Fallback
        
    # Create 5 bands from quantiles
    qs = np.linspace(0.1, 0.9, 6) # 5 intervals
    bands = []
    for i in range(5):
        lo, hi = np.quantile(valid_freqs, qs[i]), np.quantile(valid_freqs, qs[i+1])
        bands.append((lo + hi) / 2)
        
    return np.array(bands)

# ============================================================
# 3. The Bandit
# ============================================================

class ChaosFrequencyBandit:
    def __init__(self, freq_bands, epsilon=0.3):
        self.freq_bands = np.array(freq_bands, dtype=np.float32)
        self.epsilon = epsilon
        self.counts = np.zeros(len(freq_bands), dtype=np.int32)
        self.mean_reward = np.zeros(len(freq_bands), dtype=np.float32)
        self.history = []

    def select_band(self):
        # Explore if no data or epsilon roll
        if np.random.rand() < self.epsilon or self.counts.sum() == 0:
            idx = np.random.randint(len(self.freq_bands))
            was_explore = True
        else:
            idx = np.argmax(self.mean_reward)
            was_explore = False
        return idx, self.freq_bands[idx], was_explore

    def update(self, idx, reward):
        self.counts[idx] += 1
        n = self.counts[idx]
        old_mean = self.mean_reward[idx]
        self.mean_reward[idx] += (reward - self.mean_reward[idx]) / n
        self.history.append({'idx': idx, 'freq': self.freq_bands[idx], 'reward': reward})

# ============================================================
# 4. Modulated Learner
# ============================================================

@dataclass
class Genome:
    m0: float; l0: float; pm0: float; pl0: float
    metrics: OrbitMetrics = None

class ModulatedLearner:
    def __init__(self, pop_size=50):
        self.pop_size = pop_size
        self.rng = np.random.default_rng(101)
        self.pop = [self._random_genome() for _ in range(pop_size)]
        self.best_global_score = -float('inf')
        self.best_genome = None
        
    def _random_genome(self):
        r = self.rng.uniform(0, 2.0)
        th = self.rng.uniform(0, 2*np.pi)
        return Genome(r*np.cos(th), r*np.sin(th), 
                      self.rng.normal(0,0.5), self.rng.normal(0,0.5))
        
    def _mutate(self, g: Genome, scale=0.1):
        # Mutation logic
        return Genome(
            g.m0 + self.rng.normal(0, scale),
            g.l0 + self.rng.normal(0, scale),
            g.pm0 + self.rng.normal(0, scale*0.5),
            g.pl0 + self.rng.normal(0, scale*0.5)
        )

    def run_one_generation(self, F_c: float) -> float:
        """
        Run one generation using physics tuned to chaos frequency F_c.
        Returns: Improvement in best score (reward).
        """
        # 1. Modulate Physics/Scoring based on Chaos Frequency
        # Higher freq = faster escape typical = shorter t_max needed to see interesting stuff
        # Higher freq = we want to reward surviving HIGH chaos, so increase frustration weight
        
        # Base settings
        base_t_max = 80.0
        
        # Dynamic settings
        # If F_c is high (e.g. 0.5 -> T=2s), we don't need T=80s.
        # But we want to encourage long life relative to the chaos.
        # Let's say t_max is scaled inversely but with a floor.
        t_max = max(20.0, min(100.0, 5.0 / (F_c + 0.01))) 
        
        # Frustration weight modulation
        # High chaos freq -> high frustration weight (reward riding the lightning)
        w_frus = 1.0 + (F_c * 4.0) 
        
        # Evaluate Population
        current_best_score = -float('inf')
        
        for g in self.pop:
            # We must re-evaluate everyone because the scoring function (w_frus) changed!
            # The environment has changed "difficulty modes".
            m = integrate_orbit(
                g.m0, g.l0, g.pm0, g.pl0, 
                t_max=t_max, dt=0.05, escape_r2=16.0,
                w_life=1.0, w_eff=0.7, w_frus=w_frus
            )
            g.metrics = m
            if m.score > current_best_score:
                current_best_score = m.score
                
        # Sort
        self.pop.sort(key=lambda x: x.metrics.score, reverse=True)
        best_of_gen = self.pop[0]
        
        # Calculate Reward
        # Since the scoring function changes every step, we can't just compare raw scores 
        # to the previous generation's raw score directly. 
        # Instead, reward is: (Best Score - Average Score) / Standard Deviation
        # This measures "how much better did the elite get relative to the pack under THESE conditions?"
        scores = [p.metrics.score for p in self.pop]
        mu, std = np.mean(scores), np.std(scores) + 1e-6
        reward = (best_of_gen.metrics.score - mu) / std
        
        # Save global best (just for tracking, though metrics aren't perfectly comparable)
        if self.best_genome is None or best_of_gen.metrics.frustration > self.best_genome.metrics.frustration:
             # We bias "Global Best" to the most frustrated survivor we've ever seen
             if not best_of_gen.metrics.escaped:
                 self.best_genome = best_of_gen

        # Evolution (Elitism + Mutation)
        elites = self.pop[:10]
        new_pop = []
        new_pop.extend(elites)
        while len(new_pop) < self.pop_size:
            parent = self.rng.choice(elites)
            child = self._mutate(parent, scale=0.15) # slightly higher mutation
            new_pop.append(child)
        self.pop = new_pop
        
        return reward

# ============================================================
# 5. Main Execution Loop
# ============================================================

if __name__ == "__main__":
    # 1. Discover Bands
    freq_bands = discover_frequency_bands()
    print(f"Discovered Chaos Frequency Bands (Hz): {freq_bands}")
    
    # 2. Init Bandit & Learner
    bandit = ChaosFrequencyBandit(freq_bands, epsilon=0.25)
    learner = ModulatedLearner(pop_size=64)
    
    rewards_history = []
    
    print("\nStarting Meta-Evolution (Bandit-Driven)...")
    print(f"{'Gen':<4} | {'F_c':<6} | {'Reward':<7} | {'MeanR':<6} | {'Best Frust':<10} | {'Mode'}")
    print("-" * 60)
    
    for gen in range(25): # Meta-generations
        # A. Bandit chooses frequency
        idx, F_c, explore = bandit.select_band()
        mode_str = "Explr" if explore else "Exploit"
        
        # B. Learner runs one generation under that frequency
        reward = learner.run_one_generation(F_c)
        
        # C. Update Bandit
        bandit.update(idx, reward)
        rewards_history.append(reward)
        
        # D. Logging
        best_f = learner.best_genome.metrics.frustration if learner.best_genome else 0
        print(f"{gen:<4} | {F_c:<6.3f} | {reward:<7.3f} | {bandit.mean_reward[idx]:<6.2f} | {best_f:<10.3f} | {mode_str}")

    # Plot Bandit Beliefs
    plt.figure(figsize=(10,4))
    plt.bar(range(len(freq_bands)), bandit.mean_reward, tick_label=[f"{f:.2f}" for f in freq_bands])
    plt.xlabel("Chaos Frequency Band (1/T_esc)")
    plt.ylabel("Mean Reward (Score Improvement)")
    plt.title("Bandit Beliefs: Which Chaos Frequencies Teach Best?")
    plt.savefig("wada_bandit_beliefs.png")
    
    # Plot Best Orbit
    if learner.best_genome:
        m = learner.best_genome.metrics
        plt.figure(figsize=(6,6))
        plt.plot(m.m_traj, m.l_traj, 'k-', lw=0.5, alpha=0.8)
        plt.title(f"Bandit-Optimized Orbit\nFrust={m.frustration:.3f}, Score={m.score:.3f}")
        plt.savefig("wada_bandit_orbit.png")
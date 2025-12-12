import gymnasium as gym
import numpy as np
import time
from collections import deque
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("KAPPA_FILTER")

# --- GLOBAL PHYSICS CONSTANTS (from space_fractal.py) ---
TWIST = 3.8
GAMMA = 0.5 

# ============================================================
# 1. THE KAPPA-HYPERFILTER CORE (The Discrete Space Sampler)
# ============================================================

class KappaHyperfilter:
    """
    Synthesizes the output of the four macro-fractal maps (Helicity, Stiffness, Coherence)
    into a single scalar: Kappa-Priority (kP).
    kP dictates solution quality.
    """
    
    def get_fractal_force_vector(self, m, lam):
        # Full Unified Field Laws (from space_fractal.py)
        F_teal_m = -(m + 0.866) 
        F_teal_lam = -(lam - 0.5)

        F_red_m = -(m - 0.0)
        p_violation = TWIST * np.sin(m * 2.5) 
        F_red_lam = -(lam + 1.0) + p_violation

        # Non-linear Confinement (The Squeeze)
        sum_m = (F_teal_m + F_red_m)
        sum_lam = (F_teal_lam + F_red_lam)
        magnitude = np.sqrt(sum_m**2 + sum_lam**2)
        scaling_factor = np.sqrt(magnitude)
        F_gold_m = sum_m * scaling_factor
        F_gold_lam = sum_lam * scaling_factor
        
        # Calculate weights (as in the original)
        angle = np.degrees(np.arctan2(lam, m)) % 360
        diff_g = np.abs(angle - 30); diff_g = np.minimum(diff_g, 360-diff_g)
        w_gold = np.exp(-(diff_g/80)**2)
        diff_t = np.abs(angle - 150); diff_t = np.minimum(diff_t, 360-diff_t)
        w_teal = np.exp(-(diff_t/80)**2)
        diff_r = np.abs(angle - 270); diff_r = np.minimum(diff_r, 360-diff_r)
        w_red = np.exp(-(diff_r/80)**2)
        tot = w_gold + w_teal + w_red + 1e-6
        
        nw_red = w_red / tot
        nw_teal = w_teal / tot
        nw_gold = w_gold / tot
        
        Fm = (nw_teal * F_teal_m + nw_red * F_red_m + nw_gold * F_gold_m)
        Flam = (nw_teal * F_teal_lam + nw_red * F_red_lam + nw_gold * F_gold_lam)
        
        return Fm, Flam, nw_red, nw_teal, nw_gold

    def sample_filters(self, m, lam):
        """
        Calculates local physics properties based on position (m, lam).
        This replaces the lookup from the pre-computed fractal maps.
        """
        # --- 1. Helicity / Tension Proxy ---
        r = np.sqrt(m**2 + lam**2)
        
        # Helicity Proxy: Rotational sensitivity near the origin (where density is highest)
        helicity_proxy = np.abs(m * lam) * np.exp(-0.5 * r)
        
        # --- 2. Vacuum Stiffness Proxy ---
        # Stiffness is proxied by the magnitude of the force itself (approximation of L1 eigenvalue)
        Fm, Flam, nw_red, nw_teal, nw_gold = self.get_fractal_force_vector(m, lam)
        force_mag = np.sqrt(Fm**2 + Flam**2)
        stiffness_proxy = np.log1p(force_mag)
        
        # --- 3. Cosmic Caustic / Coherence Proxy ---
        # Coherence is highest where flow is smooth
        # Use the weighting of the less-chaotic components (Teal/Gold)
        coherence_proxy = (nw_teal + nw_gold) / (nw_red + 1e-6)
        
        # Normalize and combine to Kappa-Priority (kP)
        kP = (
            1.0 * np.tanh(coherence_proxy / 10.0)  # Strong weight for smooth flow
            - 0.5 * np.tanh(stiffness_proxy)      # Penalty for high resistance
            + 0.5 * np.tanh(helicity_proxy * 5.0) # Bonus for sitting in a high-sensitivity, but stable, region
        )
        
        # Recalculate dominant basin for mutation logic
        if nw_teal > nw_red and nw_teal > nw_gold: color = "Teal"
        elif nw_red > nw_teal and nw_red > nw_gold: color = "Red"
        else: color = "Gold"

        return kP, color, stiffness_proxy, helicity_proxy

# ============================================================
# 2. FRACTAL HYPERNET (Weight Generator)
# ============================================================
class FractalHypernet:
    def __init__(self, output_dim):
        self.output_dim = output_dim
        self.filter = KappaHyperfilter()
        
    def generate_weights(self, m, lam):
        weights = []
        curr_m, curr_l = m, lam
        sigma, dt, ESCAPE = 1.0, 0.1, 10.0
        
        # Basin Identity (The "Sand State") is now calculated by the filter
        kP, color, _, _ = self.filter.sample_filters(m, lam)
        
        # This Hénon-Heiles loop serves as the 'DNA' sequence generator
        while len(weights) < self.output_dim:
            if abs(curr_m) > ESCAPE or abs(curr_l) > ESCAPE:
                curr_m = np.fmod(curr_m, 2.0); curr_l = np.fmod(curr_l, 2.0)
            try:
                # Use the Hénon-Heiles potential gradient for sequencing
                grad_m = curr_m + 2 * sigma * curr_m * curr_l
                grad_l = curr_l + sigma * (curr_m**2 - curr_l**2)
                curr_m += dt * grad_m
                curr_l += dt * grad_l
            except: curr_m, curr_l = 0.0, 0.0
            
            # Use Tanh as an activation function for the weights
            weights.append(np.tanh(curr_m)); weights.append(np.tanh(curr_l))
            
        return np.array(weights[:self.output_dim], dtype=np.float32), color, kP

# ============================================================
# 3. DELTA ORBIT AGENT
# ============================================================
class OrbitAgent:
    def __init__(self, env_name, gene):
        self.gene = gene
        dummy = gym.make(env_name)
        self.act_dim = dummy.action_space.shape[0]
        self.obs_dim = dummy.observation_space.shape[0]
        self.hypernet = FractalHypernet(self.obs_dim * self.act_dim)
        dummy.close()

    def get_action_data(self, obs, t_step):
        # Unpack Gene: [Cm, Cl, Rm, Rl, Tilt, Freq, Phase]
        cm, cl, rm, rl, tilt, freq, phase = self.gene
        
        # Orbit in Phase Space
        angle = phase + (t_step * 0.02 * freq * 2 * np.pi)
        cos_a, sin_a = np.cos(angle), np.sin(angle)
        cos_t, sin_t = np.cos(tilt), np.sin(tilt)
        
        m = cm + (rm * cos_a * cos_t - rl * sin_a * sin_t)
        lam = cl + (rm * cos_a * sin_t + rl * sin_a * cos_t)
        
        # Generate weights and get the Kappa-Priority (kP)
        weights, color, kP = self.hypernet.generate_weights(m, lam)
        W = weights.reshape(self.act_dim, self.obs_dim)
        
        # Action is weighted by kP. If kP is low, the action is suppressed (less confident)
        action = np.tanh(W @ obs) * (0.5 + 0.5 * np.tanh(kP)) 
        
        return action, color, kP

# ============================================================
# 4. THE DELTA SCOREKEEPER
# ============================================================
class DeltaScorekeeper:
    def __init__(self, alpha=0.05):
        self.baseline = 0.0
        self.alpha = alpha # Learning rate for the baseline
        
    def get_delta_score(self, raw_score, avg_kP):
        """
        Weighted Delta: (Raw Score - Baseline) * (1 + avg_kP)
        Solutions in high-kP (consistent) regions get an exponential reward boost.
        """
        # Normalize kP slightly for robust scaling
        scaled_kP = np.clip(avg_kP, -1.0, 1.0)
        
        # The Delta: How much better is this than usual?
        delta = raw_score - self.baseline
        
        # Apply the kP filter
        weighted_delta = delta * (1.0 + scaled_kP)
        
        # Update Baseline only with raw score to prevent runaway inflation
        self.baseline = (1 - self.alpha) * self.baseline + self.alpha * raw_score
        
        return weighted_delta, scaled_kP

# ============================================================
# 5. DELTA-KI TRAINER (kP-Aware Evolution)
# ============================================================
class DeltaKiTrainer:
    def __init__(self, env_name, n_heads=6):
        self.env_name = env_name
        self.heads = [{'gene': self.random_gene(), 'scorekeeper': DeltaScorekeeper()} for _ in range(n_heads)]
        self.global_best_dist = 0.0
        self.global_best_gene = None

    def random_gene(self):
        # [Cm, Cl, Rm, Rl, Tilt, Freq, Phase]
        return np.array([
            np.random.normal(0, 0.3), np.random.normal(0, 0.3),
            np.random.uniform(0.5, 1.2), np.random.uniform(0.5, 1.2), # Forced Large Radius
            np.random.uniform(0, np.pi), np.random.uniform(0.5, 1.5),
            np.random.uniform(0, 2*np.pi)
        ])

    def evaluate(self, gene, scorekeeper, render=False):
        agent = OrbitAgent(self.env_name, gene)
        env = gym.make(self.env_name, render_mode="human" if render else None)
        obs, _ = env.reset()
        
        start_x = env.unwrapped.hull.position.x
        max_dist = 0
        basin_counts = {"Gold": 0, "Red": 0, "Teal": 0}
        sum_kP = 0.0
        steps = 0
        
        # --- NEW PENALTY INITIALIZATION ---
        air_penalty = 0.0
        AIR_PENALTY_PER_STEP = 0.05 # A constant cost for being airborne
        
        while steps < 600:
            action, color, kP = agent.get_action_data(obs, steps)
            
            # --- EXTRACT FOOT CONTACT SENSORS ---
            # BipedalWalker observation: [..., hip_speed, knee_speed, contact_L, contact_R]
            # Contact sensors are typically obs[8] and obs[9] in BipedalWalker-v3
            contact_l = obs[8]
            contact_r = obs[9]
            
            # Apply No-Fly Penalty
            if contact_l < 0.1 and contact_r < 0.1:
                air_penalty += AIR_PENALTY_PER_STEP
            
            obs, reward, term, trunc, _ = env.step(action)
            
            # Track Fractal State
            basin_counts[color] += 1
            sum_kP += kP
            
            # Metric: Pure Distance
            curr_x = env.unwrapped.hull.position.x
            dist = curr_x - start_x
            max_dist = max(max_dist, dist)
            
            steps += 1
            if term or trunc: break
        env.close()
        
        avg_kP = sum_kP / steps if steps > 0 else 0.0
        
        # --- FINAL SCORE CALCULATION ---
        # Raw score is distance minus the total penalty for being airborne.
        final_raw_score = max_dist - air_penalty
        
        # Calculate Weighted Delta
        weighted_delta, scaled_kP = scorekeeper.get_delta_score(final_raw_score, avg_kP)
        
        # Determine Dominant Basin
        dominant_basin = max(basin_counts, key=basin_counts.get)
        
        return weighted_delta, final_raw_score, dominant_basin, avg_kP

    def run(self, generations=20):
        logger.info(f"\n{'='*50}")
        logger.info(f"🌊 KAPPA-HYPERFILTER TRAINER: {self.env_name}")
        logger.info("   Reward = (Distance - Baseline) * (1 + avg_kP).")
        logger.info("   Mutation driven by kP consistency.")
        logger.info(f"{'='*50}")
        
        for g in range(generations):
            logger.info(f"\n--- Generation {g} ---")
            
            for i, head in enumerate(self.heads):
                # 1. Evaluate
                weighted_delta, raw_dist, basin, avg_kP = self.evaluate(head['gene'], head['scorekeeper'])
                
                # 2. Check Global Record
                if raw_dist > self.global_best_dist:
                    self.global_best_dist = raw_dist
                    self.global_best_gene = head['gene'].copy()
                    logger.info(f"   🏆 NEW RECORD: {raw_dist:.1f}m (Head {i})")
                
                # 3. Sand/Filter Logic: Adjust Mutation based on kP
                if avg_kP > 0.5:
                    mutation_scale = 0.03 # High Consistency: Fine-tune the current orbit
                    strategy = "Refining (High kP)"
                elif avg_kP > -0.2:
                    mutation_scale = 0.15 # Moderate Consistency: Exploring, but cautiously
                    strategy = "Exploring (Med kP)"
                else: 
                    mutation_scale = 0.30 # Low Consistency: Scramble the orbit parameters
                    strategy = "Scrambling (Low kP)"
                
                # 4. Evolution Step
                if weighted_delta > 0:
                    pass 
                else:
                    pass
                
                # Apply Mutation
                noise = np.random.normal(0, mutation_scale, size=7)
                head['gene'] += noise
                
                # Constraints
                head['gene'][2] = max(0.5, head['gene'][2]) # Radius M
                head['gene'][3] = max(0.5, head['gene'][3]) # Radius L

                logger.info(f"   Head {i}: Dist {raw_dist:.1f}m | $\Delta_\\kappa$ {weighted_delta:+.2f} | Basin: {basin} | Avg $\kappa$P: {avg_kP:.2f} ({strategy})")

            if self.global_best_dist > 50.0:
                logger.info("   > Goal Reached.")
                break
                
        return self.global_best_gene

if __name__ == "__main__":
    try:
        # Note: BipedalWalker-v3 needs gym==0.26.2. 
        trainer = DeltaKiTrainer("BipedalWalker-v3", n_heads=6)
        best_gene = trainer.run(generations=15)
        
        if best_gene is not None:
            logger.info("\nVisualizing the Kappa-Filter Walker (Note: Requires a graphics environment)...")
            dummy_sk = DeltaScorekeeper()
            trainer.evaluate(best_gene, dummy_sk, render=True)
    except Exception as e:
        logger.error(f"Error: {e}")
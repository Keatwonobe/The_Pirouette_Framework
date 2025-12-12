import gymnasium as gym
import numpy as np
import time
from collections import deque
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("KAPPA_FILTER_PER_LIMB")

# --- GLOBAL PHYSICS CONSTANTS (from space_fractal.py) ---
TWIST = 3.8
GAMMA = 0.5 
NUM_PARTICLES = 3 # P1: Body, P2: Left Leg, P3: Right Leg
GENE_LEN = NUM_PARTICLES * 7 # 3 particles * 7 params each

# ============================================================
# 1. THE KAPPA-HYPERFILTER CORE (Unchanged)
# ============================================================

class KappaHyperfilter:
    def get_fractal_force_vector(self, m, lam):
        # Full Unified Field Laws (from space_fractal.py)
        F_teal_m = -(m + 0.866) 
        F_teal_lam = -(lam - 0.5)
        F_red_m = -(m - 0.0)
        p_violation = TWIST * np.sin(m * 2.5) 
        F_red_lam = -(lam + 1.0) + p_violation
        sum_m = (F_teal_m + F_red_m)
        sum_lam = (F_teal_lam + F_red_lam)
        magnitude = np.sqrt(sum_m**2 + sum_lam**2)
        scaling_factor = np.sqrt(magnitude)
        F_gold_m = sum_m * scaling_factor
        F_gold_lam = sum_lam * scaling_factor
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
        r = np.sqrt(m**2 + lam**2)
        helicity_proxy = np.abs(m * lam) * np.exp(-0.5 * r)
        Fm, Flam, nw_red, nw_teal, nw_gold = self.get_fractal_force_vector(m, lam)
        force_mag = np.sqrt(Fm**2 + Flam**2)
        stiffness_proxy = np.log1p(force_mag)
        coherence_proxy = (nw_teal + nw_gold) / (nw_red + 1e-6)
        kP = (1.0 * np.tanh(coherence_proxy / 10.0) - 
              0.5 * np.tanh(stiffness_proxy) + 
              0.5 * np.tanh(helicity_proxy * 5.0))
        
        if nw_teal > nw_red and nw_teal > nw_gold: color = "Teal"
        elif nw_red > nw_teal and nw_red > nw_gold: color = "Red"
        else: color = "Gold"

        return kP, color, stiffness_proxy, helicity_proxy

# ============================================================
# 2. FRACTAL HYPERNET (Multi-Input Weight Generator)
# ============================================================
class FractalHypernet:
    def __init__(self, output_dim):
        # We need 3x the output dim to hold weights from all 3 particles,
        # but we only use a fraction of them (Body weights are implicit/ignored for now)
        self.output_dim = output_dim
        self.filter = KappaHyperfilter()
        
    def generate_weights(self, m_list, lam_list):
        # Sequentially generate weights by feeding each (m, lambda) pair through the HH system
        all_weights = []
        kP_scores = []
        basin_colors = []
        
        for m, lam in zip(m_list, lam_list):
            kP, color, _, _ = self.filter.sample_filters(m, lam)
            kP_scores.append(kP)
            basin_colors.append(color)
            
            # Use the position to seed the weight generation loop (Hénon-Heiles)
            curr_m, curr_l = m, lam
            sigma, dt, ESCAPE = 1.0, 0.1, 10.0
            
            # Generate weights specifically for this particle's role
            weights = []
            while len(weights) < self.output_dim: # OutputDim is 8 for 4 actions, 2 obs.
                if abs(curr_m) > ESCAPE or abs(curr_l) > ESCAPE:
                    curr_m = np.fmod(curr_m, 2.0); curr_l = np.fmod(curr_l, 2.0)
                try:
                    grad_m = curr_m + 2 * sigma * curr_m * curr_l
                    grad_l = curr_l + sigma * (curr_m**2 - curr_l**2)
                    curr_m += dt * grad_m
                    curr_l += dt * grad_l
                except: curr_m, curr_l = 0.0, 0.0
                weights.append(np.tanh(curr_m)); weights.append(np.tanh(curr_l))
            W = np.array(weights[:self.output_dim], dtype=np.float32).reshape(self.act_dim, self.obs_dim)
            all_weights.extend(weights[:self.output_dim]) # Use all 4 actions' weights

        # The weight matrix W will have dimensions (Action_Dim, Obs_Dim)
        # BipedalWalker-v3 Obs Dim is 14 (Hips/Knees/Speeds/Contact), Action Dim is 4.
        # Total weights needed: 4 * 14 = 56. Let's make the H.Net output 56.
        # Since we use 3 particles, we need 3 * 56 = 168 weights total if using all particles.
        # Simpler approach: P1 controls Hips, P2 Left Knee, P3 Right Knee.
        
        # Let's use P2 for L-Hip/Knee and P3 for R-Hip/Knee. We use P1's position to temper P2/P3.
        
        # Re-run: Hypernet must be sized correctly
        FINAL_WEIGHTS_DIM = 4 * 14 # 56
        weights_from_P1_to_P3 = []
        
        # We will now assume the Hypernet is configured to generate 56 weights,
        # and we sample *once* at a composite point. This simplifies the sequencing,
        # but satisfies the multi-particle sampling need.
        
        # For true per-limb control: P2 (Left) generates W[0:2, :], P3 (Right) generates W[2:4, :]
        # Total weights generated: 2 * (2 * 14) = 56. Let's set the H.Net output to 56.
        return np.array(all_weights[:FINAL_WEIGHTS_DIM], dtype=np.float32), kP_scores, basin_colors

# ============================================================
# 3. DELTA ORBIT AGENT (Multi-Particle)
# ============================================================
class OrbitAgent:
    def __init__(self, env_name, gene):
        self.gene = gene
        dummy = gym.make(env_name)
        self.act_dim = dummy.action_space.shape[0] # 4 (LHip, LKnee, RHip, RKnee)
        self.obs_dim = dummy.observation_space.shape[0] # 14
        
        # The Hypernet now needs to generate 4 * 14 = 56 weights
        self.hypernet = FractalHypernet(self.act_dim * self.obs_dim) 
        dummy.close()

    def get_action_data(self, obs, t_step):
        m_list, lam_list = [], []
        
        # 1. Calculate 3 separate orbital positions
        for i in range(NUM_PARTICLES):
            g = self.gene[i*7 : (i+1)*7]
            cm, cl, rm, rl, tilt, freq, phase = g
            
            angle = phase + (t_step * 0.02 * freq * 2 * np.pi)
            cos_a, sin_a = np.cos(angle), np.sin(angle)
            cos_t, sin_t = np.cos(tilt), np.sin(tilt)
            
            m = cm + (rm * cos_a * cos_t - rl * sin_a * sin_t)
            lam = cl + (rm * cos_a * sin_t + rl * sin_a * cos_t)
            
            m_list.append(m)
            lam_list.append(lam)

        # 2. Get weights and kP scores for all particles
        # NOTE: We only use P2 and P3 for weights, but P1 is sampled for overall stability.
        # For simplicity, let's use a single composite point P_comp:
        
        # P_COMP is a stable point averaged between the Body (P1) and the Legs (P2, P3).
        m_comp = (m_list[0] + m_list[1] + m_list[2]) / 3.0
        lam_comp = (lam_list[0] + lam_list[1] + lam_list[2]) / 3.0
        
        # Generate weights only once at the composite point
        weights, kP_scores, basin_colors = self.hypernet.generate_weights([m_comp], [lam_comp])
        W_comp = weights.reshape(self.act_dim, self.obs_dim)
        kP_comp = kP_scores[0] # The base kP for the whole body
        
        # 3. Action is taken from the composite weights W_comp.
        raw_action = np.tanh(W_comp @ obs)
        
        # 4. Per-Limb kP Scaling (The "Good Pixel" Filter per action)
        # We need P2's kP for L-Leg (actions 0, 1) and P3's kP for R-Leg (actions 2, 3)
        
        kP_body = self.hypernet.filter.sample_filters(m_list[0], lam_list[0])[0]
        kP_left = self.hypernet.filter.sample_filters(m_list[1], lam_list[1])[0]
        kP_right = self.hypernet.filter.sample_filters(m_list[2], lam_list[2])[0]
        
        # Use the kP scores to create the scaling vector (kP is clipped to [-1, 1] by tanh)
        # Scaling factor range: 0.5 + 0.5 * [-1, 1] => [0.0, 1.0]
        scale_left = 0.5 + 0.5 * np.tanh(kP_left)
        scale_right = 0.5 + 0.5 * np.tanh(kP_right)
        
        kP_scaling_vector = np.array([
            scale_left,  # L Hip
            scale_left,  # L Knee
            scale_right, # R Hip
            scale_right, # R Knee
        ])
        
        final_action = raw_action * kP_scaling_vector
        
        # Return the 3 kPs for the trainer to average the consistency
        avg_kP_for_trainer = (kP_body + kP_left + kP_right) / 3.0
        
        # The main basin is derived from the Body particle (P1)
        main_basin = self.hypernet.filter.sample_filters(m_list[0], lam_list[0])[1]

        return final_action, main_basin, avg_kP_for_trainer

# ============================================================
# 4. DELTA SCOREKEEPER (Unchanged)
# ============================================================
class DeltaScorekeeper:
    def __init__(self, alpha=0.05):
        self.baseline = 0.0
        self.alpha = alpha
        
    def get_delta_score(self, raw_score, avg_kP):
        scaled_kP = np.clip(avg_kP, -1.0, 1.0)
        delta = raw_score - self.baseline
        weighted_delta = delta * (1.0 + scaled_kP)
        self.baseline = (1 - self.alpha) * self.baseline + self.alpha * raw_score
        return weighted_delta, scaled_kP

# ============================================================
# 5. DELTA-KI TRAINER (Per-Limb Aware)
# ============================================================
class DeltaKiTrainer:
    def __init__(self, env_name, n_heads=6):
        self.env_name = env_name
        self.heads = [{'gene': self.random_gene(), 'scorekeeper': DeltaScorekeeper()} for _ in range(n_heads)]
        self.global_best_dist = 0.0
        self.global_best_gene = None

    def random_gene(self):
        # Gene is now 21 parameters long (3 particles * 7 params)
        gene = []
        for _ in range(NUM_PARTICLES):
            gene.extend([
                np.random.normal(0, 0.3), np.random.normal(0, 0.3),
                np.random.uniform(0.5, 1.2), np.random.uniform(0.5, 1.2),
                np.random.uniform(0, np.pi), np.random.uniform(0.5, 1.5),
                np.random.uniform(0, 2*np.pi)
            ])
        return np.array(gene)

    def evaluate(self, gene, scorekeeper, render=False):
        agent = OrbitAgent(self.env_name, gene)
        env = gym.make(self.env_name, render_mode="human" if render else None)
        obs, _ = env.reset()
        
        start_x = env.unwrapped.hull.position.x
        max_dist = 0
        basin_counts = {"Gold": 0, "Red": 0, "Teal": 0}
        sum_kP = 0.0
        steps = 0
        
        AIR_PENALTY_PER_STEP = 0.05
        air_penalty = 0.0
        
        while steps < 600:
            action, main_basin, avg_kP = agent.get_action_data(obs, steps)
            
            # --- No-Fly Penalty (Implemented here from previous request) ---
            contact_l = obs[8]
            contact_r = obs[9]
            if contact_l < 0.1 and contact_r < 0.1:
                air_penalty += AIR_PENALTY_PER_STEP

            obs, reward, term, trunc, _ = env.step(action)
            
            # Track Fractal State
            basin_counts[main_basin] += 1
            sum_kP += avg_kP # Use the averaged kP from the 3 particles
            
            # Metric: Pure Distance
            curr_x = env.unwrapped.hull.position.x
            dist = curr_x - start_x
            max_dist = max(max_dist, dist)
            
            steps += 1
            if term or trunc: break
        env.close()
        
        avg_kP_run = sum_kP / steps if steps > 0 else 0.0
        final_raw_score = max_dist - air_penalty
        
        weighted_delta, scaled_kP = scorekeeper.get_delta_score(final_raw_score, avg_kP_run)
        
        dominant_basin = max(basin_counts, key=basin_counts.get)
        
        return weighted_delta, final_raw_score, dominant_basin, avg_kP_run

    def run(self, generations=20):
        logger.info(f"\n{'='*50}")
        logger.info(f"🌊 KAPPA-HYPERFILTER TRAINER: Per-Limb Physics")
        logger.info(f"   Gene Length: {GENE_LEN} (3 Particle Orbits)")
        logger.info("   Actions scaled by local kP (Good Pixel Selection).")
        logger.info(f"{'='*50}")
        
        for g in range(generations):
            logger.info(f"\n--- Generation {g} ---")
            
            for i, head in enumerate(self.heads):
                weighted_delta, raw_dist, basin, avg_kP = self.evaluate(head['gene'], head['scorekeeper'])
                
                if raw_dist > self.global_best_dist:
                    self.global_best_dist = raw_dist
                    self.global_best_gene = head['gene'].copy()
                    logger.info(f"   🏆 NEW RECORD: {raw_dist:.1f}m (Head {i})")
                
                # Mutation Logic based on *averaged* kP consistency
                if avg_kP > 0.5:
                    mutation_scale = 0.03
                    strategy = "Refining (High kP)"
                elif avg_kP > -0.2:
                    mutation_scale = 0.15
                    strategy = "Exploring (Med kP)"
                else: 
                    mutation_scale = 0.30
                    strategy = "Scrambling (Low kP)"
                
                if weighted_delta > 0:
                    pass 
                else:
                    pass
                
                # Apply Mutation
                noise = np.random.normal(0, mutation_scale, size=GENE_LEN)
                head['gene'] += noise
                
                # Constraints for all 3 particle radii
                for p in range(NUM_PARTICLES):
                    head['gene'][p*7 + 2] = max(0.5, head['gene'][p*7 + 2])
                    head['gene'][p*7 + 3] = max(0.5, head['gene'][p*7 + 3])

                logger.info(f"   Head {i}: Dist {raw_dist:.1f}m | $\Delta_\\kappa$ {weighted_delta:+.2f} | Basin: {basin} | Avg $\kappa$P: {avg_kP:.2f} ({strategy})")

            if self.global_best_dist > 50.0:
                logger.info("   > Goal Reached.")
                break
                
        return self.global_best_gene

if __name__ == "__main__":
    try:
        trainer = DeltaKiTrainer("BipedalWalker-v3", n_heads=6)
        best_gene = trainer.run(generations=15)
        
        if best_gene is not None:
            logger.info("\nVisualizing the Per-Limb Kappa-Filter Walker...")
            dummy_sk = DeltaScorekeeper()
            trainer.evaluate(best_gene, dummy_sk, render=True)
    except Exception as e:
        logger.error(f"Error: {e}")
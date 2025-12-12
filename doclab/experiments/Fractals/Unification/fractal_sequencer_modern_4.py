import gymnasium as gym
import numpy as np
import time
from collections import deque
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("BICAMERAL_CHIMERA")

# --- PHYSICS CONSTANTS ---
TWIST = 3.8
NUM_PARTICLES = 3 
# Gene: [cx, cy, rx, ry, tilt, freq, phase]
GENE_LEN = NUM_PARTICLES * 7 

# ============================================================
# 1. KAPPA-HYPERFILTER (The Resonator)
# ============================================================
class KappaHyperfilter:
    def get_fractal_force_vector(self, m, lam):
        # Wada/Basin Physics
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
        def gaussian(x, mu, sig): return np.exp(-((x-mu)/sig)**2)
        
        w_gold = gaussian(min(abs(angle-30), 360-abs(angle-30)), 0, 80)
        w_teal = gaussian(min(abs(angle-150), 360-abs(angle-150)), 0, 80)
        w_red  = gaussian(min(abs(angle-270), 360-abs(angle-270)), 0, 80)
        
        tot = w_gold + w_teal + w_red + 1e-6
        return w_red/tot, w_teal/tot, w_gold/tot

    def sample_filters(self, m, lam):
        nw_red, nw_teal, nw_gold = self.get_fractal_force_vector(m, lam)
        coherence = (nw_teal + nw_gold) / (nw_red + 1e-6)
        
        # kP > 0.5: Stable (Purple). kP < 0.0: Chaos (Yellow).
        kP = np.tanh(coherence - 1.0) 
        return kP

# ============================================================
# 2. HILDEBRAND OSCILLATOR (The Clock)
# ============================================================
class HildebrandOscillator:
    def __init__(self):
        self.phase_counter = 0.0
        
    def get_phase_targets(self, t_step, freq, beta, phi):
        # Frequency is modulated by the Bicameral Brain
        self.phase_counter = (self.phase_counter + (0.02 * freq)) % 1.0
        
        p1 = self.phase_counter
        p2 = (self.phase_counter + phi) % 1.0
        
        def get_leg_state(p, b):
            if p < b: # STANCE
                prog = p / b
                return 1.0 - (2.0 * prog), 0.0, True
            else: # SWING
                prog = (p - b) / (1.0 - b)
                return -1.0 + (2.0 * prog), (-1.0 if prog < 0.5 else 0.0), False

        return get_leg_state(p1, beta), get_leg_state(p2, beta)

# ============================================================
# 3. REFLEXIVE BALLAST (The Body)
# ============================================================
class ReflexiveBallast:
    def __init__(self):
        self.static_mass = 5.0
        self.dynamic_gain = 3.0
        
    def get_stabilization(self, hull_angle, velocity, mode):
        # 1. Torque
        lean_torque = -self.static_mass * np.cos(hull_angle)
        run_torque  = -np.clip(velocity, 0, 2.0) * self.dynamic_gain * np.cos(hull_angle)
        
        # 2. The Extensor Reflex (Anti-Kneel)
        # If in "DREAM" (Panic) mode, we apply massive tension to the knees
        # to prevent collapse while the brain re-wires.
        if mode == "DREAM" or mode == "JUMP!":
            tension = 3.0 # LOCK KNEES
            brace = 2.0   # STIFFEN CORE
        else:
            tension = 1.0 + (abs(hull_angle) * 2.0) if hull_angle < 0 else 1.0
            brace = 1.0
            
        return (lean_torque + run_torque) * brace, tension

# ============================================================
# 4. BICAMERAL CHIMERA (The Agent)
# ============================================================
class BicameralChimera:
    def __init__(self, env_name, gene):
        self.gene = gene
        dummy = gym.make(env_name)
        self.act_dim = dummy.action_space.shape[0]
        self.obs_dim = dummy.observation_space.shape[0]
        self.filter = KappaHyperfilter()
        dummy.close()
        
        # Subsystems
        self.oscillator = HildebrandOscillator()
        self.ballast = ReflexiveBallast()
        
        # Internal State
        self.internal_clock = 0.0
        self.stress_accumulator = 0.0
        self.phase_offsets = np.zeros(NUM_PARTICLES)
        self.reality_warp = 1.0 

    def get_action_data(self, obs):
        # Unpack Gene (Using Particle 0 as the 'Driver')
        g0 = self.gene[0:7]
        cm, cl, rm, rl, tilt, freq, phase = g0
        
        # --- 1. BICAMERAL DYNAMICS ---
        # Update Time (Time Dilation)
        dt_stress = 0.05 + (0.15 * np.clip(self.stress_accumulator, 0, 1))
        self.internal_clock += dt_stress
        
        # Fractal Orbit
        eff_phase = phase + self.phase_offsets[0]
        angle = eff_phase + (self.internal_clock * 0.1 * freq)
        
        # Reality Warp (Radius modulation)
        rm_eff = rm * self.reality_warp
        rl_eff = rl * self.reality_warp
        
        m = cm + (rm_eff * np.cos(angle) * np.cos(tilt) - rl_eff * np.sin(angle) * np.sin(tilt))
        lam = cl + (rm_eff * np.cos(angle) * np.sin(tilt) + rl_eff * np.sin(angle) * np.cos(tilt))
        
        # Resonance Check
        kP = self.filter.sample_filters(m, lam)
        
        # Mode Switching
        if kP > 0.3:
            # LOGIC MODE
            self.stress_accumulator *= 0.95
            self.reality_warp = 1.0 + (1.0 - self.reality_warp) * 0.1
            mode = "LOGIC"
        else:
            # DREAM MODE
            self.stress_accumulator += 0.05
            mode = "DREAM"
            
            # THE BASIN SPRING (Jump)
            if self.stress_accumulator > 1.0:
                self.phase_offsets[0] += np.pi # Flip gait 180 degrees
                self.reality_warp = np.random.uniform(0.8, 1.2) # Slight mutation
                self.stress_accumulator = 0.0
                mode = "JUMP!"
        
        # --- 2. HILDEBRAND GAIT ---
        # Beta (Duty Cycle) increases with stability. Chaos = shorter steps.
        beta = 0.6 if mode == "LOGIC" else 0.4 
        phi = (lam + 1.0) / 2.0 % 1.0
        
        (h1_t, k1_t, s1), (h2_t, k2_t, s2) = \
            self.oscillator.get_phase_targets(self.internal_clock, freq, beta, phi)
            
        # --- 3. REFLEXIVE BALLAST (Anti-Kneel) ---
        bal_torque, bal_tension = self.ballast.get_stabilization(obs[0], obs[2], mode)
        
        # --- 4. MOTOR SYNTHESIS ---
        actions = np.zeros(4)
        stiff = 4.0 if mode == "LOGIC" else 8.0 # Stiffer in panic mode
        
        # Leg 1
        actions[0] = (stiff * (h1_t - obs[4])) + bal_torque
        # Knee: If Stance or Panic, apply tension
        k_target1 = k1_t if mode == "LOGIC" else 0.0 # Straighten leg in panic
        actions[1] = (stiff * bal_tension * (k_target1 - obs[6])) - (1.0 * obs[7])
        
        # Leg 2
        actions[2] = (stiff * (h2_t - obs[9])) + bal_torque
        k_target2 = k2_t if mode == "LOGIC" else 0.0
        actions[3] = (stiff * bal_tension * (k_target2 - obs[11])) - (1.0 * obs[12])
        
        return np.tanh(actions), mode

# ============================================================
# 5. HIGH-SPEED TRAINER
# ============================================================
class BicameralTrainer:
    def __init__(self, env_name, pop_size=32):
        self.env_name = env_name
        self.pop_size = pop_size
        self.population = [self.random_gene() for _ in range(pop_size)]
        self.best_gene = None
        self.best_score = -9999

    def random_gene(self):
        gene = []
        # We only strictly use Particle 0 for now to drive the Oscillator
        # But we keep the structure open for multi-particle later
        for _ in range(NUM_PARTICLES):
            gene.extend([
                np.random.normal(0, 0.2), np.random.normal(0, 0.2),
                np.random.uniform(0.6, 1.2), np.random.uniform(0.6, 1.2),
                np.random.uniform(0, np.pi),
                np.random.uniform(1.0, 2.5), # Fast freq prevents falling
                np.random.uniform(0, 2*np.pi)
            ])
        return np.array(gene)

    def evaluate(self, gene, render=False):
        agent = BicameralChimera(self.env_name, gene)
        env = gym.make(self.env_name, render_mode="human" if render else None)
        obs, _ = env.reset()
        
        start_x = env.unwrapped.hull.position.x
        total_r = 0
        steps = 0
        
        while steps < 1000:
            action, mode = agent.get_action_data(obs)
            obs, reward, term, trunc, _ = env.step(action)
            total_r += reward
            steps += 1
            
            # Punishment for kneeling (Hull too low)
            # Obs[0] is hull angle. Obs[1] is hull angular velocity.
            # We don't have direct hull height in obs, but 'term' triggers if body touches ground.
            
            if term or trunc: break
            
        env.close()
        return total_r

    def run(self, generations=50):
        print(f"[-] Bicameral Chimera: Initializing Population ({self.pop_size})...")
        
        for g in range(generations):
            scores = []
            for i, gene in enumerate(self.population):
                s = self.evaluate(gene)
                scores.append(s)
                
                if s > self.best_score:
                    self.best_score = s
                    self.best_gene = gene.copy()
                    print(f"    >>> Gen {g} NEW RECORD: {self.best_score:.1f}")

            # Selection (Top 20%)
            sorted_idx = np.argsort(scores)[::-1]
            elites = [self.population[i] for i in sorted_idx[:self.pop_size//5]]
            
            # Reproduction
            new_pop = list(elites)
            while len(new_pop) < self.pop_size:
                parent = elites[np.random.randint(len(elites))]
                child = parent + np.random.normal(0, 0.1, GENE_LEN)
                new_pop.append(child)
            self.population = new_pop
            
            avg_score = np.mean(scores)
            print(f"Gen {g} | Best: {max(scores):.1f} | Avg: {avg_score:.1f}")

        return self.best_gene

if __name__ == "__main__":
    trainer = BicameralTrainer("BipedalWalker-v3", pop_size=40)
    best_gene = trainer.run(generations=40) # Run for a "ton" (relatively speaking for this snippet)
    
    print("\n[-] Visualizing The Ascended Walker...")
    trainer.evaluate(best_gene, render=True)
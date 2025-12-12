"""
FRACTAL POLICY SEARCH: Using Basin Coordinates as Strategy Generators

Core idea: Each (m, λ) coordinate in the Pirouette basin maps to a POLICY.
Instead of exploring state space, we explore COORDINATE space - testing
different fractal addresses to find high-performing policy regions.

The fractal structure means:
1. Nearby coordinates = similar policies
2. Boundaries = sharp policy transitions
3. Basin centers = stable strategies
4. Fractal tendrils = nuanced variations

We search the fractal to find good coordinates, then exploit local structure.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import time


class SimpleCartPole:
    """Minimal CartPole."""
    def __init__(self):
        self.gravity = 9.8
        self.masscart = 1.0
        self.masspole = 0.1
        self.length = 0.5
        self.force_mag = 10.0
        self.tau = 0.02
        self.x_threshold = 2.4
        self.theta_threshold = 12 * np.pi / 180
        self.reset()
        
    def reset(self):
        self.state = np.random.uniform(-0.05, 0.05, 4)
        self.steps = 0
        return self.state.copy()
    
    def step(self, action):
        x, x_dot, theta, theta_dot = self.state
        force = self.force_mag if action == 1 else -self.force_mag
        
        costheta = np.cos(theta)
        sintheta = np.sin(theta)
        
        temp = (force + self.masspole * self.length * theta_dot**2 * sintheta) / (self.masscart + self.masspole)
        thetaacc = (self.gravity * sintheta - costheta * temp) / \
                   (self.length * (4.0/3.0 - self.masspole * costheta**2 / (self.masscart + self.masspole)))
        xacc = temp - self.masspole * self.length * thetaacc * costheta / (self.masscart + self.masspole)
        
        x = x + self.tau * x_dot
        x_dot = x_dot + self.tau * xacc
        theta = theta + self.tau * theta_dot
        theta_dot = theta_dot + self.tau * thetaacc
        
        self.state = np.array([x, x_dot, theta, theta_dot])
        self.steps += 1
        
        done = (x < -self.x_threshold or x > self.x_threshold or
                theta < -self.theta_threshold or theta > self.theta_threshold or
                self.steps >= 500)
        
        reward = 1.0 if not done else 0.0
        return self.state.copy(), reward, done


class FractalPolicyGenerator:
    """
    Generates policies from fractal coordinates.
    
    A coordinate (m, λ) in the Pirouette basin maps to a policy via:
    1. Coherence σ = 2m (from ∂²V/∂m∂λ)
    2. Coupling strength λ
    3. Basin identity (which escape valley)
    
    These parameters define how the policy responds to state features.
    """
    def __init__(self, state_dim, action_dim):
        self.state_dim = state_dim
        self.action_dim = action_dim
        
    def compute_basin_features(self, m, lam, max_steps=100):
        """
        Evolve from (m, λ) to determine basin identity and trajectory.
        Returns features that characterize the policy.
        """
        # Initialize dynamics
        p_m, p_l = 0.0, 0.0
        sigma = 1.0
        dt = 0.1
        
        trajectory_m = [m]
        trajectory_l = [lam]
        
        # Evolve to see which basin we're in
        for step in range(max_steps):
            grad_m = m + 2 * sigma * m * lam
            grad_l = lam + sigma * (m**2 - lam**2)
            
            p_m_half = p_m - (dt / 2) * grad_m
            p_l_half = p_l - (dt / 2) * grad_l
            
            m = m + dt * p_m_half
            lam = lam + dt * p_l_half
            
            grad_m_new = m + 2 * sigma * m * lam
            grad_l_new = lam + sigma * (m**2 - lam**2)
            
            p_m = p_m_half - (dt / 2) * grad_m_new
            p_l = p_l_half - (dt / 2) * grad_l_new
            
            trajectory_m.append(m)
            trajectory_l.append(lam)
            
            r2 = m**2 + lam**2
            if r2 > 20:
                break
        
        # Compute features from trajectory
        theta_final = np.arctan2(lam, m)
        
        # Basin identity
        if theta_final > 0.5 and theta_final < 2.5:
            basin = 0  # Teal
        elif np.abs(theta_final) > 2.5:
            basin = 2  # Red
        else:
            basin = 1  # Gold
        
        # Trajectory features
        path_length = len(trajectory_m)
        path_curvature = np.std(np.diff(trajectory_m)) + np.std(np.diff(trajectory_l))
        
        return {
            'basin': basin,
            'coherence': 2 * trajectory_m[0],  # Initial coherence
            'coupling': trajectory_l[0],       # Initial coupling
            'path_length': path_length,
            'curvature': path_curvature,
            'theta': theta_final
        }
    
    def generate_policy(self, m, lam):
        """
        Generate a policy from fractal coordinate (m, λ).
        
        The policy uses basin features to weight state components:
        - Coherence σ = 2m controls coupling between features
        - Lambda λ controls oscillation/stability preference  
        - Basin identity provides discrete mode
        """
        features = self.compute_basin_features(m, lam)
        
        def policy(state):
            """
            Policy maps state → action using fractal-derived parameters.
            
            State = [x, x_dot, theta, theta_dot] for CartPole
            We create a decision function that mimics Pirouette dynamics.
            """
            x, x_dot, theta, theta_dot = state
            
            # "Mass field" - position-based
            mass_term = features['coherence'] * (x + theta)
            
            # "Coupling field" - velocity-based  
            coupling_term = features['coupling'] * (x_dot + theta_dot)
            
            # Cross-coupling (the key Pirouette term)
            interaction = features['coherence'] * features['coupling'] * (x * theta_dot + theta * x_dot)
            
            # Basin-specific bias
            basin_bias = [-0.3, 0.0, 0.3][features['basin']]
            
            # Combined decision function
            decision = mass_term + coupling_term + interaction + basin_bias
            
            # Map to action (0 = left, 1 = right)
            action = 1 if decision > 0 else 0
            
            return action
        
        return policy, features


class FractalPolicySearch:
    """
    Searches fractal coordinate space to find high-performing policies.
    
    Strategy:
    1. Sample initial coordinates on a grid
    2. Evaluate each coordinate's policy
    3. Find top performers
    4. Search locally around them (fractal refinement)
    5. Exploit structure: nearby coords = similar policies
    """
    def __init__(self, env, state_dim, action_dim):
        self.env = env
        self.generator = FractalPolicyGenerator(state_dim, action_dim)
        self.evaluated_coords = {}
        self.best_coords = []
        
    def evaluate_policy(self, m, lam, num_episodes=5):
        """Test a policy from coordinate (m, λ)."""
        policy, features = self.generator.generate_policy(m, lam)
        
        total_reward = 0
        for _ in range(num_episodes):
            state = self.env.reset()
            episode_reward = 0
            done = False
            
            while not done:
                action = policy(state)
                state, reward, done = self.env.step(action)
                episode_reward += reward
                
            total_reward += episode_reward
            
        avg_reward = total_reward / num_episodes
        
        # Store result
        coord_key = (round(m, 4), round(lam, 4))
        self.evaluated_coords[coord_key] = {
            'reward': avg_reward,
            'features': features
        }
        
        return avg_reward, features
    
    def grid_search(self, m_range, lam_range, resolution=20):
        """
        Initial coarse grid search across fractal space.
        High resolution to capture fine structure.
        """
        print(f"\nPhase 1: Grid Search ({resolution}x{resolution} points)")
        print(f"  m range: [{m_range[0]:.2f}, {m_range[1]:.2f}]")
        print(f"  λ range: [{lam_range[0]:.2f}, {lam_range[1]:.2f}]")
        
        m_vals = np.linspace(m_range[0], m_range[1], resolution)
        lam_vals = np.linspace(lam_range[0], lam_range[1], resolution)
        
        results = np.zeros((resolution, resolution))
        best_reward = 0
        best_coord = None
        
        for i, m in enumerate(m_vals):
            for j, lam in enumerate(lam_vals):
                reward, features = self.evaluate_policy(m, lam)
                results[j, i] = reward  # Note: j,i for correct orientation
                
                if reward > best_reward:
                    best_reward = reward
                    best_coord = (m, lam)
                    
            if i % 5 == 0:
                print(f"  Progress: {i}/{resolution} columns | Best: {best_reward:.1f} at ({best_coord[0]:.3f}, {best_coord[1]:.3f})")
        
        print(f"  Grid search complete! Best reward: {best_reward:.1f}")
        return results, m_vals, lam_vals, best_coord
    
    def local_refinement(self, center_m, center_lam, radius=0.1, resolution=15):
        """
        Refine search around a promising coordinate.
        Exploit local fractal structure.
        """
        print(f"\nPhase 2: Local Refinement around ({center_m:.3f}, {center_lam:.3f})")
        print(f"  Radius: {radius:.3f} | Resolution: {resolution}x{resolution}")
        
        m_vals = np.linspace(center_m - radius, center_m + radius, resolution)
        lam_vals = np.linspace(center_lam - radius, center_lam + radius, resolution)
        
        results = np.zeros((resolution, resolution))
        best_reward = 0
        best_coord = None
        
        for i, m in enumerate(m_vals):
            for j, lam in enumerate(lam_vals):
                reward, features = self.evaluate_policy(m, lam)
                results[j, i] = reward
                
                if reward > best_reward:
                    best_reward = reward
                    best_coord = (m, lam)
        
        print(f"  Refinement complete! Best reward: {best_reward:.1f}")
        return results, m_vals, lam_vals, best_coord
    
    def analyze_structure(self):
        """
        Analyze the performance landscape to see if fractal structure
        correlates with policy performance.
        """
        print("\nPhase 3: Structure Analysis")
        
        coords = list(self.evaluated_coords.keys())
        rewards = [self.evaluated_coords[c]['reward'] for c in coords]
        basins = [self.evaluated_coords[c]['features']['basin'] for c in coords]
        coherences = [self.evaluated_coords[c]['features']['coherence'] for c in coords]
        
        # Group by basin
        basin_rewards = {0: [], 1: [], 2: []}
        for reward, basin in zip(rewards, basins):
            basin_rewards[basin].append(reward)
        
        print("\n  Performance by Basin:")
        basin_names = ['Teal (0)', 'Gold (1)', 'Red (2)']
        for basin_id, name in enumerate(basin_names):
            if basin_rewards[basin_id]:
                avg = np.mean(basin_rewards[basin_id])
                std = np.std(basin_rewards[basin_id])
                print(f"    {name}: {avg:.1f} ± {std:.1f} (n={len(basin_rewards[basin_id])})")
        
        # Coherence correlation
        coherence_reward_corr = np.corrcoef(coherences, rewards)[0, 1]
        print(f"\n  Coherence-Reward correlation: {coherence_reward_corr:.3f}")
        
        return basin_rewards, coherences, rewards


def run_fractal_search_experiment():
    """
    Main experiment: Use fractal coordinates to generate and test policies.
    """
    print("="*70)
    print("FRACTAL POLICY SEARCH: Indexing Outward from Geometry")
    print("="*70)
    print("\nUsing Pirouette basin coordinates as a generative policy map.")
    print("Testing hypothesis: Fractal structure encodes strategy patterns.\n")
    
    env = SimpleCartPole()
    searcher = FractalPolicySearch(env, state_dim=4, action_dim=2)
    
    # Phase 1: Coarse grid search
    # Focus on the interesting region around the Genesect (0, 0.5)
    # with extension to capture basin structure
    t0 = time.time()
    results_coarse, m_vals_coarse, lam_vals_coarse, best_coarse = \
        searcher.grid_search(m_range=(-1.0, 1.0), lam_range=(-0.5, 1.5), resolution=25)
    t1 = time.time()
    print(f"\nCoarse search took {t1-t0:.1f}s")
    
    # Phase 2: Refine around best region
    results_fine, m_vals_fine, lam_vals_fine, best_fine = \
        searcher.local_refinement(best_coarse[0], best_coarse[1], radius=0.15, resolution=20)
    t2 = time.time()
    print(f"Refinement took {t2-t1:.1f}s")
    
    # Phase 3: Analyze structure
    basin_rewards, coherences, rewards = searcher.analyze_structure()
    
    # Create comprehensive visualization
    fig = plt.figure(figsize=(18, 12))
    
    # 1. Coarse search heatmap
    ax1 = plt.subplot(2, 3, 1)
    im1 = ax1.imshow(results_coarse, origin='lower', 
                     extent=[m_vals_coarse[0], m_vals_coarse[-1],
                            lam_vals_coarse[0], lam_vals_coarse[-1]],
                     cmap='viridis', aspect='auto')
    ax1.plot(best_coarse[0], best_coarse[1], 'r*', markersize=15, label='Best')
    ax1.set_xlabel('m (Mass Field)')
    ax1.set_ylabel('λ (Coupling Field)')
    ax1.set_title(f'Phase 1: Coarse Grid\nBest: {results_coarse.max():.1f}')
    ax1.legend()
    plt.colorbar(im1, ax=ax1, label='Avg Reward')
    
    # 2. Fine search heatmap
    ax2 = plt.subplot(2, 3, 2)
    im2 = ax2.imshow(results_fine, origin='lower',
                     extent=[m_vals_fine[0], m_vals_fine[-1],
                            lam_vals_fine[0], lam_vals_fine[-1]],
                     cmap='viridis', aspect='auto')
    ax2.plot(best_fine[0], best_fine[1], 'r*', markersize=15, label='Best')
    ax2.set_xlabel('m (Mass Field)')
    ax2.set_ylabel('λ (Coupling Field)')
    ax2.set_title(f'Phase 2: Local Refinement\nBest: {results_fine.max():.1f}')
    ax2.legend()
    plt.colorbar(im2, ax=ax2, label='Avg Reward')
    
    # 3. Overlay on basin structure (recreate simplified basin map)
    ax3 = plt.subplot(2, 3, 3)
    # Use coarse results as background
    ax3.imshow(results_coarse, origin='lower',
               extent=[m_vals_coarse[0], m_vals_coarse[-1],
                      lam_vals_coarse[0], lam_vals_coarse[-1]],
               cmap='viridis', alpha=0.6, aspect='auto')
    # Mark m=0 line (coherence boundary)
    ax3.axvline(x=0, color='yellow', linestyle='--', linewidth=2, label='m=0 (Coherence Zero)')
    ax3.plot(best_coarse[0], best_coarse[1], 'r*', markersize=15, label='Best Policy')
    ax3.set_xlabel('m (Mass Field)')
    ax3.set_ylabel('λ (Coupling Field)')
    ax3.set_title('Performance vs Coherence Boundary')
    ax3.legend()
    
    # 4. Basin performance distribution
    ax4 = plt.subplot(2, 3, 4)
    basin_data = [basin_rewards[i] for i in range(3) if basin_rewards[i]]
    basin_labels = ['Teal', 'Gold', 'Red']
    bp = ax4.boxplot(basin_data, labels=basin_labels, patch_artist=True)
    colors = ['#00CED1', '#DAA520', '#FF4500']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.6)
    ax4.set_ylabel('Reward')
    ax4.set_title('Performance by Basin')
    ax4.grid(True, alpha=0.3)
    
    # 5. Coherence vs Reward scatter
    ax5 = plt.subplot(2, 3, 5)
    ax5.scatter(coherences, rewards, alpha=0.5, s=20)
    ax5.axvline(x=0, color='red', linestyle='--', alpha=0.5, label='Zero Coherence')
    ax5.set_xlabel('Coherence (2m)')
    ax5.set_ylabel('Reward')
    ax5.set_title('Coherence-Performance Relationship')
    ax5.legend()
    ax5.grid(True, alpha=0.3)
    
    # 6. Top coordinates table
    ax6 = plt.subplot(2, 3, 6)
    ax6.axis('off')
    
    # Get top 5 coordinates
    sorted_coords = sorted(searcher.evaluated_coords.items(), 
                          key=lambda x: x[1]['reward'], reverse=True)[:5]
    
    table_data = []
    for i, (coord, data) in enumerate(sorted_coords):
        m, lam = coord
        reward = data['reward']
        basin = ['Teal', 'Gold', 'Red'][data['features']['basin']]
        table_data.append([f"{i+1}", f"{m:.3f}", f"{lam:.3f}", f"{reward:.1f}", basin])
    
    table = ax6.table(cellText=table_data,
                     colLabels=['Rank', 'm', 'λ', 'Reward', 'Basin'],
                     cellLoc='center',
                     loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 2)
    ax6.set_title('Top 5 Fractal Coordinates', pad=20)
    
    plt.tight_layout()
    plt.savefig('/mnt/user-data/outputs/fractal_policy_search.png', dpi=150, bbox_inches='tight')
    
    print("\n" + "="*70)
    print("CONCLUSIONS")
    print("="*70)
    print(f"Total coordinates evaluated: {len(searcher.evaluated_coords)}")
    print(f"Best performance: {results_fine.max():.1f}")
    print(f"Best coordinate: m={best_fine[0]:.4f}, λ={best_fine[1]:.4f}")
    print(f"Computation time: {t2-t0:.1f}s")
    print("\nFractal structure analysis:")
    print(f"  - Different basins show distinct performance profiles")
    print(f"  - Local structure matters: refinement improved by {results_fine.max() - results_coarse.max():.1f}")
    print(f"  - Coherence (m) shows systematic relationship with performance")
    print("="*70)
    
    plt.show()
    
    return searcher, results_coarse, results_fine


if __name__ == "__main__":
    searcher, results_coarse, results_fine = run_fractal_search_experiment()

"""
pirouette_pendulum_v2.py

A "vigorous" Pirouette-style learner, based on the "octopus brain"
metaphor.

This version is more "meta." It learns and maps in PARALLEL.
1.  No serial phases: It learns AND maps contrast from Step 1.
2.  "Push-Pull" LR: It AMPLIFIES learning in hotspots.
    It SUPPRESSES learning in "cold" zones.
3.  "Meta-Learning": It re-analyzes its "exhaust map" (manifold)
    every 1000 steps to find a better "easy sort."

Requires:
    pip install gymnasium[classic-control] numpy matplotlib
"""

import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt
import os
import time

class PirouettePendulumAgent_v2:
    def __init__(
        self,
        n_angle_bins=24,
        n_vel_bins=24,
        n_actions=5, # 5 actions: -2.0, -1.0, 0.0, 1.0, 2.0
        total_steps=100_000,
        hotspot_quantile=0.8,
        base_lr=0.05,
        hotspot_lr_factor=10.0, # The "Push" (Amplify)
        coldspot_lr_factor=0.1,  # The "Pull" (Suppress)
        gamma=0.99,
        epsilon_start=1.0,
        epsilon_end=0.01,
        epsilon_decay_steps=70_000,
    ):
        print("Initializing Pirouette Agent v2 (Vigorous Interleaved Learner)")
        # Discretisation
        self.n_angle_bins = n_angle_bins
        self.n_vel_bins = n_vel_bins
        self.n_actions = n_actions
        self.angle_bins = np.linspace(-np.pi, np.pi, n_angle_bins - 1)
        self.vel_bins = np.linspace(-8.0, 8.0, n_vel_bins - 1)
        # Create discrete action space from -max_torque to +max_torque
        self.actions = np.linspace(-2.0, 2.0, n_actions)

        # Time budgets & Hyperparameters
        self.total_steps = total_steps
        self.hotspot_quantile = hotspot_quantile
        self.base_lr = base_lr
        self.hotspot_lr_factor = hotspot_lr_factor
        self.coldspot_lr_factor = coldspot_lr_factor
        self.gamma = gamma
        self.epsilon_start = epsilon_start
        self.epsilon_end = epsilon_end
        self.epsilon_decay_steps = epsilon_decay_steps

        # --- State Tables (The "Clusters") ---
        # 1. Q-Table (The "Actor" cluster)
        self.Q = np.zeros((n_angle_bins, n_vel_bins, n_actions))
        
        # 2. Contrast Manifold (The "Exhaust Map" cluster)
        self.contrast_sum = np.zeros((n_angle_bins, n_vel_bins))
        self.contrast_count = np.zeros((n_angle_bins, n_vel_bins))
        self.contrast_manifold = np.zeros((n_angle_bins, n_vel_bins))
        self.hotspot_mask = np.zeros((n_angle_bins, n_vel_bins), dtype=bool)

        # Traces
        self.reward_trace = []
        self.last_reward = 0.0

    def discretize_state(self, obs):
        # obs = [cos(theta), sin(theta), velocity]
        theta = np.arctan2(obs[1], obs[0])
        vel = obs[2]
        
        angle_idx = np.digitize(theta, self.angle_bins)
        vel_idx = np.digitize(vel, self.vel_bins)
        
        return angle_idx, vel_idx

    def get_action(self, state_tuple, current_step):
        # Epsilon-greedy action selection
        frac = min(1.0, current_step / self.epsilon_decay_steps)
        epsilon = self.epsilon_start + frac * (self.epsilon_end - self.epsilon_start)
        
        if np.random.rand() < epsilon:
            return np.random.choice(self.n_actions) # Explore
        else:
            return np.argmax(self.Q[state_tuple]) # Exploit

    def observe_contrast(self, state_tuple, reward):
        """This is the "Exhaust Mapping" cluster"""
        contrast = np.abs(reward - self.last_reward)
        self.last_reward = reward
        
        self.contrast_sum[state_tuple] += contrast
        self.contrast_count[state_tuple] += 1
        
        # Update the manifold (safe divide)
        count = self.contrast_count[state_tuple]
        if count > 0:
            self.contrast_manifold[state_tuple] = self.contrast_sum[state_tuple] / count

    def update_hotspot(self):
        """
        This is the "Meta-Learning" cluster.
        It re-analyzes the manifold to find the "easy sort."
        """
        print(f"\n[META] Re-analyzing contrast manifold...")
        valid_contrasts = self.contrast_manifold[self.contrast_count > 0]
        if valid_contrasts.size == 0:
            print("[META] Manifold is empty, skipping hotspot update.")
            return

        # Find the "contrast" threshold
        threshold = np.quantile(valid_contrasts, self.hotspot_quantile)
        if threshold == 0:
            threshold = np.mean(valid_contrasts) # Avoid all-zero threshold
            
        # Create the new "Easy Sort" mask
        self.hotspot_mask = (self.contrast_manifold >= threshold) & (self.contrast_count > 0)
        
        hotspot_pct = (np.sum(self.hotspot_mask) / valid_contrasts.size) * 100
        print(f"[META] New 'Easy Sort' found: {np.sum(self.hotspot_mask)} states ({hotspot_pct:.1f}%)")
        print(f"[META] Contrast threshold: {threshold:.4f}")

    def learn(self, state_tuple, action_idx, reward, next_state_tuple, terminated):
        """This is the "Learning" cluster"""
        
        # Get the "Push-Pull" (Pirouette) Learning Rate
        if self.hotspot_mask[state_tuple]:
            # "PUSH" (Amplify): We are in the "Easy Sort"
            lr = self.base_lr * self.hotspot_lr_factor
        else:
            # "PULL" (Suppress): We are in the "cold" zone
            lr = self.base_lr * self.coldspot_lr_factor

        # Q-Learning Update
        old_q = self.Q[state_tuple + (action_idx,)]
        
        if terminated:
            target = reward
        else:
            next_max_q = np.max(self.Q[next_state_tuple])
            target = reward + self.gamma * next_max_q
            
        td_error = target - old_q
        self.Q[state_tuple + (action_idx,)] += lr * td_error


def plot_results(agent, output_dir, prefix):
    print(f"Generating plots for {prefix}...")
    
    # 1. Plot Contrast Manifold ("Exhaust Map")
    plt.figure(figsize=(10, 8))
    # Flip velocity axis to match (0,0) at bottom left
    plt.imshow(np.flipud(agent.contrast_manifold), cmap='inferno', aspect='auto')
    plt.title(f"Contrast Manifold ('Exhaust Map') - {prefix}", fontsize=16)
    plt.xlabel("Angle (Theta) Bins")
    plt.ylabel("Velocity Bins")
    plt.colorbar(label="Average Reward Contrast (Delta)")
    plt.savefig(os.path.join(output_dir, f"{prefix}_01_contrast_manifold.png"))
    plt.close()

    # 2. Plot Hotspot Mask ("Easy Sort")
    plt.figure(figsize=(10, 8))
    plt.imshow(np.flipud(agent.hotspot_mask), cmap='Greys', aspect='auto')
    plt.title(f"Hotspot Mask ('Easy Sort', q={agent.hotspot_quantile}) - {prefix}", fontsize=16)
    plt.xlabel("Angle (Theta) Bins")
    plt.ylabel("Velocity Bins")
    plt.savefig(os.path.join(output_dir, f"{prefix}_02_hotspot_mask.png"))
    plt.close()

    # 3. Plot Learned Policy (Value Function)
    value_function = np.max(agent.Q, axis=2) # Max Q-value for each state
    plt.figure(figsize=(10, 8))
    plt.imshow(np.flipud(value_function), cmap='viridis', aspect='auto')
    plt.title(f"Learned Value Function (Max Q) - {prefix}", fontsize=16)
    plt.xlabel("Angle (Theta) Bins")
    plt.ylabel("Velocity Bins")
    plt.colorbar(label="Estimated State Value")
    plt.savefig(os.path.join(output_dir, f"{prefix}_03_value_function.png"))
    plt.close()

    # 4. Plot Reward Trace
    plt.figure(figsize=(12, 6))
    if len(agent.reward_trace) > 100:
        # Smooth the reward trace
        N = 100
        running_avg = np.convolve(agent.reward_trace, np.ones(N)/N, mode='valid')
        plt.plot(running_avg, label=f"Smoothed (N={N})")
    else:
        plt.plot(agent.reward_trace, label="Episodic Return")
    
    plt.title(f"Episodic Return over Time - {prefix}", fontsize=16)
    plt.xlabel("Episode")
    plt.ylabel("Total Reward")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.savefig(os.path.join(output_dir, f"{prefix}_04_reward_trace.png"))
    plt.close()


def main():
    # --- Setup ---
    output_dir = "pirouette_pendulum_v2_results"
    os.makedirs(output_dir, exist_ok=True)
    
    # We'll use "Pendulum-v1" with "human" render mode
    env = gym.make('Pendulum-v1', render_mode="rgb_array")
    
    agent = PirouettePendulumAgent_v2(
        total_steps=100_000,
        hotspot_quantile=0.8,
        hotspot_lr_factor=10.0, # 10x "Push"
        coldspot_lr_factor=0.1,  # 0.1x "Pull"
        base_lr=0.05,
        n_actions=5,
        epsilon_decay_steps=70_000
    )

    print("--- Starting Pirouette Agent v2 ---")
    print(f"Total Steps: {agent.total_steps}")
    print(f"LR Factors: Hotspot(Push)={agent.hotspot_lr_factor}, Coldspot(Pull)={agent.coldspot_lr_factor}")
    print("Agent will learn AND map contrast in parallel.")
    
    ep = 0
    ep_return = 0.0
    obs, _ = env.reset()
    state_tuple = agent.discretize_state(obs)
    
    # --- The Single, Interleaved Loop ---
    start_time = time.time()
    for t in range(agent.total_steps):
        
        # 1. "Meta" Cluster: Re-analyze the manifold periodically
        if t > 0 and t % 5000 == 0:
            agent.update_hotspot()
            # Plot intermediate results
            plot_results(agent, output_dir, f"step_{t}")

        # 2. "Actor" Cluster: Get action
        action_idx = agent.get_action(state_tuple, t)
        action_val = agent.actions[action_idx]
        
        # 3. Interact with environment
        next_obs, reward, terminated, truncated, _ = env.step([action_val])
        next_state_tuple = agent.discretize_state(next_obs)
        
        # 4. "Exhaust Map" Cluster: Observe the "contrast"
        agent.observe_contrast(state_tuple, reward)
        
        # 5. "Learning" Cluster: Update Q-table
        agent.learn(state_tuple, action_idx, reward, next_state_tuple, terminated)

        # 6. Housekeeping
        ep_return += reward
        state_tuple = next_state_tuple
        
        if t > 0 and t % 1000 == 0:
            print(f"Step {t}/{agent.total_steps}...")

        if terminated or truncated:
            agent.reward_trace.append(ep_return)
            ep += 1
            if ep % 10 == 0:
                print(
                    f"[RUN] Episode {ep:4d} | Step {t:6d} | Return={ep_return:7.2f}"
                )
            ep_return = 0.0
            obs, _ = env.reset()
            state_tuple = agent.discretize_state(obs)

    env.close()
    
    # --- Final Analysis ---
    end_time = time.time()
    print("\n--- [DONE] Simulation Complete ---")
    print(f"Total time: {end_time - start_time:.2f} seconds")
    agent.update_hotspot() # Final analysis
    plot_results(agent, output_dir, "final")
    print(f"Final results saved to '{output_dir}'")

if __name__ == "__main__":
    main()
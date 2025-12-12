"""
COMPARATIVE EXPERIMENT: Vanilla DQN vs Boundary Rider

Does fractal boundary learning actually help? Let's find out.
"""

import numpy as np
from collections import deque
import matplotlib.pyplot as plt
import time


class SimpleCartPole:
    """Minimal CartPole implementation."""
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


class SimpleNetwork:
    """Simple 2-layer network."""
    def __init__(self, input_dim, output_dim, hidden_dim=128, lr=0.01):
        self.W1 = np.random.randn(input_dim, hidden_dim) * np.sqrt(2.0 / input_dim)
        self.b1 = np.zeros(hidden_dim)
        self.W2 = np.random.randn(hidden_dim, hidden_dim) * np.sqrt(2.0 / hidden_dim)
        self.b2 = np.zeros(hidden_dim)
        self.W3 = np.random.randn(hidden_dim, output_dim) * np.sqrt(2.0 / hidden_dim)
        self.b3 = np.zeros(output_dim)
        self.lr = lr
        
    def forward(self, x):
        self.x = x
        self.z1 = x @ self.W1 + self.b1
        self.a1 = np.maximum(0, self.z1)
        self.z2 = self.a1 @ self.W2 + self.b2
        self.a2 = np.maximum(0, self.z2)
        self.z3 = self.a2 @ self.W3 + self.b3
        return self.z3
    
    def backward(self, grad_output):
        # Gradient clipping for stability
        grad_output = np.clip(grad_output, -1.0, 1.0)
        
        dz3 = grad_output
        dW3 = self.a2.T @ dz3
        db3 = np.sum(dz3, axis=0)
        
        da2 = dz3 @ self.W3.T
        dz2 = da2 * (self.z2 > 0)
        dW2 = self.a1.T @ dz2
        db2 = np.sum(dz2, axis=0)
        
        da1 = dz2 @ self.W2.T
        dz1 = da1 * (self.z1 > 0)
        dW1 = self.x.T @ dz1
        db1 = np.sum(dz1, axis=0)
        
        # Gradient clipping
        dW3 = np.clip(dW3, -1.0, 1.0)
        dW2 = np.clip(dW2, -1.0, 1.0)
        dW1 = np.clip(dW1, -1.0, 1.0)
        
        self.W3 -= self.lr * dW3
        self.b3 -= self.lr * db3
        self.W2 -= self.lr * dW2
        self.b2 -= self.lr * db2
        self.W1 -= self.lr * dW1
        self.b1 -= self.lr * db1
    
    def copy_from(self, other):
        self.W1 = other.W1.copy()
        self.b1 = other.b1.copy()
        self.W2 = other.W2.copy()
        self.b2 = other.b2.copy()
        self.W3 = other.W3.copy()
        self.b3 = other.b3.copy()


class ReplayBuffer:
    """Standard replay buffer."""
    def __init__(self, capacity=10000):
        self.buffer = deque(maxlen=capacity)
        
    def push(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))
        
    def sample(self, batch_size):
        if len(self.buffer) < batch_size:
            return None
        indices = np.random.choice(len(self.buffer), batch_size, replace=False)
        batch = [self.buffer[i] for i in indices]
        states, actions, rewards, next_states, dones = zip(*batch)
        return (np.array(states), np.array(actions), np.array(rewards),
                np.array(next_states), np.array(dones))
    
    def __len__(self):
        return len(self.buffer)


class PrioritizedReplayBuffer:
    """Boundary-prioritized replay buffer."""
    def __init__(self, capacity=10000, alpha=2.0):
        self.capacity = capacity
        self.buffer = []
        self.priorities = []
        self.alpha = alpha
        self.position = 0
        
    def push(self, state, action, reward, next_state, done, priority=1.0):
        # priority = boundary signal
        priority = 1.0 + self.alpha * (priority ** 2)
        
        if len(self.buffer) < self.capacity:
            self.buffer.append((state, action, reward, next_state, done))
            self.priorities.append(priority)
        else:
            self.buffer[self.position] = (state, action, reward, next_state, done)
            self.priorities[self.position] = priority
        self.position = (self.position + 1) % self.capacity
        
    def sample(self, batch_size):
        if len(self.buffer) < batch_size:
            return None
        priorities = np.array(self.priorities[:len(self.buffer)])
        probs = priorities / priorities.sum()
        indices = np.random.choice(len(self.buffer), batch_size, p=probs, replace=False)
        batch = [self.buffer[i] for i in indices]
        states, actions, rewards, next_states, dones = zip(*batch)
        return (np.array(states), np.array(actions), np.array(rewards),
                np.array(next_states), np.array(dones))
    
    def __len__(self):
        return len(self.buffer)


class VanillaDQN:
    """Standard DQN agent."""
    def __init__(self, state_dim, action_dim, lr=0.01, gamma=0.99):
        self.action_dim = action_dim
        self.gamma = gamma
        self.q_network = SimpleNetwork(state_dim, action_dim, hidden_dim=128, lr=lr)
        self.target_network = SimpleNetwork(state_dim, action_dim, hidden_dim=128, lr=lr)
        self.target_network.copy_from(self.q_network)
        self.memory = ReplayBuffer(capacity=50000)
        self.losses = []
        
    def select_action(self, state, epsilon):
        if np.random.random() < epsilon:
            return np.random.randint(self.action_dim)
        q_values = self.q_network.forward(state.reshape(1, -1))[0]
        return np.argmax(q_values)
    
    def train_step(self, batch_size=64):
        batch = self.memory.sample(batch_size)
        if batch is None:
            return None
        states, actions, rewards, next_states, dones = batch
        
        current_q = self.q_network.forward(states)
        current_q_actions = current_q[np.arange(batch_size), actions]
        
        next_q = self.target_network.forward(next_states)
        next_q_max = np.max(next_q, axis=1)
        target_q = rewards + self.gamma * next_q_max * (1 - dones)
        
        td_error = current_q_actions - target_q
        loss = np.mean(td_error ** 2)
        
        grad_q = np.zeros_like(current_q)
        grad_q[np.arange(batch_size), actions] = 2 * td_error / batch_size
        self.q_network.backward(grad_q)
        
        self.losses.append(loss)
        return loss
    
    def update_target_network(self):
        self.target_network.copy_from(self.q_network)


class BoundaryDQN:
    """Boundary-aware DQN agent."""
    def __init__(self, state_dim, action_dim, lr=0.01, gamma=0.99):
        self.action_dim = action_dim
        self.gamma = gamma
        self.q_network = SimpleNetwork(state_dim, action_dim, hidden_dim=128, lr=lr)
        self.target_network = SimpleNetwork(state_dim, action_dim, hidden_dim=128, lr=lr)
        self.target_network.copy_from(self.q_network)
        self.memory = PrioritizedReplayBuffer(capacity=50000, alpha=2.0)
        self.losses = []
        self.boundary_signals = []
        
    def compute_boundary_signal(self, q_values):
        """Compute boundary signal from Q-value variance."""
        q_var = np.var(q_values)
        q_mean = np.mean(np.abs(q_values))
        return q_var / (q_mean + 1e-6)
    
    def select_action(self, state, epsilon, boost=0.3):
        state_input = state.reshape(1, -1)
        q_values = self.q_network.forward(state_input)[0]
        boundary_signal = self.compute_boundary_signal(q_values)
        self.boundary_signals.append(boundary_signal)
        
        # Boost exploration at boundaries
        effective_epsilon = epsilon + boost * boundary_signal
        effective_epsilon = min(effective_epsilon, 1.0)
        
        if np.random.random() < effective_epsilon:
            return np.random.randint(self.action_dim), boundary_signal
        return np.argmax(q_values), boundary_signal
    
    def train_step(self, batch_size=64):
        batch = self.memory.sample(batch_size)
        if batch is None:
            return None
        states, actions, rewards, next_states, dones = batch
        
        current_q = self.q_network.forward(states)
        current_q_actions = current_q[np.arange(batch_size), actions]
        
        next_q = self.target_network.forward(next_states)
        next_q_max = np.max(next_q, axis=1)
        target_q = rewards + self.gamma * next_q_max * (1 - dones)
        
        td_error = current_q_actions - target_q
        loss = np.mean(td_error ** 2)
        
        grad_q = np.zeros_like(current_q)
        grad_q[np.arange(batch_size), actions] = 2 * td_error / batch_size
        self.q_network.backward(grad_q)
        
        self.losses.append(loss)
        return loss
    
    def update_target_network(self):
        self.target_network.copy_from(self.q_network)


def run_experiment(agent_type, episodes=300, name="Agent"):
    """Run a training experiment."""
    env = SimpleCartPole()
    state_dim = 4
    action_dim = 2
    
    if agent_type == "vanilla":
        agent = VanillaDQN(state_dim, action_dim, lr=0.01)
    else:
        agent = BoundaryDQN(state_dim, action_dim, lr=0.01)
    
    epsilon = 1.0
    epsilon_end = 0.01
    epsilon_decay = 0.995
    target_update_freq = 10
    
    episode_rewards = []
    episode_boundaries = [] if agent_type == "boundary" else None
    
    print(f"\n{name}: Training for {episodes} episodes...")
    t0 = time.time()
    
    for episode in range(episodes):
        state = env.reset()
        episode_reward = 0
        ep_boundaries = []
        done = False
        
        while not done:
            if agent_type == "vanilla":
                action = agent.select_action(state, epsilon)
                agent.memory.push(state, action, 0, state, False)  # placeholder
            else:
                action, boundary_signal = agent.select_action(state, epsilon, boost=0.3)
                ep_boundaries.append(boundary_signal)
            
            next_state, reward, done = env.step(action)
            
            if agent_type == "vanilla":
                agent.memory.push(state, action, reward, next_state, done)
            else:
                agent.memory.push(state, action, reward, next_state, done, 
                                 ep_boundaries[-1] if ep_boundaries else 0)
            
            if len(agent.memory) > 64:
                agent.train_step(batch_size=64)
            
            state = next_state
            episode_reward += reward
        
        if episode % target_update_freq == 0:
            agent.update_target_network()
        
        epsilon = max(epsilon_end, epsilon * epsilon_decay)
        episode_rewards.append(episode_reward)
        
        if agent_type == "boundary" and ep_boundaries:
            episode_boundaries.append(np.mean(ep_boundaries))
        
        if episode % 50 == 0:
            avg_reward = np.mean(episode_rewards[-50:]) if len(episode_rewards) >= 50 else np.mean(episode_rewards)
            print(f"  Episode {episode:3d} | Reward: {episode_reward:6.1f} | Avg(50): {avg_reward:6.1f}")
    
    dt = time.time() - t0
    print(f"  Complete in {dt:.1f}s | Final avg: {np.mean(episode_rewards[-50:]):.1f}")
    
    return episode_rewards, episode_boundaries, agent


def main():
    """Run comparative experiment."""
    print("="*70)
    print("COMPARATIVE EXPERIMENT: Vanilla DQN vs Boundary Rider")
    print("="*70)
    print("\nTesting if fractal boundary learning provides an advantage...")
    
    np.random.seed(42)
    vanilla_rewards, _, vanilla_agent = run_experiment("vanilla", episodes=300, name="Vanilla DQN")
    
    np.random.seed(42)
    boundary_rewards, boundary_signals, boundary_agent = run_experiment("boundary", episodes=300, name="Boundary Rider")
    
    # Visualization
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    window = 20
    
    # Raw rewards
    ax1 = axes[0, 0]
    ax1.plot(vanilla_rewards, alpha=0.3, color='blue', label='Vanilla DQN')
    ax1.plot(boundary_rewards, alpha=0.3, color='red', label='Boundary Rider')
    ax1.set_xlabel('Episode')
    ax1.set_ylabel('Reward')
    ax1.set_title('Learning Curves (Raw)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Smoothed rewards
    ax2 = axes[0, 1]
    if len(vanilla_rewards) > window:
        smooth_vanilla = np.convolve(vanilla_rewards, np.ones(window)/window, mode='valid')
        smooth_boundary = np.convolve(boundary_rewards, np.ones(window)/window, mode='valid')
        ax2.plot(range(window-1, len(vanilla_rewards)), smooth_vanilla, 
                 color='blue', linewidth=2, label='Vanilla DQN')
        ax2.plot(range(window-1, len(boundary_rewards)), smooth_boundary, 
                 color='red', linewidth=2, label='Boundary Rider')
    ax2.set_xlabel('Episode')
    ax2.set_ylabel('Reward (smoothed)')
    ax2.set_title(f'Learning Curves (MA-{window})')
    ax2.axhline(y=200, color='green', linestyle='--', alpha=0.5)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Boundary signal over time
    ax3 = axes[1, 0]
    if boundary_signals:
        ax3.plot(boundary_signals, alpha=0.6, color='purple')
        if len(boundary_signals) > window:
            smooth_boundary_sig = np.convolve(boundary_signals, np.ones(window)/window, mode='valid')
            ax3.plot(range(window-1, len(boundary_signals)), smooth_boundary_sig, 
                     color='darkviolet', linewidth=2)
    ax3.set_xlabel('Episode')
    ax3.set_ylabel('Boundary Signal')
    ax3.set_title('Boundary Rider: Decision Uncertainty')
    ax3.grid(True, alpha=0.3)
    
    # Comparison statistics
    ax4 = axes[1, 1]
    bins = np.linspace(0, max(max(vanilla_rewards), max(boundary_rewards)), 30)
    ax4.hist(vanilla_rewards, bins=bins, alpha=0.5, color='blue', label='Vanilla DQN')
    ax4.hist(boundary_rewards, bins=bins, alpha=0.5, color='red', label='Boundary Rider')
    ax4.set_xlabel('Episode Reward')
    ax4.set_ylabel('Frequency')
    ax4.set_title('Reward Distribution')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/mnt/user-data/outputs/comparative_experiment.png', dpi=150, bbox_inches='tight')
    
    print("\n" + "="*70)
    print("RESULTS")
    print("="*70)
    print(f"Vanilla DQN:")
    print(f"  Final avg (last 50): {np.mean(vanilla_rewards[-50:]):.1f}")
    print(f"  Peak reward: {np.max(vanilla_rewards):.1f}")
    print(f"  Episodes > 200: {np.sum(np.array(vanilla_rewards) > 200)}")
    print(f"\nBoundary Rider:")
    print(f"  Final avg (last 50): {np.mean(boundary_rewards[-50:]):.1f}")
    print(f"  Peak reward: {np.max(boundary_rewards):.1f}")
    print(f"  Episodes > 200: {np.sum(np.array(boundary_rewards) > 200)}")
    
    improvement = (np.mean(boundary_rewards[-50:]) - np.mean(vanilla_rewards[-50:])) / np.mean(vanilla_rewards[-50:]) * 100
    print(f"\nBoundary Rider improvement: {improvement:+.1f}%")
    print("="*70)
    
    plt.show()


if __name__ == "__main__":
    main()

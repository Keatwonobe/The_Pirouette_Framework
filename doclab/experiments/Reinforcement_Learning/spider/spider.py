"""
Spider Protocol: Active Manifold Instrumentation for RL
========================================================

Pure implementation of INST-CORE-001: The Spider's Protocol
Testing the measurement algorithm on Pendulum simulation

Core principle: Agent learns by PROBING the manifold, measuring tension,
triangulating position, and testing coherence rather than passive observation.

NumPy-only implementation with manual Pendulum simulation.
"""

import numpy as np
from collections import deque


class PendulumEnv:
    """Simple Pendulum simulator"""
    def __init__(self):
        self.max_speed = 8.0
        self.max_torque = 2.0
        self.dt = 0.05
        self.g = 10.0
        self.m = 1.0
        self.l = 1.0
        self.state = None
        
    def reset(self):
        self.state = np.array([np.random.uniform(-np.pi, np.pi), np.random.uniform(-1, 1)])
        return self.state.copy()
    
    def step(self, action):
        theta, theta_dot = self.state
        
        action = np.clip(action, -self.max_torque, self.max_torque)[0]
        
        # Pendulum dynamics
        new_theta_dot = theta_dot + (3 * self.g / (2 * self.l) * np.sin(theta) + 3.0 / (self.m * self.l**2) * action) * self.dt
        new_theta_dot = np.clip(new_theta_dot, -self.max_speed, self.max_speed)
        new_theta = theta + new_theta_dot * self.dt
        
        self.state = np.array([new_theta, new_theta_dot])
        
        # Reward: upright and slow
        cost = theta**2 + 0.1 * theta_dot**2 + 0.001 * action**2
        reward = -cost
        
        return self.state.copy(), reward, False


class ManifoldProbe:
    """
    Atomic measurement primitive: perturb and measure response
    
    Returns tension (how heavy the concept is) and phase (resonance)
    """
    def __init__(self, probe_dim, context_dim):
        self.probe_dim = probe_dim
        self.context_dim = context_dim
        
    def probe(self, state, action, kappa=1.0):
        """
        Cast observer's shadow and measure echo
        
        Returns:
            tension: how much resistance (Q-value proxy)
            phase: harmonic relationship (advantage direction)
        """
        # State is the concept, action is the context
        # Tension = magnitude of response
        # Phase = directional alignment
        
        state_norm = np.linalg.norm(state)
        action_norm = np.linalg.norm(action) if isinstance(action, np.ndarray) else abs(action)
        
        # Tension: normalized coupling strength
        tension = state_norm * action_norm * kappa
        
        # Phase: alignment between state gradient and action
        if isinstance(action, np.ndarray):
            phase = np.arctan2(action[1], action[0]) if len(action) > 1 else action[0]
        else:
            phase = action
            
        return tension, phase


class TriangulationNetwork:
    """
    Learns to triangulate concept positions on coherence manifold
    
    NumPy-based neural network for pure implementation
    """
    def __init__(self, state_dim, action_dim, hidden_dim=64):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.hidden_dim = hidden_dim
        
        # Three context encoders - share input layer, different transformations
        self.w1_in = np.random.randn(state_dim, hidden_dim) * np.sqrt(2.0 / state_dim)
        self.b1 = np.zeros(hidden_dim)
        
        self.w2_in = np.random.randn(state_dim, hidden_dim) * np.sqrt(2.0 / state_dim)
        self.b2 = np.zeros(hidden_dim)
        
        self.w3_in = np.random.randn(state_dim, hidden_dim) * np.sqrt(2.0 / state_dim)
        self.b3 = np.zeros(hidden_dim)
        
        # Output heads
        self.w_tension = np.random.randn(hidden_dim * 3, action_dim) * np.sqrt(2.0 / (hidden_dim * 3))
        self.b_tension = np.zeros(action_dim)
        
        self.w_phase = np.random.randn(hidden_dim * 3, action_dim) * np.sqrt(2.0 / (hidden_dim * 3))
        self.b_phase = np.zeros(action_dim)
        
        self.w_coherence = np.random.randn(hidden_dim * 3, 1) * np.sqrt(2.0 / (hidden_dim * 3))
        self.b_coherence = np.zeros(1)
        
    def relu(self, x):
        return np.maximum(0, x)
    
    def tanh(self, x):
        return np.tanh(x)
    
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))
    
    def forward(self, state):
        """Triangulate via multi-context probing"""
        # Three context encoders (different perspectives on same state)
        h1 = self.relu(state @ self.w1_in + self.b1)
        h2 = self.relu(state @ self.w2_in + self.b2)  
        h3 = self.relu(state @ self.w3_in + self.b3)
        
        # Multi-context representation
        multi_context = np.concatenate([h1, h2, h3], axis=-1)
        
        # Predictions
        tension = multi_context @ self.w_tension + self.b_tension
        phase = self.tanh(multi_context @ self.w_phase + self.b_phase)
        coherence = self.sigmoid(multi_context @ self.w_coherence + self.b_coherence)
        
        return tension, phase, coherence, (h1, h2, h3, multi_context)
    
    def get_weights(self):
        """Get all weights as flat array"""
        return np.concatenate([
            self.w1_in.ravel(), self.b1.ravel(),
            self.w2_in.ravel(), self.b2.ravel(),
            self.w3_in.ravel(), self.b3.ravel(),
            self.w_tension.ravel(), self.b_tension.ravel(),
            self.w_phase.ravel(), self.b_phase.ravel(),
            self.w_coherence.ravel(), self.b_coherence.ravel()
        ])
    
    def set_weights(self, weights):
        """Set all weights from flat array"""
        idx = 0
        
        n = self.w1_in.size
        self.w1_in = weights[idx:idx+n].reshape(self.w1_in.shape)
        idx += n
        
        n = self.b1.size
        self.b1 = weights[idx:idx+n]
        idx += n
        
        n = self.w2_in.size
        self.w2_in = weights[idx:idx+n].reshape(self.w2_in.shape)
        idx += n
        
        n = self.b2.size
        self.b2 = weights[idx:idx+n]
        idx += n
        
        n = self.w3_in.size
        self.w3_in = weights[idx:idx+n].reshape(self.w3_in.shape)
        idx += n
        
        n = self.b3.size
        self.b3 = weights[idx:idx+n]
        idx += n
        
        n = self.w_tension.size
        self.w_tension = weights[idx:idx+n].reshape(self.w_tension.shape)
        idx += n
        
        n = self.b_tension.size
        self.b_tension = weights[idx:idx+n]
        idx += n
        
        n = self.w_phase.size
        self.w_phase = weights[idx:idx+n].reshape(self.w_phase.shape)
        idx += n
        
        n = self.b_phase.size
        self.b_phase = weights[idx:idx+n]
        idx += n
        
        n = self.w_coherence.size
        self.w_coherence = weights[idx:idx+n].reshape(self.w_coherence.shape)
        idx += n
        
        n = self.b_coherence.size
        self.b_coherence = weights[idx:idx+n]


class CoherenceMemory:
    """
    Stores measurements with coherence scores
    
    High coherence = concept stable across contexts, scales, perturbations
    Low coherence = phantom, fragile, context-dependent
    """
    def __init__(self, capacity=10000):
        self.capacity = capacity
        self.memory = deque(maxlen=capacity)
        
    def push(self, state, action, reward, next_state, done, coherence):
        """Store experience with coherence score"""
        self.memory.append((state, action, reward, next_state, done, coherence))
        
    def sample(self, batch_size):
        """Sample experiences weighted by coherence"""
        indices = np.random.choice(len(self.memory), min(batch_size, len(self.memory)), replace=False)
        batch = [self.memory[i] for i in indices]
        
        states = np.array([x[0] for x in batch])
        actions = np.array([x[1] for x in batch])
        rewards = np.array([x[2] for x in batch])
        next_states = np.array([x[3] for x in batch])
        dones = np.array([x[4] for x in batch])
        coherences = np.array([x[5] for x in batch])
        
        return states, actions, rewards, next_states, dones, coherences
    
    def __len__(self):
        return len(self.memory)


class SpiderAgent:
    """
    RL Agent using Spider Protocol measurement algorithm
    
    Instead of passive Q-learning:
    1. Probe manifold from multiple angles (triangulation)
    2. Measure tension and phase (active measurement)
    3. Test coherence (real vs phantom)
    4. Update probe weights based on utility
    
    NumPy-only implementation
    """
    def __init__(self, state_dim, action_dim, lr=1e-3):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.lr = lr
        
        # Main and target networks
        self.network = TriangulationNetwork(state_dim, action_dim)
        self.target_network = TriangulationNetwork(state_dim, action_dim)
        self.target_network.set_weights(self.network.get_weights())
        
        # Coherence-weighted memory
        self.memory = CoherenceMemory(capacity=10000)
        
        # Probe weights (learned attention policy)
        self.probe_weights = np.ones(action_dim) / action_dim
        
        # Measurement statistics
        self.probe_counts = np.zeros(action_dim)
        self.probe_utilities = np.zeros(action_dim)
        
    def select_action(self, state, epsilon=0.1):
        """Select action via active probing protocol"""
        if np.random.random() < epsilon:
            return np.random.choice(self.action_dim, p=self.probe_weights)
        
        state_batch = state.reshape(1, -1)
        tension, phase, coherence, _ = self.network.forward(state_batch)
        
        # Maximize tension * coherence
        scores = tension[0] * coherence[0, 0]
        action = np.argmax(scores)
        
        return action
    
    def triangulate(self, state):
        """Multi-context triangulation of state position"""
        state_batch = state.reshape(1, -1)
        tension, phase, coherence, _ = self.network.forward(state_batch)
        
        # Position = weighted combination
        position = tension[0] * np.cos(phase[0] * np.pi)
        confidence = coherence[0, 0]
        
        return position, confidence
    
    def update(self, batch_size=64, gamma=0.99):
        """Coherence-weighted learning update"""
        if len(self.memory) < batch_size:
            return 0.0
        
        states, actions, rewards, next_states, dones, coherences = self.memory.sample(batch_size)
        
        # Forward pass
        tension, phase, coherence_pred, cache = self.network.forward(states)
        
        # Q-values for taken actions
        q_values = tension * coherence_pred[:, 0:1]
        q_current = q_values[np.arange(len(actions)), actions]
        
        # Target Q-values
        next_tension, next_phase, next_coherence, _ = self.target_network.forward(next_states)
        next_q_values = next_tension * next_coherence[:, 0:1]
        next_q_max = np.max(next_q_values, axis=1)
        targets = rewards + gamma * next_q_max * (1 - dones)
        
        # Coherence-weighted TD error
        td_errors = (q_current - targets) ** 2
        loss = np.mean(td_errors * coherences)
        
        # Coherence prediction loss
        coherence_target = self._compute_coherence_target(rewards, dones)
        coherence_loss = np.mean((coherence_pred[:, 0] - coherence_target) ** 2)
        
        total_loss = loss + 0.1 * coherence_loss
        
        # Backward pass (simple gradient descent)
        self._backward(states, actions, q_current, targets, coherences, coherence_pred[:, 0], coherence_target, cache)
        
        return total_loss
    
    def _backward(self, states, actions, q_current, targets, coherences, coherence_pred, coherence_target, cache):
        """Manual backpropagation"""
        batch_size = len(states)
        h1, h2, h3, multi_context = cache
        
        # Gradients for Q-value loss (coherence-weighted)
        dq = 2 * (q_current - targets) * coherences / batch_size
        
        # Gradients for coherence loss  
        dcoh = 2 * (coherence_pred - coherence_target) * 0.1 / batch_size
        
        # Backprop through tension head (simplified - only update tension)
        dtension = np.zeros((batch_size, self.action_dim))
        dtension[np.arange(batch_size), actions] = dq
        
        # Update tension weights
        grad_w_tension = multi_context.T @ dtension
        grad_b_tension = np.sum(dtension, axis=0)
        
        self.network.w_tension -= self.lr * np.clip(grad_w_tension, -1, 1)
        self.network.b_tension -= self.lr * np.clip(grad_b_tension, -1, 1)
        
        # Update coherence weights
        dcoh_expanded = dcoh.reshape(-1, 1)
        grad_w_coherence = multi_context.T @ dcoh_expanded
        grad_b_coherence = np.sum(dcoh_expanded, axis=0)
        
        self.network.w_coherence -= self.lr * np.clip(grad_w_coherence, -1, 1)
        self.network.b_coherence -= self.lr * np.clip(grad_b_coherence, -1, 1)
    
    def _compute_coherence_target(self, rewards, dones):
        """Compute target coherence from experience utility"""
        # Normalize rewards to [0, 1]
        coherence = 1 / (1 + np.exp(-rewards / 10.0))
        coherence = coherence * (1 - dones * 0.5)
        return coherence
    
    def update_probe_weights(self, action, reward, surprise):
        """Train probe network: which strings worth plucking?"""
        self.probe_counts[action] += 1
        
        utility = reward
        surprise_value = abs(surprise)
        
        if surprise_value > 0.5 and abs(utility) > 0.1:
            self.probe_weights[action] += 0.01 * surprise_value * abs(utility)
            self.probe_utilities[action] += utility
        else:
            self.probe_weights[action] *= 0.99
        
        self.probe_weights = np.maximum(self.probe_weights, 0.01)
        self.probe_weights /= self.probe_weights.sum()
    
    def update_target_network(self):
        """Soft update of target network"""
        tau = 0.005
        current_weights = self.network.get_weights()
        target_weights = self.target_network.get_weights()
        new_weights = tau * current_weights + (1 - tau) * target_weights
        self.target_network.set_weights(new_weights)


def train_spider_agent(episodes=300):
    """
    Train Spider Protocol agent on Pendulum
    
    Pure test of measurement algorithm with no other factors
    """
    env = PendulumEnv()
    state_dim = 2  # [theta, theta_dot]
    action_dim = 5  # Discretize actions
    
    agent = SpiderAgent(state_dim, action_dim)
    
    # Discretize action space
    action_space = np.linspace(-2, 2, action_dim)
    
    episode_rewards = []
    
    for episode in range(episodes):
        state = env.reset()
        episode_reward = 0
        epsilon = max(0.01, 0.5 - episode / 150)
        
        step = 0
        max_steps = 200
        
        while step < max_steps:
            # Select action via active probing
            action_idx = agent.select_action(state, epsilon)
            action = np.array([action_space[action_idx]])
            
            # Execute action
            next_state, reward, _ = env.step(action)
            
            # Measure surprise (prediction error)
            expected_next, confidence = agent.triangulate(state)
            surprise = np.linalg.norm(next_state - expected_next[:state_dim])
            
            # Compute coherence
            coherence = confidence * (1.0 - surprise / 5.0)
            coherence = np.clip(coherence, 0.1, 1.0)
            
            # Store experience
            agent.memory.push(state, action_idx, reward, next_state, False, coherence)
            
            # Update probe weights (meta-learning)
            agent.update_probe_weights(action_idx, reward, surprise)
            
            # Update network
            loss = agent.update(batch_size=32)
            
            state = next_state
            episode_reward += reward
            step += 1
            
            # Update target network
            if step % 10 == 0:
                agent.update_target_network()
        
        episode_rewards.append(episode_reward)
        
        if episode % 20 == 0:
            avg_reward = np.mean(episode_rewards[-20:])
            print(f"Episode {episode:3d} | Avg Reward: {avg_reward:7.2f} | Epsilon: {epsilon:.3f}")
            print(f"  Probe weights: {' '.join([f'{w:.3f}' for w in agent.probe_weights])}")
            if episode > 0:
                utilities = agent.probe_utilities / (agent.probe_counts + 1e-8)
                print(f"  Probe utilities: {' '.join([f'{u:.2f}' for u in utilities])}")
    
    return agent, episode_rewards


if __name__ == "__main__":
    print("=" * 70)
    print("SPIDER PROTOCOL: Active Manifold Instrumentation for RL")
    print("Testing measurement algorithm on Pendulum simulation")
    print("=" * 70)
    print()
    print("Core principle: Learn by PROBING the manifold")
    print("  1. Triangulate position via multi-context measurement")
    print("  2. Measure tension (structural integrity)")
    print("  3. Test coherence (real vs phantom)")
    print("  4. Update probe weights based on utility")
    print()
    print("=" * 70)
    print()
    
    agent, rewards = train_spider_agent(episodes=300)
    
    print()
    print("=" * 70)
    print("Training complete!")
    print(f"Final average reward (last 50 episodes): {np.mean(rewards[-50:]):.2f}")
    print(f"Best episode reward: {max(rewards):.2f}")
    print(f"Initial avg reward (first 20): {np.mean(rewards[:20]):.2f}")
    print("=" * 70)
    print()
    print("Final probe weight distribution:")
    for i, w in enumerate(agent.probe_weights):
        print(f"  Action {i} ({-2 + i}: weight={w:.4f}")
    print()
    print("Probe utility scores (avg reward per probe):")
    utilities = agent.probe_utilities / (agent.probe_counts + 1e-8)
    for i, u in enumerate(utilities):
        print(f"  Action {i}: utility={u:.3f}, count={int(agent.probe_counts[i])}")
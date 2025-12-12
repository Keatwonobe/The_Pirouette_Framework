"""
Spider Protocol on Pendulum-v1
==============================

A lightweight "Spider" agent that probes the Pendulum manifold using
discrete torques and learns via REINFORCE (policy gradient) with:

- Advantage normalization ("tension" stabilization)
- Temperature annealing (probing -> coherence)
- Checkpointing so you can resume training runs

Dependencies:
    pip install gymnasium    # preferred
    # or pip install gym     # fallback

Run:
    python spider_pendulum_runner.py
"""

import os
import numpy as np

# --- Try gymnasium first, then fall back to gym --------------------------------
try:
    import gymnasium as gym
    GYMNASIUM_API = True
except ImportError:
    import gym
    GYMNASIUM_API = False


# ------------------------------------------------------------------------------
# Utility functions: env wrappers, discounting, softmax
# ------------------------------------------------------------------------------

def make_pendulum_env():
    """Create Pendulum environment with version fallback."""
    for env_id in ["Pendulum-v1", "Pendulum-v0"]:
        try:
            env = gym.make(env_id)
            print(f"[ENV] Using {env_id}")
            return env
        except Exception:
            continue
    raise RuntimeError("Could not create Pendulum environment (v1 or v0).")


def env_reset(env):
    if GYMNASIUM_API:
        obs, info = env.reset()
        return obs
    else:
        obs = env.reset()
        return obs


def env_step(env, action):
    """
    Step environment, supporting both gymnasium and gym APIs.
    Returns (obs, reward, done).
    """
    step_out = env.step(action)
    if GYMNASIUM_API:
        obs, reward, terminated, truncated, info = step_out
        done = terminated or truncated
    else:
        obs, reward, done, info = step_out
    return obs, reward, done


def discount_returns(rewards, gamma):
    """
    Compute discounted returns G_t from a sequence of rewards.
    """
    T = len(rewards)
    returns = np.zeros(T, dtype=np.float32)
    G = 0.0
    for t in reversed(range(T)):
        G = rewards[t] + gamma * G
        returns[t] = G
    return returns


def softmax(x):
    """
    Numerically stable softmax.
    """
    x = x - np.max(x)
    e = np.exp(x)
    return e / (np.sum(e) + 1e-8)


# ------------------------------------------------------------------------------
# Spider Policy: Linear logits over discretized actions
# ------------------------------------------------------------------------------

class SpiderPolicy:
    """
    Simple "Spider" head: linear logits over discretized actions.

    π(a | s) = softmax( (W s + b) / T )

    where:
        s: state vector (Pendulum observation)
        a: discrete torque index
        W: (n_actions, state_dim)
        b: (n_actions,)
        T: temperature controlling exploration vs coherence.

    Training uses REINFORCE:
        Δθ ∝ A_t * ∇_θ log π(a_t | s_t)
    """

    def __init__(self, state_dim, n_actions, action_values, lr=1e-2, init_scale=0.1):
        self.state_dim = state_dim
        self.n_actions = n_actions
        self.action_values = np.array(action_values, dtype=np.float32)

        # Policy parameters
        self.W = np.random.randn(n_actions, state_dim) * init_scale
        self.b = np.zeros(n_actions, dtype=np.float32)

        self.lr = lr

        # Moving baseline for returns (coherence reference)
        self.baseline = 0.0
        self.baseline_momentum = 0.99

        # Temperature (for probing)
        self.temperature = 1.0  # start fairly exploratory

    def choose_action(self, state, explore=True):
        """
        Sample action index and torque given the current state.
        Returns (action_index, torque, probs).
        """
        logits = self.W.dot(state) + self.b
        if explore:
            probs = softmax(logits / self.temperature)
        else:
            # Greedy for evaluation
            probs = softmax(logits / max(1e-6, self.temperature))
        action_idx = np.random.choice(self.n_actions, p=probs)
        torque = np.array([self.action_values[action_idx]], dtype=np.float32)
        return action_idx, torque, probs

    def update(self, states, actions, rewards, gamma):
        """
        Perform a single REINFORCE update from one episode.

        states : (T, state_dim)
        actions: (T,) integer action indices
        rewards: (T,)
        """
        # 1. Discounted returns ("tension" over time)
        returns = discount_returns(rewards, gamma)

        # 2. Update moving baseline (coherence reference)
        episode_return = returns[0]
        self.baseline = (
            self.baseline_momentum * self.baseline
            + (1.0 - self.baseline_momentum) * episode_return
        )

        # 3. Advantages = tension vs baseline
        advantages = returns - self.baseline

        # 4. Normalize advantages (stabilize)
        adv_mean = np.mean(advantages)
        adv_std = np.std(advantages) + 1e-8
        advantages = (advantages - adv_mean) / adv_std

        # 5. Compute gradients
        dW = np.zeros_like(self.W)
        db = np.zeros_like(self.b)

        for t in range(len(states)):
            s = states[t]  # shape (state_dim,)
            a = actions[t]
            A = advantages[t]

            logits = self.W.dot(s) + self.b
            probs = softmax(logits / self.temperature)

            # Gradient of log π(a|s) wrt logits: one_hot(a) - probs
            one_hot = np.zeros(self.n_actions, dtype=np.float32)
            one_hot[a] = 1.0
            grad_logits = (one_hot - probs) * A  # scaled by advantage

            # Chain rule to W, b
            dW += grad_logits[:, None] * s[None, :]
            db += grad_logits

        # 6. Gradient ascent step
        self.W += self.lr * dW
        self.b += self.lr * db

        return float(episode_return)

    def anneal_temperature(self, moving_reward, target=-300.0):
        """
        Simple heuristic: if moving_reward improves, slowly reduce temperature.
        """
        # If we're better than a target, start tightening
        if moving_reward > target:
            self.temperature = max(0.1, self.temperature * 0.995)


# ------------------------------------------------------------------------------
# Checkpoint helpers
# ------------------------------------------------------------------------------

def save_checkpoint(path, policy, episode, reward_history):
    np.savez(
        path,
        W=policy.W,
        b=policy.b,
        baseline=policy.baseline,
        temperature=policy.temperature,
        episode=episode,
        reward_history=np.array(reward_history, dtype=np.float32),
    )
    print(f"[CKPT] Saved checkpoint at episode {episode} -> {path}")


def load_checkpoint(path, policy):
    data = np.load(path, allow_pickle=True)
    policy.W = data["W"]
    policy.b = data["b"]
    policy.baseline = float(data["baseline"])
    policy.temperature = float(data["temperature"])
    start_episode = int(data["episode"])
    reward_history = data["reward_history"].tolist()
    print(f"[CKPT] Loaded checkpoint from episode {start_episode} <- {path}")
    return start_episode, reward_history


# ------------------------------------------------------------------------------
# Training loop
# ------------------------------------------------------------------------------

def train_spider_on_pendulum(
    num_episodes=1000,
    max_steps=200,
    gamma=0.99,
    lr=1e-2,
    checkpoint_path="spider_pendulum_ckpt.npz",
    checkpoint_every=50,
):
    env = make_pendulum_env()

    # Pendulum obs is usually 3D: [cos(theta), sin(theta), theta_dot]
    state_dim = env.observation_space.shape[0]

    # Discretize torque in [-2, 2]
    action_values = np.linspace(-2.0, 2.0, num=7)  # 7-probe spider
    n_actions = len(action_values)

    policy = SpiderPolicy(
        state_dim=state_dim,
        n_actions=n_actions,
        action_values=action_values,
        lr=lr,
        init_scale=0.1,
    )

    # Load checkpoint if exists
    reward_history = []
    start_episode = 0
    if os.path.exists(checkpoint_path):
        start_episode, reward_history = load_checkpoint(checkpoint_path, policy)

    moving_reward = np.mean(reward_history[-50:]) if reward_history else -1000.0

    for episode in range(start_episode, num_episodes):
        state = env_reset(env)
        states = []
        actions = []
        rewards = []

        for t in range(max_steps):
            action_idx, torque, probs = policy.choose_action(state, explore=True)
            next_state, reward, done = env_step(env, torque)

            states.append(state)
            actions.append(action_idx)
            rewards.append(float(reward))

            state = next_state
            if done:
                break

        states = np.array(states, dtype=np.float32)
        actions = np.array(actions, dtype=np.int32)
        rewards = np.array(rewards, dtype=np.float32)

        episode_return = policy.update(states, actions, rewards, gamma)
        reward_history.append(episode_return)

        # Update moving average reward (for logging & temp schedule)
        if len(reward_history) >= 50:
            moving_reward = np.mean(reward_history[-50:])
        else:
            moving_reward = np.mean(reward_history)

        policy.anneal_temperature(moving_reward)

        # Logging
        if (episode + 1) % 10 == 0 or episode == 0:
            print(
                f"[Ep {episode+1:4d}] "
                f"Return={episode_return:8.2f}  "
                f"Mean(50)={moving_reward:8.2f}  "
                f"T={policy.temperature:.3f}"
            )

        # Checkpointing
        if (episode + 1) % checkpoint_every == 0:
            save_checkpoint(checkpoint_path, policy, episode + 1, reward_history)

    # Final scoring summary
    rewards_array = np.array(reward_history, dtype=np.float32)
    print("=" * 70)
    print("[TRAINING COMPLETE]")
    print(f"Final avg reward (last 50): {np.mean(rewards_array[-50:]):.2f}")
    print(f"Best episode reward:        {np.max(rewards_array):.2f}")
    print(f"Initial avg reward (first 20): {np.mean(rewards_array[:20]):.2f}")
    print("=" * 70)

    env.close()
    return policy, reward_history


if __name__ == "__main__":
    # You can tweak these numbers for longer training.
    train_spider_on_pendulum(
        num_episodes=15000,
        max_steps=200,
        gamma=0.99,
        lr=1e-2,
        checkpoint_path="spider_pendulum_ckpt.npz",
        checkpoint_every=50,
    )

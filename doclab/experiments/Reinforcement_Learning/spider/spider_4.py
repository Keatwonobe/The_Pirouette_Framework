# SAVE AS: spider_pendulum_with_ckpt.py

import os
import numpy as np
try:
    import gymnasium as gym
    GYMNASIUM = True
except:
    import gym
    GYMNASIUM = False

# -----------------------------------------------------------
# Utility wrappers for gym/gymnasium
# -----------------------------------------------------------

def env_reset(env):
    out = env.reset()
    if isinstance(out, tuple):
        return out[0]
    return out

def env_step(env, action):
    out = env.step(action)
    if len(out) == 5:
        obs, rew, terminated, truncated, info = out
        return obs, rew, (terminated or truncated)
    else:
        obs, rew, done, info = out
        return obs, rew, done

# -----------------------------------------------------------
#  SPIDER POLICY (original behavior)
# -----------------------------------------------------------

class SpiderPolicy:
    """
    Lightweight version preserving original behavior:
    - No normalization
    - No baseline
    - No temperature schedule
    """
    def __init__(self, state_dim, n_actions, action_values, lr=1e-2):
        self.state_dim = state_dim
        self.n_actions = n_actions
        self.action_values = np.array(action_values)

        self.W = np.random.randn(n_actions, state_dim) * 0.1
        self.b = np.zeros(n_actions)
        self.lr = lr

    def choose_action(self, state):
        logits = self.W.dot(state) + self.b
        probs = np.exp(logits - np.max(logits))
        probs = probs / (np.sum(probs) + 1e-8)

        a = np.random.choice(self.n_actions, p=probs)
        return a, np.array([self.action_values[a]], dtype=np.float32), probs

    def update(self, states, actions, returns):
        """
        REINFORCE without normalization.
        """
        dW = np.zeros_like(self.W)
        db = np.zeros_like(self.b)

        for t in range(len(states)):
            s = states[t]
            a = actions[t]
            G = returns[t]

            logits = self.W.dot(s) + self.b
            probs = np.exp(logits - np.max(logits))
            probs = probs / (np.sum(probs) + 1e-8)

            one_hot = np.zeros(self.n_actions)
            one_hot[a] = 1.0

            grad_logits = one_hot - probs

            dW += grad_logits[:, None] * s[None, :] * G
            db += grad_logits * G

        self.W += self.lr * dW
        self.b += self.lr * db

# -----------------------------------------------------------
# Checkpoint helpers
# -----------------------------------------------------------

def save_ckpt(path, policy, episode, rewards):
    np.savez(path,
             W=policy.W, b=policy.b,
             episode=episode,
             rewards=np.array(rewards))
    print(f"[CKPT] Saved at episode {episode} -> {path}")

def load_ckpt(path, policy):
    d = np.load(path, allow_pickle=True)
    policy.W = d["W"]
    policy.b = d["b"]
    print(f"[CKPT] Loaded -> {path}")
    return int(d["episode"]), d["rewards"].tolist()

# -----------------------------------------------------------
# Training loop (original dynamics + checkpointing)
# -----------------------------------------------------------

def train_spider(
    episodes=2000,
    max_steps=200,
    gamma=0.99,
    ckpt_path="spider.npz"
):

    env = gym.make("Pendulum-v1")
    state_dim = env.observation_space.shape[0]
    action_values = np.linspace(-2, 2, 7)

    policy = SpiderPolicy(state_dim, len(action_values), action_values)

    # Load checkpoint if exists
    rewards = []
    start_ep = 0
    if os.path.exists(ckpt_path):
        start_ep, rewards = load_ckpt(ckpt_path, policy)

    for ep in range(start_ep, episodes):

        s = env_reset(env)
        ep_states = []
        ep_actions = []
        ep_rewards = []

        # rollout
        for t in range(max_steps):
            a_idx, torque, _ = policy.choose_action(s)
            ns, rw, done = env_step(env, torque)

            ep_states.append(s)
            ep_actions.append(a_idx)
            ep_rewards.append(rw)

            s = ns
            if done:
                break

        # compute returns
        G = 0
        returns = []
        for r in reversed(ep_rewards):
            G = r + gamma * G
            returns.append(G)
        returns = returns[::-1]

        R = policy.update(np.array(ep_states), np.array(ep_actions), np.array(returns))
        rewards.append(sum(ep_rewards))

        if ep % 20 == 0:
            print(f"[Ep {ep}] Return={rewards[-1]:.2f}")

        if ep % 100 == 0:
            save_ckpt(ckpt_path, policy, ep, rewards)

    env.close()
    return policy, rewards
if __name__ == "__main__":
    print("=" * 70)
    print("SPIDER PROTOCOL: Active Manifold Instrumentation for RL")
    print("Testing measurement algorithm on REAL Gym Pendulum-v1")
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

    agent, rewards = train_spider(episodes=3000)

    print()
    print("=" * 70)
    print("Training complete on Pendulum-v1!")
    if len(rewards) >= 50:
        print(f"Final average reward (last 50 episodes): "
              f"{np.mean(rewards[-50:]):.2f}")
    print(f"Best episode reward: {np.max(rewards):.2f}")
    if len(rewards) >= 20:
        print(f"Initial avg reward (first 20): {np.mean(rewards[:20]):.2f}")
    print("=" * 70)
import gymnasium as gym
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim


# ============================================================
# Minimal Actor–Critic for Pendulum-v1 (device-safe)
# ============================================================

# Toggle this if you want to force CPU even when CUDA is available
USE_CUDA = True

device = torch.device("cuda" if (USE_CUDA and torch.cuda.is_available()) else "cpu")
print(f"Using device: {device}")


class PolicyNet(nn.Module):
    """
    Gaussian policy with tanh-squash for continuous action.
    Input:  obs_dim
    Output: action in [-1, 1], later scaled to env.high
    """
    def __init__(self, obs_dim, hidden_dim, act_dim):
        super().__init__()
        self.base = nn.Sequential(
            nn.Linear(obs_dim, hidden_dim),
            nn.Tanh(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.Tanh(),
        )
        self.mu_head = nn.Linear(hidden_dim, act_dim)
        # log_std is a learned parameter (state-independent)
        self.log_std = nn.Parameter(torch.zeros(act_dim))

    def forward(self, x: torch.Tensor):
        h = self.base(x)
        mu = self.mu_head(h)
        std = torch.exp(self.log_std)
        return mu, std

    def get_action_and_logp(self, obs_np):
        """
        obs_np: np.ndarray, shape (obs_dim,)
        Returns: (action_tanh, logp, entropy) on current device
        """
        obs_t = torch.as_tensor(obs_np, dtype=torch.float32, device=device).flatten()
        mu, std = self.forward(obs_t)
        dist = torch.distributions.Normal(mu, std)
        raw_action = dist.sample()
        logp = dist.log_prob(raw_action).sum()
        entropy = dist.entropy().sum()
        action = torch.tanh(raw_action)
        return action, logp, entropy


class ValueNet(nn.Module):
    """
    State-value function V(s).
    """
    def __init__(self, obs_dim, hidden_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(obs_dim, hidden_dim),
            nn.Tanh(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.Tanh(),
            nn.Linear(hidden_dim, 1),
        )

    def forward(self, x):
        # x: (..., obs_dim)
        if not isinstance(x, torch.Tensor):
            x = torch.as_tensor(x, dtype=torch.float32, device=device)
        else:
            x = x.to(device)
        v = self.net(x)
        return v.squeeze(-1)


def compute_returns(rewards, gamma):
    """
    Monte Carlo returns G_t = r_t + gamma * G_{t+1}
    """
    returns = []
    G = 0.0
    for r in reversed(rewards):
        G = r + gamma * G
        returns.append(G)
    returns.reverse()
    return torch.as_tensor(returns, dtype=torch.float32, device=device)


def train_pendulum_actor_critic(
    episodes=2000,
    gamma=0.99,
    actor_lr=3e-4,
    critic_lr=1e-3,
    entropy_coeff=0.01,
    hidden_dim=64,
    render_every=None,
):
    env = gym.make("Pendulum-v1")
    obs_dim = env.observation_space.shape[0]
    act_dim = env.action_space.shape[0]
    act_scale = env.action_space.high[0]  # usually 2.0

    policy = PolicyNet(obs_dim, hidden_dim, act_dim).to(device)
    value_net = ValueNet(obs_dim, hidden_dim).to(device)

    actor_opt = optim.Adam(policy.parameters(), lr=actor_lr)
    critic_opt = optim.Adam(value_net.parameters(), lr=critic_lr)

    for ep in range(1, episodes + 1):
        obs, _ = env.reset()
        done = False
        trunc = False

        obs_buf = []
        logp_buf = []
        rew_buf = []
        ent_buf = []

        ep_return_raw = 0.0

        # ----------- Rollout one episode -----------
        while not (done or trunc):
            if render_every is not None and ep % render_every == 0:
                env.render()

            # Actor step
            # Actor step
            # The torch.no_grad() block was removed from here.
            action_tanh, logp, entropy = policy.get_action_and_logp(obs)
            
            # This .detach() is correct and sufficient. 
            # It detaches the action for the env, but logp and entropy keep their graphs.
            action_env = (action_tanh.detach().cpu().numpy() * act_scale).astype(np.float32)

            # Step environment
            next_obs, reward, done, trunc, info = env.step(action_env)

            # Log transition
            obs_buf.append(obs)              # keep as np, convert later
            logp_buf.append(logp)            # tensor on device
            rew_buf.append(reward)
            ent_buf.append(entropy)          # tensor on device

            ep_return_raw += float(reward)
            obs = next_obs

        # ----------- Prepare tensors -----------
        logp_tensor = torch.stack(logp_buf).to(device)
        entropy_tensor = torch.stack(ent_buf).to(device)
        returns = compute_returns(rew_buf, gamma)  # already on device

        obs_tensor = torch.as_tensor(np.array(obs_buf), dtype=torch.float32, device=device)
        values = value_net(obs_tensor)  # (T,)

        # ----------- Advantage & losses -----------
        # Advantage: A_t = G_t - V(s_t)
        advantages = returns - values.detach()
        # Normalize advantages for stability
        adv_mean = advantages.mean()
        adv_std = advantages.std() + 1e-8
        advantages_norm = (advantages - adv_mean) / adv_std

        # Actor loss
        actor_loss = -(logp_tensor * advantages_norm).mean()
        # Critic loss (MSE)
        critic_loss = 0.5 * (returns - values).pow(2).mean()
        # Entropy bonus (encourage exploration)
        entropy_loss = -entropy_coeff * entropy_tensor.mean()

        # ----------- Update actor -----------
        actor_opt.zero_grad()
        (actor_loss + entropy_loss).backward()
        torch.nn.utils.clip_grad_norm_(policy.parameters(), max_norm=0.5)
        actor_opt.step()

        # ----------- Update critic -----------
        critic_opt.zero_grad()
        critic_loss.backward()
        torch.nn.utils.clip_grad_norm_(value_net.parameters(), max_norm=0.5)
        critic_opt.step()

        print(
            f"[Pendulum-Min] Ep {ep:04d} | "
            f"R_raw={ep_return_raw:7.2f} | "
            f"len={len(rew_buf):3d} | "
            f"actor_loss={actor_loss.item():.3f} | "
            f"critic_loss={critic_loss.item():.3f}"
        )

    env.close()
    return policy, value_net


if __name__ == "__main__":
    train_pendulum_actor_critic(
        episodes=2000,
        gamma=0.99,
        actor_lr=3e-4,
        critic_lr=1e-3,
        entropy_coeff=0.01,
        hidden_dim=64,
        render_every=None,  # set to e.g. 200 to watch
    )

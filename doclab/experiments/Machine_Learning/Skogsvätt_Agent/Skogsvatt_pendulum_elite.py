import gymnasium as gym
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import copy

# ============================================================
# Survival-of-the-Fittest Actor–Critic for Pendulum-v1
# ============================================================

# Toggle this if you want to force CPU even when CUDA is available
USE_CUDA = True
device = torch.device("cuda" if (USE_CUDA and torch.cuda.is_available()) else "cpu")
print(f"Using device: {device}")


class PolicyNet(nn.Module):
    """
    Gaussian policy with tanh-squash for continuous action.
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


def train_one_episode(
    env,
    policy,
    value_net,
    actor_opt,
    critic_opt,
    gamma=0.99,
    entropy_coeff=0.01,
):
    """
    Run a single on-policy A2C training episode and update weights in-place.
    Returns: (raw_return, actor_loss, critic_loss, episode_length)
    """
    obs, _ = env.reset()
    done = False
    trunc = False

    obs_buf = []
    logp_buf = []
    rew_buf = []
    ent_buf = []

    ep_return = 0.0

    while not (done or trunc):
        # sample action
        action_tanh, logp, entropy = policy.get_action_and_logp(obs)
        action_env = (action_tanh.detach().cpu().numpy()
                      * env.action_space.high[0]).astype(np.float32)

        next_obs, reward, done, trunc, info = env.step(action_env)

        obs_buf.append(obs)
        logp_buf.append(logp)
        rew_buf.append(reward)
        ent_buf.append(entropy)

        ep_return += float(reward)
        obs = next_obs

    # ----- Prepare tensors -----
    logp_t = torch.stack(logp_buf).to(device)
    ent_t = torch.stack(ent_buf).to(device)
    returns = compute_returns(rew_buf, gamma)
    obs_t = torch.as_tensor(np.array(obs_buf), dtype=torch.float32, device=device)
    values = value_net(obs_t)

    # Advantage
    advantages = returns - values.detach()
    adv_mean = advantages.mean()
    adv_std = advantages.std() + 1e-8
    adv_norm = (advantages - adv_mean) / adv_std

    # Losses
    actor_loss = -(logp_t * adv_norm).mean()
    critic_loss = 0.5 * (returns - values).pow(2).mean()
    entropy_loss = -entropy_coeff * ent_t.mean()

    # Update actor
    actor_opt.zero_grad()
    (actor_loss + entropy_loss).backward()
    torch.nn.utils.clip_grad_norm_(policy.parameters(), max_norm=0.5)
    actor_opt.step()

    # Update critic
    critic_opt.zero_grad()
    critic_loss.backward()
    torch.nn.utils.clip_grad_norm_(value_net.parameters(), max_norm=0.5)
    critic_opt.step()

    return ep_return, actor_loss.item(), critic_loss.item(), len(rew_buf)


def evaluate_policy(env, policy, episodes=5, max_steps=200, seeds=None):
    """
    Deterministic multi-episode evaluation of a policy.

    We run the same policy for several episodes and average the return.
    If `seeds` is provided, we reuse those seeds so different generations
    are evaluated on exactly the same initial conditions. This reduces
    evaluation noise and gives the elite a clearer foothold.
    """
    policy.eval()
    total = 0.0
    scale = env.action_space.high[0]

    with torch.no_grad():
        for i in range(episodes):
            seed = None
            if seeds is not None:
                # Reuse a fixed seed per eval index for fair comparison.
                seed = int(seeds[i % len(seeds)])
                obs, _ = env.reset(seed=seed)
            else:
                obs, _ = env.reset()

            done = False
            trunc = False
            t = 0
            ep_ret = 0.0

            while not (done or trunc) and t < max_steps:
                obs_t = torch.as_tensor(obs, dtype=torch.float32, device=device).flatten()
                mu, std = policy.forward(obs_t)
                # Deterministic mean action at eval time
                action_tanh = torch.tanh(mu)
                action_env = (action_tanh.detach().cpu().numpy() * scale).astype(np.float32)

                obs, r, done, trunc, info = env.step(action_env)
                ep_ret += float(r)
                t += 1

            total += ep_ret

    policy.train()
    return total / episodes

def train_pendulum_elite(
    generations=50,
    train_episodes_per_gen=50,
    eval_episodes=15,
    gamma=0.99,
    actor_lr=1e-4,
    critic_lr=5e-4,
    entropy_coeff=0.01,
    hidden_dim=64,
    improvement_margin=5.0,  # "stiffness": how much better than best to accept
    allow_sideways=True,      # allow small sideways moves (equal/slightly better)
):
    env = gym.make("Pendulum-v1")
    eval_env = gym.make("Pendulum-v1")

    # Fixed seeds for evaluation so different generations are
    # judged on the same initial conditions.
    eval_seeds = np.random.randint(0, 10_000_000, size=eval_episodes)

    obs_dim = env.observation_space.shape[0]
    act_dim = env.action_space.shape[0]

    policy = PolicyNet(obs_dim, hidden_dim, act_dim).to(device)
    value_net = ValueNet(obs_dim, hidden_dim).to(device)

    actor_opt = optim.Adam(policy.parameters(), lr=actor_lr)
    critic_opt = optim.Adam(value_net.parameters(), lr=critic_lr)

    # ----- Initialize elite from random policy -----
    best_eval = evaluate_policy(eval_env, policy, episodes=eval_episodes, seeds=eval_seeds)
    best_policy_state = copy.deepcopy(policy.state_dict())
    best_value_state = copy.deepcopy(value_net.state_dict())
    print(f"[INIT] best_eval={best_eval:.2f}")

    total_eps = 0

    for gen in range(1, generations + 1):
        # Start each generation from the current elite
        policy.load_state_dict(best_policy_state)
        value_net.load_state_dict(best_value_state)

        print(f"\n=== Generation {gen}/{generations} ===")

        # --------- Training phase (mutation) ---------
        gen_returns = []
        for k in range(train_episodes_per_gen):
            ep_ret, a_loss, c_loss, length = train_one_episode(
                env,
                policy,
                value_net,
                actor_opt,
                critic_opt,
                gamma=gamma,
                entropy_coeff=entropy_coeff,
            )
            total_eps += 1
            gen_returns.append(ep_ret)
            print(
                f"[Train] Gen {gen} Ep {k+1}/{train_episodes_per_gen} "
                f"GlobalEp {total_eps} | R_raw={ep_ret:7.2f} | len={length:3d} | "
                f"actor_loss={a_loss:.3f} | critic_loss={c_loss:.3f}"
            )

        avg_train = float(np.mean(gen_returns))

        # --------- Evaluation phase (selection) ---------
        avg_eval = evaluate_policy(eval_env, policy, episodes=eval_episodes, seeds=eval_seeds)
        print(
            f"[Eval] Gen {gen} | avg_train={avg_train:7.2f} "
            f"| avg_eval={avg_eval:7.2f} | best_eval={best_eval:7.2f}"
        )

        # Survival-of-the-fittest selection
        if avg_eval >= best_eval + improvement_margin:
            # clear improvement
            best_eval = avg_eval
            best_policy_state = copy.deepcopy(policy.state_dict())
            best_value_state = copy.deepcopy(value_net.state_dict())
            print(f"[SELECT] New elite (improved) with avg_eval={avg_eval:.2f}")
        elif allow_sideways and avg_eval >= best_eval:
            # sideways / tiny improvement (helps avoid overfitting to a single lucky seed)
            best_eval = avg_eval
            best_policy_state = copy.deepcopy(policy.state_dict())
            best_value_state = copy.deepcopy(value_net.state_dict())
            print(f"[SIDEWAYS] Elite updated without margin (avg_eval={avg_eval:.2f})")
        else:
            # candidate discarded
            print(f"[REJECT] Candidate discarded; keeping previous elite.")

    env.close()
    eval_env.close()

    # restore elite before returning
    policy.load_state_dict(best_policy_state)
    value_net.load_state_dict(best_value_state)
    return policy, value_net



if __name__ == "__main__":
    train_pendulum_elite()

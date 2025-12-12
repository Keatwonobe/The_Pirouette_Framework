import gymnasium as gym
import numpy as np
import copy
import torch
import torch.nn as nn
import torch.optim as optim
from collections import namedtuple
from dataclasses import dataclass
from typing import List

# ------------------------------------------------------------
# Utility: simple Dark Residue over state
# ------------------------------------------------------------

def dark_residue_simple(state: np.ndarray) -> float:
    """
    Smooth, general DR: mean squared norm of the state vector.
    """
    return float(np.dot(state, state)) / max(1, len(state))

def evaluate_policy(env, policy, episodes: int = 3, max_steps: int = 200):
    """
    Run the current policy for several episodes (no learning)
    and return average *raw* return. Uses deterministic mean actions.
    """
    policy.eval()
    total = 0.0
    action_scale = env.action_space.high[0]

    with torch.no_grad():
        for _ in range(episodes):
            obs, _ = env.reset()
            ep_ret = 0.0
            done = False
            trunc = False
            t = 0

            while not (done or trunc) and t < max_steps:
                obs_t = torch.as_tensor(obs, dtype=torch.float32).flatten()
                mu, std = policy.forward(obs_t)
                # deterministic eval: use mean, not sampling
                action_tanh = torch.tanh(mu).squeeze()
                action_env = np.array([action_tanh.item() * action_scale])

                obs, r, done, trunc, info = env.step(action_env)
                ep_ret += float(r)
                t += 1

            total += ep_ret

    policy.train()
    return total / episodes

def evaluate_policy(env, policy, episodes: int = 3, max_steps: int = 200):
    """
    Run the current policy for several episodes (no learning)
    and return average *raw* return. Uses deterministic mean actions.
    """
    policy.eval()
    total = 0.0
    action_scale = env.action_space.high[0]

    with torch.no_grad():
        for _ in range(episodes):
            obs, _ = env.reset()
            ep_ret = 0.0
            done = False
            trunc = False
            t = 0

            while not (done or trunc) and t < max_steps:
                obs_t = torch.as_tensor(obs, dtype=torch.float32).flatten()
                mu, std = policy.forward(obs_t)
                # deterministic eval: mean, no sampling noise
                action_tanh = torch.tanh(mu).squeeze()
                action_env = np.array([action_tanh.item() * action_scale])

                obs, r, done, trunc, info = env.step(action_env)
                ep_ret += float(r)
                t += 1

            total += ep_ret

    policy.train()
    return total / episodes


# ------------------------------------------------------------
# Triadic Supervisor (Pendulum-tuned)
# ------------------------------------------------------------

class TriadicSupervisor:
    def __init__(self, dr_shadow: float = 3.0):
        self.dr_shadow = dr_shadow
        self.last_dr = None

        # phase / rhythm
        self.phi = 0.0
        self.omega = 0.4 * np.pi
        self.update_window = (0.0, np.pi / 2)

        # precision coefficients
        self.a0  = -1.0
        self.aS  =  0.8
        self.aDR =  0.3
        self.aG  =  0.2

        # triadic weights (gentler for continuous control)
        self.w_Q = 0.3   # coherence gain
        self.w_C = 0.1   # contrast
        self.w_B = 0.5   # DR shadow

    def step_metrics(self, state: np.ndarray, gamma_load: float = 0.1):
        dr = dark_residue_simple(state)

        if self.last_dr is None:
            self.last_dr = dr

        delta_dr = dr - self.last_dr
        Q = max(0.0, -delta_dr)   # coherence gain
        C = abs(delta_dr)         # contrast
        B = 1.0 if dr > self.dr_shadow else 0.0
        S = C                     # surprise proxy

        # phase gate
        self.phi = (self.phi + self.omega + 0.05 * np.random.randn()) % (2 * np.pi)
        g = 1.0 if self.update_window[0] <= self.phi <= self.update_window[1] else 0.0

        # precision: open under surprise, close under high DR/load
        Pi = 1.0 / (1.0 + np.exp(
            -(self.a0 + self.aS * S - self.aDR * dr - self.aG * abs(gamma_load))
        ))

        raw_w = Pi + self.w_Q * Q + self.w_C * C - self.w_B * B
        w = g * raw_w

        self.last_dr = dr

        return {
            "DR": dr,
            "ΔDR": delta_dr,
            "Q": Q,
            "C": C,
            "B": B,
            "S": S,
            "Pi": Pi,
            "g": g,
            "w": w,
        }


# ------------------------------------------------------------
# Policy Network (continuous actor for Pendulum)
# ------------------------------------------------------------

class PolicyNet(nn.Module):
    def __init__(self, obs_dim: int, hidden: int, n_actions: int):
        super().__init__()
        self.actor_base = nn.Sequential(
            nn.Linear(obs_dim, hidden),
            nn.Tanh(),
            nn.Linear(hidden, hidden),
            nn.Tanh(),
        )
        self.actor_mu = nn.Linear(hidden, n_actions)
        self.actor_log_std = nn.Parameter(torch.zeros(1, n_actions))

    def forward(self, x: torch.Tensor):
        base_out = self.actor_base(x)
        mu = self.actor_mu(base_out)
        std = torch.exp(self.actor_log_std)
        return mu, std

    def act(self, obs: np.ndarray):
        obs_t = torch.as_tensor(obs, dtype=torch.float32).flatten()
        mu, std = self.forward(obs_t)
        dist = torch.distributions.Normal(mu, std)

        action_raw = dist.sample()
        logp = dist.log_prob(action_raw).sum(dim=-1).squeeze()
        entropy = dist.entropy().sum(dim=-1).squeeze()

        action_out = torch.tanh(action_raw).squeeze()
        return action_out, logp, entropy


# ------------------------------------------------------------
# Critic Network (value function)
# ------------------------------------------------------------

class ValueNet(nn.Module):
    def __init__(self, obs_dim: int, hidden: int):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(obs_dim, hidden),
            nn.Tanh(),
            nn.Linear(hidden, hidden),
            nn.Tanh(),
            nn.Linear(hidden, 1),
        )

    def forward(self, x: torch.Tensor):
        v = self.net(x)
        return v.squeeze(-1)


# ------------------------------------------------------------
# Stage 1: Episodic engrams (top-K good trajectories)
# ------------------------------------------------------------

@dataclass
class Trajectory:
    obs: List[np.ndarray]
    acts: List[float]
    rews: List[float]
    R_raw: float
    origin_ep: int

@dataclass
class Macro:
    pattern: np.ndarray     # shape (macro_len,)
    origin_ep: int
    origin_R: float
    score: float = -1e9


StepRecord = namedtuple("StepRecord", ["logp", "reward_learn", "w", "entropy", "obs"])


def evaluate_macro(env, macro: Macro, episodes: int = 3, max_steps: int = 200):
    """
    Open-loop evaluation: run the macro as the controller and return
    average raw return over 'episodes' episodes.
    """
    total = 0.0
    action_scale = env.action_space.high[0]
    pattern = macro.pattern
    L = len(pattern)

    for _ in range(episodes):
        obs, _ = env.reset()
        ep_ret = 0.0
        done = False
        trunc = False
        t = 0
        while not (done or trunc) and t < max_steps:
            a = pattern[t % L]
            action_env = np.array([a * action_scale])
            obs, r, done, trunc, info = env.step(action_env)
            ep_ret += float(r)
            t += 1
        total += ep_ret

    return total / episodes


def shape_reward(raw_reward: float) -> float:
    """
    Gentle reward scaling for Pendulum: keep sign, shrink magnitude.
    """
    return raw_reward / 10.0


def distill_engrams_into_policy(
    policy: PolicyNet,
    optimizer: optim.Optimizer,
    best_trajs: List[Trajectory],
    engram_steps: int = 50,
    engram_lr_scale: float = 0.1,
):
    """
    Behavioral cloning step: distill top-K trajectories into the policy.
    """
    if not best_trajs:
        return

    obs_list = []
    act_list = []
    for traj in best_trajs:
        obs_list.extend(traj.obs)
        act_list.extend(traj.acts)

    obs_batch = torch.as_tensor(np.array(obs_list), dtype=torch.float32)
    act_batch = torch.as_tensor(np.array(act_list), dtype=torch.float32).unsqueeze(-1)

    # Reduce LR temporarily for engram tuning
    orig_lrs = [g["lr"] for g in optimizer.param_groups]
    for g in optimizer.param_groups:
        g["lr"] *= engram_lr_scale

    for _ in range(engram_steps):
        mu, std = policy.forward(obs_batch)
        pred = torch.tanh(mu)  # mean-based deterministic intent
        bc_loss = ((pred - act_batch) ** 2).mean()

        optimizer.zero_grad()
        bc_loss.backward()
        torch.nn.utils.clip_grad_norm_(policy.parameters(), max_norm=0.5)
        optimizer.step()

    # Restore LR
    for g, lr in zip(optimizer.param_groups, orig_lrs):
        g["lr"] = lr


# ------------------------------------------------------------
# Stage 2: Cadence primitives (macro action templates)
# ------------------------------------------------------------

def build_or_update_macros(
    best_trajs: List[Trajectory],
    macro_library: List[Macro],
    eval_env,
    macro_len: int = 20,
    max_macros: int = 10,
):
    """
    Build/update macro library from best_trajs.
    - For each best trajectory, extract a cadence pattern.
    - If it's new (different origin_ep), create a Macro.
    - Evaluate each macro and keep top 'max_macros' by score.
    """
    # Track which episodes already contributed macros
    existing_eps = {m.origin_ep for m in macro_library}

    # 1. Add new macros from best_trajs
    for traj in best_trajs:
        origin_ep = getattr(traj, "origin_ep", None)
        if origin_ep is None:
            continue

        if origin_ep in existing_eps:
            continue  # already have a macro from this episode

        acts = np.array(traj.acts, dtype=np.float32)
        T = len(acts)
        if T < macro_len:
            continue

        idxs = np.linspace(0, T - 1, macro_len).astype(int)
        pattern = acts[idxs]
        macro_library.append(Macro(
            pattern=pattern,
            origin_ep=origin_ep,
            origin_R=traj.R_raw,
        ))

    # 2. Evaluate or re-evaluate all macros
    for m in macro_library:
        m.score = evaluate_macro(eval_env, m, episodes=3, max_steps=200)

    # 3. Keep only the top max_macros
    macro_library.sort(key=lambda m: m.score, reverse=True)
    if len(macro_library) > max_macros:
        macro_library[:] = macro_library[:max_macros]

    # Optional: print a small scoreboard
    print("[MACRO-RANK] Top macros:")
    for i, m in enumerate(macro_library):
        print(f"  #{i+1}: score={m.score:7.2f} | origin_ep={m.origin_ep:4d} | origin_R={m.origin_R:7.2f}")


# ------------------------------------------------------------
# Training loop with Actor–Critic + Stage 1 + Stage 2
# ------------------------------------------------------------

def train_skogsvatt_pendulum(
    episodes: int = 3000,
    gamma: float = 0.99,
    lr: float = 3e-4,
    entropy_coeff: float = 0.005,
    value_coef: float = 0.5,
    render_every=None,
    top_k: int = 10,
    distill_every: int = 200,
):
    env = gym.make("Pendulum-v1")
    eval_env = gym.make("Pendulum-v1")  # for macro ranking
    best_eval_return = -1e9
    best_policy_state = None

    obs_dim = env.observation_space.shape[0]
    n_actions = env.action_space.shape[0]
    action_scale = env.action_space.high[0]

    policy = PolicyNet(obs_dim, hidden=64, n_actions=n_actions)
    value_net = ValueNet(obs_dim, hidden=64)

    optimizer = optim.Adam(
        list(policy.parameters()) + list(value_net.parameters()),
        lr=lr
    )

    supervisor = TriadicSupervisor()

    best_trajs: List[Trajectory] = []
    macro_library: List[Macro] = []

    # ---- NEW: long-term best snapshot + rollback state ----
    best_eval_return = -1e9
    best_policy_state = copy.deepcopy(policy.state_dict())
    best_value_state = copy.deepcopy(value_net.state_dict())

    no_improve_evals = 0
    rollback_patience = 3         # how many bad evals in a row before rollback
    rollback_delta = 50.0         # how much worse than best before counting as "bad"
    eval_every = 10               # evaluate every N episodes
    eval_episodes = 5             # number of episodes per eval

    last_ep_loss = 0.0

    for ep in range(1, episodes + 1):
        obs, _ = env.reset()
        supervisor.last_dr = None

        step_records = []
        ep_reward_raw = 0.0

        ep_obs = []
        ep_acts = []
        ep_rews = []

        done = False
        trunc = False

        while not (done or trunc):
            if render_every and ep % render_every == 0:
                env.render()

            action_tanh, logp, entropy = policy.act(obs)
            action_env = np.array([action_tanh.item() * action_scale])
            obs_next, reward_raw, done, trunc, info = env.step(action_env)

            reward_learn = shape_reward(reward_raw)
            metrics = supervisor.step_metrics(obs, gamma_load=last_ep_loss)
            w = metrics["w"]

            step_records.append(StepRecord(
                logp=logp,
                reward_learn=reward_learn,
                w=w,
                entropy=entropy,
                obs=obs.copy(),
            ))

            ep_reward_raw += float(reward_raw)
            ep_obs.append(obs.copy())
            ep_acts.append(float(action_tanh.item()))
            ep_rews.append(float(reward_raw))

            obs = obs_next

        # ----- Episodic engram storage (Stage 1) -----
        traj = Trajectory(
            obs=ep_obs,
            acts=ep_acts,
            rews=ep_rews,
            R_raw=ep_reward_raw,
            origin_ep=ep,
        )

        if len(best_trajs) < top_k or ep_reward_raw > best_trajs[-1].R_raw:
            best_trajs.append(traj)
            best_trajs = sorted(best_trajs, key=lambda t: t.R_raw, reverse=True)[:top_k]
            print(f"[ENGRAM] New good episode stored at ep {ep}: R_raw={ep_reward_raw:.2f}")
            # Rebuild cadence macros whenever library updates (Stage 2)
            build_or_update_macros(
                best_trajs=best_trajs,
                macro_library=macro_library,
                eval_env=eval_env,
                macro_len=20,
                max_macros=10,
            )

        # ----- Compute returns -----
        rewards_learn = [r.reward_learn for r in step_records]
        returns = []
        G = 0.0
        for r in reversed(rewards_learn):
            G = r + gamma * G
            returns.append(G)
        returns.reverse()
        returns = torch.as_tensor(returns, dtype=torch.float32)

        # ----- Prepare tensors -----
        obs_batch = torch.as_tensor(
            np.array([rec.obs for rec in step_records]),
            dtype=torch.float32
        )
        logps = torch.stack([rec.logp for rec in step_records])
        entropies = torch.stack([rec.entropy for rec in step_records])
        weights = torch.as_tensor([rec.w for rec in step_records], dtype=torch.float32)

        # ----- Critic: estimate V(s) -----
        values = value_net(obs_batch)

        # Advantage: G_t - V(s_t)
        advantages_raw = returns - values.detach()
        # Normalize advantages for stability
        adv_mean = advantages_raw.mean()
        adv_std = advantages_raw.std() + 1e-8
        advantages_norm = (advantages_raw - adv_mean) / adv_std

        # Gentle triadic modulation
        tri = 0.3 * torch.tanh(weights)   # in [-0.3, +0.3]
        advantages = advantages_norm * (1.0 + tri)

        # ----- Losses -----
        actor_loss = -(logps * advantages.detach()).mean()
        critic_loss = 0.5 * (returns - values).pow(2).mean()
        entropy_loss = -entropy_coeff * entropies.mean()

        loss = actor_loss + value_coef * critic_loss + entropy_loss

        optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(
            list(policy.parameters()) + list(value_net.parameters()),
            max_norm=0.5
        )
        optimizer.step()

        last_ep_loss = float(loss.item())

        # ----- Periodic engram distillation into policy (Stage 1) -----
        if ep % distill_every == 0 and best_trajs:
            print(f"[ENGRAM] Distilling {len(best_trajs)} trajectories into policy at ep {ep}...")
            distill_engrams_into_policy(
                policy,
                optimizer,
                best_trajs,
                engram_steps=40,
                engram_lr_scale=0.1,
            )

        print(
            f"[Pendulum] Ep {ep:04d} | "
            f"R_raw={ep_reward_raw:7.2f} | "
            f"len={len(step_records):3d} | "
            f"loss={loss.item():.3f}"
        )

        # ----- Periodic multi-episode evaluation + rollback logic -----
        if ep % eval_every == 0:
            avg_eval = evaluate_policy(eval_env, policy, episodes=eval_episodes, max_steps=200)
            print(f"[EVAL] Ep {ep:04d} | avg_eval={avg_eval:.2f} over {eval_episodes} episodes "
                  f"(best={best_eval_return:.2f})")

            if avg_eval > best_eval_return:
                # New long-term champion
                best_eval_return = avg_eval
                best_policy_state = copy.deepcopy(policy.state_dict())
                best_value_state = copy.deepcopy(value_net.state_dict())
                no_improve_evals = 0
                print(f"[CHECKPOINT] New best policy at ep {ep}: avg_eval={avg_eval:.2f}")
            else:
                # No improvement
                # Count it as "bad" only if it's significantly worse than best
                if avg_eval < best_eval_return - rollback_delta:
                    no_improve_evals += 1
                    print(f"[EVAL] Worse than best by {best_eval_return - avg_eval:.2f}; "
                          f"no_improve_evals={no_improve_evals}")
                else:
                    # small fluctuation, don't punish
                    print("[EVAL] Slightly below best; not counting against patience.")
                    # Optionally: no_improve_evals = 0  # if you want to forgive small drops

                # If we've had several significantly-bad evals, rollback
                if no_improve_evals >= rollback_patience:
                    print(f"[ROLLBACK] Restoring best policy (best_eval={best_eval_return:.2f}) "
                          f"after {no_improve_evals} bad evals.")
                    policy.load_state_dict(best_policy_state)
                    value_net.load_state_dict(best_value_state)
                    no_improve_evals = 0

    env.close()
    eval_env.close()

    # Ensure we return the best known policy, not just the last one
    policy.load_state_dict(best_policy_state)
    value_net.load_state_dict(best_value_state)

    return policy, value_net, best_trajs, macro_library


if __name__ == "__main__":
    train_skogsvatt_pendulum(
        episodes=3000,
        lr=3e-4,
        entropy_coeff=0.005,
        value_coef=0.5,
        render_every=None,
        top_k=10,
        distill_every=200,
    )

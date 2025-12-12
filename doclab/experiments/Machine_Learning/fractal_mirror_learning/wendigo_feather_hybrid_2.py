#!/usr/bin/env python3
"""
WENDIGO FEATHER++ (Multitask)
CartPole-v1  | Pendulum-v1 | Acrobot-v1

Core:
- SAC policy with geodesic navigation (state→(binned) action→expected DR)
- Reverse Pareto critical-moment mining per episode
- Global clean-transition bank for cross-task sharpening (transfer)
- Task-aware DR functions + per-task binning/bridging

Author: you+me
"""

import os, json, time
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Any, Optional

import gymnasium as gym
import numpy as np

from stable_baselines3 import SAC
from stable_baselines3.common.logger import configure

# ------------------------- Tunables ------------------------- #
GALLERY_DIR = "gallery_feather_multi"
os.makedirs(GALLERY_DIR, exist_ok=True)

# Reward shaping weights (task-agnostic)
GAMMA_COHERENCE = 1.4
BETA_DURATION   = 0.05
DELTA_DISSONANCE= 1.0

# Geodesic parameters
GEODESIC_INFLUENCE = 0.35
EXPLORATION_DECAY  = 0.995
MIN_EXPLORATION    = 0.08

# RPA
RPA_THRESHOLD = 0.8

# Global transfer
GLOBAL_BANK_MAX = 5000
GLOBAL_BANK_SAMPLE_K = 64
GOLD_SAVE_K = 64

# Episodes
NUM_EPISODES = 750

# --------------------- Task library --------------------- #
@dataclass
class TaskSpec:
    name: str
    gym_id: str
    kind: str                 # "discrete" or "continuous"
    # For geodesic action binning (continuous only)
    bins: int = 5
    # For reporting/mastery feeling, not used as hard gates here
    step_cap: int = 500
    reward_min: float = -1000.
    reward_max: float = 1000.

def make_tasks() -> List[TaskSpec]:
    return [
        TaskSpec(name="cartpole", gym_id="CartPole-v1", kind="discrete",
                 step_cap=500, reward_min=0, reward_max=500),
        TaskSpec(name="pendulum", gym_id="Pendulum-v1", kind="continuous",
                 bins=7, step_cap=200, reward_min=-1600, reward_max=0),
        TaskSpec(name="acrobot",  gym_id="Acrobot-v1", kind="discrete",
                 step_cap=500, reward_min=-500, reward_max=0),
    ]

# ----------------- DR functions per task ----------------- #
def dr_cartpole(obs4: np.ndarray) -> float:
    cart_pos, cart_vel, pole_angle, pole_vel = obs4
    return float(0.4*abs(cart_pos) + 0.2*abs(cart_vel) + 1.5*abs(pole_angle) + 0.3*abs(pole_vel))

def pend_angle_err(obs3: np.ndarray) -> float:
    cos_th, sin_th, thdot = obs3
    return float(np.arctan2(sin_th, cos_th))

def dr_pendulum(obs3: np.ndarray, action_scalar: float) -> float:
    # action in [-2,2] (we’ll scale)
    cos_th, sin_th, thdot = obs3
    ang = np.arctan2(sin_th, cos_th)
    return float(0.8*abs(ang) + 0.15*abs(thdot) + 0.05*abs(action_scalar))

def dr_acrobot(obs6: np.ndarray, disc_action: int) -> float:
    # obs = [c1, s1, c2, s2, th1dot, th2dot]
    c1, s1, c2, s2, d1, d2 = obs6
    # Penalize angle deviation from upright, plus velocities and torque usage proxy
    th1 = np.arctan2(s1, c1)
    th2 = np.arctan2(s2, c2)
    # Acrobot wants to raise the end-effector upward: rough proxy is angles near 0
    base = 0.5*abs(th1) + 0.5*abs(th2) + 0.15*(abs(d1)+abs(d2))
    # small action-use term to encourage “clean” swings (three discrete actions: 0,1,2)
    use = 0.05 * (0 if disc_action==1 else 1)  # center action ~ "no torque"
    return float(base + use)

# ----------------- Witness / Episodes ----------------- #
@dataclass
class Transition:
    state: np.ndarray
    action_cont: np.ndarray       # the SAC continuous action emitted in [-1,1]
    next_state: np.ndarray
    reward: float
    done: bool
    # bookkeeping
    dark_residue: float = 0.0
    dr_derivative: float = 0.0
    coherence_gain: float = 0.0
    # for geodesic
    task_id: int = 0
    action_idx: int = 0

    def state_hash(self) -> int:
        disc = (self.state*10).astype(int)
        # include task id so maps don’t collide blindly; keeps optional transfer via global bank
        return hash((int(self.task_id), *disc.tolist()))

@dataclass
class Episode:
    episode_num: int
    task_id: int
    task_name: str
    transitions: List[Transition] = field(default_factory=list)
    total_reward: float = 0.0         # This is your shaped reward
    total_env_reward: float = 0.0     # This will be the raw gym reward
    total_score: int = 0
    mean_dr: float = 0.0
    total_coherence_gain: float = 0.0
    critical_indices: List[int] = field(default_factory=list)
    critical_states: List[int] = field(default_factory=list)
    timestamp: float = field(default_factory=time.time)

    def compute(self):
        if not self.transitions: return
        self.total_score = len(self.transitions)
        self.total_reward = float(sum(t.reward for t in self.transitions))
        self.mean_dr = float(np.mean([t.dark_residue for t in self.transitions]))
        self.total_coherence_gain = float(sum(t.coherence_gain for t in self.transitions))
        # Note: total_env_reward is summed up during the episode run directly

    def as_dict(self) -> Dict[str, Any]:
        return dict(
            episode_num=self.episode_num,
            task_id=self.task_id,
            task_name=self.task_name,
            total_score=self.total_score,
            total_reward=self.total_reward,
            total_env_reward=self.total_env_reward, # Added for gallery saves
            mean_dr=self.mean_dr,
            total_coherence_gain=self.total_coherence_gain,
            critical_moment_count=len(self.critical_indices),
            timestamp=self.timestamp,
        )

class ReversePareto:
    @staticmethod
    def analyze(ep: Episode, threshold: float = RPA_THRESHOLD) -> List[Tuple[int,int,float]]:
        if not ep.transitions: return []
        items = [{'idx':i, 'hash':t.state_hash(), 'dr':t.dark_residue}
                 for i,t in enumerate(ep.transitions)]
        items.sort(key=lambda x: x['dr'], reverse=True)
        total = sum(x['dr'] for x in items)
        if total <= 0: return []
        out, run = [], 0.0
        for x in items:
            out.append((x['idx'], x['hash'], x['dr']))
            run += x['dr']
            if run/total >= threshold: break
        return out

# --------- Geodesic Map (state→action_bin→E[DR]) --------- #
class GeodesicMap:
    def __init__(self):
        # (state_hash) -> {action_idx: (avg_dr, count)}
        self.tab: Dict[int, Dict[int, Tuple[float,int]]] = {}
        self.known: set = set()

    def update(self, state_hash: int, action_idx: int, dr: float, weight: int = 1):
        self.known.add(state_hash)
        slot = self.tab.setdefault(state_hash, {})
        if action_idx not in slot:
            slot[action_idx] = (dr, weight)
        else:
            avg, cnt = slot[action_idx]
            new_avg = (avg*cnt + dr*weight) / (cnt + weight)
            slot[action_idx] = (new_avg, cnt + weight)

    def best_action(self, state_hash: int) -> int:
        if state_hash not in self.tab or not self.tab[state_hash]: return -1
        return min(self.tab[state_hash].keys(), key=lambda a: self.tab[state_hash][a][0])

    def expected_dr(self, state_hash: int, action_idx: int) -> float:
        if state_hash in self.tab and action_idx in self.tab[state_hash]:
            return self.tab[state_hash][action_idx][0]
        return 1e9

# ---------------- Witness / Bank / Scheduler -------------- #
class GeodesicWitness:
    def __init__(self, top_k: int = 15):
        self.top_k = top_k
        self.all: List[Episode] = []
        self.top: List[Episode] = []
        self.map = GeodesicMap()
        self.explore = 1.0

    def observe(self, ep: Episode):
        ep.compute()
        self.all.append(ep)
        self.top.append(ep)
        self.top.sort(key=lambda e: (e.total_score, -e.mean_dr), reverse=True)
        if len(self.top) > self.top_k:
            self.top = self.top[:self.top_k]

        crit = ReversePareto.analyze(ep)
        ep.critical_indices = [i for i,_,_ in crit]
        ep.critical_states  = [h for _,h,_ in crit]

        # Learn from all transitions, double-weight criticals
        crit_set = {i for i,_,_ in crit}
        for i,t in enumerate(ep.transitions):
            h = t.state_hash()
            w = 2 if i in crit_set else 1
            self.map.update(h, t.action_idx, t.dark_residue, weight=w)

        self._decay_explore()

    def _decay_explore(self):
        self.explore = max(MIN_EXPLORATION, self.explore * EXPLORATION_DECAY)

    def should_explore(self) -> bool:
        return np.random.rand() < self.explore

    def geodesic_recommend(self, state: np.ndarray, task_id: int) -> int:
        disc = (state * 10).astype(int)
        h = hash((int(task_id), *disc.tolist()))
        return self.map.best_action(h)

    def save_gallery(self, name="gallery.json"):
        data = dict(
            total_episodes=len(self.all),
            geodesic_map_size=len(self.map.known),
            exploration_rate=self.explore,
            top_episodes=[e.as_dict() for e in self.top],
        )
        with open(os.path.join(GALLERY_DIR, name), "w") as f:
            json.dump(data, f, indent=2)

class GlobalTransitionBank:
    """Cross-task transfer: keep the globally cleanest transitions."""
    def __init__(self, max_size=GLOBAL_BANK_MAX):
        self.items: List[Tuple[float,int,Tuple]] = []
        self.max_size = max_size

    def add(self, task_id: int, transition_tuple: Tuple, dr: float):
        self.items.append((dr, task_id, transition_tuple))
        self.items.sort(key=lambda x: x[0])
        if len(self.items) > self.max_size:
            self.items = self.items[:self.max_size]

    def sample(self, k: int = GLOBAL_BANK_SAMPLE_K) -> List[Tuple]:
        if not self.items: return []
        return [x[2] for x in self.items[:min(k, len(self.items))]]

# ------------------- Multitask wrapper ------------------- #
class MultiTaskEnv(gym.Env):
    """
    Presents a unified Box([-1,1], shape=(1,)) action-space to SAC.
    Internally routes to 3 tasks. For discrete tasks, continuous action is
    quantized into an index; for continuous tasks, it's scaled to env’s range.
    """
    metadata = {"render_modes": []}

    def __init__(self, specs: List[TaskSpec]):
        super().__init__()
        self.specs = specs
        self.envs = [gym.make(s.gym_id) for s in specs]
        self.num_tasks = len(specs)
        self.cur_id: int = 0
        self.cur_env = self.envs[0]

        self.action_space = gym.spaces.Box(low=-1.0, high=1.0, shape=(1,), dtype=np.float32)

        # 8-wide obs to be generous: pad task obs to 7 and append task_id_norm
        high = np.array([np.inf]*8, dtype=np.float32)
        self.observation_space = gym.spaces.Box(low=-high, high=high, dtype=np.float32)

    def _choose_task(self) -> int:
        # simple round-robin favoring unmastered would be fine; start uniform random
        self.cur_id = int(np.random.randint(0, self.num_tasks))
        self.cur_env = self.envs[self.cur_id]
        return self.cur_id

    def _pack_obs(self, raw_obs: np.ndarray, task_id: int) -> np.ndarray:
        raw = np.array(raw_obs, dtype=np.float32).flatten()
        base = np.zeros(7, dtype=np.float32)
        base[: min(len(raw), 7)] = raw[: min(len(raw), 7)]
        task_norm = task_id / max(1, self.num_tasks - 1)
        return np.concatenate([base, np.array([task_norm], dtype=np.float32)], axis=0)

    def reset(self, *, seed: Optional[int]=None, options: Optional[dict]=None):
        super().reset(seed=seed)
        tid = self._choose_task()
        obs, info = self.cur_env.reset(seed=seed)
        return self._pack_obs(obs, tid), {"task_id": tid, "task_name": self.specs[tid].name, "inner_info": info}

    def _disc_map_cartpole(self, a_cont: float) -> int:
        return 0 if a_cont < 0 else 1

    def _disc_map_acrobot(self, a_cont: float) -> int:
        # 3 bins: [-1,-0.33), [-0.33,0.33), [0.33,1]
        if a_cont < -0.33: return 0
        if a_cont < 0.33:  return 1
        return 2

    def _bins_for_cont(self, bins: int, a_cont: float, low: float, high: float) -> Tuple[int, float]:
        """
        Returns (bin_idx, env_action_scalar)
        - a_cont in [-1,1]
        - env action space scaled [low, high]
        """
        # choose bin center in [-1,1]
        edges = np.linspace(-1.0, 1.0, bins+1)
        centers = 0.5*(edges[:-1]+edges[1:])
        # pick closest center
        idx = int(np.argmin(np.abs(centers - a_cont)))
        a_center = float(centers[idx])
        # scale center to env range
        env_a = low + (a_center+1.0)*0.5*(high-low)
        return idx, env_a

    def step(self, action: np.ndarray):
        a = float(action[0])
        spec = self.specs[self.cur_id]
        name = spec.name

        # Helper to handle both old (gym) and new (gymnasium) API return values
        def handle_step_result(step_return):
            if len(step_return) == 4:
                # Old API: obs, rew, done, info
                obs, rew, done, info = step_return
                term, trunc = bool(done), bool(done)
                return obs, rew, term, trunc, info
            else:
                # New API: obs, rew, term, trunc, info
                return step_return

        if name == "cartpole":
            disc = self._disc_map_cartpole(a)
            step_return = self.cur_env.step(disc)
            obs, rew, term, trunc, info = handle_step_result(step_return)
            return self._pack_obs(obs, self.cur_id), rew, term, trunc, {"task_id": self.cur_id, "task_name": name, "action_idx": disc}

        elif name == "acrobot":
            disc = self._disc_map_acrobot(a)
            step_return = self.cur_env.step(disc)
            obs, rew, term, trunc, info = handle_step_result(step_return)
            return self._pack_obs(obs, self.cur_id), rew, term, trunc, {"task_id": self.cur_id, "task_name": name, "action_idx": disc}

        elif name == "pendulum":
            # action space [-2,2]
            idx, env_a = self._bins_for_cont(spec.bins, a, -2.0, 2.0)
            step_return = self.cur_env.step(np.array([env_a], dtype=np.float32))
            obs, rew, term, trunc, info = handle_step_result(step_return)
            return self._pack_obs(obs, self.cur_id), rew, term, trunc, {"task_id": self.cur_id, "task_name": name, "action_idx": idx, "raw_action": env_a}

        else:
            raise RuntimeError("unknown task")

# -------------- Geodesic-aware action gate -------------- #
class GeodesicGate:
    """
    Doesn’t rewrite the action coming out of SAC; instead, at log-time we
    *interpret* the action into an action_idx and give the geodesic map a chance
    to replace the idx with a recommended idx (discrete or bin center).
    For continuous tasks we map idx back to the nearest bin center in [-1,1].
    """
    def __init__(self, witness: GeodesicWitness, specs: List[TaskSpec]):
        self.witness = witness
        self.specs = specs

    def maybe_override(self, obs: np.ndarray, task_id: int, sac_a_cont: float) -> Tuple[float, int]:
        # If exploring, let SAC drive.
        if self.witness.should_explore():
            return sac_a_cont, -1

        # Ask geodesic for best idx
        geo_idx = self.witness.geodesic_recommend(obs, task_id)
        if geo_idx < 0:
            return sac_a_cont, -1

        # Map idx to a representative continuous action in [-1,1]
        spec = self.specs[task_id]
        if spec.kind == "discrete":
            # we’ll just output a continuous number that will quantize into that index
            if spec.name == "cartpole":
                return (-0.5 if geo_idx == 0 else 0.5), geo_idx
            if spec.name == "acrobot":
                return (-0.66 if geo_idx==0 else (0.0 if geo_idx==1 else 0.66)), geo_idx
        else:
            # continuous: choose bin center in [-1,1]
            edges = np.linspace(-1.0, 1.0, spec.bins+1)
            centers = 0.5*(edges[:-1]+edges[1:])
            center = float(centers[max(0, min(spec.bins-1, geo_idx))])
            return center, geo_idx

        return sac_a_cont, -1

# ---------------------- Train loop ---------------------- #
def main():
    print("="*80)
    print("WENDIGO FEATHER++  |  Multitask Geodesic SAC (CartPole, Pendulum, Acrobot)")
    print("="*80)

    specs = make_tasks()
    env = MultiTaskEnv(specs)
    witness = GeodesicWitness(top_k=15)
    gate = GeodesicGate(witness, specs)

    agent = SAC("MlpPolicy", env, verbose=0, train_freq=(1, "step"))
    agent.set_logger(configure(None, ["stdout"]))

    # Warm up replay buffer with random actions in the unified space
    WARMUP = 8000
    obs, _ = env.reset()
    for _ in range(WARMUP):
        a = env.action_space.sample()
        # Handle both old and new gym API returns for robustness
        step_return = env.step(a)
        if len(step_return) == 5:
            nxt, _, term, trunc, _ = step_return
            d = term or trunc
        else: # len == 4
            nxt, _, d, _ = step_return
        
        agent.replay_buffer.add(obs, nxt, a, 0.0, d, [{}])
        obs = nxt
        if d:
            obs, _ = env.reset()

    # Global transfer bank
    bank = GlobalTransitionBank(max_size=GLOBAL_BANK_MAX)

    print("Warmup complete. Training...\n")
    best15 = 0

    for ep in range(1, NUM_EPISODES+1):
        obs, info = env.reset()
        task_id = info["task_id"]
        task_name = info["task_name"]

        episode = Episode(episode_num=ep, task_id=task_id, task_name=task_name)

        done = False
        prev_dr = 0.0
        first_step = True

        while not done:
            # SAC proposes a continuous action
            a_cont, _ = agent.predict(obs, deterministic=False)

            # Let geodesic gate bias toward known clean bins when not exploring
            a_cont_eff, geo_idx = gate.maybe_override(obs, task_id, float(a_cont[0]))
            a_for_env = np.array([a_cont_eff], dtype=np.float32)

            nxt, env_rew, term, trunc, step_info = env.step(a_for_env)
            done = bool(term or trunc)
            episode.total_env_reward += env_rew # <-- ACCUMULATE RAW REWARD HERE

            # Interpret action_idx actually taken by env (quantization happens inside env)
            # so we always know which bucket was executed.
            action_idx = int(step_info.get("action_idx", geo_idx if geo_idx>=0 else 0))

            # ------- Compute task-specific DR and shaped reward ------- #
            if task_name == "cartpole":
                cur_dr = dr_cartpole(nxt[:4])
                coh_gain = max(0.0, (prev_dr - cur_dr))
                shaped = (GAMMA_COHERENCE*coh_gain + BETA_DURATION - DELTA_DISSONANCE*cur_dr)

            elif task_name == "acrobot":
                cur_dr = dr_acrobot(nxt[:6], action_idx)
                coh_gain = max(0.0, (prev_dr - cur_dr))
                # Acrobot gives sparse negative rewards until terminal; keep small survival pat
                shaped = env_rew*0.02 + GAMMA_COHERENCE*coh_gain + 0.03 - 0.8*cur_dr

            elif task_name == "pendulum":
                raw_a = float(step_info.get("raw_action", 0.0))
                cur_dr = dr_pendulum(nxt[:3], raw_a)
                coh_gain = max(0.0, (prev_dr - cur_dr))
                shaped = (env_rew/8.0) + GAMMA_COHERENCE*coh_gain + 0.03 - 0.8*cur_dr

            else:
                cur_dr, coh_gain, shaped = 0.0, 0.0, env_rew

            if first_step:
                prev_dr = cur_dr
                first_step = False

            # record transition (state hash includes task id)
            tr = Transition(
                state=obs.copy(),
                action_cont=a_for_env.copy(),
                next_state=nxt.copy(),
                reward=shaped,
                done=done,
                dark_residue=cur_dr,
                dr_derivative=cur_dr - prev_dr,
                coherence_gain=coh_gain,
                task_id=task_id,
                action_idx=action_idx,
            )
            episode.transitions.append(tr)

            # add to agent buffer + quick train step
            agent.replay_buffer.add(obs, nxt, a_for_env, shaped, done, [{}])
            agent.train(gradient_steps=1)

            # add to global transfer bank (for cross-task sharpening)
            bank.add(task_id, (obs, a_for_env, nxt, shaped, cur_dr, done, task_id), cur_dr)

            obs = nxt
            prev_dr = cur_dr

        # Episode bookkeeping / witness
        witness.observe(episode)

        # Sharpen from globally clean transitions (transfer)
        if ep > 15:
            clean = bank.sample(k=GLOBAL_BANK_SAMPLE_K)
            # mildly upweight the clean transitions as “teacher” hits
            for (o, a, n, r, dr, dn, tid) in clean:
                extra = r + 0.1*max(0.0, 0.35 - dr) - 0.05*dr
                agent.replay_buffer.add(o, n, a, extra, dn, [{}])
            agent.train(gradient_steps=min(10, len(clean)))

        # Logs
        # --- MODIFIED PRINT STATEMENT ---
        top_avg = float(np.mean([e.total_score for e in witness.top])) if witness.top else 0.0
        best15 = max(best15, int(top_avg))
        
        # Conditionally add the raw environment score for relevant tasks
        env_score_str = ""
        if task_name in ["pendulum", "acrobot"]:
            env_score_str = f"| envR={episode.total_env_reward: 7.1f} "

        print(f"Ep {ep:03d} | task={task_name:9s} | steps={episode.total_score:4d} {env_score_str}"
              f"| meanDR={episode.mean_dr: .3f} | crit={len(episode.critical_indices):2d} "
              f"| Geo={len(witness.map.known):5d} | Explore={witness.explore:.3f}")

        if ep % 50 == 0:
            witness.save_gallery(f"gallery_ep{ep:03d}.json")

    # Finalize
    witness.save_gallery("gallery_final.json")
    agent.save(os.path.join(GALLERY_DIR, "wendigo_feather_multi.zip"))
    print("\nTRAINING COMPLETE.")
    print(f"Seen states in geodesic map: {len(witness.map.known)}")
    print(f"Top-15 (steps avg proxy): {best15}")
    env.close()

if __name__ == "__main__":
    main()

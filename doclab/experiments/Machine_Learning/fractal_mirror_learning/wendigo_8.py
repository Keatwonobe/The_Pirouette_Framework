# wendigo_8.py (Corrected)
import gymnasium as gym
import numpy as np
import torch as th
import torch.nn as nn
import torch.optim as optim
from torch.distributions import Normal
import logging
import json
from dataclasses import dataclass, field
from collections import deque
from typing import List, Tuple, Dict

# --- Basic Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
device = th.device("cuda" if th.cuda.is_available() else "cpu")

# --- Pirouette-Inspired Dark Residue Functions ---

def dark_residue_cartpole(obs: np.ndarray) -> float:
    x, x_dot, theta, theta_dot = obs
    dr = 0.5 * abs(x) + 0.5 * abs(theta) + 0.05 * abs(x_dot) + 0.05 * abs(theta_dot)
    return float(dr)

def dark_residue_pendulum_helical(obs: np.ndarray, action: float, prev_obs: np.ndarray) -> float:
    cos_th, sin_th, th_dot = obs
    prev_cos, _, prev_th_dot = prev_obs
    
    angle_err = np.arctan2(sin_th, cos_th)
    angular_accel = th_dot - prev_th_dot
    angular_momentum_echo = th_dot * prev_th_dot

    dr = (
        0.6 * abs(angle_err)
        + 0.2 * abs(angular_accel)
        + 0.15 * max(0, -angular_momentum_echo)
        + 0.05 * abs(action)
    )
    return float(dr)

def dark_residue_mountaincar_arrow(obs: np.ndarray, action: float) -> float:
    position, velocity = obs
    
    base_dr = (0.9 * (0.5 - position)) if position < 0.5 else 0.0
    base_dr += 0.1 * (0.01 - abs(velocity)) if abs(velocity) < 0.01 else 0.0
    
    goal_vector = 0.5 - position
    action_alignment = np.sign(action) * np.sign(goal_vector)

    dr_arrow_mod = np.exp(-0.5 * max(0, action_alignment) * abs(goal_vector))
    
    return float(base_dr * dr_arrow_mod)

# --- Wound Channel Memory ---
class WoundChannelMemory:
    def __init__(self, state_dim: int, history_len: int = 100, decay: float = 0.99):
        self.echo_tensor = np.zeros((state_dim, state_dim))
        self.history_window = deque(maxlen=history_len)
        self.decay = decay
        self.state_dim = state_dim

    def update(self, state: np.ndarray):
        state = state[:self.state_dim]
        self.history_window.append(state)
        self.echo_tensor += np.outer(state, state)
        self.echo_tensor *= self.decay

    def get_inertial_force(self, state_change: np.ndarray) -> float:
        if len(state_change) != self.state_dim:
            padded_change = np.zeros(self.state_dim)
            min_len = min(len(state_change), self.state_dim)
            padded_change[:min_len] = state_change[:min_len]
            state_change = padded_change
        
        resistance = state_change.T @ self.echo_tensor @ state_change
        return float(np.clip(resistance, 0, 1.0))

# --- Data Structures & Task Management ---

@dataclass
class TaskSpec:
    name: str
    reward_min: float
    reward_max: float
    solve_threshold_norm: float
    score_metric: str
    step_cap: int
    state_dim: int
    window: int = 25
    scores: deque = field(default_factory=lambda: deque(maxlen=25))
    dr_min: float = 0.0
    dr_max: float = 3.0
    
    def update(self, raw_score: float): self.scores.append(raw_score)
    def normalize_single_score(self, raw_score: float) -> float:
        if self.reward_max == self.reward_min: return 0.0
        clamped = max(self.reward_min, min(self.reward_max, raw_score))
        return (clamped - self.reward_min) / (self.reward_max - self.reward_min)
    def normalize_dr(self, dr: float) -> float:
        clamped = max(self.dr_min, min(self.dr_max, dr))
        return (clamped - self.dr_min) / (self.dr_max - self.dr_min)
    def normalized_scores(self) -> List[float]: return [self.normalize_single_score(s) for s in self.scores]
    def mastery(self) -> Tuple[bool, float]:
        if len(self.scores) < self.window: return False, 0.0
        ns = self.normalized_scores()
        avg = float(np.mean(ns)); score_variance = float(np.var(ns))
        return avg >= self.solve_threshold_norm and score_variance > 1e-4, avg

class TaskLibrary:
    def __init__(self):
        self.tasks = {}; self.task_order = []; self.task_id_map = {}
    def register(self, task_id: int, spec: TaskSpec):
        self.tasks[spec.name] = spec
        if spec.name not in self.task_order: self.task_order.append(spec.name)
        self.task_id_map[spec.name] = task_id
        logging.info(f"Registered task {task_id} ('{spec.name}') score_metric='{spec.score_metric}' range=[{spec.reward_min}, {spec.reward_max}]")
    def choose_task(self) -> Tuple[int, str]:
        unmastered = [n for n, s in self.tasks.items() if not s.mastery()[0]]
        chosen = np.random.choice(unmastered) if np.random.rand() < 0.9 and unmastered else np.random.choice(self.task_order)
        return self.task_id_map[chosen], chosen
    def update_score(self, task_name: str, score: float): self.tasks[task_name].update(score)
    def mastery_report(self) -> Dict:
        return {n: {"mastered": s.mastery()[0], "norm_avg": round(s.mastery()[1],3), "raw_recent_avg": round(np.mean(s.scores) if s.scores else 0.0, 1)} for n, s in self.tasks.items()}

class MultiTaskWendigoEnv(gym.Env):
    def __init__(self, task_library: TaskLibrary):
        super().__init__()
        self.task_lib = task_library
        self.envs = {"cartpole": gym.make("CartPole-v1"), "pendulum": gym.make("InvertedPendulum-v4"), "mountaincar_cont": gym.make("MountainCarContinuous-v0")}
        self.action_space = self.envs["pendulum"].action_space
        self.num_tasks = len(self.task_lib.task_order)
        self.current_env = None
    def _select_task(self):
        self.current_task_id, self.current_task_name = self.task_lib.choose_task()
        self.current_env = self.envs[self.current_task_name]
        self.observation_space = self.current_env.observation_space
    def reset(self, seed=None, options=None):
        super().reset(seed=seed); self._select_task()
        obs, info = self.current_env.reset(seed=seed, options=options)
        info.update({"task_id": self.current_task_id, "task_name": self.current_task_name})
        return obs, info
    def step(self, action):
        raw_action = action.copy()
        if self.current_task_name == "cartpole": processed_action = 0 if action[0] < 0 else 1
        elif self.current_task_name == "pendulum": processed_action = action * 2.0
        else: processed_action = action
        obs, reward, done, truncated, info = self.current_env.step(processed_action)
        info.update({"task_id": self.current_task_id, "task_name": self.current_task_name, "raw_action": raw_action})
        return obs, reward, done, truncated, info
    def close(self): [env.close() for env in self.envs.values()]

@dataclass
class GoldEpisode:
    task_id: int; task_name: str; score: float; mean_dr: float; transitions: List[Tuple]; vigor: int; rigor: int

class GoldWindow:
    def __init__(self, max_size: int = 64): self.buffer = deque(maxlen=max_size)
    def maybe_add(self, episode: GoldEpisode):
        self.buffer.append(episode)
        self.buffer = deque(sorted(list(self.buffer), key=lambda x: x.mean_dr), maxlen=self.buffer.maxlen)

class GlobalTopKNorm:
    def __init__(self, k=15): self.k = k; self.items = []
    def add(self, task_name, score, task_lib):
        norm_score = task_lib.tasks[task_name].normalize_single_score(score)
        self.items.append((norm_score, task_name, score))
        self.items = sorted(self.items, key=lambda x: x[0], reverse=True)[:self.k]
    def average_norm(self): return np.mean([item[0] for item in self.items]) if self.items else 0.0

class AutopoieticReplayBuffer:
    def __init__(self, max_size=5000): self.max_size = max_size; self.items = []
    def maybe_add(self, task_id: int, transition: Tuple, dr: float):
        priority = 1.0/(dr+1e-3) + (dr if dr>2.5 else 0.0)
        self.items.append((priority, dr, task_id, transition))
        self.items = sorted(self.items, key=lambda x:x[0], reverse=True)[:self.max_size]
    def sample(self, k: int = 64) -> List[Tuple]:
        if not self.items: return []
        return [x[3] for x in self.items[:min(k, len(self.items))]]

class Actor(nn.Module):
    def __init__(self, s_dim, a_dim, min_log=-20, max_log=2):
        super().__init__(); self.min_log, self.max_log = min_log, max_log
        self.net = nn.Sequential(nn.Linear(s_dim, 256), nn.ReLU(), nn.Linear(256, 256), nn.ReLU(), nn.Linear(256, 2*a_dim))
    def forward(self, s): mean, log_std = self.net(s).chunk(2, -1); return mean, th.clamp(log_std, self.min_log, self.max_log).exp()

class Critic(nn.Module):
    def __init__(self, s_dim, a_dim):
        super().__init__(); self.net = nn.Sequential(nn.Linear(s_dim+a_dim, 256), nn.ReLU(), nn.Linear(256, 256), nn.ReLU(), nn.Linear(256, 1))
    def forward(self, s, a): return self.net(th.cat([s, a], -1))

class PredictiveHead(nn.Module):
    def __init__(self):
        super().__init__(); self.net = nn.Sequential(nn.Linear(6,64), nn.ReLU(), nn.Linear(64,32), nn.ReLU(), nn.Linear(32,3))
    def forward(self, x): return self.net(x)

class CoherenceHead(nn.Module):
    def __init__(self):
        super().__init__(); self.net = nn.Sequential(nn.Linear(4,64), nn.ReLU(), nn.Linear(64,32), nn.ReLU(), nn.Linear(32,1))
    def forward(self, x): return self.net(x)

class SAC:
    def __init__(self, s_dim, a_dim, lr=3e-4, gamma=0.99, tau=0.005, alpha=0.2):
        self.actor = Actor(s_dim, a_dim).to(device)
        self.c1, self.c2 = Critic(s_dim, a_dim).to(device), Critic(s_dim, a_dim).to(device)
        self.tc1, self.tc2 = Critic(s_dim, a_dim).to(device), Critic(s_dim, a_dim).to(device)
        self.tc1.load_state_dict(self.c1.state_dict()); self.tc2.load_state_dict(self.c2.state_dict())
        self.a_opt, self.c1_opt, self.c2_opt = optim.Adam(self.actor.parameters(), lr), optim.Adam(self.c1.parameters(), lr), optim.Adam(self.c2.parameters(), lr)
        self.gamma, self.tau, self.alpha = gamma, tau, alpha
        self.replay = deque(maxlen=int(1e6))
    def select_action(self, s):
        with th.no_grad(): mean, std = self.actor(th.FloatTensor(s).to(device)); return Normal(mean, std).sample().cpu().numpy()
    def update(self, size):
        if len(self.replay) < size: return
        batch = [self.replay[i] for i in np.random.choice(len(self.replay), size, replace=False)]
        s, a, ns, r, d = map(lambda x: th.FloatTensor(np.array(x)).to(device), zip(*batch))
        r, d = r.unsqueeze(1), d.unsqueeze(1)
        with th.no_grad():
            nm, nstd = self.actor(ns); nd = Normal(nm, nstd); na = nd.sample()
            nlp = nd.log_prob(na).sum(-1, keepdim=True)
            min_q = th.min(self.tc1(ns, na), self.tc2(ns, na)) - self.alpha * nlp
            tq = r + (1-d) * self.gamma * min_q
        q1, q2 = self.c1(s, a), self.c2(s, a)
        c1l, c2l = nn.MSELoss()(q1, tq), nn.MSELoss()(q2, tq)
        self.c1_opt.zero_grad(); c1l.backward(); self.c1_opt.step()
        self.c2_opt.zero_grad(); c2l.backward(); self.c2_opt.step()
        m, std = self.actor(s); dist = Normal(m, std); na = dist.sample(); lp = dist.log_prob(na).sum(-1, keepdim=True)
        al = (self.alpha*lp - th.min(self.c1(s, na), self.c2(s, na))).mean()
        self.a_opt.zero_grad(); al.backward(); self.a_opt.step()
        for t, p in zip(self.tc1.parameters(), self.c1.parameters()): t.data.copy_(self.tau*p.data + (1-self.tau)*t.data)
        for t, p in zip(self.tc2.parameters(), self.c2.parameters()): t.data.copy_(self.tau*p.data + (1-self.tau)*t.data)
    def add_to_replay_buffer(self, s, a, ns, r, d): self.replay.append((s,a,ns,r,d))
    def save(self, p): th.save({'a':self.actor.state_dict(),'c1':self.c1.state_dict(),'c2':self.c2.state_dict()}, f"{p}_sac.pth")
    def load(self, p): d = th.load(f"{p}_sac.pth"); self.actor.load_state_dict(d['a']); self.c1.load_state_dict(d['c1']); self.c2.load_state_dict(d['c2']); self.tc1.load_state_dict(self.c1.state_dict()); self.tc2.load_state_dict(self.c2.state_dict())

class WendigoMultiAgent:
    def __init__(self, env: MultiTaskWendigoEnv):
        self.env, self.state_dim, self.action_dim = env, 4, 1 # Use fixed dims for simplicity
        self.sac = SAC(self.state_dim, self.action_dim)
        self.coh_head, self.pred_head = CoherenceHead().to(device), PredictiveHead().to(device)
        self.coh_opt, self.pred_opt = optim.Adam(self.coh_head.parameters(), 1e-4), optim.Adam(self.pred_head.parameters(), 1e-4)
        self.dark_hist, self.autopoietic_buf = deque(maxlen=2000), deque(maxlen=20)
        self.lambda_coh, self.lambda_pred, self.alpha_res = 0.5, 0.5, 0.25
        self.anneal = 500; self.global_episode = 0
        self.wound_channels = {n: WoundChannelMemory(s.state_dim, 150) for n, s in env.task_lib.tasks.items()}
    def _pad(self, obs): padded = np.zeros(self.state_dim); min_len = min(len(obs), self.state_dim); padded[:min_len] = obs[:min_len]; return padded
    def predict_action(self, obs):
        ts = getattr(self, 'last_teacher_signal', 0.5)
        act = self.sac.select_action(self._pad(obs)) if np.random.rand() > ts else self.env.action_space.sample()
        return act, "Vigor" if np.random.rand() > ts else "Rigor"
    def step_learn(self, o, a, no, r, d):
        self.sac.add_to_replay_buffer(self._pad(o), a, self._pad(no), r, float(d))
        if self.global_episode > 10: self.sac.update(128)
    def train_coh_head(self, mdr, vr, eln, tid, score, ts):
        x, y = th.tensor([[mdr,vr,eln,tid]], device=device), th.tensor([[ts.normalize_single_score(score)]], device=device)
        loss = nn.MSELoss()(self.coh_head(x), y); self.coh_opt.zero_grad(); loss.backward()
        for p in self.coh_head.parameters(): p.grad *= self.lambda_coh
        self.coh_opt.step(); return float(loss.item())
    def predict_coh_score(self, mdr, vr, eln, tid):
        with th.no_grad(): return float(self.coh_head(th.tensor([[mdr,vr,eln,tid]], device=device)).clamp(0,1).item())
    def train_pred_head(self, mdr, vr, eln, dtn, chn, score, tid, ts, ep_idx):
        sn, mdrn = ts.normalize_single_score(score), ts.normalize_dr(mdr)
        a = max(0.1, 1-(ep_idx/self.anneal)); lag_t = float(np.clip(a*sn + (1-a)*(sn-self.alpha_res*mdr), 0,1))
        x, y = th.tensor([[mdr,vr,eln,dtn,chn,tid]], device=device), th.tensor([[sn, lag_t, mdrn]], device=device)
        out = self.pred_head(x); sh, lh, dh = out[0,0], out[0,1], out[0,2]
        loss = ((sh-y[0,0])**2) + 0.5*((lh-y[0,1])**2) + 0.5*((dh-y[0,2])**2)
        self.pred_opt.zero_grad(); loss.backward()
        for p in self.pred_head.parameters(): p.grad *= self.lambda_pred
        self.pred_opt.step(); self.last_teacher_signal = float(lh.clamp(0,1).item())
        return float(loss.item()), float(sh.item()), float(lh.item()), lag_t, float(dh.item())
    def sharpen(self, transitions):
        if not transitions or len(transitions) < 10: return
        correct_shape = [t for t in transitions if np.shape(t[1])==(self.action_dim,)]
        if len(correct_shape) < 10: return
        s, a, ns, r, _, d, _ = zip(*correct_shape)
        s, a, ns, r, d = [th.FloatTensor(np.array(x)).to(device) for x in [s,a,ns,r,d]]
        r, d = r.unsqueeze(1), d.unsqueeze(1)
        with th.no_grad():
            nm,nstd=self.sac.actor(ns);nd=Normal(nm,nstd);na=nd.sample();nlp=nd.log_prob(na).sum(-1,keepdim=True)
            min_q = th.min(self.sac.tc1(ns,na), self.sac.tc2(ns,na))-self.sac.alpha*nlp; tq=r+(1-d)*self.sac.gamma*min_q
        cl = sum(nn.MSELoss()(c(s,a), tq) for c in [self.sac.c1,self.sac.c2])
        self.sac.c1_opt.zero_grad(); self.sac.c2_opt.zero_grad(); cl.backward(); self.sac.c1_opt.step(); self.sac.c2_opt.step()

# --- Main ---
def main():
    task_lib = TaskLibrary()
    task_lib.register(0, TaskSpec("cartpole", 0, 500, .95, "steps", 500, 4, dr_max=2.))
    task_lib.register(1, TaskSpec("pendulum", -1600., 0., .8, "reward", 200, 3, dr_max=5.))
    task_lib.register(2, TaskSpec("mountaincar_cont", -100., 100., .95, "reward", 999, 2, dr_max=1.))
    
    env = MultiTaskWendigoEnv(task_lib)
    agent = WendigoMultiAgent(env)
    gold, auto_buf, leaderboard = GoldWindow(), AutopoieticReplayBuffer(), GlobalTopKNorm()
    
    for ep in range(1, 751):
        agent.global_episode = ep
        obs, info = env.reset()
        task_id, task_name = info["task_id"], info["task_name"]
        spec, channel = task_lib.tasks[task_name], agent.wound_channels[task_name]
        
        done, trunc, ep_r, ep_s, ep_dr, v_ct, r_ct = False, False, 0., 0, 0., 0, 0
        prev_obs, ep_trans, dr_vals = obs, [], []

        while not done and not trunc:
            action, mode = agent.predict_action(obs)
            if mode=="Vigor": v_ct+=1
            else: r_ct+=1
            
            next_obs, env_r, done, trunc, step_info = env.step(action)
            
            if task_name == "cartpole": dark = dark_residue_cartpole(next_obs); sr = env_r - 0.05*dark
            elif task_name == "pendulum": dark = dark_residue_pendulum_helical(next_obs, step_info["raw_action"][0], prev_obs); sr = (env_r/10.)-0.2*dark
            elif task_name == "mountaincar_cont": dark = dark_residue_mountaincar_arrow(next_obs, step_info["raw_action"][0]); sr = env_r - 0.1*dark
            else: dark, sr = 0., env_r

            sr -= 0.1 * channel.get_inertial_force(next_obs - obs)
            agent.dark_hist.append(dark); dr_vals.append(dark); channel.update(obs)
            
            trans = (obs, action, next_obs, sr, dark, done or trunc, task_id)
            ep_trans.append(trans); auto_buf.maybe_add(task_id, trans, dark)
            agent.step_learn(obs, action, next_obs, sr, done or trunc)

            obs, prev_obs = next_obs, obs
            ep_r += env_r; ep_s += 1; ep_dr += dark

        score = ep_r if spec.score_metric == "reward" else ep_s
        mean_dr = ep_dr/ep_s
        task_lib.update_score(task_name, score)
        leaderboard.add(task_name, score, task_lib)
        
        agent.train_coh_head(mean_dr, v_ct/(v_ct+r_ct if v_ct+r_ct>0 else 1), ep_s/spec.step_cap, task_id/2., score, spec)
        coh_pred = agent.predict_coh_score(mean_dr, v_ct/(v_ct+r_ct if v_ct+r_ct>0 else 1), ep_s/spec.step_cap, task_id/2.)
        agent.train_pred_head(mean_dr, v_ct/(v_ct+r_ct if v_ct+r_ct>0 else 1), ep_s/spec.step_cap, leaderboard.average_norm()*0.75, coh_pred, score, task_id/2., spec, ep)

        if spec.mastery()[0] and mean_dr < agent.current_dark_median()*0.8:
            gold.maybe_add(GoldEpisode(task_id, task_name, score, mean_dr, ep_trans, v_ct, r_ct))
        if ep > 20: agent.sharpen(auto_buf.sample())

        run_type = "Coherent" if mean_dr <= agent.current_dark_median() else "Dissonant"
        print(f"Ep {ep}: {run_type} ({task_name}) Score: {score:.1f}, DR: {mean_dr:.2f}, V/R: {v_ct}/{r_ct}, Gold: {len(gold.buffer)}")
        
        if ep % 25 == 0:
            logging.info(f"--- Episode {ep} Summary ---")
            logging.info(f"Mastery: {json.dumps(task_lib.mastery_report())}")
            leaderboard_log = [(round(n, 2), t, int(s)) for n, t, s in leaderboard.items]
            logging.info(f"Top-15: {leaderboard_log} | AvgNorm={leaderboard.average_norm():.3f}")

        if ep % 100 == 0: agent.sac.save(f"wendigo_8_ep{ep}")

    agent.sac.save("wendigo_8_final")
    env.close()

if __name__ == "__main__":
    main()
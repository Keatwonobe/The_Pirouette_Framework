import gymnasium as gym
import numpy as np
import os
import pickle


# ---------------------------------------------------------------------------
# Static Reader: maps a low-D static vector to action logits
# ---------------------------------------------------------------------------

class StaticReader:
    """
    Ultra-light static policy WITHOUT requiring dim % n_actions == 0.

    We interpret the static vector as:
      - W_flat: first (n_actions * obs_dim) entries
      - b:      remaining entries (or zero if not enough)
    """

    def __init__(self, dim: int, n_actions: int, obs_dim: int = 8):
        self.dim = dim
        self.n_actions = n_actions
        self.obs_dim = obs_dim

        # How many weights do we really need?
        self.W_size = n_actions * obs_dim

        # If static_vec < needed, we wrap/pad inside act() dynamically.
        # No strict assertion needed.
        # This keeps things cheap and extremely robust.
        pass

    def act(self, static_vec: np.ndarray, obs: np.ndarray) -> int:
        # Pad or tile obs to obs_dim
        if obs.shape[0] >= self.obs_dim:
            o = obs[:self.obs_dim]
        else:
            reps = (self.obs_dim + obs.shape[0] - 1) // obs.shape[0]
            o = np.tile(obs, reps)[:self.obs_dim]

        # Ensure static_vec is long enough
        if len(static_vec) < self.W_size:
            reps = (self.W_size + len(static_vec) - 1) // len(static_vec)
            sv = np.tile(static_vec, reps)[:self.W_size]
        else:
            sv = static_vec[:self.W_size]

        # Build W
        W = sv.reshape(self.n_actions, self.obs_dim)

        # Compute logits
        logits = W @ o

        # Softmax
        logits = logits - np.max(logits)
        probs = np.exp(logits)
        probs /= np.sum(probs)

        return int(np.random.choice(self.n_actions, p=probs))



# ---------------------------------------------------------------------------
# Environment-specific configs (safety + action mapping)
# ---------------------------------------------------------------------------

def build_env_config(env, env_id: str):
    """
    Build a small config dict for the given environment:

      - n_actions: size of discrete action space used by StaticReader
      - action_transform: maps action_idx -> env_action
      - safety_fn: (obs, terminated, truncated) -> (stability, failure_dir)
    """

    # --------- Action mapping (discrete or discretized) ---------
    from gymnasium.spaces import Discrete, Box

    if isinstance(env.action_space, Discrete):
        # Native discrete (CartPole, Acrobot)
        n_actions = env.action_space.n

        def action_transform(a_idx: int):
            return int(a_idx)

    elif isinstance(env.action_space, Box) and env_id.startswith("Pendulum"):
        # Discretize Pendulum's continuous torque into a few bins
        # Cheap and simple: {-2, 0, +2}
        torque_values = np.array([-2.0, 0.0, 2.0], dtype=np.float32)
        n_actions = torque_values.shape[0]

        def action_transform(a_idx: int, torques=torque_values):
            # env expects float or array-like; we give small array
            return np.array([torques[a_idx]], dtype=np.float32)

    else:
        raise NotImplementedError(
            f"Env {env_id} has unsupported action space: {env.action_space}"
        )

    # --------- Safety / "what didn't happen" shaping ---------

    if env_id == "CartPole-v1":
        x_thresh = env.unwrapped.x_threshold
        theta_thresh = env.unwrapped.theta_threshold_radians

        def safety_fn(obs, terminated: bool, truncated: bool):
            """
            Stability ~ centered cart + upright pole, in [0, 1].
            """
            x, x_dot, theta, theta_dot = obs

            # margins: 1.0 when centered and upright, 0.0 at the threshold
            margin_x = max(0.0, 1.0 - abs(x) / x_thresh)
            margin_theta = max(0.0, 1.0 - abs(theta) / theta_thresh)

            stability = 0.5 * (margin_x + margin_theta)

            failure_dir = 0.0
            if terminated or truncated:
                failure_dir = float(np.sign(theta))

            return stability, failure_dir

    elif env_id.startswith("Pendulum"):
        # Pendulum state: [cos(theta), sin(theta), theta_dot]
        # Upright is theta == 0. Downward is +/- pi.
        max_speed = getattr(env.unwrapped, "max_speed", 8.0)

        def safety_fn(obs, terminated: bool, truncated: bool):
            cos_th, sin_th, thdot = obs

            angle = np.arctan2(sin_th, cos_th)  # [-pi, pi]
            angle_dist = abs(angle)             # 0 at upright

            margin_angle = max(0.0, 1.0 - angle_dist / np.pi)
            margin_speed = max(
                0.0,
                1.0 - min(1.0, abs(thdot) / (max_speed if max_speed > 0 else 1.0))
            )

            stability = 0.5 * (margin_angle + margin_speed)

            failure_dir = 0.0
            if terminated or truncated:
                failure_dir = float(np.sign(angle))

            return stability, failure_dir

    elif env_id.startswith("Acrobot"):
        # Acrobot state: [cos(theta1), sin(theta1),
        #                cos(theta2), sin(theta2),
        #                thetaDot1, thetaDot2]
        # Goal: raise end-effector above a threshold height.
        # We approximate "stability" as how raised the links are.
        def safety_fn(obs, terminated: bool, truncated: bool):
            cos1, sin1, cos2, sin2, thdot1, thdot2 = obs

            cos_sum = cos1 + cos2  # ≈ 2 when hanging down, ≈ -2 when raised
            # Map cos_sum ∈ [-2, 2] to stability ∈ [0, 1], where raised ~ 1
            stability = (2.0 - cos_sum) / 4.0
            stability = max(0.0, min(1.0, stability))

            failure_dir = 0.0
            if terminated or truncated:
                failure_dir = float(np.sign(cos_sum))

            return stability, failure_dir

    else:
        # Fallback: no extra stability information — just return 0
        def safety_fn(obs, terminated: bool, truncated: bool):
            return 0.0, 0.0

    return {
        "env_id": env_id,
        "n_actions": n_actions,
        "action_transform": action_transform,
        "safety_fn": safety_fn,
    }


# ---------------------------------------------------------------------------
# Evaluation with composite fitness (return + stability + late margin)
# ---------------------------------------------------------------------------

def evaluate_static(
    env,
    reader: StaticReader,
    static_vec: np.ndarray,
    cfg: dict,
    n_episodes: int = 5,
    lambda_stab: float = 5.0,
    lambda_margin: float = 10.0,
    last_k_margin: int = 10,
):
    """
    Evaluate a single static vector by running multiple episodes.

    Returns:
      fitness, mean_return, mean_stability, mean_margin_last_k
    """
    returns = []
    stab_scores = []
    margins_last = []

    safety_fn = cfg["safety_fn"]
    action_transform = cfg["action_transform"]

    for _ in range(n_episodes):
        obs, _ = env.reset()
        done = False
        ep_ret = 0.0
        stability_traj = []

        while not done:
            a_idx = reader.act(static_vec, obs)
            env_action = action_transform(a_idx)

            obs_next, reward, terminated, truncated, _info = env.step(env_action)

            stability, failure_dir = safety_fn(obs_next, terminated, truncated)
            stability_traj.append(stability)

            ep_ret += reward
            obs = obs_next
            done = terminated or truncated

        returns.append(ep_ret)
        stab_scores.append(float(np.mean(stability_traj)))

        # stability over the last_k steps = how "clean" the landing / ending was
        if len(stability_traj) >= last_k_margin:
            margins_last.append(
                float(np.mean(stability_traj[-last_k_margin:]))
            )
        else:
            margins_last.append(float(np.mean(stability_traj)))

    mean_return = float(np.mean(returns))
    mean_stab = float(np.mean(stab_scores))
    mean_margin_last = float(np.mean(margins_last))

    # Composite fitness: "what we did" + "what didn't happen"
    fitness = (
        mean_return
        + lambda_stab * mean_stab
        + lambda_margin * mean_margin_last
    )

    return fitness, mean_return, mean_stab, mean_margin_last


def eval_return_only(
    env,
    reader: StaticReader,
    static_vec: np.ndarray,
    cfg: dict,
    n_episodes: int = 20,
) -> float:
    """
    For final evaluation: pure average return, no safety bonuses.
    """
    returns = []
    action_transform = cfg["action_transform"]

    for _ in range(n_episodes):
        obs, _ = env.reset()
        done = False
        ep_ret = 0.0
        while not done:
            a_idx = reader.act(static_vec, obs)
            env_action = action_transform(a_idx)

            obs, r, terminated, truncated, _ = env.step(env_action)
            ep_ret += r
            done = terminated or truncated
        returns.append(ep_ret)
    return float(np.mean(returns))


# ---------------------------------------------------------------------------
# Evolutionary loop: static → coherence via pressure
# ---------------------------------------------------------------------------

def run_static_bifurcation(
    env_id: str = "CartPole-v1",
    pop_size: int = 64,
    dim: int = 8,
    generations: int = 25,
    sigma_init: float = 0.5,
    elite_frac: float = 0.2,
    n_eval: int = 5,
    seed: int | None = None,
    ckpt_dir: str = "checkpoints"  # <--- New argument
):
    """
    Ultralight ES loop with Checkpointing.
    """
    print(f"\n=== Running static bifurcation on {env_id} ===")

    # Ensure checkpoint directory exists
    os.makedirs(ckpt_dir, exist_ok=True)
    ckpt_path = os.path.join(ckpt_dir, f"{env_id}_ckpt.pkl")

    if seed is not None:
        np.random.seed(seed)

    env = gym.make(env_id)
    cfg = build_env_config(env, env_id)

    reader = StaticReader(
        dim=dim,
        n_actions=cfg["n_actions"],
        obs_dim=env.observation_space.shape[0]
    )

    # --- CHECKPOINT LOADING ---
    start_gen = 1
    pop = None
    hall_best = None
    hall_fitness = -np.inf

    if os.path.exists(ckpt_path):
        try:
            print(f"Found checkpoint: {ckpt_path}. Resuming...")
            with open(ckpt_path, "rb") as f:
                state = pickle.load(f)
                pop = state["pop"]
                hall_best = state["hall_best"]
                hall_fitness = state["hall_fitness"]
                start_gen = state["gen"] + 1
                # Restore RNG state if you want exact reproducibility, 
                # but for ES, restoring population is usually enough.
        except Exception as e:
            print(f"Failed to load checkpoint (starting fresh): {e}")

    # If no checkpoint (or failed load), initialize fresh
    if pop is None:
        pop = np.random.randn(pop_size, dim) * sigma_init

    # --- MAIN LOOP ---
    # If we resumed, start_gen will be > 1
    for gen in range(start_gen, generations + 1):
        fitnesses = np.zeros(pop_size, dtype=np.float32)
        returns = np.zeros(pop_size, dtype=np.float32)
        
        # Evaluate each static vector
        for i in range(pop_size):
            fit, r, s, m = evaluate_static(
                env,
                reader,
                pop[i],
                cfg,
                n_episodes=n_eval,
                lambda_stab=5.0,
                lambda_margin=10.0,
                last_k_margin=10,
            )
            fitnesses[i] = fit
            returns[i] = r

        # Track hall-of-fame
        gen_best_idx = int(np.argmax(fitnesses))
        gen_best_fit = float(fitnesses[gen_best_idx])
        gen_best_ret = float(returns[gen_best_idx])

        if gen_best_fit > hall_fitness or hall_best is None:
            hall_fitness = gen_best_fit
            hall_best = pop[gen_best_idx].copy()

        print(
            f"[Gen {gen:3d}] "
            f"GenBestRet={gen_best_ret:8.2f}  "
            f"GenMeanRet={returns.mean():8.2f}  "
            f"HallFit={hall_fitness:10.2f}"
        )

        # Selection
        elite_count = max(1, int(elite_frac * pop_size))
        elite_idx = np.argsort(fitnesses)[-elite_count:]
        elites = pop[elite_idx]

        # Reproduce
        new_pop = []
        for _ in range(pop_size):
            parent = elites[np.random.randint(elite_count)]
            child = parent + np.random.randn(dim) * sigma_init
            new_pop.append(child)
        pop = np.stack(new_pop, axis=0)

        # --- CHECKPOINT SAVING ---
        # Save at the end of every generation
        state = {
            "pop": pop,
            "hall_best": hall_best,
            "hall_fitness": hall_fitness,
            "gen": gen
        }
        # Write to temp file then rename to avoid corruption if crash happens during write
        temp_path = ckpt_path + ".tmp"
        with open(temp_path, "wb") as f:
            pickle.dump(state, f)
        os.replace(temp_path, ckpt_path)

    # --- FINAL EVALUATION ---
    if hall_best is not None:
        fit, r, s, m = evaluate_static(env, reader, hall_best, cfg, n_episodes=10)
        print("\n=== Final Hall-of-Fame Evaluation ===")
        print(f"Hall mean composite fitness:               {fit:.2f}")
        print(f"Hall mean return (with stepwise bonuses):  {r:.2f}")
        true_mean = eval_return_only(env, reader, hall_best, cfg, n_episodes=50)
        print(f"Hall mean *true* return (no bonuses):      {true_mean:.2f}")
    else:
        print("No hall-of-fame vector recorded; something went wrong.")

    env.close()

    # Remove checkpoint on successful completion so next run starts fresh
    if os.path.exists(ckpt_path):
        os.remove(ckpt_path)
        print("Run complete. Checkpoint removed.")
    
    return hall_best


if __name__ == "__main__":
    # Cheap multi-env sweep; comment out any you don't want.
    # CartPole: easy, quick sanity check.
    #run_static_bifurcation(
        #env_id="CartPole-v1",
        #pop_size=64,
        #dim=8,
        #generations=25,
        #sigma_init=0.5,
        #elite_frac=0.2,
        #n_eval=5,
        #seed=0,
    #)

    # Pendulum: discretized torque, negative rewards; harder.
    run_static_bifurcation(
        env_id="Pendulum-v1",
        pop_size=64,
        dim=8,         # still fine; obs is 3D and we truncate/pad
        generations=8000,
        sigma_init=0.5,
        elite_frac=0.2,
        n_eval=5,
        seed=1,
    )

    # Acrobot: underactuated, trickier; treated as "level above".
    run_static_bifurcation(
        env_id="Acrobot-v1",
        pop_size=64,
        dim=12,        # 3 actions × 4 dims per action
        generations=50,
        sigma_init=0.5,
        elite_frac=0.2,
        n_eval=5,
        seed=2,
    )

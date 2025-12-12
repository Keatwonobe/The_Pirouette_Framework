# static_agent_v2.py
import gymnasium as gym
import numpy as np

# -----------------------
# Config
# -----------------------
ENV_ID = "CartPole-v1"

POP_SIZE = 32          # number of macros per generation
ELITE_FRAC = 0.25      # fraction of elites kept each generation
EVAL_ROLLOUTS = 5      # <-- each macro tested this many times
GENERATIONS = 200      # number of generations
MACRO_LEN = 64         # length of the static sequence (time texture)
MUTATION_STD = 0.10    # noise added to elites to create children

RNG = np.random.default_rng(42)


# -----------------------
# Macro Representation
# -----------------------
class StaticMacro:
    """
    A macro is a greyscale vector z in [0,1]^MACRO_LEN.
    At step t, we read z[t % MACRO_LEN] and turn it into a discrete action
    via a value->index lookup.
    """

    def __init__(self, n_actions, macro_len=MACRO_LEN, init=None):
        self.n_actions = n_actions
        self.macro_len = macro_len
        if init is None:
            # random static in [0,1]
            self.z = RNG.random(macro_len)
        else:
            self.z = np.clip(init.copy(), 0.0, 1.0)

    def act(self, t: int) -> int:
        """
        Deterministic "Ki rhythm": at each time step t we *must* pick an action.
        No no-op, just read the texture.
        """
        idx = t % self.macro_len
        v = float(self.z[idx])  # in [0,1]
        # map v to [0, n_actions-1]
        a = int(v * self.n_actions)
        if a == self.n_actions:  # handle edge case when v==1.0
            a = self.n_actions - 1
        return a

    def mutated(self, std=MUTATION_STD) -> "StaticMacro":
        """
        Add Gaussian noise and re-clamp to [0,1].
        """
        new_z = np.clip(self.z + RNG.normal(scale=std, size=self.z.shape),
                        0.0, 1.0)
        return StaticMacro(self.n_actions, self.macro_len, init=new_z)


# -----------------------
# Evaluation
# -----------------------
def run_episode(env, macro: StaticMacro, render: bool = False) -> float:
    """
    Run one episode using a fixed macro as an open-loop-ish policy.
    We still feed env observations, but macro doesn't look at them.
    """
    obs, info = env.reset()
    total_reward = 0.0
    t = 0

    done = False
    while not done:
        action = macro.act(t)   # Ki: must move every time step
        obs, reward, terminated, truncated, info = env.step(action)
        total_reward += reward
        t += 1
        done = terminated or truncated

        if render:
            env.render()

    return total_reward


def evaluate_macro(env, macro: StaticMacro,
                   n_rollouts: int = EVAL_ROLLOUTS) -> float:
    """
    Evaluate a macro multiple times and return mean return.
    This is the key "whole policy" view you wanted.
    """
    returns = []
    for _ in range(n_rollouts):
        ret = run_episode(env, macro)
        returns.append(ret)
    return float(np.mean(returns))


# -----------------------
# Training Loop (ES-style)
# -----------------------
def train_static_agent():
    env = gym.make(ENV_ID)
    n_actions = env.action_space.n

    # Initial population
    population = [StaticMacro(n_actions) for _ in range(POP_SIZE)]
    hall_of_fame = None   # (macro, score)
    hall_best_score = -np.inf

    n_elite = max(1, int(POP_SIZE * ELITE_FRAC))

    for gen in range(1, GENERATIONS + 1):
        scores = []
        for macro in population:
            score = evaluate_macro(env, macro)
            scores.append(score)

        scores = np.array(scores)
        gen_best_idx = int(np.argmax(scores))
        gen_best_score = float(scores[gen_best_idx])
        gen_mean = float(np.mean(scores))

        # Update hall-of-fame with a re-check so we don't bless pure luck
        candidate = population[gen_best_idx]
        candidate_confirm = evaluate_macro(env, candidate)
        if candidate_confirm > hall_best_score:
            hall_best_score = candidate_confirm
            hall_of_fame = StaticMacro(n_actions, MACRO_LEN,
                                       init=candidate.z.copy())

        print(
            f"[Gen {gen:3d}] "
            f"GenBest={gen_best_score:.1f}  "
            f"GenMean={gen_mean:.1f}  "
            f"HallBest={hall_best_score:.1f}"
        )

        # ------------------
        # ES reproduction
        # ------------------
        # Select elites
        elite_indices = np.argsort(scores)[-n_elite:]
        elites = [population[i] for i in elite_indices]

        # Create new population:
        #   - keep elites
        #   - fill rest with mutations of elites
        new_population = []
        for e in elites:
            new_population.append(StaticMacro(n_actions, MACRO_LEN, init=e.z))

        while len(new_population) < POP_SIZE:
            parent = elites[RNG.integers(0, len(elites))]
            child = parent.mutated()
            new_population.append(child)

        population = new_population

    env.close()

    # One more sanity check on the champion
    if hall_of_fame is not None:
        print("\n=== Final Hall-of-Fame Evaluation ===")
        env = gym.make(ENV_ID, render_mode=None)
        final_score = evaluate_macro(env, hall_of_fame, n_rollouts=10)
        print(f"Champion mean return over 10 eval episodes: {final_score:.1f}")
        env.close()


if __name__ == "__main__":
    train_static_agent()

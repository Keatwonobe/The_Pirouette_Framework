import gymnasium as gym
import numpy as np
import random
from dataclasses import dataclass
from typing import List

# --- Static Macro Agent v0.1 ---
# Idea:
#   - Static = sequence of greyscale values in [0,1].
#   - A "reader" maps greyscale -> discrete actions via a dynamic histogram.
#   - Successful episodes:
#       * reinforce the reader's action weights
#       * bias selection & mutation toward better static macros.


@dataclass
class StaticMacro:
    id: int
    values: np.ndarray          # shape: [macro_len], floats in [0,1]
    mean_return: float = 0.0
    trials: int = 0

    def update_return(self, episode_return: float, beta: float = 0.1):
        """Exponential moving average of returns."""
        self.trials += 1
        if self.trials == 1:
            self.mean_return = episode_return
        else:
            self.mean_return = (1 - beta) * self.mean_return + beta * episode_return


class GreyscaleReader:
    """
    Maps greyscale value in [0,1] to an action index, using
    a dynamic histogram of action weights. Successful episodes
    increase weights for the actions that were used.
    """

    def __init__(self, n_actions: int, alpha: float = 0.1):
        self.n_actions = n_actions
        self.alpha = alpha
        self.weights = np.ones(n_actions, dtype=np.float32)  # start uniform

    def value_to_action(self, v: float) -> int:
        # Clamp to [0,1]
        v = float(max(0.0, min(1.0, v)))
        w = self.weights
        probs = w / w.sum()
        cdf = np.cumsum(probs)
        idx = int(np.searchsorted(cdf, v, side="right"))
        if idx >= self.n_actions:
            idx = self.n_actions - 1
        return idx

    def reinforce_episode(self, actions: List[int], success_scale: float = 1.0):
        """
        Increase weight for actions that appeared in a "good" episode.
        success_scale ∈ [0,1] scales how much we reinforce.
        """
        for a in actions:
            self.weights[a] += self.alpha * success_scale


class StaticAgent:
    def __init__(
        self,
        env_id: str = "CartPole-v1",
        pop_size: int = 16,
        macro_len: int = 32,
        mutation_scale: float = 0.15,
        elite_frac: float = 0.05,
        seed: int = 42,
    ):
        self.env_id = env_id
        self.env = gym.make(env_id)
        self.rng = np.random.RandomState(seed)
        self.pop_size = pop_size
        self.macro_len = macro_len
        self.mutation_scale = mutation_scale
        self.elite_frac = elite_frac

        n_actions = self.env.action_space.n
        self.reader = GreyscaleReader(n_actions=n_actions, alpha=0.05)

        self.population: List[StaticMacro] = []
        self._init_population()

    def _init_population(self):
        self.population = []
        for i in range(self.pop_size):
            vals = self.rng.rand(self.macro_len).astype(np.float32)
            self.population.append(StaticMacro(id=i, values=vals))

    def _mutate_macro(self, parent: StaticMacro, new_id: int) -> StaticMacro:
        noise = self.rng.randn(*parent.values.shape).astype(np.float32) * self.mutation_scale
        vals = parent.values + noise
        vals = np.clip(vals, 0.0, 1.0)
        return StaticMacro(id=new_id, values=vals)

    def _select_macro(self) -> StaticMacro:
        """
        Softmax over mean_return to bias toward better macros,
        but keep exploration if returns are similar.
        """
        means = np.array([m.mean_return for m in self.population], dtype=np.float32)
        if np.allclose(means, means[0]):
            # all equal (e.g. at start) -> uniform random
            return random.choice(self.population)

        temp = 10.0  # high temperature = gentle bias
        logits = means / temp
        logits -= logits.max()
        probs = np.exp(logits)
        probs /= probs.sum()
        idx = int(self.rng.choice(len(self.population), p=probs))
        return self.population[idx]

    def run(self, episodes: int = 2000, print_every: int = 50):
        best_return = -1e9
        best_macro = None

        for ep in range(1, episodes + 1):
            macro = self._select_macro()
            ep_return, ep_len, ep_actions = self._run_episode(macro)
            macro.update_return(ep_return)

            # For CartPole-v1, max return is 500; use that to scale success.
            success_scale = max(0.0, min(1.0, ep_return / 500.0))
            if success_scale > 0:
                self.reader.reinforce_episode(ep_actions, success_scale=success_scale)

            if ep_return > best_return:
                best_return = ep_return
                best_macro = macro

            if ep % print_every == 0:
                avg_ret = np.mean([m.mean_return for m in self.population])
                print(
                    f"[Ep {ep}] "
                    f"BestRet={best_return:.1f} | "
                    f"PopAvg={avg_ret:.1f} | "
                    f"ReaderWeights={self.reader.weights}"
                )
                # evolve the static population occasionally
                self._evolve_population()

        print("=== Training complete ===")
        print(f"Best return observed: {best_return:.1f}")
        if best_macro is not None:
            print(f"Best macro ID={best_macro.id}, mean_return={best_macro.mean_return:.1f}")
        self.env.close()

    def _run_episode(self, macro: StaticMacro):
        obs, info = self.env.reset()
        total_reward = 0.0
        actions_used: List[int] = []
        max_steps = 500  # safety cap

        for t in range(max_steps):
            v = macro.values[t % self.macro_len]   # looping through static
            a = self.reader.value_to_action(v)     # static -> action via reader

            obs, reward, terminated, truncated, info = self.env.step(a)
            total_reward += reward
            actions_used.append(a)

            if terminated or truncated:
                break

        return total_reward, len(actions_used), actions_used

    def _evolve_population(self):
        # Keep a fraction of the best macros and mutate them to refill the population.
        sorted_pop = sorted(self.population, key=lambda m: m.mean_return, reverse=True)
        n_elite = max(1, int(self.elite_frac * self.pop_size))
        elites = sorted_pop[:n_elite]

        new_pop: List[StaticMacro] = []
        # retain elites (relabel IDs)
        for i, e in enumerate(elites):
            e.id = i
            new_pop.append(e)

        # refill with mutated copies of elites
        next_id = len(new_pop)
        while len(new_pop) < self.pop_size:
            parent = random.choice(elites)
            child = self._mutate_macro(parent, new_id=next_id)
            new_pop.append(child)
            next_id += 1

        self.population = new_pop


if __name__ == "__main__":
    agent = StaticAgent(env_id="CartPole-v1")
    agent.run(episodes=2000, print_every=25)

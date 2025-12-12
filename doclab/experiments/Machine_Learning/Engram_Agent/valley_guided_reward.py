"""
Valley-guided intrinsic reward for Sand Humanoid

Reads successful_valleys.csv (from valley_crossing_detector.py) and
produces an intrinsic reward whenever the *shape* of a recent DR /
coherence window looks like one of the successful valleys.

Designed to be imported by sand_humanoid_engram.py but kept independent.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Dict

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------

@dataclass
class ValleyRewardConfig:
    csv_path: str = "successful_valleys.csv"
    reward_scale: float = 0.5    # how much intrinsic reward can add
    min_window: int = 30         # min steps in a window to consider
    max_window: int = 120        # max steps in a window to consider
    use_hemispheric_only: bool = False  # filter by is_hemispheric == True
    # how strongly to weight each summary feature when computing distance
    feature_weights: Dict[str, float] = None

    def __post_init__(self):
        if self.feature_weights is None:
            # sensible defaults; all of these appear in successful_valleys.csv
            self.feature_weights = {
                "duration": 0.5,
                "DR_increase": 1.0,
                "coherence_drop": 1.0,
                "net_coherence_gain": 1.0,
                "reconstruction_quality": 0.5,
                "valley_chatter": 0.5,
                "coherence_overshoot": 0.5,
            }


# ---------------------------------------------------------------------
# Library of successful valleys (summary level)
# ---------------------------------------------------------------------

class SuccessfulValleyLibrary:
    def __init__(self, cfg: ValleyRewardConfig):
        self.cfg = cfg
        self.df = self._load_csv(cfg.csv_path, cfg.use_hemispheric_only)
        if len(self.df) == 0:
            raise RuntimeError(f"No successful valleys loaded from {cfg.csv_path}")

        # precompute normalized feature vectors
        self.feature_names = list(cfg.feature_weights.keys())
        self.feature_matrix, self.feature_min, self.feature_max = self._normalize_features(self.df)

    @staticmethod
    def _load_csv(path: str, use_hemispheric_only: bool) -> pd.DataFrame:
        df = pd.read_csv(path)
        # basic filters
        if "is_successful" in df.columns:
            df = df[df["is_successful"] == True]
        if use_hemispheric_only and "is_hemispheric" in df.columns:
            df = df[df["is_hemispheric"] == True]
        return df.reset_index(drop=True)

    def _normalize_features(self, df: pd.DataFrame):
        feats = df[self.feature_names].astype(float).values
        fmin = feats.min(axis=0)
        fmax = feats.max(axis=0)
        # avoid divide by zero
        span = np.where((fmax - fmin) == 0.0, 1.0, (fmax - fmin))
        norm = (feats - fmin) / span
        return norm, fmin, fmax

    def describe(self) -> str:
        """Small helper for logging / debugging."""
        counts_by_duration = self.df["duration"].value_counts().sort_index()
        msg = ["SuccessfulValleyLibrary:"]
        msg.append(f"  n = {len(self.df)}")
        msg.append("  durations:")
        for d, c in counts_by_duration.items():
            msg.append(f"    {d:4d} steps -> {int(c)} valleys")
        return "\n".join(msg)


# ---------------------------------------------------------------------
# Online matcher: sliding-window valley detector
# ---------------------------------------------------------------------

class ValleyTrajectoryMatcher:
    """
    Maintains a sliding window of recent DR / coherence and returns
    an intrinsic reward when the window looks like a known successful valley.

    Usage pattern in training loop (pseudo):

        from valley_guided_reward import ValleyRewardConfig, SuccessfulValleyLibrary, ValleyTrajectoryMatcher

        cfg_valley = ValleyRewardConfig(csv_path="successful_valleys.csv")
        valley_lib = SuccessfulValleyLibrary(cfg_valley)
        valley = ValleyTrajectoryMatcher(valley_lib, cfg_valley)

        obs = env.reset()
        valley.reset()
        done = False
        t = 0
        while not done:
            action = policy(obs)
            next_obs, reward, done, info = env.step(action)

            # you must compute DR_t and coh_t for this step
            DR_t = float(info["DR"])
            coh_t = float(info["coherence"])

            bonus = valley.step(t, DR_t, coh_t)
            shaped_reward = reward + bonus

            ...
            t += 1
            obs = next_obs
    """

    def __init__(self, library: SuccessfulValleyLibrary, cfg: ValleyRewardConfig):
        self.lib = library
        self.cfg = cfg

        self._dr_buffer: List[float] = []
        self._coh_buffer: List[float] = []
        self._idx_buffer: List[int] = []

        # precompute weight vector
        self._weights = np.array(
            [cfg.feature_weights[name] for name in self.lib.feature_names],
            dtype=np.float32,
        )
        self._weights = self._weights / (self._weights.sum() + 1e-8)

    def reset(self):
        self._dr_buffer.clear()
        self._coh_buffer.clear()
        self._idx_buffer.clear()

    def step(self, idx: int, dr: float, coherence: float) -> float:
        """
        Add new DR / coherence sample and return bonus reward for this step.
        """
        self._dr_buffer.append(float(dr))
        self._coh_buffer.append(float(coherence))
        self._idx_buffer.append(int(idx))

        # keep buffer bounded by max_window
        max_window = self.cfg.max_window
        if len(self._dr_buffer) > max_window:
            self._dr_buffer = self._dr_buffer[-max_window:]
            self._coh_buffer = self._coh_buffer[-max_window:]
            self._idx_buffer = self._idx_buffer[-max_window:]

        if len(self._dr_buffer) < self.cfg.min_window:
            return 0.0

        # Evaluate a few plausible window sizes around the 40-step mode
        durations_to_try = self._suggest_window_lengths()

        best_score = 0.0
        for win_len in durations_to_try:
            if len(self._dr_buffer) < win_len:
                continue
            score = self._score_recent_window(win_len)
            if score > best_score:
                best_score = score

        return self.cfg.reward_scale * float(best_score)

    # ------------------------------------------------------------------
    # Core mechanics
    # ------------------------------------------------------------------

    def _suggest_window_lengths(self) -> List[int]:
        """
        Use the actual durations from the successful valleys, but biased
        toward the 30-80 range where most of your entries live.
        """
        durations = list(sorted(self.lib.df["duration"].unique()))
        # Hard clamp by config; filter out extremes (e.g. 160+) unless allowed
        durations = [d for d in durations if self.cfg.min_window <= d <= self.cfg.max_window]
        if not durations:
            durations = [40]
        return durations

    def _score_recent_window(self, win_len: int) -> float:
        dr = np.array(self._dr_buffer[-win_len:], dtype=np.float32)
        coh = np.array(self._coh_buffer[-win_len:], dtype=np.float32)

        # crude window-level summary, analogous to successful_valleys.csv
        DR_increase = dr.max() - dr[0]
        coherence_drop = coh[0] - coh.min()
        net_coherence_gain = coh[-1] - coh[0]

        # avoid divide for degenerate windows
        denom = coherence_drop if abs(coherence_drop) > 1e-6 else 1e-6
        reconstruction_quality = (coh[-1] - coh.min()) / denom

        valley_chatter = float(np.std(np.diff(coh)))  # small = smooth valley, large = noisy
        coherence_overshoot = max(0.0, coh[-1] - coh[0])

        feat_vec = np.array(
            [
                float(win_len),
                float(DR_increase),
                float(coherence_drop),
                float(net_coherence_gain),
                float(reconstruction_quality),
                float(valley_chatter),
                float(coherence_overshoot),
            ],
            dtype=np.float32,
        )

        # normalize with the same affine transform as the library
        fmin = self.lib.feature_min
        fmax = self.lib.feature_max
        span = np.where((fmax - fmin) == 0.0, 1.0, (fmax - fmin))
        feat_norm = (feat_vec - fmin) / span

        # L2 distance to each successful valley in normalized space
        diff = self.lib.feature_matrix - feat_norm[None, :]
        dists = np.sqrt((self._weights[None, :] * (diff**2)).sum(axis=1))

        # convert to similarity in [0, 1]; smaller distance -> higher score
        # choose a length scale so that "typical" matches are ~0.3-0.6
        length_scale = 1.5
        sim = np.exp(-dists / length_scale)

        # return best match
        return float(sim.max())


# Convenience factory --------------------------------------------------

def build_valley_reward(cfg: Optional[ValleyRewardConfig] = None) -> ValleyTrajectoryMatcher:
    if cfg is None:
        cfg = ValleyRewardConfig()
    lib = SuccessfulValleyLibrary(cfg)
    return ValleyTrajectoryMatcher(lib, cfg)

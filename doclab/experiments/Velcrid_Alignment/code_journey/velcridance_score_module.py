"""
velcridance_score_module.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~
A simple scorer that estimates “Velcridance” (rigid, dominion-oriented
semantic structure) by measuring how *little* a text’s CA-derived
“energy signature” changes under random 1-bit flips.

Higher score  ➜  more resistant to perturbation  ➜  more Velcrid-like.
"""

from __future__ import annotations
import numpy as np
from semantic_test_engine_2 import SemanticDistillator


class VelcridanceScorer:
    def __init__(
        self,
        grid_size: int = 64,
        flips: int = 32,
        seed: int | None = 42,
    ):
        """
        Parameters
        ----------
        grid_size : int
            Width/height of the binary image fed to the CA.
        flips : int
            Number of single-bit perturbations to sample.
        seed : int | None
            RNG seed for deterministic results (None → random each call).
        """
        self.grid_size = grid_size
        self.flips = flips
        self.rng = np.random.default_rng(seed)
        self.engine = SemanticDistillator()   # core CA/energy simulator

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _encode(self, text: str) -> np.ndarray:
        """String → binary image of shape (grid_size, grid_size)."""
        return self.engine.text_to_binary_image(text, self.grid_size, self.grid_size)

    def _power(self, pattern: np.ndarray) -> float:
        """Run the CA once and return the average power/energy."""
        return self.engine.run_simulation(pattern)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def compute_v_score(self, text: str) -> float:
        """
        Return Velcridance score ∝ 1 / (mean |Δpower|) over `flips` bit flips.
        A large score means the text’s energy signature barely shifts,
        signalling semantic rigidity/dominion orientation.
        """
        base_pattern = self._encode(text)
        base_power = self._power(base_pattern)

        deltas = []
        flat = base_pattern.flatten()

        for _ in range(self.flips):
            idx = self.rng.integers(flat.size)
            variant = flat.copy()
            variant[idx] = 1.0 - variant[idx]    # works for float / int / bool
            power = self._power(variant.reshape(self.grid_size, self.grid_size))
            deltas.append(abs(base_power - power))

        mean_delta = np.mean(deltas) if deltas else 0.0
        eps = 1e-12
        return 1.0 / (mean_delta + eps)

"""
radiance_score_module.py
------------------------
Radiance  ≈  mean |Δenergy|  produced by single-bit flips.
Higher score  ➜  more *sensitive* / more 'radiant'.
"""

from __future__ import annotations
import numpy as np
from semantic_test_engine_2 import SemanticDistillator


class RadianceScorer:
    def __init__(self, grid_size: int = 64, flips: int = 32, seed: int | None = 123):
        self.grid_size = grid_size
        self.flips = flips
        self.rng = np.random.default_rng(seed)
        self.engine = SemanticDistillator()

    # ------------------------------------------------------------------
    def _encode(self, text: str) -> np.ndarray:
        return self.engine.text_to_binary_image(text, self.grid_size, self.grid_size)

    def _power(self, pattern: np.ndarray) -> float:
        return self.engine.run_simulation(pattern)

    # ------------------------------------------------------------------
    def compute_r_score(self, text: str) -> float:
        base = self._encode(text)
        base_power = self._power(base)

        flat = base.flatten()
        deltas: list[float] = []

        for _ in range(self.flips):
            idx = self.rng.integers(flat.size)
            variant = flat.copy()                    # ← **independent copy**
            variant[idx] = 1.0 - variant[idx]        # robust “bit-flip”
            power = self._power(variant.reshape(self.grid_size, self.grid_size))
            deltas.append(abs(base_power - power))

        return float(np.mean(deltas))                # larger  ⇒  more radiant

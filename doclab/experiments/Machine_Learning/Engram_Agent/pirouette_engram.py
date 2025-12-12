#!/usr/bin/env python3
"""
Pirouette Generative Engram Library
====================================

Implements COG-RES-004's Generative Engram as a modular, reusable component.
An engram is not a stored trajectory - it's a *generator* that can be reactivated
through resonance-based lookup.

Core Principle:
--------------
Memory = DDE Attractor (not a recording)
Recall = Resonance Activation (not retrieval)
The form IS the generator.

Architecture:
------------
1. Engram: A trajectory + its generating conditions (Γ, T_p, DR_profile)
2. EngramLibrary: A resonance-addressable collection
3. EngramDistiller: Transfers engram knowledge to policy via coherence-weighted BC
"""

from dataclasses import dataclass, field
from typing import List, Optional, Tuple
import numpy as np
import torch
import torch.nn as nn
from pathlib import Path
import json


# =====================================================================
# §1: Engram Definition (COG-RES-004 §4)
# =====================================================================

@dataclass
class GenerativeEngram:
    """
    A Generative Engram per COG-RES-004.
    
    This is NOT a stored trajectory - it's a *resonance pattern* that can
    regenerate behavior. The trajectory is the *trace* of the DDE attractor.
    
    Components map to COG-RES-006 Triadic Operator:
    - obs, actions: surface manifestation (exhaust)
    - hiddens: Ki core rhythm state (the DDE attractor coordinates)
    - brain_features: (Γ, DR, S, π) - the generating conditions
    - coherence_profile: temporal coherence signature for resonance matching
    """
    # Surface trajectory (the "exhaust" of the engram)
    obs: np.ndarray           # (T, obs_dim)
    actions: np.ndarray       # (T, act_dim)
    brain_features: np.ndarray # (T, brain_dim)
    hiddens: np.ndarray       # (T, hidden_dim) - the Ki rhythm
    
    # Generating conditions (the "seed" that produces the attractor)
    mean_gamma: float         # Average Γ (load) during generation
    mean_DR: float            # Average Dark Residue
    mean_surprise: float      # Average S (prediction error)
    return_raw: float         # Environmental return (fitness)
    
    # Resonance signature (for lookup)
    coherence_profile: np.ndarray = field(default=None) # (T,) temporal coherence
    origin_episode: int = 0
    
    def __post_init__(self):
        """Compute coherence profile if not provided."""
        if self.coherence_profile is None:
            # Compute coherence as stability of hidden state trajectory
            # High coherence = smooth flow in attractor basin
            h_diff = np.diff(self.hiddens, axis=0)
            h_vel = np.linalg.norm(h_diff, axis=-1)
            # Coherence inversely related to velocity (smoother = more coherent)
            self.coherence_profile = np.exp(-h_vel / h_vel.mean())
            # Add back first step
            self.coherence_profile = np.concatenate([[1.0], self.coherence_profile])
    
    @property
    def length(self) -> int:
        """Trajectory length."""
        return len(self.obs)
    
    @property
    def mean_coherence(self) -> float:
        """Average coherence across trajectory."""
        return float(np.mean(self.coherence_profile))
    
    def resonance_score(self, query_gamma: float, query_DR: float, 
                       query_surprise: float) -> float:
        """
        Compute resonance between this engram and a query state.
        
        Per COG-RES-006 §6: match based on (Γ, DR, S) tuple.
        Returns score in [0, 1], with 1 = perfect match.
        """
        # Normalized distance in (Γ, DR, S) space
        gamma_dist = abs(self.mean_gamma - query_gamma) / (self.mean_gamma + 1e-6)
        DR_dist = abs(self.mean_DR - query_DR) / (self.mean_DR + 1e-6)
        S_dist = abs(self.mean_surprise - query_surprise) / (self.mean_surprise + 1e-6)
        
        # Combined distance with emphasis on Γ (most important for matching)
        dist = 0.5 * gamma_dist + 0.3 * DR_dist + 0.2 * S_dist
        
        # Convert to similarity score
        score = np.exp(-dist)
        return float(score)
    
    def to_dict(self) -> dict:
        """Serialize for storage."""
        return {
            "obs": self.obs.tolist(),
            "actions": self.actions.tolist(),
            "brain_features": self.brain_features.tolist(),
            "hiddens": self.hiddens.tolist(),
            "mean_gamma": self.mean_gamma,
            "mean_DR": self.mean_DR,
            "mean_surprise": self.mean_surprise,
            "return_raw": self.return_raw,
            "coherence_profile": self.coherence_profile.tolist(),
            "origin_episode": self.origin_episode
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "GenerativeEngram":
        """Deserialize from storage."""
        return cls(
            obs=np.array(data["obs"]),
            actions=np.array(data["actions"]),
            brain_features=np.array(data["brain_features"]),
            hiddens=np.array(data["hiddens"]),
            mean_gamma=data["mean_gamma"],
            mean_DR=data["mean_DR"],
            mean_surprise=data["mean_surprise"],
            return_raw=data["return_raw"],
            coherence_profile=np.array(data["coherence_profile"]),
            origin_episode=data["origin_episode"]
        )


# =====================================================================
# §2: Engram Library (Resonance-Addressable Collection)
# =====================================================================

class EngramLibrary:
    """
    A resonance-addressable library of generative engrams.
    
    Per COG-RES-004 §6: Query by resonance, not by key.
    The library doesn't "retrieve" - it "activates" patterns.
    """
    
    def __init__(self, capacity: int = 20):
        self.capacity = capacity
        self.engrams: List[GenerativeEngram] = []
        self.next_id = 0
    
    def __len__(self) -> int:
        return len(self.engrams)
    
    def add(self, engram: GenerativeEngram) -> bool:
        """
        Add an engram if it's worthy (high return or unique resonance).
        Returns True if added.
        """
        # Always add if under capacity
        if len(self.engrams) < self.capacity:
            self.engrams.append(engram)
            self.engrams.sort(key=lambda e: e.return_raw, reverse=True)
            return True
        
        # Only add if better than worst engram
        if engram.return_raw > self.engrams[-1].return_raw:
            self.engrams.append(engram)
            self.engrams.sort(key=lambda e: e.return_raw, reverse=True)
            self.engrams = self.engrams[:self.capacity]
            return True
        
        return False
    
    def query(self, gamma: float, DR: float, surprise: float, 
              top_k: int = 5) -> List[Tuple[GenerativeEngram, float]]:
        """
        Query library by resonance.
        
        Returns top-k engrams ranked by resonance score with query conditions.
        Returns list of (engram, score) tuples.
        """
        if not self.engrams:
            return []
        
        # Score all engrams
        scored = [(e, e.resonance_score(gamma, DR, surprise)) 
                  for e in self.engrams]
        
        # Sort by score descending
        scored.sort(key=lambda x: x[1], reverse=True)
        
        return scored[:top_k]
    
    def get_best(self, n: int = 10) -> List[GenerativeEngram]:
        """Get top-n engrams by raw return."""
        return self.engrams[:min(n, len(self.engrams))]
    
    def save(self, path: Path):
        """Save library to disk."""
        data = {
            "capacity": self.capacity,
            "engrams": [e.to_dict() for e in self.engrams],
            "next_id": self.next_id
        }
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
    
    @classmethod
    def load(cls, path: Path) -> "EngramLibrary":
        """Load library from disk."""
        with open(path, 'r') as f:
            data = json.load(f)
        
        lib = cls(capacity=data["capacity"])
        lib.engrams = [GenerativeEngram.from_dict(e) for e in data["engrams"]]
        lib.next_id = data["next_id"]
        return lib
    
    def stats(self) -> dict:
        """Get library statistics."""
        if not self.engrams:
            return {
                "count": 0,
                "mean_return": 0.0,
                "max_return": 0.0,
                "mean_coherence": 0.0,
                "mean_length": 0.0
            }
        
        returns = [e.return_raw for e in self.engrams]
        coherences = [e.mean_coherence for e in self.engrams]
        lengths = [e.length for e in self.engrams]
        
        return {
            "count": len(self.engrams),
            "mean_return": np.mean(returns),
            "max_return": np.max(returns),
            "mean_coherence": np.mean(coherences),
            "mean_length": np.mean(lengths),
            "mean_gamma": np.mean([e.mean_gamma for e in self.engrams]),
            "mean_DR": np.mean([e.mean_DR for e in self.engrams])
        }


# =====================================================================
# §3: Engram Distiller (Coherence-Weighted Behavioral Cloning)
# =====================================================================

class EngramDistiller:
    """
    Transfers engram knowledge to policy via coherence-weighted behavioral cloning.
    
    Key insight from COG-RES-004: We don't clone the entire trajectory uniformly.
    We weight by coherence - learn more from high-coherence (stable attractor) segments.
    
    This implements the "formular induction via DDE" concept: the policy learns
    to reproduce the DDE attractor patterns, not just the surface actions.
    """
    
    def __init__(self, 
                 lr_scale: float = 0.1,
                 grad_clip: float = 0.5,
                 coherence_weight: bool = True):
        """
        Args:
            lr_scale: Temporary LR reduction for stable knowledge transfer
            grad_clip: Gradient clipping for stability
            coherence_weight: If True, weight loss by coherence profile
        """
        self.lr_scale = lr_scale
        self.grad_clip = grad_clip
        self.coherence_weight = coherence_weight
    
    def distill(self,
                policy: nn.Module,
                optimizer: torch.optim.Optimizer,
                engrams: List[GenerativeEngram],
                n_steps: int = 50,
                device: str = "cuda") -> float:
        """
        Distill engram knowledge into policy.
        
        Returns: final loss value
        """
        if not engrams:
            return 0.0
        
        print(f"\n{'='*60}")
        print(f"[ENGRAM DISTILL] Transferring {len(engrams)} engrams to policy...")
        print(f"  Coherence weighting: {self.coherence_weight}")
        print(f"  LR scale: {self.lr_scale}, Steps: {n_steps}")
        
        # Prepare data
        obs_list, act_list, brain_list, h0_list, coherence_list = [], [], [], [], []
        
        for eng in engrams:
            obs_list.append(torch.tensor(eng.obs, dtype=torch.float32))
            act_list.append(torch.tensor(eng.actions, dtype=torch.float32))
            brain_list.append(torch.tensor(eng.brain_features, dtype=torch.float32))
            h0_list.append(torch.tensor(eng.hiddens[0], dtype=torch.float32))
            
            if self.coherence_weight:
                coherence_list.append(torch.tensor(eng.coherence_profile, dtype=torch.float32))
        
        # Pad sequences
        obs_batch = nn.utils.rnn.pad_sequence(obs_list, batch_first=True).to(device)
        act_batch = nn.utils.rnn.pad_sequence(act_list, batch_first=True).to(device)
        brain_batch = nn.utils.rnn.pad_sequence(brain_list, batch_first=True).to(device)
        h0_batch = torch.stack(h0_list).to(device)
        
        if self.coherence_weight:
            coherence_batch = nn.utils.rnn.pad_sequence(coherence_list, batch_first=True).to(device)
        
        B, T, _ = obs_batch.shape
        
        # Reduce LR temporarily
        orig_lrs = [g["lr"] for g in optimizer.param_groups]
        for g in optimizer.param_groups:
            g["lr"] *= self.lr_scale
        
        # Distillation loop
        losses = []
        for step in range(n_steps):
            # Unroll RNN
            h_step = h0_batch
            total_loss = 0.0
            
            for t in range(T):
                obs_t = obs_batch[:, t, :]
                brain_t = brain_batch[:, t, :]
                act_t = act_batch[:, t, :]
                
                # Get policy prediction
                mu, _, h_next = policy.forward(obs_t, brain_t, h_step)
                pred = torch.tanh(mu)
                
                # Compute loss
                sq_error = ((pred - act_t) ** 2).mean(dim=-1)  # (B,)
                
                # Weight by coherence if enabled
                if self.coherence_weight:
                    coh_t = coherence_batch[:, t]
                    sq_error = sq_error * coh_t
                
                # Mask padding
                act_mag = torch.abs(act_t).sum(dim=-1)
                mask = (act_mag > 1e-5).float()
                
                loss_t = (sq_error * mask).sum() / mask.sum().clamp(min=1.0)
                total_loss += loss_t
                
                h_step = h_next
            
            loss = total_loss / T
            
            # Update
            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(policy.parameters(), self.grad_clip)
            optimizer.step()
            
            losses.append(loss.item())
            
            if step % 10 == 0 or step == n_steps - 1:
                print(f"  Step {step:3d}/{n_steps}: loss={loss.item():.4f}")
        
        # Restore LR
        for g, lr in zip(optimizer.param_groups, orig_lrs):
            g["lr"] = lr
        
        final_loss = losses[-1]
        print(f"[ENGRAM DISTILL] Complete. Final loss: {final_loss:.4f}")
        print(f"{'='*60}\n")
        
        return final_loss


# =====================================================================
# §4: Engram Factory (Creates engrams from trajectories)
# =====================================================================

class EngramFactory:
    """
    Factory for creating GenerativeEngrams from raw trajectory data.
    
    Extracts the generating conditions (Γ, DR, S) and coherence signature.
    """
    
    @staticmethod
    def from_trajectory(
        obs: np.ndarray,
        actions: np.ndarray,
        brain_features: np.ndarray,
        hiddens: np.ndarray,
        return_raw: float,
        episode: int = 0
    ) -> GenerativeEngram:
        """
        Create an engram from a trajectory.
        
        Args:
            obs: (T, obs_dim)
            actions: (T, act_dim)
            brain_features: (T, brain_dim) - must include [DR, S, Gamma, ...]
            hiddens: (T, hidden_dim)
            return_raw: environmental return
            episode: origin episode number
        """
        # Extract generating conditions from brain features
        # Assuming: brain_features = [DR, S, Gamma, pi, g, O_P, O_S, O_C, norm, B]
        DR_trace = brain_features[:, 0]
        S_trace = brain_features[:, 1]
        Gamma_trace = brain_features[:, 2]
        
        return GenerativeEngram(
            obs=obs,
            actions=actions,
            brain_features=brain_features,
            hiddens=hiddens,
            mean_gamma=float(np.mean(Gamma_trace)),
            mean_DR=float(np.mean(DR_trace)),
            mean_surprise=float(np.mean(S_trace)),
            return_raw=return_raw,
            origin_episode=episode
        )


# =====================================================================
# §5: Usage Example
# =====================================================================

if __name__ == "__main__":
    """
    Example: Creating and querying engrams.
    """
    # Create library
    lib = EngramLibrary(capacity=10)
    
    # Create some dummy engrams
    for i in range(5):
        T = np.random.randint(100, 500)
        engram = GenerativeEngram(
            obs=np.random.randn(T, 10),
            actions=np.random.randn(T, 5),
            brain_features=np.random.randn(T, 10),
            hiddens=np.random.randn(T, 256),
            mean_gamma=1.0 + 0.3 * i,
            mean_DR=0.8 + 0.05 * i,
            mean_surprise=0.5 + 0.1 * i,
            return_raw=100.0 + 50.0 * i,
            origin_episode=i
        )
        lib.add(engram)
    
    # Query by resonance
    print("\n=== Query by Resonance ===")
    query_results = lib.query(gamma=1.5, DR=0.85, surprise=0.6, top_k=3)
    for eng, score in query_results:
        print(f"  Engram ep={eng.origin_episode}, return={eng.return_raw:.1f}, "
              f"resonance={score:.3f}")
    
    # Get library stats
    print("\n=== Library Stats ===")
    stats = lib.stats()
    for k, v in stats.items():
        print(f"  {k}: {v:.2f}")
    
    print("\n✓ Engram library operational!")

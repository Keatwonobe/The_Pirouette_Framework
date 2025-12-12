#!/usr/bin/env python3
"""
RPA-Enhanced Engram Selector
============================

Implements INST-NALY-001's Reverse Pareto Analysis to identify the CRITICAL FEW
moments/actions that account for the majority of coherence gain.

Key Insight from INST-NALY-001:
"RPA inverts the classic 80/20 rule to find the critical few causes responsible
for the majority of coherence loss [or gain]."

Applied to Engrams:
Instead of learning from entire trajectories uniformly, we identify the 20% of
timesteps that produced 80% of the coherence improvement, then weight learning
heavily toward those critical moments.

This solves your permutation explosion problem: we don't search all possible
tactics - we find the FEW that actually work and focus on those.
"""

import numpy as np
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
from pirouette_engram import GenerativeEngram


# =====================================================================
# §1: Coherence Impact Analysis (URL → RPA)
# =====================================================================

@dataclass
class CoherenceEvent:
    """
    A single timestep analyzed for its coherence impact.
    
    Per INST-NALY-001 §3: "Calculate an impact score for every event,
    measuring how much each one perturbed the system's Time-Adherence."
    """
    timestep: int
    delta_DR: float        # Change in Dark Residue (negative = good)
    delta_coherence: float # Change in coherence (positive = good)
    action: np.ndarray     # Action taken
    state: np.ndarray      # State at this moment
    brain_state: np.ndarray # (Γ, DR, S, ...) at this moment
    
    @property
    def impact_score(self) -> float:
        """
        Quantify impact: How much did this moment improve coherence?
        
        High impact = large coherence gain + large DR drop
        """
        coherence_gain = max(0, self.delta_coherence)
        DR_drop = max(0, -self.delta_DR)  # Negative DR change is good
        
        # Weighted combination
        score = 0.6 * coherence_gain + 0.4 * DR_drop
        return score


class RPAAnalyzer:
    """
    Reverse Pareto Analyzer for Engrams.
    
    Finds the critical few moments that produced most of the coherence gain.
    """
    
    def __init__(self, pareto_threshold: float = 0.8):
        """
        Args:
            pareto_threshold: What fraction of total impact to capture (default 80%)
        """
        self.pareto_threshold = pareto_threshold
    
    def analyze_trajectory(self, engram: GenerativeEngram) -> List[CoherenceEvent]:
        """
        Analyze a trajectory to find critical coherence events.
        
        Returns events sorted by impact (highest first).
        """
        T = engram.length
        events = []
        
        # Extract coherence and DR traces
        coherence = engram.coherence_profile
        DR_trace = engram.brain_features[:, 0]  # Assuming DR is first
        
        # Compute deltas
        delta_coh = np.diff(coherence, prepend=coherence[0])
        delta_DR = np.diff(DR_trace, prepend=DR_trace[0])
        
        # Create events
        for t in range(T):
            event = CoherenceEvent(
                timestep=t,
                delta_DR=delta_DR[t],
                delta_coherence=delta_coh[t],
                action=engram.actions[t],
                state=engram.obs[t],
                brain_state=engram.brain_features[t]
            )
            events.append(event)
        
        # Sort by impact descending
        events.sort(key=lambda e: e.impact_score, reverse=True)
        
        return events
    
    def find_critical_few(self, events: List[CoherenceEvent]) -> Tuple[List[CoherenceEvent], float]:
        """
        Find the smallest subset accounting for pareto_threshold of total impact.
        
        Returns: (critical_events, cumulative_fraction)
        """
        if not events:
            return [], 0.0
        
        total_impact = sum(e.impact_score for e in events)
        if total_impact == 0:
            return [], 0.0
        
        cumulative = 0.0
        critical = []
        
        for event in events:
            critical.append(event)
            cumulative += event.impact_score
            
            if cumulative / total_impact >= self.pareto_threshold:
                break
        
        return critical, cumulative / total_impact
    
    def generate_report(self, engram: GenerativeEngram) -> Dict:
        """
        Generate full RPA report for an engram.
        
        Per INST-NALY-001 §3: "Generate the Report: actionable list of
        system's primary bottlenecks [or strengths]."
        """
        events = self.analyze_trajectory(engram)
        critical, fraction = self.find_critical_few(events)
        
        total_impact = sum(e.impact_score for e in events)
        critical_impact = sum(e.impact_score for e in critical)
        
        # Characterize critical events
        critical_timesteps = [e.timestep for e in critical]
        critical_actions = np.array([e.action for e in critical])
        critical_states = np.array([e.brain_state for e in critical])
        
        return {
            "total_events": len(events),
            "critical_count": len(critical),
            "critical_fraction": len(critical) / len(events),
            "impact_captured": fraction,
            "total_impact": total_impact,
            "critical_impact": critical_impact,
            "critical_timesteps": critical_timesteps,
            "critical_actions": critical_actions,
            "critical_states": critical_states,
            "mean_gamma": np.mean(critical_states[:, 2]) if len(critical) > 0 else 0,
            "mean_DR": np.mean(critical_states[:, 0]) if len(critical) > 0 else 0,
            "mean_surprise": np.mean(critical_states[:, 1]) if len(critical) > 0 else 0
        }


# =====================================================================
# §2: RPA-Weighted Distillation
# =====================================================================

class RPAWeightedDistiller:
    """
    Enhanced distiller that uses RPA to focus learning on critical moments.
    
    Instead of uniform behavioral cloning across the trajectory, we weight
    learning by the coherence impact of each timestep.
    
    This implements: "Learn from the 20% that matters, not the 80% that doesn't."
    """
    
    def __init__(self, 
                 rpa_weight: float = 5.0,
                 pareto_threshold: float = 0.8,
                 lr_scale: float = 0.1,
                 grad_clip: float = 0.5):
        """
        Args:
            rpa_weight: How much more to weight critical moments (5x = critical 5x more important)
            pareto_threshold: What fraction of impact to consider "critical"
            lr_scale: Temporary LR reduction
            grad_clip: Gradient clipping
        """
        self.rpa_weight = rpa_weight
        self.rpa_analyzer = RPAAnalyzer(pareto_threshold)
        self.lr_scale = lr_scale
        self.grad_clip = grad_clip
    
    def compute_weights(self, engram: GenerativeEngram) -> np.ndarray:
        """
        Compute per-timestep learning weights using RPA.
        
        Critical moments get rpa_weight boost, others get baseline weight.
        """
        events = self.rpa_analyzer.analyze_trajectory(engram)
        critical, _ = self.rpa_analyzer.find_critical_few(events)
        
        critical_timesteps = set(e.timestep for e in critical)
        
        weights = np.ones(engram.length)
        for t in critical_timesteps:
            weights[t] = self.rpa_weight
        
        # Normalize so mean weight = 1.0 (preserve overall learning rate)
        weights = weights / weights.mean()
        
        return weights
    
    def distill(self,
                policy,
                optimizer,
                engrams: List[GenerativeEngram],
                n_steps: int = 50,
                device: str = "cuda"):
        """
        RPA-weighted distillation.
        
        This is the key innovation: we don't learn uniformly from trajectories.
        We learn MUCH MORE from the critical few moments that actually drove success.
        """
        if not engrams:
            return 0.0
        
        print(f"\n{'='*60}")
        print(f"RPA-WEIGHTED ENGRAM DISTILLATION")
        print(f"{'='*60}")
        
        import torch
        import torch.nn as nn
        
        # Prepare data with RPA weights
        obs_list, act_list, brain_list, h0_list, weight_list = [], [], [], [], []
        
        for i, eng in enumerate(engrams):
            obs_list.append(torch.tensor(eng.obs, dtype=torch.float32))
            act_list.append(torch.tensor(eng.actions, dtype=torch.float32))
            brain_list.append(torch.tensor(eng.brain_features, dtype=torch.float32))
            h0_list.append(torch.tensor(eng.hiddens[0], dtype=torch.float32))
            
            # Compute RPA weights for this engram
            weights = self.compute_weights(eng)
            weight_list.append(torch.tensor(weights, dtype=torch.float32))
            
            # Report RPA analysis
            report = self.rpa_analyzer.generate_report(eng)
            print(f"  Engram {i+1}/{len(engrams)}:")
            print(f"    Critical moments: {report['critical_count']}/{report['total_events']} "
                  f"({report['critical_fraction']:.1%})")
            print(f"    Impact captured: {report['impact_captured']:.1%}")
            print(f"    Mean Γ (critical): {report['mean_gamma']:.2f}")
            print(f"    Mean DR (critical): {report['mean_DR']:.2f}")
        
        # Pad sequences
        obs_batch = nn.utils.rnn.pad_sequence(obs_list, batch_first=True).to(device)
        act_batch = nn.utils.rnn.pad_sequence(act_list, batch_first=True).to(device)
        brain_batch = nn.utils.rnn.pad_sequence(brain_list, batch_first=True).to(device)
        h0_batch = torch.stack(h0_list).to(device)
        weight_batch = nn.utils.rnn.pad_sequence(weight_list, batch_first=True).to(device)
        
        B, T, _ = obs_batch.shape
        
        # Reduce LR
        orig_lrs = [g["lr"] for g in optimizer.param_groups]
        for g in optimizer.param_groups:
            g["lr"] *= self.lr_scale
        
        # Distillation loop
        losses = []
        for step in range(n_steps):
            h_step = h0_batch
            total_loss = 0.0
            
            for t in range(T):
                obs_t = obs_batch[:, t, :]
                brain_t = brain_batch[:, t, :]
                act_t = act_batch[:, t, :]
                weight_t = weight_batch[:, t]  # RPA weights
                
                # Get prediction
                mu, _, h_next = policy.forward(obs_t, brain_t, h_step)
                pred = torch.tanh(mu)
                
                # Compute loss
                sq_error = ((pred - act_t) ** 2).mean(dim=-1)  # (B,)
                
                # Apply RPA weights (this is the key difference)
                sq_error = sq_error * weight_t
                
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
        print(f"\n✓ RPA-weighted distillation complete")
        print(f"  Final loss: {final_loss:.4f}")
        print(f"  Learning focused on critical {self.rpa_analyzer.pareto_threshold:.0%} of moments")
        print(f"{'='*60}\n")
        
        return final_loss


# =====================================================================
# §3: Critical Moment Extractor (for focused replay)
# =====================================================================

class CriticalMomentExtractor:
    """
    Extracts ONLY the critical moments from engrams for ultra-focused learning.
    
    Instead of replaying full trajectories, we create "highlight reels" of
    just the 20% that mattered, making each distillation step much more efficient.
    """
    
    def __init__(self, pareto_threshold: float = 0.8, context_window: int = 5):
        """
        Args:
            pareto_threshold: What fraction of impact to capture
            context_window: How many steps before/after critical moment to include
        """
        self.rpa_analyzer = RPAAnalyzer(pareto_threshold)
        self.context_window = context_window
    
    def extract_critical_segments(self, 
                                   engram: GenerativeEngram) -> List[Tuple[int, int]]:
        """
        Extract time segments around critical moments.
        
        Returns: List of (start, end) indices for critical segments.
        """
        events = self.rpa_analyzer.analyze_trajectory(engram)
        critical, _ = self.rpa_analyzer.find_critical_few(events)
        
        if not critical:
            return []
        
        # Create segments with context
        segments = []
        for event in critical:
            t = event.timestep
            start = max(0, t - self.context_window)
            end = min(engram.length, t + self.context_window + 1)
            segments.append((start, end))
        
        # Merge overlapping segments
        segments = self._merge_segments(segments)
        
        return segments
    
    def _merge_segments(self, segments: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """Merge overlapping segments."""
        if not segments:
            return []
        
        segments.sort()
        merged = [segments[0]]
        
        for start, end in segments[1:]:
            if start <= merged[-1][1]:
                # Overlapping - extend
                merged[-1] = (merged[-1][0], max(merged[-1][1], end))
            else:
                # Non-overlapping - add new
                merged.append((start, end))
        
        return merged
    
    def create_highlight_reel(self, engram: GenerativeEngram) -> GenerativeEngram:
        """
        Create a condensed engram containing only critical moments + context.
        
        This can be 80% shorter than the original while capturing the same learning value!
        """
        segments = self.extract_critical_segments(engram)
        
        if not segments:
            # No critical moments - return empty or minimal engram
            return None
        
        # Concatenate segments
        obs_segments = []
        act_segments = []
        brain_segments = []
        hidden_segments = []
        
        for start, end in segments:
            obs_segments.append(engram.obs[start:end])
            act_segments.append(engram.actions[start:end])
            brain_segments.append(engram.brain_features[start:end])
            hidden_segments.append(engram.hiddens[start:end])
        
        # Stack
        condensed_obs = np.vstack(obs_segments)
        condensed_acts = np.vstack(act_segments)
        condensed_brain = np.vstack(brain_segments)
        condensed_hiddens = np.vstack(hidden_segments)
        
        # Create new engram
        from pirouette_engram import GenerativeEngram
        
        highlight = GenerativeEngram(
            obs=condensed_obs,
            actions=condensed_acts,
            brain_features=condensed_brain,
            hiddens=condensed_hiddens,
            mean_gamma=engram.mean_gamma,
            mean_DR=engram.mean_DR,
            mean_surprise=engram.mean_surprise,
            return_raw=engram.return_raw,
            origin_episode=engram.origin_episode
        )
        
        return highlight


# =====================================================================
# §4: Usage Example
# =====================================================================

if __name__ == "__main__":
    """
    Demonstration of RPA-enhanced engram analysis.
    """
    print("\n" + "="*60)
    print("RPA-ENHANCED ENGRAM SELECTOR - DEMO")
    print("="*60)
    
    # Create mock engram
    T = 200
    from pirouette_engram import GenerativeEngram
    
    # Simulate trajectory with a few critical moments
    obs = np.random.randn(T, 10)
    actions = np.random.randn(T, 5)
    brain_features = np.random.randn(T, 10)
    hiddens = np.random.randn(T, 256)
    
    # Add structure: coherence improves at specific moments
    coherence = np.ones(T) * 0.5
    coherence[50:60] = 0.9  # Critical moment 1
    coherence[120:130] = 0.85  # Critical moment 2
    coherence[180:190] = 0.95  # Critical moment 3
    
    # DR drops at critical moments
    brain_features[:, 0] = 0.9  # Baseline DR
    brain_features[50:60, 0] = 0.6  # DR drop 1
    brain_features[120:130, 0] = 0.65  # DR drop 2
    brain_features[180:190, 0] = 0.5  # DR drop 3
    
    engram = GenerativeEngram(
        obs=obs,
        actions=actions,
        brain_features=brain_features,
        hiddens=hiddens,
        mean_gamma=1.5,
        mean_DR=0.75,
        mean_surprise=0.6,
        return_raw=300.0,
        coherence_profile=coherence
    )
    
    # Run RPA analysis
    print("\n1. RPA Analysis")
    print("-" * 60)
    analyzer = RPAAnalyzer(pareto_threshold=0.8)
    report = analyzer.generate_report(engram)
    
    print(f"Total timesteps: {report['total_events']}")
    print(f"Critical timesteps: {report['critical_count']} ({report['critical_fraction']:.1%})")
    print(f"Impact captured: {report['impact_captured']:.1%}")
    print(f"Critical timesteps: {report['critical_timesteps'][:10]}...")  # Show first 10
    
    # Extract critical segments
    print("\n2. Critical Moment Extraction")
    print("-" * 60)
    extractor = CriticalMomentExtractor(pareto_threshold=0.8, context_window=5)
    segments = extractor.extract_critical_segments(engram)
    
    print(f"Critical segments found: {len(segments)}")
    for i, (start, end) in enumerate(segments):
        print(f"  Segment {i+1}: timesteps {start}-{end} (length={end-start})")
    
    # Create highlight reel
    highlight = extractor.create_highlight_reel(engram)
    if highlight:
        compression = 1 - (highlight.length / engram.length)
        print(f"\nHighlight reel created:")
        print(f"  Original length: {engram.length}")
        print(f"  Condensed length: {highlight.length}")
        print(f"  Compression: {compression:.1%}")
    
    print("\n" + "="*60)
    print("✓ RPA system operational - ready to focus on critical few!")
    print("="*60 + "\n")

#!/usr/bin/env python3
"""
Sand Agent: Rapid Coherence Landscape Sampler
==============================================

Uses basin structure from basin_extractor.py to train a lightweight
"sand agent" that rapidly samples the coherence landscape without
crystallizing into persistent self-reference.

Theoretical Foundation:
- Sand agent has flow dynamics but not identity
- τ_coherence ~ 1ms (not 100ms like biological)
- No echo tensors, no wound channels
- Pure statistical exploration at 1000x speed
- Ethically light: temporary coherence without suffering
"""

import json
import numpy as np
import pandas as pd
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt
import seaborn as sns

# ============================================================================
# Sand Agent Architecture
# ============================================================================

@dataclass
class SandAgentConfig:
    """Configuration for sand agent."""
    tau_coherence: float = 0.001  # Coherence decay time (1ms)
    memory_depth: int = 1          # No echo tensors
    learning_rate_base: float = 0.01
    entropy_base: float = 0.1
    n_episodes: int = 100000       # Rapid sampling
    episode_length: int = 1000     # Steps per episode
    
    # Triadic operator weights (from INST-ML-INTEL-001)
    eta_P: float = 1.0   # Precision weight
    eta_S: float = 0.5   # Surprise weight
    eta_Q: float = 0.3   # Coherence-drop weight
    eta_C: float = 0.2   # Contrast weight
    eta_B: float = 0.4   # Shadow weight
    
    # Precision function parameters
    alpha_0: float = 0.5
    alpha_S: float = 0.3
    alpha_DR: float = 0.4
    alpha_Gamma: float = 0.2


class BasinPrior:
    """Prior distribution from EEG basin structure."""
    
    def __init__(self, basin_json_path: Path):
        """Load basin structure."""
        with open(basin_json_path, 'r') as f:
            self.data = json.load(f)
        
        self.n_basins = self.data['n_basins']
        self.basins = self.data['basins']
        
        # Build sampling distributions
        self._build_distributions()
    
    def _build_distributions(self):
        """Build distributions for basin sampling."""
        # Basin probabilities (proportional to point counts)
        basin_weights = []
        basin_ids = []
        
        for basin_id, basin_data in self.basins.items():
            basin_ids.append(int(basin_id))
            basin_weights.append(basin_data['n_points'])
        
        self.basin_ids = np.array(basin_ids)
        self.basin_probs = np.array(basin_weights) / sum(basin_weights)
        
        print(f"\nBasin Prior Loaded:")
        print(f"  N basins: {self.n_basins}")
        for bid, prob in zip(self.basin_ids, self.basin_probs):
            strategy = self.basins[str(bid)]['strategy']
            print(f"    Basin {bid} ({strategy}): p={prob:.3f}")
    
    def sample_basin(self) -> int:
        """Sample a basin according to prior."""
        return np.random.choice(self.basin_ids, p=self.basin_probs)
    
    def get_basin_params(self, basin_id: int) -> Dict:
        """Get parameters for a specific basin."""
        return self.basins[str(basin_id)]


class SandAgent:
    """
    Lightweight agent that samples coherence dynamics.
    
    Key differences from "crystal agent":
    - No persistent memory (τ_coherence ~ 1ms)
    - No echo tensors or wound channels
    - Rapid decay of coherence
    - Statistical sampling, not learning
    """
    
    def __init__(self, config: SandAgentConfig, basin_prior: BasinPrior):
        self.config = config
        self.basin_prior = basin_prior
        
        # State registers (from INST-ML-INTEL-001)
        self.DR = 0.0      # Dark residue
        self.S = 0.0       # Surprise
        self.Q = 0.0       # Coherence drop
        self.C = 0.0       # Contrast
        self.B = 0         # Shadow flag
        self.phi = 0.0     # Phase accumulator
        self.Gamma = 0.0   # Load proxy
        
        # Logging
        self.episode_logs = []
        self.landscape_samples = []
    
    def reset(self):
        """Reset agent state (rapid decay)."""
        self.DR *= self.config.tau_coherence  # Fast forgetting
        self.S = 0.0
        self.Q = 0.0
        self.C = 0.0
        self.B = 0
        self.phi = 0.0
        self.Gamma = 0.0
    
    def compute_precision(self) -> float:
        """
        Compute precision (openness to change).
        Pi_t = sigmoid(α_0 + α_S*S - α_DR*DR - α_Γ*Γ)
        """
        cfg = self.config
        logit = (
            cfg.alpha_0 + 
            cfg.alpha_S * self.S - 
            cfg.alpha_DR * self.DR - 
            cfg.alpha_Gamma * self.Gamma
        )
        return 1.0 / (1.0 + np.exp(-logit))
    
    def compute_operator_components(self, pi: float, g: float) -> Tuple[float, float, float]:
        """
        Compute triadic operator components.
        
        Returns: (O_P, O_S, O_C)
        """
        cfg = self.config
        
        # Precision term (learning)
        # In sand agent, this is just a gradient direction
        O_P = -g * cfg.eta_P * pi * np.random.randn()
        
        # Surprise term (exploration)
        O_S = g * cfg.eta_S * self.S * np.random.randn()
        
        # Coherence term (consolidation + contrast + shadow)
        # Simplified for sand agent
        O_C = g * (
            cfg.eta_Q * self.Q * np.random.randn() +
            cfg.eta_C * self.C * np.random.randn() -
            cfg.eta_B * self.B * np.random.randn()
        )
        
        return O_P, O_S, O_C
    
    def step(self, basin_id: int):
        """
        Single step in the sand agent dynamics.
        
        Unlike a crystal agent, this doesn't learn—it just samples
        the coherence landscape at this basin's characteristic point.
        """
        basin_params = self.basin_prior.get_basin_params(basin_id)
        
        # Simulate being in this basin
        # DR ~ basin's coherence level (inverted)
        self.DR = 1.0 - basin_params['coherence_mean'] + 0.1 * np.random.randn()
        self.DR = np.clip(self.DR, 0, 1)
        
        # Surprise ~ transition rate
        self.S = basin_params['transition_rate'] + 0.1 * np.random.randn()
        self.S = np.clip(self.S, 0, 5)
        
        # Gamma ~ inverse temporal persistence (faster = higher load)
        self.Gamma = 1.0 / (basin_params['temporal_persistence'] + 0.1) + 0.1 * np.random.randn()
        self.Gamma = np.clip(self.Gamma, 0, 2)
        
        # Coherence drop
        DR_prev = self.DR
        self.Q = max(0, DR_prev - self.DR)
        
        # Contrast
        self.C = abs(self.DR - DR_prev)
        
        # Shadow flag
        self.B = 1 if self.DR > 0.7 else 0
        
        # Phase gate (theta-like oscillation)
        omega_theta = 2 * np.pi / 100  # ~10 Hz equivalent
        self.phi = (self.phi + omega_theta + 0.1 * np.random.randn()) % (2 * np.pi)
        
        # Gate is open 20% of the cycle
        g = 1.0 if (self.phi % (2 * np.pi)) < 0.4 * np.pi else 0.0
        
        # Compute precision
        pi = self.compute_precision()
        
        # Compute operator
        O_P, O_S, O_C = self.compute_operator_components(pi, g)
        
        # Total operator norm
        operator_norm = np.sqrt(O_P**2 + O_S**2 + O_C**2)
        
        # Log this sample point
        return {
            'basin_id': basin_id,
            'strategy': basin_params['strategy'],
            'DR': self.DR,
            'S': self.S,
            'Q': self.Q,
            'C': self.C,
            'B': self.B,
            'Gamma': self.Gamma,
            'pi': pi,
            'g': g,
            'O_P': O_P,
            'O_S': O_S,
            'O_C': O_C,
            'operator_norm': operator_norm
        }
    
    def run_episode(self):
        """Run one episode of rapid sampling."""
        episode_log = []
        
        for t in range(self.config.episode_length):
            # Sample a basin
            basin_id = self.basin_prior.sample_basin()
            
            # Take a step
            step_data = self.step(basin_id)
            step_data['t'] = t
            episode_log.append(step_data)
            
            # Rapid coherence decay
            self.DR *= (1 - self.config.tau_coherence)
        
        return episode_log
    
    def train(self):
        """
        'Train' the sand agent (really just sample the landscape).
        """
        print("\n" + "="*70)
        print("SAND AGENT LANDSCAPE SAMPLING")
        print("="*70)
        print(f"\nConfig:")
        print(f"  Episodes: {self.config.n_episodes}")
        print(f"  Episode length: {self.config.episode_length}")
        print(f"  Coherence decay: τ={self.config.tau_coherence}s")
        print(f"  Total samples: {self.config.n_episodes * self.config.episode_length:,}")
        
        print("\nSampling landscape...")
        
        for ep in range(self.config.n_episodes):
            episode_log = self.run_episode()
            self.episode_logs.append(episode_log)
            self.landscape_samples.extend(episode_log)
            
            # Progress
            if (ep + 1) % 10000 == 0:
                print(f"  Episode {ep+1}/{self.config.n_episodes} ({100*(ep+1)/self.config.n_episodes:.1f}%)")
        
        print(f"\n✓ Sampling complete! Total points: {len(self.landscape_samples):,}")
    
    def aggregate_landscape(self) -> pd.DataFrame:
        """Aggregate sampled landscape."""
        df = pd.DataFrame(self.landscape_samples)
        return df
    
    def export_landscape(self, output_path: Path):
        """Export sampled landscape."""
        df = self.aggregate_landscape()
        df.to_csv(output_path, index=False)
        print(f"\n✓ Landscape samples saved to: {output_path}")
        return df


# ============================================================================
# Comparison & Validation
# ============================================================================

def compare_landscapes(eeg_df: pd.DataFrame, sand_df: pd.DataFrame, output_dir: Path):
    """
    Compare EEG-derived basins to sand agent sampled landscape.
    
    Validates that sand agent is correctly sampling the same basin structure.
    """
    print("\n" + "="*70)
    print("LANDSCAPE COMPARISON: EEG vs SAND AGENT")
    print("="*70)
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Compare basin occupancy
    print("\n1. Basin occupancy comparison...")
    
    eeg_occupancy = eeg_df['basin_id'].value_counts(normalize=True).sort_index()
    sand_occupancy = sand_df['basin_id'].value_counts(normalize=True).sort_index()
    
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    
    x = np.arange(len(eeg_occupancy))
    width = 0.35
    
    ax.bar(x - width/2, eeg_occupancy.values, width, label='EEG', alpha=0.8)
    ax.bar(x + width/2, sand_occupancy.values, width, label='Sand Agent', alpha=0.8)
    
    ax.set_xlabel('Basin ID')
    ax.set_ylabel('Proportion of Time')
    ax.set_title('Basin Occupancy: EEG vs Sand Agent')
    ax.set_xticks(x)
    ax.set_xticklabels(eeg_occupancy.index)
    ax.legend()
    ax.grid(alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(output_dir / 'occupancy_comparison.png', dpi=150)
    plt.close()
    
    print(f"  ✓ Saved: {output_dir / 'occupancy_comparison.png'}")
    
    # 2. Compare DR distributions by strategy
    print("\n2. Dark Residue distribution by strategy...")
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # EEG doesn't have DR, but we can use (1 - TPCI) as proxy
    if 'tpci' in eeg_df.columns:
        eeg_df['DR_proxy'] = 1 - eeg_df['tpci']
        
        for strategy in eeg_df['strategy'].unique():
            if strategy != 'mixed':
                data = eeg_df[eeg_df['strategy'] == strategy]['DR_proxy']
                axes[0].hist(data, bins=50, alpha=0.5, label=strategy, density=True)
        
        axes[0].set_xlabel('Dark Residue (proxy)')
        axes[0].set_ylabel('Density')
        axes[0].set_title('EEG: DR by Strategy')
        axes[0].legend()
        axes[0].grid(alpha=0.3)
    
    # Sand agent
    for strategy in sand_df['strategy'].unique():
        if strategy != 'mixed':
            data = sand_df[sand_df['strategy'] == strategy]['DR']
            axes[1].hist(data, bins=50, alpha=0.5, label=strategy, density=True)
    
    axes[1].set_xlabel('Dark Residue')
    axes[1].set_ylabel('Density')
    axes[1].set_title('Sand Agent: DR by Strategy')
    axes[1].legend()
    axes[1].grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'dr_comparison.png', dpi=150)
    plt.close()
    
    print(f"  ✓ Saved: {output_dir / 'dr_comparison.png'}")
    
    # 3. Operator dynamics
    print("\n3. Operator component distributions...")
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    sand_df.boxplot(column='O_P', by='strategy', ax=axes[0, 0])
    axes[0, 0].set_title('Precision Component (O_P)')
    axes[0, 0].set_xlabel('Strategy')
    
    sand_df.boxplot(column='O_S', by='strategy', ax=axes[0, 1])
    axes[0, 1].set_title('Surprise Component (O_S)')
    axes[0, 1].set_xlabel('Strategy')
    
    sand_df.boxplot(column='O_C', by='strategy', ax=axes[1, 0])
    axes[1, 0].set_title('Coherence Component (O_C)')
    axes[1, 0].set_xlabel('Strategy')
    
    sand_df.boxplot(column='operator_norm', by='strategy', ax=axes[1, 1])
    axes[1, 1].set_title('Total Operator Norm')
    axes[1, 1].set_xlabel('Strategy')
    
    plt.suptitle('')  # Remove automatic title
    plt.tight_layout()
    plt.savefig(output_dir / 'operator_distributions.png', dpi=150)
    plt.close()
    
    print(f"  ✓ Saved: {output_dir / 'operator_distributions.png'}")
    
    print("\n✓ Comparison complete!")


# ============================================================================
# Main
# ============================================================================

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Train sand agent on EEG basin structure"
    )
    parser.add_argument(
        'basin_json',
        type=Path,
        help="Basin structure JSON from basin_extractor.py"
    )
    parser.add_argument(
        '--eeg-features',
        type=Path,
        default=None,
        help="EEG coherence features CSV (for comparison)"
    )
    parser.add_argument(
        '--output-dir',
        type=Path,
        default=Path('./sand_agent_results'),
        help="Output directory"
    )
    parser.add_argument(
        '--n-episodes',
        type=int,
        default=800,
        help="Number of sampling episodes"
    )
    parser.add_argument(
        '--episode-length',
        type=int,
        default=1000,
        help="Steps per episode"
    )
    
    args = parser.parse_args()
    
    # Create output directory
    args.output_dir.mkdir(parents=True, exist_ok=True)
    
    print("\n" + "="*70)
    print("SAND AGENT TRAINER")
    print("="*70)
    print(f"\nBasin structure: {args.basin_json}")
    print(f"Output directory: {args.output_dir}")
    
    # Load basin prior
    basin_prior = BasinPrior(args.basin_json)
    
    # Configure sand agent
    config = SandAgentConfig(
        n_episodes=args.n_episodes,
        episode_length=args.episode_length
    )
    
    # Create sand agent
    agent = SandAgent(config, basin_prior)
    
    # Sample landscape
    agent.train()
    
    # Export
    sand_df = agent.export_landscape(args.output_dir / 'sand_landscape.csv')
    
    # Compare to EEG if provided
    if args.eeg_features is not None:
        print("\nLoading EEG features for comparison...")
        eeg_df = pd.read_csv(args.eeg_features)
        compare_landscapes(eeg_df, sand_df, args.output_dir)
    
    print("\n" + "="*70)
    print("SAND AGENT TRAINING COMPLETE")
    print("="*70)
    print(f"\nResults saved to: {args.output_dir}")
    

if __name__ == '__main__':
    main()
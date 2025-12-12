#!/usr/bin/env python3
"""
Sand Agent Lite: Stable, Memory-Efficient Version
==================================================

Fixes for stability:
1. Batch processing with periodic saves
2. Numpy array pre-allocation (no list appending)
3. Memory cleanup after each batch
4. Better error handling
5. Progress checkpointing
"""

import json
import numpy as np
import pandas as pd
from pathlib import Path
from dataclasses import dataclass
from typing import Dict
import gc
import sys

# ============================================================================
# Configuration
# ============================================================================

@dataclass
class SandAgentConfig:
    """Configuration for sand agent."""
    tau_coherence: float = 0.001  # Coherence decay time (1ms)
    memory_depth: int = 1          # No echo tensors
    
    # Triadic operator weights
    eta_P: float = 1.0
    eta_S: float = 0.5
    eta_Q: float = 0.3
    eta_C: float = 0.2
    eta_B: float = 0.4
    
    # Precision function parameters
    alpha_0: float = 0.5
    alpha_S: float = 0.3
    alpha_DR: float = 0.4
    alpha_Gamma: float = 0.2
    
    # Batch processing
    batch_size: int = 10000  # Process 10k episodes at a time
    save_interval: int = 5000  # Save every 5k episodes


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
    
    def sample_basin_batch(self, n_samples: int) -> np.ndarray:
        """Sample multiple basins at once (more efficient)."""
        return np.random.choice(self.basin_ids, size=n_samples, p=self.basin_probs)
    
    def get_basin_params(self, basin_id: int) -> Dict:
        """Get parameters for a specific basin."""
        return self.basins[str(basin_id)]


class SandAgentLite:
    """
    Lightweight, stable sand agent.
    
    Key improvements:
    - Pre-allocated arrays (no dynamic appending)
    - Batch processing with memory cleanup
    - Periodic checkpointing
    - Better error handling
    """
    
    def __init__(self, config: SandAgentConfig, basin_prior: BasinPrior):
        self.config = config
        self.basin_prior = basin_prior
        
        # State (scalar, not arrays)
        self.DR = 0.0
        self.S = 0.0
        self.Gamma = 0.0
    
    def compute_precision(self, DR: float, S: float, Gamma: float) -> float:
        """Compute precision (vectorized)."""
        cfg = self.config
        logit = (
            cfg.alpha_0 + 
            cfg.alpha_S * S - 
            cfg.alpha_DR * DR - 
            cfg.alpha_Gamma * Gamma
        )
        return 1.0 / (1.0 + np.exp(-logit))
    
    def simulate_batch(self, n_samples: int) -> pd.DataFrame:
        """
        Simulate a batch of samples efficiently.
        
        Uses vectorized operations instead of loops.
        """
        # Sample basins for entire batch
        basin_ids = self.basin_prior.sample_basin_batch(n_samples)
        
        # Pre-allocate arrays
        DR_array = np.zeros(n_samples)
        S_array = np.zeros(n_samples)
        Gamma_array = np.zeros(n_samples)
        Q_array = np.zeros(n_samples)
        C_array = np.zeros(n_samples)
        B_array = np.zeros(n_samples, dtype=int)
        pi_array = np.zeros(n_samples)
        g_array = np.zeros(n_samples)
        O_P_array = np.zeros(n_samples)
        O_S_array = np.zeros(n_samples)
        O_C_array = np.zeros(n_samples)
        operator_norm_array = np.zeros(n_samples)
        strategy_array = np.empty(n_samples, dtype=object)
        
        # Get basin parameters for each sample
        coherence_means = np.zeros(n_samples)
        transition_rates = np.zeros(n_samples)
        temporal_persistence = np.zeros(n_samples)
        
        for i, bid in enumerate(basin_ids):
            params = self.basin_prior.get_basin_params(bid)
            coherence_means[i] = params['coherence_mean']
            transition_rates[i] = params['transition_rate']
            temporal_persistence[i] = params['temporal_persistence']
            strategy_array[i] = params['strategy']
        
        # Vectorized state computation
        DR_array = np.clip(
            1.0 - coherence_means + 0.1 * np.random.randn(n_samples),
            0, 1
        )
        
        S_array = np.clip(
            transition_rates + 0.1 * np.random.randn(n_samples),
            0, 5
        )
        
        Gamma_array = np.clip(
            1.0 / (temporal_persistence + 0.1) + 0.1 * np.random.randn(n_samples),
            0, 2
        )
        
        # Coherence drop and contrast (simplified)
        Q_array = np.abs(0.1 * np.random.randn(n_samples))
        C_array = np.abs(0.05 * np.random.randn(n_samples))
        
        # Shadow flag
        B_array = (DR_array > 0.7).astype(int)
        
        # Phase gate (theta oscillation)
        phi = 2 * np.pi * np.random.rand(n_samples)
        g_array = (phi < 0.4 * np.pi).astype(float)
        
        # Precision
        pi_array = self.compute_precision(DR_array, S_array, Gamma_array)
        
        # Operator components (vectorized)
        cfg = self.config
        
        O_P_array = -g_array * cfg.eta_P * pi_array * np.random.randn(n_samples)
        O_S_array = g_array * cfg.eta_S * S_array * np.random.randn(n_samples)
        O_C_array = g_array * (
            cfg.eta_Q * Q_array * np.random.randn(n_samples) +
            cfg.eta_C * C_array * np.random.randn(n_samples) -
            cfg.eta_B * B_array * np.random.randn(n_samples)
        )
        
        operator_norm_array = np.sqrt(O_P_array**2 + O_S_array**2 + O_C_array**2)
        
        # Build dataframe
        df = pd.DataFrame({
            'basin_id': basin_ids,
            'strategy': strategy_array,
            'DR': DR_array,
            'S': S_array,
            'Q': Q_array,
            'C': C_array,
            'B': B_array,
            'Gamma': Gamma_array,
            'pi': pi_array,
            'g': g_array,
            'O_P': O_P_array,
            'O_S': O_S_array,
            'O_C': O_C_array,
            'operator_norm': operator_norm_array
        })
        
        return df
    
    def train(self, n_episodes: int, episode_length: int, output_dir: Path):
        """
        Train with batch processing and checkpointing.
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        print("\n" + "="*70)
        print("SAND AGENT LITE - STABLE TRAINING")
        print("="*70)
        print(f"\nConfig:")
        print(f"  Total samples: {n_episodes * episode_length:,}")
        print(f"  Batch size: {self.config.batch_size:,}")
        print(f"  Save interval: {self.config.save_interval:,}")
        
        total_samples = n_episodes * episode_length
        n_batches = int(np.ceil(total_samples / self.config.batch_size))
        
        print(f"  Number of batches: {n_batches}")
        print(f"\nStarting batch processing...")
        
        # Track checkpoint files
        checkpoint_files = []
        
        for batch_idx in range(n_batches):
            try:
                # Compute batch size (last batch may be smaller)
                batch_start = batch_idx * self.config.batch_size
                batch_end = min((batch_idx + 1) * self.config.batch_size, total_samples)
                current_batch_size = batch_end - batch_start
                
                print(f"\n  Batch {batch_idx + 1}/{n_batches} ({current_batch_size:,} samples)...", end=' ')
                sys.stdout.flush()
                
                # Simulate batch
                df_batch = self.simulate_batch(current_batch_size)
                
                # Save batch
                checkpoint_file = output_dir / f'checkpoint_batch_{batch_idx:04d}.csv'
                df_batch.to_csv(checkpoint_file, index=False)
                checkpoint_files.append(checkpoint_file)
                
                print("✓")
                
                # Memory cleanup
                del df_batch
                gc.collect()
                
                # Progress update
                if (batch_idx + 1) % 10 == 0:
                    progress_pct = 100 * (batch_idx + 1) / n_batches
                    print(f"    Progress: {progress_pct:.1f}% complete")
                
            except Exception as e:
                print(f"\n  ✗ Batch {batch_idx + 1} failed: {e}")
                print(f"    Continuing with next batch...")
                continue
        
        print("\n✓ All batches complete!")
        print(f"\nMerging {len(checkpoint_files)} checkpoint files...")
        
        # Merge all checkpoints
        try:
            dfs = []
            for i, ckpt_file in enumerate(checkpoint_files):
                if (i + 1) % 10 == 0:
                    print(f"  Loading checkpoint {i+1}/{len(checkpoint_files)}...")
                dfs.append(pd.read_csv(ckpt_file))
            
            df_final = pd.concat(dfs, ignore_index=True)
            
            # Save final result
            final_path = output_dir / 'sand_landscape_final.csv'
            df_final.to_csv(final_path, index=False)
            
            print(f"\n✓ Final landscape saved: {final_path}")
            print(f"  Total samples: {len(df_final):,}")
            
            # Clean up checkpoints
            print(f"\nCleaning up {len(checkpoint_files)} checkpoint files...")
            for ckpt_file in checkpoint_files:
                ckpt_file.unlink()
            
            print("✓ Cleanup complete!")
            
            return df_final
            
        except Exception as e:
            print(f"\n✗ Merge failed: {e}")
            print(f"  Checkpoint files preserved in: {output_dir}")
            print(f"  You can manually merge them later.")
            return None


# ============================================================================
# Analysis Functions
# ============================================================================

def analyze_landscape(df: pd.DataFrame, output_dir: Path):
    """Generate analysis plots."""
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    output_dir = Path(output_dir)
    
    print("\n" + "="*70)
    print("LANDSCAPE ANALYSIS")
    print("="*70)
    
    # Summary statistics
    print("\nBasin Statistics:")
    basin_stats = df.groupby('basin_id').agg({
        'DR': ['mean', 'std'],
        'S': ['mean', 'std'],
        'operator_norm': ['mean', 'std'],
        'strategy': 'first'
    }).round(3)
    print(basin_stats)
    
    # Strategy statistics
    print("\nStrategy Statistics:")
    strategy_stats = df.groupby('strategy').agg({
        'DR': 'mean',
        'S': 'mean',
        'Gamma': 'mean',
        'operator_norm': 'mean'
    }).round(3)
    print(strategy_stats)
    
    # Plot 1: DR distribution by strategy
    print("\nGenerating plots...")
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # DR by strategy
    for strategy in df['strategy'].unique():
        data = df[df['strategy'] == strategy]['DR']
        axes[0, 0].hist(data, bins=50, alpha=0.5, label=strategy, density=True)
    axes[0, 0].set_xlabel('Dark Residue')
    axes[0, 0].set_ylabel('Density')
    axes[0, 0].set_title('DR Distribution by Strategy')
    axes[0, 0].legend()
    axes[0, 0].grid(alpha=0.3)
    
    # Surprise by strategy
    for strategy in df['strategy'].unique():
        data = df[df['strategy'] == strategy]['S']
        axes[0, 1].hist(data, bins=50, alpha=0.5, label=strategy, density=True)
    axes[0, 1].set_xlabel('Surprise')
    axes[0, 1].set_ylabel('Density')
    axes[0, 1].set_title('Surprise Distribution by Strategy')
    axes[0, 1].legend()
    axes[0, 1].grid(alpha=0.3)
    
    # Operator norm by strategy
    df.boxplot(column='operator_norm', by='strategy', ax=axes[1, 0])
    axes[1, 0].set_title('Operator Norm by Strategy')
    axes[1, 0].set_xlabel('Strategy')
    axes[1, 0].set_ylabel('Operator Norm')
    
    # Precision vs Gamma
    for strategy in df['strategy'].unique():
        mask = df['strategy'] == strategy
        axes[1, 1].scatter(
            df[mask]['Gamma'],
            df[mask]['pi'],
            alpha=0.1,
            s=1,
            label=strategy
        )
    axes[1, 1].set_xlabel('Temporal Pressure (Γ)')
    axes[1, 1].set_ylabel('Precision (Π)')
    axes[1, 1].set_title('Precision vs Temporal Pressure')
    axes[1, 1].legend()
    axes[1, 1].grid(alpha=0.3)
    
    plt.tight_layout()
    plot_path = output_dir / 'sand_landscape_analysis.png'
    plt.savefig(plot_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Analysis plot saved: {plot_path}")


# ============================================================================
# Main
# ============================================================================

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Sand Agent Lite - Stable, memory-efficient training"
    )
    parser.add_argument(
        'basin_json',
        type=Path,
        help="Basin structure JSON from basin_extractor.py"
    )
    parser.add_argument(
        '--output-dir',
        type=Path,
        default=Path('./sand_agent_lite_results'),
        help="Output directory"
    )
    parser.add_argument(
        '--n-episodes',
        type=int,
        default=1000,
        help="Number of episodes (default: 1000)"
    )
    parser.add_argument(
        '--episode-length',
        type=int,
        default=100,
        help="Samples per episode (default: 100)"
    )
    parser.add_argument(
        '--batch-size',
        type=int,
        default=10000,
        help="Batch size for processing (default: 10000)"
    )
    
    args = parser.parse_args()
    
    # Create output directory
    args.output_dir.mkdir(parents=True, exist_ok=True)
    
    print("\n" + "="*70)
    print("SAND AGENT LITE")
    print("="*70)
    print(f"\nBasin structure: {args.basin_json}")
    print(f"Output directory: {args.output_dir}")
    
    # Load basin prior
    basin_prior = BasinPrior(args.basin_json)
    
    # Configure
    config = SandAgentConfig(batch_size=args.batch_size)
    
    # Create agent
    agent = SandAgentLite(config, basin_prior)
    
    # Train
    df = agent.train(
        n_episodes=args.n_episodes,
        episode_length=args.episode_length,
        output_dir=args.output_dir
    )
    
    # Analyze
    if df is not None:
        analyze_landscape(df, args.output_dir)
    
    print("\n" + "="*70)
    print("COMPLETE")
    print("="*70)


if __name__ == '__main__':
    main()
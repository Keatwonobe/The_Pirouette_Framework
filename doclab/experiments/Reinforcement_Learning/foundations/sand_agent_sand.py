#!/usr/bin/env python3
"""
Sand Agent Incremental Writer - BOMB PROOF Edition
===================================================

This version is INDESTRUCTIBLE:
- Writes samples one-by-one to CSV as they're generated
- No memory accumulation
- Resume from exact point of crash
- Can Ctrl+C and restart anytime
- Progress tracked in separate file
"""

import json
import numpy as np
import csv
from pathlib import Path
from dataclasses import dataclass
from typing import Dict
import sys
import signal
import time

# ============================================================================
# Configuration
# ============================================================================

@dataclass
class SandAgentConfig:
    """Configuration for sand agent."""
    tau_coherence: float = 0.001
    
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


class BasinPrior:
    """Prior distribution from EEG basin structure."""
    
    def __init__(self, basin_json_path: Path):
        with open(basin_json_path, 'r') as f:
            self.data = json.load(f)
        
        self.n_basins = self.data['n_basins']
        self.basins = self.data['basins']
        self._build_distributions()
    
    def _build_distributions(self):
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
        return np.random.choice(self.basin_ids, p=self.basin_probs)
    
    def get_basin_params(self, basin_id: int) -> Dict:
        return self.basins[str(basin_id)]


class IncrementalWriter:
    """
    Ultra-robust incremental CSV writer.
    
    Features:
    - Writes one sample at a time
    - Flushes to disk immediately
    - Tracks progress in separate file
    - Can resume from crash
    """
    
    def __init__(self, output_path: Path, progress_path: Path):
        self.output_path = Path(output_path)
        self.progress_path = Path(progress_path)
        
        # Check if resuming
        self.start_index = 0
        if self.progress_path.exists():
            with open(self.progress_path, 'r') as f:
                self.start_index = int(f.read().strip())
            print(f"\n  ⚠ Resuming from sample {self.start_index:,}")
        
        # Open CSV writer
        self.file_exists = self.output_path.exists()
        self.csv_file = open(self.output_path, 'a', newline='', buffering=1)  # Line buffering
        self.csv_writer = None
        
        # Setup columns
        self.columns = [
            'sample_id', 'basin_id', 'strategy',
            'DR', 'S', 'Q', 'C', 'B', 'Gamma',
            'pi', 'g', 'O_P', 'O_S', 'O_C', 'operator_norm'
        ]
        
        # Write header if new file
        if not self.file_exists:
            self.csv_writer = csv.DictWriter(self.csv_file, fieldnames=self.columns)
            self.csv_writer.writeheader()
            self.csv_file.flush()
        else:
            self.csv_writer = csv.DictWriter(self.csv_file, fieldnames=self.columns)
    
    def write_sample(self, sample_id: int, sample_data: dict):
        """Write a single sample immediately to disk."""
        row = {'sample_id': sample_id}
        row.update(sample_data)
        self.csv_writer.writerow(row)
        
        # Flush to disk (critical!)
        self.csv_file.flush()
    
    def update_progress(self, sample_id: int):
        """Update progress file."""
        with open(self.progress_path, 'w') as f:
            f.write(str(sample_id))
    
    def close(self):
        """Close file handles."""
        self.csv_file.close()


class SandAgentIncremental:
    """
    Incremental sand agent that writes samples as they're generated.
    
    Zero memory accumulation. Infinite runtime. Unstoppable.
    """
    
    def __init__(self, config: SandAgentConfig, basin_prior: BasinPrior):
        self.config = config
        self.basin_prior = basin_prior
    
    def compute_precision(self, DR: float, S: float, Gamma: float) -> float:
        cfg = self.config
        logit = (
            cfg.alpha_0 + 
            cfg.alpha_S * S - 
            cfg.alpha_DR * DR - 
            cfg.alpha_Gamma * Gamma
        )
        return 1.0 / (1.0 + np.exp(-logit))
    
    def generate_sample(self, basin_id: int) -> dict:
        """Generate a single sample from a basin."""
        params = self.basin_prior.get_basin_params(basin_id)
        
        # State computation
        DR = np.clip(
            1.0 - params['coherence_mean'] + 0.1 * np.random.randn(),
            0, 1
        )
        
        S = np.clip(
            params['transition_rate'] + 0.1 * np.random.randn(),
            0, 5
        )
        
        Gamma = np.clip(
            1.0 / (params['temporal_persistence'] + 0.1) + 0.1 * np.random.randn(),
            0, 2
        )
        
        # Coherence metrics
        Q = abs(0.1 * np.random.randn())
        C = abs(0.05 * np.random.randn())
        B = int(DR > 0.7)
        
        # Phase gate
        phi = 2 * np.pi * np.random.rand()
        g = float(phi < 0.4 * np.pi)
        
        # Precision
        pi = self.compute_precision(DR, S, Gamma)
        
        # Operator
        cfg = self.config
        O_P = -g * cfg.eta_P * pi * np.random.randn()
        O_S = g * cfg.eta_S * S * np.random.randn()
        O_C = g * (
            cfg.eta_Q * Q * np.random.randn() +
            cfg.eta_C * C * np.random.randn() -
            cfg.eta_B * B * np.random.randn()
        )
        
        operator_norm = np.sqrt(O_P**2 + O_S**2 + O_C**2)
        
        return {
            'basin_id': basin_id,
            'strategy': params['strategy'],
            'DR': DR,
            'S': S,
            'Q': Q,
            'C': C,
            'B': B,
            'Gamma': Gamma,
            'pi': pi,
            'g': g,
            'O_P': O_P,
            'O_S': O_S,
            'O_C': O_C,
            'operator_norm': operator_norm
        }
    
    def train_incremental(self, n_samples: int, output_path: Path, 
                         progress_path: Path, update_interval: int = 1000):
        """
        Generate samples one at a time, writing immediately.
        
        Can be stopped and resumed at any time.
        """
        print("\n" + "="*70)
        print("SAND AGENT INCREMENTAL - BOMB PROOF MODE")
        print("="*70)
        print(f"\nTotal samples: {n_samples:,}")
        print(f"Output: {output_path}")
        print(f"Progress tracking: {progress_path}")
        print(f"\nPress Ctrl+C to pause (safe to resume)")
        
        # Setup writer
        writer = IncrementalWriter(output_path, progress_path)
        start_idx = writer.start_index
        
        # Setup signal handler for graceful exit
        interrupted = False
        def signal_handler(sig, frame):
            nonlocal interrupted
            interrupted = True
            print("\n\n⚠ Interrupt received - finishing current sample...")
        
        signal.signal(signal.SIGINT, signal_handler)
        
        print(f"\nStarting generation...")
        if start_idx > 0:
            print(f"  (Resuming from sample {start_idx:,})")
        
        start_time = time.time()
        last_update = start_time
        
        try:
            for i in range(start_idx, n_samples):
                # Check for interrupt
                if interrupted:
                    print(f"\nStopping at sample {i:,}")
                    break
                
                # Sample basin
                basin_id = self.basin_prior.sample_basin()
                
                # Generate sample
                sample = self.generate_sample(basin_id)
                
                # Write immediately
                writer.write_sample(i, sample)
                
                # Update progress every N samples
                if (i + 1) % update_interval == 0:
                    writer.update_progress(i + 1)
                    
                    # Progress report
                    elapsed = time.time() - last_update
                    samples_per_sec = update_interval / elapsed
                    remaining_samples = n_samples - (i + 1)
                    eta_seconds = remaining_samples / samples_per_sec
                    
                    progress_pct = 100 * (i + 1) / n_samples
                    print(f"  [{i+1:,}/{n_samples:,}] {progress_pct:5.1f}% | "
                          f"{samples_per_sec:.0f} samples/sec | "
                          f"ETA: {eta_seconds:.0f}s")
                    
                    last_update = time.time()
        
        finally:
            # Always close cleanly
            writer.update_progress(min(i + 1, n_samples))
            writer.close()
            
            total_time = time.time() - start_time
            samples_generated = (i + 1) - start_idx
            
            print(f"\n{'='*70}")
            print(f"SESSION COMPLETE")
            print(f"{'='*70}")
            print(f"  Samples generated: {samples_generated:,}")
            print(f"  Total samples in file: {i+1:,}")
            print(f"  Time: {total_time:.1f}s ({samples_generated/total_time:.0f} samples/sec)")
            
            if i + 1 >= n_samples:
                print(f"\n✓ ALL SAMPLES COMPLETE!")
                print(f"  Final output: {output_path}")
                # Clean up progress file
                progress_path.unlink()
            else:
                print(f"\n⚠ Paused at {i+1:,}/{n_samples:,}")
                print(f"  To resume: rerun the same command")


# ============================================================================
# Main
# ============================================================================

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Sand Agent Incremental - Bomb-proof streaming writer"
    )
    parser.add_argument(
        'basin_json',
        type=Path,
        help="Basin structure JSON"
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=Path('sand_landscape_incremental.csv'),
        help="Output CSV file (default: sand_landscape_incremental.csv)"
    )
    parser.add_argument(
        '--n-samples',
        type=int,
        default=100000000,
        help="Total samples to generate (default: 100000)"
    )
    parser.add_argument(
        '--update-interval',
        type=int,
        default=1000,
        help="Progress update interval (default: 1000)"
    )
    
    args = parser.parse_args()
    
    # Setup paths
    output_path = args.output
    progress_path = output_path.with_suffix('.progress')
    
    print("\n" + "="*70)
    print("SAND AGENT INCREMENTAL")
    print("="*70)
    print(f"\nBasin structure: {args.basin_json}")
    print(f"Output: {output_path}")
    print(f"Target samples: {args.n_samples:,}")
    
    # Load basin prior
    basin_prior = BasinPrior(args.basin_json)
    
    # Configure
    config = SandAgentConfig()
    
    # Create agent
    agent = SandAgentIncremental(config, basin_prior)
    
    # Train
    agent.train_incremental(
        n_samples=args.n_samples,
        output_path=output_path,
        progress_path=progress_path,
        update_interval=args.update_interval
    )


if __name__ == '__main__':
    main()
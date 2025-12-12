#!/usr/bin/env python3
"""
Valley Crossing Detector - Coherence Phase Transition Analysis
===============================================================

Treats 3.3M+ sand_agent_sand samples as a temporal trajectory through
coherence phase space. Identifies moments where the agent:

1. **Entered a coherence valley** (DR spike, coherence drop)
2. **Traversed the valley** (sustained high Γ, high curvature)
3. **Exited to higher basin** (coherence reconstructs at higher level)

This captures the "symmetry break" moment and gives us a template for
inducing valley crossings on demand.

Key Innovation: We're treating your massive dataset not as random samples,
but as a **journey through information space** - watching the agent discover
its hemispheric structure in real-time.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from scipy.signal import find_peaks, savgol_filter
from scipy.ndimage import gaussian_filter1d
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import argparse
from dataclasses import dataclass
from typing import List, Tuple, Optional

sns.set_style("darkgrid")
plt.rcParams['figure.facecolor'] = 'white'


# =====================================================================
# §1: Valley Crossing Event Definition
# =====================================================================

@dataclass
class ValleyCrossing:
    """
    A detected valley crossing event.
    
    Per the challenge: A sequence where DR increases, coherence drops,
    then both reconstruct at a higher level.
    """
    # Temporal bounds
    entry_idx: int        # When valley entry detected
    nadir_idx: int        # Deepest point of valley
    exit_idx: int         # When valley exit detected
    
    # Entry state
    entry_DR: float
    entry_coherence: float
    entry_gamma: float
    entry_PC1: float
    
    # Nadir state (deepest in valley)
    nadir_DR: float
    nadir_coherence: float
    nadir_gamma: float
    nadir_curvature: float
    
    # Exit state
    exit_DR: float
    exit_coherence: float
    exit_gamma: float
    exit_PC1: float
    
    # Metrics
    DR_increase: float          # Entry → Nadir
    DR_decrease: float          # Nadir → Exit
    coherence_drop: float       # Entry → Nadir
    coherence_gain: float       # Nadir → Exit
    net_coherence_gain: float   # Entry → Exit
    valley_duration: int        # Timesteps
    
    # New temporal shape fields
    drop_duration: int          # entry → nadir
    recovery_duration: int      # nadir → exit
    recovery_fraction: float    # recovery_duration / valley_duration

    # New micro-structure fields
    valley_chatter: float       # std of high-freq coherence residual
    coherence_overshoot: float  # exit_coherence - entry_coherence

    # Classification
    is_successful: bool         # Did it reach higher coherence?
    is_hemispheric_split: bool  # Did PC1 cross boundary?
    
    @property
    def valley_depth(self) -> float:
        """How deep into the valley (peak DR increase)."""
        return self.DR_increase
    
    @property
    def reconstruction_quality(self) -> float:
        """How well did coherence reconstruct (exit/entry ratio)."""
        if self.entry_coherence > 0:
            return self.exit_coherence / self.entry_coherence
        return 0.0
    
    def __repr__(self):
        return (f"ValleyCrossing(t={self.entry_idx}->{self.exit_idx}, "
                f"ΔDR={self.DR_increase:.3f}, "
                f"Δcoh={self.net_coherence_gain:.3f}, "
                f"success={self.is_successful})")


# =====================================================================
# §2: Coherence Metrics Computer
# =====================================================================

class CoherenceMetrics:
    """
    Computes derived coherence metrics from raw sand agent data.
    
    These aren't in your CSV but are needed for valley detection.
    """
    
    @staticmethod
    def compute_coherence_proxy(df: pd.DataFrame) -> np.ndarray:
        """
        Estimate coherence from available metrics.
        
        High coherence = low DR + high precision + stable operator norm
        """
        # Normalize each component to [0, 1]
        # Use .values to get raw numpy arrays, avoiding index-alignment issues
        DR_norm_series = 1 - (df['DR'] - df['DR'].min()) / (df['DR'].max() - df['DR'].min() + 1e-6)
        pi_norm_series = (df['pi'] - df['pi'].min()) / (df['pi'].max() - df['pi'].min() + 1e-6)
        
        DR_norm = DR_norm_series.values
        pi_norm = pi_norm_series.values
        
        # Operator stability (inverse of variance in local window)
        op_norm = df['operator_norm'].values
        op_smooth = gaussian_filter1d(op_norm, sigma=10)
        op_stability = 1 - np.abs(op_norm - op_smooth) / (np.abs(op_norm - op_smooth).max() + 1e-6)
        
        # Weighted combination (now pure numpy math)
        coherence = 0.5 * DR_norm + 0.3 * pi_norm + 0.2 * op_stability
        
        return coherence
    
    @staticmethod
    def compute_curvature(df: pd.DataFrame, window: int = 50) -> np.ndarray:
        """
        Estimate manifold curvature κ from local variance in (Γ, DR, S).
        
        High curvature = near basin boundary = potential valley crossing.
        """
        features = df[['Gamma', 'DR', 'S']].values
        
        curvature = np.zeros(len(df))
        for i in range(window, len(df) - window):
            local_window = features[i-window:i+window]
            # Curvature ≈ trace of covariance matrix
            cov = np.cov(local_window.T)
            curvature[i] = np.trace(cov)
        
        # Smooth
        curvature = gaussian_filter1d(curvature, sigma=5)
        
        return curvature


# =====================================================================
# §3: Valley Crossing Detector
# =====================================================================

class ValleyCrossingDetector:
    """
    Detects valley crossing events in temporal coherence trajectories.
    
    Algorithm:
    1. Find DR spikes (potential valley entries)
    2. Check if coherence drops during spike
    3. Verify reconstruction after spike
    4. Classify as successful valley crossing if net coherence gain
    """
    
    def __init__(self,
                 DR_spike_threshold: float = 0.15,
                 coherence_drop_threshold: float = 0.10,
                 min_valley_duration: int = 20,
                 max_valley_duration: int = 500):
        """
        Args:
            DR_spike_threshold: Minimum DR increase to consider valley entry
            coherence_drop_threshold: Minimum coherence drop to confirm valley
            min_valley_duration: Minimum timesteps for valid valley
            max_valley_duration: Maximum timesteps to search for exit
        """
        self.DR_spike_threshold = DR_spike_threshold
        self.coherence_drop_threshold = coherence_drop_threshold
        self.min_valley_duration = min_valley_duration
        self.max_valley_duration = max_valley_duration
    
    def detect_valleys(self, df: pd.DataFrame) -> List[ValleyCrossing]:
        """
        Main detection algorithm.
        
        Returns list of detected valley crossing events.
        """
        print("\n" + "="*70)
        print("VALLEY CROSSING DETECTION")
        print("="*70)
        
        # Compute coherence if not present
        if 'coherence' not in df.columns:
            print("Computing coherence proxy from (DR, π, operator_norm)...")
            df['coherence'] = CoherenceMetrics.compute_coherence_proxy(df)
        
        # Compute curvature if not present
        if 'curvature' not in df.columns:
            print("Computing manifold curvature κ...")
            df['curvature'] = CoherenceMetrics.compute_curvature(df)
        
        # Smooth traces for peak detection
        DR_smooth = gaussian_filter1d(df['DR'].values, sigma=10)
        coherence_smooth = gaussian_filter1d(df['coherence'].values, sigma=10)
        
        # Find DR spikes (potential valley entries)
        DR_peaks, _ = find_peaks(DR_smooth, 
                          prominence=self.DR_spike_threshold,
                          distance=self.min_valley_duration)
        
        print(f"\nFound {len(DR_peaks)} potential valley entries (DR spikes)")
        
        valleys = []
        
        for peak_idx in DR_peaks:
            valley = self._analyze_potential_valley(df, peak_idx, DR_smooth, coherence_smooth)
            if valley:
                valleys.append(valley)
        
        # Sort by entry time
        valleys.sort(key=lambda v: v.entry_idx)
        
        print(f"\n✓ Detected {len(valleys)} valley crossing events")
        print(f"  Successful crossings: {sum(v.is_successful for v in valleys)}")
        print(f"  Hemispheric splits: {sum(v.is_hemispheric_split for v in valleys)}")
        
        return valleys
    
    def _analyze_potential_valley(self,
                                   df: pd.DataFrame,
                                   peak_idx: int,
                                   DR_smooth: np.ndarray,
                                   coherence_smooth: np.ndarray) -> Optional[ValleyCrossing]:
        """
        Analyze a DR spike to determine if it's a valid valley crossing.
        
        Returns ValleyCrossing object if valid, None otherwise.
        """
        # Find valley entry (before peak)
        entry_window = max(0, peak_idx - self.min_valley_duration)
        entry_idx = entry_window
        
        # Find valley exit (after peak)
        exit_window = min(len(df), peak_idx + self.max_valley_duration)
        
        # Check for coherence drop around peak
        coherence_at_entry = coherence_smooth[entry_idx]
        coherence_at_peak = coherence_smooth[peak_idx]
        coherence_drop = coherence_at_entry - coherence_at_peak
        
        if coherence_drop < self.coherence_drop_threshold:
            return None  # No significant coherence drop
        
        # Search for exit (coherence reconstruction)
        exit_idx = None
        for i in range(peak_idx + self.min_valley_duration, exit_window):
            if coherence_smooth[i] > coherence_at_entry * 0.95:  # Recovered to 95% of entry
                exit_idx = i
                break
        
        if exit_idx is None:
            return None  # No exit found
        
        # Validate duration
        valley_duration = exit_idx - entry_idx
        if valley_duration < self.min_valley_duration:
            return None
        
        # Temporal shape
        drop_duration = peak_idx - entry_idx
        recovery_duration = exit_idx - peak_idx
        recovery_fraction = recovery_duration / max(valley_duration, 1)

        # --- Chatter / high-frequency structure inside valley ---
        # Use a slower smoothing to define the trend, then measure residuals.
        coherence_full = df['coherence'].values

        # Slow trend – higher sigma than the main detector
        coherence_trend = gaussian_filter1d(coherence_full, sigma=50)

        residual = coherence_full - coherence_trend

        # Restrict to inside-valley segment
        valley_residual = residual[entry_idx:exit_idx + 1]
        valley_chatter = float(np.std(valley_residual))

        # Extract states
        entry_state = df.iloc[entry_idx]
        nadir_state = df.iloc[peak_idx]
        exit_state = df.iloc[exit_idx]
        coherence_overshoot = exit_state['coherence'] - entry_state['coherence']        

        # Compute metrics
        DR_increase = nadir_state['DR'] - entry_state['DR']
        DR_decrease = nadir_state['DR'] - exit_state['DR']
        coherence_gain = exit_state['coherence'] - nadir_state['coherence']
        net_coherence_gain = exit_state['coherence'] - entry_state['coherence']
        
        # Check if hemispheric boundary crossed
        PC1_entry = entry_state.get('PC1', 0)
        PC1_exit = exit_state.get('PC1', 0)
        is_hemispheric = np.sign(PC1_entry) != np.sign(PC1_exit)
        
        # Classify success
        is_successful = net_coherence_gain > 0
        
        valley = ValleyCrossing(
            entry_idx=entry_idx,
            nadir_idx=peak_idx,
            exit_idx=exit_idx,
            entry_DR=entry_state['DR'],
            entry_coherence=entry_state['coherence'],
            entry_gamma=entry_state['Gamma'],
            entry_PC1=PC1_entry,
            nadir_DR=nadir_state['DR'],
            nadir_coherence=nadir_state['coherence'],
            nadir_gamma=nadir_state['Gamma'],
            nadir_curvature=nadir_state.get('curvature', 0),
            exit_DR=exit_state['DR'],
            exit_coherence=exit_state['coherence'],
            exit_gamma=exit_state['Gamma'],
            exit_PC1=PC1_exit,
            DR_increase=DR_increase,
            DR_decrease=DR_decrease,
            coherence_drop=coherence_drop,
            coherence_gain=coherence_gain,
            net_coherence_gain=net_coherence_gain,
            valley_duration=valley_duration,
            drop_duration=drop_duration,
            recovery_duration=recovery_duration,
            recovery_fraction=recovery_fraction,
            valley_chatter=valley_chatter,
            coherence_overshoot=coherence_overshoot,
            is_successful=is_successful,
            is_hemispheric_split=is_hemispheric
        )

        
        return valley
    
    def find_symmetry_break(self, df: pd.DataFrame, valleys: List[ValleyCrossing]) -> Optional[ValleyCrossing]:
        """
        Identify THE symmetry break - the valley crossing that created hemispheric structure.
        
        This is the FIRST successful hemispheric split.
        """
        hemispheric_valleys = [v for v in valleys if v.is_hemispheric_split and v.is_successful]
        
        if not hemispheric_valleys:
            return None
        
        # Return earliest
        symmetry_break = min(hemispheric_valleys, key=lambda v: v.entry_idx)
        
        print(f"\n🌟 SYMMETRY BREAK DETECTED at sample {symmetry_break.entry_idx}")
        print(f"  Duration: {symmetry_break.valley_duration} samples")
        print(f"  DR increase: {symmetry_break.DR_increase:.3f}")
        print(f"  Coherence drop: {symmetry_break.coherence_drop:.3f}")
        print(f"  Net coherence gain: {symmetry_break.net_coherence_gain:.3f}")
        print(f"  PC1: {symmetry_break.entry_PC1:.3f} → {symmetry_break.exit_PC1:.3f}")
        
        return symmetry_break


# =====================================================================
# §4: Visualization Suite
# =====================================================================

class ValleyVisualizer:
    """Visualizes valley crossing events in multiple views."""
    
    @staticmethod
    def plot_valley_timeline(df: pd.DataFrame, 
                             valleys: List[ValleyCrossing],
                             output_path: Path):
        """
        Plot the full timeline with valley crossings marked.
        """
        fig, axes = plt.subplots(4, 1, figsize=(16, 12), sharex=True)
        
        time = np.arange(len(df))
        
        # Downsample for plotting (every 100th point)
        step = max(1, len(df) // 10000)
        time_plot = time[::step]
        
        # 1. DR trace with valleys
        ax = axes[0]
        ax.plot(time_plot, df['DR'].values[::step], 'b-', linewidth=0.5, alpha=0.6)
        
        for valley in valleys:
            color = 'green' if valley.is_successful else 'red'
            alpha = 0.8 if valley.is_hemispheric_split else 0.3
            ax.axvspan(valley.entry_idx, valley.exit_idx, 
                      color=color, alpha=alpha, linewidth=0)
        
        ax.set_ylabel('DR', fontsize=12)
        ax.set_title('Valley Crossing Timeline (Green=Success, Red=Failed)', 
                    fontsize=14, fontweight='bold')
        ax.grid(alpha=0.3)
        
        # 2. Coherence trace
        ax = axes[1]
        ax.plot(time_plot, df['coherence'].values[::step], 'purple', linewidth=0.5, alpha=0.6)
        
        for valley in valleys:
            if valley.is_successful:
                ax.plot([valley.entry_idx, valley.exit_idx],
                       [valley.entry_coherence, valley.exit_coherence],
                       'g-', linewidth=2, alpha=0.5)
        
        ax.set_ylabel('Coherence', fontsize=12)
        ax.set_title('Coherence Reconstruction', fontsize=14, fontweight='bold')
        ax.grid(alpha=0.3)
        
        # 3. Gamma (load)
        ax = axes[2]
        ax.plot(time_plot, df['Gamma'].values[::step], 'orange', linewidth=0.5, alpha=0.6)
        ax.set_ylabel('Γ (Load)', fontsize=12)
        ax.set_title('Temporal Pressure During Crossings', fontsize=14, fontweight='bold')
        ax.grid(alpha=0.3)
        
        # 4. Curvature
        ax = axes[3]
        if 'curvature' in df.columns:
            ax.plot(time_plot, df['curvature'].values[::step], 'brown', linewidth=0.5, alpha=0.6)
            ax.set_ylabel('κ (Curvature)', fontsize=12)
            ax.set_title('Manifold Curvature (Basin Boundaries)', fontsize=14, fontweight='bold')
        ax.set_xlabel('Sample Index', fontsize=12)
        ax.grid(alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Timeline plot saved: {output_path.name}")
    
    @staticmethod
    def plot_valley_phase_space(df: pd.DataFrame,
                                valleys: List[ValleyCrossing],
                                output_path: Path):
        """
        Plot valleys in (DR, coherence, Γ) phase space.
        """
        fig = plt.figure(figsize=(16, 6))
        
        # 1. DR vs Coherence
        ax1 = fig.add_subplot(131)
        
        # Background points (sample)
        sample = df.sample(min(5000, len(df)))
        ax1.scatter(sample['DR'], sample['coherence'], 
                   c='lightgray', s=1, alpha=0.3, label='Background')
        
        # Valley trajectories
        for valley in valleys:
            color = 'green' if valley.is_successful else 'red'
            ax1.plot([valley.entry_DR, valley.nadir_DR, valley.exit_DR],
                    [valley.entry_coherence, valley.nadir_coherence, valley.exit_coherence],
                    'o-', color=color, markersize=6, linewidth=2, alpha=0.7)
        
        ax1.set_xlabel('DR', fontsize=12)
        ax1.set_ylabel('Coherence', fontsize=12)
        ax1.set_title('Valley Trajectories in DR-Coherence Space', fontsize=13, fontweight='bold')
        ax1.grid(alpha=0.3)
        
        # 2. Gamma vs Coherence
        ax2 = fig.add_subplot(132)
        
        ax2.scatter(sample['Gamma'], sample['coherence'],
                   c='lightgray', s=1, alpha=0.3)
        
        for valley in valleys:
            color = 'green' if valley.is_successful else 'red'
            ax2.plot([valley.entry_gamma, valley.nadir_gamma, valley.exit_gamma],
                    [valley.entry_coherence, valley.nadir_coherence, valley.exit_coherence],
                    'o-', color=color, markersize=6, linewidth=2, alpha=0.7)
        
        ax2.set_xlabel('Γ (Load)', fontsize=12)
        ax2.set_ylabel('Coherence', fontsize=12)
        ax2.set_title('Load-Coherence Dynamics', fontsize=13, fontweight='bold')
        ax2.grid(alpha=0.3)
        
        # 3. 3D view (if PC coords available)
        ax3 = fig.add_subplot(133, projection='3d')
        
        if 'PC1' in df.columns and 'PC2' in df.columns:
            sample_3d = df.sample(min(2000, len(df)))
            ax3.scatter(sample_3d['PC1'], sample_3d['PC2'], sample_3d['coherence'],
                       c='lightgray', s=1, alpha=0.2)
            
            for valley in valleys:
                color = 'green' if valley.is_successful else 'red'
                ax3.plot([valley.entry_PC1, valley.exit_PC1],
                        [0, 0],  # Would need PC2 data
                        [valley.entry_coherence, valley.exit_coherence],
                        'o-', color=color, markersize=6, linewidth=2, alpha=0.7)
            
            ax3.set_xlabel('PC1', fontsize=10)
            ax3.set_ylabel('PC2', fontsize=10)
            ax3.set_zlabel('Coherence', fontsize=10)
            ax3.set_title('Hemispheric View', fontsize=13, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Phase space plot saved: {output_path.name}")
    
    @staticmethod
    def plot_symmetry_break_detail(df: pd.DataFrame,
                                   symmetry_break: ValleyCrossing,
                                   output_path: Path,
                                   context_window: int = 500):
        """
        Detailed analysis of THE symmetry break moment.
        """
        fig, axes = plt.subplots(3, 2, figsize=(16, 12))
        
        # Extract window around symmetry break
        start = max(0, symmetry_break.entry_idx - context_window)
        end = min(len(df), symmetry_break.exit_idx + context_window)
        window = df.iloc[start:end].copy()
        window['relative_t'] = np.arange(len(window)) - (symmetry_break.entry_idx - start)
        
        # Mark key moments
        entry_t = symmetry_break.entry_idx - start
        nadir_t = symmetry_break.nadir_idx - start
        exit_t = symmetry_break.exit_idx - start
        
        # 1. DR trajectory
        ax = axes[0, 0]
        ax.plot(window['relative_t'], window['DR'], 'b-', linewidth=1.5)
        ax.axvline(0, color='orange', linestyle='--', label='Entry', linewidth=2)
        ax.axvline(nadir_t - entry_t, color='red', linestyle='--', label='Nadir', linewidth=2)
        ax.axvline(exit_t - entry_t, color='green', linestyle='--', label='Exit', linewidth=2)
        ax.axvspan(0, exit_t - entry_t, alpha=0.2, color='yellow')
        ax.set_ylabel('DR', fontsize=12)
        ax.set_title('Dark Residue Spike', fontsize=13, fontweight='bold')
        ax.legend()
        ax.grid(alpha=0.3)
        
        # 2. Coherence trajectory
        ax = axes[0, 1]
        ax.plot(window['relative_t'], window['coherence'], 'purple', linewidth=1.5)
        ax.axvline(0, color='orange', linestyle='--', linewidth=2)
        ax.axvline(nadir_t - entry_t, color='red', linestyle='--', linewidth=2)
        ax.axvline(exit_t - entry_t, color='green', linestyle='--', linewidth=2)
        ax.axvspan(0, exit_t - entry_t, alpha=0.2, color='yellow')
        ax.set_ylabel('Coherence', fontsize=12)
        ax.set_title('Coherence Valley & Reconstruction', fontsize=13, fontweight='bold')
        ax.grid(alpha=0.3)
        
        # 3. Gamma
        ax = axes[1, 0]
        ax.plot(window['relative_t'], window['Gamma'], 'orange', linewidth=1.5)
        ax.axvline(0, color='orange', linestyle='--', linewidth=2)
        ax.axvline(nadir_t - entry_t, color='red', linestyle='--', linewidth=2)
        ax.axvline(exit_t - entry_t, color='green', linestyle='--', linewidth=2)
        ax.set_ylabel('Γ (Load)', fontsize=12)
        ax.set_title('Temporal Pressure', fontsize=13, fontweight='bold')
        ax.grid(alpha=0.3)
        
        # 4. Precision
        ax = axes[1, 1]
        ax.plot(window['relative_t'], window['pi'], 'teal', linewidth=1.5)
        ax.axvline(0, color='orange', linestyle='--', linewidth=2)
        ax.axvline(nadir_t - entry_t, color='red', linestyle='--', linewidth=2)
        ax.axvline(exit_t - entry_t, color='green', linestyle='--', linewidth=2)
        ax.set_ylabel('π (Precision)', fontsize=12)
        ax.set_title('Attention/Precision Dynamics', fontsize=13, fontweight='bold')
        ax.grid(alpha=0.3)
        
        # 5. PC1 (hemisphere)
        ax = axes[2, 0]
        if 'PC1' in window.columns:
            ax.plot(window['relative_t'], window['PC1'], 'brown', linewidth=1.5)
            ax.axhline(0, color='k', linestyle='-', linewidth=2, label='Boundary')
            ax.axvline(0, color='orange', linestyle='--', linewidth=2)
            ax.axvline(nadir_t - entry_t, color='red', linestyle='--', linewidth=2)
            ax.axvline(exit_t - entry_t, color='green', linestyle='--', linewidth=2)
            ax.fill_between(window['relative_t'], 0, window['PC1'], 
                           where=(window['PC1'] > 0), alpha=0.3, color='coral', label='Right')
            ax.fill_between(window['relative_t'], 0, window['PC1'],
                           where=(window['PC1'] < 0), alpha=0.3, color='steelblue', label='Left')
        ax.set_xlabel('Relative Time (samples)', fontsize=12)
        ax.set_ylabel('PC1', fontsize=12)
        ax.set_title('Hemispheric Transition', fontsize=13, fontweight='bold')
        ax.legend()
        ax.grid(alpha=0.3)
        
        # 6. Summary statistics
        ax = axes[2, 1]
        ax.axis('off')
        
        stats_text = f"""
SYMMETRY BREAK STATISTICS

Temporal:
  Entry:    Sample {symmetry_break.entry_idx}
  Nadir:    Sample {symmetry_break.nadir_idx}
  Exit:     Sample {symmetry_break.exit_idx}
  Duration: {symmetry_break.valley_duration} samples

Dynamics:
  DR increase:   {symmetry_break.DR_increase:.4f}
  DR decrease:   {symmetry_break.DR_decrease:.4f}
  Coherence drop: {symmetry_break.coherence_drop:.4f}
  Coherence gain: {symmetry_break.coherence_gain:.4f}
  Net Δcoherence: {symmetry_break.net_coherence_gain:.4f}

Phase Space:
  Entry Γ:  {symmetry_break.entry_gamma:.3f}
  Nadir Γ:  {symmetry_break.nadir_gamma:.3f}
  Exit Γ:   {symmetry_break.exit_gamma:.3f}
  Nadir κ:  {symmetry_break.nadir_curvature:.4f}

Hemisphere:
  Entry PC1: {symmetry_break.entry_PC1:+.3f}
  Exit PC1:  {symmetry_break.exit_PC1:+.3f}
  Crossed:   {symmetry_break.is_hemispheric_split}

Classification:
  Successful:  {symmetry_break.is_successful}
  Reconstruction quality: {symmetry_break.reconstruction_quality:.2f}x
        """
        
        ax.text(0.1, 0.95, stats_text, transform=ax.transAxes,
               fontsize=10, verticalalignment='top', family='monospace',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Symmetry break detail plot saved: {output_path.name}")


# =====================================================================
# §5: Valley Signature Extractor
# =====================================================================

class ValleySignatureExtractor:
    """
    Extract the characteristic signature of valley crossings.
    
    This signature can be used as a template to induce future crossings.
    """
    
    @staticmethod
    def extract_signature(valley: ValleyCrossing, df: pd.DataFrame) -> dict:
        # Get trajectory
        traj = df.iloc[valley.entry_idx:valley.exit_idx+1]

        # --- Temporal structure inside the valley ---
        drop_duration = max(1, valley.nadir_idx - valley.entry_idx)
        recovery_duration = max(1, valley.exit_idx - valley.nadir_idx)
        recovery_fraction = recovery_duration / (drop_duration + recovery_duration)

        coh = traj['coherence'].values.astype(float)

        # Smooth coherence to get the low-freq “shape”
        coh_smooth = gaussian_filter1d(coh, sigma=5)
        residual = coh - coh_smooth

        # Chatter = high-freq energy per step
        valley_chatter = float(np.mean(np.abs(residual)))

        # Overshoot relative to entry coherence
        peak_coh = float(coh.max())
        entry_coh = float(valley.entry_coherence)
        coherence_overshoot = max(0.0, peak_coh - entry_coh)

        signature = {
            'duration': valley.valley_duration,
            'duration_normalized': valley.valley_duration / len(df),

            # New temporal breakdown
            'drop_duration': drop_duration,
            'recovery_duration': recovery_duration,
            'recovery_fraction': recovery_fraction,

            # Entry conditions
            'entry_DR': valley.entry_DR,
            'entry_coherence': valley.entry_coherence,
            'entry_gamma': valley.entry_gamma,
            'entry_PC1': valley.entry_PC1,

            # Valley characteristics
            'DR_increase_rate': valley.DR_increase / valley.valley_duration,
            'coherence_drop_rate': valley.coherence_drop / valley.valley_duration,
            'peak_gamma': float(traj['Gamma'].max()),
            'mean_gamma': float(traj['Gamma'].mean()),
            'peak_curvature': float(
                traj['curvature'].max() if 'curvature' in traj.columns else 0.0
            ),

            # New “texture” metrics
            'valley_chatter': valley_chatter,
            'coherence_overshoot': coherence_overshoot,

            # Exit conditions
            'exit_DR': valley.exit_DR,
            'exit_coherence': valley.exit_coherence,
            'exit_gamma': valley.exit_gamma,
            'exit_PC1': valley.exit_PC1,

            # Success metrics
            'net_coherence_gain': valley.net_coherence_gain,
            'reconstruction_quality': valley.reconstruction_quality,
            'is_hemispheric': valley.is_hemispheric_split,

            # Full trajectories (for hyperspace coordinates)
            'DR_trajectory': coh * 0 + traj['DR'].values,  # keep shape identical
            'coherence_trajectory': coh,
            'gamma_trajectory': traj['Gamma'].values,
        }

        return signature

    
    @staticmethod
    def compute_average_signature(valleys: List[ValleyCrossing], df: pd.DataFrame) -> dict:
        """
        Compute average signature across multiple valleys.
        
        This is the "canonical valley crossing template".
        """
        successful_valleys = [v for v in valleys if v.is_successful]
        
        if not successful_valleys:
            return {}
        
        signatures = [ValleySignatureExtractor.extract_signature(v, df) 
                     for v in successful_valleys]
        
        # Average scalar values
        avg_signature = {
            'count': len(successful_valleys),
            'avg_duration': np.mean([s['duration'] for s in signatures]),
            'avg_DR_increase_rate': np.mean([s['DR_increase_rate'] for s in signatures]),
            'avg_coherence_drop_rate': np.mean([s['coherence_drop_rate'] for s in signatures]),
            'avg_peak_gamma': np.mean([s['peak_gamma'] for s in signatures]),
            'avg_reconstruction_quality': np.mean([s['reconstruction_quality'] for s in signatures]),
            'avg_recovery_fraction': np.mean([s['recovery_fraction'] for s in signatures]),
            'avg_valley_chatter': np.mean([s['valley_chatter'] for s in signatures]),
            'avg_coherence_overshoot': np.mean([s['coherence_overshoot'] for s in signatures]),
            'fraction_hemispheric': np.mean([s['is_hemispheric'] for s in signatures]),
        }

        
        return avg_signature


# =====================================================================
# §6: Main Analysis Pipeline
# =====================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Valley Crossing Detector - Find coherence phase transitions"
    )
    parser.add_argument(
        'csv_file',
        type=Path,
        help="Sand landscape CSV file (100K or 3.3M samples)"
    )
    parser.add_argument(
        '--output-dir',
        type=Path,
        default=Path('./valley_analysis'),
        help="Output directory"
    )
    parser.add_argument(
        '--max-samples',
        type=int,
        default=1000000,
        help="Max samples to load (for memory)"
    )
    parser.add_argument(
        '--DR-threshold',
        type=float,
        default=0.15,
        help="DR spike threshold for valley detection"
    )
    parser.add_argument(
        '--coherence-threshold',
        type=float,
        default=0.10,
        help="Coherence drop threshold"
    )
    
    args = parser.parse_args()
    
    # Create output directory
    args.output_dir.mkdir(parents=True, exist_ok=True)
    
    print("="*70)
    print("VALLEY CROSSING DETECTOR")
    print("Coherence Phase Transition Analysis")
    print("="*70)
    print(f"\nInput: {args.csv_file}")
    print(f"Output: {args.output_dir}")
    
    # Load data
    print("\nLoading sand landscape data...")
    if args.csv_file.stat().st_size > 100 * 1024 * 1024:  # >100MB
        # Chunked loading for large files
        chunks = []
        for chunk in pd.read_csv(args.csv_file, chunksize=100000):
            chunks.append(chunk)
            if len(pd.concat(chunks)) >= args.max_samples:
                break
        df = pd.concat(chunks, ignore_index=True)
    else:
        df = pd.read_csv(args.csv_file)
    
    if len(df) > args.max_samples:
        df = df.sample(n=args.max_samples, random_state=42).reset_index(drop=True)
    
    print(f"✓ Loaded {len(df):,} samples")
    
    # Ensure sample_id for temporal ordering
    if 'sample_id' not in df.columns:
        df['sample_id'] = np.arange(len(df))
    
    df = df.sort_values('sample_id').reset_index(drop=True)
    
    # Add PCA coordinates if not present (for hemisphere analysis)
    if 'PC1' not in df.columns:
        print("\nComputing PCA coordinates...")
        features = ['DR', 'S', 'Gamma', 'pi', 'operator_norm']
        X = df[features].values
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(X_scaled)
        df['PC1'] = X_pca[:, 0]
        df['PC2'] = X_pca[:, 1]
    
    # Detect valleys
    detector = ValleyCrossingDetector(
        DR_spike_threshold=args.DR_threshold,
        coherence_drop_threshold=args.coherence_threshold
    )
    
    valleys = detector.detect_valleys(df)
    
    if not valleys:
        print("\n⚠ No valleys detected. Try lowering thresholds.")
        return
    
    # Find symmetry break
    symmetry_break = detector.find_symmetry_break(df, valleys)
    
    # Generate visualizations
    print("\n" + "="*70)
    print("GENERATING VISUALIZATIONS")
    print("="*70)
    
    visualizer = ValleyVisualizer()
    
    visualizer.plot_valley_timeline(
        df, valleys, args.output_dir / 'valley_timeline.png'
    )
    
    visualizer.plot_valley_phase_space(
        df, valleys, args.output_dir / 'valley_phase_space.png'
    )
    
    if symmetry_break:
        visualizer.plot_symmetry_break_detail(
            df, symmetry_break, args.output_dir / 'symmetry_break_detail.png'
        )
    
    # Extract signatures
    print("\n" + "="*70)
    print("EXTRACTING VALLEY SIGNATURES")
    print("="*70)
    
    extractor = ValleySignatureExtractor()
    
    if symmetry_break:
        signature = extractor.extract_signature(symmetry_break, df)
        
        # Save signature
        import json
        with open(args.output_dir / 'symmetry_break_signature.json', 'w') as f:
            # Convert numpy arrays to lists for JSON
            json_signature = {k: (v.tolist() if isinstance(v, np.ndarray) else (v.item() if isinstance(v, np.generic) else v))
                                for k, v in signature.items()}
            json.dump(json_signature, f, indent=2)
        
        print(f"✓ Symmetry break signature saved")
    
    # Average signature
    avg_sig = extractor.compute_average_signature(valleys, df)
    if avg_sig:
        print(f"\nAverage Valley Signature (n={avg_sig['count']}):")
        for k, v in avg_sig.items():
            if k != 'count':
                print(f"  {k}: {v:.4f}")
    
    # Save annotated data
    df.to_csv(args.output_dir / 'landscape_with_valleys.csv', index=False)
    
    # Summary report
    print("\n" + "="*70)
    print("ANALYSIS COMPLETE")
    print("="*70)
    print(f"\nResults in: {args.output_dir}")
    print(f"\nDetected valleys: {len(valleys)}")
    print(f"  Successful: {sum(v.is_successful for v in valleys)}")
    print(f"  Failed: {sum(not v.is_successful for v in valleys)}")
    print(f"  Hemispheric splits: {sum(v.is_hemispheric_split for v in valleys)}")
    
    if symmetry_break:
        print(f"\n🌟 Symmetry break at sample {symmetry_break.entry_idx}")
        print(f"  This is your template for inducing valley crossings!")
    
    print("\nGenerated files:")
    for f in sorted(args.output_dir.glob('*')):
        print(f"  - {f.name}")


if __name__ == '__main__':
    main()

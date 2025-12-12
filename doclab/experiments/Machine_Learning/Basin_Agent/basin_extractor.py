#!/usr/bin/env python3
"""
Basin Extractor: Statistical Coherence Landscape Analysis
==========================================================

Extracts basin topology from EEG resonant manifolds.

This script:
1. Loads all manifold JSONs from a directory
2. Builds the population-level coherence landscape
3. Identifies strategy basins (sampler/locker/navigator)
4. Outputs statistical attractors for sand agent training

Theoretical Foundation:
- Each subject's manifold is a trajectory through coherence space
- The landscape V(f1, f2, f3, t, Γ) has multiple basins
- Different strategies = different geodesics through the same landscape
"""

import json
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from scipy.ndimage import gaussian_filter
from scipy.stats import entropy
import matplotlib.pyplot as plt
import seaborn as sns
from dataclasses import dataclass
from typing import List, Dict, Tuple
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# Data Structures
# ============================================================================

@dataclass
class ManifoldData:
    """Container for a single subject's manifold."""
    subject_id: str
    task: str
    triad_labels: List[str]
    time_points: np.ndarray
    manifold_low: np.ndarray  # Shape: (n_triads, n_timepoints)
    manifold_high: np.ndarray
    n_epochs_low: int
    n_epochs_high: int
    
    @classmethod
    def from_json(cls, json_path: Path):
        """Load from manifold JSON file."""
        with open(json_path, 'r') as f:
            data = json.load(f)

        # --- FIX STARTS HERE ---
        # 1. Default to data inside JSON
        subject_id = data.get('subject', 'unknown')
        
        # 2. If default is generic, force-read from filename
        # Looks for pattern: "sub-001_..." or just takes the first part
        fname_id = json_path.stem.split('_')[0]
        
        if subject_id in ['sub', 'manifold', 'unknown'] or fname_id.startswith('sub-'):
            subject_id = fname_id
        # --- FIX ENDS HERE ---
        
        return cls(
            subject_id=subject_id,
            task=data['task'],
            triad_labels=data['triad_labels'],
            time_points=np.array(data['time_points_sec']),
            manifold_low=np.array(data['manifold_low_load']),
            manifold_high=np.array(data['manifold_high_load']),
            n_epochs_low=data['n_epochs_low'],
            n_epochs_high=data['n_epochs_high']
        )
    
    def parse_triad(self, triad_label: str) -> Tuple[float, float, float]:
        """Parse triad label like '4.0-8.0-12.0' into (f1, f2, f3)."""
        parts = triad_label.split('-')
        return tuple(float(p) for p in parts)
    
    def get_frequency_array(self) -> np.ndarray:
        """Get array of (f1, f2, f3) for all triads. Shape: (n_triads, 3)."""
        return np.array([self.parse_triad(label) for label in self.triad_labels])


@dataclass
class BasinMetrics:
    """Metrics characterizing a coherence basin."""
    basin_id: int
    n_points: int
    centroid: np.ndarray  # In (f1, f2, f3, t) space
    coherence_mean: float
    coherence_std: float
    temporal_persistence: float  # How long coherence is sustained
    frequency_bandwidth: float   # Spread in frequency space
    transition_rate: float       # Rate of basin-hopping


# ============================================================================
# Core Analysis Functions
# ============================================================================

class CoherenceLandscape:
    """Statistical coherence landscape from population data."""
    
    def __init__(self):
        self.manifolds: List[ManifoldData] = []
        self.basins: Dict[str, BasinMetrics] = {}
        self.landscape_grid = None
        self.strategy_labels = None
        
    def load_manifolds(self, json_dir: Path, pattern: str = "*.json"):
        """Load all manifold JSONs from directory."""
        json_files = sorted(Path(json_dir).glob(pattern))
        
        if not json_files:
            raise ValueError(f"No JSON files found in {json_dir} matching {pattern}")
        
        print(f"Loading {len(json_files)} manifold files...")
        
        for json_path in json_files:
            try:
                manifold = ManifoldData.from_json(json_path)
                self.manifolds.append(manifold)
                print(f"  ✓ Loaded {manifold.subject_id} ({manifold.task})")
            except Exception as e:
                print(f"  ✗ Failed to load {json_path.name}: {e}")
        
        print(f"\nSuccessfully loaded {len(self.manifolds)} manifolds.\n")
        
    def extract_coherence_features(self, load_condition: str = 'high') -> pd.DataFrame:
        """
        Extract feature vectors for clustering.
        
        Each point in the manifold becomes a row with features:
        - f1, f2, f3: frequency triad
        - t: time point
        - TPCI: coherence value
        - subject_id: which subject
        - temporal_gradient: dTPCI/dt
        - frequency_gradient: how TPCI changes across nearby triads
        """
        rows = []
        
        for manifold in self.manifolds:
            freqs = manifold.get_frequency_array()
            times = manifold.time_points
            
            # Select load condition
            if load_condition == 'high':
                tpci_matrix = manifold.manifold_high
            else:
                tpci_matrix = manifold.manifold_low
            
            n_triads, n_times = tpci_matrix.shape
            
            for i_triad in range(n_triads):
                f1, f2, f3 = freqs[i_triad]
                
                for i_time in range(n_times):
                    tpci = tpci_matrix[i_triad, i_time]
                    t = times[i_time]
                    
                    # Compute temporal gradient
                    if i_time > 0:
                        dt = times[i_time] - times[i_time - 1]
                        dtpci_dt = (tpci - tpci_matrix[i_triad, i_time - 1]) / dt
                    else:
                        dtpci_dt = 0.0
                    
                    # Compute frequency gradient (average over nearby triads)
                    freq_neighbors = []
                    for j in range(max(0, i_triad - 2), min(n_triads, i_triad + 3)):
                        if j != i_triad:
                            freq_neighbors.append(tpci_matrix[j, i_time])
                    
                    if freq_neighbors:
                        dtpci_df = tpci - np.mean(freq_neighbors)
                    else:
                        dtpci_df = 0.0
                    
                    rows.append({
                        'subject_id': manifold.subject_id,
                        'f1': f1,
                        'f2': f2,
                        'f3': f3,
                        't': t,
                        'tpci': tpci,
                        'dtpci_dt': dtpci_dt,
                        'dtpci_df': dtpci_df,
                        'triad_idx': i_triad,
                        'time_idx': i_time
                    })
        
        df = pd.DataFrame(rows)
        print(f"Extracted {len(df)} coherence points from {len(self.manifolds)} subjects.")
        return df
    
    def identify_basins(self, df: pd.DataFrame, eps: float = 0.3, min_samples: int = 50):
        """
        Cluster coherence points to identify basins.
        
        Uses DBSCAN in normalized (f1, f2, f3, t, tpci, dtpci_dt) space.
        """
        print("\n" + "="*70)
        print("BASIN IDENTIFICATION")
        print("="*70)
        
        # Select features for clustering
        feature_cols = ['f1', 'f2', 'f3', 't', 'tpci', 'dtpci_dt', 'dtpci_df']
        X = df[feature_cols].values
        
        # Normalize
        scaler = StandardScaler()
        X_norm = scaler.fit_transform(X)
        
        # Cluster
        print(f"\nRunning DBSCAN (eps={eps}, min_samples={min_samples})...")
        clusterer = DBSCAN(eps=eps, min_samples=min_samples, n_jobs=-1)
        labels = clusterer.fit_predict(X_norm)
        
        df['basin_id'] = labels
        
        n_basins = len(set(labels)) - (1 if -1 in labels else 0)
        n_noise = np.sum(labels == -1)
        
        print(f"  ✓ Found {n_basins} basins")
        print(f"  ✓ Noise points: {n_noise} ({100*n_noise/len(df):.1f}%)")
        
        # Diagnostic: if no basins found, suggest parameters
        if n_basins == 0:
            print("\n  ⚠ WARNING: No basins found! All points classified as noise.")
            print("  This usually means:")
            print("    1. Data is too heterogeneous (subjects have very different patterns)")
            print("    2. eps parameter is too small (points too far apart to cluster)")
            print("    3. min_samples is too large (not enough nearby points)")
            print("\n  Suggestions:")
            
            # Compute nearest neighbor distances to suggest eps
            from sklearn.neighbors import NearestNeighbors
            nn = NearestNeighbors(n_neighbors=min_samples)
            nn.fit(X_norm)
            distances, _ = nn.kneighbors(X_norm)
            
            # 90th percentile of k-nearest neighbor distance
            suggested_eps = np.percentile(distances[:, -1], 90)
            
            print(f"    - Try increasing eps to {suggested_eps:.2f} (90th percentile of {min_samples}-nearest distances)")
            print(f"    - Or reduce min_samples to {min_samples // 2}")
            print(f"    - Or analyze subjects individually first")
            print("\n  Continuing with landscape analysis anyway...")
        
        # Compute basin metrics
        self._compute_basin_metrics(df)
        
        return df
    
    def _compute_basin_metrics(self, df: pd.DataFrame):
        """Compute metrics for each basin."""
        print("\nComputing basin metrics...")
        
        basins = {}
        
        for basin_id in sorted(df['basin_id'].unique()):
            if basin_id == -1:  # Skip noise
                continue
            
            basin_df = df[df['basin_id'] == basin_id]
            
            # Centroid in (f1, f2, f3, t) space
            centroid = basin_df[['f1', 'f2', 'f3', 't']].mean().values
            
            # Coherence stats
            coherence_mean = basin_df['tpci'].mean()
            coherence_std = basin_df['tpci'].std()
            
            # Temporal persistence: how long does coherence stay in this basin?
            time_span = basin_df['t'].max() - basin_df['t'].min()
            
            # Frequency bandwidth: spread in frequency space
            freq_bandwidth = np.sqrt(
                basin_df['f1'].std()**2 + 
                basin_df['f2'].std()**2 + 
                basin_df['f3'].std()**2
            )
            
            # Transition rate: how often does dtpci/dt spike?
            transition_rate = (np.abs(basin_df['dtpci_dt']) > basin_df['dtpci_dt'].std()).mean()
            
            basins[basin_id] = BasinMetrics(
                basin_id=basin_id,
                n_points=len(basin_df),
                centroid=centroid,
                coherence_mean=coherence_mean,
                coherence_std=coherence_std,
                temporal_persistence=time_span,
                frequency_bandwidth=freq_bandwidth,
                transition_rate=transition_rate
            )
            
            print(f"\n  Basin {basin_id}:")
            print(f"    Points: {basins[basin_id].n_points}")
            print(f"    Coherence: {coherence_mean:.3f} ± {coherence_std:.3f}")
            print(f"    Temporal span: {time_span:.2f}s")
            print(f"    Freq bandwidth: {freq_bandwidth:.2f} Hz")
            print(f"    Transition rate: {transition_rate:.3f}")
        
        self.basins = basins
    
    def classify_strategies(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Classify basins into strategy types.
        
        Strategy signatures:
        - Sampler: Low temporal persistence, high transition rate
        - Locker: High temporal persistence, low transition rate, high coherence
        - Navigator: Medium persistence, smooth gradients (low dtpci_df variance)
        """
        print("\n" + "="*70)
        print("STRATEGY CLASSIFICATION")
        print("="*70)
        
        if len(self.basins) == 0:
            print("\n  ⚠ No basins to classify (all points are noise)")
            df['strategy'] = 'noise'
            self.strategy_labels = {}
            return df
        
        strategy_map = {}
        
        for basin_id, metrics in self.basins.items():
            # Decision tree for strategy type
            if metrics.temporal_persistence < 0.3 and metrics.transition_rate > 0.3:
                strategy = 'sampler'
            elif metrics.temporal_persistence > 0.5 and metrics.coherence_mean > 0.15:
                strategy = 'locker'
            elif metrics.frequency_bandwidth > 3.0:
                strategy = 'navigator'
            else:
                strategy = 'mixed'
            
            strategy_map[basin_id] = strategy
            
            print(f"\n  Basin {basin_id} → {strategy.upper()}")
            print(f"    Temporal persistence: {metrics.temporal_persistence:.2f}s")
            print(f"    Transition rate: {metrics.transition_rate:.3f}")
            print(f"    Coherence: {metrics.coherence_mean:.3f}")
        
        df['strategy'] = df['basin_id'].map(strategy_map)
        self.strategy_labels = strategy_map
        
        return df
    
    def build_population_landscape(self, df: pd.DataFrame, grid_resolution: int = 50):
        """
        Build the population-average coherence landscape V(f1, f2, t).
        
        Averages TPCI across all subjects for each (f1, f2, t) point.
        We'll marginalize over f3 for visualization.
        """
        print("\n" + "="*70)
        print("BUILDING POPULATION LANDSCAPE")
        print("="*70)
        
        # Define grid
        f1_range = np.linspace(df['f1'].min(), df['f1'].max(), grid_resolution)
        f2_range = np.linspace(df['f2'].min(), df['f2'].max(), grid_resolution)
        t_range = np.linspace(df['t'].min(), df['t'].max(), grid_resolution)
        
        # Initialize grid
        landscape_grid = np.zeros((grid_resolution, grid_resolution, grid_resolution))
        counts = np.zeros_like(landscape_grid)
        
        print(f"\nGridding {len(df)} points onto {grid_resolution}³ grid...")
        
        # Bin data points
        f1_bins = np.digitize(df['f1'], f1_range) - 1
        f2_bins = np.digitize(df['f2'], f2_range) - 1
        t_bins = np.digitize(df['t'], t_range) - 1
        
        # Accumulate
        for i in range(len(df)):
            i1, i2, it = f1_bins[i], f2_bins[i], t_bins[i]
            
            # Bounds check
            if 0 <= i1 < grid_resolution and 0 <= i2 < grid_resolution and 0 <= it < grid_resolution:
                landscape_grid[i1, i2, it] += df.iloc[i]['tpci']
                counts[i1, i2, it] += 1
        
        # Average
        mask = counts > 0
        landscape_grid[mask] /= counts[mask]
        
        # Smooth
        landscape_grid = gaussian_filter(landscape_grid, sigma=1.0)
        
        self.landscape_grid = {
            'V': landscape_grid,
            'f1_range': f1_range,
            'f2_range': f2_range,
            't_range': t_range
        }
        
        print(f"  ✓ Landscape grid shape: {landscape_grid.shape}")
        print(f"  ✓ Mean coherence: {landscape_grid[mask].mean():.3f}")
        print(f"  ✓ Coherence range: [{landscape_grid[mask].min():.3f}, {landscape_grid[mask].max():.3f}]")
        
        return landscape_grid
    
    def export_basin_structure(self, output_path: Path, df: pd.DataFrame):
        """Export basin structure for sand agent training."""
        print("\n" + "="*70)
        print("EXPORTING BASIN STRUCTURE")
        print("="*70)
        
        # Summary stats
        summary = {
            'n_subjects': len(self.manifolds),
            'n_basins': len(self.basins),
            'basins': {}
        }
        
        for basin_id, metrics in self.basins.items():
            summary['basins'][str(basin_id)] = {
                'strategy': self.strategy_labels.get(basin_id, 'unknown'),
                'n_points': metrics.n_points,
                'centroid': metrics.centroid.tolist(),
                'coherence_mean': float(metrics.coherence_mean),
                'coherence_std': float(metrics.coherence_std),
                'temporal_persistence': float(metrics.temporal_persistence),
                'frequency_bandwidth': float(metrics.frequency_bandwidth),
                'transition_rate': float(metrics.transition_rate)
            }
        
        # Subject-basin mapping (only if we have basins)
        if len(self.basins) > 0:
            subject_basins = df.groupby('subject_id')['basin_id'] \
                                .value_counts() \
                                .unstack(fill_value=0) \
                                .to_dict('index')
            
            summary['subject_basin_preferences'] = {
                str(k): {str(kk): int(vv) for kk, vv in v.items()} 
                for k, v in subject_basins.items()
            }
        else:
            summary['subject_basin_preferences'] = {}
        
        # Save
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n✓ Basin structure saved to: {output_path}")
        
        return summary


# ============================================================================
# Visualization
# ============================================================================

def plot_basin_summary(landscape: CoherenceLandscape, df: pd.DataFrame, output_dir: Path):
    """Generate comprehensive basin visualization."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("\n" + "="*70)
    print("GENERATING VISUALIZATIONS")
    print("="*70)
    
    # 1. Basin distribution in PCA space
    print("\n1. Basin distribution (PCA projection)...")
    
    feature_cols = ['f1', 'f2', 'f3', 't', 'tpci']
    X = df[feature_cols].values
    
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(StandardScaler().fit_transform(X))
    
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    
    # Plot each basin
    for basin_id in sorted(df['basin_id'].unique()):
        if basin_id == -1:
            continue
        
        mask = df['basin_id'] == basin_id
        strategy = landscape.strategy_labels.get(basin_id, 'unknown')
        
        ax.scatter(
            X_pca[mask, 0], 
            X_pca[mask, 1], 
            alpha=0.3, 
            s=10,
            label=f"Basin {basin_id} ({strategy})"
        )
    
    ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.1%} var)")
    ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.1%} var)")
    ax.set_title("Basin Distribution in PCA Space")
    ax.legend()
    ax.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_dir / "basin_pca.png", dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"  ✓ Saved: {output_dir / 'basin_pca.png'}")
    
    # 2. Strategy composition by subject
    print("\n2. Subject-strategy composition...")
    
    subject_strategy = df.groupby(['subject_id', 'strategy']).size().unstack(fill_value=0)
    subject_strategy = subject_strategy.div(subject_strategy.sum(axis=1), axis=0)
    
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    subject_strategy.plot(kind='bar', stacked=True, ax=ax, colormap='tab10')
    ax.set_xlabel("Subject")
    ax.set_ylabel("Proportion of Time")
    ax.set_title("Strategy Usage by Subject")
    ax.legend(title="Strategy", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(output_dir / "subject_strategies.png", dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"  ✓ Saved: {output_dir / 'subject_strategies.png'}")
    
    # 3. Coherence potential landscape (2D slice at median time)
    if landscape.landscape_grid is not None:
        print("\n3. Coherence potential landscape...")
        
        grid = landscape.landscape_grid
        V = grid['V']
        f1_range = grid['f1_range']
        f2_range = grid['f2_range']
        t_range = grid['t_range']
        
        # Slice at median time
        t_median_idx = len(t_range) // 2
        V_slice = V[:, :, t_median_idx]
        
        fig, ax = plt.subplots(1, 1, figsize=(10, 8))
        
        im = ax.contourf(
            f2_range, f1_range, V_slice,
            levels=20, cmap='viridis'
        )
        
        # Overlay basin centroids
        for basin_id, metrics in landscape.basins.items():
            f1_c, f2_c, _, _ = metrics.centroid
            strategy = landscape.strategy_labels.get(basin_id, 'unknown')
            
            ax.plot(f2_c, f1_c, 'r*', markersize=15, 
                   label=f"Basin {basin_id} ({strategy})")
        
        ax.set_xlabel("f2 (Hz)")
        ax.set_ylabel("f1 (Hz)")
        ax.set_title(f"Coherence Landscape at t={t_range[t_median_idx]:.2f}s")
        
        plt.colorbar(im, ax=ax, label="Mean TPCI")
        ax.legend(bbox_to_anchor=(1.3, 1), loc='upper left')
        plt.tight_layout()
        plt.savefig(output_dir / "landscape_2d.png", dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"  ✓ Saved: {output_dir / 'landscape_2d.png'}")
    
    # 4. Basin metrics comparison
    print("\n4. Basin metrics comparison...")
    
    metrics_df = pd.DataFrame([
        {
            'basin_id': basin_id,
            'strategy': landscape.strategy_labels.get(basin_id, 'unknown'),
            'coherence': metrics.coherence_mean,
            'temporal_persistence': metrics.temporal_persistence,
            'frequency_bandwidth': metrics.frequency_bandwidth,
            'transition_rate': metrics.transition_rate
        }
        for basin_id, metrics in landscape.basins.items()
    ])
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Coherence by strategy
    sns.boxplot(data=metrics_df, x='strategy', y='coherence', ax=axes[0, 0])
    axes[0, 0].set_title("Coherence by Strategy")
    axes[0, 0].set_ylabel("Mean TPCI")
    
    # Temporal persistence by strategy
    sns.boxplot(data=metrics_df, x='strategy', y='temporal_persistence', ax=axes[0, 1])
    axes[0, 1].set_title("Temporal Persistence by Strategy")
    axes[0, 1].set_ylabel("Time Span (s)")
    
    # Frequency bandwidth by strategy
    sns.boxplot(data=metrics_df, x='strategy', y='frequency_bandwidth', ax=axes[1, 0])
    axes[1, 0].set_title("Frequency Bandwidth by Strategy")
    axes[1, 0].set_ylabel("Bandwidth (Hz)")
    
    # Transition rate by strategy
    sns.boxplot(data=metrics_df, x='strategy', y='transition_rate', ax=axes[1, 1])
    axes[1, 1].set_title("Transition Rate by Strategy")
    axes[1, 1].set_ylabel("Transition Rate")
    
    plt.tight_layout()
    plt.savefig(output_dir / "basin_metrics.png", dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"  ✓ Saved: {output_dir / 'basin_metrics.png'}")
    
    print("\n✓ All visualizations complete!")


# ============================================================================
# Main Pipeline
# ============================================================================

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Extract basin topology from EEG resonant manifolds"
    )
    parser.add_argument(
        'manifold_dir',
        type=Path,
        help="Directory containing manifold JSON files"
    )
    parser.add_argument(
        '--output-dir',
        type=Path,
        default=Path('./basin_analysis'),
        help="Output directory for results"
    )
    parser.add_argument(
        '--load-condition',
        choices=['low', 'high'],
        default='high',
        help="Which load condition to analyze"
    )
    parser.add_argument(
        '--eps',
        type=float,
        default=0.3,
        help="DBSCAN eps parameter (basin separation)"
    )
    parser.add_argument(
        '--min-samples',
        type=int,
        default=50,
        help="DBSCAN min_samples parameter"
    )
    
    args = parser.parse_args()
    
    # Create output directory
    args.output_dir.mkdir(parents=True, exist_ok=True)
    
    print("\n" + "="*70)
    print("COHERENCE BASIN EXTRACTOR")
    print("="*70)
    print(f"\nManifold directory: {args.manifold_dir}")
    print(f"Output directory: {args.output_dir}")
    print(f"Load condition: {args.load_condition}")
    print(f"DBSCAN parameters: eps={args.eps}, min_samples={args.min_samples}")
    
    # Build landscape
    landscape = CoherenceLandscape()
    landscape.load_manifolds(args.manifold_dir)
    
    # Extract features
    df = landscape.extract_coherence_features(load_condition=args.load_condition)
    
    # Identify basins
    df = landscape.identify_basins(df, eps=args.eps, min_samples=args.min_samples)
    
    # Classify strategies
    df = landscape.classify_strategies(df)
    
    # Build population landscape
    landscape.build_population_landscape(df)
    
    # Export basin structure
    basin_json_path = args.output_dir / 'basin_structure.json'
    landscape.export_basin_structure(basin_json_path, df)
    
    # Visualize
    plot_basin_summary(landscape, df, args.output_dir)
    
    # Save full feature dataframe
    df_path = args.output_dir / 'coherence_features.csv'
    df.to_csv(df_path, index=False)
    print(f"\n✓ Feature dataframe saved to: {df_path}")
    
    print("\n" + "="*70)
    print("ANALYSIS COMPLETE")
    print("="*70)
    print(f"\nResults saved to: {args.output_dir}")
    print("\nGenerated files:")
    print(f"  - basin_structure.json (for sand agent)")
    print(f"  - coherence_features.csv (full dataset)")
    print(f"  - basin_pca.png")
    print(f"  - subject_strategies.png")
    print(f"  - landscape_2d.png")
    print(f"  - basin_metrics.png")
    

if __name__ == '__main__':
    main()
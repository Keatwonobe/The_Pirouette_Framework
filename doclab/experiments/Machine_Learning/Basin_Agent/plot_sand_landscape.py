#!/usr/bin/env python3
"""
Sand Landscape Plotter - Comprehensive Visualization Suite
===========================================================

Creates beautiful plots from sand agent landscape data.
Handles massive datasets efficiently using chunked reading and downsampling.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from scipy.stats import gaussian_kde
from matplotlib.colors import LinearSegmentedColormap
import argparse

# Set style
sns.set_style("darkgrid")
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = '#f8f9fa'

# ============================================================================
# Data Loading (with smart downsampling)
# ============================================================================

def load_landscape(csv_path: Path, max_samples: int = 500000):
    """
    Load landscape data with smart downsampling.
    
    If dataset is huge, randomly sample to keep plots manageable.
    """
    print(f"\nLoading data from {csv_path.name}...")
    
    # Check file size
    import os
    file_size_mb = os.path.getsize(csv_path) / (1024 * 1024)
    print(f"  File size: {file_size_mb:.1f} MB")
    
    # Load (possibly in chunks)
    if file_size_mb > 100:  # If > 100MB, use chunked loading
        print(f"  Large file detected - using chunked loading...")
        chunks = []
        for chunk in pd.read_csv(csv_path, chunksize=100000):
            chunks.append(chunk)
            if len(pd.concat(chunks)) >= max_samples:
                break
        df = pd.concat(chunks, ignore_index=True)
    else:
        df = pd.read_csv(csv_path)
    
    # Downsample if needed
    if len(df) > max_samples:
        print(f"  Downsampling from {len(df):,} to {max_samples:,} samples...")
        df = df.sample(n=max_samples, random_state=42)
    
    print(f"  ✓ Loaded {len(df):,} samples")
    print(f"  Strategies: {df['strategy'].unique().tolist()}")
    print(f"  Basins: {sorted(df['basin_id'].unique())}")
    
    return df


# ============================================================================
# Plot 1: Strategy Phase Space (DR vs S vs Γ)
# ============================================================================

def plot_strategy_phase_space(df: pd.DataFrame, output_dir: Path):
    """
    3D scatter of DR vs Surprise vs Gamma, colored by strategy.
    
    This shows the full coherence landscape in (DR, S, Γ) space.
    """
    print("\n1. Plotting strategy phase space...")
    
    from mpl_toolkits.mplot3d import Axes3D
    
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot each strategy
    strategies = df['strategy'].unique()
    colors = plt.cm.tab10(np.linspace(0, 1, len(strategies)))
    
    for strategy, color in zip(strategies, colors):
        mask = df['strategy'] == strategy
        data = df[mask].sample(min(10000, mask.sum()))  # Max 10k points per strategy
        
        ax.scatter(
            data['S'], 
            data['DR'], 
            data['Gamma'],
            c=[color],
            label=strategy,
            alpha=0.3,
            s=1
        )
    
    ax.set_xlabel('Surprise (S)', fontsize=12)
    ax.set_ylabel('Dark Residue (DR)', fontsize=12)
    ax.set_zlabel('Temporal Pressure (Γ)', fontsize=12)
    ax.set_title('Strategy Phase Space: DR × S × Γ', fontsize=14, fontweight='bold')
    ax.legend(loc='upper left')
    
    plt.tight_layout()
    output_path = output_dir / 'phase_space_3d.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"  ✓ Saved: {output_path.name}")


# ============================================================================
# Plot 2: Operator Manifold (P-S-C Triadic Structure)
# ============================================================================

def plot_operator_manifold(df: pd.DataFrame, output_dir: Path):
    """
    Visualize the triadic operator structure (O_P, O_S, O_C).
    
    Shows how Precision, Surprise, and Coherence components interact.
    """
    print("\n2. Plotting operator manifold...")
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    
    # Downsample for scatter plots
    df_plot = df.sample(min(50000, len(df)))
    
    strategies = df['strategy'].unique()
    
    # Plot 1: O_P vs O_S
    for strategy in strategies:
        mask = df_plot['strategy'] == strategy
        axes[0, 0].scatter(
            df_plot[mask]['O_P'],
            df_plot[mask]['O_S'],
            alpha=0.3,
            s=2,
            label=strategy
        )
    axes[0, 0].set_xlabel('Precision Component (O_P)', fontsize=10)
    axes[0, 0].set_ylabel('Surprise Component (O_S)', fontsize=10)
    axes[0, 0].set_title('P-S Plane', fontweight='bold')
    axes[0, 0].legend()
    axes[0, 0].grid(alpha=0.3)
    axes[0, 0].axhline(0, color='k', linewidth=0.5, alpha=0.5)
    axes[0, 0].axvline(0, color='k', linewidth=0.5, alpha=0.5)
    
    # Plot 2: O_P vs O_C
    for strategy in strategies:
        mask = df_plot['strategy'] == strategy
        axes[0, 1].scatter(
            df_plot[mask]['O_P'],
            df_plot[mask]['O_C'],
            alpha=0.3,
            s=2,
            label=strategy
        )
    axes[0, 1].set_xlabel('Precision Component (O_P)', fontsize=10)
    axes[0, 1].set_ylabel('Coherence Component (O_C)', fontsize=10)
    axes[0, 1].set_title('P-C Plane', fontweight='bold')
    axes[0, 1].legend()
    axes[0, 1].grid(alpha=0.3)
    axes[0, 1].axhline(0, color='k', linewidth=0.5, alpha=0.5)
    axes[0, 1].axvline(0, color='k', linewidth=0.5, alpha=0.5)
    
    # Plot 3: O_S vs O_C
    for strategy in strategies:
        mask = df_plot['strategy'] == strategy
        axes[1, 0].scatter(
            df_plot[mask]['O_S'],
            df_plot[mask]['O_C'],
            alpha=0.3,
            s=2,
            label=strategy
        )
    axes[1, 0].set_xlabel('Surprise Component (O_S)', fontsize=10)
    axes[1, 0].set_ylabel('Coherence Component (O_C)', fontsize=10)
    axes[1, 0].set_title('S-C Plane', fontweight='bold')
    axes[1, 0].legend()
    axes[1, 0].grid(alpha=0.3)
    axes[1, 0].axhline(0, color='k', linewidth=0.5, alpha=0.5)
    axes[1, 0].axvline(0, color='k', linewidth=0.5, alpha=0.5)
    
    # Plot 4: Operator norm distribution
    for strategy in strategies:
        mask = df['strategy'] == strategy
        axes[1, 1].hist(
            df[mask]['operator_norm'],
            bins=50,
            alpha=0.5,
            label=strategy,
            density=True
        )
    axes[1, 1].set_xlabel('Operator Norm ||O||', fontsize=10)
    axes[1, 1].set_ylabel('Density', fontsize=10)
    axes[1, 1].set_title('Operator Magnitude Distribution', fontweight='bold')
    axes[1, 1].legend()
    axes[1, 1].grid(alpha=0.3)
    
    plt.suptitle('Triadic Operator Manifold (P-S-C)', fontsize=16, fontweight='bold', y=1.00)
    plt.tight_layout()
    
    output_path = output_dir / 'operator_manifold.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"  ✓ Saved: {output_path.name}")


# ============================================================================
# Plot 3: Precision Landscape (Π vs DR vs Γ)
# ============================================================================

def plot_precision_landscape(df: pd.DataFrame, output_dir: Path):
    """
    Heatmap of precision as function of (DR, Γ).
    
    Shows the coherence potential V(DR, Γ) through precision modulation.
    """
    print("\n3. Plotting precision landscape...")
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # Create 2D histogram/heatmap
    from scipy.stats import binned_statistic_2d
    
    # Bin the data
    DR_bins = np.linspace(0, 1, 50)
    Gamma_bins = np.linspace(0, 2, 50)
    
    # Average precision in each bin
    precision_grid, DR_edges, Gamma_edges, _ = binned_statistic_2d(
        df['DR'],
        df['Gamma'],
        df['pi'],
        statistic='mean',
        bins=[DR_bins, Gamma_bins]
    )
    
    # Plot 1: Precision heatmap
    im1 = axes[0].imshow(
        precision_grid.T,
        origin='lower',
        aspect='auto',
        extent=[0, 1, 0, 2],
        cmap='viridis',
        interpolation='bilinear'
    )
    axes[0].set_xlabel('Dark Residue (DR)', fontsize=12)
    axes[0].set_ylabel('Temporal Pressure (Γ)', fontsize=12)
    axes[0].set_title('Precision Landscape: Π(DR, Γ)', fontsize=14, fontweight='bold')
    plt.colorbar(im1, ax=axes[0], label='Precision (Π)')
    
    # Overlay basin centroids if we have basin info
    if 'basin_id' in df.columns:
        basin_centers = df.groupby('basin_id').agg({
            'DR': 'mean',
            'Gamma': 'mean',
            'strategy': 'first'
        })
        
        for basin_id, row in basin_centers.iterrows():
            axes[0].plot(
                row['DR'],
                row['Gamma'],
                'r*',
                markersize=15,
                markeredgecolor='white',
                markeredgewidth=1,
                label=f"Basin {basin_id} ({row['strategy']})"
            )
    
    # Plot 2: Contour plot with strategy overlays
    CS = axes[1].contour(
        DR_edges[:-1],
        Gamma_edges[:-1],
        precision_grid.T,
        levels=10,
        cmap='viridis',
        linewidths=2
    )
    axes[1].clabel(CS, inline=True, fontsize=8)
    
    # Overlay strategy samples
    for strategy in df['strategy'].unique():
        mask = df['strategy'] == strategy
        sample = df[mask].sample(min(5000, mask.sum()))
        axes[1].scatter(
            sample['DR'],
            sample['Gamma'],
            alpha=0.1,
            s=1,
            label=strategy
        )
    
    axes[1].set_xlabel('Dark Residue (DR)', fontsize=12)
    axes[1].set_ylabel('Temporal Pressure (Γ)', fontsize=12)
    axes[1].set_title('Precision Contours + Strategy Samples', fontsize=14, fontweight='bold')
    axes[1].legend()
    axes[1].grid(alpha=0.3)
    
    plt.tight_layout()
    output_path = output_dir / 'precision_landscape.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"  ✓ Saved: {output_path.name}")


# ============================================================================
# Plot 4: Basin Topology (KDE in reduced space)
# ============================================================================

def plot_basin_topology(df: pd.DataFrame, output_dir: Path):
    """
    KDE density plot showing basin structure.
    
    Uses PCA to reduce to 2D, then shows density contours.
    """
    print("\n4. Plotting basin topology...")
    
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler
    
    # Select features
    features = ['DR', 'S', 'Gamma', 'pi', 'operator_norm']
    X = df[features].values
    
    # Normalize and reduce
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)
    
    # Create figure
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # Plot 1: Scatter by strategy
    for strategy in df['strategy'].unique():
        mask = df['strategy'] == strategy
        sample_idx = np.random.choice(np.where(mask)[0], size=min(10000, mask.sum()), replace=False)
        axes[0].scatter(
            X_pca[sample_idx, 0],
            X_pca[sample_idx, 1],
            alpha=0.3,
            s=3,
            label=strategy
        )
    
    axes[0].set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%} var)', fontsize=12)
    axes[0].set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%} var)', fontsize=12)
    axes[0].set_title('Basin Topology (PCA Space)', fontsize=14, fontweight='bold')
    axes[0].legend()
    axes[0].grid(alpha=0.3)
    
    # Plot 2: KDE density contours
    from scipy.stats import gaussian_kde
    
    # Downsample for KDE
    sample_size = min(20000, len(X_pca))
    sample_idx = np.random.choice(len(X_pca), size=sample_size, replace=False)
    X_sample = X_pca[sample_idx]
    
    # Compute KDE
    kde = gaussian_kde(X_sample.T)
    
    # Create grid
    x_min, x_max = X_pca[:, 0].min(), X_pca[:, 0].max()
    y_min, y_max = X_pca[:, 1].min(), X_pca[:, 1].max()
    
    xx, yy = np.meshgrid(
        np.linspace(x_min, x_max, 100),
        np.linspace(y_min, y_max, 100)
    )
    
    positions = np.vstack([xx.ravel(), yy.ravel()])
    density = kde(positions).reshape(xx.shape)
    
    # Plot density
    im = axes[1].contourf(xx, yy, density, levels=15, cmap='viridis', alpha=0.8)
    axes[1].contour(xx, yy, density, levels=10, colors='white', linewidths=0.5, alpha=0.5)
    
    # Overlay basin centroids
    if 'basin_id' in df.columns:
        for basin_id in df['basin_id'].unique():
            if basin_id == -1:  # Skip noise
                continue
            mask = df['basin_id'] == basin_id
            centroid_features = df[mask][features].mean().values
            centroid_scaled = scaler.transform([centroid_features])
            centroid_pca = pca.transform(centroid_scaled)
            
            strategy = df[mask]['strategy'].iloc[0]
            axes[1].plot(
                centroid_pca[0, 0],
                centroid_pca[0, 1],
                'r*',
                markersize=20,
                markeredgecolor='white',
                markeredgewidth=2,
                label=f"Basin {basin_id} ({strategy})"
            )
    
    axes[1].set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%} var)', fontsize=12)
    axes[1].set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%} var)', fontsize=12)
    axes[1].set_title('Coherence Density (KDE)', fontsize=14, fontweight='bold')
    plt.colorbar(im, ax=axes[1], label='Density')
    axes[1].legend(bbox_to_anchor=(1.3, 1), loc='upper left')
    
    plt.tight_layout()
    output_path = output_dir / 'basin_topology.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"  ✓ Saved: {output_path.name}")


# ============================================================================
# Plot 5: Strategy Signatures (Radar/Spider Chart)
# ============================================================================

def plot_strategy_signatures(df: pd.DataFrame, output_dir: Path):
    """
    Radar chart showing characteristic profile of each strategy.
    """
    print("\n5. Plotting strategy signatures...")
    
    # Compute strategy means
    strategy_means = df.groupby('strategy').agg({
        'DR': 'mean',
        'S': 'mean',
        'Gamma': 'mean',
        'pi': 'mean',
        'operator_norm': 'mean',
        'g': 'mean'
    })
    
    # Normalize to [0, 1]
    from sklearn.preprocessing import MinMaxScaler
    scaler = MinMaxScaler()
    strategy_means_norm = pd.DataFrame(
        scaler.fit_transform(strategy_means),
        index=strategy_means.index,
        columns=strategy_means.columns
    )
    
    # Radar chart
    categories = ['DR', 'Surprise', 'Pressure (Γ)', 'Precision (Π)', 'Operator', 'Gate']
    N = len(categories)
    
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]  # Complete the circle
    
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
    
    for strategy in strategy_means_norm.index:
        values = strategy_means_norm.loc[strategy].tolist()
        values += values[:1]  # Complete the circle
        
        ax.plot(angles, values, 'o-', linewidth=2, label=strategy)
        ax.fill(angles, values, alpha=0.15)
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, size=12)
    ax.set_ylim(0, 1)
    ax.set_title('Strategy Signatures\n(Normalized Metrics)', 
                 size=16, fontweight='bold', pad=20)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
    ax.grid(True)
    
    plt.tight_layout()
    output_path = output_dir / 'strategy_signatures.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"  ✓ Saved: {output_path.name}")


# ============================================================================
# Plot 6: The Grand Overview (Dashboard)
# ============================================================================

def plot_grand_dashboard(df: pd.DataFrame, output_dir: Path):
    """
    Single comprehensive dashboard with all key metrics.
    """
    print("\n6. Creating grand dashboard...")
    
    fig = plt.figure(figsize=(20, 12))
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    # 1. DR distribution
    ax1 = fig.add_subplot(gs[0, 0])
    for strategy in df['strategy'].unique():
        mask = df['strategy'] == strategy
        ax1.hist(df[mask]['DR'], bins=50, alpha=0.5, label=strategy, density=True)
    ax1.set_xlabel('Dark Residue')
    ax1.set_ylabel('Density')
    ax1.set_title('DR Distribution', fontweight='bold')
    ax1.legend()
    ax1.grid(alpha=0.3)
    
    # 2. Surprise distribution
    ax2 = fig.add_subplot(gs[0, 1])
    for strategy in df['strategy'].unique():
        mask = df['strategy'] == strategy
        ax2.hist(df[mask]['S'], bins=50, alpha=0.5, label=strategy, density=True)
    ax2.set_xlabel('Surprise')
    ax2.set_ylabel('Density')
    ax2.set_title('Surprise Distribution', fontweight='bold')
    ax2.legend()
    ax2.grid(alpha=0.3)
    
    # 3. Operator norm distribution
    ax3 = fig.add_subplot(gs[0, 2])
    for strategy in df['strategy'].unique():
        mask = df['strategy'] == strategy
        ax3.hist(df[mask]['operator_norm'], bins=50, alpha=0.5, label=strategy, density=True)
    ax3.set_xlabel('Operator Norm')
    ax3.set_ylabel('Density')
    ax3.set_title('Operator Magnitude', fontweight='bold')
    ax3.legend()
    ax3.grid(alpha=0.3)
    
    # 4. DR vs S scatter
    ax4 = fig.add_subplot(gs[1, 0])
    for strategy in df['strategy'].unique():
        mask = df['strategy'] == strategy
        sample = df[mask].sample(min(5000, mask.sum()))
        ax4.scatter(sample['DR'], sample['S'], alpha=0.3, s=2, label=strategy)
    ax4.set_xlabel('Dark Residue')
    ax4.set_ylabel('Surprise')
    ax4.set_title('DR vs Surprise', fontweight='bold')
    ax4.legend()
    ax4.grid(alpha=0.3)
    
    # 5. Precision vs Gamma
    ax5 = fig.add_subplot(gs[1, 1])
    for strategy in df['strategy'].unique():
        mask = df['strategy'] == strategy
        sample = df[mask].sample(min(5000, mask.sum()))
        ax5.scatter(sample['Gamma'], sample['pi'], alpha=0.3, s=2, label=strategy)
    ax5.set_xlabel('Temporal Pressure (Γ)')
    ax5.set_ylabel('Precision (Π)')
    ax5.set_title('Precision vs Load', fontweight='bold')
    ax5.legend()
    ax5.grid(alpha=0.3)
    
    # 6. O_P vs O_S
    ax6 = fig.add_subplot(gs[1, 2])
    for strategy in df['strategy'].unique():
        mask = df['strategy'] == strategy
        sample = df[mask].sample(min(5000, mask.sum()))
        ax6.scatter(sample['O_P'], sample['O_S'], alpha=0.3, s=2, label=strategy)
    ax6.set_xlabel('O_P')
    ax6.set_ylabel('O_S')
    ax6.set_title('Precision vs Surprise Operator', fontweight='bold')
    ax6.legend()
    ax6.grid(alpha=0.3)
    ax6.axhline(0, color='k', linewidth=0.5)
    ax6.axvline(0, color='k', linewidth=0.5)
    
    # 7. Basin occupancy
    ax7 = fig.add_subplot(gs[2, 0])
    basin_counts = df['basin_id'].value_counts().sort_index()
    basin_counts.plot(kind='bar', ax=ax7, color='steelblue')
    ax7.set_xlabel('Basin ID')
    ax7.set_ylabel('Sample Count')
    ax7.set_title('Basin Occupancy', fontweight='bold')
    ax7.grid(alpha=0.3, axis='y')
    
    # 8. Strategy pie chart
    ax8 = fig.add_subplot(gs[2, 1])
    strategy_counts = df['strategy'].value_counts()
    ax8.pie(strategy_counts.values, labels=strategy_counts.index, autopct='%1.1f%%')
    ax8.set_title('Strategy Distribution', fontweight='bold')
    
    # 9. Summary stats table
    ax9 = fig.add_subplot(gs[2, 2])
    ax9.axis('off')
    
    summary_stats = df.groupby('strategy').agg({
        'DR': 'mean',
        'S': 'mean',
        'Gamma': 'mean',
        'operator_norm': 'mean'
    }).round(3)
    
    table_data = []
    table_data.append(['Strategy', 'DR', 'S', 'Γ', '||O||'])
    for strategy, row in summary_stats.iterrows():
        table_data.append([strategy, f"{row['DR']:.3f}", f"{row['S']:.3f}", 
                          f"{row['Gamma']:.3f}", f"{row['operator_norm']:.3f}"])
    
    table = ax9.table(cellText=table_data, cellLoc='center', loc='center',
                     colWidths=[0.25, 0.15, 0.15, 0.15, 0.15])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2)
    
    # Header row formatting
    for i in range(5):
        table[(0, i)].set_facecolor('#4472C4')
        table[(0, i)].set_text_props(weight='bold', color='white')
    
    ax9.set_title('Mean Metrics by Strategy', fontweight='bold', pad=20)
    
    plt.suptitle('Sand Agent Landscape - Grand Overview', 
                 fontsize=18, fontweight='bold', y=0.98)
    
    output_path = output_dir / 'grand_dashboard.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"  ✓ Saved: {output_path.name}")


# ============================================================================
# Main
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Plot sand agent landscape data"
    )
    parser.add_argument(
        'csv_file',
        type=Path,
        help="Sand landscape CSV file"
    )
    parser.add_argument(
        '--output-dir',
        type=Path,
        default=Path('./sand_plots'),
        help="Output directory for plots"
    )
    parser.add_argument(
        '--max-samples',
        type=int,
        default=500000,
        help="Max samples to load (for memory management)"
    )
    parser.add_argument(
        '--plots',
        nargs='+',
        choices=['all', 'phase', 'operator', 'precision', 'topology', 'signatures', 'dashboard'],
        default=['all'],
        help="Which plots to generate"
    )
    
    args = parser.parse_args()
    
    # Create output directory
    args.output_dir.mkdir(parents=True, exist_ok=True)
    
    print("="*70)
    print("SAND LANDSCAPE PLOTTER")
    print("="*70)
    print(f"\nInput: {args.csv_file}")
    print(f"Output: {args.output_dir}")
    
    # Load data
    df = load_landscape(args.csv_file, args.max_samples)
    
    print("\n" + "="*70)
    print("GENERATING PLOTS")
    print("="*70)
    
    # Determine which plots to make
    plot_all = 'all' in args.plots
    
    if plot_all or 'phase' in args.plots:
        plot_strategy_phase_space(df, args.output_dir)
    
    if plot_all or 'operator' in args.plots:
        plot_operator_manifold(df, args.output_dir)
    
    if plot_all or 'precision' in args.plots:
        plot_precision_landscape(df, args.output_dir)
    
    if plot_all or 'topology' in args.plots:
        plot_basin_topology(df, args.output_dir)
    
    if plot_all or 'signatures' in args.plots:
        plot_strategy_signatures(df, args.output_dir)
    
    if plot_all or 'dashboard' in args.plots:
        plot_grand_dashboard(df, args.output_dir)
    
    print("\n" + "="*70)
    print("✓ ALL PLOTS COMPLETE!")
    print("="*70)
    print(f"\nPlots saved to: {args.output_dir}")
    print("\nGenerated files:")
    for plot_file in sorted(args.output_dir.glob('*.png')):
        print(f"  - {plot_file.name}")


if __name__ == '__main__':
    main()
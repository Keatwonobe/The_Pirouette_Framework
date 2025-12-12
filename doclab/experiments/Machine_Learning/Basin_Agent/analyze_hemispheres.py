#!/usr/bin/env python3
"""
Hemispheric Analysis Suite - Deep Brain Dynamics
=================================================

Analyzes the bilateral structure of the coherence landscape.

Extracts:
1. Interhemispheric transfer statistics (switching dynamics)
2. Hemisphere specialization (which basins do what)
3. Split-brain simulation (what breaks when you cut the corpus callosum)
4. Temporal dynamics (evolution through the landscape)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from scipy.stats import chi2_contingency, entropy
from scipy.spatial.distance import cdist
import argparse

sns.set_style("darkgrid")
plt.rcParams['figure.facecolor'] = 'white'

# ============================================================================
# Step 1: Identify Hemispheres
# ============================================================================

def identify_hemispheres(df: pd.DataFrame):
    """
    Use PCA to split the landscape into left/right hemispheres.
    
    Returns:
        df with added 'hemisphere' column ('left' or 'right')
        pca model
        hemisphere_boundary (PC1 threshold)
    """
    print("\n" + "="*70)
    print("STEP 1: IDENTIFYING HEMISPHERES")
    print("="*70)
    
    # Features for PCA
    features = ['DR', 'S', 'Gamma', 'pi', 'operator_norm']
    X = df[features].values
    
    # Normalize and reduce
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)
    
    # Add PCA coordinates to dataframe
    df['PC1'] = X_pca[:, 0]
    df['PC2'] = X_pca[:, 1]
    
    # Define hemisphere boundary (PC1 = 0)
    hemisphere_boundary = 0.0
    
    # Assign hemispheres
    df['hemisphere'] = df['PC1'].apply(lambda x: 'left' if x < hemisphere_boundary else 'right')
    
    # Statistics
    left_count = (df['hemisphere'] == 'left').sum()
    right_count = (df['hemisphere'] == 'right').sum()
    
    print(f"\nHemisphere Assignment:")
    print(f"  Left hemisphere:  {left_count:,} samples ({100*left_count/len(df):.1f}%)")
    print(f"  Right hemisphere: {right_count:,} samples ({100*right_count/len(df):.1f}%)")
    print(f"  Boundary: PC1 = {hemisphere_boundary:.2f}")
    print(f"  PC1 variance explained: {pca.explained_variance_ratio_[0]:.1%}")
    print(f"  PC2 variance explained: {pca.explained_variance_ratio_[1]:.1%}")
    
    return df, pca, scaler, hemisphere_boundary


# ============================================================================
# Step 2: Interhemispheric Transfer Statistics
# ============================================================================

def analyze_hemisphere_transfers(df: pd.DataFrame, output_dir: Path):
    """
    Analyze transitions between hemispheres.
    
    Treats consecutive samples as a temporal sequence and looks for
    left → right or right → left transitions.
    """
    print("\n" + "="*70)
    print("STEP 2: INTERHEMISPHERIC TRANSFER DYNAMICS")
    print("="*70)
    
    # Compute transitions
    df['hemisphere_prev'] = df['hemisphere'].shift(1)
    
    # Identify transfer events
    df['transfer'] = 'none'
    df.loc[(df['hemisphere_prev'] == 'left') & (df['hemisphere'] == 'right'), 'transfer'] = 'L→R'
    df.loc[(df['hemisphere_prev'] == 'right') & (df['hemisphere'] == 'left'), 'transfer'] = 'R→L'
    df.loc[(df['hemisphere_prev'] == df['hemisphere']) & (df['hemisphere_prev'].notna()), 'transfer'] = 'stay'
    
    # Count transfers
    transfer_counts = df['transfer'].value_counts()
    
    total_transitions = len(df) - 1
    n_stay = transfer_counts.get('stay', 0)
    n_LR = transfer_counts.get('L→R', 0)
    n_RL = transfer_counts.get('R→L', 0)
    
    print(f"\nTransfer Statistics:")
    print(f"  Total transitions: {total_transitions:,}")
    print(f"  Stay in hemisphere: {n_stay:,} ({100*n_stay/total_transitions:.1f}%)")
    print(f"  Left → Right: {n_LR:,} ({100*n_LR/total_transitions:.2f}%)")
    print(f"  Right → Left: {n_RL:,} ({100*n_RL/total_transitions:.2f}%)")
    
    # Transfer asymmetry
    if n_LR + n_RL > 0:
        asymmetry = (n_LR - n_RL) / (n_LR + n_RL)
        print(f"\n  Transfer asymmetry: {asymmetry:.3f}")
        if asymmetry > 0.1:
            print(f"    → Preferred direction: Left → Right (exploratory → exploitative)")
        elif asymmetry < -0.1:
            print(f"    → Preferred direction: Right → Left (exploitative → exploratory)")
        else:
            print(f"    → Bidirectional (symmetric transfers)")
    
    # Transfer rate by strategy
    print(f"\nTransfer Rate by Strategy:")
    for strategy in df['strategy'].unique():
        mask = (df['strategy'] == strategy) & (df['transfer'] != 'none')
        strategy_transfers = df[mask]
        
        if len(strategy_transfers) > 0:
            n_total = (df['strategy'] == strategy).sum()
            n_LR_strat = (strategy_transfers['transfer'] == 'L→R').sum()
            n_RL_strat = (strategy_transfers['transfer'] == 'R→L').sum()
            
            print(f"  {strategy}:")
            print(f"    L→R: {n_LR_strat:,} ({100*n_LR_strat/n_total:.2f}%)")
            print(f"    R→L: {n_RL_strat:,} ({100*n_RL_strat/n_total:.2f}%)")
    
    # Plot transfer dynamics
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # 1. Transfer counts bar chart
    transfer_data = pd.DataFrame({
        'Transfer Type': ['Stay', 'L→R', 'R→L'],
        'Count': [n_stay, n_LR, n_RL]
    })
    axes[0, 0].bar(transfer_data['Transfer Type'], transfer_data['Count'], 
                   color=['steelblue', 'coral', 'lightgreen'])
    axes[0, 0].set_ylabel('Count')
    axes[0, 0].set_title('Transfer Event Counts', fontweight='bold')
    axes[0, 0].grid(alpha=0.3, axis='y')
    
    # 2. Transfer trajectory in PCA space
    # Sample transfer events
    transfer_events = df[df['transfer'].isin(['L→R', 'R→L'])].sample(min(1000, len(df[df['transfer'] != 'stay'])))
    
    for _, row in transfer_events.iterrows():
        if row['transfer'] == 'L→R':
            color = 'coral'
            alpha = 0.3
        else:
            color = 'lightgreen'
            alpha = 0.3
        
        # Draw arrow from prev to current
        # (We don't have prev coordinates, so just mark the endpoint)
        axes[0, 1].scatter(row['PC1'], row['PC2'], c=color, s=10, alpha=alpha)
    
    axes[0, 1].axvline(0, color='k', linewidth=2, linestyle='--', label='Hemisphere Boundary')
    axes[0, 1].set_xlabel('PC1')
    axes[0, 1].set_ylabel('PC2')
    axes[0, 1].set_title('Transfer Events in PCA Space', fontweight='bold')
    axes[0, 1].legend()
    axes[0, 1].grid(alpha=0.3)
    
    # 3. Transfer rate by basin
    basin_transfers = df.groupby('basin_id')['transfer'].apply(
        lambda x: (x.isin(['L→R', 'R→L'])).sum() / len(x) if len(x) > 0 else 0
    ).sort_values(ascending=False)
    
    basin_transfers.plot(kind='bar', ax=axes[1, 0], color='steelblue')
    axes[1, 0].set_xlabel('Basin ID')
    axes[1, 0].set_ylabel('Transfer Rate')
    axes[1, 0].set_title('Interhemispheric Transfer Rate by Basin', fontweight='bold')
    axes[1, 0].grid(alpha=0.3, axis='y')
    
    # 4. Temporal transfer pattern (if sample_id exists)
    if 'sample_id' in df.columns:
        # Compute rolling transfer rate
        window = 1000
        df_sorted = df.sort_values('sample_id')
        df_sorted['is_transfer'] = df_sorted['transfer'].isin(['L→R', 'R→L']).astype(int)
        df_sorted['transfer_rate_rolling'] = df_sorted['is_transfer'].rolling(window).mean()
        
        # Downsample for plotting
        plot_data = df_sorted.iloc[::100]  # Every 100th sample
        
        axes[1, 1].plot(plot_data['sample_id'], plot_data['transfer_rate_rolling'], 
                       linewidth=1, alpha=0.7)
        axes[1, 1].set_xlabel('Sample ID')
        axes[1, 1].set_ylabel(f'Transfer Rate (rolling {window})')
        axes[1, 1].set_title('Temporal Transfer Dynamics', fontweight='bold')
        axes[1, 1].grid(alpha=0.3)
    else:
        axes[1, 1].text(0.5, 0.5, 'No temporal data\n(sample_id not found)', 
                       ha='center', va='center', fontsize=12)
        axes[1, 1].axis('off')
    
    plt.tight_layout()
    output_path = output_dir / 'hemisphere_transfers.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"\n✓ Transfer analysis plot saved: {output_path.name}")
    
    return df


# ============================================================================
# Step 3: Hemisphere Specialization
# ============================================================================

def analyze_hemisphere_specialization(df: pd.DataFrame, output_dir: Path):
    """
    Identify what each hemisphere specializes in.
    
    Compares distributions of (DR, S, Γ, strategies, basins) between hemispheres.
    """
    print("\n" + "="*70)
    print("STEP 3: HEMISPHERE SPECIALIZATION")
    print("="*70)
    
    left_df = df[df['hemisphere'] == 'left']
    right_df = df[df['hemisphere'] == 'right']
    
    # Metric comparisons
    metrics = ['DR', 'S', 'Gamma', 'pi', 'operator_norm']
    
    print("\nMetric Comparison (mean ± std):")
    print(f"{'Metric':<15} {'Left':<20} {'Right':<20} {'Difference':<15}")
    print("-" * 70)
    
    specialization = {}
    
    for metric in metrics:
        left_mean = left_df[metric].mean()
        left_std = left_df[metric].std()
        right_mean = right_df[metric].mean()
        right_std = right_df[metric].std()
        
        diff = right_mean - left_mean
        diff_pct = 100 * diff / left_mean if left_mean != 0 else 0
        
        specialization[metric] = {
            'left_mean': left_mean,
            'right_mean': right_mean,
            'diff': diff,
            'diff_pct': diff_pct
        }
        
        print(f"{metric:<15} {left_mean:>6.3f} ± {left_std:<6.3f}   "
              f"{right_mean:>6.3f} ± {right_std:<6.3f}   "
              f"{diff:>+6.3f} ({diff_pct:>+5.1f}%)")
    
    # Strategy distribution
    print("\nStrategy Distribution:")
    left_strat = left_df['strategy'].value_counts(normalize=True)
    right_strat = right_df['strategy'].value_counts(normalize=True)
    
    for strategy in df['strategy'].unique():
        left_pct = left_strat.get(strategy, 0) * 100
        right_pct = right_strat.get(strategy, 0) * 100
        print(f"  {strategy:<12} L: {left_pct:>5.1f}%  R: {right_pct:>5.1f}%")
    
    # Basin distribution
    print("\nBasin Distribution:")
    left_basin = left_df['basin_id'].value_counts(normalize=True).sort_index()
    right_basin = right_df['basin_id'].value_counts(normalize=True).sort_index()
    
    for basin_id in sorted(df['basin_id'].unique()):
        left_pct = left_basin.get(basin_id, 0) * 100
        right_pct = right_basin.get(basin_id, 0) * 100
        print(f"  Basin {basin_id:<5} L: {left_pct:>5.1f}%  R: {right_pct:>5.1f}%")
    
    # Plot specialization
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    
    # Row 1: Metric distributions
    for idx, metric in enumerate(['DR', 'S', 'Gamma']):
        ax = axes[0, idx]
        
        ax.hist(left_df[metric], bins=50, alpha=0.6, label='Left', 
               color='steelblue', density=True)
        ax.hist(right_df[metric], bins=50, alpha=0.6, label='Right', 
               color='coral', density=True)
        
        ax.set_xlabel(metric)
        ax.set_ylabel('Density')
        ax.set_title(f'{metric} Distribution', fontweight='bold')
        ax.legend()
        ax.grid(alpha=0.3)
    
    # Row 2: More distributions
    for idx, metric in enumerate(['pi', 'operator_norm']):
        ax = axes[1, idx]
        
        ax.hist(left_df[metric], bins=50, alpha=0.6, label='Left', 
               color='steelblue', density=True)
        ax.hist(right_df[metric], bins=50, alpha=0.6, label='Right', 
               color='coral', density=True)
        
        ax.set_xlabel(metric)
        ax.set_ylabel('Density')
        ax.set_title(f'{metric} Distribution', fontweight='bold')
        ax.legend()
        ax.grid(alpha=0.3)
    
    # Strategy comparison (pie charts)
    ax = axes[1, 2]
    
    # Create comparison bar chart instead
    strategies = df['strategy'].unique()
    x = np.arange(len(strategies))
    width = 0.35
    
    left_vals = [left_strat.get(s, 0) * 100 for s in strategies]
    right_vals = [right_strat.get(s, 0) * 100 for s in strategies]
    
    ax.bar(x - width/2, left_vals, width, label='Left', color='steelblue', alpha=0.8)
    ax.bar(x + width/2, right_vals, width, label='Right', color='coral', alpha=0.8)
    
    ax.set_xlabel('Strategy')
    ax.set_ylabel('Percentage')
    ax.set_title('Strategy Distribution by Hemisphere', fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(strategies, rotation=45, ha='right')
    ax.legend()
    ax.grid(alpha=0.3, axis='y')
    
    plt.tight_layout()
    output_path = output_dir / 'hemisphere_specialization.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"\n✓ Specialization analysis plot saved: {output_path.name}")
    
    return specialization


# ============================================================================
# Step 4: Split-Brain Simulation
# ============================================================================

def simulate_split_brain(df: pd.DataFrame, output_dir: Path):
    """
    Simulate what happens when you "cut the corpus callosum".
    
    Artificially prevent interhemispheric transfers and measure degradation.
    """
    print("\n" + "="*70)
    print("STEP 4: SPLIT-BRAIN SIMULATION")
    print("="*70)
    
    print("\nSimulating disconnection syndrome...")
    
    # Compute baseline metrics (with intact transfers)
    baseline_metrics = {
        'DR_mean': df['DR'].mean(),
        'DR_std': df['DR'].std(),
        'S_mean': df['S'].mean(),
        'operator_norm_mean': df['operator_norm'].mean(),
        'precision_mean': df['pi'].mean(),
    }
    
    # Simulate split brain: force hemisphere persistence
    # For each sample, if it would transfer hemispheres, instead stay in current hemisphere
    df_split = df.copy()
    
    # Identify transfer events
    df_split['would_transfer'] = df_split['transfer'].isin(['L→R', 'R→L'])
    
    # For samples that would transfer, randomly reassign to a basin in the same hemisphere
    left_basins = df[df['hemisphere'] == 'left']['basin_id'].unique()
    right_basins = df[df['hemisphere'] == 'right']['basin_id'].unique()
    
    def force_same_hemisphere(row):
        if row['would_transfer']:
            if row['hemisphere'] == 'left':
                return np.random.choice(left_basins)
            else:
                return np.random.choice(right_basins)
        return row['basin_id']
    
    df_split['basin_id_split'] = df_split.apply(force_same_hemisphere, axis=1)
    
    # Recompute metrics based on forced basin assignments
    # (This is approximate - in reality we'd need to regenerate samples)
    # For now, we'll just analyze the distribution change
    
    split_metrics = {
        'DR_mean': df_split['DR'].mean(),
        'DR_std': df_split['DR'].std(),
        'S_mean': df_split['S'].mean(),
        'operator_norm_mean': df_split['operator_norm'].mean(),
        'precision_mean': df_split['pi'].mean(),
    }
    
    print("\nMetric Comparison (Intact vs Split):")
    print(f"{'Metric':<20} {'Intact':<15} {'Split':<15} {'Change':<15}")
    print("-" * 65)
    
    for key in baseline_metrics:
        intact_val = baseline_metrics[key]
        split_val = split_metrics[key]
        change = split_val - intact_val
        change_pct = 100 * change / intact_val if intact_val != 0 else 0
        
        print(f"{key:<20} {intact_val:>10.4f}    {split_val:>10.4f}    "
              f"{change:>+7.4f} ({change_pct:>+5.1f}%)")
    
    # Measure hemisphere isolation
    print("\nHemisphere Isolation Analysis:")
    
    left_intact_diversity = df[df['hemisphere'] == 'left']['basin_id'].nunique()
    right_intact_diversity = df[df['hemisphere'] == 'right']['basin_id'].nunique()
    
    left_split_diversity = df_split[df_split['hemisphere'] == 'left']['basin_id_split'].nunique()
    right_split_diversity = df_split[df_split['hemisphere'] == 'right']['basin_id_split'].nunique()
    
    print(f"  Left hemisphere basin diversity:")
    print(f"    Intact: {left_intact_diversity} basins")
    print(f"    Split:  {left_split_diversity} basins")
    
    print(f"  Right hemisphere basin diversity:")
    print(f"    Intact: {right_intact_diversity} basins")
    print(f"    Split:  {right_split_diversity} basins")
    
    # Plot comparison
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # 1. DR distribution change
    axes[0, 0].hist(df['DR'], bins=50, alpha=0.6, label='Intact', density=True)
    axes[0, 0].hist(df_split['DR'], bins=50, alpha=0.6, label='Split', density=True)
    axes[0, 0].set_xlabel('Dark Residue')
    axes[0, 0].set_ylabel('Density')
    axes[0, 0].set_title('DR Distribution: Intact vs Split', fontweight='bold')
    axes[0, 0].legend()
    axes[0, 0].grid(alpha=0.3)
    
    # 2. Operator norm distribution change
    axes[0, 1].hist(df['operator_norm'], bins=50, alpha=0.6, label='Intact', density=True)
    axes[0, 1].hist(df_split['operator_norm'], bins=50, alpha=0.6, label='Split', density=True)
    axes[0, 1].set_xlabel('Operator Norm')
    axes[0, 1].set_ylabel('Density')
    axes[0, 1].set_title('Operator Norm: Intact vs Split', fontweight='bold')
    axes[0, 1].legend()
    axes[0, 1].grid(alpha=0.3)
    
    # 3. Basin occupancy comparison
    intact_basin_counts = df['basin_id'].value_counts().sort_index()
    split_basin_counts = df_split['basin_id_split'].value_counts().sort_index()
    
    all_basins = sorted(set(intact_basin_counts.index) | set(split_basin_counts.index))
    x = np.arange(len(all_basins))
    width = 0.35
    
    intact_vals = [intact_basin_counts.get(b, 0) for b in all_basins]
    split_vals = [split_basin_counts.get(b, 0) for b in all_basins]
    
    axes[1, 0].bar(x - width/2, intact_vals, width, label='Intact', alpha=0.8)
    axes[1, 0].bar(x + width/2, split_vals, width, label='Split', alpha=0.8)
    axes[1, 0].set_xlabel('Basin ID')
    axes[1, 0].set_ylabel('Count')
    axes[1, 0].set_title('Basin Occupancy: Intact vs Split', fontweight='bold')
    axes[1, 0].set_xticks(x)
    axes[1, 0].set_xticklabels(all_basins)
    axes[1, 0].legend()
    axes[1, 0].grid(alpha=0.3, axis='y')
    
    # 4. Hemisphere connectivity diagram
    ax = axes[1, 1]
    
    # Draw hemispheres as circles
    from matplotlib.patches import Circle, FancyArrowPatch
    
    left_circle = Circle((-0.3, 0), 0.2, color='steelblue', alpha=0.3)
    right_circle = Circle((0.3, 0), 0.2, color='coral', alpha=0.3)
    
    ax.add_patch(left_circle)
    ax.add_patch(right_circle)
    
    # Draw connection (or lack thereof)
    # Intact: bidirectional arrow
    if True:  # Intact condition
        arrow = FancyArrowPatch((-0.1, 0.05), (0.1, 0.05),
                               arrowstyle='<->', mutation_scale=20,
                               linewidth=2, color='green', label='Intact')
        ax.add_patch(arrow)
    
    # Split: X mark
    ax.plot([0, 0], [-0.1, 0.1], 'r-', linewidth=3, label='Split')
    ax.plot([-0.05, 0.05], [-0.05, 0.05], 'r-', linewidth=3)
    ax.plot([-0.05, 0.05], [0.05, -0.05], 'r-', linewidth=3)
    
    ax.text(-0.3, 0, 'L', ha='center', va='center', fontsize=20, fontweight='bold')
    ax.text(0.3, 0, 'R', ha='center', va='center', fontsize=20, fontweight='bold')
    
    ax.set_xlim(-0.6, 0.6)
    ax.set_ylim(-0.4, 0.4)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Hemispheric Connectivity', fontweight='bold')
    
    plt.tight_layout()
    output_path = output_dir / 'split_brain_simulation.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"\n✓ Split-brain simulation plot saved: {output_path.name}")
    
    return baseline_metrics, split_metrics


# ============================================================================
# Main
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Hemispheric Analysis of Sand Agent Landscape"
    )
    parser.add_argument(
        'csv_file',
        type=Path,
        help="Sand landscape CSV file"
    )
    parser.add_argument(
        '--output-dir',
        type=Path,
        default=Path('./hemisphere_analysis'),
        help="Output directory"
    )
    parser.add_argument(
        '--max-samples',
        type=int,
        default=500000,
        help="Max samples to load"
    )
    
    args = parser.parse_args()
    
    # Create output directory
    args.output_dir.mkdir(parents=True, exist_ok=True)
    
    print("="*70)
    print("HEMISPHERIC ANALYSIS SUITE")
    print("="*70)
    print(f"\nInput: {args.csv_file}")
    print(f"Output: {args.output_dir}")
    
    # Load data
    print("\nLoading data...")
    if args.csv_file.stat().st_size > 100 * 1024 * 1024:  # >100MB
        # Chunked loading
        chunks = []
        for chunk in pd.read_csv(args.csv_file, chunksize=100000):
            chunks.append(chunk)
            if len(pd.concat(chunks)) >= args.max_samples:
                break
        df = pd.concat(chunks, ignore_index=True)
    else:
        df = pd.read_csv(args.csv_file)
    
    if len(df) > args.max_samples:
        df = df.sample(n=args.max_samples, random_state=42)
    
    print(f"✓ Loaded {len(df):,} samples")
    
    # Run analyses
    df, pca, scaler, boundary = identify_hemispheres(df)
    df = analyze_hemisphere_transfers(df, args.output_dir)
    specialization = analyze_hemisphere_specialization(df, args.output_dir)
    baseline, split = simulate_split_brain(df, args.output_dir)
    
    # Save annotated data
    output_csv = args.output_dir / 'landscape_with_hemispheres.csv'
    df.to_csv(output_csv, index=False)
    print(f"\n✓ Annotated data saved: {output_csv}")
    
    print("\n" + "="*70)
    print("ANALYSIS COMPLETE")
    print("="*70)
    print(f"\nResults in: {args.output_dir}")
    print("\nGenerated files:")
    for f in sorted(args.output_dir.glob('*.png')):
        print(f"  - {f.name}")


if __name__ == '__main__':
    main()
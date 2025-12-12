#!/usr/bin/env python3
"""
Engram Analysis and Visualization Tools
=======================================

Tools for analyzing the structure and dynamics of learned engrams.
Helps understand:
1. What patterns the agent discovered
2. How coherence relates to performance
3. The geometry of the (Γ, DR, S) attractor space
4. Whether bifurcation (hemispheric structure) emerged
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from typing import List, Optional
import seaborn as sns
from scipy.spatial.distance import pdist, squareform
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

from pirouette_engram import GenerativeEngram, EngramLibrary


class EngramAnalyzer:
    """Analyzes the structure and dynamics of an engram library."""
    
    def __init__(self, library: EngramLibrary):
        self.lib = library
        
    def coherence_performance_plot(self, save_path: Optional[Path] = None):
        """
        Plot relationship between coherence and performance.
        
        Per COG-RES-004: High coherence should correlate with high return
        in stable attractor basins.
        """
        if len(self.lib) == 0:
            print("No engrams to analyze")
            return
        
        coherences = [e.mean_coherence for e in self.lib.engrams]
        returns = [e.return_raw for e in self.lib.engrams]
        gammas = [e.mean_gamma for e in self.lib.engrams]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Coherence vs Return
        scatter = ax1.scatter(coherences, returns, c=gammas, 
                             cmap='viridis', s=100, alpha=0.6)
        ax1.set_xlabel('Mean Coherence', fontsize=12)
        ax1.set_ylabel('Return', fontsize=12)
        ax1.set_title('Coherence-Performance Relationship', fontsize=14)
        ax1.grid(True, alpha=0.3)
        plt.colorbar(scatter, ax=ax1, label='Mean Γ (Load)')
        
        # Coherence distribution
        ax2.hist(coherences, bins=15, alpha=0.7, color='steelblue', edgecolor='black')
        ax2.axvline(np.mean(coherences), color='red', linestyle='--', 
                   label=f'Mean: {np.mean(coherences):.3f}')
        ax2.set_xlabel('Mean Coherence', fontsize=12)
        ax2.set_ylabel('Count', fontsize=12)
        ax2.set_title('Coherence Distribution', fontsize=14)
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"Saved coherence-performance plot to {save_path}")
        else:
            plt.show()
    
    def attractor_space_plot(self, save_path: Optional[Path] = None):
        """
        Visualize engrams in (Γ, DR, S) attractor space.
        
        This is the space of "generating conditions" per COG-RES-006.
        Good engrams should cluster in specific regions.
        """
        if len(self.lib) == 0:
            print("No engrams to analyze")
            return
        
        gammas = np.array([e.mean_gamma for e in self.lib.engrams])
        DRs = np.array([e.mean_DR for e in self.lib.engrams])
        Ss = np.array([e.mean_surprise for e in self.lib.engrams])
        returns = np.array([e.return_raw for e in self.lib.engrams])
        
        fig = plt.figure(figsize=(14, 5))
        
        # 3D scatter
        ax1 = fig.add_subplot(131, projection='3d')
        scatter = ax1.scatter(gammas, DRs, Ss, c=returns, 
                             cmap='plasma', s=100, alpha=0.7)
        ax1.set_xlabel('Γ (Load)', fontsize=10)
        ax1.set_ylabel('DR', fontsize=10)
        ax1.set_zlabel('S (Surprise)', fontsize=10)
        ax1.set_title('Attractor Space (Γ, DR, S)', fontsize=12)
        plt.colorbar(scatter, ax=ax1, label='Return', shrink=0.7)
        
        # Γ-DR projection
        ax2 = fig.add_subplot(132)
        scatter2 = ax2.scatter(gammas, DRs, c=returns, cmap='plasma', 
                              s=100, alpha=0.7, edgecolors='black')
        ax2.set_xlabel('Γ (Load)', fontsize=12)
        ax2.set_ylabel('DR', fontsize=12)
        ax2.set_title('Load-Residue Projection', fontsize=14)
        ax2.grid(True, alpha=0.3)
        plt.colorbar(scatter2, ax=ax2, label='Return')
        
        # DR-S projection
        ax3 = fig.add_subplot(133)
        scatter3 = ax3.scatter(DRs, Ss, c=returns, cmap='plasma',
                              s=100, alpha=0.7, edgecolors='black')
        ax3.set_xlabel('DR', fontsize=12)
        ax3.set_ylabel('S (Surprise)', fontsize=12)
        ax3.set_title('Residue-Surprise Projection', fontsize=14)
        ax3.grid(True, alpha=0.3)
        plt.colorbar(scatter3, ax=ax3, label='Return')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"Saved attractor space plot to {save_path}")
        else:
            plt.show()
    
    def hidden_state_manifold(self, n_samples: int = 100, 
                             save_path: Optional[Path] = None):
        """
        Analyze the geometry of hidden state trajectories.
        
        Key question: Do hidden states cluster into distinct basins?
        Is there evidence of hemispheric bifurcation?
        """
        if len(self.lib) == 0:
            print("No engrams to analyze")
            return
        
        # Sample hidden states from each engram
        all_hiddens = []
        engram_ids = []
        returns = []
        
        for i, eng in enumerate(self.lib.engrams):
            # Sample evenly from trajectory
            indices = np.linspace(0, eng.length-1, n_samples, dtype=int)
            sampled = eng.hiddens[indices]
            all_hiddens.append(sampled)
            engram_ids.extend([i] * len(sampled))
            returns.extend([eng.return_raw] * len(sampled))
        
        all_hiddens = np.vstack(all_hiddens)
        engram_ids = np.array(engram_ids)
        returns = np.array(returns)
        
        # Reduce dimensionality
        print(f"Analyzing {all_hiddens.shape[0]} hidden states...")
        
        # PCA
        pca = PCA(n_components=3)
        hiddens_pca = pca.fit_transform(all_hiddens)
        
        # t-SNE (slower but better for structure)
        print("Computing t-SNE embedding...")
        tsne = TSNE(n_components=2, perplexity=30, random_state=42)
        hiddens_tsne = tsne.fit_transform(all_hiddens)
        
        # Plot
        fig, axes = plt.subplots(1, 3, figsize=(18, 5))
        
        # PCA 3D
        ax1 = fig.add_subplot(131, projection='3d')
        scatter1 = ax1.scatter(hiddens_pca[:, 0], hiddens_pca[:, 1], hiddens_pca[:, 2],
                              c=returns, cmap='viridis', s=20, alpha=0.6)
        ax1.set_title('Hidden State Manifold (PCA)', fontsize=14)
        ax1.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.2%})')
        ax1.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.2%})')
        ax1.set_zlabel(f'PC3 ({pca.explained_variance_ratio_[2]:.2%})')
        plt.colorbar(scatter1, ax=ax1, label='Return', shrink=0.7)
        
        # t-SNE by engram
        ax2 = axes[1]
        scatter2 = ax2.scatter(hiddens_tsne[:, 0], hiddens_tsne[:, 1],
                              c=engram_ids, cmap='tab20', s=20, alpha=0.6)
        ax2.set_title('Hidden State Clusters (t-SNE)', fontsize=14)
        ax2.set_xlabel('t-SNE 1')
        ax2.set_ylabel('t-SNE 2')
        ax2.grid(True, alpha=0.3)
        
        # t-SNE by return
        ax3 = axes[2]
        scatter3 = ax3.scatter(hiddens_tsne[:, 0], hiddens_tsne[:, 1],
                              c=returns, cmap='plasma', s=20, alpha=0.6)
        ax3.set_title('Hidden State Performance (t-SNE)', fontsize=14)
        ax3.set_xlabel('t-SNE 1')
        ax3.set_ylabel('t-SNE 2')
        ax3.grid(True, alpha=0.3)
        plt.colorbar(scatter3, ax=ax3, label='Return')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"Saved hidden state manifold to {save_path}")
        else:
            plt.show()
        
        # Print variance explained
        print(f"\nPCA explained variance: {pca.explained_variance_ratio_[:5]}")
        print(f"Total variance (5 PCs): {pca.explained_variance_ratio_[:5].sum():.2%}")
    
    def resonance_matrix(self, save_path: Optional[Path] = None):
        """
        Compute pairwise resonance scores between all engrams.
        
        Shows which engrams are similar in (Γ, DR, S) space.
        Highly modular structure suggests distinct solution classes.
        """
        if len(self.lib) < 2:
            print("Need at least 2 engrams")
            return
        
        n = len(self.lib.engrams)
        resonance = np.zeros((n, n))
        
        for i, eng_i in enumerate(self.lib.engrams):
            for j, eng_j in enumerate(self.lib.engrams):
                resonance[i, j] = eng_i.resonance_score(
                    eng_j.mean_gamma,
                    eng_j.mean_DR,
                    eng_j.mean_surprise
                )
        
        # Plot
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Resonance matrix
        im1 = ax1.imshow(resonance, cmap='viridis', aspect='auto')
        ax1.set_title('Engram Resonance Matrix', fontsize=14)
        ax1.set_xlabel('Engram Index')
        ax1.set_ylabel('Engram Index')
        plt.colorbar(im1, ax=ax1, label='Resonance Score')
        
        # Hierarchical clustering (dendrogram-like)
        from scipy.cluster.hierarchy import linkage, dendrogram
        dist_matrix = 1 - resonance  # Convert similarity to distance
        np.fill_diagonal(dist_matrix, 0)
        
        # Only compute if we have enough engrams
        if n >= 3:
            linkage_matrix = linkage(squareform(dist_matrix), method='average')
            dendrogram(linkage_matrix, ax=ax2)
            ax2.set_title('Engram Clustering', fontsize=14)
            ax2.set_xlabel('Engram Index')
            ax2.set_ylabel('Distance (1 - Resonance)')
        else:
            ax2.text(0.5, 0.5, 'Need ≥3 engrams\nfor clustering',
                    ha='center', va='center', transform=ax2.transAxes)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"Saved resonance matrix to {save_path}")
        else:
            plt.show()
    
    def temporal_dynamics(self, engram_idx: int = 0, 
                         save_path: Optional[Path] = None):
        """
        Visualize temporal dynamics of a single engram.
        
        Shows how (Γ, DR, S, coherence) evolve over the trajectory.
        Reveals attractor structure and phase transitions.
        """
        if engram_idx >= len(self.lib):
            print(f"Engram {engram_idx} not found")
            return
        
        eng = self.lib.engrams[engram_idx]
        T = eng.length
        time = np.arange(T)
        
        # Extract traces
        DR_trace = eng.brain_features[:, 0]
        S_trace = eng.brain_features[:, 1]
        Gamma_trace = eng.brain_features[:, 2]
        coherence = eng.coherence_profile
        
        # Hidden state velocity (attractor flow speed)
        h_diff = np.diff(eng.hiddens, axis=0)
        h_vel = np.linalg.norm(h_diff, axis=-1)
        h_vel = np.concatenate([[h_vel[0]], h_vel])  # Pad
        
        # Plot
        fig, axes = plt.subplots(3, 2, figsize=(14, 10))
        fig.suptitle(f'Engram {engram_idx} Temporal Dynamics | Return: {eng.return_raw:.1f}',
                    fontsize=16, fontweight='bold')
        
        # Γ, DR, S
        ax1 = axes[0, 0]
        ax1.plot(time, Gamma_trace, label='Γ (Load)', color='red', linewidth=1.5)
        ax1.plot(time, DR_trace, label='DR', color='blue', linewidth=1.5)
        ax1.plot(time, S_trace, label='S (Surprise)', color='green', linewidth=1.5)
        ax1.set_ylabel('Value', fontsize=12)
        ax1.set_title('Generating Conditions', fontsize=14)
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Coherence
        ax2 = axes[0, 1]
        ax2.plot(time, coherence, color='purple', linewidth=1.5)
        ax2.axhline(eng.mean_coherence, color='purple', linestyle='--',
                   label=f'Mean: {eng.mean_coherence:.3f}')
        ax2.set_ylabel('Coherence', fontsize=12)
        ax2.set_title('Temporal Coherence', fontsize=14)
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Hidden state velocity
        ax3 = axes[1, 0]
        ax3.plot(time, h_vel, color='orange', linewidth=1.5)
        ax3.set_ylabel('||dh/dt||', fontsize=12)
        ax3.set_title('Attractor Flow Speed', fontsize=14)
        ax3.grid(True, alpha=0.3)
        
        # Phase portrait: Γ vs DR
        ax4 = axes[1, 1]
        scatter = ax4.scatter(Gamma_trace, DR_trace, c=time, cmap='viridis',
                             s=20, alpha=0.6)
        ax4.set_xlabel('Γ (Load)', fontsize=12)
        ax4.set_ylabel('DR', fontsize=12)
        ax4.set_title('Phase Portrait: Load-Residue', fontsize=14)
        ax4.grid(True, alpha=0.3)
        plt.colorbar(scatter, ax=ax4, label='Time Step')
        
        # Action magnitude
        ax5 = axes[2, 0]
        act_mag = np.linalg.norm(eng.actions, axis=-1)
        ax5.plot(time, act_mag, color='darkgreen', linewidth=1.5)
        ax5.set_xlabel('Time Step', fontsize=12)
        ax5.set_ylabel('||Action||', fontsize=12)
        ax5.set_title('Action Magnitude', fontsize=14)
        ax5.grid(True, alpha=0.3)
        
        # Observation magnitude
        ax6 = axes[2, 1]
        obs_mag = np.linalg.norm(eng.obs, axis=-1)
        ax6.plot(time, obs_mag, color='navy', linewidth=1.5)
        ax6.set_xlabel('Time Step', fontsize=12)
        ax6.set_ylabel('||Observation||', fontsize=12)
        ax6.set_title('State Magnitude', fontsize=14)
        ax6.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"Saved temporal dynamics to {save_path}")
        else:
            plt.show()
    
    def generate_report(self, output_dir: Path):
        """Generate a comprehensive analysis report."""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"\n{'='*60}")
        print(f"Generating Engram Analysis Report")
        print(f"{'='*60}")
        
        # Statistics
        stats = self.lib.stats()
        print("\nLibrary Statistics:")
        for k, v in stats.items():
            print(f"  {k}: {v:.3f}")
        
        # Generate all plots
        print("\nGenerating visualizations...")
        self.coherence_performance_plot(output_dir / "coherence_performance.png")
        self.attractor_space_plot(output_dir / "attractor_space.png")
        self.resonance_matrix(output_dir / "resonance_matrix.png")
        
        if len(self.lib) > 0:
            self.hidden_state_manifold(save_path=output_dir / "hidden_manifold.png")
            self.temporal_dynamics(0, save_path=output_dir / "temporal_dynamics_best.png")
        
        print(f"\n✓ Report saved to {output_dir}")
        print(f"{'='*60}\n")


# =====================================================================
# CLI for standalone analysis
# =====================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Analyze engram library")
    parser.add_argument("--library", type=Path, required=True,
                       help="Path to saved engram library JSON")
    parser.add_argument("--output-dir", type=Path, default=Path("./engram_analysis"),
                       help="Output directory for plots")
    args = parser.parse_args()
    
    # Load library
    print(f"Loading engram library from {args.library}")
    lib = EngramLibrary.load(args.library)
    print(f"Loaded {len(lib)} engrams")
    
    # Analyze
    analyzer = EngramAnalyzer(lib)
    analyzer.generate_report(args.output_dir)

#!/usr/bin/env python3
"""
Coherence Chess Visualizer

Plots the coherence manifold, stratagem tug, and move distributions
for chess positions analyzed through the Pirouette framework.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch
from matplotlib.collections import PathCollection
import seaborn as sns
from typing import List, Tuple
from coherence_chess import (
    CoherenceChessSolver, PositionSegment, CoherenceClass, CoherenceMetrics
)
import chess


class CoherenceVisualizer:
    """Visualize the coherence manifold for chess positions"""
    
    def __init__(self):
        self.class_colors = {
            CoherenceClass.LAMINAR_PRESERVING: '#2ecc71',      # Green
            CoherenceClass.CONSTRUCTIVE_FORCING: '#3498db',    # Blue
            CoherenceClass.OPPORTUNISTIC_TURBULENT: '#e74c3c', # Red
            CoherenceClass.RESIDUE_HEAVY: '#95a5a6',           # Gray
        }
        
        self.class_markers = {
            CoherenceClass.LAMINAR_PRESERVING: 'o',
            CoherenceClass.CONSTRUCTIVE_FORCING: '^',
            CoherenceClass.OPPORTUNISTIC_TURBULENT: 's',
            CoherenceClass.RESIDUE_HEAVY: 'x',
        }
    
    def plot_manifold(self, segments: List[PositionSegment], 
                     stratagem_tug: np.ndarray,
                     title: str = "Coherence Manifold",
                     save_path: str = None):
        """
        Plot the full coherence manifold visualization
        """
        fig, axes = plt.subplots(2, 2, figsize=(14, 12))
        
        # Main manifold plot (K_tau vs V_Gamma)
        self._plot_coherence_space(axes[0, 0], segments, stratagem_tug)
        
        # Lagrangian distribution
        self._plot_lagrangian_distribution(axes[0, 1], segments)
        
        # Dark residue analysis
        self._plot_residue_analysis(axes[1, 0], segments)
        
        # CPB ratio plot
        self._plot_cpb_analysis(axes[1, 1], segments)
        
        fig.suptitle(title, fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Saved visualization to {save_path}")
        
        return fig
    
    def _plot_coherence_space(self, ax, segments: List[PositionSegment],
                             stratagem_tug: np.ndarray):
        """
        Main plot: K_tau vs V_Gamma with coherence regions
        """
        # Plot background regions
        self._draw_coherence_regions(ax)
        
        # Plot each move
        for seg in segments:
            if seg.metrics:
                color = self.class_colors[seg.coherence_class]
                marker = self.class_markers[seg.coherence_class]
                
                # Size by L_p magnitude
                size = max(50, 200 * abs(seg.metrics.L_p))
                
                ax.scatter(
                    seg.metrics.K_tau, 
                    seg.metrics.V_Gamma,
                    c=color,
                    marker=marker,
                    s=size,
                    alpha=0.7,
                    edgecolors='black',
                    linewidth=1,
                    label=seg.coherence_class.value if seg == segments[0] else ""
                )
        
        # Draw stratagem tug vector
        if stratagem_tug is not None and len(stratagem_tug) == 2:
            ax.arrow(
                0.5, 0.5,
                stratagem_tug[0] * 0.3, stratagem_tug[1] * 0.3,
                head_width=0.05,
                head_length=0.05,
                fc='purple',
                ec='purple',
                linewidth=3,
                alpha=0.7,
                label='Stratagem Tug'
            )
        
        ax.set_xlabel('K_τ (Temporal Coherence)', fontsize=12, fontweight='bold')
        ax.set_ylabel('V_Γ (Temporal Pressure)', fontsize=12, fontweight='bold')
        ax.set_title('Coherence Manifold', fontsize=13, fontweight='bold')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.grid(True, alpha=0.3)
        ax.legend(loc='upper right', fontsize=9)
    
    def _draw_coherence_regions(self, ax):
        """Draw the four coherence regions as background"""
        # Laminar (high K, low V)
        ax.add_patch(plt.Rectangle(
            (0.6, 0), 0.4, 0.5,
            alpha=0.1, color='green', label='Laminar Zone'
        ))
        
        # Constructive Forcing (mid-high K, high V)
        ax.add_patch(plt.Rectangle(
            (0.4, 0.6), 0.6, 0.4,
            alpha=0.1, color='blue', label='Forcing Zone'
        ))
        
        # Turbulent (high V)
        ax.add_patch(plt.Rectangle(
            (0, 0.7), 0.4, 0.3,
            alpha=0.1, color='red', label='Turbulent Zone'
        ))
        
        # Stagnant (low K, low V)
        ax.add_patch(plt.Rectangle(
            (0, 0), 0.3, 0.3,
            alpha=0.1, color='gray', label='Stagnant Zone'
        ))
    
    def _plot_lagrangian_distribution(self, ax, segments: List[PositionSegment]):
        """Plot distribution of L_p values"""
        L_p_values = [seg.metrics.L_p for seg in segments if seg.metrics]
        classes = [seg.coherence_class for seg in segments if seg.metrics]
        
        # Create grouped data
        class_data = {}
        for cls in CoherenceClass:
            class_data[cls.value] = [
                L_p_values[i] for i, c in enumerate(classes) if c == cls
            ]
        
        # Box plot
        data_to_plot = [class_data[cls.value] for cls in CoherenceClass 
                       if class_data[cls.value]]
        labels = [cls.value for cls in CoherenceClass 
                 if class_data[cls.value]]
        colors = [self.class_colors[cls] for cls in CoherenceClass
                 if class_data[cls.value]]
        
        bp = ax.boxplot(data_to_plot, labels=labels, patch_artist=True)
        
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.6)
        
        ax.axhline(y=0, color='red', linestyle='--', linewidth=2, alpha=0.5,
                  label='L_p = 0')
        ax.set_ylabel('L_p = K_τ - V_Γ', fontsize=12, fontweight='bold')
        ax.set_title('Lagrangian Distribution', fontsize=13, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        ax.legend()
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=15, ha='right')
    
    def _plot_residue_analysis(self, ax, segments: List[PositionSegment]):
        """Plot dark residue vs L_p"""
        L_p_values = []
        D_values = []
        colors = []
        
        for seg in segments:
            if seg.metrics:
                L_p_values.append(seg.metrics.L_p)
                D_values.append(seg.metrics.D)
                colors.append(self.class_colors[seg.coherence_class])
        
        ax.scatter(L_p_values, D_values, c=colors, s=100, alpha=0.6,
                  edgecolors='black', linewidth=1)
        
        # Draw residue budget line
        if segments:
            D_max = max(D_values) if D_values else 0.5
            ax.axhline(y=D_max, color='red', linestyle='--', linewidth=2,
                      label=f'D_max = {D_max:.2f}')
        
        # Draw optimal region (high L_p, low D)
        ax.axvline(x=0, color='gray', linestyle='-', linewidth=1, alpha=0.3)
        ax.axhline(y=0.3, color='orange', linestyle='--', linewidth=1,
                  alpha=0.5, label='Low Residue Threshold')
        
        ax.set_xlabel('L_p (Pirouette Lagrangian)', fontsize=12, fontweight='bold')
        ax.set_ylabel('D (Dark Residue)', fontsize=12, fontweight='bold')
        ax.set_title('Residue vs Performance', fontsize=13, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend()
    
    def _plot_cpb_analysis(self, ax, segments: List[PositionSegment]):
        """Plot CPB ratio histogram and zones"""
        cpb_values = [seg.metrics.CPB for seg in segments if seg.metrics]
        classes = [seg.coherence_class for seg in segments if seg.metrics]
        
        # Create stacked histogram
        class_data = {}
        for cls in CoherenceClass:
            class_data[cls] = [
                cpb_values[i] for i, c in enumerate(classes) if c == cls
            ]
        
        bins = np.linspace(0, max(cpb_values) if cpb_values else 2, 15)
        
        for cls in CoherenceClass:
            if class_data[cls]:
                ax.hist(
                    class_data[cls],
                    bins=bins,
                    alpha=0.6,
                    label=cls.value,
                    color=self.class_colors[cls],
                    edgecolor='black',
                    linewidth=0.5
                )
        
        # Mark key zones
        ax.axvline(x=1.0, color='green', linestyle='--', linewidth=2,
                  label='CPB = 1 (Balance)', alpha=0.7)
        ax.axvspan(0.8, 1.5, alpha=0.1, color='green', label='Healthy Zone')
        
        ax.set_xlabel('CPB Ratio (K_τ / V_Γ)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Number of Moves', fontsize=12, fontweight='bold')
        ax.set_title('Coherence-Pressure Balance', fontsize=13, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        ax.legend(fontsize=9)
    
    def plot_move_trajectory(self, position_history: List[chess.Board],
                           solver: CoherenceChessSolver,
                           save_path: str = None):
        """
        Plot the trajectory through coherence space over a game
        """
        fig, ax = plt.subplots(figsize=(12, 10))
        
        trajectory = []
        for i, board in enumerate(position_history):
            segments = solver.evaluate_position(board)
            if segments:
                best = segments[0]
                trajectory.append((
                    best.metrics.K_tau,
                    best.metrics.V_Gamma,
                    best.metrics.L_p
                ))
        
        if not trajectory:
            return None
        
        # Draw background regions
        self._draw_coherence_regions(ax)
        
        # Plot trajectory
        K_vals = [t[0] for t in trajectory]
        V_vals = [t[1] for t in trajectory]
        L_vals = [t[2] for t in trajectory]
        
        # Color by L_p
        scatter = ax.scatter(
            K_vals, V_vals,
            c=L_vals,
            cmap='RdYlGn',
            s=200,
            alpha=0.7,
            edgecolors='black',
            linewidth=2
        )
        
        # Draw trajectory line
        ax.plot(K_vals, V_vals, 'k--', alpha=0.3, linewidth=1)
        
        # Annotate move numbers
        for i, (k, v) in enumerate(zip(K_vals, V_vals)):
            ax.annotate(
                str(i+1),
                (k, v),
                fontsize=8,
                fontweight='bold',
                ha='center',
                va='center'
            )
        
        plt.colorbar(scatter, ax=ax, label='L_p')
        
        ax.set_xlabel('K_τ (Temporal Coherence)', fontsize=12, fontweight='bold')
        ax.set_ylabel('V_Γ (Temporal Pressure)', fontsize=12, fontweight='bold')
        ax.set_title('Game Trajectory Through Coherence Space', 
                    fontsize=14, fontweight='bold')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.grid(True, alpha=0.3)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Saved trajectory to {save_path}")
        
        return fig
    
    def create_coherence_heatmap(self, segments: List[PositionSegment],
                                resolution: int = 50,
                                save_path: str = None):
        """
        Create a heatmap of L_p values across the K_tau-V_Gamma space
        """
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Create grid
        K_grid = np.linspace(0, 1, resolution)
        V_grid = np.linspace(0, 1, resolution)
        L_p_grid = np.zeros((resolution, resolution))
        
        # Populate grid with interpolated L_p values
        from scipy.interpolate import griddata
        
        points = np.array([
            [seg.metrics.K_tau, seg.metrics.V_Gamma] 
            for seg in segments if seg.metrics
        ])
        values = np.array([
            seg.metrics.L_p 
            for seg in segments if seg.metrics
        ])
        
        if len(points) > 3:
            # Create mesh grid
            K_mesh, V_mesh = np.meshgrid(K_grid, V_grid)
            
            # Interpolate
            L_p_grid = griddata(
                points, values,
                (K_mesh, V_mesh),
                method='cubic',
                fill_value=0
            )
            
            # Plot heatmap
            im = ax.imshow(
                L_p_grid,
                extent=[0, 1, 0, 1],
                origin='lower',
                aspect='auto',
                cmap='RdYlGn',
                alpha=0.8
            )
            
            plt.colorbar(im, ax=ax, label='L_p')
            
            # Overlay actual moves
            for seg in segments:
                if seg.metrics:
                    ax.plot(
                        seg.metrics.K_tau,
                        seg.metrics.V_Gamma,
                        'ko',
                        markersize=8,
                        markeredgewidth=2,
                        markerfacecolor='white',
                        alpha=0.7
                    )
        
        ax.set_xlabel('K_τ (Temporal Coherence)', fontsize=12, fontweight='bold')
        ax.set_ylabel('V_Γ (Temporal Pressure)', fontsize=12, fontweight='bold')
        ax.set_title('Coherence Landscape Heatmap', fontsize=14, fontweight='bold')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Saved heatmap to {save_path}")
        
        return fig


def visualize_position(fen: str = None, output_dir: str = "/mnt/user-data/outputs"):
    """
    Complete visualization of a chess position
    """
    import os
    
    solver = CoherenceChessSolver(D_max=0.5, base_depth=2)
    visualizer = CoherenceVisualizer()
    
    # Setup position
    board = chess.Board(fen) if fen else chess.Board()
    
    print(f"Analyzing position: {board.fen()}\n")
    print(board)
    print()
    
    # Evaluate
    segments = solver.evaluate_position(board)
    tug = solver.navigator.compute_stratagem_tug(segments[:10])
    
    # Text analysis
    analysis = solver.analyze_position(board, top_n=8)
    print(analysis)
    
    # Create visualizations
    os.makedirs(output_dir, exist_ok=True)
    
    manifold_path = os.path.join(output_dir, "coherence_manifold.png")
    fig1 = visualizer.plot_manifold(
        segments, tug,
        title=f"Coherence Analysis: {board.fen()[:30]}...",
        save_path=manifold_path
    )
    
    heatmap_path = os.path.join(output_dir, "coherence_heatmap.png")
    fig2 = visualizer.create_coherence_heatmap(
        segments,
        save_path=heatmap_path
    )
    
    plt.show()
    
    return solver, segments


def demo_game_trajectory(n_moves: int = 10, output_dir: str = "/mnt/user-data/outputs"):
    """
    Play a game and visualize the trajectory
    """
    import os
    
    solver = CoherenceChessSolver(D_max=0.5, base_depth=2)
    visualizer = CoherenceVisualizer()
    
    board = chess.Board()
    position_history = [board.copy()]
    move_history = []
    
    print("Playing coherence-optimal game...\n")
    
    for i in range(n_moves):
        if board.is_game_over():
            break
        
        print(f"Move {i+1}:")
        best_move, metrics = solver.select_best_move(board, move_history, verbose=False)
        print(f"  {best_move.uci()}: L_p={metrics.L_p:+.3f}")
        
        board.push(best_move)
        move_history.append(best_move)
        position_history.append(board.copy())
    
    print(f"\nFinal position:\n{board}\n")
    
    # Visualize trajectory
    os.makedirs(output_dir, exist_ok=True)
    trajectory_path = os.path.join(output_dir, "game_trajectory.png")
    
    fig = visualizer.plot_move_trajectory(
        position_history,
        solver,
        save_path=trajectory_path
    )
    
    plt.show()
    
    return solver, position_history


if __name__ == "__main__":
    print("Coherence Chess Visualizer\n")
    print("=" * 60)
    
    # Example 1: Analyze starting position
    print("\n1. Analyzing starting position...")
    visualize_position()
    
    # Example 2: Game trajectory
    print("\n2. Playing coherence-optimal game...")
    demo_game_trajectory(n_moves=15)
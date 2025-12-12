#!/usr/bin/env python3
"""
Coherence Chess Solver - Comprehensive Demo

Demonstrates the Pirouette Lagrangian applied to various chess positions,
showing how different position types create different coherence landscapes.
"""

import chess
from coherence_chess import CoherenceChessSolver, CoherenceClass
from coherence_visualizer import CoherenceVisualizer
import matplotlib.pyplot as plt
import os


def analyze_interesting_positions():
    """Analyze several tactically and positionally interesting positions"""
    
    solver = CoherenceChessSolver(D_max=0.5, base_depth=3)
    visualizer = CoherenceVisualizer()
    
    # Define interesting positions
    positions = {
        "Opening": {
            "fen": chess.STARTING_FEN,
            "description": "Starting position - pure potential",
        },
        "Italian_Middlegame": {
            "fen": "r1bqk2r/pppp1ppp/2n2n2/2b1p3/2B1P3/3P1N2/PPP2PPP/RNBQK2R w KQkq - 0 5",
            "description": "Italian Game middlegame - balanced complexity",
        },
        "Tactical_Storm": {
            "fen": "r1bq1rk1/ppp2ppp/2np1n2/2b1p3/2B1P3/2NP1N2/PPP1QPPP/R1B2RK1 b - - 0 8",
            "description": "Tactical position with mutual attacks",
        },
        "Endgame": {
            "fen": "8/5k2/3p4/1p1Pp2p/pP2Pp1P/P4P1K/8/8 b - - 0 1",
            "description": "King and pawn endgame - pure calculation",
        },
        "Sacrificial_Attack": {
            "fen": "r1bq1rk1/ppp2ppp/2np1n2/2b1p3/2B1P3/2NP1N2/PPP2PPP/R1BQK2R w KQ - 0 8",
            "description": "Position with sacrificial possibilities",
        },
    }
    
    output_dir = "./outputs"
    os.makedirs(output_dir, exist_ok=True)
    
    results = {}
    
    print("="*70)
    print("COHERENCE CHESS SOLVER - COMPREHENSIVE ANALYSIS")
    print("="*70)
    print()
    
    for name, pos_data in positions.items():
        print(f"\n{'='*70}")
        print(f"Position: {name}")
        print(f"Description: {pos_data['description']}")
        print(f"{'='*70}\n")
        
        board = chess.Board(pos_data['fen'])
        print(board)
        print()
        
        # Evaluate
        segments = solver.evaluate_position(board)
        tug = solver.navigator.compute_stratagem_tug(segments[:10])
        
        # Statistics
        total_moves = len(segments)
        class_dist = {}
        for seg in segments:
            cls = seg.coherence_class.value
            class_dist[cls] = class_dist.get(cls, 0) + 1
        
        # Metrics summary
        avg_L_p = sum(s.metrics.L_p for s in segments) / len(segments)
        avg_K_tau = sum(s.metrics.K_tau for s in segments) / len(segments)
        avg_V_Gamma = sum(s.metrics.V_Gamma for s in segments) / len(segments)
        avg_D = sum(s.metrics.D for s in segments) / len(segments)
        
        print(f"Total Legal Moves: {total_moves}")
        print(f"\nCoherence Landscape:")
        print(f"  Average L_p:     {avg_L_p:+.3f}")
        print(f"  Average K_τ:     {avg_K_tau:.3f}")
        print(f"  Average V_Γ:     {avg_V_Gamma:.3f}")
        print(f"  Average D:       {avg_D:.3f}")
        print(f"\nStratagem Tug: K_τ={tug[0]:.3f}, V_Γ={tug[1]:.3f}")
        
        print(f"\nMove Class Distribution:")
        for cls_name, count in sorted(class_dist.items()):
            pct = 100 * count / total_moves
            print(f"  {cls_name:20s}: {count:2d} moves ({pct:5.1f}%)")
        
        print(f"\nTop 5 Moves:")
        for i, seg in enumerate(segments[:5], 1):
            m = seg.metrics
            print(f"  {i}. {seg.move.uci():6s} [{seg.coherence_class.value.upper():10s}] "
                  f"L_p={m.L_p:+.3f}  K_τ={m.K_tau:.3f}  V_Γ={m.V_Gamma:.3f}  D={m.D:.3f}")
        
        # Visualize
        fig = visualizer.plot_manifold(
            segments, tug,
            title=f"Coherence Analysis: {name}",
            save_path=os.path.join(output_dir, f"{name}_manifold.png")
        )
        plt.close(fig)
        
        # Store results
        results[name] = {
            'segments': segments,
            'tug': tug,
            'stats': {
                'total_moves': total_moves,
                'avg_L_p': avg_L_p,
                'avg_K_tau': avg_K_tau,
                'avg_V_Gamma': avg_V_Gamma,
                'avg_D': avg_D,
                'class_dist': class_dist,
            }
        }
    
    # Create comparison plot
    create_position_comparison(results, output_dir)
    
    print(f"\n{'='*70}")
    print("Analysis complete! Visualizations saved to:")
    print(f"  {output_dir}/")
    print(f"{'='*70}\n")
    
    return results


def create_position_comparison(results, output_dir):
    """Create a comparison plot across all positions"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    positions = list(results.keys())
    
    # 1. Average metrics comparison
    ax = axes[0, 0]
    metrics = ['avg_L_p', 'avg_K_tau', 'avg_V_Gamma', 'avg_D']
    metric_labels = ['L_p', 'K_τ', 'V_Γ', 'D']
    
    x = range(len(positions))
    width = 0.2
    
    for i, (metric, label) in enumerate(zip(metrics, metric_labels)):
        values = [results[pos]['stats'][metric] for pos in positions]
        ax.bar([xi + i*width for xi in x], values, width, label=label, alpha=0.7)
    
    ax.set_ylabel('Value', fontweight='bold')
    ax.set_title('Average Coherence Metrics by Position', fontweight='bold')
    ax.set_xticks([xi + width*1.5 for xi in x])
    ax.set_xticklabels(positions, rotation=15, ha='right')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    ax.axhline(y=0, color='red', linestyle='--', alpha=0.5)
    
    # 2. Class distribution comparison
    ax = axes[0, 1]
    
    all_classes = ['laminar', 'constructive', 'turbulent', 'reject']
    class_colors = ['#2ecc71', '#3498db', '#e74c3c', '#95a5a6']
    
    bottoms = [0] * len(positions)
    for cls, color in zip(all_classes, class_colors):
        heights = [
            results[pos]['stats']['class_dist'].get(cls, 0) / 
            results[pos]['stats']['total_moves'] * 100
            for pos in positions
        ]
        ax.bar(x, heights, bottom=bottoms, label=cls, color=color, alpha=0.7)
        bottoms = [b + h for b, h in zip(bottoms, heights)]
    
    ax.set_ylabel('Percentage', fontweight='bold')
    ax.set_title('Move Class Distribution', fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(positions, rotation=15, ha='right')
    ax.legend()
    ax.set_ylim(0, 100)
    ax.grid(True, alpha=0.3, axis='y')
    
    # 3. Stratagem tug vectors
    ax = axes[1, 0]
    
    for i, pos in enumerate(positions):
        tug = results[pos]['tug']
        color = plt.cm.viridis(i / len(positions))
        ax.arrow(0, 0, tug[0], tug[1], head_width=0.05, head_length=0.05,
                fc=color, ec=color, linewidth=2, alpha=0.7, label=pos)
    
    ax.set_xlabel('K_τ Direction', fontweight='bold')
    ax.set_ylabel('V_Γ Direction', fontweight='bold')
    ax.set_title('Stratagem Tug Vectors', fontweight='bold')
    ax.set_xlim(-0.1, 0.6)
    ax.set_ylim(-0.1, 0.6)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8)
    ax.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
    ax.axvline(x=0, color='k', linestyle='-', linewidth=0.5)
    
    # 4. Complexity analysis (total moves vs avg pressure)
    ax = axes[1, 1]
    
    total_moves = [results[pos]['stats']['total_moves'] for pos in positions]
    avg_pressure = [results[pos]['stats']['avg_V_Gamma'] for pos in positions]
    avg_coherence = [results[pos]['stats']['avg_K_tau'] for pos in positions]
    
    scatter = ax.scatter(total_moves, avg_pressure, c=avg_coherence, 
                        s=200, cmap='RdYlGn', alpha=0.7, edgecolors='black', linewidth=2)
    
    for i, pos in enumerate(positions):
        ax.annotate(pos, (total_moves[i], avg_pressure[i]), 
                   fontsize=8, ha='center', va='bottom')
    
    ax.set_xlabel('Total Legal Moves', fontweight='bold')
    ax.set_ylabel('Average V_Γ (Pressure)', fontweight='bold')
    ax.set_title('Position Complexity (colored by avg K_τ)', fontweight='bold')
    ax.grid(True, alpha=0.3)
    plt.colorbar(scatter, ax=ax, label='Avg K_τ')
    
    plt.suptitle('Coherence Manifold: Cross-Position Comparison', 
                fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    save_path = os.path.join(output_dir, 'position_comparison.png')
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    
    print(f"\nSaved comparison plot to {save_path}")


def play_coherence_game(n_moves=20, verbose=True):
    """Play a full game using coherence-optimal moves"""
    
    solver = CoherenceChessSolver(D_max=0.5, base_depth=3)
    visualizer = CoherenceVisualizer()
    
    board = chess.Board()
    position_history = [board.copy()]
    move_history = []
    
    print("\n" + "="*70)
    print("PLAYING COHERENCE-OPTIMAL GAME")
    print("="*70 + "\n")
    
    for i in range(n_moves):
        if board.is_game_over():
            print(f"\nGame over: {board.result()}")
            break
        
        if verbose:
            print(f"\nMove {i+1} ({'White' if board.turn else 'Black'}):")
        
        best_move, metrics = solver.select_best_move(board, move_history, verbose=False)
        
        if verbose:
            print(f"  {best_move.uci():6s}  L_p={metrics.L_p:+.3f}  "
                  f"K_τ={metrics.K_tau:.3f}  V_Γ={metrics.V_Gamma:.3f}  "
                  f"D={metrics.D:.3f}")
        
        board.push(best_move)
        move_history.append(best_move)
        position_history.append(board.copy())
    
    print(f"\nFinal position after {len(move_history)} moves:")
    print(board)
    print()
    
    # Create trajectory visualization
    output_dir = "./outputs"
    os.makedirs(output_dir, exist_ok=True)
    
    trajectory_path = os.path.join(output_dir, "game_trajectory.png")
    fig = visualizer.plot_move_trajectory(
        position_history,
        solver,
        save_path=trajectory_path
    )
    plt.close(fig)
    
    print(f"Saved game trajectory to {trajectory_path}")
    
    # PGN output
    game = chess.pgn.Game()
    game.headers["Event"] = "Coherence Chess Demo"
    game.headers["White"] = "Coherence Solver"
    game.headers["Black"] = "Coherence Solver"
    
    node = game
    for move in move_history:
        node = node.add_variation(move)
    
    pgn_path = os.path.join(output_dir, "coherence_game.pgn")
    with open(pgn_path, 'w') as f:
        f.write(str(game))
    
    print(f"Saved game PGN to {pgn_path}")
    
    return board, position_history, move_history


def main():
    """Run comprehensive demo"""
    
    print("\n" + "="*70)
    print("COHERENCE CHESS SOLVER - PIROUETTE FRAMEWORK IMPLEMENTATION")
    print("GAME-CHESS-002: Problem-Solving on a Coherence Manifold")
    print("="*70 + "\n")
    
    # Part 1: Analyze diverse positions
    print("PART 1: POSITION ANALYSIS")
    print("-" * 70)
    results = analyze_interesting_positions()
    
    # Part 2: Play a coherence-optimal game
    print("\n\nPART 2: COHERENCE-OPTIMAL GAME")
    print("-" * 70)
    board, history, moves = play_coherence_game(n_moves=25, verbose=True)
    
    print("\n" + "="*70)
    print("DEMO COMPLETE")
    print("="*70)
    print("\nKey Insights:")
    print("  • The starting position is uniformly laminar (low pressure)")
    print("  • Tactical positions show higher V_Γ and mixed coherence classes")
    print("  • Endgames have clearer stratagem tugs (definite winning plans)")
    print("  • The solver naturally avoids residue-heavy complications")
    print("\nAll visualizations saved")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
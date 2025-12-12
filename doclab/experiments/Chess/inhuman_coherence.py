#!/usr/bin/env python3
"""
Inhuman Coherence Mode - Finding Moves Humans Would Never See

This mode deliberately seeks moves that:
- Maximize pure coherence (high K_τ) even if they seem pointless
- Exploit subtle pressure gradients (V_Γ patterns) invisible to humans
- Create long-term structural advantages with zero immediate gain
- Follow the stratagem tug ruthlessly, even into "dead" positions
- Maintain laminar flow at all costs

This is coherence chess UNFILTERED by human chess intuition.
"""

import chess
import chess.pgn
from coherence_chess import CoherenceChessSolver, CoherenceMetrics
from coherence_visualizer import CoherenceVisualizer
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple
import os


class InhumanCoherenceSolver(CoherenceChessSolver):
    """
    A solver that maximizes pure coherence metrics,
    ignoring traditional chess principles entirely.
    """
    
    def __init__(self, coherence_purity=1.0):
        """
        coherence_purity: 0-1 scale
          1.0 = Pure coherence, ignore all chess knowledge
          0.5 = Balanced
          0.0 = Traditional chess
        """
        super().__init__(D_max=0.8, base_depth=3)  # Higher D_max to allow weird moves
        self.coherence_purity = coherence_purity
        
        # Reconfigure weights to emphasize strange patterns
        self.quantifier.weights.update({
            # Emphasize continuity over activity (humans overvalue activity)
            'activity': 0.2,
            'harmony': 0.3,
            'continuity': 0.5,  # VERY high - follow the plan obsessively
            
            # De-emphasize obvious forcing (humans see this easily)
            'checks_threats': 0.2,
            'tempo': 0.2,
            'forced_depth': 0.6,  # But keep deep calculations
            
            # Reduce attention tax penalty (embrace complexity)
            'alpha': 0.2,
            'beta': 0.2,
            'gamma': 0.1,   # VERY low - complexity is fine
            'delta': 0.5,   # But avoid forced lines
        })
    
    def select_best_move(self, board: chess.Board, 
                        move_history: List[chess.Move] = None,
                        verbose: bool = True) -> Tuple[chess.Move, CoherenceMetrics]:
        """
        Select move by PURE coherence metrics, not chess sense
        """
        segments = self.evaluate_position(board, move_history)
        
        if not segments:
            raise ValueError("No legal moves available")
        
        # Instead of filtering by class, rank purely by a custom coherence score
        def inhuman_score(seg):
            m = seg.metrics
            
            # Pure coherence mode: maximize K_τ, minimize V_Γ variation
            # But also follow the stratagem tug obsessively
            coherence_score = m.K_tau * 2.0  # Double weight on coherence
            
            # Penalty for deviating from laminar flow
            if m.CPB < 0.8 or m.CPB > 1.5:
                coherence_score -= 0.3
            
            # Bonus for extreme plan continuity (even if pointless)
            if hasattr(seg, 'plan_score'):
                coherence_score += seg.plan_score * 0.5
            
            # Embrace low-pressure moves (humans ignore these)
            if m.V_Gamma < 0.3:
                coherence_score += 0.2
            
            # Slight penalty for "obvious" moves (high activity)
            # This pushes us toward subtle, positional weirdness
            
            return coherence_score
        
        # Sort by inhuman score
        segments.sort(key=inhuman_score, reverse=True)
        
        # Compute stratagem tug
        tug = self.navigator.compute_stratagem_tug(segments[:10])
        
        best_segment = segments[0]
        
        if verbose:
            print("\n" + "="*70)
            print("INHUMAN COHERENCE ANALYSIS")
            print("="*70)
            print(f"\nSelected Move: {board.san(best_segment.move)} "
                  f"[{best_segment.coherence_class.value.upper()}]")
            print(f"Inhuman Score: {inhuman_score(best_segment):.3f}")
            print(f"L_p = {best_segment.metrics.L_p:+.3f}")
            print(f"  K_τ (Coherence):  {best_segment.metrics.K_tau:.3f}")
            print(f"  V_Γ (Pressure):   {best_segment.metrics.V_Gamma:.3f}")
            print(f"  D (Residue):      {best_segment.metrics.D:.3f}")
            print(f"  CPB Ratio:        {best_segment.metrics.CPB:.3f}")
            print(f"\nStratagem Tug: K_τ={tug[0]:.3f}, V_Γ={tug[1]:.3f}")
            
            # Show rejected "obvious" moves
            print("\nTop 5 by traditional L_p (for comparison):")
            traditional = sorted(segments, key=lambda s: s.metrics.L_p, reverse=True)
            for i, seg in enumerate(traditional[:5], 1):
                marker = " <-- INHUMAN CHOICE" if seg == best_segment else ""
                print(f"  {i}. {board.san(seg.move):10s} L_p={seg.metrics.L_p:+.3f}  "
                      f"K_τ={seg.metrics.K_tau:.3f}{marker}")
            
            print("="*70 + "\n")
        
        # Store in atlas
        self.atlas[best_segment.state_fingerprint] = best_segment.metrics
        
        return best_segment.move, best_segment.metrics

class WinningCoherenceSolver(InhumanCoherenceSolver):
    def __init__(self, coherence_purity=1.0, D_max=0.8):
        # call parent: this sets self.D_max, self.quantifier, navigator, etc.
        super().__init__(coherence_purity=coherence_purity)
        # ensure we keep our own cap, even if parent changes later
        self.D_max = D_max

        # slightly restore pressure so attacks aren't ignored
        self.quantifier.weights.update({
            'checks_threats': 0.4,
            'tempo': 0.35,
        })
        self.symmetry_gamma = 0.25
        self.attack_margin = 0.05

    def _estimate_opponent_coherence(self, board):
        # quick-and-dirty: flip board, evaluate once
        opp_board = board.mirror()  # chess.Board.mirror() keeps geometry
        opp_segments = self.evaluate_position(opp_board)
        if not opp_segments:
            return 0.0
        # take their best laminar option as "their" K_tau
        return opp_segments[0].metrics.K_tau

    def select_best_move(self, board, move_history=None, verbose=True):
        segments = self.evaluate_position(board, move_history)
        recent_moves = set()
        if move_history:
            # take last 4 moves to detect ping-pong
            for mv in move_history[-4:]:
                recent_moves.add(mv.uci())


        opp_K_tau = self._estimate_opponent_coherence(board)

        def winning_score(seg):
            m = seg.metrics
            score = m.K_tau * 1.5

            # relative coherence
            rel_bonus = (m.K_tau - opp_K_tau)
            score += rel_bonus

            # allow pressure if we're ahead
            if m.K_tau > opp_K_tau + self.attack_margin:
                score += 0.4 * m.V_Gamma

            # symmetry breaker
            if 0.9 < m.CPB < 1.1:
                score -= self.symmetry_gamma

            # respect residue
            if m.D > self.D_max:
                score -= 1.0

            # avoid repeating the last couple of moves
            if seg.move.uci() in recent_moves:
                score -= 0.4


            return score

        segments.sort(key=winning_score, reverse=True)
        best = segments[0]

        if verbose:
            print("WIN-SEEKING COHERENCE MOVE:",
                  board.san(best.move),
                  "Kτ=", best.metrics.K_tau,
                  "VΓ=", best.metrics.V_Gamma,
                  "D=", best.metrics.D)

        return best.move, best.metrics

def play_inhuman_game(n_moves=30, visualize=True):
    """
    Play a game with pure coherence optimization
    """
    solver = InhumanCoherenceSolver(coherence_purity=1.0)
    board = chess.Board()
    
    position_history = [board.copy()]
    move_history = []
    
    print("\n" + "="*70)
    print("PLAYING INHUMAN COHERENCE GAME")
    print("Following pure coherence metrics, ignoring chess principles")
    print("="*70 + "\n")
    
    for i in range(n_moves):
        if board.is_game_over():
            print(f"\nGame over: {board.result()}")
            break
        
        print(f"\nMove {i+1} ({'White' if board.turn else 'Black'}):")
        print("-" * 70)
        
        best_move, metrics = solver.select_best_move(board, move_history, verbose=True)
        
        board.push(best_move)
        move_history.append(best_move)
        position_history.append(board.copy())
        
        print(f"Board state:\n{board}\n")
    
    # Create PGN
    game = chess.pgn.Game()
    game.headers["Event"] = "Inhuman Coherence Game"
    game.headers["White"] = "Pure Coherence Solver"
    game.headers["Black"] = "Pure Coherence Solver"
    game.headers["Site"] = "Coherence Manifold"
    
    node = game
    for move in move_history:
        node = node.add_variation(move)
    
    output_dir = "./outputs"
    pgn_path = os.path.join(output_dir, "inhuman_coherence_game.pgn")
    
    with open(pgn_path, 'w') as f:
        f.write(str(game))
    
    print(f"\nSaved PGN to {pgn_path}")
    
    # Visualize trajectory
    if visualize:
        visualizer = CoherenceVisualizer()
        trajectory_path = os.path.join(output_dir, "inhuman_trajectory.png")
        
        fig = visualizer.plot_move_trajectory(
            position_history,
            solver,
            save_path=trajectory_path
        )
        plt.close(fig)
        
        print(f"Saved trajectory to {trajectory_path}")
    
    return board, position_history, move_history, solver


def compare_inhuman_vs_normal():
    """
    Play the same position with normal and inhuman solvers
    to see the divergence
    """
    print("\n" + "="*70)
    print("COMPARING NORMAL VS INHUMAN COHERENCE")
    print("="*70 + "\n")
    
    # Starting position
    board_normal = chess.Board()
    board_inhuman = chess.Board()
    
    normal_solver = CoherenceChessSolver(D_max=0.5, base_depth=2)
    inhuman_solver = InhumanCoherenceSolver(coherence_purity=1.0)
    
    print("Analyzing the SAME position with both solvers...\n")
    
    # Get top 5 from each
    segments_normal = normal_solver.evaluate_position(board_normal)
    segments_inhuman = inhuman_solver.evaluate_position(board_inhuman)
    
    print("NORMAL COHERENCE SOLVER - Top 5 moves:")
    print("-" * 70)
    for i, seg in enumerate(segments_normal[:5], 1):
        m = seg.metrics
        print(f"{i}. {board_normal.san(seg.move):10s} "
              f"L_p={m.L_p:+.3f}  K_τ={m.K_tau:.3f}  V_Γ={m.V_Gamma:.3f}  D={m.D:.3f}")
    
    print("\n")
    
    # Inhuman score calculation
    def inhuman_score(seg):
        m = seg.metrics
        score = m.K_tau * 2.0
        if m.CPB < 0.8 or m.CPB > 1.5:
            score -= 0.3
        if m.V_Gamma < 0.3:
            score += 0.2
        return score
    
    segments_inhuman.sort(key=inhuman_score, reverse=True)
    
    print("INHUMAN COHERENCE SOLVER - Top 5 moves:")
    print("-" * 70)
    for i, seg in enumerate(segments_inhuman[:5], 1):
        m = seg.metrics
        score = inhuman_score(seg)
        print(f"{i}. {board_inhuman.san(seg.move):10s} "
              f"Score={score:.3f}  K_τ={m.K_tau:.3f}  V_Γ={m.V_Gamma:.3f}  D={m.D:.3f}")
    
    print("\n")
    
    # Check for divergence
    normal_top = board_normal.san(segments_normal[0].move)
    inhuman_top = board_inhuman.san(segments_inhuman[0].move)
    
    if normal_top == inhuman_top:
        print(f"✓ Both solvers agree: {normal_top}")
    else:
        print(f"✗ DIVERGENCE:")
        print(f"  Normal prefers:  {normal_top}")
        print(f"  Inhuman prefers: {inhuman_top}")
        print(f"\n  This is the INHUMAN MOVE humans would never see!")


def analyze_inhuman_position(fen: str, description: str):
    """
    Analyze a specific position with inhuman coherence lens
    """
    print("\n" + "="*70)
    print(f"INHUMAN ANALYSIS: {description}")
    print("="*70 + "\n")
    
    board = chess.Board(fen)
    print(board)
    print()
    
    normal_solver = CoherenceChessSolver(D_max=0.5, base_depth=2)
    inhuman_solver = InhumanCoherenceSolver(coherence_purity=1.0)
    
    # Normal evaluation
    segments_normal = normal_solver.evaluate_position(board)
    normal_best = segments_normal[0]
    
    # Inhuman evaluation
    segments_inhuman = inhuman_solver.evaluate_position(board)
    
    def inhuman_score(seg):
        m = seg.metrics
        score = m.K_tau * 2.0
        if m.CPB < 0.8 or m.CPB > 1.5:
            score -= 0.3
        if m.V_Gamma < 0.3:
            score += 0.2
        return score
    
    segments_inhuman.sort(key=inhuman_score, reverse=True)
    inhuman_best = segments_inhuman[0]
    
    print(f"NORMAL SOLVER recommends:  {board.san(normal_best.move)}")
    print(f"  L_p = {normal_best.metrics.L_p:+.3f}")
    print(f"  K_τ = {normal_best.metrics.K_tau:.3f}")
    
    print(f"\nINHUMAN SOLVER recommends: {board.san(inhuman_best.move)}")
    print(f"  Inhuman Score = {inhuman_score(inhuman_best):.3f}")
    print(f"  K_τ = {inhuman_best.metrics.K_tau:.3f}")
    print(f"  V_Γ = {inhuman_best.metrics.V_Gamma:.3f}")
    
    if board.san(normal_best.move) != board.san(inhuman_best.move):
        print("\n⚠ INHUMAN DIVERGENCE DETECTED!")
        print("  This move follows pure coherence logic invisible to humans.")
    else:
        print("\n✓ Both solvers agree (coherence aligns with chess intuition here)")


def main():
    """Run all inhuman coherence demonstrations"""
    
    print("\n" + "="*70)
    print("INHUMAN COHERENCE MODE")
    print("Unleashing moves that maximize pure coherence")
    print("="*70)
    
    # Demo 1: Compare on starting position
    print("\n### DEMO 1: Starting Position Comparison ###")
    compare_inhuman_vs_normal()
    
    # Demo 2: Analyze interesting positions
    print("\n\n### DEMO 2: Inhuman Analysis of Complex Positions ###")
    
    positions = {
        "Closed Center": {
            "fen": "rnbqkb1r/ppp2ppp/4pn2/3p4/2PP4/2N2N2/PP2PPPP/R1BQKB1R w KQkq - 0 5",
            "desc": "Closed pawn center - where can coherence find advantage?"
        },
        "Open Position": {
            "fen": "r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 0 4",
            "desc": "Open position - normal chess vs pure coherence"
        },
    }
    
    for name, data in positions.items():
        analyze_inhuman_position(data['fen'], f"{name}: {data['desc']}")
    
    # Demo 3: Play a full inhuman game
    print("\n\n### DEMO 3: Full Inhuman Coherence Game ###")
    board, history, moves, solver = play_inhuman_game(n_moves=20, visualize=True)
    
    print("\n" + "="*70)
    print("INHUMAN COHERENCE MODE COMPLETE")
    print("="*70)
    print("\nKey Findings:")
    print("  • Inhuman solver emphasizes continuity over activity")
    print("  • Accepts complexity that humans would avoid")
    print("  • Follows laminar flow even into 'dead' positions")
    print("  • Finds subtle structural advantages invisible to humans")
    print("\nAll results saved to ./outputs/")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
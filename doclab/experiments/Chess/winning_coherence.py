#!/usr/bin/env python3
"""
Winning Coherence Chess Solver
...
"""

import chess
import chess.pgn
import numpy as np
from coherence_chess import CoherenceChessSolver, CoherenceMetrics, PositionSegment, CoherenceClass
from typing import List, Tuple, Optional
import traceback


class WinningCoherenceSolver(CoherenceChessSolver):
    """
    A coherence solver that seeks WINNING coherent strategies,
    not just maximum coherence.
    """
    
    def __init__(self, D_max: float = 0.6, base_depth: int = 3):
        super().__init__(D_max=D_max, base_depth=base_depth)
        
        # Store D_max for access in scoring
        self.D_max = D_max
        
        # --- CHANGED: More aggressive winning parameters ---
        self.material_coherence_coupling = 1.5  # Material amplifies coherence value
        self.asymmetry_bonus = 1.0              # <--- Increased from 0.3
        self.progress_weight = 1.2              # <--- Increased from 0.4
        self.opponent_coherence_weight = 0.8    # Consider opponent's coherence
        self.repetition_penalty = 1.0           # <--- Increased from 0.6
        self.stagnation_penalty = 0.7           # <--- NEW: Penalty for drawish moves
        # --- END CHANGE ---
        
        # Adjust weights to balance coherence with winning
        self.quantifier.weights.update({
            # Keep some activity (for attacks)
            'activity': 0.35,
            'harmony': 0.30,
            'continuity': 0.35,  # Reduced from pure coherence mode
            
            # Increase pressure recognition (to create threats)
            'checks_threats': 0.45,
            'tempo': 0.30,
            'forced_depth': 0.25,
            
            # Moderate residue penalties (allow tactical complexity)
            'alpha': 0.25,   # square_exposure
            'beta': 0.25,    # structure_debt
            'gamma': 0.20,   # attention_tax (allow some complexity)
            'delta': 0.30,   # autonomy_loss
        })
        
        # <--- NEW: Cache for the expensive opponent coherence calculation
        self.opponent_coherence_cache = {}
        # <--- NEW: Mechanism to clear caches periodically
        self.moves_since_cache_clear = 0
    
    def _compute_material_balance(self, board: chess.Board) -> float:
        """
        Compute material balance from perspective of side to move.
        Returns value in range ~[-1, 1]
        """
        piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0
        }
        
        our_material = 0
        their_material = 0
        
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                value = piece_values.get(piece.piece_type, 0)
                if piece.color == board.turn:
                    our_material += value
                else:
                    their_material += value
        
        # Normalize to [-1, 1] range (max material ~39)
        balance = (our_material - their_material) / 39.0
        return balance
    
    def _compute_position_asymmetry(self, board: chess.Board) -> float:
        """
        Measure how asymmetric the position is.
        Higher values = more imbalanced position (good for winning chances)
        """
        # Pawn structure asymmetry
        white_pawns = board.pieces(chess.PAWN, chess.WHITE)
        black_pawns = board.pieces(chess.PAWN, chess.BLACK)
        
        white_pawn_files = set(chess.square_file(sq) for sq in white_pawns)
        black_pawn_files = set(chess.square_file(sq) for sq in black_pawns)
        
        file_asymmetry = len(white_pawn_files ^ black_pawn_files) / 8.0
        
        # Material asymmetry (different piece types)
        piece_types_diff = 0
        for piece_type in [chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN]:
            white_count = len(board.pieces(piece_type, chess.WHITE))
            black_count = len(board.pieces(piece_type, chess.BLACK))
            piece_types_diff += abs(white_count - black_count)
        
        type_asymmetry = piece_types_diff / 10.0  # Normalize
        
        return (file_asymmetry + type_asymmetry) / 2.0
    
    def _compute_progress_score(self, board: chess.Board, move: chess.Move) -> float:
        """
        Measure forward progress: development, space control, king safety improvement
        """
        board_copy = board.copy()
        
        # Score before move
        score_before = self._position_score(board_copy)
        
        # Score after move
        board_copy.push(move)
        score_after = self._position_score(board_copy)
        
        return score_after - score_before
    
    def _position_score(self, board: chess.Board) -> float:
        """Quick heuristic position evaluation"""
        score = 0.0
        
        # Piece mobility
        mobility = len(list(board.legal_moves)) / 40.0
        score += mobility * 0.3
        
        # Center control
        center_squares = [chess.D4, chess.E4, chess.D5, chess.E5]
        for sq in center_squares:
            if board.is_attacked_by(board.turn, sq):
                score += 0.1
        
        # Development (pieces off back rank)
        back_rank = 0 if board.turn == chess.WHITE else 7
        developed = 0
        for sq in chess.SQUARES:
            piece = board.piece_at(sq)
            if piece and piece.color == board.turn:
                if chess.square_rank(sq) != back_rank or piece.piece_type == chess.PAWN:
                    developed += 1
        score += developed / 16.0
        
        return score
    
    # <--- CRITICAL BUG FIX HERE ---
    def _estimate_opponent_coherence(self, board: chess.Board) -> float:
        """
        Estimate opponent's best coherence from their perspective
        The 'board' passed in is *already* set to the opponent's turn.
        """
        
        # <--- NEW: Use the cache ---
        # Use FEN as the cache key (only board state, not move counts)
        board_fen = board.fen().split(' ')[0]
        if board_fen in self.opponent_coherence_cache:
            return self.opponent_coherence_cache[board_fen]
        # --- END NEW ---

        # Board is already opponent's turn, so copy it
        opponent_board = board.copy()

        try:
            move_history = list(opponent_board.move_stack)
            opponent_segments = self.evaluate_position(opponent_board, move_history)
            
            if opponent_segments:
                # Take their best K_tau
                best_opp_k_tau = opponent_segments[0].metrics.K_tau
                # <--- NEW: Store in cache
                self.opponent_coherence_cache[board_fen] = best_opp_k_tau
                return best_opp_k_tau
        except Exception as e:
            print("\n" + "="*50)
            print(f"!!! CRITICAL ERROR in _estimate_opponent_coherence:")
            print(f"!!! Board FEN: {opponent_board.fen()}")
            traceback.print_exc() 
            print("="*50 + "\n")
            pass
        
        # <--- NEW: Cache the default value too
        self.opponent_coherence_cache[board_fen] = 0.5
        return 0.5  # Default neutral
    # <--- END FIX ---
    
    def _is_repetition(self, board: chess.Board, move: chess.Move) -> bool:
        """Check if move leads to position repetition"""
        test_board = board.copy()
        test_board.push(move)
        return test_board.is_repetition(count=2)
    
    # <--- UPDATED SCORING LOGIC HERE ---
    def winning_score(self, segment: PositionSegment, board: chess.Board, 
                     move_history: Optional[List[chess.Move]] = None) -> float:
        """
        Compute a score that balances coherence with winning potential
        
        Formula:
        score = (base_coherence * material_factor) + asymmetry + progress + 
                coherence_advantage - stagnation - repetition - residue
        """
        m = segment.metrics
        
        # Base coherence score (K_tau is still important!)
        base_coherence = m.K_tau
        
        # Material factor: winning material amplifies coherence value
        material_balance = self._compute_material_balance(board)
        if material_balance > 0:
            material_factor = 1.0 + (material_balance * self.material_coherence_coupling)
        else:
            material_factor = 1.0 + (material_balance * 0.5)  # Less penalty for being down
        
        # --- CHANGED: Asymmetry and Progress calculation ---
        
        # Push the move to analyze the resulting position
        board.push(segment.move)
        asymmetry = self._compute_position_asymmetry(board)
        # We must pop *before* estimating opponent coherence
        board.pop() 
        
        asymmetry_score = asymmetry * self.asymmetry_bonus
        
        # Progress: reward moves that improve position
        progress = self._compute_progress_score(board, segment.move)
        progress_score = progress * self.progress_weight
        
        # Coherence advantage: be MORE coherent than opponent
        # Push move again for opponent estimation
        board.push(segment.move)
        opp_coherence = self._estimate_opponent_coherence(board)
        board.pop()
        
        coherence_advantage = (m.K_tau - opp_coherence) * self.opponent_coherence_weight
        # --- END CHANGE ---
        
        # Pressure component: use V_Gamma when ahead or equal
        pressure_score = 0.0
        if material_balance >= -0.1:  # Not significantly behind
            pressure_score = m.V_Gamma * 0.4
        
        # Repetition penalty
        repetition_malus = 0.0
        if self._is_repetition(board, segment.move):
            repetition_malus = self.repetition_penalty
        
        # Residue penalty (keep some coherence discipline)
        residue_malus = 0.0
        if m.D > self.D_max:
            residue_malus = (m.D - self.D_max) * 2.0
            
        # --- NEW: Stagnation Penalty ---
        # Punish moves that are "stably coherent" but do nothing
        stagnation_malus = 0.0
        # A move is stagnant if it makes no progress, creates no asymmetry,
        # and we aren't already winning.
        is_stagnant = (progress_score < 0.01 and 
                       asymmetry_score < 0.01 and 
                       material_balance < 0.1)
                       
        if is_stagnant and m.K_tau > 0.6: # High coherence but no progress
            # Penalize based on how coherent the "boring" move is
            stagnation_malus = (m.K_tau * self.stagnation_penalty)
        # --- END NEW ---
        
        # Final score
        score = (base_coherence * material_factor + 
                asymmetry_score + 
                progress_score + 
                coherence_advantage +
                pressure_score - 
                repetition_malus -
                residue_malus -
                stagnation_malus) # <--- Added stagnation
        
        return score
    # <--- END UPDATED SCORING ---
    
    def select_best_move(self, board: chess.Board, 
                        move_history: Optional[List[chess.Move]] = None,
                        verbose: bool = True) -> Tuple[chess.Move, CoherenceMetrics]:
        """
        Select move that maximizes winning coherence score
        """
        
        # --- (All your existing logic to find the best move) ---
        segments = self.evaluate_position(board, move_history)
        
        if not segments:
            raise ValueError("No legal moves available")
        
        scored_segments = [
            (seg, self.winning_score(seg, board, move_history))
            for seg in segments
        ]
        
        scored_segments.sort(key=lambda x: x[1], reverse=True)
        
        best_segment, best_score = scored_segments[0]
        
        if verbose:
            self._print_winning_analysis(best_segment, best_score, 
                                        scored_segments, board)
        
        # Store in atlas
        self.atlas[best_segment.state_fingerprint] = best_segment.metrics
        
        # <--- NEW: Cache clearing mechanism ---
        self.moves_since_cache_clear += 1
        # Clear caches every 10 *full moves* (20 half-moves)
        # to prevent memory overruns, as requested.
        if self.moves_since_cache_clear >= 20:
            print("\n" + "-"*70)
            print(f"CACHE: Clearing caches (Atlas: {len(self.atlas)}, Opponent: {len(self.opponent_coherence_cache)})")
            print("-"*70 + "\n")
            self.atlas = {}
            self.opponent_coherence_cache = {}
            self.moves_since_cache_clear = 0
        # --- END NEW ---

        return best_segment.move, best_segment.metrics
    
    def _print_winning_analysis(self, best: PositionSegment, best_score: float,
                               scored_segments: List[Tuple[PositionSegment, float]],
                               board: chess.Board):
        """Print analysis focusing on winning elements"""
        print("\n" + "="*70)
        print("WINNING COHERENCE ANALYSIS")
        print("="*70)
        
        m = best.metrics
        material = self._compute_material_balance(board)
        
        print(f"\nSelected Move: {board.san(best.move)} [{best.coherence_class.value.upper()}]")
        print(f"Winning Score: {best_score:.3f}")
        print(f"\nCoherence Metrics:")
        print(f"  K_τ (Coherence):  {m.K_tau:.3f}")
        print(f"  V_Γ (Pressure):   {m.V_Gamma:.3f}")
        print(f"  D (Residue):      {m.D:.3f}")
        print(f"  L_p (Lagrangian): {m.L_p:+.3f}")
        
        print(f"\nWinning Factors:")
        print(f"  Material Balance: {material:+.3f}")
        
        board.push(best.move)
        asymmetry = self._compute_position_asymmetry(board)
        board.pop()
        print(f"  Position Asymmetry: {asymmetry:.3f}")
        
        print(f"\nTop 5 Moves by Winning Score:")
        print("-" * 70)
        for i, (seg, score) in enumerate(scored_segments[:5], 1):
            print(f"{i}. {board.san(seg.move):8s}  Score: {score:+.3f}  "
                  f"K_τ: {seg.metrics.K_tau:.3f}  V_Γ: {seg.metrics.V_Gamma:.3f}")
        
        print("="*70 + "\n")


def demo():
    """Demonstrate the winning coherence solver"""
    print("\n" + "="*70)
    print("WINNING COHERENCE CHESS SOLVER")
    print("Finding coherent paths to victory, not just maximum coherence")
    print("="*70 + "\n")
    
    solver = WinningCoherenceSolver(D_max=0.6, base_depth=3)
    board = chess.Board()
    
    # <--- CHANGED: Run for 40 half-moves to test cache clearing
    for i in range(40): 
        if board.is_game_over():
            print("Game over.")
            break
        
        print(f"\nMove {i+1} ({'White' if board.turn else 'Black'}):")
        print("-" * 70)
        
        try:
            best_move, metrics = solver.select_best_move(board, list(board.move_stack), verbose=True)
            
            board.push(best_move)
            
            print(f"\nBoard after move:")
            print(board)
            print()
        except Exception as e:
            # Fixed the typo in the error print
            print("\n" + "!"*70)
            print(f"!!! FATAL ERROR during move {i+1} analysis:")
            print(f"!!! Board FEN: {board.fen()}")
            traceback.print_exc()
            print("!"*70 + "\n")
            break


if __name__ == "__main__":
    demo()
#!/usr/bin/env python3
"""
Coherence Chess Solver - GAME-CHESS-002 Implementation

A chess engine that evaluates positions through the lens of the Pirouette 
Lagrangian: L_p = K_τ - V_Γ, constrained by dark residue budget.

This is a RUTHLESS implementation - we optimize for coherence victory,
not human playability.
"""

import chess
import chess.pgn
import numpy as np
from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional
from enum import Enum
import math


class CoherenceClass(Enum):
    """The four canonical coherence classes for moves"""
    LAMINAR_PRESERVING = "laminar"          # High K_τ, low/mid V_Γ, low D
    CONSTRUCTIVE_FORCING = "constructive"   # Mid+ K_τ, high V_Γ, controlled D
    OPPORTUNISTIC_TURBULENT = "turbulent"   # Low/mid K_τ, very high V_Γ, controlled D
    RESIDUE_HEAVY = "reject"                # High D or (low K_τ and low V_Γ)


@dataclass
class CoherenceMetrics:
    """The fundamental metrics of a position segment"""
    K_tau: float        # Temporal Coherence (plan coherence)
    V_Gamma: float      # Temporal Pressure (forcing nature)
    D: float            # Dark Residue (unintended cost)
    
    @property
    def L_p(self) -> float:
        """The Pirouette Lagrangian"""
        return self.K_tau - self.V_Gamma
    
    @property
    def CPB(self) -> float:
        """Coherence-Pressure Balance (K_τ / V_Γ)"""
        return self.K_tau / max(self.V_Gamma, 0.01)


@dataclass
class PositionSegment:
    """A position + candidate move + reply window"""
    board: chess.Board
    move: chess.Move
    intent_context: Optional[str] = None
    reply_depth: int = 2
    
    # Computed metrics
    metrics: Optional[CoherenceMetrics] = None
    coherence_class: Optional[CoherenceClass] = None
    
    # For manifold tracking
    state_fingerprint: Optional[str] = None


class CoherenceQuantifier:
    """
    Sublayer A: Domain Quantifier
    Converts chess positions into (K_τ, V_Γ, D) metrics
    """
    
    def __init__(self):
        # Empirical weights - these will be tuned by the autopoietic loop
        self.weights = {
            # K_tau components
            'activity': 0.4,
            'harmony': 0.3,
            'continuity': 0.3,
            
            # V_Gamma components
            'checks_threats': 0.4,
            'tempo': 0.3,
            'forced_depth': 0.3,
            
            # Dark Residue components
            'alpha': 0.25,  # square_exposure
            'beta': 0.25,   # structure_debt
            'gamma': 0.30,  # attention_tax
            'delta': 0.20,  # autonomy_loss
        }
        
        self.depth_norm = 10.0  # Normalization for forced variation depth
    
    def compute_K_tau(self, board: chess.Board, move: chess.Move, 
                      prev_position: Optional[chess.Board] = None) -> float:
        """
        Temporal Coherence = piece_activity + structural_harmony + plan_continuity
        Range: [0, 1]
        """
        board.push(move)
        
        activity = self._piece_activity_score(board)
        harmony = self._structural_harmony_score(board)
        continuity = self._plan_continuity_score(board, prev_position) if prev_position else 0.5
        
        board.pop()
        
        K_tau = (
            self.weights['activity'] * activity +
            self.weights['harmony'] * harmony +
            self.weights['continuity'] * continuity
        )
        
        return K_tau
    
    def compute_V_Gamma(self, board: chess.Board, move: chess.Move, 
                        reply_depth: int = 2) -> float:
        """
        Temporal Pressure = checks_threats + tempo_race + forced_variation_depth
        Range: [0, 1+]
        """
        board.push(move)
        
        checks_threats = self._checks_and_threats_score(board)
        tempo = self._tempo_race_factor(board)
        forced_depth = self._forced_variation_depth(board, reply_depth) / self.depth_norm
        
        board.pop()
        
        V_Gamma = (
            self.weights['checks_threats'] * checks_threats +
            self.weights['tempo'] * tempo +
            self.weights['forced_depth'] * forced_depth
        )
        
        return V_Gamma
    
    def compute_D(self, board: chess.Board, move: chess.Move) -> float:
        """
        Dark Residue = α·square_exposure + β·structure_debt + 
                       γ·attention_tax + δ·autonomy_loss
        Range: [0, 1+]
        """
        board_before = board.copy()
        board_after = board.copy()
        board_after.push(move)
        
        exposure = self._square_exposure(board_before, board_after)
        structure = self._structure_debt(board_before, board_after)
        attention = self._attention_tax(board_before, board_after, move)
        autonomy = self._autonomy_loss(board_after)
        
        D = (
            self.weights['alpha'] * exposure +
            self.weights['beta'] * structure +
            self.weights['gamma'] * attention +
            self.weights['delta'] * autonomy
        )
        
        return D
    
    # ============= K_tau Components =============
    
    def _piece_activity_score(self, board: chess.Board) -> float:
        """
        Computes a normalized piece activity score based on mobility.
        
        <--- CHANGED: This version uses board.attacks() instead of 
        board.legal_moves to avoid re-entrancy bugs and improve performance.
        """
        score = 0.0
        total_pieces = 0
        
        # Define relative weights for mobility
        # (e.g., knight/bishop mobility is more valuable)
        mobility_weights = {
            chess.PAWN: 0.5,
            chess.KNIGHT: 1.0,
            chess.BISHOP: 1.0,
            chess.ROOK: 0.5,
            chess.QUEEN: 0.25,
            chess.KING: 0.1  # King activity/safety
        }
        
        # Iterate over all piece types
        for piece_type in mobility_weights.keys():
            # Get a bitboard of all our pieces of this type
            our_pieces = board.pieces(piece_type, board.turn)
            
            # Iterate through each piece's square
            for square in chess.scan_reversed(int(our_pieces)):
                # Get a bitmask of all squares this piece *attacks*
                # This does NOT generate legal moves and is safe.
                attack_mask = board.attacks(square)
                
                # Count the number of bits (squares) in the mask
                # This is a fast way to get the number of attacked squares
                mobility = bin(attack_mask).count('1')
                
                # Apply weights
                score += mobility * mobility_weights[piece_type]
                total_pieces += 1
        
        if total_pieces == 0:
            return 0.0
        
        # Normalize the score
        # A rough normalization: avg 8 squares * 1.0 weight
        return score / (total_pieces * 8.0)
    
    def _structural_harmony_score(self, board: chess.Board) -> float:
        """
        Measures how well pieces (Knights/Bishops) are supported
        by the pawn structure.
        """
        harmony = 0.0
        piece_count = 0
        
        # <--- FIX: Initialize pawns to an empty set
        pawns = chess.SquareSet()
        
        for piece_type in [chess.KNIGHT, chess.BISHOP, chess.PAWN]:
            pieces = board.pieces(piece_type, board.turn)
            if piece_type == chess.PAWN:
                pawns = pieces
                continue
            
            for square in pieces:
                piece_count += 1
                # Get neighboring squares
                neighbors = [
                    square + 7, square + 9,  # Diagonal forward
                    square - 7, square - 9   # Diagonal back
                ]
                
                # Check if any neighboring square has one of our pawns
                if any(n in pawns for n in neighbors if 0 <= n < 64):
                    harmony += 1.0

        if piece_count == 0:
            return 0.5  # Neutral score if no minor pieces
        
        return harmony / piece_count
    
    def _plan_continuity_score(self, board: chess.Board, 
                               prev_board: Optional[chess.Board]) -> float:
        """
        Measure whether we're still pursuing the same strategic goals
        """
        if not prev_board:
            return 0.5
        
        # Simple heuristic: are we still targeting the same weaknesses?
        # For now, check if piece activity patterns are similar
        
        curr_attacked = self._get_attacked_squares(board)
        prev_attacked = self._get_attacked_squares(prev_board)
        
        overlap = len(curr_attacked & prev_attacked)
        union = len(curr_attacked | prev_attacked)
        
        if union == 0:
            return 0.5
        
        return overlap / union
    
    # ============= V_Gamma Components =============
    
    def _checks_and_threats_score(self, board: chess.Board) -> float:
        """
        Count checks, captures available, hanging pieces
        """
        score = 0.0
        
        # Check
        if board.is_check():
            score += 0.4
        
        # Available captures (for opponent now)
        captures = [m for m in board.legal_moves if board.is_capture(m)]
        score += len(captures) / 20.0  # Normalize
        
        # Hanging pieces
        hanging = self._count_hanging_pieces(board)
        score += hanging / 16.0
        
        return min(score, 1.0)
    
    def _tempo_race_factor(self, board: chess.Board) -> float:
        """
        Detect tempo races: passed pawns, opposite-side castling attacks
        """
        score = 0.0
        
        # Passed pawns
        passed = self._count_passed_pawns(board)
        score += passed / 8.0
        
        # Development lead (pieces off back rank)
        developed = sum(1 for sq in chess.SQUARES 
                       if board.piece_at(sq) and 
                          board.piece_at(sq).color == board.turn and
                          chess.square_rank(sq) not in [0, 7])
        score += developed / 16.0
        
        return min(score, 1.0)
    
    def _forced_variation_depth(self, board: chess.Board, max_depth: int) -> int:
        """
        Recursively find the depth of the *most forcing* variation.
        """
        if max_depth <= 0:
            return 0
        
        # <--- FIX: Materialize the list to prevent re-entrancy
        legal_moves_list = list(board.legal_moves)

        forcing_moves = [
            m for m in legal_moves_list # <--- Use the new list
            if board.is_capture(m) or board.gives_check(m)
        ]

        if not forcing_moves:
            return 0  # No forcing moves, depth is 0

        # Find the *deepest* forced line
        max_reply_depth = 0
        for move in forcing_moves:
            board.push(move)
            # Recursively find the opponent's *counter-forcing* moves
            reply_depth = self._forced_variation_depth(board, max_depth - 1)
            board.pop()
            max_reply_depth = max(max_reply_depth, reply_depth)

        return 1 + max_reply_depth
    
    # ============= Dark Residue Components =============
    
    def _square_exposure(self, board_before: chess.Board, 
                        board_after: chess.Board) -> float:
        """
        New weak squares created by this move
        """
        before_weak = self._count_weak_squares(board_before)
        after_weak = self._count_weak_squares(board_after)
        
        new_weaknesses = max(0, after_weak - before_weak)
        return new_weaknesses / 8.0  # Normalize
    
    def _structure_debt(self, board_before: chess.Board, 
                       board_after: chess.Board) -> float:
        """
        Long-term pawn weaknesses introduced
        """
        # Count doubled, isolated, backward pawns
        before_issues = self._pawn_structure_issues(board_before)
        after_issues = self._pawn_structure_issues(board_after)
        
        new_issues = max(0, after_issues - before_issues)
        return new_issues / 8.0
    
    def _attention_tax(self, board_before: chess.Board, board_after: chess.Board, move: chess.Move) -> float:
        """
        Calculates the 'tax' of a move based on how much new,
        urgent, or complex information it introduces (blunders, pins).
        """
        tax = 0.0

        # 1. Tactical Blunder (Losing material)
        if board_after.is_capture(move):
            # Check for simple undefended captures
            if not board_before.is_attacked_by(board_before.turn, move.to_square):
                pass # This is a good capture
            else:
                # This is an exchange, check material
                # This logic is complex, skip for now.
                pass
        
        # Check if the moved piece is now hanging
        if not board_after.is_attacked_by(board_after.turn, move.to_square):
            # Moved to an undefended square. Is it attacked by opponent?
            if board_after.is_attacked_by(not board_after.turn, move.to_square):
                tax += self.weights['gamma'] * 1.0 # Hanging piece

        # <--- FIX: This block is also removed.
        # It was another source of re-entrancy and was not defined.
        # revealed_attackers = self._get_revealed_attackers(board_before, move)
        # if revealed_attackers:
        #    tax += self.weights['gamma'] * 0.3 * len(revealed_attackers)
        # <--- END FIX

        return tax
    
    def _autonomy_loss(self, board: chess.Board) -> float:
        """
        Calculates the loss of 'choice' (autonomy) by seeing
        how many moves are forcing.
        """
        # <--- FIX: Materialize the list to prevent re-entrancy
        legal_moves_list = list(board.legal_moves)
        
        if not legal_moves_list:
            return 0.0

        forcing_replies = [
            m for m in legal_moves_list # <--- Use the new list
            if board.is_capture(m) or board.gives_check(m)
        ]
        
        # If a high % of our moves are just forced reactions, autonomy is low.
        autonomy_loss = len(forcing_replies) / len(legal_moves_list)
        
        # Additional penalty: if *all* moves are (almost) forcing,
        # it's a very constrained position.
        if len(forcing_replies) >= len(legal_moves_list) * 0.8: # <--- Use the new list
            return 1.0
        
        return autonomy_loss
    
    # ============= Helper Methods =============
    
    def _material_balance(self, board: chess.Board) -> float:
        """Material advantage for side to move (-1 to 1)"""
        values = {
            chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3,
            chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 0
        }
        
        balance = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                value = values[piece.piece_type]
                balance += value if piece.color == board.turn else -value
        
        return balance / 39.0  # Normalize by max material
    
    def _get_attacked_squares(self, board: chess.Board) -> set:
        """Get all squares attacked by side to move"""
        attacked = set()
        for move in board.legal_moves:
            attacked.add(move.to_square)
        return attacked
    
    def _count_hanging_pieces(self, board: chess.Board) -> int:
        """Count undefended pieces for the opponent (defensive version)."""
        hanging = 0

        # be robust if chess.SQUARES got shadowed somehow
        squares = getattr(chess, "SQUARES", None)
        if squares is None or not hasattr(squares, "__iter__"):
            squares = range(64)

        for square in squares:
            piece = board.piece_at(square)
            if not piece:
                continue
            # only look at opponent pieces
            if piece.color == board.turn:
                continue
            # if that square is not defended by its own color, it's hanging
            if not board.is_attacked_by(piece.color, square):
                hanging += 1

        return hanging

    
    def _count_passed_pawns(self, board: chess.Board) -> int:
        """Count passed pawns for side to move"""
        passed = 0
        pawns = board.pieces(chess.PAWN, board.turn)
        
        for sq in pawns:
            file = chess.square_file(sq)
            rank = chess.square_rank(sq)
            
            # Check if any enemy pawns block this pawn
            is_passed = True
            for enemy_sq in board.pieces(chess.PAWN, not board.turn):
                enemy_file = chess.square_file(enemy_sq)
                enemy_rank = chess.square_rank(enemy_sq)
                
                if abs(enemy_file - file) <= 1:
                    if board.turn == chess.WHITE and enemy_rank > rank:
                        is_passed = False
                    elif board.turn == chess.BLACK and enemy_rank < rank:
                        is_passed = False
            
            if is_passed:
                passed += 1
        
        return passed
    
    def _count_weak_squares(self, board: chess.Board) -> int:
        """Count squares around king that are weak"""
        king_sq = board.king(board.turn)
        if not king_sq:
            return 0
        
        weak = 0
        for delta in [-9, -8, -7, -1, 1, 7, 8, 9]:
            sq = king_sq + delta
            if 0 <= sq < 64:
                if not board.is_attacked_by(board.turn, sq):
                    weak += 1
        
        return weak
    
    def _pawn_structure_issues(self, board: chess.Board) -> int:
        """Count doubled, isolated, backward pawns"""
        issues = 0
        pawns = board.pieces(chess.PAWN, board.turn)
        
        for sq in pawns:
            file = chess.square_file(sq)
            
            # Doubled pawns
            same_file = [p for p in pawns if chess.square_file(p) == file]
            if len(same_file) > 1:
                issues += 1
            
            # Isolated pawns (no friendly pawns on adjacent files)
            adjacent_files = [file - 1, file + 1]
            has_neighbor = any(
                chess.square_file(p) in adjacent_files for p in pawns
            )
            if not has_neighbor:
                issues += 1
        
        return issues
    
    def _creates_pin(self, board_before: chess.Board, board_after: chess.Board,
                     move: chess.Move) -> bool:
        """
        Check if a move creates a new pin that wasn't there before.
        """
        
        # <--- FIX: Replaced the generator with a simple 'for' loop
        # This completely avoids the Python 'cell' closure bug
        # that was corrupting the board object's internal state.

        pins_before = 0
        # Use a clean local variable for the board
        board_b = board_before
        for sq in chess.SQUARES:
            piece = board_b.piece_at(sq)
            # Check for opponent's pieces
            if piece and piece.color != board_b.turn:
                if board_b.is_pinned(sq, piece.color):
                    pins_before += 1
        
        pins_after = 0
        # Use a clean local variable for the board
        board_a = board_after
        for sq in chess.SQUARES:
            piece = board_a.piece_at(sq)
            # Check for opponent's pieces
            if piece and piece.color != board_a.turn:
                if board_a.is_pinned(sq, piece.color):
                    pins_after += 1
        
        return pins_after > pins_before
    
    def _creates_discovered_attack(self, board_before: chess.Board, board_after: chess.Board, move: chess.Move) -> bool:
        """Check if move creates discovered attack"""
        # Simplified heuristic: check if we're revealing an attack line
        # by moving a piece away from between attacker and target
        return False  # TODO: implement properly
    
    def _piece_value(self, piece: Optional[chess.Piece]) -> int:
        """Standard piece values"""
        if not piece:
            return 0
        values = {
            chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3,
            chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 100
        }
        return values[piece.piece_type]


class ManifoldNavigator:
    """
    Sublayer B: Manifold Navigator
    Groups moves by coherence class and computes stratagem tug
    """
    
    def __init__(self, D_max: float = 0.5):
        self.D_max = D_max  # Dark residue budget
    
    def classify_move(self, metrics: CoherenceMetrics) -> CoherenceClass:
        """
        Assign move to one of four coherence classes
        """
        K = metrics.K_tau
        V = metrics.V_Gamma
        D = metrics.D
        
        # Reject immediately if over budget
        if D > self.D_max:
            return CoherenceClass.RESIDUE_HEAVY
        
        # Laminar-Preserving: High K_τ, low/mid V_Γ, low D
        if K > 0.6 and V < 0.5 and D < 0.3:
            return CoherenceClass.LAMINAR_PRESERVING
        
        # Constructive-Forcing: Mid+ K_τ, high V_Γ, controlled D
        if K >= 0.4 and V > 0.6 and D <= self.D_max:
            return CoherenceClass.CONSTRUCTIVE_FORCING
        
        # Opportunistic-Turbulent: Low/mid K_τ, very high V_Γ, controlled D
        if V > 0.7 and D <= self.D_max:
            return CoherenceClass.OPPORTUNISTIC_TURBULENT
        
        # Otherwise: Residue-Heavy or weak
        if K < 0.3 and V < 0.3:
            return CoherenceClass.RESIDUE_HEAVY
        
        # Default to laminar if uncertain
        return CoherenceClass.LAMINAR_PRESERVING
    
    def compute_stratagem_tug(self, segments: List[PositionSegment]) -> np.ndarray:
        """
        Compute the weighted gradient of L_p across all moves
        Returns a vector indicating strategic direction
        """
        if not segments:
            return np.zeros(2)
        
        # Weight by L_p value
        tug = np.zeros(2)
        total_weight = 0.0
        
        for seg in segments:
            if seg.metrics:
                weight = max(seg.metrics.L_p, 0.01)
                
                # Project into 2D strategy space: (K_tau axis, V_Gamma axis)
                direction = np.array([seg.metrics.K_tau, seg.metrics.V_Gamma])
                tug += weight * direction
                total_weight += weight
        
        if total_weight > 0:
            tug /= total_weight
        
        return tug
    
    def should_expand_depth(self, metrics: CoherenceMetrics, 
                           current_depth: int, max_depth: int = 10) -> bool:
        """
        Coherence-triggered depth escalation
        """
        if current_depth >= max_depth:
            return False
        
        # Escalate if entering temporal forge (high V_Γ) with manageable CPB
        if metrics.V_Gamma > 0.7 and 0.8 <= metrics.CPB <= 1.5:
            if metrics.D < self.D_max * 0.8:  # Still have residue budget
                return True
        
        return False


class CoherenceChessSolver:
    """
    Main solver: orchestrates quantification and navigation
    """
    
    def __init__(self, D_max: float = 0.5, base_depth: int = 2):
        self.quantifier = CoherenceQuantifier()
        self.navigator = ManifoldNavigator(D_max=D_max)
        self.base_depth = base_depth
        
        # Atlas for tracking coherence profiles
        self.atlas: Dict[str, CoherenceMetrics] = {}
    
    def evaluate_position(self, board: chess.Board, 
                         move_history: Optional[List[chess.Move]] = None) -> List[PositionSegment]:
        """
        Evaluate all legal moves from current position
        Returns sorted list of position segments
        """
        segments = []
        prev_board = self._get_previous_board(board, move_history)
        
        for move in board.legal_moves:
            # Create position segment
            segment = PositionSegment(
                board=board.copy(),
                move=move,
                reply_depth=self.base_depth
            )
            
            # Compute metrics
            K_tau = self.quantifier.compute_K_tau(board, move, prev_board)
            V_Gamma = self.quantifier.compute_V_Gamma(board, move, self.base_depth)
            D = self.quantifier.compute_D(board, move)
            
            segment.metrics = CoherenceMetrics(K_tau, V_Gamma, D)
            segment.coherence_class = self.navigator.classify_move(segment.metrics)
            
            # State fingerprint for atlas
            segment.state_fingerprint = self._fingerprint(board, move)
            
            segments.append(segment)
        
        # Sort by L_p (descending)
        segments.sort(key=lambda s: s.metrics.L_p, reverse=True)
        
        return segments
    
    def select_best_move(self, board: chess.Board, 
                        move_history: Optional[List[chess.Move]] = None,
                        verbose: bool = True) -> Tuple[chess.Move, CoherenceMetrics]:
        """
        Select the best move according to coherence principles
        Returns (move, metrics)
        """
        segments = self.evaluate_position(board, move_history)
        
        if not segments:
            raise ValueError("No legal moves available")
        
        # Filter out residue-heavy moves
        viable_segments = [
            s for s in segments 
            if s.coherence_class != CoherenceClass.RESIDUE_HEAVY
        ]
        
        if not viable_segments:
            # All moves are residue-heavy, pick least bad
            viable_segments = segments
        
        # Compute stratagem tug
        tug = self.navigator.compute_stratagem_tug(viable_segments)
        
        # Select move with highest L_p from viable set
        best_segment = viable_segments[0]
        
        if verbose:
            self._print_analysis(best_segment, segments, tug)
        
        # Store in atlas
        self.atlas[best_segment.state_fingerprint] = best_segment.metrics
        
        return best_segment.move, best_segment.metrics
    
    def analyze_position(self, board: chess.Board, 
                        move_history: Optional[List[chess.Move]] = None,
                        top_n: int = 5) -> str:
        """
        Detailed coherence analysis of position
        """
        segments = self.evaluate_position(board, move_history)
        tug = self.navigator.compute_stratagem_tug(segments[:top_n])
        
        lines = []
        lines.append("=" * 60)
        lines.append("COHERENCE MANIFOLD ANALYSIS")
        lines.append("=" * 60)
        lines.append(f"\nPosition: {board.fen()}")
        lines.append(f"Stratagem Tug: K_τ={tug[0]:.3f}, V_Γ={tug[1]:.3f}")
        lines.append(f"\nTop {top_n} Moves (by L_p):")
        lines.append("-" * 60)
        
        for i, seg in enumerate(segments[:top_n], 1):
            m = seg.metrics
            lines.append(f"\n{i}. {seg.move.uci():6s} [{seg.coherence_class.value.upper()}]")
            lines.append(f"   L_p = {m.L_p:+.3f} = K_τ({m.K_tau:.3f}) - V_Γ({m.V_Gamma:.3f})")
            lines.append(f"   Dark Residue: {m.D:.3f}")
            lines.append(f"   CPB Ratio: {m.CPB:.3f}")
        
        lines.append("\n" + "=" * 60)
        
        return "\n".join(lines)
    
    def _get_previous_board(self, board: chess.Board, 
                           move_history: Optional[List[chess.Move]]) -> Optional[chess.Board]:
        """Reconstruct previous board position for continuity scoring"""
        if not move_history or len(move_history) < 2:
            return None
        
        prev_board = chess.Board()
        for move in move_history[:-1]:
            prev_board.push(move)
        
        return prev_board
    
    def _fingerprint(self, board: chess.Board, move: chess.Move) -> str:
        """Create unique identifier for position + move"""
        return f"{board.fen()}:{move.uci()}"
    
    def _print_analysis(self, best: PositionSegment, 
                       all_segments: List[PositionSegment],
                       tug: np.ndarray):
        """Print analysis to console"""
        print("\n" + "="*60)
        print("COHERENCE CHESS ANALYSIS")
        print("="*60)
        print(f"\nSelected Move: {best.move.uci()} [{best.coherence_class.value.upper()}]")
        print(f"L_p = {best.metrics.L_p:+.3f}")
        print(f"  K_τ (Coherence):  {best.metrics.K_tau:.3f}")
        print(f"  V_Γ (Pressure):   {best.metrics.V_Gamma:.3f}")
        print(f"  D (Residue):      {best.metrics.D:.3f}")
        print(f"  CPB Ratio:        {best.metrics.CPB:.3f}")
        
        print(f"\nStratagem Tug: K_τ={tug[0]:.3f}, V_Γ={tug[1]:.3f}")
        
        # Class distribution
        class_counts = {}
        for seg in all_segments:
            cls = seg.coherence_class.value
            class_counts[cls] = class_counts.get(cls, 0) + 1
        
        print("\nMove Distribution:")
        for cls, count in class_counts.items():
            print(f"  {cls:15s}: {count:2d} moves")
        
        print("="*60 + "\n")


def demo():
    """Demonstration of the coherence chess solver"""
    solver = CoherenceChessSolver(D_max=0.5, base_depth=2)
    
    # Starting position
    board = chess.Board()
    
    print("Analyzing starting position...\n")
    analysis = solver.analyze_position(board)
    print(analysis)
    
    # Play a few moves
    moves_played = []
    for i in range(3):
        print(f"\n{'='*60}")
        print(f"Move {i+1}")
        print(f"{'='*60}")
        
        best_move, metrics = solver.select_best_move(board, moves_played, verbose=True)
        
        board.push(best_move)
        moves_played.append(best_move)
        
        print(f"Board after move:\n{board}\n")


if __name__ == "__main__":
    demo()
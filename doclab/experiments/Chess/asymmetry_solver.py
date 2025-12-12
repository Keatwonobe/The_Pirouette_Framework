#!/usr/bin/env python3
"""
Coherence Asymmetry Solver (Layer 3)

This script implements the "Tipping Point" model.
It searches for "asymmetric coherence" by finding the move
that maximizes the *coherence differential* between the
player and the opponent.

Layers 1-3 (Prism, Photovoltaic, Mask) are identical.
Layer 4 (Solver) is upgraded.

-   New Metric:
    Score = My_Future_Coherence - Opponent_Future_Coherence
"""

import chess
from typing import Dict, List, Tuple

# --- LAYER 1: The "Prism" (Piece Algorithm) ---
def get_piece_light(board: chess.Board, square: chess.Square) -> int:
    """THE "PRISM" (Unchanged)"""
    return board.attacks(square)

# --- LAYER 2: The "Photovoltaic" (Heuristic) ---
def translate_light_to_coherence(board: chess.Board, light_mask: int) -> float:
    """THE "PHOTOVOLTAIC" (Unchanged)"""
    our_pieces = board.occupied_co[board.turn]
    their_pieces = board.occupied_co[not board.turn]
    supported_light = bin(light_mask & our_pieces).count('1')
    attacked_light = bin(light_mask & their_pieces).count('1')
    coherence_value = (attacked_light * 1.5) + (supported_light * 1.0)
    return coherence_value

# --- LAYER 3: The "Mask" (Engram Generator) ---
def create_coherence_mask(
    board: chess.Board
) -> List[Tuple[int, str, float]]:
    """THE "MASK" / ENGRAM GENERATOR (Unchanged)"""
    coherence_readings = {}
    
    for piece_type in [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING]:
        our_pieces_of_type = board.pieces(piece_type, board.turn)
        
        for square in chess.scan_reversed(int(our_pieces_of_type)):
            light_mask = get_piece_light(board, square)
            coherence_value = translate_light_to_coherence(board, light_mask)
            piece_name = f"{chess.piece_name(piece_type).upper()} on {chess.square_name(square)}"
            coherence_readings[square] = (piece_name, coherence_value)

    sorted_mask_items = sorted(
        coherence_readings.items(), 
        key=lambda item: item[1][1], 
        reverse=True
    )
    final_mask = [
        (sq, name, val) for sq, (name, val) in sorted_mask_items if val > 0
    ]
    return final_mask

def get_peak_coherence(board: chess.Board) -> float:
    """
    This is our "evaluation function" (the "FFT").
    It runs an engram scan and returns the peak coherence value.
    """
    # Note: We are now passing board.turn, which is critical.
    # The 'board' object will have its turn already set to
    # whoever we are trying to evaluate.
    engram_mask = create_coherence_mask(board)
    if not engram_mask:
        return 0.0
    
    # The "peak" coherence of the manifold
    peak_coherence = engram_mask[0][2]
    return peak_coherence

# --- LAYER 4: The "Asymmetry Solver" (Tipping Point Finder) ---

def find_asymmetry_tipping_point(
    board: chess.Board, 
    pruning_threshold: int = 5
) -> Tuple[chess.Move, float, List[Tuple[chess.Move, float]]]:
    """
    THE SOLVER (Upgraded to Layer 3)
    Finds the move that maximizes the "Coherence Differential."
    """
    
    # 1. Generate the Engram (FFT) for *our* turn
    engram_mask = create_coherence_mask(board)
    
    # 2. Prune the Engram (Laser Point)
    pruned_pieces = engram_mask[:pruning_threshold]
    pruned_squares = {sq for (sq, name, val) in pruned_pieces}
    
    print("\n" + "="*70)
    print("LAYER 4: ASYMMETRY SOLVER (Finding Tipping Points)")
    print("="*70)
    print(f"Pruning search to TOP {pruning_threshold} 'laser-pointed' pieces:")
    for sq, name, val in pruned_pieces:
        print(f"  - {name:<20} | Coherence: {val:.2f}")

    # 3. Find the "Participants"
    solution_space = []
    for move in board.legal_moves:
        if move.from_square in pruned_squares:
            solution_space.append(move)
            
    print(f"\nFound {len(solution_space)} 'participant' moves from these pieces.")
    
    # 4. Find the "Tipping Point" (Evaluate the Asymmetry)
    evaluated_moves = []
    for move in solution_space:
        # --- THIS IS THE NEW LOGIC ---
        
        # a. Go to our future state
        board.push(move)
        # b. Calculate *our* future coherence
        my_future_coherence = get_peak_coherence(board)
        
        # c. Go to opponent's *reply* state (pass the turn)
        board.push(chess.Move.null())
        # d. Calculate *opponent's* future coherence
        opponent_future_coherence = get_peak_coherence(board)
        
        # e. Undo both moves
        board.pop() # Undo null move
        board.pop() # Undo our move
        
        # f. The new score is the *differential*
        coherence_differential = my_future_coherence - opponent_future_coherence
        
        # --- END NEW LOGIC ---
        
        evaluated_moves.append((move, coherence_differential))
        
    if not evaluated_moves:
        print("No coherent moves found.")
        return None, 0, []

    # Sort to find the best "tipping point"
    evaluated_moves.sort(key=lambda item: item[1], reverse=True)
    
    best_move, best_score = evaluated_moves[0]
    return best_move, best_score, evaluated_moves

def demo():
    """
    Run a demo of the Asymmetry Solver.
    """
    
    fen = "r1q2rk1/1b1n1pp1/p2bp2p/1p1n4/3P4/PB1Q1N2/1PPB1PPP/R3R1K1 w - - 4 17"
    board = chess.Board(fen)

    print("="*70)
    print("COHERENCE ASYMMETRY SOLVER (Layer 3)")
    print("="*70)
    print("Analyzing board (Time Domain):")
    print(board)

    # Call our new Layer 3 solver
    best_move, best_score, all_moves = find_asymmetry_tipping_point(
        board, 
        pruning_threshold=5 # <-- Only look at Top 5 pieces
    )

    print("\n" + "="*70)
    print("SOLVER RESULTS (ASYMMETRY)")
    print("="*70)
    print("The 'Tipping Points' (best moves to hoard coherence):")
    
    for move, score in all_moves[:5]:
        print(f"  - Move: {move.uci():<8} | Coherence Differential: {score:+.2f}")

    print("\n" + "-"*70)
    print(f"Chosen 'Tipping Point': {best_move.uci()}")
    print(f"This move creates the largest 'asymmetric coherence' ({best_score:+.2f}),")
    print("by maximizing our future state while minimizing the opponent's.")


if __name__ == "__main__":
    demo()
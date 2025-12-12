#!/usr/bin/env python3
"""
Coherence Engram Solver

This script implements the "Prism / Photovoltaic / Mask" model
and adds the "Solver" layer.

1.  Prism: A piece's "light" (attack mask).
2.  Photovoltaic: Translates "light" into a "coherence value."
3.  Mask (Engram): A prioritized list of high-potential pieces.
4.  Solver (Inverse FFT): Uses the Engram to find the move that
    leads to the *next* most coherent board state. This determines
    the "order of participants" that "respects the manifold."
"""

import chess
from typing import Dict, List, Tuple

# --- LAYER 1: The "Prism" (Piece Algorithm) ---

def get_piece_light(board: chess.Board, square: chess.Square) -> int:
    """
    THE "PRISM"
    Gets the "light" a piece projects. This is its raw attack mask.
    """
    return board.attacks(square)

# --- LAYER 2: The "Photovoltaic" (Heuristic) ---

def translate_light_to_coherence(board: chess.Board, light_mask: int) -> float:
    """
    THE "PHOTOVOLTAIC"
    Translates a "light" mask into a "coherence value."
    """
    our_pieces = board.occupied_co[board.turn]
    their_pieces = board.occupied_co[not board.turn]

    supported_light = bin(light_mask & our_pieces).count('1')
    attacked_light = bin(light_mask & their_pieces).count('1')

    # Value attacking more than supporting
    coherence_value = (attacked_light * 1.5) + (supported_light * 1.0)
    
    return coherence_value

# --- LAYER 3: The "Mask" (Engram Generator) ---

def create_coherence_mask(
    board: chess.Board
) -> List[Tuple[int, str, float]]:
    """
    THE "MASK" / ENGRAM GENERATOR
    This function "laser points" to the pieces that have
    the most coherent potential.
    
    <-- CHANGED: Now returns the piece's SQUARE (int) for the solver.
    """
    coherence_readings = {}
    
    for piece_type in [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING]:
        our_pieces_of_type = board.pieces(piece_type, board.turn)
        
        for square in chess.scan_reversed(int(our_pieces_of_type)):
            light_mask = get_piece_light(board, square)
            coherence_value = translate_light_to_coherence(board, light_mask)
            
            piece_name = f"{chess.piece_name(piece_type).upper()} on {chess.square_name(square)}"
            # Store by square so we can get it back easily
            coherence_readings[square] = (piece_name, coherence_value)

    # Sort by coherence value (item[1][1])
    sorted_mask_items = sorted(
        coherence_readings.items(), 
        key=lambda item: item[1][1], 
        reverse=True
    )
    
    # Format the final list: (square, piece_name, value)
    final_mask = [
        (sq, name, val) for sq, (name, val) in sorted_mask_items if val > 0
    ]
    
    return final_mask

# --- LAYER 4: The "Solver" (Inverse FFT) ---

def evaluate_future_coherence(board: chess.Board) -> float:
    """
    This is our "evaluation function" for the solver.
    It runs an "FFT" on the *future* board state and returns
    its peak coherence. This is how we "respect the manifold."
    """
    future_engram = create_coherence_mask(board)
    if not future_engram:
        return 0.0
    
    # For simplicity, we define the "coherence of the manifold"
    # as the coherence of its *most active piece*.
    peak_coherence = future_engram[0][2]
    return peak_coherence

def find_coherent_solution(
    board: chess.Board, 
    pruning_threshold: int = 5
) -> Tuple[chess.Move, float, List[Tuple[chess.Move, float]]]:
    """
    THE SOLVER
    Finds the "order of participants" by finding the best move
    from the "laser-pointed" pieces.
    """
    
    # 1. Generate the Engram (FFT)
    engram_mask = create_coherence_mask(board)
    
    # 2. Prune the Engram (Laser Point)
    # We will *only* consider pieces in the Top N of the mask.
    pruned_pieces = engram_mask[:pruning_threshold]
    pruned_squares = {sq for (sq, name, val) in pruned_pieces}
    
    print("\n" + "="*70)
    print("LAYER 4: SOLVER (Inverse FFT)")
    print("="*70)
    print(f"Pruning search to TOP {pruning_threshold} 'laser-pointed' pieces:")
    for sq, name, val in pruned_pieces:
        print(f"  - {name:<20} | Coherence: {val:.2f}")

    # 3. Find the "Participants" (Get moves from pieces)
    # This is the "Inverse FFT" step: from pieces back to moves.
    solution_space = []
    for move in board.legal_moves:
        if move.from_square in pruned_squares:
            solution_space.append(move)
            
    print(f"\nFound {len(solution_space)} 'participant' moves from these pieces.")
    
    # 4. Find the "Order" (Evaluate the Manifold Sequence)
    # Which "participant" move leads to the most coherent future?
    evaluated_moves = []
    for move in solution_space:
        board.push(move)
        # Evaluate the *next* board state
        future_score = evaluate_future_coherence(board)
        board.pop()
        evaluated_moves.append((move, future_score))
        
    if not evaluated_moves:
        print("No coherent moves found.")
        return None, 0, []

    # Sort to find the move that "respects the manifold"
    evaluated_moves.sort(key=lambda item: item[1], reverse=True)
    
    best_move, best_score = evaluated_moves[0]
    return best_move, best_score, evaluated_moves

def demo():
    """
    Run a demo of the Engram Solver.
    """
    
    # A complex, messy mid-game FEN
    fen = "r1q2rk1/1b1n1pp1/p2bp2p/1p1n4/3P4/PB1Q1N2/1PPB1PPP/R3R1K1 w - - 4 17"
    board = chess.Board(fen)

    print("="*70)
    print("COHERENCE ENGRAM SOLVER")
    print("="*70)
    print("Analyzing board (Time Domain):")
    print(board)

    # Call our main solver
    best_move, best_score, all_moves = find_coherent_solution(
        board, 
        pruning_threshold=5 # <-- Only look at Top 5 pieces
    )

    print("\n" + "="*70)
    print("SOLVER RESULTS")
    print("="*70)
    print("The 'Order of Participants' (best moves respecting the manifold):")
    
    for move, score in all_moves[:5]:
        print(f"  - Move: {move.uci():<8} | Leads to Coherence: {score:.2f}")

    print("\n" + "-"*70)
    print(f"Chosen 'Sequence': {best_move.uci()} (Queen first)")
    print(f"This move creates a new board with the highest")
    print(f"future coherence ({best_score:.2f}), respecting the manifold.")


if __name__ == "__main__":
    demo()
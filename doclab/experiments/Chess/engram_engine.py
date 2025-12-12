#!/usr/bin/env python3
"""
Coherence Engram Engine

This script implements the "Prism / Photovoltaic / Mask" model.
It does not search for moves. Instead, it analyzes a static board
state and generates a "coherence mask," or engram, which identifies
the pieces with the highest potential to create coherent solutions.

-   Prism: A piece's "algorithm," represented by the squares it
    projects its influence (light) onto.
-   Photovoltaic: A function that translates the "light" (attacks,
    supports) into a "coherence value."
-   Mask: The final, filtered list of pieces, prioritized by their
    coherence, which "laser points" to the agents of change.
"""

import chess
from typing import Dict, List, Tuple

def get_piece_light(board: chess.Board, square: chess.Square) -> int:
    """
    THE "PRISM"
    Gets the "light" a piece projects. This is its raw attack mask.
    """
    # board.attacks() is the perfect "prism" function.
    # It shows all light cast by the piece, even through
    # other pieces (which is what we want).
    return board.attacks(square)

def translate_light_to_coherence(board: chess.Board, light_mask: int) -> float:
    """
    THE "PHOTOVOLTAIC"
    Translates a "light" mask into a "coherence value."
    This is the core heuristic.
    
    Our simple model:
    -   Coherence is high if the light hits (attacks) enemy pieces.
    -   Coherence is good if the light hits (supports) our pieces.
    """
    our_pieces = board.occupied_co[board.turn]
    their_pieces = board.occupied_co[not board.turn]

    # Use bitwise AND to see where the light overlaps with pieces
    supported_light = bin(light_mask & our_pieces).count('1')
    attacked_light = bin(light_mask & their_pieces).count('1')

    # A simple weighted value. This is the "photovoltaic" translation.
    # We value attacking their pieces more than supporting our own.
    coherence_value = (attacked_light * 1.5) + (supported_light * 1.0)
    
    return coherence_value

def create_coherence_mask(board: chess.Board) -> List[Tuple[str, float]]:
    """
    THE "MASK" / ENGRAM GENERATOR
    This function "laser points" to the pieces that have
    the most coherent potential.
    """
    print(f"\nScanning {board.turn} pieces as 'Prisms'...")
    
    # This dict will store the "photovoltaic" reading for each piece
    coherence_readings = {}
    
    # 1. Iterate over all our pieces (the Prisms)
    for piece_type in [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING]:
        # Get a bitmask of all our pieces of this type
        our_pieces_of_type = board.pieces(piece_type, board.turn)
        
        for square in chess.scan_reversed(int(our_pieces_of_type)):
            
            # 2. Get the "light" projected by the prism
            light_mask = get_piece_light(board, square)
            
            # 3. Translate that light with the "photovoltaic"
            coherence_value = translate_light_to_coherence(board, light_mask)
            
            # Store the reading
            piece_name = f"{chess.piece_name(piece_type).upper()} on {chess.square_name(square)}"
            coherence_readings[piece_name] = coherence_value

    # 4. Create the Mask: Sort all pieces by their coherence value
    # This is the final "Engram" — a prioritized list of
    # coherent potential.
    sorted_mask = sorted(coherence_readings.items(), key=lambda item: item[1], reverse=True)
    
    return sorted_mask

def demo():
    """
    Run a demo of the Engram generator on a sample mid-game position.
    """
    
    # A complex, messy mid-game FEN
    # This is our "signal in the time domain"
    fen = "r1q2rk1/1b1n1pp1/p2bp2p/1p1n4/3P4/PB1Q1N2/1PPB1PPP/R3R1K1 w - - 4 17"
    board = chess.Board(fen)

    print("="*70)
    print("COHERENCE ENGRAM GENERATOR")
    print("="*70)
    print("Analyzing board (Time Domain):")
    print(board)

    # Call our main function to "FFT" this position
    # This translates it to the "Coherence (Frequency) Domain"
    engram_mask = create_coherence_mask(board)

    print("\n" + "="*70)
    print("COHERENCE ENGRAM (THE 'MASK')")
    print("="*70)
    print("The 'laser-pointed' pieces with the most coherent potential:")
    
    for piece, value in engram_mask:
        if value > 0:
            print(f"  - {piece:<20} | Coherence Value: {value:.2f}")
    
    print("\nThis mask is the 'engram'—a memory of the board's potential.")
    print("A solver would use this mask to *prune* its search,")
    print("focusing *only* on moves from these high-potential pieces.")


if __name__ == "__main__":
    demo()
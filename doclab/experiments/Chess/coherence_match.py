#!/usr/bin/env python3
import chess
from winning_coherence import WinningCoherenceSolver
from coherence_chess import CoherenceChessSolver

def safe_select(engine, board, move_history, side_label=""):
    """
    Try to get a move from the engine.
    If the engine explodes, fall back to a legal move so the game continues.
    """
    try:
        move, metrics = engine.select_best_move(
            board, move_history, verbose=True
        )
        return move, metrics
    except Exception as e:
        print(f"\n[FALLBACK] {side_label} engine failed, using first legal move.")
        print(f"[FALLBACK] error: {e}\n")
        # take any legal move so we don't kill the game
        move = next(iter(board.legal_moves))
        return move, None

def play_match(max_plies: int = 80):
    board = chess.Board()

    white_engine = WinningCoherenceSolver(D_max=0.6, base_depth=3)
    black_engine = CoherenceChessSolver(D_max=0.5, base_depth=2)

    move_history = []

    print("\n======================================================")
    print("COHERENCE MATCH: WinningCoherence (White) vs Base (Black)")
    print("======================================================\n")
    print(board, "\n")

    for ply in range(max_plies):
        if board.is_game_over():
            print("Game over:", board.result(), board.outcome())
            break

        if board.turn:  # white
            move, _ = safe_select(white_engine, board, move_history, "White")
            side = "White"
        else:  # black
            move, _ = safe_select(black_engine, board, move_history, "Black")
            side = "Black"

        san = board.san(move)
        board.push(move)
        move_history.append(move)

        print(f"{side} plays: {san}")
        print(board, "\n")

    print("\nFinal FEN:", board.fen())
    print("Move count:", len(move_history))

if __name__ == "__main__":
    play_match()

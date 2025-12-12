#!/usr/bin/env python3
"""
coherence_board_solver.py with Dark Residue

- runs N games
- default: chess
- per move we now log:
    * coherence score (asymmetry)
    * dark_residue D
    * the 4 components of D

This gives us data to do reverse-Pareto on residue afterwards.
"""
from __future__ import annotations
import os, json, argparse, datetime

# ============================================================
# CONFIG
# ============================================================

GAME_CONFIG = {
    "game_type": "chess",
    "board_size": 8,
    "max_plies": 120,
    "actor_limit": 5,
    "log_masks": True,
    # Dark Residue weights — tune these
    "D_alpha": 1.0,   # Div(welfare)
    "D_beta": 1.0,    # Ext(risk)
    "D_gamma": 0.7,   # Attention debt
    "D_delta": 0.5,   # Loss of autonomy
    "D_epsilon": 10.0 # <--- CHANGED: Add a high penalty for repetition
}

# ============================================================
# ADAPTERS
# ============================================================

try:
    import chess
except ImportError:
    print("Failed to import 'chess'. Please install it: pip install chess")
    chess = None


class BaseGameAdapter:
    def new_board(self):
        raise NotImplementedError

    def is_game_over(self, board):
        raise NotImplementedError

    def result(self, board):
        raise NotImplementedError

    def legal_moves(self, board):
        raise NotImplementedError

    def push(self, board, move):
        raise NotImplementedError

    def pop(self, board):
        raise NotImplementedError

    def null_move(self, board):
        raise NotImplementedError

    def serialize_move(self, board, move):
        return str(move)

    def fen(self, board):
        return ""

    def side_to_move(self, board):
        raise NotImplementedError


class ChessAdapter(BaseGameAdapter):
    def new_board(self):
        return chess.Board()

    def is_game_over(self, board):
        return board.is_game_over()

    def result(self, board):
        return board.result()

    def legal_moves(self, board):
        return list(board.legal_moves)

    def push(self, board, move):
        board.push(move)

    def pop(self, board):
        board.pop()

    def null_move(self, board):
        board.push(chess.Move.null())

    def serialize_move(self, board, move):
        try:
            return board.san(move)
        except Exception:
            return move.uci()

    def fen(self, board):
        try:
            return board.fen()
        except Exception:
            return board.board_fen()

    def side_to_move(self, board):
        return board.turn


# ============================================================
# DARK RESIDUE (chess specialization)
# ============================================================

def _safe_all_squares():
    # This is robust
    return range(64)


def _king_safety(board: chess.Board, color: bool) -> float:
    """
    Very cheap king safety proxy:
    - penalize open files near king
    - reward own pawns on king side
    """
    king_sq = board.king(color)
    if king_sq is None:
        return 0.0
    file_idx = chess.square_file(king_sq)
    rank_idx = chess.square_rank(king_sq)

    score = 0.0

    # own pawns in adjacent files
    for df in (-1, 0, 1):
        f = file_idx + df
        if 0 <= f < 8:
            for dr in (1, 2):
                r = rank_idx + (dr if color == chess.WHITE else -dr)
                if 0 <= r < 8:
                    sq = chess.square(f, r)
                    piece = board.piece_at(sq)
                    if piece and piece.piece_type == chess.PAWN and piece.color == color:
                        score += 0.5
    return score


def _opponent_attack_surface(board: chess.Board, color: bool) -> int:
    """
    Count how many squares the opponent controls.
    """
    opp = not color
    total = 0
    for sq in _safe_all_squares():
        piece = board.piece_at(sq)
        if not piece or piece.color != opp:
            continue
        # Use a safe way to get attacks
        try:
            total += bin(board.attacks(sq)).count('1')
        except Exception:
            pass # Failsafe if board is corrupt
    return total


def _undefended_own_pieces(board: chess.Board, color: bool) -> int:
    """
    Count own pieces that are attacked but not defended.
    """
    me = color
    opp = not color
    count = 0
    for sq in _safe_all_squares():
        piece = board.piece_at(sq)
        if not piece or piece.color != me:
            continue
        attacked = board.is_attacked_by(opp, sq)
        defended = board.is_attacked_by(me, sq)
        if attacked and not defended:
            count += 1
    return count


def _legal_move_count(board: chess.Board) -> int:
    try:
        return len(list(board.legal_moves))
    except Exception:
        # If board is corrupt (e.g., no king), legal_moves fails.
        return 0


def compute_dark_residue_chess(board_before: chess.Board,
                               board_after: chess.Board,
                               acting_color: bool,
                               cfg: dict) -> dict:
    """
    D = α Div(welfare) + β Ext(risk) + γ AttentionDebt + δ LossAutonomy
    specialized to chess.
    ...
    """
    α = cfg["D_alpha"]
    β = cfg["D_beta"]
    γ = cfg["D_gamma"]
    δ = cfg["D_delta"]
    # Epsilon (repetition) is handled in the main search loop

    try:
        # before
        ks_before = _king_safety(board_before, acting_color)
        risk_before = _opponent_attack_surface(board_before, acting_color)
        undef_before = _undefended_own_pieces(board_before, acting_color)
        legal_before = _legal_move_count(board_before)

        # after
        ks_after = _king_safety(board_after, acting_color)
        risk_after = _opponent_attack_surface(board_after, acting_color)
        undef_after = _undefended_own_pieces(board_after, acting_color)

        # to measure autonomy, we need to give the move back to us
        legal_after = 0
        board_after.push(chess.Move.null())
        legal_after = _legal_move_count(board_after)
        board_after.pop()

    except Exception as e:
        return {
            "D": 100.0, # High penalty
            "Div_welfare": 0.0, "Ext_risk": 0.0,
            "Attention_debt": 0.0, "Loss_autonomy": 0.0,
            "Repetition": 0.0
        }


    div_welfare = max(0.0, (ks_before - ks_after))  # we got less safe
    ext_risk = max(0.0, (risk_after - risk_before))
    attention_debt = max(0.0, (undef_after - undef_before))
    loss_autonomy = max(0.0, (legal_before - legal_after))

    D = (
        α * div_welfare
        + β * ext_risk
        + γ * attention_debt
        + δ * loss_autonomy
    )

    return {
        "D": D,
        "Div_welfare": div_welfare,
        "Ext_risk": ext_risk,
        "Attention_debt": attention_debt,
        "Loss_autonomy": loss_autonomy,
        "Repetition": 0.0 # Placeholder
    }


# ============================================================
# COHERENCE / ASYMMETRY SOLVER
# ============================================================

class CoherenceAsymmetrySolver:
    def __init__(self, adapter: BaseGameAdapter, cfg: dict):
        self.adapter = adapter
        self.cfg = cfg
        self.actor_limit = cfg["actor_limit"]

    # ---- actor mask (chess) ----
    def _chess_actor_mask(self, board: chess.Board):
        actors = []
        for sq in _safe_all_squares():
            try:
                piece = board.piece_at(sq)
            except Exception: # Board might be corrupt
                continue 
            if not piece or piece.color != board.turn:
                continue
            
            try:
                attacks = board.attacks(sq)
                influence = bin(attacks).count('1')
            except Exception:
                influence = 0 # Board corrupt
                
            # center bias
            file_idx = chess.square_file(sq)
            rank_idx = chess.square_rank(sq)
            if file_idx in (3, 4):
                influence += 0.5
            if rank_idx in (3, 4):
                influence += 0.5
            actors.append((sq, influence, {"piece": piece.symbol()}))
        actors.sort(key=lambda x: x[1], reverse=True)
        return actors[: self.actor_limit]

    def create_actor_mask(self, board):
        # only chess for now
        return self._chess_actor_mask(board)

    def _peak_coherence_one_ply(self, board):
        # <--- RESTORED: This is a 1-ply search again (restoring the "extra dimension")
        # It receives a board, which is a COPY, and is safe to mutate.
        
        # <--- CRITICAL FIX: Materialize the list to prevent re-entrancy crashes
        moves = list(self.adapter.legal_moves(board))
        if not moves:
            return 0.0
            
        best = -1e9
        for mv in moves:
            self.adapter.push(board, mv)
            
            # Use the 0-ply "static" evaluation inside the 1-ply search
            mask = self.create_actor_mask(board)
            val = mask[0][1] if mask else 0.0
            
            self.adapter.pop(board)
            if val > best:
                best = val
        return best

    def choose_move(self, board, log_masks=False):
        adapter = self.adapter
        actor_mask = self.create_actor_mask(board)
        actor_squares = {sq for (sq, _, _) in actor_mask}
        legal = adapter.legal_moves(board)
        if not legal:
            return None, {"reason": "no_moves", "mask": actor_mask}

        best_move = None
        best_score = -1e9
        best_meta = None
        move_logs = []

        # Use the first legal move as a fallback
        best_move = legal[0]

        for mv in legal:
            from_sq = mv.from_square if hasattr(mv, "from_square") else None
            
            if from_sq is None or from_sq not in actor_squares:
                continue # not today's actor

            # snapshot before
            board_before = board.copy()

            # my branch
            adapter.push(board, mv) # <-- This mutates the main board
            
            my_future = self._peak_coherence_one_ply(board.copy())

            # opponent branch
            try:
                adapter.null_move(board)
                their_future = self._peak_coherence_one_ply(board.copy())
                adapter.pop(board) # pop null
            except Exception:
                their_future = 0.0

            # compute Dark Residue on the two boards
            board_after = board.copy() # board_after is current board state
            acting_color = board_before.turn
            D_pack = compute_dark_residue_chess(board_before, board_after, acting_color, self.cfg)

            # ---
            # <--- CHANGED: Add the Repetition Penalty (D_epsilon)
            # ---
            # We check the main board *after* the move was pushed
            # to see if this move *causes* a repetition.
            repetition_cost = 0.0
            if board.is_repetition(2): # This move creates the 2nd appearance
                repetition_cost = self.cfg["D_epsilon"] * 0.5
            if board.is_repetition(3): # This move *is* the 3rd appearance (a draw)
                repetition_cost = self.cfg["D_epsilon"]
            
            D_pack["Repetition"] = repetition_cost
            D_pack["D"] += repetition_cost
            # ---
            
            adapter.pop(board)  # undo my move (mv)

            # main asymmetry score
            asym_score = my_future - their_future

            # we can make D “punish” the score right here:
            total_score = asym_score - D_pack["D"]

            if total_score > best_score:
                best_score = total_score
                best_move = mv
                best_meta = {
                    "mask": actor_mask if log_masks else None,
                    "my_future": my_future,
                    "their_future": their_future,
                    "asym_score": asym_score,
                    "dark_residue": D_pack,
                }

            if log_masks:
                move_logs.append({
                    "move": adapter.serialize_move(board_before, mv),
                    "my_future": my_future,
                    "their_future": their_future,
                    "asym_score": asym_score,
                    "dark_residue": D_pack,
                })

        if best_meta is not None and log_masks:
            best_meta["move_eval"] = move_logs

        # This can happen if all pruned moves are worse than the default
        if best_move is None and legal:
            best_move = legal[0]

        return best_move, best_meta


# ============================================================
# RUNNER
# ============================================================

def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


def run_games(num_games: int, out_dir: str, cfg: dict):
    if cfg["game_type"] != "chess":
        raise NotImplementedError("Only chess wired right now")
    if chess is None:
        print("Chess adapter failed to load. Aborting.")
        return

    adapter = ChessAdapter()
    solver_white = CoherenceAsymmetrySolver(adapter, cfg)
    solver_black = CoherenceAsymmetrySolver(adapter, cfg)

    ensure_dir(out_dir)

    for g in range(num_games):
        board = adapter.new_board()
        game_log = {
            "game_index": g,
            "moves": [],
            "result": None,
            "game_type": cfg["game_type"],
        }
        print(f"\nStarting Game {g+1}/{num_games}...")

        for ply in range(cfg["max_plies"]):
            if adapter.is_game_over(board):
                game_log["result"] = adapter.result(board)
                break

            side = "white" if adapter.side_to_move(board) else "black"
            solver = solver_white if side == "white" else solver_black

            move, meta = solver.choose_move(board, log_masks=cfg["log_masks"])
            
            if move is None:
                print(f"  Ply {ply} ({side}): No move found.")
                game_log["result"] = "NoMoveFound"
                break

            fen_before = adapter.fen(board)
            move_s = adapter.serialize_move(board, move)
            adapter.push(board, move)
            
            # Updated print to show the full D score
            dr_score = meta.get('dark_residue', {}).get('D', 0)
            print(f"  Ply {ply} ({side}): {move_s:6} (Score: {meta.get('asym_score', 0):.2f}, D: {dr_score:.2f})")

            game_log["moves"].append({
                "ply": ply,
                "side": side,
                "move": move_s,
                "fen_before": fen_before,
                "score": meta.get("asym_score") if meta else None,
                "dark_residue": meta.get("dark_residue") if meta else None,
                "mask": meta.get("mask") if meta else None,
                "move_eval": meta.get("move_eval") if meta else None,
            })

        if game_log["result"] is None:
            game_log["result"] = adapter.result(board)
            
        print(f"Game {g+1} Result: {game_log['result']}")

        stamp = datetime.datetime.now().strftime("%Y%m%d")
        game_dir = os.path.join(out_dir, stamp)
        ensure_dir(game_dir)
        out_path = os.path.join(game_dir, f"game_{g:04d}.json")

        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(game_log, f, indent=2)

        print(f"[{g+1}/{num_games}] saved {out_path}")


def main():
    parser = argparse.ArgumentParser(description="Coherence solver with Dark Residue")
    parser.add_argument("--games", type=int, default=5)
    parser.add_argument("--out-dir", type=str, default="./runs")
    args = parser.parse_args()

    run_games(args.games, args.out_dir, GAME_CONFIG)


if __name__ == "__main__":
    main()
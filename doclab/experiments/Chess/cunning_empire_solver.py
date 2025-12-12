#!/usr/bin/env python3
"""
cunning_empire_solver.py

Chess solver that:
- still measures coherence (actor mask, influence)
- but in "empire" mode tries to INDUCE dark residue in the opponent
  by agitating their boundary and creating follow-up burdens.

Usage:
    python cunning_empire_solver.py --games 5 --out-dir ./runs
"""

from __future__ import annotations
import os, json, argparse, datetime

try:
    import chess
except ImportError:
    chess = None

# ============================================================
# CONFIG
# ============================================================

GAME_CONFIG = {
    "game_type": "chess",
    "max_plies": 120,
    "actor_limit": 5,
    "log_masks": True,

    # survival vs empire
    "mode": "empire",          # "survival" or "empire"

    # coherence side
    "aggression_factor": 1.2,

    # dark residue weights (ours vs theirs)
    "D_alpha": 1.0,
    "D_beta": 1.0,
    "D_gamma": 0.7,
    "D_delta": 0.5,

    # empire extras
    "induce_weight": 1.2,      # ρ: how much we LIKE giving them residue
    "self_D_weight": 0.4,      # θ: how much we still dislike our own residue
    "boundary_bonus": 0.6,     # extra for hitting opponent pawn/front
}

# ============================================================
# ADAPTER
# ============================================================

class ChessAdapter:
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
# DARK RESIDUE PRIMITIVES (same as before, but we will compute
# for us AND estimate for them)
# ============================================================

def _safe_all_squares():
    if hasattr(chess, "SQUARES"):
        sqs = getattr(chess, "SQUARES")
        try:
            iter(sqs)
            return sqs
        except TypeError:
            return range(64)
    return range(64)


def _king_safety(board: "chess.Board", color: bool) -> float:
    king_sq = board.king(color)
    if king_sq is None:
        return 0.0
    file_idx = chess.square_file(king_sq)
    rank_idx = chess.square_rank(king_sq)
    score = 0.0
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


def _opponent_attack_surface(board: "chess.Board", color: bool) -> int:
    opp = not color
    total = 0
    for sq in _safe_all_squares():
        piece = board.piece_at(sq)
        if not piece or piece.color != opp:
            continue
        total += len(board.attacks(sq))
    return total


def _undefended_own_pieces(board: "chess.Board", color: bool) -> int:
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


def _legal_move_count(board: "chess.Board") -> int:
    try:
        return len(list(board.legal_moves))
    except Exception:
        return 0


def compute_dark_residue(board_before: "chess.Board",
                         board_after: "chess.Board",
                         acting_color: bool,
                         cfg: dict) -> dict:
    α = cfg["D_alpha"]; β = cfg["D_beta"]; γ = cfg["D_gamma"]; δ = cfg["D_delta"]

    ks_before = _king_safety(board_before, acting_color)
    risk_before = _opponent_attack_surface(board_before, acting_color)
    undef_before = _undefended_own_pieces(board_before, acting_color)
    legal_before = _legal_move_count(board_before)

    ks_after = _king_safety(board_after, acting_color)
    risk_after = _opponent_attack_surface(board_after, acting_color)
    undef_after = _undefended_own_pieces(board_after, acting_color)

    # <--- THIS BLOCK IS THE FIX ---
    legal_after = 0
    pushed_null = False # Flag to track if we pushed a move
    try:
        # autonomy: give the move back to us
        board_after.push(chess.Move.null())
        pushed_null = True # Mark the push as successful
        legal_after = _legal_move_count(board_after)
    except Exception:
        legal_after = 0 # Failsafe
    finally:
        # CRITICAL: This MUST run even if the 'try' fails.
        # Only pop if we successfully pushed.
        if pushed_null:
            board_after.pop()
    # <--- END FIX ---

    div_welfare = max(0.0, ks_before - ks_after)
    ext_risk = max(0.0, risk_after - risk_before)
    attention_debt = max(0.0, undef_after - undef_before)
    loss_autonomy = max(0.0, legal_before - legal_after)

    D = α * div_welfare + β * ext_risk + γ * attention_debt + δ * loss_autonomy

    return {
        "D": D,
        "Div_welfare": div_welfare,
        "Ext_risk": ext_risk,
        "Attention_debt": attention_debt,
        "Loss_autonomy": loss_autonomy,
    }


# ============================================================
# RESONANT BOUNDARY DOMINANCE (chess version)
# poke enemy boundary → extra points
# ============================================================

def is_boundary_poke(board: "chess.Board", move: "chess.Move") -> bool:
    """
    Boundary = opponent pawn belt, plus files a/h.
    If we move into / attack those squares, we count it.
    """
    them = not board.turn  # we're about to move, board.turn = us
    target = move.to_square
    rank = chess.square_rank(target)
    file_ = chess.square_file(target)

    # edge files
    if file_ in (0, 7):
        return True

    # hit their pawn belt
    if them == chess.WHITE:
        # we are black; white pawn belt ~ ranks 3/4
        return rank in (3, 4)
    else:
        # we are white; black pawn belt ~ ranks 4/5
        return rank in (4, 5)


# ============================================================
# CORE SOLVER
# ============================================================

class CunningEmpireSolver:
    def __init__(self, adapter: ChessAdapter, cfg: dict):
        self.adapter = adapter
        self.cfg = cfg
        self.actor_limit = cfg["actor_limit"]
        self.mode = cfg.get("mode", "empire")

    # actor mask = same as before: pick our most influential pieces
    def create_actor_mask(self, board: "chess.Board"):
        actors = []
        for sq in _safe_all_squares():
            piece = board.piece_at(sq)
            if not piece or piece.color != board.turn:
                continue
            attacks = board.attacks(sq)
            influence = len(attacks)
            f = chess.square_file(sq); r = chess.square_rank(sq)
            if f in (3, 4):
                influence += 0.5
            if r in (3, 4):
                influence += 0.5
            actors.append((sq, influence, {"piece": piece.symbol()}))
        actors.sort(key=lambda x: x[1], reverse=True)
        return actors[: self.actor_limit]

    def _peak_coherence_one_ply(self, board: "chess.Board") -> float:
        # <--- FIX 1: This function was also mutating the board it was iterating.
        moves = self.adapter.legal_moves(board)
        if not moves:
            return 0.0
        best = -1e9
        for mv in moves:
            # Create a disposable copy for this move
            board_after = board.copy()
            self.adapter.push(board_after, mv)
            
            # Evaluate the copy
            mask2 = self.create_actor_mask(board_after)
            val = mask2[0][1] if mask2 else 0.0
            
            # No pop needed, we just discard the copy
            if val > best:
                best = val
        return best

    def _estimate_induced_residue_on_opponent(self, board_after_our_move: "chess.Board") -> float:
        """
        After we move, it's their turn. We look at THEIR position
        and ask: how bad is it for them to move now?
        ...
        """
        opp = board_after_our_move.turn
        
        # <--- FIX 2: This function was *also* mutating the board (board_after_our_move)
        # that it was iterating over.
        legal_opp = list(board_after_our_move.legal_moves)
        if not legal_opp:
            return 0.0

        best_they_can_do = float("inf")
        for mv in legal_opp:
            # We use the un-mutated 'board_after_our_move' as the "before" state
            before = board_after_our_move
            
            # Create a new disposable copy for the opponent's move
            board_after_opp_move = board_after_our_move.copy()
            board_after_opp_move.push(mv)
            
            # 'after' is just this new copy
            after = board_after_opp_move
            
            Dp = compute_dark_residue(before, after, opp, self.cfg)
            
            # No pop needed
            if Dp["D"] < best_they_can_do:
                best_they_can_do = Dp["D"]

        return best_they_can_do if best_they_can_do > 0 else 0.0

    def choose_move(self, board: "chess.Board", log_masks=False):
        mask = self.create_actor_mask(board)
        mask_squares = {sq for (sq, _, _) in mask}
        legal = self.adapter.legal_moves(board)
        if not legal:
            return None, {"reason": "no_moves"}

        best_move = None
        best_meta = None
        best_score = -1e9
        move_logs = []

        for mv in legal:
            # <--- FIX 3: This is the main re-entrancy fix.
            # We NEVER mutate the main 'board' object.
            # We create one 'board_after' copy for *this move*
            # and do all our work on it.
            
            board_after = board.copy()
            self.adapter.push(board_after, mv)

            # our coherence (pass a copy to the 2-ply search)
            my_future = self._peak_coherence_one_ply(board_after.copy())

            # opponent coherence (pass a copy to the 2-ply search)
            try:
                # Create a *new* copy for the null move
                their_board = board_after.copy()
                self.adapter.null_move(their_board)
                their_future = self._peak_coherence_one_ply(their_board.copy())
            except Exception:
                their_future = 0.0

            # our own residue for this move
            # 'board' is the *original* board, 'board_after' is the new state
            our_color = board.turn
            D_me = compute_dark_residue(board, board_after, our_color, self.cfg)

            # empire piece: how much residue did we force them to face?
            induced = self._estimate_induced_residue_on_opponent(board_after)

            # boundary poke?
            boundary_bonus = self.cfg["boundary_bonus"] if is_boundary_poke(board, mv) else 0.0

            # score
            aggression = self.cfg["aggression_factor"]
            induce_w = self.cfg["induce_weight"]
            selfD_w = self.cfg["self_D_weight"]

            asym = (my_future * aggression) - their_future

            if self.mode == "survival":
                total = asym - D_me["D"]  # classic
            else:  # empire
                total = (
                    asym
                    + induce_w * induced
                    + boundary_bonus
                    - selfD_w * D_me["D"]
                )

            # No 'pop' needed, we just let 'board_after' go out of scope
            # <--- END FIX 3

            if total > best_score:
                best_score = total
                best_move = mv
                best_meta = {
                    "mask": mask if log_masks else None,
                    "my_future": my_future,
                    "their_future": their_future,
                    "asym": asym,
                    "our_D": D_me,
                    "induced_D_them": induced,
                    "boundary_bonus": boundary_bonus,
                    "total": total,
                }

            if log_masks:
                move_logs.append({
                    "move": self.adapter.serialize_move(board, mv),
                    "my_future": my_future,
                    "their_future": their_future,
                    "asym": asym,
                    "our_D": D_me,
                    "induced_D_them": induced,
                    "boundary_bonus": boundary_bonus,
                    "total": total,
                })

        if best_meta and log_masks:
            best_meta["moves_eval"] = move_logs
            
        # Add a fallback in case all moves have terrible scores
        if best_move is None:
            best_move = legal[0]
        print("moved.")
        return best_move, best_meta


# ============================================================
# RUNNER
# ============================================================

def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


def run_games(num_games: int, out_dir: str, cfg: dict):
    adapter = ChessAdapter()
    solver_w = CunningEmpireSolver(adapter, cfg)
    solver_b = CunningEmpireSolver(adapter, cfg)

    stamp = datetime.datetime.now().strftime("%Y%m%d")
    day_dir = os.path.join(out_dir, stamp)
    ensure_dir(day_dir)

    for g in range(num_games):
        board = adapter.new_board()
        game_log = {
            "game_index": g,
            "moves": [],
            "result": None,
            "mode": cfg["mode"],
        }

        for ply in range(cfg["max_plies"]):
            if adapter.is_game_over(board):
                game_log["result"] = adapter.result(board)
                break

            side = "white" if adapter.side_to_move(board) else "black"
            solver = solver_w if side == "white" else solver_b

            move, meta = solver.choose_move(board, log_masks=cfg["log_masks"])
            if move is None:
                game_log["result"] = adapter.result(board)
                break

            fen_before = adapter.fen(board)
            mv_s = adapter.serialize_move(board, move)
            adapter.push(board, move)

            game_log["moves"].append({
                "ply": ply,
                "side": side,
                "move": mv_s,
                "fen_before": fen_before,
                "meta": meta,
            })

        if game_log["result"] is None:
            game_log["result"] = adapter.result(board)

        out_path = os.path.join(day_dir, f"game_{g:04d}.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(game_log, f, indent=2)

        print(f"[{g+1}/{num_games}] saved {out_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--games", type=int, default=5)
    parser.add_argument("--out-dir", type=str, default="./runs")
    parser.add_argument("--mode", type=str, default="empire")
    args = parser.parse_args()

    GAME_CONFIG["mode"] = args.mode
    run_games(args.games, args.out_dir, GAME_CONFIG)


if __name__ == "__main__":
    main()

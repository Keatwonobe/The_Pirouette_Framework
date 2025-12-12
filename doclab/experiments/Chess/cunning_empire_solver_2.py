#!/usr/bin/env python3
"""
Hardened Coherence Batch Solver (no fragile board.copy / clear_board calls)
Based on: coherence_batch_solver_5.py
"""

from __future__ import annotations
import os, json, argparse, datetime, time

try:
    import chess
except ImportError:
    print("Failed to import 'chess'. Please install it: pip install chess")
    chess = None

GAME_CONFIG = {
    "game_type": "chess",
    "board_size": 8,
    "max_plies": 120,
    "actor_limit": 5,
    "log_masks": True,
    "D_alpha": 1.0,
    "D_beta": 1.0,
    "D_gamma": 0.7,
    "D_delta": 0.5,
    "D_epsilon": 10.0,
    "dark_budget_pieces": ["p", "n", "b", "q"],
    "aggression_factor": 1.2,
    "destruction_weight": 2.0,
}

# ---------- adapters ----------
class ChessAdapter:
    def new_board(self): return chess.Board()
    def is_game_over(self, board): return board.is_game_over()
    def result(self, board): return board.result()
    def legal_moves(self, board): return list(board.legal_moves)
    def push(self, board, move): board.push(move)
    def pop(self, board): board.pop()
    def null_move(self, board): board.push(chess.Move.null())
    def serialize_move(self, board, move):
        try: return board.san(move)
        except Exception: return move.uci()
    def fen(self, board):
        try: return board.fen()
        except Exception: return board.board_fen()
    def side_to_move(self, board): return board.turn

# ---------- helpers ----------
def _safe_all_squares(): return range(64)

def _king_safety(board: chess.Board, color: bool) -> float:
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
                if 0 <= r < 0 or r >= 8:
                    continue
                sq = chess.square(f, r)
                piece = board.piece_at(sq)
                if piece and piece.piece_type == chess.PAWN and piece.color == color:
                    score += 0.5
    return score

def _opponent_attack_surface(board: chess.Board, color: bool) -> int:
    # safer: just count len(attacks)
    opp = not color
    total = 0
    for sq in _safe_all_squares():
        piece = board.piece_at(sq)
        if not piece or piece.color != opp:
            continue
        try:
            total += len(board.attacks(sq))
        except Exception:
            pass
    return total

def _undefended_own_pieces(board: chess.Board, color: bool) -> int:
    me, opp = color, not color
    count = 0
    for sq in _safe_all_squares():
        piece = board.piece_at(sq)
        if not piece or piece.color != me:
            continue
        if board.is_attacked_by(opp, sq) and not board.is_attacked_by(me, sq):
            count += 1
    return count

def _legal_move_count(board: chess.Board) -> int:
    try:
        return len(list(board.legal_moves))
    except Exception:
        return 0

def compute_dark_residue_chess(board_before: chess.Board,
                               board_after: chess.Board,
                               acting_color: bool,
                               cfg: dict) -> dict:
    α, β, γ, δ = cfg["D_alpha"], cfg["D_beta"], cfg["D_gamma"], cfg["D_delta"]
    try:
        ks_before = _king_safety(board_before, acting_color)
        risk_before = _opponent_attack_surface(board_before, acting_color)
        undef_before = _undefended_own_pieces(board_before, acting_color)
        legal_before = _legal_move_count(board_before)

        ks_after = _king_safety(board_after, acting_color)
        risk_after = _opponent_attack_surface(board_after, acting_color)
        undef_after = _undefended_own_pieces(board_after, acting_color)

        legal_after = 0
        pushed = False
        try:
            board_after.push(chess.Move.null())
            pushed = True
            legal_after = _legal_move_count(board_after)
        finally:
            if pushed:
                board_after.pop()

    except Exception:
        # fallback if anything goes weird
        return {
            "D": 100.0,
            "Div_welfare": 0.0,
            "Ext_risk": 0.0,
            "Attention_debt": 0.0,
            "Loss_autonomy": 0.0,
            "Repetition": 0.0,
        }

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
        "Repetition": 0.0,
    }

def _chess_actor_mask(board: chess.Board, actor_limit: int):
    in_check = board.is_check()
    candidates = []
    king_candidates = []

    for sq in range(64):
        piece = board.piece_at(sq)
        if not piece or piece.color != board.turn:
            continue

        # base influence
        try:
            influence = len(board.attacks(sq))
        except Exception:
            influence = 0

        f = chess.square_file(sq)
        r = chess.square_rank(sq)
        if f in (3, 4):
            influence += 0.5
        if r in (3, 4):
            influence += 0.5

        entry = (sq, influence, {"piece": piece.symbol()})

        # separate kings
        if piece.piece_type == chess.KING and not in_check:
            king_candidates.append(entry)
        else:
            candidates.append(entry)

    # sort non-king pieces first
    candidates.sort(key=lambda x: x[1], reverse=True)

    masked = candidates[:actor_limit]

    # if we got NOTHING (e.g. endgame, or very small board), allow king
    if not masked:
        king_candidates.sort(key=lambda x: x[1], reverse=True)
        masked = king_candidates[:actor_limit]

    return masked


def _peak_coherence_0_ply(board: chess.Board, actor_limit: int) -> float:
    mask = _chess_actor_mask(board, actor_limit)
    return mask[0][1] if mask else 0.0

# ---------- fast opponent ----------
class SimpleGreedySolver:
    def __init__(self, adapter: ChessAdapter, cfg: dict):
        self.adapter = adapter
        self.cfg = cfg
        self.actor_limit = cfg["actor_limit"]
        self.aggression = cfg.get("aggression_factor", 1.0)

    def choose_move(self, board, log_masks=False):
        legal = self.adapter.legal_moves(board)
        if not legal:
            return None, {"reason": "no_moves"}

        best_move = legal[0]
        best_score = -1e9

        for mv in legal:
            self.adapter.push(board, mv)
            my_future = _peak_coherence_0_ply(board, self.actor_limit)
            try:
                self.adapter.null_move(board)
                their_future = _peak_coherence_0_ply(board, self.actor_limit)
                self.adapter.pop(board)
            except Exception:
                their_future = 0.0
            self.adapter.pop(board)

            total = (my_future * self.aggression) - their_future
            if total > best_score:
                best_score = total
                best_move = mv

        return best_move, {"asym_score": best_score, "dark_residue": {"D": 0.0}}

# ---------- hardened batch agent ----------
class CoherenceBatchSolver:
    def __init__(self, adapter: ChessAdapter, cfg: dict):
        self.adapter = adapter
        self.cfg = cfg
        self.actor_limit = cfg["actor_limit"]
        self.aggression = cfg.get("aggression_factor", 1.0)
        self.destruction_weight = cfg.get("destruction_weight", 1.0)
        self.last_their_future = None

    def reset_game(self):
        self.last_their_future = None

    def _apply_dark_budget(self, board: chess.Board) -> chess.Board:
        budget_symbols = self.cfg.get("dark_budget_pieces", [])
        if not budget_symbols:
            return board

        # make an empty board that's version-friendly
        try:
            budget_board = chess.Board.empty()  # newer versions
        except Exception:
            budget_board = chess.Board(None)    # older versions

        # keep turn / ep / castling so logic stays sane
        budget_board.turn = board.turn
        budget_board.castling_rights = board.castling_rights
        budget_board.ep_square = board.ep_square

        for sq in _safe_all_squares():
            piece = board.piece_at(sq)
            if piece and piece.symbol().lower() in budget_symbols:
                budget_board.set_piece_at(sq, piece)

        return budget_board

    def _peak_coherence_2_ply(self, board: chess.Board) -> float:
        moves = list(self.adapter.legal_moves(board))
        if not moves:
            return 0.0
        best = -1e9
        for mv in moves:
            self.adapter.push(board, mv)
            val = _peak_coherence_0_ply(board, self.actor_limit)
            self.adapter.pop(board)
            if val > best:
                best = val
        return best

    def generate_tasks(self, board: chess.Board, task_file_path: str) -> int:
        actor_mask = _chess_actor_mask(board, self.actor_limit)
        actor_squares = {sq for (sq, _, _) in actor_mask}
        tasks = []
        move_stack_uci = [mv.uci() for mv in board.move_stack]

        in_check = board.is_check()

        for mv in self.adapter.legal_moves(board):
            # only consider moves by selected actors
            if mv.from_square not in actor_squares:
                continue

            piece = board.piece_at(mv.from_square)
            is_king_move = piece is not None and piece.piece_type == chess.KING

            # don't let the king eat the turn unless we must
            if is_king_move and not in_check and not board.is_castling(mv):
                continue

            tasks.append({
                "move_stack_uci": move_stack_uci,
                "move_uci": mv.uci(),
            })

        with open(task_file_path, "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=2)
        return len(tasks)


    def process_task_file(self, task_file_path: str, results_file_path: str):
        with open(task_file_path, "r", encoding="utf-8") as f:
            tasks = json.load(f)

        results = []
        for i, task in enumerate(tasks):
            board = chess.Board()
            for m in task["move_stack_uci"]:
                try:
                    board.push(chess.Move.from_uci(m))
                except Exception:
                    pass

            mv = chess.Move.from_uci(task["move_uci"])
            board_before = board.copy()
            board.push(mv)

            pruned_me = self._apply_dark_budget(board.copy())
            my_future = self._peak_coherence_2_ply(pruned_me)

            try:
                board.null()
            except Exception:
                pass

            try:
                board.push(chess.Move.null())
                pruned_them = self._apply_dark_budget(board.copy())
                their_future = self._peak_coherence_2_ply(pruned_them)
                board.pop()
            except Exception:
                their_future = 0.0

            board_after = board.copy()
            D_pack = compute_dark_residue_chess(board_before, board_after, board_before.turn, self.cfg)

            destruction = 0.0
            if self.last_their_future is not None:
                destruction = max(0.0, self.last_their_future - their_future)

            asym_score = (my_future * self.aggression) - their_future
            total_score = asym_score - D_pack["D"] + self.destruction_weight * destruction

            results.append({
                "move_uci": mv.uci(),
                "total_score": total_score,
                "asym_score": asym_score,
                "dark_residue": D_pack,
            })
            self.last_their_future = their_future

            print(f"    ... processed task {i+1}/{len(tasks)}: {mv.uci()} (Score: {total_score:.2f})")

        with open(results_file_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)

# ---------- runner ----------
def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

def run_games(num_games: int, out_dir: str, cfg: dict):
    if cfg["game_type"] != "chess" or chess is None:
        print("Chess not available.")
        return

    adapter = ChessAdapter()
    agent = CoherenceBatchSolver(adapter, cfg)
    easy = SimpleGreedySolver(adapter, cfg)

    ensure_dir(out_dir)
    task_dir = os.path.join(out_dir, "tasks")
    ensure_dir(task_dir)
    task_file = os.path.join(task_dir, "ply_tasks.json")
    results_file = os.path.join(task_dir, "ply_results.json")

    for g in range(num_games):
        board = adapter.new_board()
        agent.reset_game()
        game_log = {"game_index": g, "moves": [], "result": None}
        print(f"\nGame {g+1}/{num_games}...")

        for ply in range(cfg["max_plies"]):
            if adapter.is_game_over(board):
                game_log["result"] = adapter.result(board)
                break

            side = "white" if adapter.side_to_move(board) else "black"
            start = time.time()

            if side == "white":
                ntasks = agent.generate_tasks(board, task_file)
                if ntasks == 0:
                    move, meta = easy.choose_move(board)
                else:
                    agent.process_task_file(task_file, results_file)
                    move, meta = agent_select_best(board, results_file)
            else:
                move, meta = easy.choose_move(board)

            if move is None:
                game_log["result"] = "NoMoveFound"
                break

            fen_before = adapter.fen(board)
            move_s = adapter.serialize_move(board, move)
            adapter.push(board, move)

            end = time.time()
            print(f"  Ply {ply} ({side}): {move_s} in {end-start:.2f}s")

            game_log["moves"].append({
                "ply": ply,
                "side": side,
                "move": move_s,
                "fen_before": fen_before,
                "meta": meta,
            })

        if game_log["result"] is None:
            game_log["result"] = adapter.result(board)

        stamp = datetime.datetime.now().strftime("%Y%m%d")
        dated_dir = os.path.join(out_dir, stamp)
        ensure_dir(dated_dir)
        out_path = os.path.join(dated_dir, f"game_{g:04d}.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(game_log, f, indent=2)
        print(f"[{g+1}/{num_games}] saved {out_path}")

def agent_select_best(board: chess.Board, results_file_path: str):
    with open(results_file_path, "r", encoding="utf-8") as f:
        results = json.load(f)
    if not results:
        legal = list(board.legal_moves)
        return (legal[0], {"reason": "no_results"}) if legal else (None, {"reason": "no_moves"})
    results.sort(key=lambda x: x["total_score"], reverse=True)
    best = results[0]
    return chess.Move.from_uci(best["move_uci"]), {
        "asym_score": best["asym_score"],
        "dark_residue": best["dark_residue"],
        "move_eval": results,
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--games", type=int, default=1)
    parser.add_argument("--out-dir", type=str, default="./batch_runs")
    args = parser.parse_args()
    run_games(args.games, args.out_dir, GAME_CONFIG)

if __name__ == "__main__":
    main()

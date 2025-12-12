#!/usr/bin/env python3
"""
Engram Chess Solver (Pirouette-style)

- Agent: CoherenceBatchSolver with Dark Residue + action engrams
- Opponent: SimpleGreedySolver (fast, 1-ply, D-ignorant)

Each candidate move in the batch gets an "action engram" attached:

    {
        "state_fingerprint": FEN_before,
        "action": move_uci,
        "side_to_move": "white" or "black",
        "K_tau_before": ...,
        "V_Gamma_before": ...,
        "K_tau_after": ...,
        "V_Gamma_after": ...,
        "L_p_before": ...,
        "L_p_after": ...,
        "delta_L_p": ...,
        "CPB_after": K_tau_after / max(V_Gamma_after, eps),
        "class": "laminar" | "constructive" | "turbulent" | "reject",
        "dark_residue": { ... }  # same pack as before
    }

So the solver both plays and emits a dataset usable as a
general "manifold problem" atlas.

Requires: python-chess  (pip install chess)
"""

from __future__ import annotations
import os, json, argparse, datetime, time

# ============================================================
# CONFIG
# ============================================================

GAME_CONFIG = {
    "game_type": "chess",
    "board_size": 8,
    "max_plies": 120,
    "actor_limit": 5,        # Prism pruning for both solvers
    "log_masks": True,

    # Dark Residue (D) Weights
    "D_alpha": 1.0,          # Div(welfare)
    "D_beta": 1.0,           # Ext(risk)
    "D_gamma": 0.7,          # Attention debt
    "D_delta": 0.5,          # Loss of autonomy
    "D_epsilon": 10.0,       # Repetition penalty

    # Dark Budget: restrict 2-ply to these pieces
    "dark_budget_pieces": ["p", "n", "b", "q"],

    # Goal Gradient (Aggression)
    "aggression_factor": 1.2,
    "destruction_weight": 2.0,
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
# (Mostly as in coherence_batch_solver_5.py)
# ============================================================

def _safe_all_squares():
    return range(64)


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
                if 0 <= r < 8:
                    sq = chess.square(f, r)
                    piece = board.piece_at(sq)
                    if piece and piece.piece_type == chess.PAWN and piece.color == color:
                        score += 0.5
    return score


def _opponent_attack_surface(board: chess.Board, color: bool) -> int:
    opp = not color
    total = 0
    for sq in _safe_all_squares():
        piece = board.piece_at(sq)
        if not piece or piece.color != opp:
            continue
        try:
            attacks = board.attacks(sq)
            total += bin(attacks).count("1")
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


def compute_dark_residue_chess(
    board_before: chess.Board,
    board_after: chess.Board,
    acting_color: bool,
    cfg: dict,
) -> dict:
    α = cfg["D_alpha"]
    β = cfg["D_beta"]
    γ = cfg["D_gamma"]
    δ = cfg["D_delta"]

    try:
        ks_before = _king_safety(board_before, acting_color)
        risk_before = _opponent_attack_surface(board_before, acting_color)
        undef_before = _undefended_own_pieces(board_before, acting_color)
        legal_before = _legal_move_count(board_before)

        ks_after = _king_safety(board_after, acting_color)
        risk_after = _opponent_attack_surface(board_after, acting_color)
        undef_after = _undefended_own_pieces(board_after, acting_color)

        board_after.push(chess.Move.null())
        legal_after = _legal_move_count(board_after)
        board_after.pop()
    except Exception:
        # if something goes sideways, mark the move as highly costly
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


# ============================================================
# SHARED PRISM / COHERENCE
# ============================================================

def _chess_actor_mask(board: chess.Board, actor_limit: int):
    """
    Static 0-ply "Prism" evaluation: pick the top-influence pieces.
    """
    actors = []
    for sq in _safe_all_squares():
        try:
            piece = board.piece_at(sq)
        except Exception:
            continue
        if not piece or piece.color != board.turn:
            continue

        try:
            attacks = board.attacks(sq)
            influence = bin(attacks).count("1")
        except Exception:
            influence = 0

        file_idx = chess.square_file(sq)
        rank_idx = chess.square_rank(sq)
        if file_idx in (3, 4):
            influence += 0.5
        if rank_idx in (3, 4):
            influence += 0.5

        actors.append((sq, influence, {"piece": piece.symbol()}))

    actors.sort(key=lambda x: x[1], reverse=True)
    return actors[:actor_limit]


def _peak_coherence_0_ply(board: chess.Board, actor_limit: int) -> float:
    mask = _chess_actor_mask(board, actor_limit)
    if not mask:
        return 0.0
    return mask[0][1]


# ============================================================
# PIRouette QUANTIFIER (K_τ, V_Γ, L_p, class)
# Lightweight, chess-specific instance of GAME-CHESS-002/003 
# ============================================================

def quant_K_tau(board: chess.Board, cfg: dict) -> float:
    """
    Temporal Coherence proxy:
      - activity from Prism
      - king shelter for side to move

    Roughly normalized to [0, ~2]; we don't care about exact scale,
    just consistency across the manifold.
    """
    actor_limit = cfg["actor_limit"]
    me = board.turn
    activity = _peak_coherence_0_ply(board, actor_limit)  # 0 .. ~? (depends on position)
    ks = _king_safety(board, me)                          # 0 .. ~2-ish

    # Very rough normalization; you can tune later
    act_norm = min(1.0, activity / 16.0)
    ks_norm = min(1.0, ks / 3.0)
    return act_norm + ks_norm


def quant_V_Gamma(board: chess.Board, cfg: dict) -> float:
    """
    Temporal Pressure proxy:
      - opponent attack surface on side to move
      - check flag
      - local tempo via mobility

    Again: not absolute, just a consistent "pressure gauge".
    """
    me = board.turn
    risk = _opponent_attack_surface(board, me)
    in_check = 1.0 if board.is_check() else 0.0
    mobility = _legal_move_count(board)

    risk_norm = min(2.0, risk / 16.0)
    mob_norm = min(2.0, mobility / 20.0)

    return in_check + 0.5 * risk_norm + 0.3 * mob_norm


def classify_move(
    K_before: float,
    V_before: float,
    K_after: float,
    V_after: float,
    D: float,
) -> tuple[str, float, float, float, float]:
    """
    Classify the move into laminar / constructive / turbulent / reject.

    Returns:
        class_label, L_p_before, L_p_after, delta_L_p, CPB_after
    """
    L_before = K_before - V_before
    L_after = K_after - V_after
    delta_L = L_after - L_before

    eps = 1e-6
    CPB_after = K_after / max(V_after, eps) if V_after > eps else float("inf")

    # Simple heuristic thresholds; easy to tune
    if delta_L <= 0:
        label = "reject"
    else:
        if D > 1.0:
            label = "turbulent"
        else:
            if 0.8 <= CPB_after <= 1.2:
                label = "laminar"
            elif CPB_after > 1.2:
                label = "constructive"
            else:
                label = "turbulent"

    return label, L_before, L_after, delta_L, CPB_after


def build_action_engram(
    board_before: chess.Board,
    board_after: chess.Board,
    move_uci: str,
    cfg: dict,
    D_pack: dict,
) -> dict:
    """
    Build the full Pirouette-style action engram for a single move.
    """
    K_before = quant_K_tau(board_before, cfg)
    V_before = quant_V_Gamma(board_before, cfg)
    K_after = quant_K_tau(board_after, cfg)
    V_after = quant_V_Gamma(board_after, cfg)

    label, L_before, L_after, delta_L, CPB_after = classify_move(
        K_before, V_before, K_after, V_after, D_pack["D"]
    )

    side_label = "white" if board_before.turn == chess.WHITE else "black"

    return {
        "state_fingerprint": board_before.fen(),
        "action": move_uci,
        "side_to_move": side_label,
        "K_tau_before": K_before,
        "V_Gamma_before": V_before,
        "K_tau_after": K_after,
        "V_Gamma_after": V_after,
        "L_p_before": L_before,
        "L_p_after": L_after,
        "delta_L_p": delta_L,
        "CPB_after": CPB_after,
        "class": label,
        "dark_residue": D_pack,
    }


# ============================================================
# SOLVER 1: "EASY MODE" (fast, greedy, D-ignorant)
# ============================================================

class SimpleGreedySolver:
    def __init__(self, adapter: BaseGameAdapter, cfg: dict):
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

            asym_score = (my_future * self.aggression) - their_future
            total_score = asym_score

            if total_score > best_score:
                best_score = total_score
                best_move = mv

        return best_move, {
            "asym_score": best_score,
            "dark_residue": {"D": 0.0},
        }


# ============================================================
# SOLVER 2: "AGENT" (2-ply, D-aware, action-engrams, batch)
# ============================================================

class CoherenceBatchSolver:
    def __init__(self, adapter: BaseGameAdapter, cfg: dict):
        self.adapter = adapter
        self.cfg = cfg
        self.actor_limit = cfg["actor_limit"]
        self.aggression = cfg.get("aggression_factor", 1.0)
        self.last_their_future = None
        self.destruction_weight = cfg.get("destruction_weight", 1.0)

    def reset_game(self):
        self.last_their_future = None

    def create_actor_mask(self, board):
        return _chess_actor_mask(board, self.actor_limit)

    def _apply_dark_budget(self, board: chess.Board) -> chess.Board:
        """
        Implements the "Dark Budget" / "Presacrifice" idea.
        """
        budget_symbols = self.cfg.get("dark_budget_pieces", [])
        if not budget_symbols:
            return board

        budget_board = board.copy(stack=False)
        budget_board.clear_board()

        for sq in _safe_all_squares():
            piece = board.piece_at(sq)
            if piece and piece.symbol().lower() in budget_symbols:
                budget_board.set_piece_at(sq, piece)

        return budget_board

    def _peak_coherence_2_ply(self, board: chess.Board) -> float:
        """
        2-ply lookahead on the pruned ("dark budget") board.
        """
        try:
            moves = list(self.adapter.legal_moves(board))
        except Exception:
            return 0.0

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
        """
        Writes tasks with history to fix repetition bug.
        """
        actor_mask = self.create_actor_mask(board)
        actor_squares = {sq for (sq, _, _) in actor_mask}
        legal = self.adapter.legal_moves(board)

        move_stack_uci = [mv.uci() for mv in board.move_stack]

        tasks = []
        for mv in legal:
            from_sq = mv.from_square if hasattr(mv, "from_square") else None
            if from_sq is None or from_sq not in actor_squares:
                continue

            tasks.append({
                "move_stack_uci": move_stack_uci,
                "move_uci": mv.uci(),
            })

        with open(task_file_path, "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=2)

        return len(tasks)

    def process_task_file(self, task_file_path: str, results_file_path: str):
        """
        Reads tasks, rebuilds board with history,
        applies Dark Budget, and computes engrams.
        """
        with open(task_file_path, "r", encoding="utf-8") as f:
            tasks = json.load(f)

        results = []

        for i, task in enumerate(tasks):
            # Rehydrate board with full move history
            board = chess.Board()
            for m_uci in task["move_stack_uci"]:
                try:
                    board.push(chess.Move.from_uci(m_uci))
                except Exception:
                    pass

            mv = chess.Move.from_uci(task["move_uci"])

            board_before = board.copy()
            self.adapter.push(board, mv)

            # A) 2-ply on pruned boards
            my_budget_board = self._apply_dark_budget(board.copy())
            my_future = self._peak_coherence_2_ply(my_budget_board)

            try:
                self.adapter.null_move(board)
                their_budget_board = self._apply_dark_budget(board.copy())
                their_future = self._peak_coherence_2_ply(their_budget_board)
                self.adapter.pop(board)
            except Exception:
                their_future = 0.0

            # B) Dark Residue on real boards
            board_after = board.copy()
            acting_color = board_before.turn
            D_pack = compute_dark_residue_chess(
                board_before, board_after, acting_color, self.cfg
            )

            # Repetition penalty
            repetition_cost = 0.0
            if board.is_repetition(2):
                repetition_cost = self.cfg["D_epsilon"] * 0.5
            if board.is_repetition(3):
                repetition_cost = self.cfg["D_epsilon"]

            D_pack["Repetition"] = repetition_cost
            D_pack["D"] += repetition_cost

            destruction = 0.0
            if self.last_their_future is not None:
                destruction = max(0.0, self.last_their_future - their_future)

            # C) Lagrangian-ish score (as in your existing batch solver)
            asym_score = (my_future * self.aggression) - their_future
            total_score = asym_score - D_pack["D"] + self.destruction_weight * destruction

            # D) Action Engram
            engram = build_action_engram(
                board_before, board_after, mv.uci(), self.cfg, D_pack
            )

            self.adapter.pop(board)  # undo mv

            results.append({
                "move_uci": mv.uci(),
                "total_score": total_score,
                "asym_score": asym_score,
                "dark_residue": D_pack,
                "engram": engram,
            })

            self.last_their_future = their_future
            print(
                f"    ... processed task {i+1}/{len(tasks)}: {mv.uci()} "
                f"(Score: {total_score:.2f}, class={engram['class']})"
            )

        with open(results_file_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)

    def select_best_move(self, board: chess.Board, results_file_path: str):
        with open(results_file_path, "r", encoding="utf-8") as f:
            results = json.load(f)

        if not results:
            legal = self.adapter.legal_moves(board)
            if not legal:
                return None, {"reason": "no_moves"}
            # Fallback: any move that doesn't force 3-fold repetition
            safe_move = legal[0]
            for mv in legal:
                board.push(mv)
                if not board.is_repetition(3):
                    safe_move = mv
                    board.pop()
                    break
                board.pop()
            return safe_move, {"reason": "fallback_no_tasks"}

        results.sort(key=lambda x: x["total_score"], reverse=True)
        best_result = results[0]
        best_move = chess.Move.from_uci(best_result["move_uci"])

        meta = {
            "asym_score": best_result["asym_score"],
            "dark_residue": best_result["dark_residue"],
            "engram": best_result["engram"],
            "move_eval": results if self.cfg["log_masks"] else None,
        }
        return best_move, meta


# ============================================================
# RUNNER
# ============================================================

def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


def run_games(num_games: int, out_dir: str, cfg: dict):
    if cfg["game_type"] != "chess":
        raise NotImplementedError("Only chess wired right now.")
    if chess is None:
        print("Chess adapter failed to load. Aborting.")
        return

    adapter = ChessAdapter()
    solver_agent = CoherenceBatchSolver(adapter, cfg)
    solver_easy = SimpleGreedySolver(adapter, cfg)

    ensure_dir(out_dir)
    task_dir = os.path.join(out_dir, "tasks")
    ensure_dir(task_dir)
    task_file = os.path.join(task_dir, "ply_tasks.json")
    results_file = os.path.join(task_dir, "ply_results.json")

    budget = cfg.get("dark_budget_pieces", [])
    if budget:
        print(f"Running with Dark Budget. 2-ply search limited to: {budget}")
    else:
        print("Running with NO Dark Budget. 2-ply search will be slow.")

    for g in range(num_games):
        board = adapter.new_board()
        solver_agent.reset_game()
        game_log = {
            "game_index": g,
            "moves": [],
            "result": None,
            "game_type": cfg["game_type"],
        }
        print(f"\nStarting Game {g+1}/{num_games} (AGENT vs EASY MODE)...")

        for ply in range(cfg["max_plies"]):
            if adapter.is_game_over(board):
                game_log["result"] = adapter.result(board)
                break

            side = "white" if adapter.side_to_move(board) else "black"
            start_time = time.time()

            if side == "white":
                # slow, engram-rich agent
                num_tasks = solver_agent.generate_tasks(board, task_file)
                if num_tasks == 0:
                    legal = adapter.legal_moves(board)
                    if not legal:
                        game_log["result"] = "NoMoveFound"
                        break
                    move, meta = legal[0], {"reason": "fallback_no_tasks"}
                    for mv in legal:
                        board.push(mv)
                        if not board.is_repetition(3):
                            move = mv
                            board.pop()
                            break
                        board.pop()
                else:
                    print(f"  Ply {ply} (AGENT): Generated {num_tasks} tasks. Processing...")
                    solver_agent.process_task_file(task_file, results_file)
                    move, meta = solver_agent.select_best_move(board, results_file)
            else:
                # fast greedy opponent
                move, meta = solver_easy.choose_move(board, log_masks=cfg["log_masks"])

            end_time = time.time()

            if move is None:
                print(f"  Ply {ply} ({side}): No move found.")
                game_log["result"] = "NoMoveFound"
                break

            fen_before = adapter.fen(board)
            move_s = adapter.serialize_move(board, move)
            adapter.push(board, move)

            dr_score = meta.get("dark_residue", {}).get("D", 0.0)
            engram = meta.get("engram")
            class_tag = engram["class"] if engram else "na"
            side_label = "AGENT" if side == "white" else "EASY"

            print(
                f"  Ply {ply} ({side_label}): {move_s:6} "
                f"(Score: {meta.get('asym_score', 0):.2f}, "
                f"D: {dr_score:.2f}, class={class_tag}) "
                f"[Time: {end_time - start_time:.2f}s]"
            )

            game_log["moves"].append({
                "ply": ply,
                "side": side,
                "move": move_s,
                "fen_before": fen_before,
                "score": meta.get("asym_score"),
                "dark_residue": meta.get("dark_residue"),
                "engram": engram,
                "move_eval": meta.get("move_eval"),
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
    parser = argparse.ArgumentParser(description="Engram Chess Solver")
    parser.add_argument("--games", type=int, default=1)
    parser.add_argument("--out-dir", type=str, default="./engram_runs")
    args = parser.parse_args()

    run_games(args.games, args.out_dir, GAME_CONFIG)


if __name__ == "__main__":
    main()

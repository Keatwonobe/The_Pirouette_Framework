#!/usr/bin/env python3
"""
Engine-Lens Chess Solver

White: Standard UCI engine (e.g. Stockfish)
Black: Simple greedy opponent

For each WHITE move we record a Pirouette-style action engram:

    {
        "state_fingerprint": FEN_before,
        "action": move_uci,
        "side_to_move": "white",
        "K_tau_before": ...,
        "V_Gamma_before": ...,
        "K_tau_after": ...,
        "V_Gamma_after": ...,
        "L_p_before": ...,
        "L_p_after": ...,
        "delta_L_p": ...,
        "CPB_after": ...,
        "class": "laminar" | "constructive" | "turbulent" | "reject",
        "dark_residue": {...},
        "engine_cp_after": centipawn_eval (from white POV, None if mate),
        "engine_mate_after": mate_in_n (from white POV, None if not mate),
        "engine_depth": search_depth
    }

So you get a standard chess engine *plus* Pirouette/engram metrics in the
same JSON view you're already using.
"""

from __future__ import annotations
import os, json, argparse, datetime, time

import chess
import chess.engine

# ============================================================
# CONFIG
# ============================================================

GAME_CONFIG = {
    "game_type": "chess",
    "board_size": 8,
    "max_plies": 200,          # bump this up a bit to avoid early "time draws"
    "log_masks": True,

    # Dark Residue (D) Weights
    "D_alpha": 1.0,
    "D_beta": 1.0,
    "D_gamma": 0.7,
    "D_delta": 0.5,
    "D_epsilon": 10.0,        # repetition penalty (unused here, but wired in)

    # Engine config
    "engine_path": "C:/Users/keatw/OneDrive/Documents/Doclab/Big_Datasets/target/stockfish-windows-x86-64-avx2/stockfish/stockfish-windows-x86-64-avx2.exe",   # or full path: "/usr/bin/stockfish", "stockfish.exe", etc.
    "engine_depth": 14,           # search depth for analysis

    # Coherence/Prism config for lens
    "actor_limit": 5,
}
BASELINE_CFG = {
    **GAME_CONFIG,
    "pirouette_prefilter": False,  # plain engine
}

PIR_CFG = {
    **GAME_CONFIG,
    "pirouette_prefilter": True,
    "allowed_classes": ["laminar", "constructive", "turbulent"],  # try variations later
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

    def fen(self, board):
        return board.fen()

    def side_to_move(self, board):
        return board.turn

    def serialize_move(self, board, move):
        try:
            return board.san(move)
        except Exception:
            return move.uci()


# ============================================================
# DARK RESIDUE (chess specialization)
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
        # super costly if something breaks
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
# COHERENCE / PIRouette QUANTIFIERS
# ============================================================

def _chess_actor_mask(board: chess.Board, actor_limit: int):
    actors = []
    for sq in _safe_all_squares():
        piece = board.piece_at(sq)
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

        actors.append((sq, influence))

    actors.sort(key=lambda x: x[1], reverse=True)
    return actors[:actor_limit]


def _peak_coherence_0_ply(board: chess.Board, actor_limit: int) -> float:
    mask = _chess_actor_mask(board, actor_limit)
    if not mask:
        return 0.0
    return mask[0][1]


def quant_K_tau(board: chess.Board, cfg: dict) -> float:
    actor_limit = cfg["actor_limit"]
    me = board.turn
    activity = _peak_coherence_0_ply(board, actor_limit)
    ks = _king_safety(board, me)

    act_norm = min(1.0, activity / 16.0)
    ks_norm = min(1.0, ks / 3.0)
    return act_norm + ks_norm


def quant_V_Gamma(board: chess.Board, cfg: dict) -> float:
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
):
    L_before = K_before - V_before
    L_after = K_after - V_after
    delta_L = L_after - L_before

    eps = 1e-6
    CPB_after = K_after / max(V_after, eps) if V_after > eps else float("inf")

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
# SOLVER: ENGINE WITH PIRouette LENS
# ============================================================

class EngineLensSolver:
    def __init__(self, adapter: ChessAdapter, cfg: dict, engine: chess.engine.SimpleEngine):
        self.adapter = adapter
        self.cfg = cfg
        self.engine = engine
        self.depth = cfg.get("engine_depth", 12)

        # Pirouette prefilter flags
        self.prefilter = cfg.get("pirouette_prefilter", False)
        # Only moves whose engram["class"] is in this set are allowed
        self.allowed_classes = set(cfg.get("allowed_classes", ["laminar", "constructive", "turbulent"]))

    def _classify_all_moves(self, board: chess.Board):
        """
        Build engrams for all legal moves (on copies),
        and return a list of (move, engram).
        """
        candidates = []
        legal_moves = list(board.legal_moves)
        if not legal_moves:
            return candidates

        for mv in legal_moves:
            before = board.copy()
            after = before.copy()
            after.push(mv)

            acting_color = before.turn
            D_pack = compute_dark_residue_chess(before, after, acting_color, self.cfg)
            eng = build_action_engram(before, after, mv.uci(), self.cfg, D_pack)
            eng["engine_cp_after"] = None
            eng["engine_mate_after"] = None
            eng["engine_depth"] = None

            candidates.append((mv, eng))

        return candidates

    def _pick_pirouette_override(self, board: chess.Board, engine_move: chess.Move):
        """
        If prefilter is enabled and the engine's move is in a disallowed class,
        override it with the "best" allowed move by ΔL_p.
        """
        # --- NEW OPTIMIZATION ---
        # If we are not pre-filtering (i.e., this is the 'baseline' solver),
        # we must skip all classification. Just return the engine's move.
        # The engram for this single move will be built later in `choose_move`.
        if not self.prefilter:
            return engine_move, None, None
        # --- END NEW OPTIMIZATION ---
        
        candidates = self._classify_all_moves(board)
        if not candidates:
            return engine_move, None, None  # no override, no engram, no D_pack

        # Find the engine move's engram if present
        engine_engram = None
        for mv, eng in candidates:
            if mv == engine_move:
                engine_engram = eng
                break

        # If engine move is allowed or we’re not filtering, keep it
        # (This 'not self.prefilter' check is now redundant but harmless)
        if not self.prefilter:
            return engine_move, engine_engram, None

        if engine_engram is not None and engine_engram["class"] in self.allowed_classes:
            return engine_move, engine_engram, None

        # Otherwise pick an allowed move with highest ΔL_p
        allowed = [
            (mv, eng) for (mv, eng) in candidates
            if eng["class"] in self.allowed_classes
        ]
        if not allowed:
            # Nothing is allowed, keep engine move anyway
            return engine_move, engine_engram, None

        allowed.sort(key=lambda x: x[1]["delta_L_p"], reverse=True)
        best_mv, best_engram = allowed[0]
        return best_mv, best_engram, None

    def choose_move(self, board: chess.Board):
        """
        Let the engine pick the move, then possibly override it with a
        Pirouette-approved move, then compute full engram for the final
        chosen move. Does NOT mutate the shared board.
        """
        if board.is_game_over():
            return None, {"reason": "game_over"}

        legal_moves = list(board.legal_moves)
        if not legal_moves:
            return None, {"reason": "no_moves"}

        # ---- 1) Plain engine choice (no root_moves trickery) ----
        info = self.engine.analyse(board, chess.engine.Limit(depth=self.depth))
        pv = info.get("pv")
        if pv and len(pv) > 0:
            engine_move = pv[0]
        else:
            engine_move = legal_moves[0]

        if engine_move not in legal_moves:
            engine_move = legal_moves[0]

        # ---- 2) Optional Pirouette override on a COPY ----
        override_move, cached_engram, _ = self._pick_pirouette_override(board, engine_move)
        final_move = override_move if override_move is not None else engine_move

        # ---- 3) Build full engram for the final move ----
        board_before = board.copy()
        board_after = board_before.copy()
        board_after.push(final_move)

        acting_color = board_before.turn
        D_pack = compute_dark_residue_chess(board_before, board_after, acting_color, self.cfg)

        # If we already computed an engram for this move in _pick_pirouette_override,
        # reuse it; otherwise build fresh.
        if cached_engram is not None and cached_engram["action"] == final_move.uci():
            engram = cached_engram
            engram["dark_residue"] = D_pack
        else:
            engram = build_action_engram(board_before, board_after, final_move.uci(), self.cfg, D_pack)

        # Engine eval from WHITE POV
        score = info.get("score")
        cp_eval = None
        mate_eval = None
        if score is not None:
            pov = score.pov(chess.WHITE)
            if pov.is_mate():
                mate_eval = pov.mate()
            else:
                cp_eval = pov.score(mate_score=100000)

        engram["engine_cp_after"] = cp_eval
        engram["engine_mate_after"] = mate_eval
        engram["engine_depth"] = self.depth

        meta = {
            "engine_cp": cp_eval,
            "engine_mate": mate_eval,
            "dark_residue": D_pack,
            "engram": engram,
        }

        return final_move, meta

# ============================================================
# OPPONENT: SIMPLE GREEDY (0-ply coherence)
# ============================================================

class SimpleGreedySolver:
    def __init__(self, adapter: ChessAdapter, cfg: dict):
        self.adapter = adapter
        self.cfg = cfg
        self.actor_limit = cfg["actor_limit"]

    def choose_move(self, board: chess.Board):
        legal = self.adapter.legal_moves(board)
        if not legal:
            return None, {"reason": "no_moves"}

        best_move = legal[0]
        best_score = -1e9

        for mv in legal:
            self.adapter.push(board, mv)
            val = _peak_coherence_0_ply(board, self.actor_limit)
            self.adapter.pop(board)
            if val > best_score:
                best_score = val
                best_move = mv

        return best_move, {"coherence": best_score}


# ============================================================
# RUNNER
# ============================================================

def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

def run_match(games: int, out_dir: str, base_cfg: dict, pir_cfg: dict):
    adapter = ChessAdapter()
    ensure_dir(out_dir)

    engine_path = base_cfg["engine_path"]
    print(f"Starting engine from: {engine_path}")

    with chess.engine.SimpleEngine.popen_uci(engine_path) as engine:
        # Two solvers sharing the same underlying engine
        baseline = EngineLensSolver(adapter, base_cfg, engine)
        pirouette = EngineLensSolver(adapter, pir_cfg, engine)

        scores = {"baseline": 0.0, "pirouette": 0.0, "draws": 0}

        for g in range(games):
            board = adapter.new_board()
            game_log = {
                "game_index": g,
                "moves": [],
                "result": None,
                "baseline_color": "white" if g % 2 == 0 else "black",
            }

            print(f"\n=== Game {g+1}/{games} ===")
            print(f"Baseline is {game_log['baseline_color']}")

            for ply in range(base_cfg["max_plies"]):
                if adapter.is_game_over(board):
                    game_log["result"] = adapter.result(board)
                    break

                side_white = adapter.side_to_move(board)  # True if white
                # Determine which solver moves this ply
                if side_white:
                    moving = "white"
                else:
                    moving = "black"

                if (moving == "white" and game_log["baseline_color"] == "white") or \
                   (moving == "black" and game_log["baseline_color"] == "black"):
                    solver = baseline
                    label = "baseline"
                else:
                    solver = pirouette
                    label = "pirouette"

                move, meta = solver.choose_move(board)
                if move is None:
                    game_log["result"] = meta.get("reason", "NoMoveFound")
                    break

                fen_before = adapter.fen(board)
                san = adapter.serialize_move(board, move)
                adapter.push(board, move)

                game_log["moves"].append({
                    "ply": ply,
                    "side": "white" if side_white else "black",
                    "who": label,
                    "move": san,
                    "fen_before": fen_before,
                    "engine_cp": meta.get("engine_cp"),
                    "engine_mate": meta.get("engine_mate"),
                    "dark_residue": meta.get("dark_residue"),
                    "engram": meta.get("engram"),
                })

            # Final result
            if game_log["result"] is None:
                game_log["result"] = adapter.result(board)

            res = game_log["result"]
            print(f"Game {g+1} result: {res}")
            if res == "1-0":
                if game_log["baseline_color"] == "white":
                    scores["baseline"] += 1.0
                else:
                    scores["pirouette"] += 1.0
            elif res == "0-1":
                if game_log["baseline_color"] == "black":
                    scores["baseline"] += 1.0
                else:
                    scores["pirouette"] += 1.0
            else:
                scores["draws"] += 1

            # Save the game log
            stamp = datetime.datetime.now().strftime("%Y%m%d")
            game_dir = os.path.join(out_dir, stamp)
            ensure_dir(game_dir)
            out_path = os.path.join(game_dir, f"match_game_{g:04d}.json")
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(game_log, f, indent=2)
            print(f"Saved: {out_path}")

        print("\n=== Match Summary ===")
        print(f"Baseline score   : {scores['baseline']}")
        print(f"Pirouette score  : {scores['pirouette']}")
        print(f"Draws            : {scores['draws']}")


def run_games(games: int, out_dir: str, cfg: dict):
    adapter = ChessAdapter()
    ensure_dir(out_dir)

    engine_path = cfg["engine_path"]
    print(f"Starting engine from: {engine_path}")

    with chess.engine.SimpleEngine.popen_uci(engine_path) as engine:
        solver_white = EngineLensSolver(adapter, cfg, engine)
        solver_black = SimpleGreedySolver(adapter, cfg)

        for g in range(games):
            board = adapter.new_board()
            game_log = {
                "game_index": g,
                "moves": [],
                "result": None,
                "game_type": cfg["game_type"],
            }

            print(f"\n=== Game {g+1}/{games} (ENGINE+LENS vs GREEDY) ===")

            for ply in range(cfg["max_plies"]):
                if adapter.is_game_over(board):
                    game_log["result"] = adapter.result(board)
                    break

                side = "white" if adapter.side_to_move(board) else "black"
                start_time = time.time()

                if side == "white":
                    move, meta = solver_white.choose_move(board)
                else:
                    move, meta = solver_black.choose_move(board)

                end_time = time.time()

                if move is None:
                    print(f"  Ply {ply} ({side}): no move (reason={meta.get('reason')})")
                    game_log["result"] = meta.get("reason", "NoMoveFound")
                    break

                fen_before = adapter.fen(board)
                move_s = adapter.serialize_move(board, move)
                adapter.push(board, move)

                if side == "white":
                    cp = meta.get("engine_cp")
                    mate = meta.get("engine_mate")
                    engram = meta.get("engram")
                    dr_score = meta.get("dark_residue", {}).get("D", 0.0)
                    class_tag = engram["class"] if engram else "na"

                    print(
                        f"  Ply {ply} (ENGINE): {move_s:6} "
                        f"[cp={cp}, mate={mate}, D={dr_score:.2f}, class={class_tag}] "
                        f"({end_time - start_time:.2f}s)"
                    )
                else:
                    engram = None
                    dr_score = None
                    print(
                        f"  Ply {ply} (GREEDY): {move_s:6} "
                        f"(coh={meta.get('coherence', 0):.2f}) "
                        f"({end_time - start_time:.2f}s)"
                    )

                game_log["moves"].append({
                    "ply": ply,
                    "side": side,
                    "move": move_s,
                    "fen_before": fen_before,
                    "engine_cp": meta.get("engine_cp") if side == "white" else None,
                    "engine_mate": meta.get("engine_mate") if side == "white" else None,
                    "dark_residue": meta.get("dark_residue"),
                    "engram": engram,
                })

            if game_log["result"] is None:
                game_log["result"] = adapter.result(board)

            print(f"Game {g+1} result: {game_log['result']}")

            stamp = datetime.datetime.now().strftime("%Y%m%d")
            game_dir = os.path.join(out_dir, stamp)
            ensure_dir(game_dir)
            out_path = os.path.join(game_dir, f"game_{g:04d}.json")
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(game_log, f, indent=2)
            print(f"Saved: {out_path}")


def main():
    parser = argparse.ArgumentParser(description="Engine + Pirouette Lens Chess Runner")
    parser.add_argument("--games", type=int, default=1)
    parser.add_argument("--out-dir", type=str, default="./engine_lens_runs")
    args = parser.parse_args()

    run_match(args.games, args.out_dir, base_cfg=BASELINE_CFG, pir_cfg=PIR_CFG)


if __name__ == "__main__":
    main()

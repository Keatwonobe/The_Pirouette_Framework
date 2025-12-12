#!/usr/bin/env python3
"""
Coherence Batch Solver (Task-File Architecture)

<...omitted...>
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
    "actor_limit": 5,
    "log_masks": True,
    "D_alpha": 1.0, "D_beta": 1.0, "D_gamma": 0.7,
    "D_delta": 0.5, "D_epsilon": 10.0,
    
    # <--- CHANGED: Your "Dark Budget" is now defined
    # We will only run the 2-ply search on this "core" of pieces
    "dark_budget_pieces": ["p", "n", "b", "q"], # Pawns, Knights, Bishops, Queen
    
    # <--- CHANGED: New "Aggression" factor to fix "coward" logic
    "aggression_factor": 1.2 # Weights our future coherence higher
}

# (Adapter classes are unchanged)
# ============================================================
# ADAPTERS
# ============================================================

try:
    import chess
except ImportError:
    print("Failed to import 'chess'. Please install it: pip install chess")
    chess = None

class BaseGameAdapter:
    def new_board(self): raise NotImplementedError
    def is_game_over(self, board): raise NotImplementedError
    def result(self, board): raise NotImplementedError
    def legal_moves(self, board): raise NotImplementedError
    def push(self, board, move): raise NotImplementedError
    def pop(self, board): raise NotImplementedError
    def null_move(self, board): raise NotImplementedError
    def serialize_move(self, board, move): return str(move)
    def fen(self, board): return ""
    def side_to_move(self, board): raise NotImplementedError

class ChessAdapter(BaseGameAdapter):
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

# (Dark Residue functions are unchanged)
# ============================================================
# DARK RESIDUE (chess specialization)
# ============================================================
def _safe_all_squares(): return range(64)
def _king_safety(board: chess.Board, color: bool) -> float:
    king_sq = board.king(color)
    if king_sq is None: return 0.0
    file_idx, rank_idx = chess.square_file(king_sq), chess.square_rank(king_sq)
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
        if not piece or piece.color != opp: continue
        try: total += bin(board.attacks(sq)).count('1')
        except Exception: pass
    return total
def _undefended_own_pieces(board: chess.Board, color: bool) -> int:
    me, opp = color, not color
    count = 0
    for sq in _safe_all_squares():
        piece = board.piece_at(sq)
        if not piece or piece.color != me: continue
        if board.is_attacked_by(opp, sq) and not board.is_attacked_by(me, sq):
            count += 1
    return count
def _legal_move_count(board: chess.Board) -> int:
    try: return len(list(board.legal_moves))
    except Exception: return 0
def compute_dark_residue_chess(board_before: chess.Board, board_after: chess.Board, acting_color: bool, cfg: dict) -> dict:
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
        board_after.push(chess.Move.null())
        legal_after = _legal_move_count(board_after)
        board_after.pop()
    except Exception as e:
        return {"D": 100.0, "Div_welfare": 0.0, "Ext_risk": 0.0, "Attention_debt": 0.0, "Loss_autonomy": 0.0, "Repetition": 0.0}
    div_welfare = max(0.0, (ks_before - ks_after))
    ext_risk = max(0.0, (risk_after - risk_before))
    attention_debt = max(0.0, (undef_after - undef_before))
    loss_autonomy = max(0.0, (legal_before - legal_after))
    D = (α * div_welfare + β * ext_risk + γ * attention_debt + δ * loss_autonomy)
    return {"D": D, "Div_welfare": div_welfare, "Ext_risk": ext_risk, "Attention_debt": attention_debt, "Loss_autonomy": loss_autonomy, "Repetition": 0.0}


# ============================================================
# NEW/CHANGED: BATCH SOLVER
# ============================================================

class CoherenceBatchSolver:
    def __init__(self, adapter: BaseGameAdapter, cfg: dict):
        self.adapter = adapter
        self.cfg = cfg
        self.actor_limit = cfg["actor_limit"]
        self.aggression = cfg.get("aggression_factor", 1.0)

    # --- Actor Mask (Prism) ---
    def _chess_actor_mask(self, board: chess.Board):
        # (This is the same as before)
        actors = []
        for sq in _safe_all_squares():
            try: piece = board.piece_at(sq)
            except Exception: continue 
            if not piece or piece.color != board.turn: continue
            try:
                attacks = board.attacks(sq)
                influence = bin(attacks).count('1')
            except Exception: influence = 0
            file_idx, rank_idx = chess.square_file(sq), chess.square_rank(sq)
            if file_idx in (3, 4): influence += 0.5
            if rank_idx in (3, 4): influence += 0.5
            actors.append((sq, influence, {"piece": piece.symbol()}))
        actors.sort(key=lambda x: x[1], reverse=True)
        return actors[: self.actor_limit]

    def create_actor_mask(self, board):
        return self._chess_actor_mask(board)

    # --- <NEW> Dark Budget Pruning ---
    def _apply_dark_budget(self, board: chess.Board) -> chess.Board:
        """
        Implements the "Dark Budget" / "Presacrifice" idea.
        It returns a new board containing *only* the "core"
        pieces defined in the budget.
        """
        budget_symbols = self.cfg.get("dark_budget_pieces", [])
        if not budget_symbols:
            return board # No budget, return the full board

        # Create a new, empty board but keep castling/turn info
        budget_board = board.copy(stack=False)
        budget_board.clear_board() # Remove all pieces
        
        for sq in _safe_all_squares():
            piece = board.piece_at(sq)
            if piece and piece.symbol().lower() in budget_symbols:
                # This piece is in the budget, add it to the new board
                budget_board.set_piece_at(sq, piece)
                
        return budget_board

    # --- This is the restored 2-ply (slow) search ---
    def _peak_coherence_2_ply(self, board):
        """ This is the "extra dimension" restored """
        # We pass a copy, so it's safe to mutate
        
        # CRITICAL: Materialize list to prevent re-entrancy
        try:
            moves = list(self.adapter.legal_moves(board))
        except Exception:
            return 0.0 # Board is in an invalid state (e.g., no king)
            
        if not moves:
            return 0.0
            
        best = -1e9
        for mv in moves:
            self.adapter.push(board, mv)
            # Use the 0-ply "static" evaluation
            mask = self.create_actor_mask(board)
            val = mask[0][1] if mask else 0.0
            self.adapter.pop(board)
            if val > best:
                best = val
        return best

    # --- CHANGED: Step 1 - Generate Tasks (With History) ---
    def generate_tasks(self, board: chess.Board, task_file_path: str) -> int:
        """
        Generates the list of tasks (candidate moves)
        and writes them to the dump file.
        
        <-- CHANGED: Now includes the full move history for repetition.
        """
        actor_mask = self.create_actor_mask(board)
        actor_squares = {sq for (sq, _, _) in actor_mask}
        legal = self.adapter.legal_moves(board)
        
        # Get the full history to pass to the task processor
        move_stack_uci = [mv.uci() for mv in board.move_stack]
        
        tasks = []
        for mv in legal:
            from_sq = mv.from_square if hasattr(mv, "from_square") else None
            # Prune to only our "laser-pointed" pieces
            if from_sq is None or from_sq not in actor_squares:
                continue
            
            tasks.append({
                "move_stack_uci": move_stack_uci, # <-- PASS HISTORY
                "move_uci": mv.uci(),
            })

        with open(task_file_path, "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=2)
            
        return len(tasks)

    # --- CHANGED: Step 2 - Process Tasks (With History & Budget) ---
    def process_task_file(self, task_file_path: str, results_file_path: str):
        """
        Reads the task file, runs the *expensive* analysis
        for each task, and writes to the results file.
        
        <-- CHANGED: Rebuilds board from history & uses Dark Budget.
        """
        with open(task_file_path, "r", encoding="utf-8") as f:
            tasks = json.load(f)
            
        results = []
        
        for i, task in enumerate(tasks):
            # <--- FIX 1 (REPETITION): Re-hydrate board *with history*
            board = chess.Board() # Start from default position
            for m_uci in task["move_stack_uci"]:
                try:
                    board.push(chess.Move.from_uci(m_uci))
                except Exception:
                    pass # Ignore illegal move in history (shouldn't happen)
            # --- END FIX 1 ---
            
            mv = chess.Move.from_uci(task["move_uci"])
            
            # --- This is the expensive 2-ply work ---
            board_before = board.copy()
            self.adapter.push(board, mv) # Mutate the board
            
            # <--- FIX 2 (PERFORMANCE): Apply "Dark Budget" ---
            my_budget_board = self._apply_dark_budget(board.copy())
            
            # A) Calculate my future (2-ply on pruned board)
            my_future = self._peak_coherence_2_ply(my_budget_board)

            # B) Calculate their future (2-ply on pruned board)
            try:
                self.adapter.null_move(board)
                their_budget_board = self._apply_dark_budget(board.copy())
                their_future = self._peak_coherence_2_ply(their_budget_board)
                self.adapter.pop(board) # pop null
            except Exception:
                their_future = 0.0
            # --- END FIX 2 ---

            # C) Calculate Dark Residue (on the *real* boards)
            board_after = board.copy()
            acting_color = board_before.turn
            D_pack = compute_dark_residue_chess(board_before, board_after, acting_color, self.cfg)

            # D) Add Repetition Penalty (this will work now)
            repetition_cost = 0.0
            if board.is_repetition(2):
                repetition_cost = self.cfg["D_epsilon"] * 0.5
            if board.is_repetition(3):
                repetition_cost = self.cfg["D_epsilon"]
            
            D_pack["Repetition"] = repetition_cost
            D_pack["D"] += repetition_cost
            
            # E) Final Score
            # <--- FIX 3 (LOGIC): Apply "Aggression" to fix "coward" logic
            asym_score = (my_future * self.aggression) - their_future
            total_score = asym_score - D_pack["D"]
            
            self.adapter.pop(board) # undo mv
            # --- End expensive work ---
            
            results.append({
                "move_uci": mv.uci(),
                "total_score": total_score,
                "asym_score": asym_score, # Log the *new* asymmetric score
                "dark_residue": D_pack
            })
            print(f"    ... processed task {i+1}/{len(tasks)}: {mv.uci()} (Score: {total_score:.2f})")

        with open(results_file_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)

    # --- Step 3 - Select Best Move (Unchanged) ---
    def select_best_move(self, board: chess.Board, results_file_path: str):
        """
        Reads the results file and picks the winning move.
        """
        with open(results_file_path, "r", encoding="utf-8") as f:
            results = json.load(f)
            
        if not results:
            legal = self.adapter.legal_moves(board)
            if not legal:
                return None, {"reason": "no_moves"}
            # Fallback: find *any* move not causing repetition
            safe_move = legal[0]
            for mv in legal:
                if not board.is_repetition(3):
                    safe_move = mv
                    break
            return safe_move, {"reason": "fallback_no_tasks"}
            
        results.sort(key=lambda x: x["total_score"], reverse=True)
        
        best_result = results[0]
        best_move = chess.Move.from_uci(best_result["move_uci"])
        
        # Prepare the metadata for logging
        meta = {
            "asym_score": best_result["asym_score"],
            "dark_residue": best_result["dark_residue"],
            "move_eval": results if self.cfg["log_masks"] else None
        }
        
        return best_move, meta

# ============================================================
# RUNNER (Unchanged, but added print for budget)
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
    solver = CoherenceBatchSolver(adapter, cfg)

    ensure_dir(out_dir)
    
    task_dir = os.path.join(out_dir, "tasks")
    ensure_dir(task_dir)
    task_file = os.path.join(task_dir, "ply_tasks.json")
    results_file = os.path.join(task_dir, "ply_results.json")

    # <--- NEW: Announce the budget
    budget = cfg.get("dark_budget_pieces", [])
    if budget:
        print(f"Running with Dark Budget. 2-ply search limited to: {budget}")
    else:
        print("Running with NO Dark Budget. 2-ply search will be slow.")
    # ---

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
            
            start_time = time.time()
            
            num_tasks = solver.generate_tasks(board, task_file)
            if num_tasks == 0:
                legal = adapter.legal_moves(board)
                if not legal:
                    game_log["result"] = "NoMoveFound"
                    break
                # Fallback: find *any* move not causing repetition
                move = legal[0]
                meta = {"reason": "fallback_no_tasks"}
                for mv in legal:
                    board.push(mv)
                    if not board.is_repetition(3):
                        move = mv
                        board.pop()
                        break
                    board.pop()
            else:
                print(f"  Ply {ply} ({side}): Generated {num_tasks} tasks. Processing...")
                solver.process_task_file(task_file, results_file)
                move, meta = solver.select_best_move(board, results_file)
            
            end_time = time.time()
            
            if move is None:
                print(f"  Ply {ply} ({side}): No move found.")
                game_log["result"] = "NoMoveFound"
                break

            fen_before = adapter.fen(board)
            move_s = adapter.serialize_move(board, move)
            adapter.push(board, move)
            
            dr_score = meta.get('dark_residue', {}).get('D', 0)
            print(f"  Ply {ply} ({side}): {move_s:6} (Score: {meta.get('asym_score', 0):.2f}, D: {dr_score:.2f}) [Time: {end_time-start_time:.2f}s]")

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
    parser = argparse.ArgumentParser(description="Coherence Batch Solver")
    parser.add_argument("--games", type=int, default=1) # Default to 1, this is slow!
    parser.add_argument("--out-dir", type=str, default="./batch_runs")
    args = parser.parse_args()

    run_games(args.games, args.out_dir, GAME_CONFIG)


if __name__ == "__main__":
    main()
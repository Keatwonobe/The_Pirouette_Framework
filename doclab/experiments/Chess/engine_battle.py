#!/usr/bin/env python3
"""
Chess Engine Battle Arena

Pits the Coherence Chess Solver against traditional engines:
- Stockfish (if available)
- Random player (baseline)
- Greedy material player (simple heuristic)

Tests coherence theory against computational brute force.
"""

import chess
import chess.engine
import chess.pgn
from coherence_chess import CoherenceChessSolver
from inhuman_coherence import InhumanCoherenceSolver, WinningCoherenceSolver
import subprocess
import time
import os
from typing import Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class EngineType(Enum):
    COHERENCE = "coherence"
    INHUMAN_COHERENCE = "inhuman_coherence"
    STOCKFISH = "stockfish"
    RANDOM = "random"
    GREEDY = "greedy"


@dataclass
class BattleResult:
    white: str
    black: str
    result: str  # "1-0", "0-1", "1/2-1/2"
    moves: int
    reason: str
    pgn: str
    white_type: EngineType
    black_type: EngineType


class RandomPlayer:
    """Baseline: plays random legal moves"""
    
    def __init__(self):
        self.name = "Random Player"
    
    def select_move(self, board: chess.Board) -> chess.Move:
        import random
        return random.choice(list(board.legal_moves))


class GreedyMaterialPlayer:
    """Simple heuristic: maximize material"""
    
    def __init__(self):
        self.name = "Greedy Material Player"
        self.piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0
        }
    
    def select_move(self, board: chess.Board) -> chess.Move:
        """Select move that maximizes material gain"""
        best_move = None
        best_score = float('-inf')
        
        for move in board.legal_moves:
            score = 0
            
            # Capture value
            if board.is_capture(move):
                captured = board.piece_at(move.to_square)
                if captured:
                    score += self.piece_values[captured.piece_type]
            
            # Check bonus
            board.push(move)
            if board.is_check():
                score += 0.5
            
            # Simple position score
            score += self._count_material(board, board.turn) * 0.01
            
            board.pop()
            
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move if best_move else list(board.legal_moves)[0]
    
    def _count_material(self, board: chess.Board, color: chess.Color) -> int:
        """Count total material for a color"""
        total = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece and piece.color == color:
                total += self.piece_values[piece.piece_type]
        return total


class StockfishPlayer:
    """Interface to Stockfish engine"""
    
    def __init__(self, path="/usr/games/stockfish", time_limit=0.1, depth=10):
        self.name = "Stockfish"
        self.path = path
        self.time_limit = time_limit
        self.depth = depth
        self.engine = None
        self._check_available()
    
    def _check_available(self):
        """Check if Stockfish is available"""
        try:
            result = subprocess.run(
                [self.path, '--help'],
                capture_output=True,
                timeout=2
            )
            self.available = result.returncode == 0
            if self.available:
                self.engine = chess.engine.SimpleEngine.popen_uci(self.path)
        except Exception as e:
            print(f"Stockfish not available: {e}")
            self.available = False
    
    def select_move(self, board: chess.Board) -> chess.Move:
        """Get move from Stockfish"""
        if not self.available or not self.engine:
            raise RuntimeError("Stockfish not available")
        
        result = self.engine.play(
            board,
            chess.engine.Limit(time=self.time_limit, depth=self.depth)
        )
        return result.move
    
    def close(self):
        """Clean up engine"""
        if self.engine:
            self.engine.quit()


class BattleArena:
    """Manages battles between different chess engines"""
    
    def __init__(self):
        self.results = []
    
    def create_player(self, engine_type: EngineType, **kwargs):
        """Factory for creating players"""
        if engine_type == EngineType.COHERENCE:
            return CoherenceChessSolver(D_max=0.5, base_depth=2)
        elif engine_type == EngineType.INHUMAN_COHERENCE:
            return WinningCoherenceSolver(coherence_purity=1.0)
        elif engine_type == EngineType.RANDOM:
            return RandomPlayer()
        elif engine_type == EngineType.GREEDY:
            return GreedyMaterialPlayer()
        elif engine_type == EngineType.STOCKFISH:
            return StockfishPlayer(**kwargs)
        else:
            raise ValueError(f"Unknown engine type: {engine_type}")
    
    def play_game(self, white_type: EngineType, black_type: EngineType,
                  max_moves: int = 100, verbose: bool = True) -> BattleResult:
        """
        Play a single game between two engines
        """
        # Create players
        white = self.create_player(white_type)
        black = self.create_player(black_type)
        
        white_name = getattr(white, 'name', white_type.value.title())
        black_name = getattr(black, 'name', black_type.value.title())
        
        if verbose:
            print("\n" + "="*70)
            print(f"BATTLE: {white_name} (White) vs {black_name} (Black)")
            print("="*70 + "\n")
        
        board = chess.Board()
        move_history = []
        
        start_time = time.time()
        
        result_str = "1/2-1/2"  # Default to draw
        reason = "Unknown"
        
        for move_num in range(max_moves):
            if board.is_game_over():
                break
            
            # Select move
            current_player = white if board.turn == chess.WHITE else black
            current_type = white_type if board.turn == chess.WHITE else black_type
            
            try:
                # Different interfaces for different player types
                if current_type in [EngineType.COHERENCE, EngineType.INHUMAN_COHERENCE]:
                    move, metrics = current_player.select_best_move(
                        board, move_history, verbose=False
                    )
                else:
                    move = current_player.select_move(board)
                
                if verbose and move_num < 20:  # Show first 20 moves
                    side = "White" if board.turn else "Black"
                    print(f"Move {move_num + 1} ({side}): {board.san(move)}")
                
                board.push(move)
                move_history.append(move)
                
            except Exception as e:
                print(f"Error on move {move_num + 1}: {e}")
                result_str = "0-1" if board.turn == chess.WHITE else "1-0"
                reason = f"Error: {str(e)}"
                break
        
        else:
            # Game completed normally
            if board.is_checkmate():
                result_str = "0-1" if board.turn == chess.WHITE else "1-0"
                reason = "Checkmate"
            elif board.is_stalemate():
                result_str = "1/2-1/2"
                reason = "Stalemate"
            elif board.is_insufficient_material():
                result_str = "1/2-1/2"
                reason = "Insufficient material"
            elif board.can_claim_fifty_moves():
                result_str = "1/2-1/2"
                reason = "Fifty-move rule"
            elif board.can_claim_threefold_repetition():
                result_str = "1/2-1/2"
                reason = "Threefold repetition"
            elif move_num >= max_moves - 1:
                result_str = "1/2-1/2"
                reason = f"Max moves ({max_moves}) reached"
            else:
                result_str = "1/2-1/2"
                reason = "Draw"
        
        elapsed = time.time() - start_time
        
        # Create PGN
        game = chess.pgn.Game()
        game.headers["Event"] = "Coherence Battle Arena"
        game.headers["White"] = white_name
        game.headers["Black"] = black_name
        game.headers["Result"] = result_str
        
        node = game
        board_copy = chess.Board()
        for move in move_history:
            node = node.add_variation(move)
            board_copy.push(move)
        
        pgn_str = str(game)
        
        if verbose:
            print(f"\nGame over: {result_str}")
            print(f"Reason: {reason}")
            print(f"Moves: {len(move_history)}")
            print(f"Time: {elapsed:.2f}s")
            print("="*70 + "\n")
        
        result = BattleResult(
            white=white_name,
            black=black_name,
            result=result_str,
            moves=len(move_history),
            reason=reason,
            pgn=pgn_str,
            white_type=white_type,
            black_type=black_type
        )
        
        self.results.append(result)
        
        # Cleanup
        if isinstance(white, StockfishPlayer):
            white.close()
        if isinstance(black, StockfishPlayer):
            black.close()
        
        return result
    
    def play_tournament(self, engine_types: list, games_per_matchup: int = 3):
        """
        Round-robin tournament
        """
        print("\n" + "="*70)
        print("COHERENCE BATTLE TOURNAMENT")
        print("="*70 + "\n")
        
        matchups = []
        for i, white_type in enumerate(engine_types):
            for black_type in engine_types[i+1:]:
                matchups.append((white_type, black_type))
        
        print(f"Tournament: {len(matchups)} matchups, {games_per_matchup} games each")
        print(f"Total games: {len(matchups) * games_per_matchup * 2}\n")  # *2 for reversed colors
        
        for white_type, black_type in matchups:
            print(f"\nMatchup: {white_type.value} vs {black_type.value}")
            print("-" * 70)
            
            for game_num in range(games_per_matchup):
                # Play with both color assignments
                print(f"\nGame {game_num*2 + 1}:")
                self.play_game(white_type, black_type, verbose=False)
                
                print(f"\nGame {game_num*2 + 2}:")
                self.play_game(black_type, white_type, verbose=False)
        
        self.print_tournament_results()
    
    def print_tournament_results(self):
        """Print tournament statistics"""
        print("\n" + "="*70)
        print("TOURNAMENT RESULTS")
        print("="*70 + "\n")
        
        # Calculate statistics by engine type
        stats = {}
        for result in self.results:
            for color, etype in [(result.white, result.white_type), 
                                 (result.black, result.black_type)]:
                if etype not in stats:
                    stats[etype] = {'wins': 0, 'draws': 0, 'losses': 0, 'games': 0}
                
                stats[etype]['games'] += 1
                
                if color == result.white:
                    if result.result == "1-0":
                        stats[etype]['wins'] += 1
                    elif result.result == "0-1":
                        stats[etype]['losses'] += 1
                    else:
                        stats[etype]['draws'] += 1
                else:
                    if result.result == "0-1":
                        stats[etype]['wins'] += 1
                    elif result.result == "1-0":
                        stats[etype]['losses'] += 1
                    else:
                        stats[etype]['draws'] += 1
        
        # Print standings
        print("Standings:")
        print("-" * 70)
        print(f"{'Engine':<25} {'W':>5} {'D':>5} {'L':>5} {'Games':>7} {'Score':>7}")
        print("-" * 70)
        
        for etype in sorted(stats.keys(), key=lambda e: 
                           stats[e]['wins'] + stats[e]['draws']*0.5, reverse=True):
            s = stats[etype]
            score = s['wins'] + s['draws'] * 0.5
            print(f"{etype.value:<25} {s['wins']:>5} {s['draws']:>5} {s['losses']:>5} "
                  f"{s['games']:>7} {score:>7.1f}")
        
        print("\n")


def quick_battle():
    """Quick battle between coherence and simple opponents"""
    arena = BattleArena()
    
    print("\n" + "="*70)
    print("QUICK BATTLE: Coherence vs Simple Opponents")
    print("="*70)
    
    # Coherence vs Random
    print("\n### Battle 1: Coherence vs Random ###")
    result1 = arena.play_game(EngineType.COHERENCE, EngineType.RANDOM, 
                              max_moves=50, verbose=True)
    
    # Coherence vs Greedy
    print("\n### Battle 2: Coherence vs Greedy Material ###")
    result2 = arena.play_game(EngineType.COHERENCE, EngineType.GREEDY,
                              max_moves=50, verbose=True)
    
    # Inhuman Coherence vs Normal Coherence
    print("\n### Battle 3: Inhuman Coherence vs Normal Coherence ###")
    result3 = arena.play_game(EngineType.INHUMAN_COHERENCE, EngineType.COHERENCE,
                              max_moves=50, verbose=True)
    
    # Save PGNs
    output_dir = "./outputs"
    for i, result in enumerate([result1, result2, result3], 1):
        path = os.path.join(output_dir, f"battle_{i}_{result.white.lower().replace(' ', '_')}_vs_{result.black.lower().replace(' ', '_')}.pgn")
        with open(path, 'w') as f:
            f.write(result.pgn)
        print(f"Saved game to {path}")
    
    return arena


def stockfish_battle():
    """Battle against Stockfish if available"""
    arena = BattleArena()
    
    # Check if Stockfish is available
    try:
        stockfish = StockfishPlayer(time_limit=0.1, depth=5)  # Weak Stockfish
        if not stockfish.available:
            print("Stockfish not available. Skipping Stockfish battles.")
            return None
        stockfish.close()
    except Exception:
        print("Stockfish not available. Skipping Stockfish battles.")
        return None
    
    print("\n" + "="*70)
    print("STOCKFISH CHALLENGE")
    print("Coherence vs Stockfish (depth 5, 0.1s per move)")
    print("="*70)
    
    # Coherence vs Stockfish
    result = arena.play_game(
        EngineType.COHERENCE, 
        EngineType.STOCKFISH,
        max_moves=80,
        verbose=True
    )
    
    # Save PGN
    output_dir = ".outputs"
    path = os.path.join(output_dir, "battle_coherence_vs_stockfish.pgn")
    with open(path, 'w') as f:
        f.write(result.pgn)
    print(f"\nSaved game to {path}")
    
    return arena


def main():
    """Run all battles"""
    
    print("\n" + "="*70)
    print("CHESS ENGINE BATTLE ARENA")
    print("Testing Coherence Theory Against Traditional Engines")
    print("="*70)
    
    # Quick battles
    print("\n### PHASE 1: Quick Battles ###")
    arena = quick_battle()
    
    # Try Stockfish
    print("\n### PHASE 2: Stockfish Challenge ###")
    stockfish_arena = stockfish_battle()
    
    if stockfish_arena:
        arena.results.extend(stockfish_arena.results)
    
    # Summary
    print("\n" + "="*70)
    print("BATTLE ARENA COMPLETE")
    print("="*70)
    print("\nAll game PGNs saved to .outputs/")
    print("\nKey Findings:")
    print("  • Coherence solver uses fundamentally different evaluation")
    print("  • Performance reveals if coherence correlates with winning")
    print("  • Battles show where coherence theory succeeds/fails")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
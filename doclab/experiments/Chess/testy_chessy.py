import chess
import chess.engine

# Use the EXACT same path from your main script
STOCKFISH_PATH = "C:/Users/keatw/OneDrive/Documents/Doclab/Big_Datasets/target/stockfish-windows-x86-64-avx2/stockfish/stockfish-windows-x86-64-avx2.exe"

print(f"Attempting to start engine from: {STOCKFISH_PATH}")

try:
    with chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH) as engine:
        print("\n--- Engine Started Successfully! ---")
        
        info = engine.analyse(chess.Board(), chess.engine.Limit(depth=10))
        score = info["score"].relative.score()
        
        print(f"\nEngine analysis complete.")
        print(f"Initial board score: {score} cp")
        print("\n--- Test PASSED! ---")

except Exception as e:
    print(f"\n--- Test FAILED! ---")
    print(f"An error occurred: {e}")

input("\nPress Enter to exit...")

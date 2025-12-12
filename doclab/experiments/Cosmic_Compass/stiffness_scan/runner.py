import subprocess
import time
import sys
import os

# Name of your simulation script
SCRIPT_NAME = "stiffness_scan_2.py"
# Time to wait between restarts (in seconds) to prevent CPU thrashing
RESTART_DELAY = 5

def run_simulation():
    print(f"--- [WATCHDOG] Starting {SCRIPT_NAME} ---")
    while True:
        try:
            # Run the script as a subprocess
            # sys.executable ensures we use the same Python interpreter (e.g., inside a venv)
            process = subprocess.run([sys.executable, SCRIPT_NAME])
            
            # Check exit code
            if process.returncode == 0:
                print("--- [WATCHDOG] Simulation finished successfully! ---")
                break
            else:
                print(f"--- [WATCHDOG] Process crashed with exit code {process.returncode}. ---")
                print(f"--- [WATCHDOG] Restarting in {RESTART_DELAY} seconds... ---")
                time.sleep(RESTART_DELAY)
                
        except KeyboardInterrupt:
            print("\n--- [WATCHDOG] Stopped by user. ---")
            break
        except Exception as e:
            print(f"--- [WATCHDOG] Error running subprocess: {e}")
            break

if __name__ == "__main__":
    if not os.path.exists(SCRIPT_NAME):
        print(f"Error: Could not find {SCRIPT_NAME} in the current directory.")
    else:
        run_simulation()
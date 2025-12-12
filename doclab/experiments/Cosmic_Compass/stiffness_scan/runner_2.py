#!/usr/bin/env python3
"""
Pirouette Simulation Runner
Monitors and automatically restarts crashed simulations
"""
import subprocess
import time
import sys
import os
import signal
from datetime import datetime
import psutil

SIMULATION_SCRIPT = "stiffness_scan_5.py"
MAX_RESTARTS = 100
RESTART_DELAY = 5  # seconds
HEALTH_CHECK_INTERVAL = 60  # seconds
MAX_MEMORY_GB = 12  # Kill if exceeds this

class SimulationRunner:
    def __init__(self):
        self.restart_count = 0
        self.start_time = time.time()
        self.process = None
        self.running = True
        
        # Set up signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle interruption gracefully"""
        print("\n[Runner] Interrupt received. Stopping simulation...")
        self.running = False
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                print("[Runner] Force killing process...")
                self.process.kill()
        sys.exit(0)
    
    def log(self, message):
        """Log with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")
    
    def check_memory_usage(self):
        """Check if simulation is using too much memory"""
        if not self.process:
            return False
        
        try:
            proc = psutil.Process(self.process.pid)
            mem_info = proc.memory_info()
            mem_gb = mem_info.rss / (1024**3)
            
            if mem_gb > MAX_MEMORY_GB:
                self.log(f"WARNING: Memory usage {mem_gb:.2f} GB exceeds limit {MAX_MEMORY_GB} GB")
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
        
        return False
    
    def monitor_process(self):
        """Monitor the running process"""
        last_check = time.time()
        
        while self.process.poll() is None and self.running:
            time.sleep(1)
            
            # Periodic health checks
            if time.time() - last_check > HEALTH_CHECK_INTERVAL:
                if self.check_memory_usage():
                    self.log("Killing simulation due to excessive memory usage")
                    self.process.terminate()
                    return "memory_exceeded"
                
                last_check = time.time()
        
        if not self.running:
            return "stopped"
        
        return_code = self.process.returncode
        return return_code
    
    def run_simulation(self):
        """Run the simulation script"""
        self.log(f"Starting simulation (attempt {self.restart_count + 1}/{MAX_RESTARTS})")
        
        try:
            self.process = subprocess.Popen(
                [sys.executable, SIMULATION_SCRIPT],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            # Stream output
            for line in self.process.stdout:
                print(line, end='')
                sys.stdout.flush()
            
            result = self.monitor_process()
            
            if result == "stopped":
                return False
            elif result == "memory_exceeded":
                self.log("Simulation exceeded memory limit")
                return True
            elif result == 0:
                self.log("Simulation completed successfully!")
                return False
            else:
                self.log(f"Simulation crashed with code {result}")
                return True
                
        except Exception as e:
            self.log(f"Error running simulation: {e}")
            return True
    
    def run(self):
        """Main runner loop"""
        self.log("="*60)
        self.log("PIROUETTE SIMULATION RUNNER")
        self.log(f"Script: {SIMULATION_SCRIPT}")
        self.log(f"Max restarts: {MAX_RESTARTS}")
        self.log(f"Restart delay: {RESTART_DELAY}s")
        self.log("="*60)
        
        if not os.path.exists(SIMULATION_SCRIPT):
            self.log(f"ERROR: Cannot find {SIMULATION_SCRIPT}")
            sys.exit(1)
        
        while self.running and self.restart_count < MAX_RESTARTS:
            should_restart = self.run_simulation()
            
            if not should_restart:
                break
            
            self.restart_count += 1
            
            if self.restart_count < MAX_RESTARTS:
                self.log(f"Restarting in {RESTART_DELAY} seconds...")
                time.sleep(RESTART_DELAY)
            else:
                self.log("Maximum restart attempts reached")
                break
        
        elapsed = time.time() - self.start_time
        self.log("="*60)
        self.log(f"Runner finished after {elapsed/3600:.2f} hours")
        self.log(f"Total restarts: {self.restart_count}")
        self.log("="*60)

if __name__ == "__main__":
    runner = SimulationRunner()
    runner.run()
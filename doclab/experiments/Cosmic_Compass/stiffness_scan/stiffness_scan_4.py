import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import time
import pickle
import os
import signal
import sys
import gc
import traceback
from dataclasses import dataclass, asdict
from typing import List, Tuple, Optional
import psutil
import logging

# ==============================================================================
# WINDOWS UNICODE FIX - Enable UTF-8 support
# ==============================================================================
if sys.platform == 'win32':
    # Set console to UTF-8 mode
    os.system('chcp 65001 > nul')
    # Reconfigure stdout/stderr for UTF-8
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
# ==============================================================================

# --- CONFIGURATION ---
LATTICE_SIZE = 16
N_THERM = 1000
N_MEAS = 100
N_DECORR = 10
GRID_RES = 25
CHECKPOINT_FILE = "pirouette_checkpoint.pkl"
LOG_FILE = "pirouette_simulation.log"

# Batch processing config
BATCH_SIZE = 5  # Process 5 parameter points before checkpointing
MAX_MEMORY_PERCENT = 75  # Pause if memory usage exceeds this
RETRY_ATTEMPTS = 3  # Retry failed points this many times

# Setup logging with UTF-8 encoding for Windows compatibility
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Fix StreamHandler encoding for Windows
import sys
if sys.platform == 'win32':
    # Reconfigure StreamHandler to use UTF-8
    for handler in logging.root.handlers:
        if isinstance(handler, logging.StreamHandler) and handler.stream == sys.stderr:
            handler.stream.reconfigure(encoding='utf-8')

@dataclass
class SimulationPoint:
    """Represents a single parameter point"""
    i: int
    j: int
    m_sq: float
    lambda_4: float
    xi: float = 0.0
    attempts: int = 0
    error: Optional[str] = None
    
    def __hash__(self):
        return hash((self.i, self.j))

class PirouetteLattice:
    def __init__(self, L, m_sq, lambda_4):
        self.L = L
        self.m_sq = m_sq
        self.lambda_4 = lambda_4
        self.phi = np.random.normal(0, 0.5, (L, L, L, L)).astype(np.float32)
        self.mask_even = self._make_checkerboard(0)
        self.mask_odd = self._make_checkerboard(1)
        
        # Pre-compute rolled masks for neighbor access (memory trade-off for speed)
        self._precompute_neighbor_masks()

    def _make_checkerboard(self, offset):
        coords = np.indices(self.phi.shape)
        return (np.sum(coords, axis=0) % 2) == offset
    
    def _precompute_neighbor_masks(self):
        """Pre-compute neighbor access patterns to avoid repeated rolling"""
        self.neighbor_masks = {}
        for mask_type in ['even', 'odd']:
            mask = self.mask_even if mask_type == 'even' else self.mask_odd
            neighbors = []
            for d in range(4):
                neighbors.append((np.roll(mask, 1, axis=d), d, 1))
                neighbors.append((np.roll(mask, -1, axis=d), d, -1))
            self.neighbor_masks[mask_type] = neighbors

    def update(self, steps=1):
        """Vectorized Metropolis-Hastings Update with error handling"""
        try:
            for _ in range(steps):
                for mask_type, mask in [('even', self.mask_even), ('odd', self.mask_odd)]:
                    phi_old = self.phi[mask]
                    
                    # Use pre-computed neighbor masks
                    neigh_sum = np.zeros_like(phi_old)
                    for neighbor_mask, d, direction in self.neighbor_masks[mask_type]:
                        neigh_sum += self.phi[neighbor_mask]
                    
                    # Propose update
                    delta = np.random.normal(0, 0.4, size=phi_old.shape).astype(np.float32)
                    phi_new = phi_old + delta
                    
                    # Action change
                    dS_kin = 4.0 * (phi_new**2 - phi_old**2) - (phi_new - phi_old) * neigh_sum
                    dS_mass = 0.5 * self.m_sq * (phi_new**2 - phi_old**2)
                    dS_int = (self.lambda_4 / 24.0) * (phi_new**4 - phi_old**4)
                    dS = dS_kin + dS_mass + dS_int
                    
                    # Metropolis acceptance
                    prob = np.exp(-np.clip(dS, -20, 20))  # Clip to prevent overflow
                    accept_mask = (np.random.rand(*dS.shape) < prob)
                    self.phi[mask] = np.where(accept_mask, phi_new, phi_old)
        except Exception as e:
            logger.error(f"Error during lattice update: {e}")
            raise

    def measure_correlation_stiffness(self):
        """Extract correlation length with improved error handling"""
        try:
            phi_bar = self.phi - np.mean(self.phi)
            corrs = []
            max_r = self.L // 2
            
            for r in range(max_r):
                c_sum = 0
                for d in range(4):
                    c_sum += np.mean(phi_bar * np.roll(phi_bar, -r, axis=d))
                corrs.append(c_sum / 4.0)
            
            corrs = np.array(corrs)
            
            # Handle edge cases
            if len(corrs) == 0 or corrs[0] == 0:
                return 0.0
            
            corrs /= corrs[0]
            
            # Exponential fit
            def model(r, xi, A):
                return A * np.exp(-r / xi)
            
            popt, _ = curve_fit(
                model, np.arange(max_r), corrs,
                p0=[1.0, 1.0],
                bounds=([0.01, 0], [self.L, 5.0]),
                maxfev=5000
            )
            return max(0.0, popt[0])  # Ensure non-negative
            
        except Exception as e:
            logger.warning(f"Correlation fit failed: {e}")
            return 0.0
    
    def cleanup(self):
        """Explicitly clean up large arrays"""
        del self.phi
        del self.mask_even
        del self.mask_odd
        if hasattr(self, 'neighbor_masks'):
            del self.neighbor_masks
        gc.collect()

class ResourceMonitor:
    """Monitor system resources and prevent crashes"""
    
    @staticmethod
    def check_memory():
        """Return True if memory usage is acceptable"""
        mem = psutil.virtual_memory()
        return mem.percent < MAX_MEMORY_PERCENT
    
    @staticmethod
    def wait_for_memory():
        """Wait until memory becomes available"""
        while not ResourceMonitor.check_memory():
            mem = psutil.virtual_memory()
            logger.warning(f"High memory usage: {mem.percent:.1f}%. Waiting...")
            time.sleep(5)
            gc.collect()

class BatchProcessor:
    """Process simulation points in batches for efficiency"""
    
    def __init__(self, lattice_size, n_therm, n_meas, n_decorr):
        self.lattice_size = lattice_size
        self.n_therm = n_therm
        self.n_meas = n_meas
        self.n_decorr = n_decorr
    
    def process_point(self, point: SimulationPoint) -> SimulationPoint:
        """Process a single parameter point with error handling"""
        lat = None
        try:
            # Check memory before starting
            ResourceMonitor.wait_for_memory()
            
            logger.info(f"Processing point ({point.i},{point.j}): m²={point.m_sq:.3f}, λ={point.lambda_4:.3f}")
            
            lat = PirouetteLattice(
                L=self.lattice_size,
                m_sq=point.m_sq,
                lambda_4=point.lambda_4
            )
            
            # Thermalization
            lat.update(self.n_therm)
            
            # Measurements
            xi_vals = []
            for meas in range(self.n_meas):
                lat.update(self.n_decorr)
                xi = lat.measure_correlation_stiffness()
                if not np.isnan(xi) and xi > 0:
                    xi_vals.append(xi)
                
                # Periodic memory check during long measurements
                if meas % 20 == 0:
                    gc.collect()
            
            # Store result
            if xi_vals:
                point.xi = float(np.mean(xi_vals))
                logger.info(f"  → ξ = {point.xi:.4f} (from {len(xi_vals)} measurements)")
            else:
                point.xi = 0.0
                logger.warning(f"  → No valid measurements")
            
            point.error = None
            return point
            
        except Exception as e:
            error_msg = f"{type(e).__name__}: {str(e)}"
            point.error = error_msg
            logger.error(f"  → Failed: {error_msg}")
            logger.debug(traceback.format_exc())
            return point
        
        finally:
            # Always clean up
            if lat is not None:
                lat.cleanup()
            gc.collect()
            time.sleep(0.1)  # Brief cooldown
    
    def process_batch(self, points: List[SimulationPoint]) -> List[SimulationPoint]:
        """Process a batch of points"""
        results = []
        for point in points:
            result = self.process_point(point)
            results.append(result)
        return results

class SimulationManager:
    def __init__(self):
        self.m_range = np.linspace(-1.2, 0.0, GRID_RES)
        self.l_range = np.linspace(1.0, 5.0, GRID_RES)
        self.results = np.zeros((GRID_RES, GRID_RES))
        self.error_map = np.zeros((GRID_RES, GRID_RES), dtype=object)
        self.completed_points = {}  # dict of SimulationPoint objects
        self.failed_points = []
        self.start_time = time.time()
        self.total_points = GRID_RES * GRID_RES
        self.batch_processor = BatchProcessor(LATTICE_SIZE, N_THERM, N_MEAS, N_DECORR)
        
        # Set up signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle interruption gracefully"""
        logger.warning("Interrupt received. Saving state...")
        self.save_checkpoint()
        sys.exit(0)
    
    def load_checkpoint(self):
        """Load checkpoint with backward compatibility"""
        if os.path.exists(CHECKPOINT_FILE):
            logger.info(f"Loading checkpoint: {CHECKPOINT_FILE}")
            try:
                with open(CHECKPOINT_FILE, 'rb') as f:
                    data = pickle.load(f)
                
                # Handle old checkpoint format
                if 'completed_points' in data:
                    self.completed_points = data['completed_points']
                    self.results = data['results']
                    self.error_map = data.get('error_map', self.error_map)
                    self.failed_points = data.get('failed_points', [])
                else:
                    # Convert old format
                    self.results = data['results']
                    old_completed = data.get('completed', set())
                    for (i, j) in old_completed:
                        point = SimulationPoint(
                            i=i, j=j,
                            m_sq=self.m_range[i],
                            lambda_4=self.l_range[j],
                            xi=self.results[i, j]
                        )
                        self.completed_points[(i, j)] = point
                
                completed = len(self.completed_points)
                failed = len(self.failed_points)
                logger.info(f"Resuming: {completed}/{self.total_points} completed, {failed} failed")
                
            except Exception as e:
                logger.error(f"Corrupt checkpoint: {e}. Starting fresh.")
                logger.debug(traceback.format_exc())
    
    def save_checkpoint(self):
        """Save checkpoint with metadata"""
        try:
            data = {
                'results': self.results,
                'error_map': self.error_map,
                'completed_points': self.completed_points,
                'failed_points': self.failed_points,
                'timestamp': time.time(),
                'config': {
                    'L': LATTICE_SIZE,
                    'N_THERM': N_THERM,
                    'N_MEAS': N_MEAS,
                    'GRID_RES': GRID_RES
                }
            }
            
            # Atomic write: write to temp file then rename
            temp_file = CHECKPOINT_FILE + '.tmp'
            with open(temp_file, 'wb') as f:
                pickle.dump(data, f)
            os.replace(temp_file, CHECKPOINT_FILE)
            
            logger.info(f"Checkpoint saved: {len(self.completed_points)}/{self.total_points} complete")
            
        except Exception as e:
            logger.error(f"Failed to save checkpoint: {e}")
    
    def generate_work_queue(self) -> List[SimulationPoint]:
        """Generate list of remaining work"""
        queue = []
        for i, m_sq in enumerate(self.m_range):
            for j, lam in enumerate(self.l_range):
                idx = (i, j)
                
                # Skip if already completed successfully
                if idx in self.completed_points and self.completed_points[idx].error is None:
                    continue
                
                # Retry failed points if under retry limit
                point = self.completed_points.get(idx)
                if point and point.error and point.attempts >= RETRY_ATTEMPTS:
                    continue
                
                # Create or update point
                if point:
                    point.attempts += 1
                else:
                    point = SimulationPoint(i=i, j=j, m_sq=m_sq, lambda_4=lam)
                
                queue.append(point)
        
        return queue
    
    def run(self):
        """Main execution loop with batch processing"""
        logger.info("=" * 60)
        logger.info(f"PIROUETTE FIELD VALIDATION (L={LATTICE_SIZE}^4)")
        logger.info(f"Config: Therm={N_THERM}, Meas={N_MEAS}, Grid={GRID_RES}x{GRID_RES}")
        logger.info(f"Batch size: {BATCH_SIZE}, Max memory: {MAX_MEMORY_PERCENT}%")
        logger.info("=" * 60)
        
        # Generate work queue
        work_queue = self.generate_work_queue()
        total_work = len(work_queue)
        
        if total_work == 0:
            logger.info("All points completed!")
            self.analyze_ratios()
            return
        
        logger.info(f"Work queue: {total_work} points remaining")
        
        # Process in batches
        batch_count = 0
        for batch_start in range(0, total_work, BATCH_SIZE):
            batch_end = min(batch_start + BATCH_SIZE, total_work)
            batch = work_queue[batch_start:batch_end]
            batch_count += 1
            
            logger.info(f"\n--- Batch {batch_count}/{(total_work + BATCH_SIZE - 1) // BATCH_SIZE} ---")
            
            # Process batch
            results = self.batch_processor.process_batch(batch)
            
            # Store results
            for point in results:
                self.completed_points[(point.i, point.j)] = point
                self.results[point.i, point.j] = point.xi
                if point.error:
                    self.error_map[point.i, point.j] = point.error
                    self.failed_points.append(point)
            
            # Save after each batch
            self.save_checkpoint()
            
            # Progress update
            completed = len([p for p in self.completed_points.values() if p.error is None])
            failed = len([p for p in self.completed_points.values() if p.error is not None])
            progress = (completed / self.total_points) * 100
            elapsed = time.time() - self.start_time
            
            logger.info(f"Progress: {completed}/{self.total_points} ({progress:.1f}%) | "
                       f"Failed: {failed} | Elapsed: {elapsed/3600:.2f}h")
            
            # Memory cleanup between batches
            gc.collect()
            time.sleep(0.5)
        
        logger.info("\n" + "=" * 60)
        logger.info("SIMULATION COMPLETE")
        logger.info("=" * 60)
        
        # Final analysis
        self.analyze_ratios()
        self.generate_report()
    
    def analyze_ratios(self):
        """Find Standard Model candidates"""
        logger.info("\n--- RATIO ANALYSIS (Target: 1 : 1.79 : 2.31) ---")
        
        # Collect valid data points
        data = []
        for point in self.completed_points.values():
            if point.error is None and point.xi > 0.1:
                data.append({
                    'xi': point.xi,
                    'm': point.m_sq,
                    'l': point.lambda_4,
                    'i': point.i,
                    'j': point.j
                })
        
        if not data:
            logger.warning("No valid data points for analysis")
            return
        
        data.sort(key=lambda x: x['xi'])
        logger.info(f"Valid points: {len(data)}")
        
        # Search for ratio matches
        candidates = []
        tolerance = 0.03
        
        for base in data:
            xi_3 = base['xi']
            target_2 = xi_3 * 1.79
            target_1 = xi_3 * 2.31
            
            matches_2 = [d for d in data if abs(d['xi'] - target_2) / target_2 < tolerance]
            matches_1 = [d for d in data if abs(d['xi'] - target_1) / target_1 < tolerance]
            
            if matches_2 and matches_1:
                candidates.append({
                    'SU3': base,
                    'SU2': matches_2[0],
                    'U1': matches_1[0]
                })
        
        logger.info(f"Found {len(candidates)} candidate geometries (tolerance={tolerance*100}%)")
        
        if candidates:
            # Show top candidate
            c = candidates[0]
            logger.info("\nTop Candidate:")
            logger.info(f"  SU(3): ξ={c['SU3']['xi']:.4f} (m²={c['SU3']['m']:.3f}, λ={c['SU3']['l']:.3f})")
            logger.info(f"  SU(2): ξ={c['SU2']['xi']:.4f} (m²={c['SU2']['m']:.3f}, λ={c['SU2']['l']:.3f}) "
                       f"→ Ratio: {c['SU2']['xi']/c['SU3']['xi']:.3f}")
            logger.info(f"  U(1):  ξ={c['U1']['xi']:.4f} (m²={c['U1']['m']:.3f}, λ={c['U1']['l']:.3f}) "
                       f"→ Ratio: {c['U1']['xi']/c['SU3']['xi']:.3f}")
            
            # Generate plot
            self.plot_results(c)
    
    def plot_results(self, candidate=None):
        """Generate visualization"""
        try:
            plt.figure(figsize=(12, 10))
            
            # Main stiffness map
            plt.subplot(2, 2, 1)
            im = plt.imshow(self.results, origin='lower', aspect='auto',
                           extent=[self.l_range.min(), self.l_range.max(),
                                  self.m_range.min(), self.m_range.max()],
                           cmap='viridis')
            plt.colorbar(im, label=r'Stiffness $\xi$')
            plt.xlabel(r'$\lambda$')
            plt.ylabel(r'$m^2$')
            plt.title('Pirouette Stiffness Map')
            
            if candidate:
                plt.scatter(candidate['SU3']['l'], candidate['SU3']['m'],
                           c='red', marker='x', s=100, label='SU(3)')
                plt.scatter(candidate['SU2']['l'], candidate['SU2']['m'],
                           c='orange', marker='x', s=100, label='SU(2)')
                plt.scatter(candidate['U1']['l'], candidate['U1']['m'],
                           c='white', marker='x', s=100, label='U(1)')
                plt.legend()
            
            # Error map
            plt.subplot(2, 2, 2)
            error_count = np.zeros_like(self.results)
            for i in range(GRID_RES):
                for j in range(GRID_RES):
                    if self.error_map[i, j]:
                        error_count[i, j] = 1
            plt.imshow(error_count, origin='lower', aspect='auto',
                      extent=[self.l_range.min(), self.l_range.max(),
                             self.m_range.min(), self.m_range.max()],
                      cmap='Reds')
            plt.xlabel(r'$\lambda$')
            plt.ylabel(r'$m^2$')
            plt.title('Failed Points')
            
            # Histogram of xi values
            plt.subplot(2, 2, 3)
            valid_xi = self.results[self.results > 0]
            if len(valid_xi) > 0:
                plt.hist(valid_xi, bins=50, alpha=0.7)
                plt.xlabel(r'$\xi$')
                plt.ylabel('Count')
                plt.title('Distribution of Stiffness Values')
                plt.yscale('log')
            
            # Progress/completion map
            plt.subplot(2, 2, 4)
            completion = np.zeros_like(self.results)
            for (i, j), point in self.completed_points.items():
                if point.error is None:
                    completion[i, j] = 1
            plt.imshow(completion, origin='lower', aspect='auto',
                      extent=[self.l_range.min(), self.l_range.max(),
                             self.m_range.min(), self.m_range.max()],
                      cmap='Greens')
            plt.xlabel(r'$\lambda$')
            plt.ylabel(r'$m^2$')
            plt.title('Completed Points')
            
            plt.tight_layout()
            plt.savefig('pirouette_results.png', dpi=150)
            logger.info("Saved plot: pirouette_results.png")
            plt.show()
            
        except Exception as e:
            logger.error(f"Plotting failed: {e}")
    
    def generate_report(self):
        """Generate summary report"""
        completed = len([p for p in self.completed_points.values() if p.error is None])
        failed = len([p for p in self.completed_points.values() if p.error is not None])
        elapsed = time.time() - self.start_time
        
        report = f"""
{'='*60}
SIMULATION REPORT
{'='*60}
Configuration:
  Lattice size: {LATTICE_SIZE}^4
  Thermalization: {N_THERM} sweeps
  Measurements: {N_MEAS}
  Grid resolution: {GRID_RES} x {GRID_RES}
  Batch size: {BATCH_SIZE}

Results:
  Total points: {self.total_points}
  Completed: {completed} ({100*completed/self.total_points:.1f}%)
  Failed: {failed} ({100*failed/self.total_points:.1f}%)
  
Performance:
  Total time: {elapsed/3600:.2f} hours
  Avg time per point: {elapsed/max(completed,1):.1f} seconds

Output files:
  - {CHECKPOINT_FILE} (checkpoint data)
  - {LOG_FILE} (detailed log)
  - pirouette_results.png (visualization)
{'='*60}
"""
        logger.info(report)
        
        with open('pirouette_report.txt', 'w') as f:
            f.write(report)

if __name__ == "__main__":
    sim = SimulationManager()
    sim.load_checkpoint()
    sim.run()
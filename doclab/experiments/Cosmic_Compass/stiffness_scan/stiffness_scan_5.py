import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import time
import pickle
import os
import sys
import gc
import traceback
from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Set
import psutil
import logging

# --- CONFIGURATION ---
LATTICE_SIZE = 16
N_THERM = 1000
N_MEAS = 100
N_DECORR = 10

# ADAPTIVE SCANNING PARAMETERS
COARSE_RES = 15          # Initial coarse grid (15x15 = 225 points)
FINE_RES_PER_CELL = 4    # Subdivide interesting cells into 4x4 = 16 points
MIN_XI_THRESHOLD = 0.3   # Only refine cells with xi > this
REFINE_DEPTH = 5         # How many levels of refinement

# Target ratios for your paper validation
TARGET_RATIO_1 = 1.79    # SU(2)/SU(3)
TARGET_RATIO_2 = 2.31    # U(1)/SU(3)
RATIO_TOLERANCE = 0.10   # 10% tolerance for finding candidates

CHECKPOINT_FILE = "pirouette_adaptive_checkpoint.pkl"
LOG_FILE = "pirouette_adaptive.log"
BATCH_SIZE = 1
MAX_MEMORY_PERCENT = 75
RETRY_ATTEMPTS = 3

# Windows-safe logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class GridCell:
    """Represents a region of parameter space that can be subdivided"""
    m_min: float
    m_max: float
    l_min: float
    l_max: float
    level: int = 0  # Refinement level (0 = coarse, 1+ = refined)
    points: List['SimulationPoint'] = field(default_factory=list)
    avg_xi: float = 0.0
    is_interesting: bool = False
    
    def subdivide(self, res: int) -> List['GridCell']:
        """Split this cell into res x res subcells"""
        m_vals = np.linspace(self.m_min, self.m_max, res + 1)
        l_vals = np.linspace(self.l_min, self.l_max, res + 1)
        
        subcells = []
        for i in range(res):
            for j in range(res):
                subcells.append(GridCell(
                    m_min=m_vals[i],
                    m_max=m_vals[i+1],
                    l_min=l_vals[j],
                    l_max=l_vals[j+1],
                    level=self.level + 1
                ))
        return subcells
    
    def center(self) -> Tuple[float, float]:
        """Get center point of cell"""
        return ((self.m_min + self.m_max) / 2, 
                (self.l_min + self.l_max) / 2)

@dataclass
class SimulationPoint:
    """Single parameter point to evaluate"""
    m_sq: float
    lambda_4: float
    xi: float = 0.0
    attempts: int = 0
    error: Optional[str] = None
    cell: Optional[GridCell] = None
    
    def __hash__(self):
        return hash((round(self.m_sq, 6), round(self.lambda_4, 6)))

class PirouetteLattice:
    """Same as before but streamlined"""
    def __init__(self, L, m_sq, lambda_4):
        self.L = L
        self.m_sq = m_sq
        self.lambda_4 = lambda_4
        self.phi = np.random.normal(0, 0.5, (L, L, L, L)).astype(np.float32)
        self.mask_even = self._make_checkerboard(0)
        self.mask_odd = self._make_checkerboard(1)

    def _make_checkerboard(self, offset):
        coords = np.indices(self.phi.shape)
        return (np.sum(coords, axis=0) % 2) == offset

    def update(self, steps=1):
        try:
            for _ in range(steps):
                for mask in [self.mask_even, self.mask_odd]:
                    phi_old = self.phi[mask]
                    neigh_sum = np.zeros_like(phi_old)
                    for d in range(4):
                        neigh_sum += self.phi[np.roll(mask, 1, axis=d)]
                        neigh_sum += self.phi[np.roll(mask, -1, axis=d)]
                    
                    delta = np.random.normal(0, 0.4, size=phi_old.shape).astype(np.float32)
                    phi_new = phi_old + delta
                    
                    dS = (4.0 * (phi_new**2 - phi_old**2) - (phi_new - phi_old) * neigh_sum +
                          0.5 * self.m_sq * (phi_new**2 - phi_old**2) +
                          (self.lambda_4 / 24.0) * (phi_new**4 - phi_old**4))
                    
                    prob = np.exp(-np.clip(dS, -20, 20))
                    accept_mask = (np.random.rand(*dS.shape) < prob)
                    self.phi[mask] = np.where(accept_mask, phi_new, phi_old)
        except Exception as e:
            logger.error(f"Lattice update error: {e}")
            raise

    def measure_correlation_stiffness(self):
        try:
            phi_bar = self.phi - np.mean(self.phi)
            corrs = []
            max_r = self.L // 2
            
            for r in range(max_r):
                c_sum = sum(np.mean(phi_bar * np.roll(phi_bar, -r, axis=d)) 
                           for d in range(4))
                corrs.append(c_sum / 4.0)
            
            corrs = np.array(corrs)
            if len(corrs) == 0 or corrs[0] == 0:
                return 0.0
            
            corrs /= corrs[0]
            
            def model(r, xi, A):
                return A * np.exp(-r / xi)
            
            popt, _ = curve_fit(model, np.arange(max_r), corrs,
                              p0=[1.0, 1.0], bounds=([0.01, 0], [self.L, 5.0]),
                              maxfev=5000)
            return max(0.0, popt[0])
        except:
            return 0.0
    
    def cleanup(self):
        del self.phi
        del self.mask_even
        del self.mask_odd
        gc.collect()

class AdaptiveScanner:
    """Adaptive fractal scanning for efficient parameter space exploration"""
    
    def __init__(self, m_range, l_range):
        self.m_range = m_range
        self.l_range = l_range
        self.all_points = {}  # Dict[hash, SimulationPoint]
        self.cells = []  # List of all cells
        self.refinement_queue = []  # Cells waiting to be refined
        self.completed_points = set()  # Hashes of completed points
        
        # Statistics
        self.points_by_level = {0: 0, 1: 0, 2: 0}  # Track points per refinement level
    
    def initialize_coarse_grid(self, res):
        """Create initial coarse grid"""
        logger.info(f"Initializing {res}x{res} coarse grid...")
        
        m_cells = np.linspace(self.m_range[0], self.m_range[1], res + 1)
        l_cells = np.linspace(self.l_range[0], self.l_range[1], res + 1)
        
        # Create coarse cells
        for i in range(res):
            for j in range(res):
                cell = GridCell(
                    m_min=m_cells[i], m_max=m_cells[i+1],
                    l_min=l_cells[j], l_max=l_cells[j+1],
                    level=0
                )
                
                # Sample center of each cell
                m_c, l_c = cell.center()
                point = SimulationPoint(m_sq=m_c, lambda_4=l_c, cell=cell)
                cell.points.append(point)
                self.all_points[hash(point)] = point
                self.points_by_level[0] += 1
                
                self.cells.append(cell)
        
        logger.info(f"Created {len(self.cells)} coarse cells with {len(self.all_points)} points")
    
    def mark_interesting_cells(self, threshold=MIN_XI_THRESHOLD):
        """Mark cells with high stiffness as interesting"""
        interesting_count = 0
        
        for cell in self.cells:
            if cell.level >= REFINE_DEPTH:
                continue  # Already at max refinement
            
            # Check if any point in cell has high xi
            xi_vals = [p.xi for p in cell.points if p.xi > 0 and p.error is None]
            
            if xi_vals:
                cell.avg_xi = np.mean(xi_vals)
                if cell.avg_xi > threshold:
                    cell.is_interesting = True
                    interesting_count += 1
        
        logger.info(f"Marked {interesting_count} cells as interesting (xi > {threshold})")
        return interesting_count
    
    def refine_interesting_cells(self, fine_res=FINE_RES_PER_CELL):
        """Subdivide interesting cells for higher resolution"""
        new_points = []
        
        for cell in self.cells:
            if not cell.is_interesting or cell.level >= REFINE_DEPTH:
                continue
            
            logger.info(f"Refining cell at level {cell.level}: "
                       f"m=[{cell.m_min:.3f},{cell.m_max:.3f}], "
                       f"lambda=[{cell.l_min:.3f},{cell.l_max:.3f}] "
                       f"(avg xi={cell.avg_xi:.4f})")
            
            # Subdivide
            subcells = cell.subdivide(fine_res)
            self.cells.extend(subcells)
            
            # Create points for subcells
            for subcell in subcells:
                m_c, l_c = subcell.center()
                point = SimulationPoint(m_sq=m_c, lambda_4=l_c, cell=subcell)
                
                # Only add if not already computed
                h = hash(point)
                if h not in self.all_points:
                    subcell.points.append(point)
                    self.all_points[h] = point
                    new_points.append(point)
                    self.points_by_level[subcell.level] = \
                        self.points_by_level.get(subcell.level, 0) + 1
        
        logger.info(f"Refinement created {len(new_points)} new points to evaluate")
        return new_points
    
    def get_work_queue(self) -> List[SimulationPoint]:
        """Get list of unevaluated points"""
        queue = []
        for point in self.all_points.values():
            h = hash(point)
            if h not in self.completed_points:
                if point.error is None or point.attempts < RETRY_ATTEMPTS:
                    queue.append(point)
        return queue
    
    def analyze_for_ratios(self) -> List[dict]:
        """Find parameter sets that give target stiffness ratios"""
        # Get all valid points
        valid_points = [p for p in self.all_points.values() 
                       if p.error is None and p.xi > 0.2]
        
        if len(valid_points) < 3:
            logger.warning("Not enough valid points for ratio analysis")
            return []
        
        # Sort by xi
        valid_points.sort(key=lambda p: p.xi)
        
        logger.info(f"\nAnalyzing {len(valid_points)} valid points for SM ratios...")
        logger.info(f"Xi range: {valid_points[0].xi:.4f} to {valid_points[-1].xi:.4f}")
        
        candidates = []
        
        # For each point as potential SU(3) base
        for base in valid_points:
            xi_3 = base.xi
            target_xi_2 = xi_3 * TARGET_RATIO_1  # SU(2) target
            target_xi_1 = xi_3 * TARGET_RATIO_2  # U(1) target
            
            # Find matches within tolerance
            matches_2 = [p for p in valid_points 
                        if abs(p.xi - target_xi_2) / target_xi_2 < RATIO_TOLERANCE]
            matches_1 = [p for p in valid_points 
                        if abs(p.xi - target_xi_1) / target_xi_1 < RATIO_TOLERANCE]
            
            if matches_2 and matches_1:
                # Pick closest match
                best_2 = min(matches_2, key=lambda p: abs(p.xi - target_xi_2))
                best_1 = min(matches_1, key=lambda p: abs(p.xi - target_xi_1))
                
                candidates.append({
                    'SU3': base,
                    'SU2': best_2,
                    'U1': best_1,
                    'ratio_2': best_2.xi / base.xi,
                    'ratio_1': best_1.xi / base.xi,
                    'quality': (abs(best_2.xi/base.xi - TARGET_RATIO_1) + 
                               abs(best_1.xi/base.xi - TARGET_RATIO_2))
                })
        
        # Sort by quality (lower is better)
        candidates.sort(key=lambda c: c['quality'])
        
        logger.info(f"\nFound {len(candidates)} candidate triplets!")
        
        if candidates:
            logger.info("\n=== TOP 3 CANDIDATES ===")
            for i, c in enumerate(candidates[:3]):
                logger.info(f"\nCandidate {i+1} (quality score: {c['quality']:.4f}):")
                logger.info(f"  SU(3): xi={c['SU3'].xi:.4f} at m^2={c['SU3'].m_sq:.3f}, lambda={c['SU3'].lambda_4:.3f}")
                logger.info(f"  SU(2): xi={c['SU2'].xi:.4f} at m^2={c['SU2'].m_sq:.3f}, lambda={c['SU2'].lambda_4:.3f}")
                logger.info(f"         => Ratio: {c['ratio_2']:.3f} (target: {TARGET_RATIO_1:.3f})")
                logger.info(f"  U(1):  xi={c['U1'].xi:.4f} at m^2={c['U1'].m_sq:.3f}, lambda={c['U1'].lambda_4:.3f}")
                logger.info(f"         => Ratio: {c['ratio_1']:.3f} (target: {TARGET_RATIO_2:.3f})")
        
        return candidates

class AdaptiveSimulationManager:
    """Manager for adaptive scanning simulation"""
    
    def __init__(self, m_range=(-1.2, 0.0), l_range=(1.0, 5.0)):
        self.scanner = AdaptiveScanner(m_range, l_range)
        self.start_time = time.time()
        
    def process_point(self, point: SimulationPoint) -> SimulationPoint:
        """Process single point - ASCII safe logging"""
        lat = None
        try:
            # Memory check
            mem = psutil.virtual_memory()
            while mem.percent > MAX_MEMORY_PERCENT:
                logger.warning(f"High memory: {mem.percent:.1f}%, waiting...")
                time.sleep(5)
                gc.collect()
                mem = psutil.virtual_memory()
            
            logger.info(f"Processing: m^2={point.m_sq:.4f}, lambda={point.lambda_4:.4f}")
            
            lat = PirouetteLattice(LATTICE_SIZE, point.m_sq, point.lambda_4)
            lat.update(N_THERM)
            
            xi_vals = []
            for meas in range(N_MEAS):
                lat.update(N_DECORR)
                xi = lat.measure_correlation_stiffness()
                if not np.isnan(xi) and xi > 0:
                    xi_vals.append(xi)
                
                if meas % 20 == 0:
                    gc.collect()
            
            if xi_vals:
                point.xi = float(np.mean(xi_vals))
                logger.info(f"  => xi = {point.xi:.4f}")
            else:
                point.xi = 0.0
                logger.warning(f"  => No valid measurements")
            
            point.error = None
            return point
            
        except Exception as e:
            error_msg = f"{type(e).__name__}: {str(e)}"
            point.error = error_msg
            logger.error(f"  => Failed: {error_msg}")
            return point
        
        finally:
            if lat is not None:
                lat.cleanup()
            gc.collect()
            time.sleep(0.1)
    
    def process_batch(self, points: List[SimulationPoint]) -> List[SimulationPoint]:
        """Process batch of points"""
        results = []
        for point in points:
            result = self.process_point(point)
            results.append(result)
        return results
    
    def save_checkpoint(self):
        """Save current state"""
        try:
            data = {
                'scanner': self.scanner,
                'timestamp': time.time(),
                'config': {
                    'L': LATTICE_SIZE,
                    'COARSE_RES': COARSE_RES,
                    'FINE_RES': FINE_RES_PER_CELL,
                    'REFINE_DEPTH': REFINE_DEPTH
                }
            }
            
            temp_file = CHECKPOINT_FILE + '.tmp'
            with open(temp_file, 'wb') as f:
                pickle.dump(data, f)
            os.replace(temp_file, CHECKPOINT_FILE)
            
            logger.info(f"Checkpoint saved: {len(self.scanner.completed_points)} points complete")
            
        except Exception as e:
            logger.error(f"Failed to save checkpoint: {e}")
    
    def load_checkpoint(self):
        """Load saved state"""
        if os.path.exists(CHECKPOINT_FILE):
            logger.info(f"Loading checkpoint: {CHECKPOINT_FILE}")
            try:
                with open(CHECKPOINT_FILE, 'rb') as f:
                    data = pickle.load(f)
                
                self.scanner = data['scanner']
                logger.info(f"Resumed: {len(self.scanner.completed_points)} points completed")
                
            except Exception as e:
                logger.error(f"Corrupt checkpoint: {e}. Starting fresh.")
    
    def run(self):
        """Main adaptive scanning loop"""
        logger.info("=" * 70)
        logger.info("ADAPTIVE PIROUETTE SCANNING FOR GAUGE COUPLING VALIDATION")
        logger.info("=" * 70)
        logger.info(f"Strategy: Coarse {COARSE_RES}x{COARSE_RES} grid, then refine interesting regions")
        logger.info(f"Target ratios: 1:{TARGET_RATIO_1:.2f}:{TARGET_RATIO_2:.2f}")
        logger.info("=" * 70)
        
        # Phase 1: Coarse grid
        if len(self.scanner.cells) == 0:
            logger.info("\n=== PHASE 1: COARSE GRID ===")
            self.scanner.initialize_coarse_grid(COARSE_RES)
        
        # Process coarse grid
        work_queue = self.scanner.get_work_queue()
        if work_queue:
            logger.info(f"\nProcessing {len(work_queue)} coarse grid points...")
            for batch_start in range(0, len(work_queue), BATCH_SIZE):
                batch = work_queue[batch_start:batch_start + BATCH_SIZE]
                results = self.process_batch(batch)
                
                for point in results:
                    self.scanner.completed_points.add(hash(point))
                
                if (batch_start // BATCH_SIZE) % 5 == 0:
                    self.save_checkpoint()
                
                logger.info(f"Progress: {len(self.scanner.completed_points)}/{len(self.scanner.all_points)}")
            
            self.save_checkpoint()
        
        # Phase 2+: Adaptive refinement
        for refinement_level in range(1, REFINE_DEPTH + 1):
            logger.info(f"\n=== PHASE {refinement_level + 1}: REFINEMENT LEVEL {refinement_level} ===")
            
            # Find interesting cells
            interesting = self.scanner.mark_interesting_cells()
            if interesting == 0:
                logger.info("No interesting cells to refine!")
                break
            
            # Refine them
            new_points = self.scanner.refine_interesting_cells()
            if not new_points:
                logger.info("No new points created!")
                break
            
            # Process new points
            logger.info(f"Processing {len(new_points)} refined points...")
            for batch_start in range(0, len(new_points), BATCH_SIZE):
                batch = new_points[batch_start:batch_start + BATCH_SIZE]
                results = self.process_batch(batch)
                
                for point in results:
                    self.scanner.completed_points.add(hash(point))
                
                if (batch_start // BATCH_SIZE) % 5 == 0:
                    self.save_checkpoint()
                
                logger.info(f"Progress: {len(self.scanner.completed_points)}/{len(self.scanner.all_points)}")
            
            self.save_checkpoint()
        
        # Final analysis
        logger.info("\n" + "=" * 70)
        logger.info("SCANNING COMPLETE - ANALYZING RESULTS")
        logger.info("=" * 70)
        
        # Print statistics
        logger.info(f"\nTotal points evaluated: {len(self.scanner.completed_points)}")
        for level, count in self.scanner.points_by_level.items():
            logger.info(f"  Level {level}: {count} points")
        
        elapsed = time.time() - self.start_time
        logger.info(f"\nTotal time: {elapsed/3600:.2f} hours")
        logger.info(f"Avg per point: {elapsed/len(self.scanner.completed_points):.1f} seconds")
        
        # Ratio analysis
        candidates = self.scanner.analyze_for_ratios()
        
        # Visualize
        self.plot_results(candidates)
        
        return candidates
    
    def plot_results(self, candidates):
        """Create visualization with adaptive grid overlay"""
        try:
            # Prepare data
            points = [p for p in self.scanner.all_points.values() if p.error is None]
            
            if not points:
                logger.warning("No points to plot!")
                return
            
            # Create scatter plot colored by refinement level
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
            
            # Plot 1: Stiffness map with refinement levels
            for level in [0, 1, 2]:
                level_points = [p for p in points if p.cell and p.cell.level == level]
                if level_points:
                    m_vals = [p.m_sq for p in level_points]
                    l_vals = [p.lambda_4 for p in level_points]
                    xi_vals = [p.xi for p in level_points]
                    
                    sizes = [20, 40, 80][level]  # Larger markers for refined points
                    scatter = ax1.scatter(l_vals, m_vals, c=xi_vals, s=sizes,
                                         cmap='viridis', alpha=0.7,
                                         label=f'Level {level}')
            
            ax1.set_xlabel('Coupling lambda_4')
            ax1.set_ylabel('Mass Squared m^2')
            ax1.set_title('Adaptive Stiffness Map (marker size = refinement level)')
            ax1.legend()
            plt.colorbar(scatter, ax=ax1, label='Stiffness xi')
            
            # Mark candidates if found
            if candidates:
                best = candidates[0]
                ax1.scatter(best['SU3'].lambda_4, best['SU3'].m_sq, 
                           c='red', marker='x', s=200, linewidths=3, label='SU(3)')
                ax1.scatter(best['SU2'].lambda_4, best['SU2'].m_sq,
                           c='orange', marker='x', s=200, linewidths=3, label='SU(2)')
                ax1.scatter(best['U1'].lambda_4, best['U1'].m_sq,
                           c='white', marker='x', s=200, linewidths=3, label='U(1)')
                ax1.legend()
            
            # Plot 2: Histogram of xi values
            xi_vals = [p.xi for p in points if p.xi > 0]
            ax2.hist(xi_vals, bins=50, alpha=0.7, edgecolor='black')
            ax2.set_xlabel('Stiffness xi')
            ax2.set_ylabel('Count')
            ax2.set_title(f'Distribution (n={len(xi_vals)} points)')
            ax2.set_yscale('log')
            
            # Mark target ratios
            if xi_vals:
                base_xi = np.median([p.xi for p in points if p.xi > 0.5])
                ax2.axvline(base_xi, color='red', linestyle='--', alpha=0.5, label='Base')
                ax2.axvline(base_xi * TARGET_RATIO_1, color='orange', linestyle='--', alpha=0.5, label=f'x{TARGET_RATIO_1:.2f}')
                ax2.axvline(base_xi * TARGET_RATIO_2, color='yellow', linestyle='--', alpha=0.5, label=f'x{TARGET_RATIO_2:.2f}')
                ax2.legend()
            
            plt.tight_layout()
            plt.savefig('adaptive_pirouette_results.png', dpi=150)
            logger.info("Saved plot: adaptive_pirouette_results.png")
            plt.show()
            
        except Exception as e:
            logger.error(f"Plotting failed: {e}")

if __name__ == "__main__":
    sim = AdaptiveSimulationManager()
    sim.load_checkpoint()
    candidates = sim.run()
    
    if candidates:
        print("\n" + "="*70)
        print("SUCCESS! Found gauge coupling candidates!")
        print("="*70)
    else:
        print("\n" + "="*70)
        print("No candidates found. May need:")
        print("  1. Wider parameter range")
        print("  2. More refinement levels")
        print("  3. Lower threshold for interesting regions")
        print("="*70)
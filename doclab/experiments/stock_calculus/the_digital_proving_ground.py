# INSTRUMENT: The Digital Proving Ground
# id: INST-EMERGENCE-ANALYZER-001
# version: 1.0
# parents: [DOMA-207, DOMA-042]
#
# ABSTRACT: This instrument runs a Conway's Game of Life simulation and analyzes
# the emergent "actors" (contiguous cell clusters) by mapping them onto the
# phase-space defined in DOMA-207. It calculates each actor's intrinsic dynamic
# character (kappa) and its performance, revealing the spontaneous emergence
# of Weavers, Gladiators, Drifters, and Vortices. It includes a "selection
# pressure" mode to simulate a competitive environment, demonstrating how such
# forces can shift the ecosystem's distribution towards higher performance archetypes.

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import label
from matplotlib.colors import LogNorm
import argparse
from tqdm import tqdm

def update_grid(grid):
    """
    Performs one iteration of Conway's Game of Life with periodic boundary conditions.
    """
    # Create a padded grid to handle boundary conditions smoothly
    padded_grid = np.pad(grid, 1, mode='wrap')
    
    # Calculate the number of live neighbors for each cell
    neighbors = (padded_grid[1:-1, :-2] + padded_grid[1:-1, 2:] +  # Left, Right
                 padded_grid[:-2, 1:-1] + padded_grid[2:, 1:-1] +  # Top, Bottom
                 padded_grid[:-2, :-2] + padded_grid[:-2, 2:] +    # Diagonals
                 padded_grid[2:, :-2] + padded_grid[2:, 2:])

    # Apply Game of Life rules
    # 1. A living cell with 2 or 3 live neighbors survives.
    survivors = grid & ((neighbors == 2) | (neighbors == 3))
    # 2. A dead cell with exactly 3 live neighbors becomes a live cell.
    births = ~grid & (neighbors == 3)
    
    return survivors | births

def analyze_actors(history_window, current_grid):
    """
    Analyzes actors at the end of a window, collects their metrics.
    An actor is a contiguous cluster of cells.
    """
    actor_metrics = []
    
    # Identify actors in the current grid
    labeled_array, num_features = label(current_grid)
    
    if num_features == 0:
        return []

    # Get the grid state from the start of the analysis window
    start_grid = history_window[0]

    for actor_id in range(1, num_features + 1):
        # Create a mask for the current actor
        actor_mask = (labeled_array == actor_id)
        mass_end = np.sum(actor_mask)
        
        # Heuristic to find the actor's ancestor: check for overlap.
        # This works well for stable or slow-moving actors.
        mass_start = np.sum(start_grid[actor_mask])

        # Ignore trivial actors (mass < 4 is generally unstable dust)
        if mass_start < 4:
            continue

        # Performance Score: Normalized net change in mass over the window.
        # A small epsilon prevents division by zero for new actors.
        performance = (mass_end - mass_start) / (mass_start + 1e-9)

        # Intrinsic Kappa: Sum of all state changes (births + deaths)
        # within the actor's final area over the window.
        churn = 0
        for step in range(len(history_window) - 1):
            # Calculate changes between consecutive steps
            changes = np.abs(history_window[step+1] - history_window[step])
            # Only count changes occurring within the actor's final mask
            churn += np.sum(changes[actor_mask])
        
        # Normalize kappa by window length and initial mass
        intrinsic_kappa = churn / (len(history_window) * (mass_start + 1e-9))
        
        # Clip values to keep the plot readable and avoid extreme outliers
        performance_clipped = np.clip(performance, -2, 2)
        kappa_clipped = np.clip(intrinsic_kappa, 0, 2)
        
        actor_metrics.append({
            'kappa': kappa_clipped, 
            'performance': performance_clipped, 
            'mass': mass_end
        })
        
    return actor_metrics

def apply_selection_pressure(grid, metrics, threshold):
    """
    Returns a new grid where underperforming actors have been culled.
    """
    grid_to_cull = grid.copy()
    labeled_array, num_features = label(grid)

    actor_performance = {i+1: m['performance'] for i, m in enumerate(metrics)}

    for actor_id in range(1, num_features + 1):
        if actor_performance.get(actor_id, threshold + 1) < threshold:
            grid_to_cull[labeled_array == actor_id] = 0
            
    return grid_to_cull

def plot_phase_space(metrics, selection_threshold=None):
    """
    Generates and saves the phase-space plot.
    """
    if not metrics:
        print("No dynamic actors were found to plot.")
        return

    kappas = [m['kappa'] for m in metrics]
    performances = [m['performance'] for m in metrics]
    masses = [m['mass'] for m in metrics]

    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(12, 12))

    sc = ax.scatter(performances, kappas, c=masses, s=(np.array(masses)*1.5 + 10), 
                    cmap='viridis', norm=LogNorm(), alpha=0.75, edgecolors='none')
    
    # Determine plot limits dynamically
    perf_max = np.percentile(np.abs(performances), 98) if performances else 1.5
    kappa_max = np.percentile(kappas, 98) if kappas else 1.5
    ax.set_xlim(-perf_max, perf_max)
    ax.set_ylim(-kappa_max * 0.05, kappa_max * 1.05)
    
    # Quadrant reference lines
    ax.axhline(0, color='grey', linestyle='--', linewidth=1)
    ax.axvline(0, color='grey', linestyle='--', linewidth=1)
    
    # Quadrant Labels
    plt.text(0.95, 0.95, 'Weaver', ha='right', va='top', transform=ax.transAxes, color='lightgreen', fontsize=14, weight='bold')
    plt.text(0.95, 0.05, 'Gladiator', ha='right', va='bottom', transform=ax.transAxes, color='cyan', fontsize=14, weight='bold')
    plt.text(0.05, 0.05, 'Drifter', ha='left', va='bottom', transform=ax.transAxes, color='orange', fontsize=14, weight='bold')
    plt.text(0.05, 0.95, 'Vortex', ha='left', va='top', transform=ax.transAxes, color='tomato', fontsize=14, weight='bold')

    ax.set_xlabel('Performance Score (Net Mass Change)', fontsize=12)
    ax.set_ylabel('Intrinsic Κappa (Internal Churn / Mass)', fontsize=12)
    
    title = 'Game of Life: Phase-Space of Emergent Actors'
    filename = 'game_of_life_natural_phase_space.png'
    
    if selection_threshold is not None:
        ax.axvline(x=selection_threshold, color='red', linestyle=':', linewidth=2, label=f'Selection Threshold ({selection_threshold})')
        ax.legend()
        title = f'{title}\n(with Selection Pressure)'
        filename = 'game_of_life_selection_phase_space.png'

    ax.set_title(title, fontsize=16, weight='bold')
    
    cbar = plt.colorbar(sc)
    cbar.set_label('Actor Mass (Number of Cells)', fontsize=12)
    
    plt.grid(True, linestyle=':', alpha=0.3)
    fig.tight_layout()
    plt.savefig(filename)
    print(f"\nPhase-space plot saved as '{filename}'")

def main():
    parser = argparse.ArgumentParser(description="Run a Game of Life simulation and analyze its emergent actors.")
    parser.add_argument('--grid_size', type=int, default=150, help='Size of the simulation grid (N x N).')
    parser.add_argument('--steps', type=int, default=500, help='Total number of simulation steps.')
    parser.add_argument('--density', type=float, default=0.35, help='Initial density of live cells (0.0 to 1.0).')
    parser.add_argument('--window', type=int, default=50, help='Analysis window size in steps.')
    parser.add_argument('--selection', type=float, default=None, help='Enable selection pressure. Provide a performance threshold (e.g., 0.01) to cull underperformers.')
    parser.add_argument('--seed', type=int, default=42, help='Random seed for reproducibility.')
    args = parser.parse_args()

    np.random.seed(args.seed)
    grid = np.random.choice([0, 1], size=(args.grid_size, args.grid_size), p=[1 - args.density, args.density])
    
    history = [grid.copy()]
    all_metrics = []

    print("Starting simulation...")
    for step in tqdm(range(args.steps), desc="Simulating"):
        grid = update_grid(grid)
        history.append(grid.copy())
        
        # Keep the history buffer at the desired window size
        if len(history) > args.window:
            history.pop(0)
            
            # Analyze at the end of each window
            metrics_this_window = analyze_actors(history, grid)
            if metrics_this_window:
                all_metrics.extend(metrics_this_window)

            # Apply selection pressure if enabled, at the end of each analysis window
            if args.selection is not None:
                grid = apply_selection_pressure(grid, metrics_this_window, args.selection)
                # After culling, reset the history to restart the analysis window
                history = [grid.copy()] # <-- THE FIX IS HERE

    print(f"\nSimulation finished. Analyzed {len(all_metrics)} actor-windows.")
    plot_phase_space(all_metrics, args.selection)

if __name__ == '__main__':
    main()

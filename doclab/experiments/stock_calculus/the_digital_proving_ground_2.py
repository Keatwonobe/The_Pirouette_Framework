# INSTRUMENT: The Digital Proving Ground
# id: INST-EMERGENCE-ANALYZER-001
# version: 2.1
# parents: [DOMA-207, DOMA-042]
#
# ABSTRACT: This instrument runs a Conway's Game of Life simulation and analyzes
# the emergent "actors". Version 2.1 corrects a bug in the selection pressure
# mechanism to ensure accurate culling of underperforming actors in the feedback
# model. This refinement allows for a more precise study of how environmental
# pressures shape the distribution of archetypes in a complex, self-influencing system.

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import label
from matplotlib.colors import LogNorm
import argparse
from tqdm import tqdm

# --- Model Parameters ---
# These can be tweaked to explore different dynamics
GROWTH_RATE = 0.15
DECAY_RATE = 0.15
MAX_HEALTH = 2.0
DEATH_THRESHOLD = 0.1

def update_grid_binary(grid):
    """
    Performs one iteration of Conway's Game of Life with periodic boundary conditions.
    """
    padded_grid = np.pad(grid, 1, mode='wrap')
    neighbors = (padded_grid[1:-1, :-2] + padded_grid[1:-1, 2:] +
                 padded_grid[:-2, 1:-1] + padded_grid[2:, 1:-1] +
                 padded_grid[:-2, :-2] + padded_grid[:-2, 2:] +
                 padded_grid[2:, :-2] + padded_grid[2:, 2:])
    survivors = grid & ((neighbors == 2) | (neighbors == 3))
    births = ~grid & (neighbors == 3)
    return survivors | births

def update_grid_feedback(grid):
    """
    Performs one iteration of the "Game of Complex Life" with health feedback.
    The grid contains float values representing cell health.
    """
    new_grid = grid.copy()
    padded_grid = np.pad(grid, 1, mode='wrap')
    
    # Binarize for neighbor counting
    is_alive_padded = padded_grid > 0
    
    neighbors = (is_alive_padded[1:-1, :-2] + is_alive_padded[1:-1, 2:] +
                 is_alive_padded[:-2, 1:-1] + is_alive_padded[2:, 1:-1] +
                 is_alive_padded[:-2, :-2] + is_alive_padded[:-2, 2:] +
                 is_alive_padded[2:, :-2] + is_alive_padded[2:, 2:])

    # --- Apply rules for existing cells ---
    is_alive = grid > 0
    # Stress conditions: isolation or overcrowding
    under_stress = is_alive & ((neighbors < 2) | (neighbors > 3))
    # Stability condition: coherence
    is_stable = is_alive & ((neighbors == 2) | (neighbors == 3))
    
    new_grid[under_stress] -= DECAY_RATE
    new_grid[is_stable] += GROWTH_RATE
    
    # --- Apply rules for births ---
    can_be_born = (grid == 0) & (neighbors == 3)
    if np.any(can_be_born):
        # Find the parents and calculate the investment
        parent_coords = np.argwhere(can_be_born)
        for i, j in parent_coords:
            # Sum the health of the 8 neighbors, only 3 of which are parents
            parent_health_sum = (padded_grid[i, j] + padded_grid[i, j+1] + padded_grid[i, j+2] +
                                 padded_grid[i+1, j] + padded_grid[i+1, j+2] +
                                 padded_grid[i+2, j] + padded_grid[i+2, j+1] + padded_grid[i+2, j+2])
            new_grid[i, j] = parent_health_sum / 3.0 # Birth with inherited health

    # Enforce health limits
    new_grid = np.clip(new_grid, 0, MAX_HEALTH)
    new_grid[new_grid < DEATH_THRESHOLD] = 0 # Cells with too low health die
    
    return new_grid

def analyze_actors(history_window, current_grid, is_feedback_model):
    """
    Analyzes actors at the end of a window, collecting their metrics.
    """
    actor_metrics = []
    
    is_alive_current = current_grid > 0
    labeled_array, num_features = label(is_alive_current)
    
    if num_features == 0:
        return [], None

    start_grid = history_window[0]
    is_alive_start = start_grid > 0

    for actor_id in range(1, num_features + 1):
        actor_mask = (labeled_array == actor_id)
        mass_end = np.sum(actor_mask)
        
        # Heuristic: find ancestor by overlap
        mass_start = np.sum(is_alive_start[actor_mask])
        if mass_start < 4: continue

        performance = (mass_end - mass_start) / (mass_start + 1e-9)
        
        # --- Kappa Calculation ---
        structural_churn = 0
        health_churn = 0
        for step in range(len(history_window) - 1):
            grid_t0 = history_window[step]
            grid_t1 = history_window[step+1]
            
            # Structural churn: Births and deaths
            structural_changes = np.abs((grid_t1 > 0).astype(int) - (grid_t0 > 0).astype(int))
            structural_churn += np.sum(structural_changes[actor_mask])
            
            # Health churn (only in feedback model)
            if is_feedback_model:
                health_changes = np.abs(grid_t1 - grid_t0)
                health_churn += np.sum(health_changes[actor_mask])

        total_churn = structural_churn + health_churn
        intrinsic_kappa = total_churn / (len(history_window) * (mass_start + 1e-9))
        
        performance_clipped = np.clip(performance, -2, 2)
        kappa_clipped = np.clip(intrinsic_kappa, 0, 2)
        
        actor_metrics.append({
            'id': actor_id,  # FIX: Add actor_id to the metric dictionary
            'kappa': kappa_clipped, 'performance': performance_clipped, 'mass': mass_end
        })
        
    return actor_metrics, labeled_array

def apply_selection_pressure(grid, metrics, labeled_array, threshold):
    """
    Returns a new grid where underperforming actors have been culled.
    """
    if labeled_array is None or not metrics: return grid
    
    grid_to_cull = grid.copy()
    
    # FIX: Use the 'id' from the metric to ensure we cull the correct actor
    for m in metrics:
        if m['performance'] < threshold:
            actor_id_to_cull = m['id']
            grid_to_cull[labeled_array == actor_id_to_cull] = 0
            
    return grid_to_cull

def plot_phase_space(metrics, selection_threshold=None, is_feedback_model=False):
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
    
    perf_max = np.percentile(np.abs(performances), 98) if performances else 1.5
    kappa_max = np.percentile(kappas, 98) if kappas else 1.5
    ax.set_xlim(-perf_max, perf_max)
    ax.set_ylim(-kappa_max * 0.05, kappa_max * 1.05)
    
    ax.axhline(0, color='grey', linestyle='--', linewidth=1)
    ax.axvline(0, color='grey', linestyle='--', linewidth=1)
    
    plt.text(0.95, 0.95, 'Weaver', ha='right', va='top', transform=ax.transAxes, color='lightgreen', fontsize=14, weight='bold')
    plt.text(0.95, 0.05, 'Gladiator', ha='right', va='bottom', transform=ax.transAxes, color='cyan', fontsize=14, weight='bold')
    plt.text(0.05, 0.05, 'Drifter', ha='left', va='bottom', transform=ax.transAxes, color='orange', fontsize=14, weight='bold')
    plt.text(0.05, 0.95, 'Vortex', ha='left', va='top', transform=ax.transAxes, color='tomato', fontsize=14, weight='bold')

    ax.set_xlabel('Performance Score (Net Mass Change)', fontsize=12)
    ax.set_ylabel('Intrinsic Κappa (Total Churn / Mass)', fontsize=12)
    
    model_name = "Feedback Model" if is_feedback_model else "Binary Model"
    title = f'Game of Life Phase-Space: {model_name}'
    filename = f'GoL_{"Feedback" if is_feedback_model else "Binary"}_'
    
    if selection_threshold is not None:
        ax.axvline(x=selection_threshold, color='red', linestyle=':', linewidth=2, label=f'Selection Threshold ({selection_threshold})')
        ax.legend()
        title += ' (with Selection)'
        filename += 'Selection.png'
    else:
        filename += 'Natural.png'

    ax.set_title(title, fontsize=16, weight='bold')
    cbar = plt.colorbar(sc)
    cbar.set_label('Actor Mass (Number of Cells)', fontsize=12)
    plt.grid(True, linestyle=':', alpha=0.3)
    fig.tight_layout()
    plt.savefig(filename)
    print(f"\nPhase-space plot saved as '{filename}'")

def main():
    parser = argparse.ArgumentParser(description="Run a Game of Life simulation and analyze its emergent actors.")
    parser.add_argument('--grid_size', type=int, default=150)
    parser.add_argument('--steps', type=int, default=500)
    parser.add_argument('--density', type=float, default=0.35)
    parser.add_argument('--window', type=int, default=50)
    parser.add_argument('--selection', type=float, default=None, help='Enable selection. Provide a performance threshold (e.g., 0.01).')
    parser.add_argument('--feedback', action='store_true', help='Use the health feedback model instead of the binary model.')
    parser.add_argument('--seed', type=int, default=42)
    args = parser.parse_args()

    np.random.seed(args.seed)
    if args.feedback:
        grid = np.random.choice([0, 1.0], size=(args.grid_size, args.grid_size), p=[1 - args.density, args.density])
        update_func = update_grid_feedback
    else:
        grid = np.random.choice([0, 1], size=(args.grid_size, args.grid_size), p=[1 - args.density, args.density]).astype(bool)
        update_func = update_grid_binary
    
    history = [grid.copy()]
    all_metrics = []

    print(f"Starting simulation with {'Feedback Model' if args.feedback else 'Binary Model'}...")
    for _ in tqdm(range(args.steps), desc="Simulating"):
        grid = update_func(grid)
        history.append(grid.copy())
        
        if len(history) > args.window:
            history.pop(0)
            metrics, labeled_array = analyze_actors(history, grid, args.feedback)
            if metrics: all_metrics.extend(metrics)

            if args.selection is not None:
                grid = apply_selection_pressure(grid, metrics, labeled_array, args.selection)
                history = [grid.copy() for _ in range(args.window)]

    print(f"\nSimulation finished. Analyzed {len(all_metrics)} actor-windows.")
    plot_phase_space(all_metrics, args.selection, args.feedback)

if __name__ == '__main__':
    main()


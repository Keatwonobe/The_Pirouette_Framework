"""
Visualization Tools for Vagabond

Visualize:
1. Temporal Field (Δ) landscape
2. Dark Residue over time
3. Geodesic map structure
4. Coherence manifold
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
from vagabond import Vagabond, VagabondConfig
import gymnasium as gym


def visualize_delta_field(agent: Vagabond, save_path: str = None):
    """
    Visualize the Δ temporal field as a heatmap.
    Shows which regions have high/low temporal pressure.
    """
    if agent.state_dim != 2:
        print("Δ field visualization only supports 2D state spaces")
        return
    
    # Extract Δ field data
    states = []
    deltas = []
    visits = []
    
    for state_hash, delta_val in agent.temporal_field.field.items():
        # This is simplified - in practice we'd need to reverse the hash
        # For now, we'll sample the actual state space
        pass
    
    # Sample state space
    n_samples = 50
    if hasattr(agent.env.observation_space, 'low'):
        x_min, x_max = agent.env.observation_space.low[0], \
                      agent.env.observation_space.high[0]
        y_min, y_max = agent.env.observation_space.low[1], \
                      agent.env.observation_space.high[1]
    else:
        x_min, x_max = -2, 2
        y_min, y_max = -2, 2
    
    x = np.linspace(x_min, x_max, n_samples)
    y = np.linspace(y_min, y_max, n_samples)
    X, Y = np.meshgrid(x, y)
    
    Z = np.zeros_like(X)
    for i in range(n_samples):
        for j in range(n_samples):
            state = np.array([X[i, j], Y[i, j]])
            if agent.state_dim > 2:
                state = np.concatenate([state, np.zeros(agent.state_dim - 2)])
            state_hash = agent._hash_state(state)
            Z[i, j] = agent.temporal_field.get(state_hash)
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    im = ax.contourf(X, Y, Z, levels=20, cmap='RdYlBu_r')
    ax.contour(X, Y, Z, levels=10, colors='black', alpha=0.3, linewidths=0.5)
    
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Δ (Temporal Pressure)', fontsize=12)
    
    ax.set_xlabel('State Dimension 1', fontsize=12)
    ax.set_ylabel('State Dimension 2', fontsize=12)
    ax.set_title('Temporal Field (Δ) Landscape', fontsize=14, fontweight='bold')
    
    # Highlight low-pressure regions (valleys)
    min_delta = Z.min()
    low_pressure_mask = Z < (min_delta + 0.2 * (Z.max() - min_delta))
    ax.scatter(X[low_pressure_mask], Y[low_pressure_mask], 
              c='green', s=10, alpha=0.5, label='Low Pressure (Easy)')
    
    ax.legend()
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()


def plot_dark_residue_history(agent: Vagabond, save_path: str = None):
    """Plot Dark Residue over training episodes"""
    
    if len(agent.dark_residue_history) == 0:
        print("No Dark Residue history available")
        return
    
    dr_history = list(agent.dark_residue_history)
    episodes = np.arange(len(dr_history))
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    # Raw Dark Residue
    ax1.plot(episodes, dr_history, color='#ef4444', alpha=0.6, linewidth=1)
    ax1.plot(episodes, np.convolve(dr_history, np.ones(10)/10, mode='same'),
            color='#dc2626', linewidth=2, label='Moving Average (10)')
    ax1.set_xlabel('Episode', fontsize=11)
    ax1.set_ylabel('Dark Residue', fontsize=11)
    ax1.set_title('Dark Residue Over Training', fontsize=13, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Cumulative Dark Residue
    cumulative_dr = np.cumsum(dr_history)
    ax2.plot(episodes, cumulative_dr, color='#6366f1', linewidth=2)
    ax2.set_xlabel('Episode', fontsize=11)
    ax2.set_ylabel('Cumulative Dark Residue', fontsize=11)
    ax2.set_title('Cumulative Imbalance', fontsize=13, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()


def visualize_geodesic_map(agent: Vagabond, save_path: str = None):
    """Visualize the geodesic map structure"""
    
    if len(agent.geodesic_map.map) == 0:
        print("No geodesic map entries available")
        return
    
    # Extract data
    dark_residues = []
    visit_counts = []
    
    for state_hash, (action, dr, visits) in agent.geodesic_map.map.items():
        dark_residues.append(dr)
        visit_counts.append(visits)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # DR distribution
    ax1.hist(dark_residues, bins=30, color='#6366f1', alpha=0.7, edgecolor='black')
    ax1.axvline(np.median(dark_residues), color='red', linestyle='--', 
               linewidth=2, label=f'Median: {np.median(dark_residues):.4f}')
    ax1.set_xlabel('Dark Residue', fontsize=11)
    ax1.set_ylabel('Count', fontsize=11)
    ax1.set_title('Distribution of Geodesic Dark Residues', 
                 fontsize=13, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Visit counts vs DR
    ax2.scatter(visit_counts, dark_residues, alpha=0.6, 
               c=dark_residues, cmap='RdYlGn_r', s=50)
    ax2.set_xlabel('Visit Count', fontsize=11)
    ax2.set_ylabel('Dark Residue', fontsize=11)
    ax2.set_title('Geodesic Reinforcement', fontsize=13, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    # Add colorbar
    sm = plt.cm.ScalarMappable(cmap='RdYlGn_r')
    sm.set_array(dark_residues)
    cbar = plt.colorbar(sm, ax=ax2)
    cbar.set_label('Dark Residue', fontsize=10)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()


def plot_coherence_vs_pressure(agent: Vagabond, num_rollouts: int = 10,
                               save_path: str = None):
    """
    Plot K_τ vs V_Γ for rollouts to visualize the coherence-pressure dynamics.
    """
    
    coherences = []
    pressures = []
    dark_residues = []
    
    for _ in range(num_rollouts):
        state, _ = agent.env.reset()
        done = False
        
        while not done:
            action = agent.select_action(state, evaluate=True)
            
            if agent.continuous:
                next_state, reward, terminated, truncated, _ = \
                    agent.env.step(action)
            else:
                action_idx = action if isinstance(action, (int, np.integer)) \
                            else np.argmax(action)
                next_state, reward, terminated, truncated, _ = \
                    agent.env.step(action_idx)
                action = np.array([action_idx], dtype=np.float32)
            
            done = terminated or truncated
            
            state_hash = agent._hash_state(state)
            
            # Compute components
            dr = agent.dark_residue_calc.compute(
                state, action, next_state, reward,
                agent.temporal_field, state_hash
            )
            
            # Extract K_τ and V_Γ (simplified)
            V_gamma = agent.temporal_field.get_temporal_pressure(state_hash)
            K_tau = V_gamma + dr  # Since DR = |K_τ - V_Γ|, approximately
            
            coherences.append(K_tau)
            pressures.append(V_gamma)
            dark_residues.append(dr)
            
            state = next_state
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # K_τ vs V_Γ scatter
    scatter = ax1.scatter(coherences, pressures, c=dark_residues, 
                         cmap='RdYlGn_r', alpha=0.6, s=30)
    ax1.plot([min(coherences + pressures), max(coherences + pressures)],
            [min(coherences + pressures), max(coherences + pressures)],
            'k--', linewidth=2, alpha=0.5, label='K_τ = V_Γ (Perfect Balance)')
    ax1.set_xlabel('K_τ (Temporal Coherence)', fontsize=11)
    ax1.set_ylabel('V_Γ (Temporal Pressure)', fontsize=11)
    ax1.set_title('Coherence-Pressure Phase Space', fontsize=13, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    cbar = plt.colorbar(scatter, ax=ax1)
    cbar.set_label('Dark Residue', fontsize=10)
    
    # Time series
    steps = np.arange(len(coherences))
    ax2.plot(steps, coherences, label='K_τ (Coherence)', 
            color='#6366f1', alpha=0.7, linewidth=1.5)
    ax2.plot(steps, pressures, label='V_Γ (Pressure)',
            color='#ef4444', alpha=0.7, linewidth=1.5)
    ax2.fill_between(steps, coherences, pressures, alpha=0.2, color='gray')
    ax2.set_xlabel('Step', fontsize=11)
    ax2.set_ylabel('Value', fontsize=11)
    ax2.set_title('Coherence vs Pressure Over Time', fontsize=13, fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()


def create_full_dashboard(agent: Vagabond, save_path: str = None):
    """Create comprehensive visualization dashboard"""
    
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    # 1. Dark Residue History
    ax1 = fig.add_subplot(gs[0, :2])
    if len(agent.dark_residue_history) > 0:
        dr_history = list(agent.dark_residue_history)
        episodes = np.arange(len(dr_history))
        ax1.plot(episodes, dr_history, color='#ef4444', alpha=0.6, linewidth=1)
        ax1.plot(episodes, np.convolve(dr_history, np.ones(10)/10, mode='same'),
                color='#dc2626', linewidth=2)
        ax1.set_xlabel('Episode')
        ax1.set_ylabel('Dark Residue')
        ax1.set_title('Dark Residue Over Training', fontweight='bold')
        ax1.grid(True, alpha=0.3)
    
    # 2. Geodesic Map Stats
    ax2 = fig.add_subplot(gs[0, 2])
    if len(agent.geodesic_map.map) > 0:
        dark_residues = [dr for _, (_, dr, _) in agent.geodesic_map.map.items()]
        ax2.hist(dark_residues, bins=20, color='#6366f1', alpha=0.7)
        ax2.set_xlabel('Dark Residue')
        ax2.set_ylabel('Count')
        ax2.set_title('Geodesic DR Dist', fontweight='bold')
        ax2.grid(True, alpha=0.3)
    
    # 3. Temporal Field Statistics
    ax3 = fig.add_subplot(gs[1, 0])
    delta_values = list(agent.temporal_field.field.values())
    if delta_values:
        ax3.hist(delta_values, bins=20, color='#8b5cf6', alpha=0.7)
        ax3.set_xlabel('Δ Value')
        ax3.set_ylabel('Count')
        ax3.set_title('Δ Field Distribution', fontweight='bold')
        ax3.grid(True, alpha=0.3)
    
    # 4. Visit counts
    ax4 = fig.add_subplot(gs[1, 1])
    visit_counts = list(agent.temporal_field.visits.values())
    if visit_counts:
        ax4.hist(visit_counts, bins=20, color='#10b981', alpha=0.7)
        ax4.set_xlabel('Visit Count')
        ax4.set_ylabel('Count')
        ax4.set_title('State Visit Distribution', fontweight='bold')
        ax4.set_yscale('log')
        ax4.grid(True, alpha=0.3)
    
    # 5. Key Metrics
    ax5 = fig.add_subplot(gs[1, 2])
    ax5.axis('off')
    
    metrics_text = f"""
    VAGABOND METRICS
    ───────────────────
    
    Episodes: {agent.episode_count}
    Total Steps: {agent.total_steps:,}
    
    Geodesic Map:
      Entries: {len(agent.geodesic_map.map)}
      Hit Rate: {agent.geodesic_map.get_hit_rate():.1%}
    
    Temporal Field:
      States: {len(agent.temporal_field.field)}
      Avg Δ: {np.mean(delta_values) if delta_values else 0:.4f}
    
    Dark Residue:
      Current: {dr_history[-1] if dr_history else 0:.4f}
      Min: {min(dr_history) if dr_history else 0:.4f}
      Mean: {np.mean(dr_history) if dr_history else 0:.4f}
    """
    
    ax5.text(0.1, 0.5, metrics_text, fontsize=10, family='monospace',
            verticalalignment='center')
    
    # 6. Learning Progress
    ax6 = fig.add_subplot(gs[2, :])
    if len(agent.dark_residue_history) > 10:
        window = 20
        smoothed_dr = np.convolve(dr_history, np.ones(window)/window, mode='valid')
        ax6.plot(smoothed_dr, color='#6366f1', linewidth=2)
        ax6.fill_between(range(len(smoothed_dr)), smoothed_dr, alpha=0.3, 
                        color='#6366f1')
        ax6.set_xlabel('Episode')
        ax6.set_ylabel('Smoothed Dark Residue')
        ax6.set_title('Learning Progress (20-Episode Moving Average)', 
                     fontweight='bold')
        ax6.grid(True, alpha=0.3)
    
    plt.suptitle(f'Vagabond Dashboard - {agent.env.spec.id}', 
                fontsize=16, fontweight='bold', y=0.995)
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()


def main():
    """Demo visualizations"""
    
    print("Training a quick agent for visualization...")
    
    env = gym.make('Pendulum-v1')
    config = VagabondConfig()
    agent = Vagabond(env, config)
    
    # Train for a bit
    for _ in range(1500):
        agent.train_episode()
    
    print("\nCreating visualizations...\n")
    
    # Individual plots
    plot_dark_residue_history(agent, 'dark_residue_history.png')
    visualize_geodesic_map(agent, 'geodesic_map.png')
    plot_coherence_vs_pressure(agent, num_rollouts=5, 
                               save_path='coherence_pressure.png')
    
    # Full dashboard
    create_full_dashboard(agent, 'vagabond_dashboard.png')
    
    print("✅ Visualizations complete!")


if __name__ == "__main__":
    main()
